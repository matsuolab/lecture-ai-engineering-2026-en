# Lecture 06 Exercises and Homework — Use MCP Server Tools from an Agent

## Goals for this session

- Use your own MCP server from an agent with the glossary tool from Lecture 03.
- Display and read the tool names, descriptions, and arguments sent to the model.
- Use MCP servers from other providers by adding them to a configuration file.

Work in GitHub Codespaces on your fork. Use the Gemini API key you registered in Lecture 01.

## Three ways to use an MCP server

Try each of these setups in order.

| | Start your own server | Use a published server | Connect to a remote server |
|---|---|---|---|
| Connection | The agent starts it with a command in your environment | `uvx` downloads and starts it in your environment | The agent connects to a running server |
| Exercise | STEP 1 and 2 (glossary server) | STEP 3 (fetch server) | STEP 4 (AWS Knowledge server) |
| Configuration | `"command": "uv"` | `"command": "uvx"` | `"url": "https://…"` |

Use `command` to start a server in your environment and `url` to connect to a remote server.

## Files for Lecture 06

Edit the configuration file during the exercise. Read or run the other files as needed.

| File | Purpose | What to do |
|---|---|---|
| [app/tools.py](../../app/tools.py) | Function tools, including `search_glossary` and `get_lecture_summary` from Lecture 03 | Read it |
| [app/mcp_server.py](../../app/mcp_server.py) | Exposes functions from `app/tools.py` as MCP tools | Read it. Add one line for the Basic homework |
| [app/mcp_servers.json](../../app/mcp_servers.json) | Configures the MCP servers the agent uses | Add servers in STEP 3 and STEP 4 |
| [app/mcp_agent.py](../../app/mcp_agent.py) | Connects to configured servers and uses their tools | Run it from the terminal |
| [app/agent.py](../../app/agent.py) | The agent used through Lecture 05 | Run it in STEP 1 to list its tools |

## Exercises (30 minutes)

Allow about 23 minutes for setup and STEP 1 through STEP 5.

### Preparation — Create the lec06 branch (about 2 minutes)

1. On your fork's GitHub page, select **Sync fork → Update branch** if an update is available.
2. In the Codespaces terminal, run these commands in order.

```bash
git switch main
git pull --no-rebase
git switch -c lec06
uv sync --frozen
```

3. Run `ls app/mcp_agent.py` and check that the file name appears.

- If `git switch main` stops because you have changes on the previous lecture's branch, commit your work and retry.
- If you see `a branch named 'lec06' already exists`, switch to it with `git switch lec06`.
- If `git pull --no-rebase` reports `CONFLICT`, run `git merge --abort` to keep your changes, then use the instructions below.

#### If you have unfinished work from an earlier lecture

Start from the course repository's current Lecture 06 code. Run the commands below in order.

```bash
git fetch https://github.com/matsuolab/lecture-ai-engineering-2026-en.git main
git switch -c lec06 FETCH_HEAD
uv sync --frozen
```

Use these instructions if Sync fork reports a conflict as well. Keep your commits by leaving **Discard commits** alone.

### STEP 1 — List the tools from your server (about 4 minutes)

Check that the agent starts the glossary server and passes its tools to the model.

```bash
uv run python -m app.agent --list-tools
uv run python -m app.mcp_agent --list-tools
```

Both commands work without an API key.

1. The first command lists tools in the agent used through Lecture 05, including `search_materials`.
2. The first line of the second command shows how the agent started the glossary server. The server's tools appear below it.
3. Compare the lists. Names, descriptions, and arguments reach the model in the same form.

The second command displays this output.

```text
[server] glossary: starting with command (uv run python -m app.mcp_server)
Tools visible to the model: 1

[glossary_search_glossary]
  Search the course glossary and return definitions and the sessions that cover the terms.

  Use before answering about AI engineering terms or words specific to this course (AIE2026).
  Put only one term to look up in query (for example, "LoRA").
  Arguments: {"query": {"title": "Query", "type": "string"}}
```

MCP tool names combine the server name, an underscore, and the tool name. In `glossary_search_glossary`, `glossary` comes from the configuration and `search_glossary` is the function in `app/tools.py`. The prefix distinguishes tools with the same name on different servers.

### STEP 2 — Ask the agent a question and inspect its tool call (about 4 minutes)

Check that the MCP server's tool is called when the agent answers a question.

```bash
uv run python -m app.mcp_agent --trace "What are the three homework levels in the AIE2026 course?"
```

This is the same question as in Lecture 03. Check these lines below `--- trace ---`.

1. `[tool call]` shows `glossary_search_glossary` and the arguments the model chose.
2. `[tool return]` shows the glossary content the MCP server returned.
3. `[usage]` shows at least two model responses. The model calls the tool in one response, then reads the result and answers in the next.

