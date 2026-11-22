# Lecture 05 Answers

## Exercises

- Answering model (`[model]` shown during execution):
- Comparison question:
- Target materials (also record the difference in scope between full context and the other methods):

### Results by Method

| Method | Key points and correctness of the answer | Cited pages and evidence | Time (seconds) | Input/output tokens | Model responses | Estimated generation API cost (USD) |
|---|---|---|---|---|---|---|
| Full context | | | | | | |
| Vector search | | | | | | |
| Tree | | | | | | |
| Graph | | | | | | |

<!-- State when a method was not run or a cost was unavailable. Use a separate table for each additional question. -->

- Pages found by running search alone, and what their text confirmed:
- Tool calls shown by `--trace` (names, arguments, counts, table-of-contents paths followed by Tree, etc.):
- Examples where retrieved information was insufficient, or was retrieved but not used in the answer:
- Method you would adopt for this use case, your reasons, and limitations of the comparison conditions:
- Observations and questions:

## Homework

<!-- Completing any one of Basic, Implementation, or Advanced is sufficient. -->

- Level attempted: Basic
- Configuration compared: `RAG_TOP_K = 5` and `RAG_TOP_K = 3` in `app/config.py`. The settings are inferred from the run sequence because the trace does not print the configured limit.
- Comparison question: “In Lecture 02, what does LoRA freeze and what does it train? What does QLoRA add?”
- Conditions for both runs: `gemini-3.5-flash-lite`, Python 3.12.16, the bundled vector index, and the same question with `--trace`.

### Results by Method

| Method | Key points and correctness of the answer | Cited pages and evidence | Time (seconds) | Input/output tokens | Model responses | Estimated generation API cost (USD) |
|---|---|---|---|---|---|---|
| Vector search (`RAG_TOP_K = 5`) | Correctly explains that LoRA freezes the base weights and trains a low-rank update represented by matrices A and B. QLoRA quantizes the base weights to 4 bits to reduce memory use. | Lecture 02, pp. 51–52. The first result shown in the trace is `lec02-main-p052`. | 11.45 | 2,759 / 181 | 2 | 0.001280 |
| Vector search (`RAG_TOP_K = 3`) | Correctly preserves all three points and adds a follow-up hint about GPU memory. | Lecture 02, pp. 51–52. The first result shown in the trace is `lec02-main-p052`. | 10.62 | 2,057 / 183 | 2 | 0.001075 |

- Tool calls: both runs called `search_materials` once with `LoRA freeze train QLoRA add`.
- Comparison: input fell by 702 tokens (25.4%), estimated generation cost fell by about 16%, and the answer completed 0.83 seconds sooner. Output increased by two tokens.
- Limitations: each setting was run once for this question. The truncated trace confirms the first result in both runs. The latency difference may vary across runs.
