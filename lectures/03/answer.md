# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
  For the question about the three homework levels, the bare LLM described them generically as Beginner/Core, Intermediate/Applied, and Advanced/Research & Production. The agent used course-specific information and correctly named them Basic (review the lecture), Implementation (write code), and Advanced (research and experimentation). It also said that completing any one level is enough.
- Tool calls shown by `--trace` (tool names and arguments):
  The Lecture 02 review-question trace returned: "What does Supervised Fine-Tuning (SFT) mean?" The exact `[tool call]` line(s) and arguments were not included in the output summary, so I cannot report them accurately. Copy them from the full terminal trace.
- Number of LLM calls for one question (`requests`):
  The exact `requests` value was not included in the output summary. Copy it from the `[usage]` line in the full terminal trace.
- Tool added and the description in its docstring:
  Added `make_quiz(lecture)`. It selects a glossary term from the requested lecture and returns a JSON string containing a question and its definition as the answer. Its docstring says to use it when a learner asks for a quiz or review question from a lecture, and that its result includes a question and answer.

## Homework

- Level attempted: Basic
- What you did:
  Changed the agent instructions in `app/agent.py` to use `make_quiz` for quiz or review-question requests and end responses by asking one related review question.
- Results:
  The reported tool list included `search_glossary`, `get_lecture_summary`, and `make_quiz`. In the latest reported Lecture 02 review run, the agent generated the question, "What does Supervised Fine-Tuning (SFT) mean?" The reported test run passed: 11 tests passed, with one dependency deprecation warning.
- Observations and questions:
  The bare LLM gave generic labels for the homework levels, while the agent returned the course's exact labels and explained that any one level completes the homework. The agent also generated a review question about SFT. The exact trace calls and request count still need to be copied from the full `[tool call]` and `[usage]` output; they were not present in the summaries shared here.
