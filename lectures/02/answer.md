# Lecture 02 Answers

## Exercises

Model and settings used (from [result.json](../../notebooks/baseline/result.json)):

```json
{
  "base_model": "Qwen/Qwen3.5-0.8B",
  "revision": "2fc06364715b967f1860aea9cf38778875588b17",
  "seed": 42,
  "num_train_epochs": 20,
  "warmup_steps": 6,
  "lr": 0.0002,
  "lora_r": 16,
  "lora_alpha": 32,
  "max_seq_len": 512,
  "max_new_tokens": 96,
  "gen": {"do_sample": false}
}
```

- Did you run training yourself (`executed_training_myself`): Yes. I ran sections 0–8, including training and the optional 4-bit comparison.
- Method: LoRA without quantization. Only 6,389,760 parameters (0.8421% of the total) were trainable; the base-model weights remained frozen.
- Training completed in 193 seconds, with 40 steps over 20 epochs.

Before training: 

```json
{
  "format_rate": "95.24% (20/21)",
  "content_rate": "38.10% (8/21)",
  "both_rate": "38.10% (8/21)",
}
```



After training:

```json
{
  "format_rate": "100% (21/21)",
  "content_rate": "90.48% (19/21)",
  "both_rate": "90.48% (19/21)",
}
```

Observations before training:

- Only one answer had an invalid format: `needs_review` was missing from the response to “Where should I submit my work?”.
- Several answers contained correct information from the FAQ but incorrectly set `needs_review` to `true`.
- The model made unsupported assertions about recordings, feedback, citation style, and appointments.
- For the character-limit question, the model recognized the lack of information and set `needs_review=true`, but received `Content=Fail` because the evaluator requires the keyword “Confirmation”. This illustrates a limitation of keyword-based scoring.

Questions that regressed: 

None (`regressed = []`). No question that passed both format and content before training failed afterward.

Failures remaining after training:

"Can I submit a format other than PDF?" => (Observed Behaviour) Requested confirmation with `needs_review=true`, although the FAQ specifies PDF. (Failure Type) Evasion despite evidence being present;

"Do office hours require an appointment?" => (Observed Behaviour) Returned the office-hours schedule with `needs_review=false`, although the FAQ does not specify whether appointments are required. => (Failure Type) Assertion without evidence; reused a related FAQ item 

There were no remaining format failures.

### Results of knowledge questions (section 6):

- "When is the final assignment deadline for this course?"
    - (`asserted` -> `asserted`)
    - Reused the general assignment deadline, although the exercise treats the final-assignment question as absent from the FAQ. Training did not resolve this distinction.

- "What is the instructor's name?"
    - (`needs_review` -> `needs_review`)
    - Before training, answered “None” with the review flag set. After training, explicitly stated that the FAQ lacks the information and requested confirmation.

- "When is the assignment deadline?"
    - (`asserted` -> `asserted`)
    - Correctly answered the FAQ-covered control question before and after training. An assertion is appropriate here because evidence is present.


- Similarities and changes with training:

Training made the JSON format consistent and increased measured content accuracy from 38.10% to 90.48%. Answers also became more similar to the training targets. The logged training loss decreased from 1.691805 at step 10 to 0.014992 at step 40.

However, the model still sometimes confused related information with sufficient evidence, or requested confirmation despite having evidence. Learning the output format and reproducing training text did not guarantee reliable judgment about whether the FAQ supports an answer.

Optional section 8 observation:

Loading the base model in 4-bit without training produced a `format_rate` of 100% (21/21), but a `content_rate` of only 4.76% (1/21). Compared with the before-training results, this run preserved the requested format while  reducing measured accuracy.

Saved results: [before-training outputs](../../notebooks/baseline/eval_before.json), [after-training outputs](../../notebooks/baseline/eval_after.json), [4-bit outputs](../../notebooks/baseline/eval_before_4bit.json), and [executed notebook](../../notebooks/baseline/lora_format_tuning_final_exec.ipynb).

## Homework

- Levels completed: Basic and Implementation.

### Basic
- Settings or data changed: Changed only `num_train_epochs` from 20 to 10. The dataset and other CONFIG settings remained the same.
- Results:

