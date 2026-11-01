# Lecture 02 Answers

## Exercises

- Model and settings used (from `config` in `result.json`):
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
    "gen": {
      "do_sample": false
  
- Did you run training yourself (`executed_training_myself`): Yes. I ran the notebook in Google Colab using a T4 GPU, including the LoRA training process in Section 4, followed by the evaluation and result generation in Sections 5–7
- Before training: `format_rate` = / `content_rate` = 0.9523809523809523 / 0.38095238095238093
- After training: `format_rate` = / `content_rate` = 1.0 / 0.8571428571428571
- Questions that regressed: none
- Failures remaining after training and their types (assertion without evidence / evasion through a confirmation request despite evidence being present / broken format):

3/21 failed content evaluation (no broken format, 2 out 3 evasion through a confirmation request despite evidence being present,  1 assertion without evidence) :
1. Can I submit a format other than PDF? 
-> model still asked for confirmation. 
-> Expected is (before training): No, you cannot submit a format other than PDF. The FAQ explicitly states that the assignment must be submitted as one PDF file named student_id_assignment_number.pdf.

2. Tell me how submissions after the deadline are handled?
-> model still asked for confirmation.
-> Expected is (before training): ate submissions are accepted within 48 hours of the deadline, with a grade penalty.

3. Do office hours require an appointment?
-> model answered with office hour schedule and needs_review false
Expected is (before training): no

- Results of knowledge questions (section 6; classification before → after training) and observations

| Question | Before | After | Interpretation |
|---|---|---|---|
| Final assignment deadline | `asserted` | `asserted` | Remained an unsupported assertion. |
| Instructor's name | `needs_review` | `needs_review` | Correctly recognized missing information. |
| Next lecture topic | `needs_review` | `needs_review` | Correctly recognized missing information. |
| Assignment deadline (control) | `asserted` | `asserted` | Correctly answered using information available in the FAQ. |

All four questions retained the same classification before and after LoRA training

- What changed and what stayed the same with training
  
| Metric | Before training | After training |
|---|---:|---:|
| Format rate | 95.24% | 100% |
| Content rate | 38.10% | 85.71% |
| Both rate | 38.10% | 85.71% |
| Evaluation time | 31.8 seconds | 46.5 seconds |
| Questions passing both checks | 8/21 | 18/21 |

Training improved the model's performance: format rate increased from 95.24% to 100%, while content rate rose from 38.10% to 85.71%. Questions passing both checks increased from 8 to 18 out of 21. However, some unsupported answers and unnecessary confirmation requests remained. Evaluation time increased from 31.8 to 46.5 seconds.

## Homework

- Level attempted: Basic 
- Settings or data changed: epoch to 30
- Results (comparison tables or numbers): comparing between epoch 20 and epoch 30

| Evaluation Metric | Original (20 Epochs) | Modified (30 Epochs) | Improvement |
|---|---:|---:|---:|
| Format compliance | 100% (21/21) | 100% (21/21) | No change |
| Content accuracy | 85.71% (18/21) | 90.48% (19/21) | +4.76 percentage points |
| Both format and content correct | 85.71% (18/21) | 90.48% (19/21) | +4.76 percentage points |
| Evaluation time | 46.5 seconds | 39.0 seconds | 7.5 seconds faster |

1. Both still have format accuracy 100%
2. Content accuracy improved slightly
3. One previous incorrect question improved: "Tell me how submissions after deadline handled". Before need_review: true. After need_review: false. -> CORRECT
4. No new regressions

- Discussion of when fine-tuning is and is not suitable:

Fine-tuning is useful for teaching models specific response patterns, structured formats, and task-specific rules. In this experiment, LoRA achieved 100% format compliance and improved content accuracy from 85.71% to 90.48% after increasing training from 20 to 30 epochs.

It is suitable for:
- Enforcing structured outputs, such as JSON.
- Teaching task-specific response and classification rules.
- Improving consistency across paraphrased questions.
- Adapting models to specific domains or applications.
When fine-tuning is not sufficient
Fine-tuning does not guarantee factual reliability or prevent unsupported assumptions. Even after 30 epochs, the model still struggled to distinguish missing information from facts already provided in the FAQ.

It may be insufficient when:
- Answers require information absent from training data.
- The model must distinguish facts from assumptions.
- Information changes frequently.
- Incorrect answers could lead to misleading decisions.
In these cases, RAG, external knowledge sources, and human verification can complement fine-tuning.

Analyze and wording supported with ChatGPT, verified by checking the results with the JSON results and notebook manually
