# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
  The agent gives course-oriented answers and can use glossary tools, while the bare LLM responds without those course tools. For the review-question run I shared, the agent asked, "What does LoRA mean?" and gave a hint about freezing base weights and using two smaller low-rank matrices. I don't have the bare-LLM answer to make a more specific comparison.
- Tool calls shown by `--trace` (tool names and arguments):
  The agent's final response shows that it generated a Lecture 02 review question about LoRA. The exact `[tool call]` names and arguments were not included in the output I shared, so I cannot report them accurately yet.
- Number of LLM calls for one question (`requests`):
  The exact `requests` value was not included in the output I shared. It needs to be copied from the trace's `[usage]` line.
- Tool added and the description in its docstring:
  Added `make_quiz(lecture)`. It selects a glossary term from the requested lecture and returns a JSON string containing a question and its definition as the answer. Its docstring says to use it when a learner asks for a quiz or review question from a lecture, and that its result includes a question and answer.

## Homework

- Level attempted: Basic
- What you did:
  Changed the agent instructions in `app/agent.py` to use `make_quiz` for quiz or review-question requests and end responses by asking one related review question.
- Results:
  The reported tool list included `search_glossary`, `get_lecture_summary`, and `make_quiz`. In the latest reported Lecture 02 review response, the agent asked, "What does LoRA mean?" and gave a hint about parameter-efficient fine-tuning, frozen base weights, and low-rank matrices. The reported test run passed: 11 tests passed, with one dependency deprecation warning. The exact trace calls and request count were not included in the output shared here.
- Observations and questions:
  The agent produced a review-style response as requested. To complete a before-and-after comparison for the Basic homework, compare the same prompt with the original and revised instructions and record the actual differences in tool calls and answers.