In Lecture 03, the agent called the function directly. Here the MCP server calls the function and returns its result to the agent.

### STEP 3 — Download and use a published server (about 5 minutes)

Add fetch, a server that retrieves web pages, to the configuration and confirm that the agent can use it.

1. Open `app/mcp_servers.json`. Add a comma after the closing brace of `glossary`, then add the four lines for `"fetch"`.

```json
{
  "mcpServers": {
    "glossary": {
      "command": "uv",
      "args": ["run", "python", "-m", "app.mcp_server"]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch==2026.11.11", "--no-readability-js"]
    }
  }
}
```

2. Run the first command. Look for `[server] fetch: starting with command` and `fetch_fetch` in the list.
3. Ask the question with the second command. Check the `[tool call]` line for `fetch_fetch` and its URL.

```bash
uv run python -m app.mcp_agent --list-tools
uv run python -m app.mcp_agent --trace "Summarize the opening of https://modelcontextprotocol.io/ in three lines of English."
```

- `uvx` downloads and runs a published program. The fetch server runs inside your Codespace. The first command takes about 10 seconds on its first run.
- `==2026.11.11` pins the version because updates to external servers can change their behavior.
- `--no-readability-js` tells the server to extract page content with Python alone.
- The description of `fetch_fetch` reaches the model in English, as written by the server's author.

### STEP 4 — Connect to a remote server (about 5 minutes)

Connect by URL to the MCP server hosted by AWS and confirm that the agent can use it.

1. Open `app/mcp_servers.json`. Add a comma after the closing brace of `fetch`, then add the `"aws"` line.

```json
{
  "mcpServers": {
    "glossary": {
      "command": "uv",
      "args": ["run", "python", "-m", "app.mcp_server"]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch==2026.11.11", "--no-readability-js"]
    },
    "aws": {"url": "https://knowledge-mcp.global.api.aws"}
  }
}
```

2. Run the first command. Look for `[server] aws: connecting to URL` and tools with the `aws_` prefix.
3. Ask the question with the second command. Look for an `aws_` tool on the `[tool call]` line.

```bash
uv run python -m app.mcp_agent --list-tools
uv run python -m app.mcp_agent --trace "Search the AWS documentation and explain Amazon S3 versioning in two lines."
```

The first command begins with these three lines.

```text
[server] glossary: starting with command (uv run python -m app.mcp_server)
[server] fetch: starting with command (uvx mcp-server-fetch==2026.11.11 --no-readability-js)
[server] aws: connecting to URL (https://knowledge-mcp.global.api.aws)
```

The AWS server is already running. The agent connects directly to its URL, and the question is sent to AWS.

### What to check before adding external tools

In STEP 3 and STEP 4, you used servers from other providers by adding a few lines to the configuration. Check these two things first.

1. **Who provides the server?** Identify the provider and where its source code lives. The MCP repository provides fetch. AWS provides AWS Knowledge. Add servers whose origin you can verify.
2. **What risks does the server document?** Read the README or official page for warnings and defaults. The fetch README describes security risks from possible access to internal IP addresses. A remote server sends tool inputs to its provider.

The fetch defaults protect internal resources and respect sites' rules on automated retrieval.

| Default behavior | Option |
|---|---|
| Skips private addresses such as `localhost` and internal networks | `--allow-private-ips` permits access to them |
| Skips pages whose site disallows automated retrieval in `robots.txt` | `--ignore-robots-txt` permits access to those pages |
| Fetches other pages from any host | `--allowed-hosts` restricts which hosts it can access |

Review the provider and its documented risks before adding a server, including servers from the MCP repository.

### STEP 5 — Submit and stop Codespaces (about 3 minutes)

Record your results in `answer.md`, open a PR, and stop the Codespace.

1. Open `lectures/06/answer.md`. Paste the tool name from STEP 1 and the original `[tool call]` lines with names and arguments from STEP 2 through STEP 4.
2. Commit and push.

```bash
git add -A
git commit -m "Lecture 06 exercise"
git push -u origin lec06
```

3. In GitHub, open a PR from `lec06` to `main` in your fork. Check that the base repository is your fork.
4. Select **Codespaces** at the bottom left, then **Stop Current Codespace**.

Example entry in `answer.md`.

```text
- Tool name in STEP 1 — glossary_search_glossary
- STEP 2 [tool call] — glossary_search_glossary({'query': '3 levels'})
- STEP 3 [tool call] — fetch_fetch({'url': 'https://…'})
- STEP 4 [tool call] — aws_… (Paste the line as displayed)
```

