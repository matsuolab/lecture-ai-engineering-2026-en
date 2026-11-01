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

- Level selected: Basic.
- Settings or data changed: 
- Results available so far:

Discussion of when fine-tuning is and is not suitable: