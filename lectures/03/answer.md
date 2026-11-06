# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
  The agent's Lecture 02 review response asked, "What does overfitting mean?" and included a hint about memorizing training data versus learning general patterns, and using unseen data to detect overfitting. I don't have the bare-LLM response here, so I can't make a reliable direct comparison.
- Tool calls shown by `--trace` (tool names and arguments):
  The trace output itself wasn't included in the information available to me. The command was run for a Lecture 02 review question, and the reported response was about overfitting. Copy the exact `[tool call]` line and arguments from the terminal trace here; do not infer them from the final answer.
- Number of LLM calls for one question (`requests`):
  The numeric `requests` value wasn't included in the shared output. Copy it from the `[usage]` line in the full trace.
- Tool added and the description in its docstring:
  Added `make_quiz(lecture)`. It selects a glossary term from the requested lecture and returns a JSON string containing a question and its definition as the answer. Its docstring says to use it when a learner asks for a quiz or review question from a lecture, and that its result includes a question and answer.

## Homework

- Level attempted: Basic
- What you did:
  Changed the agent instructions in `app/agent.py` to use `make_quiz` for quiz or review-question requests and end responses by asking one related review question.
- Results:
  The reported tool list included `search_glossary`, `get_lecture_summary`, and `make_quiz`. For a Lecture 02 review request, the agent returned a question about overfitting with a hint about memorization, generalization, and unseen data. The reported test run passed: 11 tests passed, with one dependency deprecation warning. The exact tool-call trace and request count were not included in the shared output.
- Observations and questions:
  The agent produced a review-style response as requested. To complete a before-and-after comparison for the Basic homework, compare the same prompt with the original and revised instructions and record the actual differences in tool calls and answers.
