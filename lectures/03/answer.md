# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
  The bare LLM gave a generic description of the homework levels: Beginner/Core, Intermediate/Applied, and Advanced/Research & Production. The agent used course-specific information from the AIE2026 glossary, so its answer was grounded in the course materials rather than a generic interpretation.

- Tool calls shown by `--trace` (tool names and arguments):
  For “What is the difference between LoRA and QLoRA?”, the agent called `search_glossary` twice, once for `LoRA` and once for `QLoRA`. For “Give me one review question from Lecture 02”, it called `make_quiz` with `{'lecture': 2}`.

- Number of LLM calls for one question (`requests`):
  Both trace runs reported `requests: 2` in the `[usage]` output.

- Tool added and the description in its docstring:
  Added `make_quiz(lecture: int) -> str`. It selects a glossary term from the requested lecture and returns a JSON string containing a question and its answer. Its docstring explains that it should be used for a quiz or review question from a lecture and that the result includes both the question and answer.

## Homework

- Level attempted: Basic
- What you did:
  I changed the instructions in `app/agent.py` to tell the agent to use `make_quiz` for review or quiz requests and to end its answer by asking one review question related to the topic.
- Results:
  The tool list included `search_glossary`, `get_lecture_summary`, and `make_quiz`. In the Lecture 02 review run, the agent called `make_quiz` with `{'lecture': 2}` and produced a review prompt such as “What does Supervised Fine-Tuning (SFT) mean?” The trace reported `requests: 2`.
- Observations and questions:
  The glossary and lecture tools give the agent access to course-specific information. Instructions and tool descriptions can affect which tools it selects. Comparing traces before and after changing one instruction is a useful way to observe changes in tool selection, arguments, request count, and answers.
