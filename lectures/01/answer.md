# Lecture 01 Answers

# Lecture 01 Answers

## Exercises

- Model's answer to the course-specific question (the 3 homework levels; a summary is fine): `gemini-3.5-flash-lite` said it has no information about the AIE2026 course and asked me to share the syllabus. It did not list the levels.
- What you noticed when comparing it with the correct meaning in the glossary: the correct levels are Basic, Implementation and Advanced. The model did not guess them in this run; it declined. The slides warn that it can also answer plausibly and wrongly, so the answer may differ between runs.
- Token counts you displayed (input / output): input=18, output=77 (`app.ask`, default question, `gemini-3.5-flash-lite`).

## Homework

- Level attempted: Advanced
- What you did:
  - Wrote `bench.py` (repo root, committed). For each (model, question, run) it calls `generate_content` and records wall-clock latency and `usage_metadata` (input, output, thinking tokens) into `bench_results.csv`. It sleeps between requests (5 s for lite, 13 s for the stronger model) and retries 429/503 once.
  - Models: `gemini-3.5-flash-lite` (3 runs per question), `gemini-3.8-flash` (2 runs per question).
  - Questions: `general` ("What is LoRA?"), `course` (the 3 homework levels), `short` ("Explain overfitting in one sentence.").
  - Ran the whole script twice. Run 1 data: `bench_results_run1.csv`. Run 2 data: `bench_results.csv`.
- Results:

  Run 2 (`bench_results.csv`):

  | model | question | n_ok | latency mean (min-max) s | in tok | out tok | thought tok | max sequential req/min |
  |---|---|---|---|---|---|---|---|
  | gemini-3.5-flash-lite | general | 3 | 3.57 (3.11-4.42) | 6 | 663.3 | 0 | 16.8 |
  | gemini-3.5-flash-lite | course | 3 | 1.41 (1.04-1.61) | 18 | 170 | 0 | 42.7 |
  | gemini-3.5-flash-lite | short | 3 | 1.15 (0.87-1.32) | 7 | 34 | 0 | 52.2 |
  | gemini-3.8-flash | general | 0 | - | - | - | - | - |
  | gemini-3.8-flash | course | 2 | 169.20 (129.28-209.12) | 18 | 343 | 1462 | 0.4 |
  | gemini-3.8-flash | short | 0 | - | - | - | - | - |

  Failed calls in run 2: 4 of 15, all on `gemini-3.8-flash` (general: 503; short: 429).

  Run 1 (`bench_results_run1.csv`), lite: general 3.48 s / 683 out tokens, course 1.32 s / 60 out, short 1.30 s / 38 out, 0 thinking tokens. All 6 `gemini-3.8-flash` calls failed with 503 (12 attempts).

- Observations and questions:
  - On lite, latency tracks output length: `general` (~660 output tokens) took about 3.5 s, `short` (34-38 tokens) about 1.2 s.
  - The same question gave different output lengths across runs. `course` averaged 60 output tokens in run 1 and 170 in run 2, so averages over n=3 are noisy and I cannot claim real differences.
  - Lite used 0 thinking tokens. `gemini-3.8-flash` (`course`, n=2) used about 1462 thinking tokens on top of 343 output tokens and took 129-209 s per call, versus about 1.4 s for lite. Thinking tokens probably explain part of the gap. I did not verify whether queueing under load also contributed.
  - Input tokens were small (6-18) because there is no system prompt or history.
  - Failures were 503 (model busy, a capacity problem, not a quota) and later 429 (rate limit). The script does not distinguish per-minute from per-day 429s. I did not verify the stronger model's daily quota usage.
  - Relation to rate limits: lite is limited to 15 req/min. Sequential max rates (60 / mean latency) were 16.8 (`general`) and 43-52 (`course`, `short`) per minute, all above 15, so a tight loop would need throttling (my script sleeps). For the stronger model (5 req/min) the measured sequential max was 0.4 req/min (`course`), far below the limit, so the per-minute limit was not what constrained it. Its capacity (503), and probably its small daily cap (about 10-20), did.
  - Limits: small sample, one session, latency includes network from Codespaces, free-tier behavior varies with load.
  - Models used: `gemini-3.5-flash-lite`, `gemini-3.8-flash`.
  - AI tools: Claude helped write `bench.py`. I ran it and checked the results.
  - No API key appears in code, logs, or this file.