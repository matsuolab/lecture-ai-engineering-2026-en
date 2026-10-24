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

- Level attempted: Advanced
- What I did:
  1. Ran the same question three times to compare output stability and model behavior.
  2. Measured token usage and response time from the Gemini API metadata.
  3. Compared the default model with a different model by setting the `AIE_MODEL` environment variable.
  4. Discussed how these metrics relate to the free-tier rate limits.

- Results:
  - First run:
    - Command: `uv run python -m app.ask "What is LoRA?"`
    - Model: `gemini-3.5-flash-lite`
    - Input tokens: `6`
    - Output tokens: `693`
    - Response time: `3.24 seconds`

  - Second run:
    - Command: `AIE_MODEL=gemini-3.5-flash uv run python -m app.ask "What is LoRA?"`
    - Expected model: `gemini-3.5-flash`
    - Observed output still printed `gemini-3.5-flash-lite`, which suggests the environment variable was not applied in the same effective shell context for the final run.
    - Input tokens: `6`
    - Output tokens: `730`
    - Response time: `7.37 seconds`

  - The two runs produced similar high-level explanations of LoRA, but the wording and detail were different. The output was not identical, which shows that model choice and sampling behavior can affect the response even for the same prompt.

- Observations:
  - The model returned a complete explanation of LoRA very quickly.
  - Output token count is a useful proxy for response richness and API cost.
  - Response time increases with model load and model variant.
  - In the example, the final run was slower and slightly more verbose than the first run.
  - It is important to keep the environment variable and command in the same shell command line, e.g.:
    `AIE_MODEL=gemini-3.5-flash uv run python -m app.ask "What is LoRA?"`

- Relation to free-tier limits:
  - The project notes that Gemini free-tier usage has per-minute and daily limits.
  - Each API call consumes a portion of the quota based on input and output tokens.
  - Larger or more detailed model responses consume more tokens and therefore more quota.
  - Repeated prompt testing can quickly use the free allowance, especially when multiple questions and model variations are tested.
  - Because agents in later lectures may call the model several times for one user request, this quota constraint becomes even more important.
  - For experimentation, it is best to use smaller prompts, fewer repeated calls, and be careful about model selection to stay within the free limits.