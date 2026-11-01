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
    }
- Did you run training yourself (`executed_training_myself`): Yes (I ran session 0-8 )
- Before training:
  - format_rate = 20/21 = 95,24%
  - content_rate = 8/21 = 38,10%
  - both_rate = 8/21 = 38,10%

- Observations before training:
  - Only one answer presented invalid format: missing_key. 
    needs_review in "Where should I submit my work?".
  - Lots of answer contained correct information from FAQ, but needs_review = true. 
  - In the question regarding character limit, the model recognised the lack of information and checked needs_review = true, and received content = fail. 

- After training: `format_rate` = 100% (21/21) / `content_rate` = 90,48% (19/21)
- Questions that regressed:
- Failures remaining after training and their types (assertion without evidence / evasion through a confirmation request despite evidence being present / broken format):
- Results of knowledge questions (section 6; classification before → after training) and observations:
- What changed and what stayed the same with training:

## Homework

- Level attempted: Basic / Implementation / Advanced
    Basic:

- Settings or data changed:
- Results (comparison tables or numbers):
- Discussion of when fine-tuning is and is not suitable:
