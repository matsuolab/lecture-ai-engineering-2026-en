# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
  _Run both versions and record the observed difference._
- Tool calls shown by `--trace` (tool names and arguments):
  _Run the trace command and record the actual tool names and arguments._
- Number of LLM calls for one question (`requests`):
  _Record the `requests` value printed by your trace._
- Tool added and the description in its docstring:
  Added `make_quiz(lecture)`. It selects a glossary term from the requested lecture and returns a JSON string containing a question and its definition as the answer. Its docstring tells the model to use it for quiz or review-question requests.

## Homework

- Level attempted: Basic
- What you did:
  Changed the final-answer instruction in `app/agent.py` from indicating the relevant lecture to ending with a review question related to the topic. Also instructed the agent to use `make_quiz` for review or quiz requests.
- Results:
  _Run the same prompt before and after the instruction change with `--trace`; record the observed tool calls, arguments, request count, and answer differences. These commands have not been run as part of this repository edit._
- Observations and questions:
  The instruction was changed, but its effect on tool selection and answers needs to be verified by running the agent with the configured model.
