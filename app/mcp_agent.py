"""Lecture 06 learning support agent and MCP client.

    uv run python -m app.mcp_agent --list-tools
    uv run python -m app.mcp_agent --trace "What is LoRA?"

Lecture 03 registered functions from tools.py directly with the agent. Here the
agent discovers the tools exposed by the servers in app/mcp_servers.json.
The model, loop and tools still work together as in Lecture 03.
"""

import argparse
import inspect
import json
from pathlib import Path

from fastmcp import Client
from mcp.shared.exceptions import MCPError
from pydantic_ai import Agent
from pydantic_ai.exceptions import AgentRunError, ModelHTTPError, UserError
from pydantic_ai.mcp import MCPToolset, StdioTransport
from pydantic_ai.messages import RetryPromptPart, ToolCallPart, ToolReturnPart
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.test import TestModel
from pydantic_ai.providers.google import GoogleProvider

from app.config import MODEL, api_error_message, get_api_key

# Guide the agent's use of the glossary and of other configured servers.
INSTRUCTIONS = """\
You are the learning support agent for the AI Engineering course (AIE2026). Answer in English.
- Check the course glossary with search_glossary before answering questions about terms or the course.
- Use get_lecture_summary when asked about the contents of a lecture.
- If the glossary has no entry, say so and avoid guessing.
- End your answer with the relevant lecture number (Lecture N).
- Give hints about the approach so learners can solve their own homework.
- For topics outside the glossary, such as web pages or AWS documentation, use a suitable tool when available.
"""

# Server configuration in the "mcpServers" format used by Claude Desktop and Cursor.
MCP_CONFIG = Path(__file__).resolve().parent / "mcp_servers.json"


class ConfigError(Exception):
    """An error in the app/mcp_servers.json configuration."""


def read_config(config_path: Path = MCP_CONFIG) -> dict:
    """Return the server names and their settings from the mcpServers object."""
    try:
        config = json.loads(Path(config_path).read_text(encoding="utf-8"))["mcpServers"]
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON near line {e.lineno} ({e.msg})") from e
    except KeyError as e:
        raise ConfigError('Missing "mcpServers"') from e
    for name, spec in config.items():
        if "command" not in spec and "url" not in spec:
            raise ConfigError(f'Server "{name}" needs "command" or "url"')
    return config


def load_mcp_servers(config_path: Path = MCP_CONFIG) -> list[MCPToolset]:
    """Build one MCP toolset for each server in the configuration.

    The command field starts a subprocess over stdio. The url field connects to
    a running server via Streamable HTTP. Prefix tool names with the server name
    so tools with the same name stay distinct.

    Pydantic AI also provides load_mcp_toolsets(). Explicit legacy mode avoids
    automatic detection warnings when connecting to older SDKs such as fetch.
    """
    toolsets = []
    for name, spec in read_config(config_path).items():
        if "url" in spec:
            transport = spec["url"]
        else:
            transport = StdioTransport(spec["command"], spec.get("args", []), env=spec.get("env"))
        toolsets.append(MCPToolset(Client(transport, mode="legacy")).prefixed(name))
    return toolsets


def describe_servers(config_path: Path = MCP_CONFIG) -> list[str]:
    """Describe how each configured server starts or connects."""
    lines = []
    for name, spec in read_config(config_path).items():
        if "url" in spec:
            lines.append(f"[server] {name}: connecting to URL ({spec['url']})")
        else:
            command = " ".join([spec["command"], *spec.get("args", [])])
            lines.append(f"[server] {name}: starting with command ({command})")
    return lines


def build_mcp_agent(config_path: Path = MCP_CONFIG) -> Agent:
    """Build an agent with MCP tools. Supply the model when running it."""
    return Agent(instructions=INSTRUCTIONS, toolsets=load_mcp_servers(config_path))


def build_model() -> GoogleModel:
    return GoogleModel(MODEL, provider=GoogleProvider(api_key=get_api_key()))


def print_tools(target: Agent) -> None:
    """Show tool names, descriptions and arguments using a test model.

    TestModel exposes the tool definitions without calling an LLM.
    """
    model = TestModel(call_tools=[])
    target.run_sync("Tool list", model=model)
    tools_seen = model.last_model_request_parameters.function_tools
    print(f"Tools visible to the model: {len(tools_seen)}")
    for tool in tools_seen:
        print(f"\n[{tool.name}]")
        print("  " + inspect.cleandoc(tool.description or "").replace("\n", "\n  "))
        params = tool.parameters_json_schema.get("properties", {})
        print(f"  Arguments: {json.dumps(params, ensure_ascii=False)}")


def print_trace(result) -> None:
    """Print tool calls, arguments and results."""
    print("\n--- trace ---")
    for message in result.all_messages():
        for part in message.parts:
            if isinstance(part, ToolCallPart):
                print(f"[tool call]   {part.tool_name}({part.args})")
            elif isinstance(part, ToolReturnPart):
                print(f"[tool return] {part.tool_name} -> {str(part.content)[:120]}…")
            elif isinstance(part, RetryPromptPart) and part.tool_name:
                # The model can use this error to decide whether to call the tool again.
                print(f"[tool error]  {part.tool_name} -> {str(part.content)[:120]}")
    usage = result.usage
    print(f"[usage] input {usage.input_tokens:,} tokens / output {usage.output_tokens:,} tokens / model responses {usage.requests}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask the learning support agent a question using MCP tools")
    parser.add_argument("question", nargs="?")
    parser.add_argument("--trace", action="store_true", help="Show tool calls")
    parser.add_argument("--list-tools", action="store_true", help="List tools visible to the model and exit (no API key required)")
    args = parser.parse_args()
    if not args.list_tools and not args.question:
        parser.error("Enter a question")

    try:
        target = build_mcp_agent()
        print("\n".join(describe_servers()))
    except ConfigError as e:
        print(f"Could not read app/mcp_servers.json: {e}")
        print("Check for a comma between servers and for a trailing comma after the last server.")
        raise SystemExit(1)
    try:
        if args.list_tools:
            print_tools(target)
            return
        model = build_model()
        print(f"[model] {MODEL}")
        print(f"[tools] MCP servers ({MCP_CONFIG.relative_to(MCP_CONFIG.parent.parent)})")
        result = target.run_sync(args.question, model=model)
    except ModelHTTPError as e:
        print(api_error_message(e.status_code, str(e.body)[:200]))
        raise SystemExit(1)
    except (AgentRunError, UserError):
        raise  # Show the original agent execution error.
    except (MCPError, RuntimeError, OSError) as e:
        # The server failed to start or connect.
        print(f"Could not connect to an MCP server: {e}")
        print("Check the command or URL for that server in app/mcp_servers.json.")
        raise SystemExit(1)
    print(result.output)
    if args.trace:
        print_trace(result)


if __name__ == "__main__":
    main()
