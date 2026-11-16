# Lecture 04 Answers

## Submission status: not complete

The Grounding policy in `data/eval/rubric.md` has been clarified. However, the required human labeling and LLM grading have not been performed in this Codespace, so there are no verified agreement or before/after results to report. Earlier labels and judge output in the repository were unverified; the labels file is being cleared and `judge_result.json` is marked `not_run`. Do not submit invented or placeholder results as measured findings.

## Exercises

- Agreement by criterion before rubric revision: pending a real run
- Number of items needing review before revision: pending a real run
- Criterion revised: Grounding
- Policy added: A general explanation after explicitly stating that a term is not in the glossary is acceptable as general information unless presented as a confirmed course fact.
- Agreement by criterion and number of review items after revision: pending a real run
- Differences from instructor labels and reasons: pending annotation and comparison
- Observations and questions: pending actual results

## Homework

- Level attempted: Basic
- What I changed: Clarified one Grounding policy in `data/eval/rubric.md`.
- Results: Not measured. Run both baseline and revised-rubric grading on the same human labels before reporting a change in agreement.
- Observations: The policy is now more explicit, but its effect on agreement has not been tested.

## To finish

1. In the repository Codespace, run `uv run --with streamlit==1.66.1 streamlit run tools/annotate.py`, label all ten cases, and save `lectures/04/labels.jsonl`.
2. Run `uv run python -m app.judge` with the course API key configured. `--model test` is a fake workflow check, not real LLM grading.
3. Run `uv run python -m app.judge --compare lectures/04/reference/labels_instructor.jsonl`.
4. For a before/after comparison, run the grader with the original rubric and the revised rubric on the same labels, then replace the pending fields above with the actual output.
