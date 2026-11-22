"""Lecture 06 glossary and lecture summaries MCP server.

    uv run python -m app.mcp_agent --list-tools
    uv run python -m app.mcp_server --http

The first command lists tools without an API key. The second serves Streamable
HTTP at http://127.0.0.1:8000/mcp.

By default the server waits for input on stdio. MCP clients such as
app.mcp_agent launch it as a subprocess. If run directly, it will wait for input.
The functions registered in Lecture 03 are available through the same protocol
to the learning agent and to other MCP clients.
"""

import argparse

from mcp.server.mcpserver import MCPServer

from app import tools

# Server name and description, shown to clients (distinct from the "glossary" key in the configuration file)
server = MCPServer(
    "aie2026-glossary",
    instructions="Provides the glossary and session key points for AIE2026 (AI Engineering Pilot Course).",
)

# Expose the same function as in Lecture 03 as an MCP tool. Its docstring and type hints become the description
server.tool()(tools.search_glossary)

# TODO(Basic homework): expose get_lecture_summary as well


def main() -> None:
    parser = argparse.ArgumentParser(description="Glossary MCP server")
    parser.add_argument("--http", action="store_true", help="Start with Streamable HTTP (default: stdio)")
    args = parser.parse_args()
    if args.http:
        print("Starting the MCP server at http://127.0.0.1:8000/mcp (Ctrl+C to stop)")
        server.run(transport="streamable-http")
    else:
        # With stdio, standard output carries protocol messages, so do not print to it
        server.run()


if __name__ == "__main__":
    main()
