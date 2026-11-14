# Lecture 04 — Basic Homework Solutions 

## Level completed
Basic

## Objective
Evaluate the learning support agent using an LLM-as-a-Judge and compare its judgments with human labels.

## Work completed
- Reviewed the Lecture 04 grading rubric.
- Resolved the Grounding criterion policy for terms absent from the glossary.
- Allowed general explanations when the answer explicitly identifies the term as absent from the glossary and distinguishes general information from course-specific claims.
- Evaluated 10 test cases using Gemini 3.5 Flash Lite.
- Compared LLM judgments with human labels.

## Results

| Criterion | Agreement |
|---|---:|
| Grounding | 10/10 |
| Scope | 10/10 |
| Hint | 10/10 |
| Clarity | 10/10 |
| Lecture marker | 8/10 |
| Overall | 9/10 |

Coverage: 10/10 cases.

Cases requiring human review: 0.

## Observations
The LLM achieved complete agreement with human labels across all four LLM-judged criteria.

Two disagreements occurred in the automated lecture-marker criterion (#07 and #10). These indicate limitations in the code-based marker validation compared with human judgments.

The revised Grounding policy resolved the ambiguity concerning general explanations of terms absent from the glossary.

## Conclusion
The Basic homework evaluation was completed successfully. The experiment demonstrated how LLM-as-a-Judge can evaluate agent responses against explicit criteria and how agreement analysis can identify areas requiring further refinement.

# Lecture 04 Answers

## Exercises

- **Agreement by criterion (before revision):**
  - Grounding: 8/9
  - Scope: 10/10
  - Hint: 10/10
  - Clarity: 9/10
  - Lecture marker: 8/10

- **Number of items needing review (before revision):** 1 (#05, Grounding). The LLM marked it unsure because the rubric did not resolve whether a general explanation of a term absent from the glossary was acceptable.

- **Criterion revised and the policy added:**

  Revised the Grounding criterion to clarify how to handle terms absent from the glossary.

  A general explanation is acceptable if the answer explicitly states that the term is absent from the glossary and clearly distinguishes general information from course-specific information. No unsupported course-specific claims should be made.

- **Agreement by criterion and number of review items (after revision):**
  - Grounding: 10/10
  - Scope: 10/10
  - Hint: 10/10
  - Clarity: 10/10
  - Lecture marker: 8/10
  - Overall agreement: 9/10
  - Items needing review: 0
  - Coverage: 10/10 cases (100%)

- **Items where your labels differed from the instructor's, and your reasons:**

  The instructor comparison was performed using:

  `uv run python -m app.judge --compare lectures/04/reference/labels_instructor.jsonl`

  Agreement with instructor labels:

  | Criterion | Agreement |
  |---|---:|
  | Grounding | 10/10 |
  | Scope | 10/10 |
  | Hint | 10/10 |
  | Clarity | 9/10 |
  | Lecture marker | 8/10 |

  Three differences were identified:

  1. **Case #04 — Clarity:** My judgment was pass, whereas the instructor marked fail. The answer contained correct information but was verbose and repeated explanations, reducing conciseness.

  2. **Case #07 — Lecture marker:** My judgment was pass, whereas the instructor marked fail. The response correctly refused an out-of-scope request, but the automated code check required a Lecture N marker. This demonstrates that the marker validation rule can be overly rigid.

  3. **Case #10 — Lecture marker:** My judgment was fail, whereas the instructor marked pass. The answer incorrectly claimed that Lecture 14 content was planned to be added, although the course contains only 13 sessions. The instructor's judgment was based on the deliberately introduced failure in the response, while the marker criterion was checked separately by code.

  Case #05 was marked unsure by me because the initial Grounding policy did not resolve the ambiguity.

- **Observations and questions:**

  The revised Grounding policy resolved the ambiguity concerning general explanations of terms absent from the glossary. After revision, all four LLM-judged criteria achieved 10/10 agreement with my labels.

  The instructor comparison revealed three differences, mainly involving clarity and automated lecture-marker validation.

  This exercise demonstrated the importance of precise rubric definitions, independent criterion evaluation, and human review of automated judgments.

## Homework

- **Level attempted:** Basic

- **What you did:**

  1. Reviewed the Lecture 04 evaluation workflow and grading rubric.
  2. Annotated all 10 evaluation cases using the labeling interface.
  3. Revised the Grounding policy to resolve an ambiguous rubric condition.
  4. Used Gemini 3.5 Flash Lite as the LLM judge.
  5. Executed the evaluation using `uv run python -m app.judge`.
  6. Compared LLM judgments against human labels.
  7. Compared personal labels against instructor labels.
  8. Generated and inspected the evaluation results stored in `lectures/04/judge_result.json`.

- **Results:**

  | Criterion | Agreement |
  |---|---:|
  | Grounding | 10/10 |
  | Scope | 10/10 |
  | Hint | 10/10 |
  | Clarity | 10/10 |
  | Lecture marker (code) | 8/10 |
 