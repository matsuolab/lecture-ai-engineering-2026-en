# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
  The bare LLM gave a generic description of the homework levels: Beginner/Core, Intermediate/Applied, and Advanced/Research & Production. The agent used course-specific information from the AIE2026 glossary, so its answer was grounded in the course materials rather than a generic interpretation.

- Tool calls shown by `--trace` (tool names and arguments):
  The review-question run produced the prompt “What does Supervised Fine-Tuning (SFT) mean?” The exact `[tool call]` lines and argument dictionaries were not captured in the information available here, so I need to copy them from my terminal trace rather than guess. The exercise instructions give `[tool call] make_quiz({'lecture': 2})` as an example of the expected call for a Lecture 02 review question.

- Number of LLM calls for one question (`requests`):
  I need to copy the actual `requests` value from the `[usage]` line in my terminal trace; it was not captured in the notes available here.

- Tool added and the description in its docstring:
  Added `make_quiz(lecture: int) -> str`. It selects a glossary term from the requested lecture and returns a JSON string containing a question and its answer. Its docstring explains that it should be used for a quiz or review question from a lecture and that the result includes both the question and answer.

## Homework

- Level attempted: Basic
- What you did:
  I changed the instructions in `app/agent.py` to tell the agent to use `make_quiz` for review or quiz requests and to end its answer by asking one review question related to the topic.
- Results:
  The tool list included `search_glossary`, `get_lecture_summary`, and `make_quiz`. In a Lecture 02 run, the agent produced the review prompt “What does Supervised Fine-Tuning (SFT) mean?” I did not capture the exact tool-call arguments or a before-and-after trace comparison, so I should add those details after rerunning the same question with `--trace`.
- Observations and questions:
  The glossary and lecture tools give the agent access to course-specific information. Instructions and tool descriptions can affect which tools it selects. A useful next test is to compare traces before and after changing one instruction, recording the tool names, arguments, request count, and answer each time.
