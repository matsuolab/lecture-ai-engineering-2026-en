# Lecture 01 Answers

## Exercises

- Model's answer to the course-specific question (the 3 homework levels; a summary is fine): Run 1 (default question): gemini-3.5-flash-lite said it has no access to specific or internal details of the "AIE2026" course, so it could not give the 3 homework levels, and asked for more context. Run 2 (reworded as 'What are the "3 levels" in the AIE2026 course homework?'): the same model answered confidently with a long, detailed answer: Level 1 "Foundations & Implementation" (basic competency, following tutorials), Level 2 "Engineering & Optimization" (production-ready code, error handling, evaluation), and Level 3 "Research, Innovation & Agents" (open-ended, multi-agent systems, advanced RAG, RLHF/DPO). It also claimed the levels work as a grading rubric (Level 1 passing, Level 2 good, Level 3 full marks).
- What you noticed when comparing it with the correct meaning in the glossary: The glossary (`homework-levels`) says the three levels are Basic (review lecture content), Implementation (write your own code) and Advanced (research and experimentation), that completing any one level completes the homework, and that as a rule it is not graded. Run 1 did not know and honestly said so. Run 2 was mostly wrong: its level names and contents were invented, and its grading-rubric claim contradicts the glossary (any one level is enough, and it is not graded). Only loose overlaps exist (an implementation level, and an advanced research level). The most important thing I noticed is that the same course question produced "I don't know" in one run and a confident, detailed, plausible but incorrect answer in another, with nothing in the text signalling that the second was made up. A bare LLM has no knowledge of this course, and its confidence is not evidence of correctness, which is why later lectures give the model tools such as glossary search.
- Token counts you displayed (input / output): Run 1: 18 input / 81 output (99 total), 0.94 s. Run 2: 20 input / 569 output (589 total), 3.09 s; the wrong, confident answer used about 7 times more output tokens than the honest "I don't know". In my benchmark, "What does LoRA stand for?" showed 8 / 111 and 8 / 57 on gemini-3.5-flash-lite (two runs) and 8 / 226 and 8 / 235 on gemini-3.6-flash, plus 324 and 290 thought tokens.

## Homework

- Level attempted: Advanced
- What you did: Extended `app/ask.py` to measure response time (`time.perf_counter()`) and read token counts from `response.usage_metadata`. Wrote `app/benchmark.py` to run 2 models x 3 questions x 2 trials (12 requests, 10 s apart), saving every trial, including failures, to `lectures/01/results.csv`. Models: `gemini-3.6-flash` and `gemini-3.5-flash-lite`. Questions, identical for both models: Q1 "What does LoRA stand for?" (8 input tokens), Q2 an explanation question (19), Q3 a long reasoning question about full fine-tuning vs LoRA on a free Colab T4 (99).
- Results:

| Model | Question | Successful / total | Avg time (s) | Avg input | Avg output | Avg thought | Avg total |
|---|---|---|---|---|---|---|---|
| gemini-3.6-flash | Q1 | 2/2 | 9.93 | 8 | 230.5 | 307 | 545.5 |
| gemini-3.6-flash | Q2 | 1/2 | 19.11 | 19 | 1181 | 972 | 2172 |
| gemini-3.6-flash | Q3 | 2/2 | 28.19 | 99 | 1142 | 1291.5 | 2532.5 |
| gemini-3.5-flash-lite | Q1 | 2/2 | 0.95 | 8 | 84 | n/a | 92 |
| gemini-3.5-flash-lite | Q2 | 2/2 | 3.46 | 19 | 792.5 | n/a | 811.5 |
| gemini-3.5-flash-lite | Q3 | 2/2 | 4.40 | 99 | 1069 | n/a | 1168 |

  The Q2 result for gemini-3.6-flash is one trial only, because trial 2 failed with a 503 (high demand). Per-trial data are in `lectures/01/results.csv`.

- Observations and questions:
  - **Speed:** gemini-3.5-flash-lite was faster on every question (about 10.5x on Q1, 5.5x on Q2, 6.4x on Q3) and very consistent between trials. gemini-3.6-flash varied a lot (Q1: 15.44 s vs 4.42 s for almost the same number of generated tokens), so length alone does not explain response time.
  - **Tokens:** input tokens were identical for both models and grew with question length (8, 19, 99). Output grew from Q1 to Q2/Q3, but Q3 had about 5x the input of Q2 without a much longer answer, so question type mattered more than input length.
  - **Hidden thinking:** gemini-3.6-flash reported thought tokens (about 45% to 56% of its total), so for it total = input + output + thought, not input + output. gemini-3.5-flash-lite reported none, and total = input + output. Thinking explains much of its extra time and token use.
  - **Quality:** both were correct on everything I could check. 3.6 was more detailed (it gave both meanings of LoRA in Q1, a worked numeric example in Q2, a table in Q3); lite was more concise. Both recommended QLoRA in Q3. Their full fine-tuning memory estimates differed (50-60 GB vs 50-80 GB) and I did not verify them.
  - **Free quota:** across 12 requests at 10 s spacing there was one 503 (capacity, not quota) and no 429 rate-limit errors. I did not test where my actual limits are and I am not claiming a precise quota. I did not verify how thought tokens count toward quota, which should be checked in the current API docs. In production I would retry on 429/503 with exponential backoff and jitter, limit request frequency, monitor token usage from `usage_metadata`, cache repeated answers, and use the smaller model for simple questions.
  - **Limits of this experiment:** only 2 trials per combination (1 for one cell), one time window, free tier, and quality judged by my own reading.
  - **Question:** does the extra thinking improve answer quality enough to justify several times the time and tokens for questions like these?