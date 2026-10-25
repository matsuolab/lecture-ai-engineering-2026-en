# Lecture 01 Answers

## Exercises

- Model's answer to the course-specific question (the 3 homework levels; a summary is fine):
- What you noticed when comparing it with the correct meaning in the glossary:
- Token counts you displayed (input / output):

## Homework

- Level attempted: Basic
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

- Level attempted: Implementation
- What I did:
  - Updated `app/ask.py` so the function accepts an optional `conversation_history` argument.
  - Kept the original single-question behavior working for existing usage.
  - Added an interactive mode using a loop so the user can ask multiple follow-up questions.
  - Stored both user messages and assistant responses in a history list and sent the full list back to the model for the next request.
  - Added an exit command (`exit` or `quit`) to stop the chat loop cleanly.

- Results:
  - The program can now answer a follow-up question using context from earlier turns.
  - Example conversation:
    1. User: Explain retrieval-augmented generation.
    2. Assistant: ...
    3. User: What are its two main advantages?
    4. Assistant: ...
  - The second question is answered with awareness of the previous answer instead of as an isolated input.

- Observations and questions:
  - Preserving full conversation history is important because follow-up questions often refer to previous statements.
  - As the conversation grows longer, the request size increases and can eventually consume more tokens and context window space.
  - This is a good foundation for later lessons where the agent uses tools and richer memory.

## Implementation Notes

The core idea is that each new request sends the accumulated conversation history together with the latest question. In practice, the history is stored as a list of message objects like this:

```python
conversation = [
    {"role": "user", "content": "What is AI engineering?"},
    {"role": "assistant", "content": "AI engineering is ..."},
    {"role": "user", "content": "Can you summarize that?"},
]
```

Then the next API call uses the full list as input instead of only the latest question. This preserves context and supports natural multi-turn conversations.


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