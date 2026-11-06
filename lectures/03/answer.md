# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
  The bare LLM answer was more general and could respond from model knowledge alone. The agent answer was grounded in the course materials: it checked the glossary and used course-specific tools before answering, and it ended by asking a review question rather than giving a direct answer only.
- Tool calls shown by `--trace` (tool names and arguments):
  The trace output showed the agent using the course tools, including `search_glossary` and `make_quiz`. For the Lecture 02 review-question prompt, the tool call pattern was consistent with a glossary lookup and a quiz request, for example `search_glossary({"query": "QLoRA"})` and `make_quiz({"lecture": 2})`.
- Number of LLM calls for one question (`requests`):
  The trace summary available here did not include a numeric `requests` value, so the exact count was not printed in the output we saw. The run still showed the model making a tool-assisted answer flow rather than a plain single-model response.
- Tool added and the description in its docstring:
  Added `make_quiz(lecture)`. It selects a glossary term from the requested lecture and returns a JSON string containing a question and its definition as the answer. Its docstring tells the model to use it for quiz or review-question requests.

## Homework

- Level attempted: Basic
- What you did:
  I updated the agent instructions in `app/agent.py` so that the agent checks the glossary before answering, uses `make_quiz` for review questions, and ends the response by asking one review question related to the topic.
- Results:
  The tool listing confirmed the relevant tools were available: `search_glossary`, `get_lecture_summary`, and `make_quiz`. The trace run produced a review question about QLoRA, and the test run passed: `11 passed` with one dependency deprecation warning.
- Observations and questions:
  The agent is more grounded and course-aware than the bare LLM because it uses the glossary and lecture-specific tools. The model’s final output was influenced by the instruction wording, especially the requirement to end by asking a review question.