If you did not finish STEP 4, submit what you completed and push later work to the same branch.

### Troubleshooting

If the issue persists, share the symptom and the displayed message in chat.

| Symptom | What to do |
|---|---|
| `No module named app.mcp_agent` | Update `main` as described in Preparation. Then run `git switch lec06` followed by `git merge main` |
| “Could not read app/mcp_servers.json” | Check for commas between servers and remove any trailing comma after the last server. Start near the line shown in the message |
| “Could not connect to an MCP server” | Check the command name or URL in `app/mcp_servers.json` |
| fetch is skipped for a URL question | Add a line to `INSTRUCTIONS` in `app/mcp_agent.py` telling the agent to use fetch to read supplied URLs |
| The connection fails after adding `aws` | Check the URL. A rate limit may also apply, so wait about a minute and retry |
| Rate limit reached | Wait about a minute and retry the command |
| Missing `GEMINI_API_KEY` | Register it as a Codespaces secret as in Lecture 01 and restart Codespaces |

## Homework (complete one level)

| Level | Task |
|---|---|
| Basic | Expose `get_lecture_summary` on the glossary server by editing `app/mcp_server.py`. Keep the agent as provided. Confirm that the tool appears in the list and is called in response to a question |
| Implementation | Add your own tool to the MCP server. Use `make_quiz` from Lecture 03 or write a new tool. Return a clear message for out-of-range arguments and see how the model receives it |
| Advanced | Use official documentation to find how a tool you use, such as Claude Code, Codex, or Gemini CLI, configures MCP servers. Use VS Code if you have no preference. Compare its configuration with `app/mcp_servers.json` |

### Basic homework

| Side | File |
|---|---|
| Server | Edit `app/mcp_server.py`, which controls which tools the server exposes |
| Agent | Keep `app/mcp_servers.json` and `app/mcp_agent.py` as provided |

1. Open `app/mcp_server.py`. Add the last line in this example underneath the `TODO` comment and save the file.

   ```python
   server.tool()(tools.search_glossary)

   # TODO(Basic homework): expose get_lecture_summary as well
   server.tool()(tools.get_lecture_summary)
   ```

2. Run `git status` and verify that `app/mcp_server.py` is the only modified file after you committed the exercise work in STEP 5.
3. Check that `glossary_get_lecture_summary` appears in the tool list.
4. Ask what Lecture 02 covers and verify that the new tool is called.
5. Run `uv run pytest -q` and confirm that the tests pass.

```bash
git status
uv run python -m app.mcp_agent --list-tools
uv run python -m app.mcp_agent --trace "What will we learn in Lecture 02?"
uv run pytest -q
```

Each time the agent starts, it asks the server for its tools. This is how it discovers the tool you added.

### Implementation homework

1. Expose `make_quiz` from Lecture 03 in `app/mcp_server.py` as in the Basic homework. If you need a new tool, define a function in that file with `@server.tool()` immediately above it.
2. Use `return` to send a clear message when an argument is out of range, such as a lecture number that does not exist.
3. Ask a question with an out-of-range argument and inspect `--trace`.

```bash
uv run python -m app.mcp_agent --trace "Make a quiz for Lecture 99."
```

- A message from `return` appears on the `[tool return]` line and goes to the model.
- An exception from `raise` appears on the `[tool error]` line. Compare what the model receives in each case.

### Advanced homework

1. Choose software you already use, such as Claude Code, Codex, or Gemini CLI. If none applies, choose VS Code. This is a research task you can do using documentation alone.
2. Look up how the software configures MCP servers in its official documentation.
3. Compare it with `app/mcp_servers.json` and record the differences.

| Research question | What to check |
|---|---|
| Where does the configuration go? | File name and location, or the command to register a server |
| How does it start a server with a command? | The equivalent of `"command"` |
| How does it connect by URL? | The equivalent of `"url"` |
| Where does the configuration apply? | One project or all projects |

Record the date you checked and the URL of the official documentation. Configuration instructions may change.

### Submit the homework

In the Homework section of `lectures/06/answer.md`, record the level, what you did, the results, and your observations or questions. Push to the same `lec06` branch. You may use AI tools. Record what you verified yourself.

## References

- [Official MCP site](https://modelcontextprotocol.io/)
- [Pydantic AI MCP client](https://pydantic.dev/docs/ai/mcp/client/)
- [MCP Python SDK for server authors](https://github.com/modelcontextprotocol/python-sdk)
- [Public MCP servers](https://github.com/modelcontextprotocol/servers)
- [fetch server README](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch)
- [AWS Knowledge MCP Server](https://awslabs.github.io/mcp/servers/aws-knowledge-mcp-server)
- [Using MCP servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers)
