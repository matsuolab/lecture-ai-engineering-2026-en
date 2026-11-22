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
- **Level attempted:** Basic

- **What you did:**
  Made a small modification to `app/agent.py` to improve how the agent handles questions containing multiple parts. The agent is now instructed to verify each requested part separately against retrieved evidence and clearly identify anything that cannot be verified instead of making unsupported assumptions.

- **Comparison question and conditions held fixed:**
  Question: "In Lecture 02, what does LoRA freeze and what does it train? What does QLoRA add?"

  The following conditions were kept constant:
  - Model: `gemini-3.5-flash-lite`
  - Question: Same question for every run.
  - Target material: Lecture 02.
  - Environment and API configuration: Unchanged.
  
  Different retrieval approaches were tested to observe their effect on answer quality, execution time, token usage and cost.

- **Results:**

  | Method | Time (s) | Input tokens | Output tokens | Estimated cost (USD) |
  |---|---:|---:|---:|---:|
  | Standard retrieval | 4.82 | 2,837 | 194 | 0.001336 |
  | Full context | 4.56 | 95,824 | 134 | 0.029082 |
  | Graph retrieval | 15.35 | 5,190 | 229 | 0.002130 |

  All three approaches returned answers identifying that LoRA freezes the original pretrained weights and trains small low-rank matrices A and B, while QLoRA additionally uses 4-bit quantization to reduce memory requirements.

- **Examples of improvements and remaining limitations:**
  The modified instruction encourages the agent to address every part of a question independently and avoid unsupported conclusions. The retrieval-based approaches also provide relevant lecture references.

  Full-context processing uses considerably more input tokens and has a higher estimated generation cost. Graph retrieval involves additional navigation steps and takes longer. Standard retrieval was faster in this particular test.

  The experiment uses only one comparison question, so the results do not establish that one approach is universally better.

- **Observations and questions:**
  The experiment showed that providing more context does not necessarily produce a proportionally better answer. Standard retrieval provided a useful balance between response quality, execution time and cost for this question.

  A useful next step would be to test the modified instructions on questions involving more topics and multiple lecture sections.
