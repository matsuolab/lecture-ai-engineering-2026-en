# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
  _Still to record: run the Lecture 01 bare-LLM comparison and describe the observed difference._
- Tool calls shown by `--trace` (tool names and arguments):
  The trace produced a Lecture 02 review question about QLoRA. The summary of the terminal output provided did not include the exact `[tool call]` lines and arguments, so record those from the full trace output if available.
- Number of LLM calls for one question (`requests`):
  _Still to record: copy the `requests` value from the trace's `[usage]` line; it was not included in the output summary._
- Tool added and the description in its docstring:
  Added `make_quiz(lecture)`. It selects a glossary term from the requested lecture and returns a JSON string containing a question and its definition as the answer. Its docstring explains that it should be used for quiz or review-question requests.

## Homework

- Level attempted: Basic
- What you did:
  Changed the final-answer instruction in `app/agent.py` to ask a review question related to the topic, and added an instruction to use `make_quiz` for review or quiz requests.
- Results:
  The reported checks completed successfully. `--list-tools` showed `search_glossary`, `get_lecture_summary`, and `make_quiz`. The trace produced a Lecture 02 review question about QLoRA. `uv run pytest -q` passed: 11 tests passed, with one dependency deprecation warning.
- Observations and questions:
  The tool-list check confirms that `make_quiz` is available to the model, and the tests pass. To complete the behavior comparison, record the exact tool call and `[usage]` request count from the full trace and compare the same prompt before and after the instruction change. The bare-LLM comparison also still needs to be recorded.
