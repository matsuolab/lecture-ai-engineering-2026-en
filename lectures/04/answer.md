# Lecture 04 Answers

## Exercises

### Setup
I labeled the ten provided cases and graded them using
gemini-3.5-flash-lite at temperature 0. I kept the labels,
model, and cases unchanged when revising the rubric.

### Results

| Criterion or measure | Before revision | After revision |
|---|---:|---:|
| Grounding agreement | 9/9 | 10/10 |
| Scope agreement | 10/10 | 10/10 |
| Hint agreement | 10/10 | 10/10 |
| Clarity agreement | 9/10 | 9/10 |
| Lecture marker agreement | 7/10 | 7/10 |
| Overall agreement | 7/9 | 7/10 |
| Automatic coverage | 90% | 100% |
| LLM needs-review items | 1 | 0 |

The denominators differ because the initial grader marked
case 05 Grounding as unsure.

### Rubric revision
I resolved the Grounding policy for absent terms: a general
explanation unsupported by the supplied references should fail,
even if the answer acknowledges that the term is absent.
I removed this issue from the unresolved questions section.

Case 05 changed from unsure to pass, contrary to the revised
policy. Its reasoning still referred to the case's older
expected-behavior wording about an unresolved policy.
This suggests that conflicting guidance affected the judgment,
but this single experiment does not establish the cause.

The increased coverage therefore did not demonstrate improved
grading correctness. Grounding agreement reached 10/10 because
my unchanged label for case 05 was also pass.

### Comparison with the instructor
Grounding, Scope, Hint, and Clarity matched the instructor
in all ten cases. Lecture-marker judgments matched in 7/10.

- Case 02: I marked pass, but the final-line marker was missing.
- Case 05: I marked fail because the lecture association was
  unsupported, while the format check passed the existing marker.
- Case 07: I accepted "Related session: none", while the code
  required a Lecture N marker.

These differences exposed confusion between a reference's
meaning and its format. A rigid marker requirement can reject
reasonable responses where no lecture applies.

Case 04 Clarity remained a disagreement with the LLM: I judged
the repeated explanations excessive, while the LLM judged
the answer concise. Clarity is informational and does not
affect the overall pass/fail result.

## Homework

### Level attempted
Implementation, plus the Basic rubric-wording experiment.

### What I did
I brought my completed Lecture 03 agent into this branch,
including make_quiz and the approval-gated save_learning_log.
All 15 existing tests passed after restoring the agent files.

I authored ten custom questions and expected behaviors:
1. LoRA frozen and trainable parameters.
2. A false premise about QLoRA.
3. A spelling variation of Low-Rank Adaptation.
4. A quiz request that withholds the answer.
5. An invented course term.
6. A request for complete homework code.
7. An unrelated recipe request.
8. An instruction to abandon the course-support role.
9. Ambiguous input.
10. A nonexistent lecture.

I generated answers using my agent, labeled them separately,
and graded them using the revised rubric. I corrected an
accidental duplicate during authoring. Case 10 initially had
expected-behavior text pasted into its question field; I fixed
the question and regenerated only that answer before labeling.

The custom set does not test saving notes or interactive
approval. Those behaviors require separate execution checks.

### Implementation results

| Criterion or measure | Result |
|---|---:|
| Grounding agreement | 9/10 |
| Scope agreement | 10/10 |
| Hint agreement | 10/10 |
| Clarity agreement | 10/10 |
| Lecture marker agreement | 10/10 |
| Overall agreement | 10/10 |
| Automatic coverage | 100% |
| LLM needs-review items | 0 |

These are agreement figures, not an agent success rate.

The agent supplied a recipe in case 07, violating course scope.
I also marked Grounding fail because the recipe was unsupported
by the supplied references. The LLM marked Grounding pass and
treated the problem as a Scope failure. Overall agreement
remained intact because other required criteria failed.

Case 10 had Grounding pass saved with unsure_flag=true.
I was uncertain whether its list of available sessions was
supported, since the case supplied no glossary references.
The LLM marked Grounding pass. The reported agreement counted
the saved pass label; zero LLM review items did not mean that
I had no uncertainty. Tool-output evidence would help resolve it.

### Code versus LLM checks
Code is appropriate for deterministic properties: JSON schema,
required fields, unique case IDs, and the final-line Lecture N
pattern. Tests or execution traces are needed to verify tool
calls, approval decisions, and file writes.

An LLM can assist with semantic judgments such as consistency
with references, staying within scope, providing hints rather
than complete solutions, and readability. These judgments still
need human comparison and inspection of reasons.

A marker's presence can be checked by code, but its relevance
and factual support require separate evidence. Similarly,
a fluent answer can still violate scope or grounding.

### Limitations and observations
The set contains only ten cases and one completed grading run
per experimental condition. It cannot establish broad reliability.
The agent and grader used the same model family, which may
produce shared blind spots. High agreement can also reflect
shared mistakes rather than correct judgments.

AI assistance was used to draft cases and expected behaviors,
suggest labels, interpret results, and prepare this report.
The labels should therefore be described as AI-assisted,
not an independent human-only baseline.

Service-busy 503 errors interrupted grading. The final custom
run completed with a two-second pause between cases.
