# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
  The bare LLM answer was generic: for the homework-level question it described the levels as Beginner/Core, Intermediate/Applied, and Advanced/Research & Production. The agent answered with the course-specific labels: Basic (review the lecture), Implementation (write code), and Advanced (research and experimentation), and it also explained that completing any one level is enough.

- Tool calls shown by `--trace` (tool names and arguments):
  The Lecture 02 review-question trace produced the question: "What does Supervised Fine-Tuning (SFT) mean?" The exact `[tool call]` lines and argument dictionaries were not included in the output summary shared here, so they are not reproduced exactly.

- Number of LLM calls for one question (`requests`):
  The exact `requests` value from the `[usage]` line was not included in the shared output summary. It should be copied from the terminal output when the trace is run.

- Tool added and the description in its docstring:
  Added `make_quiz(lecture)`. It selects a glossary term from the requested lecture and returns a JSON string containing a question and its answer. The docstring tells the model to use it when a learner asks for a quiz or review question from a lecture.

## Homework

- Level attempted: Basic
- What you did:
  I changed the agent instructions in `app/agent.py` so that the model uses `make_quiz` for review or quiz requests and ends the response by asking one review question related to the topic.
- Results:
  The tool list included `search_glossary`, `get_lecture_summary`, and `make_quiz`. In the latest Lecture 02 run, the agent produced the review prompt: "What does Supervised Fine-Tuning (SFT) mean?" The reported test pass was successful: `11` tests passed, with one dependency deprecation warning.
- Observations and questions:
  The agent is more grounded than the bare LLM because it uses course-specific tools and glossary lookups. Small wording changes in the instruction and tool descriptions change how the model chooses tools and final responses; this is the key takeaway from the Basic homework.
