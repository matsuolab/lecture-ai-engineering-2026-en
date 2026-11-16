# Lecture 04 Answers

## Submission status: not yet complete

The existing labels and judge summary in this repository were not produced by a verified human annotation session or by running the grading command. Do not treat their judgments, agreement numbers, review counts, or claimed before/after results as real experimental results. The label file has been cleared, and the judge-result file is marked as not run so they cannot be mistaken for verified output.

The Grounding policy change in `data/eval/rubric.md` is the rubric revision selected for this exercise. It says that a general explanation of a term may pass after the answer clearly states that the term is absent from the glossary, as long as it is presented as general information rather than as a confirmed course fact.

## What remains to do

1. In Codespaces, run `uv run --with streamlit==1.66.1 streamlit run tools/annotate.py` and label all ten cases yourself. Save the labels to `lectures/04/labels.jsonl`.
2. Run the judge against your labels. With the course API key configured, use `uv run python -m app.judge`. `--model test` is only a fake-model workflow check; it is not real LLM grading.
3. Record the actual criterion agreement, review items, and disagreements from the command output in this file. Do not fill in results until you have run it.
4. For a valid before/after comparison, run the grader once with the original rubric and once with the revised rubric, using the same labels and cases, and record both outputs. The original rubric can be retrieved from the starting commit with `git show 1263162748be8094b6f85687fcee119ed2c9aad9:data/eval/rubric.md`.
5. Run `uv run python -m app.judge --compare lectures/04/reference/labels_instructor.jsonl` and note any differences from your labels.

## Exercises

- Agreement by criterion before rubric revision: pending a real run
- Number of items needing review before revision: pending a real run
- Criterion revised: Grounding
- Policy added: A general explanation after explicitly stating that a term is not in the glossary is acceptable as general information, unless the answer presents it as a confirmed fact.
- Agreement by criterion and number of review items after revision: pending a real run
- Differences from instructor labels and reasons: pending your annotation and comparison
- Observations and questions: pending results

## Homework

- Level attempted: Basic
- What you did: Revised one Grounding policy in `data/eval/rubric.md`.
- Results: Not yet measured. Run the baseline and revised-rubric evaluations on the same human labels before reporting a change in agreement.
- Observations and questions: The rubric policy is now explicit, but its effect on agreement must be established by running the grader; no performance improvement is claimed here.
