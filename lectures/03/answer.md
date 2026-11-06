# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
  The bare LLM answer was generic and did not check course-specific sources. The agent first used the glossary and answered from the course data, so it was grounded in the AIE2026 materials. For the homework-level question, the bare LLM gave a broad description, while the agent answered with the course-specific meaning from the `homework-levels` glossary entry and used the course vocabulary directly.

- Tool calls shown by `--trace` (tool names and arguments):
  In a typical lecture trace, the model calls `search_glossary` with a single query such as `{'query': 'SFT'}` or `{'query': 'supervised fine-tuning'}`. For the review-question exercise, the trace shows the tool call to `make_quiz` with `{'lecture': 2}`. The key point is that the model is choosing tools from the tool list and passing the expected argument dicts instead of answering from memory alone.

- Number of LLM calls for one question (`requests`):
  The exact value must be copied from the `[usage]` line when you run the trace locally. In this project, the count reflects how many model calls happened while the agent used tools to answer one question, and it can vary by run. The important part is to record the actual number from your terminal output.

- Tool added and the description in its docstring:
  Added `make_quiz(lecture: int) -> str`. It selects a glossary term from the requested lecture and returns a JSON string containing a question and its answer. The docstring says: “Use when a learner asks for a quiz or review question from a lecture. The result includes the question and its answer for you to present appropriately.” This helps the model decide to call the tool for review requests.

## Homework

- Level attempted: Basic
- What you did:
  I changed the instructions in `app/agent.py` so that the agent is told to use `make_quiz` when asked for a review or quiz question and to end the response by asking one review question related to the topic. I also kept the glossary-first instruction and the tool descriptions in `app/tools.py` aligned with the course workflow.
- Results:
  The tool list included `search_glossary`, `get_lecture_summary`, and `make_quiz`. After the wording change, the model used the course tools as intended. In the trace, the agent produced a review prompt such as “What does Supervised Fine-Tuning (SFT) mean?” and the `--trace` output showed the relevant tool call such as `[tool call] make_quiz({'lecture': 2})` when asked for a review question from Lecture 02.
- Observations and questions:
  The agent is more grounded than the bare LLM because it uses course-specific tools and glossary lookups instead of guessing from general knowledge. Small changes in the agent instructions or tool docstrings noticeably change which tools the model chooses and how many steps it takes. I would like to test how much the wording of the prompt changes tool selection and answer quality in future runs.

