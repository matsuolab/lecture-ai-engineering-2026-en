# Lecture 01 Answers

## Exercises

- Model's answer to the course-specific question (the 3 homework levels; a summary is fine):
  When asked without tools, the bare model either politely refused (stating that AIE2026 is a specific course code outside its training data) or hallucinated plausible academic levels ("Beginner / Foundational", "Intermediate / Applied", "Advanced / Expert").

- What you noticed when comparing it with the correct meaning in the glossary:
  In `data/glossary.json`, the three actual levels are:
  1. "Basic" (review lecture content)
  2. "Implementation" (write your own code)
  3. "Advanced" (research and experimentation)
  Completing any one level completes the homework, and assignments are not graded. The bare LLM has no access to course-specific documents, which causes it to either hedge or make plausible guesses based on general academic patterns.

- Token counts you displayed (input / output):
  - Question: "What are the 3 homework levels in the AIE2026 course?" -> input: 18, output: 230
  - Question: "What is LoRA?" -> input: 6, output: 759

## Homework

- Level attempted: All (Basic, Implementation, Advanced)
- What you did:
  1. **Basic**: Ran test queries across multiple models (`gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`, `gemini-3.5-flash`, and `gemini-3.8-flash`) and varying temperatures (0.0, 0.7, 1.2).
  2. **Implementation**: Updated `app/ask.py` with `chat_loop()` and `--chat` (`-c`) support, using `client.chats.create()` to retain conversational history across follow-up questions while reporting token counts per turn.
  3. **Advanced**: Benchmarked response latency, token consumption, and model availability. Analyzed the relationship between model selection, multi-turn history accumulation, and free-tier rate limits (RPM/TPM and 503 capacity constraints).
- Results:
  - **Basic (Temperature & Models)**:
    - At temperature 0.0, responses were deterministic and focused on explicit refusals. At 0.7 and 1.2, responses varied in structure and offered helpful follow-up suggestions asking for the course syllabus.
    - `gemini-3.1-flash-lite` provided the fastest response times (2.2s–3.9s), while `gemini-3.5-flash-lite` returned comprehensive structured responses (4.7s–6.1s).
  - **Implementation (Multi-Turn Chat)**:
    - Successfully validated context retention:
      - Turn 1: "What is LoRA in 10 words?" -> input: 11 tokens, output: 16 tokens.
      - Turn 2: "Summarize that in 3 words." -> input: 37 tokens (accurately demonstrating that previous prompt/response tokens are retained in the session context), output: 6 tokens.
  - **Advanced (Latency, Token Metrics & Rate Limits)**:
    - `gemini-3.1-flash-lite`: 3.90s latency (6 input / 833 output tokens on LoRA); 2.26s latency (18 input / 461 output tokens on 3 levels).
    - `gemini-3.5-flash-lite`: 6.10s latency (6 input / 595 output tokens on LoRA); 4.70s latency (18 input / 50 output tokens on 3 levels).
    - `gemini-3.8-flash` & `gemini-3.5-flash`: Encountered high-demand throttling on the free tier (`503 UNAVAILABLE - Model currently experiencing high demand` and `504 DEADLINE_EXCEEDED`).
- Observations and questions:
  In multi-turn chat sessions, every turn resends the entire conversation history, which rapidly drives up the `prompt_token_count`. On free-tier API quotas (especially TPM limits), long conversation histories can quickly exhaust allowances, making token tracking and compact prompts essential.
