# Lecture 03 Exercises and Homework: Build a Learning Support Agent

## Goals for This Session

- Verify in your own code that an agent consists of "model + loop + tools"
- Read which tools were called with which arguments
- Add one tool

## Preparation

If you have completed the work from previous sessions, create branch `lec03` from `main`.

```bash
git switch main && git switch -c lec03
```

Otherwise, you can create a branch from the course repository's starting code (the `lec03-start` tag).

```bash
git remote -v                     # If upstream is missing, add it with the next line
git remote add upstream https://github.com/matsuolab/lecture-ai-engineering-2026.git
git fetch upstream --tags
git switch -c lec03 lec03-start
```

## Exercises (30 Minutes)

### 1. Ask the Agent the Same Question as in Lecture 01

```bash
uv run python -m app.agent "What is a lecNN-start tag in the AIE2026 course?"
```

Compare the answer with `app.ask` in Lecture 01.

### 2. Read Tool Calls

```bash
uv run python -m app.agent --trace "What is the difference between LoRA and QLoRA?"
```

On the `[tool call]` lines, check which tools the model called and with which arguments. `requests` in `[usage]` shows how many LLM calls were made for one question.

### 3. Add One Tool

Add `make_quiz` to `app/tools.py` and register it at `TODO(Lecture 03 exercise)` in `app/agent.py`.

- Example: choose one term from the specified session (`lecture: int`) and return a "What does this term mean?" question and its answer
- In the docstring, explain "when and why to use this tool" (the model reads this to decide whether to use it)

```bash
uv run python -m app.agent --trace "Give me one review question from Lecture 02"
uv run pytest -q
```

### 4. Submit

Fill in `lectures/03/answer.md` and open a PR from `lec03` to `main` in your own fork.

## Homework (Complete Any One Level)

| Level | Task |
|---|---|
| Basic | Rewrite `INSTRUCTIONS` or tool docstrings, and use `--trace` to compare and record changes in tool calls and answers |
| Implementation | Create a `save_learning_log` tool that saves learning records in `learning_log/`. Request user confirmation before saving (Pydantic AI's `requires_approval=True`). Write tests using TestModel too |
| Advanced | Choose one: (a) Rebuild the same agent with Google's ADK and compare how you write it and how it appears in `adk web`. (b) Run Pi, introduced in the lecture, in Codespaces and compare Pi's public system prompt with your agent's `INSTRUCTIONS` |

### How to Approach Advanced Option (b)

Pi is a coding agent that can read and write files and run commands. It does not request confirmation for every tool execution. Try it inside Codespaces rather than on your own PC.

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
pi
```

- Gemini reads the `GEMINI_API_KEY` environment variable, so a Codespaces secret works as is. In Pi, type `/model` and select a Gemini model
- The npm package name is `@earendil-works/pi-coding-agent` (`@mariozechner/...` in older articles is the old name)
- Pi's system prompt is in `packages/coding-agent/src/core/system-prompt.ts` in its public repository, https://github.com/earendil-works/pi. Compare it with your `INSTRUCTIONS` and see what it includes and omits
- Official documentation: https://github.com/earendil-works/pi/tree/main/packages/coding-agent/docs

## References

- Pydantic AI: https://ai.pydantic.dev/
- ADK: https://google.github.io/adk-docs/
