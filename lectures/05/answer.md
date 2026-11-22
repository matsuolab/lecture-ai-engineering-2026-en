# Lecture 05 Answers

## Exercises

- Answering model (`[model]` shown during execution): Not run. The configured default is `gemini-3.5-flash-lite`, but the runtime model was not confirmed by an execution.
- Comparison question: `In Lecture 02, what does LoRA freeze and what does it train? What does QLoRA add?`
- Target materials:
  - Full context: 8 documents and 398 pages from the supplied materials JSON.
  - Vector search, Tree, and Graph: 214 pages from the main materials for Lectures 01–03.
  - These methods were not run, so no measured comparison of answers, evidence, time, tokens, or cost is available.

### Results by Method

| Method | Key points and correctness of the answer | Cited pages and evidence | Time (seconds) | Input/output tokens | Model responses | Estimated generation API cost (USD) |
|---|---|---|---|---|---|---|
| Full context | Not run; no model answer to evaluate | Not run | Not run | Not run | Not run | Not run |
| Vector search | Not run; no model answer to evaluate | Not run | Not run | Not run | Not run | Not run |
| Tree | Not run; no model answer to evaluate | Not run | Not run | Not run | Not run | Not run |
| Graph | Not run; no model answer to evaluate | Not run | Not run | Not run | Not run | Not run |

<!-- State when a method was not run or a cost was unavailable. Use a separate table for each additional question. -->

- Pages found by running search alone, and what their text confirmed:
  - Search was not run. Direct inspection of `lec02-main-p052` in the materials confirms that LoRA freezes the original weights and trains a small low-rank change represented by A/B matrices; QLoRA adds 4-bit storage of the frozen original weights. This is source inspection, not a search result or model response.
  - Citation as labeled in the materials: Lecture 2 · Japanese source p.52 · corresponding translated PDF p.75.
- Tool calls shown by `--trace` (names, arguments, counts, table-of-contents paths followed by Tree, etc.): Not run; no traces are available.
- Examples where retrieved information was insufficient, or was retrieved but not used in the answer: Not measured; the answering and retrieval methods were not run.
- Method you would adopt for this use case, your reasons, and limitations of the comparison conditions:
  - For this specific question, I would start with vector search because one page appears to contain the necessary evidence. This is a reasoned choice based on the inspected source page, not an experimentally tested result. Tree may help when the relevant section is known; Graph may add related pages that are not necessarily evidence.
  - No empirical method comparison is available. The methods also differ in scope: full context includes all 8 documents and 398 pages, whereas vector search, Tree, and Graph use 214 pages from Lectures 01–03.
- Observations and questions:
  - The Codespace was unavailable because it was full, so live model calls, traces, timings, token counts, and costs could not be collected. “Not run” does not mean zero cost or a failed answer.

## Homework

- Level attempted: Implementation
- What you did:
  - Updated `app/retrieval.py` so normal vector search returns the vector hits plus the immediately preceding and following page within the same document, when available.
  - Original vector hits remain first. Added pages carry their full page text and citation metadata and are marked with `adjacent: true` and `adjacent_to`. Repeated neighbors and pages already in the hit set are not added twice.
  - Graph retrieval continues to seed its traversal from raw vector hits, rather than treating added context pages as vector-search seeds.
  - Added a focused unit test covering neighbor expansion, deduplication, and document boundaries.
- Comparison question and conditions held fixed:
  - Planned question: `In Lecture 02, what does LoRA freeze and what does it train? What does QLoRA add?`
  - Intended conditions: same model and Lecture 01–03 target materials before and after the retrieval change.
  - The before/after live comparison was not run because the Codespace was full; the model and execution conditions could not be verified.
- Results:
  - The code and focused test were added, but the test was not executed in this session. No claim is made that the test passed.
  - Direct inspection of `lec02-main-p052` confirms the source evidence: LoRA freezes the original weights and trains the low-rank A/B change; QLoRA stores the frozen weights at 4 bits.
  - Before/after agent answers, retrieval traces, time, token counts, and estimated generation API costs were not collected.
- Examples of improvements and remaining failures or limitations:
  - Intended improvement: if useful context is on a neighboring page, adjacent-page expansion makes that text available alongside the vector hit.
  - This benefit has not been demonstrated by a live comparison. Added neighboring pages can be irrelevant and increase model input tokens. Run the focused test and the same before/after question in a working Python 3.12 Codespace to validate behavior and measure results.
- Observations and questions:
  - The retrieval implementation is present, but answer-quality improvement remains unverified because the before/after comparison could not be run.
