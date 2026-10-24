# Lecture 01 Answers

## Exercises

- Model's answer to the course-specific question (the 3 homework levels; a summary is fine):
- What you noticed when comparing it with the correct meaning in the glossary:
- Token counts you displayed (input / output):

## Homework

- Level attempted: Basic / Implementation / Advanced
- What you did:
  Ran the same prompt three times using different generation settings:
  *AIE_MODEL=gemini-3.5-flash-lite uv run python -m app.ask "What is LoRA?"
  *AIE_MODEL=gemini-3.5-flash uv run python -m app.ask "What is LoRA?"
  *AIE_MODEL=gemini-3.5-flash-lite uv run python -m app.ask "What is LoRA?" with a higher temperature setting in the API call
  *Compared differences in wording, confidence, level of detail, and structure.

- Results:
  *The core idea stayed similar across runs, but the phrasing changed noticeably.
  *Different models produced different levels of detail and emphasis.
  *Higher temperature led to more variation and sometimes a more creative, less deterministic answer.
  *Lower temperature gave a more stable and concise response.
- Observations and questions:
  *Model choice affected clarity, brevity, and how much supporting detail was included.
  *Temperature mainly changed creativity and variability, not the underlying factual concept.
  *For course-specific questions, it is safest to check the glossary before trusting the answer.