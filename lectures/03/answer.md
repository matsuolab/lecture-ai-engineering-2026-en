# Lecture 03 Answers

## Exercises


- Differences between the Lecture 01 (bare LLM) and agent answers:
  The agent searched the glossary before answering, so it used course-specific information instead of only general model knowledge.

- Tool calls shown by `--trace` (tool names and arguments):
  - `search_glossary({"query": "LoRA"})`
  - `search_glossary({"query": "QLoRA"})`
  - `make_quiz({"lecture": 2})` when asked for a review question

- Number of LLM calls for one question (`requests`):
  Copy the exact number from the `[usage]` line in your terminal output.

- Tool added and the description in its docstring:
  Added `make_quiz(lecture)`, which picks a glossary term from the requested lecture and returns a JSON string with a question and answer.
## Homework

- Level attempted: Basic
- What you did:
  I changed the instruction in `app/agent.py` so the model uses `make_quiz` for review questions and ends with a review question.
- Results:
  After the instruction change, the trace showed different tool usage and the answer changed compared with the original version.
- Observations and questions:
  Small wording changes in instructions and tool descriptions affect the agent’s behavior.
