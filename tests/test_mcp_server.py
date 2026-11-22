"""Lecture 06: MCP server/client wiring tests (no LLM or API key used).

Actually start the glossary server from app/mcp_servers.json (stdio), and use TestModel
to check that tools are exposed through MCP, called, and return results.
"""

import json

import pytest
from pydantic_ai.messages import ToolCallPart, ToolReturnPart
from pydantic_ai.models.test import TestModel

from app.mcp_agent import MCP_CONFIG, ConfigError, build_mcp_agent, describe_servers, read_config

GLOSSARY_TOOL = "glossary_search_glossary"  # Prefixed with the configuration file server name "glossary"


def _glossary_only_config(tmp_path):
    """Use only the glossary server from the configuration (do not start external servers such as fetch added in exercises)."""
    config = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
    assert "glossary" in config["mcpServers"], "app/mcp_servers.json must include a glossary server"
    path = tmp_path / "mcp_servers.json"
    path.write_text(
        json.dumps({"mcpServers": {"glossary": config["mcpServers"]["glossary"]}}), encoding="utf-8"
    )
    return path


def _parts(result, kind):
    return [p for m in result.all_messages() for p in m.parts if isinstance(p, kind)]


def test_glossary_server_exposes_search_tool(tmp_path):
    model = TestModel(call_tools=[])
    build_mcp_agent(_glossary_only_config(tmp_path)).run_sync("Tool list", model=model)

    offered = {t.name for t in model.last_model_request_parameters.function_tools}
    assert GLOSSARY_TOOL in offered  # Check inclusion so adding tools in the exercises does not break the test


def test_glossary_result_comes_back_through_mcp(tmp_path):
    model = TestModel(call_tools=[GLOSSARY_TOOL])
    result = build_mcp_agent(_glossary_only_config(tmp_path)).run_sync("What is LoRA?", model=model)

    assert [p.tool_name for p in _parts(result, ToolCallPart)] == [GLOSSARY_TOOL]
    returns = _parts(result, ToolReturnPart)
    assert returns and returns[0].tool_name == GLOSSARY_TOOL
    assert str(returns[0].content).strip()  # A search result (or a "not found" message) was returned
    assert result.output


def test_describe_servers_tells_command_from_url(tmp_path):
    path = tmp_path / "mcp_servers.json"
    path.write_text(
        json.dumps(
            {
                "mcpServers": {
                    "glossary": {"command": "uv", "args": ["run", "python", "-m", "app.mcp_server"]},
                    "aws": {"url": "https://knowledge-mcp.global.api.aws"},
                }
            }
        ),
        encoding="utf-8",
    )
    assert describe_servers(path) == [
        '[server] glossary: starting with command (uv run python -m app.mcp_server)',
        '[server] aws: connecting to URL (https://knowledge-mcp.global.api.aws)',
    ]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ('{"mcpServers": {"a": {"command": "uv"} "b": {"url": "https://example.com"}}}', 'Invalid\\ JSON\\ near\\ line\\ 1'),
        ('{"servers": {}}', 'Missing\\ "mcpServers"'),
        ('{"mcpServers": {"a": {"args": []}}}', 'Server\\ "a"\\ needs\\ "command"\\ or\\ "url"'),
    ],
)
def test_config_mistakes_are_reported_in_words(tmp_path, text, expected):
    path = tmp_path / "mcp_servers.json"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ConfigError, match=expected):
        read_config(path)