| Metric | Baseline (20 epochs) | Basic (10 epochs) |
| --- | --- | --- |
| Optimizer steps | 40 | 20 |
| After-training format rate | 100% (21/21) | 100% (21/21) |
| After-training content rate | 90.48% (19/21) | 90.48% (19/21) |
| Last logged training loss | 0.014992 | 0.070625 |
| Training time | 193 seconds | 102 seconds |
| Regressions | None | None |

The 10-epoch run achieved the same aggregate test scores in 91 fewer seconds. Its last logged training loss was higher, but the lower loss of the 20-epoch run did not translate into better test accuracy. For this small evaluation set, the extra epochs provided no measured accuracy benefit. This does not establish that 10 epochs is optimal for other datasets or runs.

Evidence: [executed Basic notebook](../../notebooks/basic/lora_format_tuning_basic.ipynb), [10-epoch results](../../notebooks/basic/result%281%29.json), [before-training outputs](../../notebooks/basic/eval_before%281%29.json), and [after-training outputs](../../notebooks/basic/eval_after%281%29.json).

Discussion of when fine-tuning is and is not suitable:

Fine-tuning was useful for learning the required JSON structure and more consistent responses: both runs achieved 100% format compliance and improved content accuracy from 38.10% to 90.48%. The comparison also shows why training loss alone is insufficient when choosing training duration, evaluation on held-out questions matters.

Fine-tuning alone did not guarantee reliable judgment about missing evidence. The baseline still requested confirmation for a question covered by the FAQ and asserted an answer to a question without evidence. For facts that change frequently, supplying current source material through retrieval is more direct than retraining for every update, although the model's interpretation of that evidence still needs evaluation. These conclusions are limited by the small, fictional FAQ and the keyword-based content metric.

### Implementation: fictional library FAQ

I ran the adapted library notebook myself, including training and the optional 4-bit comparison. The topic was changed from course assignments to five fictional library rules: a 14-day loan period, a maximum of 3 books, returns at the front desk, weekday opening hours, and one renewal through the library portal. The original model, 20 epochs, and other baseline CONFIG settings were retained. The JSON output structure and `needs_review` design were unchanged.

The dataset contained 14 training, 7 validation, and 21 test examples. Grounded questions paraphrased the five rules, with different question templates across splits. Questions without evidence concerned policies deliberately omitted from the FAQ, including fines, membership, reservations, and exceptions such as after-hours returns or renewing a reserved book. A related rule was not treated as evidence for an unspecified exception. These questions were assigned `needs_review=true` and a confirmation request as the target answer.

| Metric | Before training | After training |
| --- | --- | --- |
| Format rate | 100% (21/21) | 100% (21/21) |
| Content rate | 42.86% (9/21) | 95.24% (20/21) |
| Both format and content | 42.86% (9/21) | 95.24% (20/21) |

Training completed in 158 seconds over 40 steps and 20 epochs. The logged loss decreased from 1.522592 at step 10 to 0.016341 at step 40. There were no regressions.

The only remaining failure was “When must I return a book after borrowing it?”. The model answered “Return borrowed books at the front desk.” with `needs_review=false`, giving the return location instead of the 14-day duration. This was a content error caused by selecting the wrong FAQ rule, despite valid formatting. All six test questions without evidence passed after training.

In section 6, the three unknown questions about the director's name, home delivery, and damaged books remained classified as `needs_review` before and after training. However, the before-training home-delivery answer was “No” despite its review flag being true. After training, it requested confirmation. This shows why the classification alone does not capture every problem in the answer text. The known loan-duration control remained `asserted` and correctly answered 14 days.

The optional untrained 4-bit model achieved 100% format compliance but only 14.29% content accuracy (3/21), compared with 42.86% for the unquantized base model. This observation concerns quantization in this run.

This experiment demonstrates improved content selection and confirmation wording even when format compliance was already perfect. The remaining error shows that training does not guarantee selection of the correct supporting fact. Its 95.24% post-training score should not be interpreted as proof that the library topic is easier than the course FAQ: the questions and expected keywords differ and both test sets used are small.

Saved Results: [Implementation results](../../notebooks/implementation/result%282%29.json), [before-training outputs](../../notebooks/implementation/eval_before%282%29.json), [after-training outputs](../../notebooks/implementation/eval_after%282%29.json), [4-bit outputs](../../notebooks/implementation/eval_before_4bit%282%29.json), and [executed notebook](../../notebooks/implementation/lora_library_implementation_colab_run.ipynb).
