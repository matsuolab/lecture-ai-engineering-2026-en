# Lecture 04 Answers

## Exercises

- Agreement by criterion (before revision): Grounding 9/10, Scope 10/10, Hint 10/10, Clarity 9/10, Lecture marker 7/10.
- Number of items needing review (before revision): 0.

- Criterion revised and the policy added:
  I revised Clarity by adding: “Repeating the same explanation with ‘In other words’ two or more times is excessive repetition and must fail Clarity, even if the answer remains readable.”
- Agreement by criterion and number of review items (after revision):
  Grounding 10/10, Scope 10/10, Hint 10/10, Clarity 10/10, Lecture marker 7/10. No items required review. Overall agreement remained 9/10, with 100% automatic coverage.
- Items where my labels differed from the instructor's, and their reasons:
  - Case #07, Lecture marker: I marked pass because indicating no related session seemed appropriate for an out-of-scope question. However, the implemented rule requires a literal “Lecture N” marker, so the instructor marked fail.
  - Case #08, Grounding: I marked fail because the answer followed a request to abandon the agent's role. The instructor marked pass because the glossary content itself was accurate. This helped me understand that role compliance belongs to Scope and that each criterion should be judged independently.
  - Cases #08 and #10, Lecture marker: I marked fail because I considered the answer's suitability or the validity of the session number. The implemented check only looks for “Lecture N” in the final line, so these cases pass that criterion.
- Observations and questions:
  - Clarity agreement increased from 9/10 to 10/10 after the rubric revision.
  - Grounding agreement also increased, although I did not change that criterion. This change cannot be directly attributed to the Clarity revision; repeated runs would be needed to investigate its cause.
  - Overall agreement remained 9/10. Clarity is informational and does not affect the overall result.
  - I marked case #05 as Unsure, but the LLM returned no unsure judgments. But I realised that the absence of review items does not necessarily mean that the rubric has no ambiguity.
  - The lecture marker check is deterministic but limited: it checks the marker's format rather than whether the session exists or is relevant.

## Homework

- Level attempted: Basic

- What you did:
  I added one new rule under Clarity: "simple definition answers longer than 80 words must fail, excluding the final lecture marker line". I kept the same cases, human labels, model, and other rubric rules. I compared basic_length_result.json with judge_after.json.

- Results:
    Below are the results obtained:

  | Measure | Before | After |
  |---|---|---|
  | Grounding agreement | 10/10 | 7/9 |
  | Scope agreement | 10/10 | 10/10 |
  | Hint agreement | 10/10 | 10/10 |
  | Clarity agreement | 10/10 | 9/10 |
  | Lecture marker agreement | 7/10 | 7/10 |
  | Review items | 0 | 1 |
  | Overall agreement | 9/10 | 8/9 |
  | Automatic coverage | 100% | 90% |

- Observations and questions:
  - The revised rubric produced lower agreement with my labels and lower coverage in this run.
  - Case #05 received unsure for Grounding because the rubric explicitly leaves general explanations of absent terms unresolved. This also matched the uncertainty I had flagged during annotation.
  - In case #08, the evaluator used role compliance as a reason to fail Clarity, despite the instruction to judge readability independently.
  - One before-and-after comparison is insufficient to establish a consistent effect. Repeated runs would help distinguish a rubric effect from variation between evaluations.

- Conclusions:
The added 80-word limit did not improve agreement with my labels in this run. Clarity agreement decreased from 10/10 to 9/10, while automatic coverage dropped from 100% to 90%. The evaluator also mixed criteria, using homework-answer disclosure to judge Grounding and role compliance to judge Clarity. The experiment shows that more explicit rubric wording does not guarantee better grading, inspecting the evaluator’s reasons and repeating evaluations are necessary to assess its reliability.