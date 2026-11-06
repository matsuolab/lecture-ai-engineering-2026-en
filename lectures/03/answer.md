# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
  _Not recorded yet. Compare the answers from both versions using the same question and describe what you observed._
- Tool calls shown by `--trace` (tool names and arguments):
  The provided terminal summary says the trace returned a Lecture 02 review question about QLoRA, but it does not include the exact `[tool call]` line(s) or arguments. Copy those from the full trace output rather than guessing.
- Number of LLM calls for one question (`requests`):
  _Not included in the terminal summary. Copy the `requests` value from the trace's `[usage]` line._
- Tool added and the description in its docstring:
  Added `make_quiz(lecture)`. It selects a glossary term from the requested lecture and returns a JSON string containing a question and its definition as the answer. Its docstring explains that it should be used for quiz or review-question requests.

## Homework

- Level attempted: Basic
- What you did:
  Changed the final-answer instruction in `app/agent.py` to ask a review question related to the topic, and added an instruction to use `make_quiz` for review or quiz requests.
- Results:
  The reported checks completed successfully. `--list-tools` showed `search_glossary`, `get_lecture_summary`, and `make_quiz`. The trace returned a Lecture 02 review question about QLoRA. `uv run pytest -q` passed: 11 tests passed, with one dependency deprecation warning.
- Observations and questions:
  The tool-list check confirms that `make_quiz` is available, and the tests pass. The provided summary does not contain the exact trace calls or request count, nor a before-and-after comparison, so those observations still need to be recorded from the full output.
