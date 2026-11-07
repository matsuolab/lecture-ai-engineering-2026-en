# Lecture 02 Answers

## Exercises

- Model and settings used (from `config` in `result.json`):
  - Base Model: `Qwen/Qwen3.5-0.8B` (Revision: `2fc06364715b967f1860aea9cf38778875588b17`)
  - LoRA settings: r = 32, alpha = 32, lr = 0.0002, num_train_epochs = 20
- Did you run training yourself (`executed_training_myself`): Yes
- Before training: `format_rate` = 0.9524 / `content_rate` = 0.3810
- After training: `format_rate` = 1.0 / `content_rate` = 0.9048
- Questions that regressed: None (`[]`)
- Failures remaining after training and their types (assertion without evidence / evasion through a confirmation request despite evidence being present / broken format):
  - A few ungrounded questions still failed because the model made assertions instead of requesting confirmation (`needs_review: true`) when the answer was not present in the FAQ.
- Results of knowledge questions (section 6; classification before → after training) and observations:
  - "When is the final assignment deadline for this course?": asserted → asserted
  - "What is the instructor's name?": needs_review → needs_review
  - "What is the topic of the next lecture?": needs_review → needs_review
  - "When is the assignment deadline?" (Control): asserted → asserted
  - Observation: The base model already had strong formatting ability, and LoRA improved format consistency and style matching, but it did not reliably prevent unsupported factual assertions on questions outside the FAQ.
- What changed and what stayed the same with training:
  - "Changed": Response format became more consistent and matched the FAQ style more closely.
  - "Stayed the same": The model still tended to assert unsupported facts on ungrounded knowledge questions; refusal behavior did not substantially improve.

## Homework

- Level attempted: Implementation
- Settings or data changed:
  - Replaced the course FAQ with a custom **Python Coding Club FAQ** (5 items covering membership, meetings in Room 402, GitHub projects, beginner workshops, and Slack/email contact).
  - Prepared 8 custom ungrounded validation/test questions on topics not in the FAQ (certification, laptop requirements, 1-on-1 mentoring, attendance, etc.).
- Results (comparison tables or numbers):
  - `before_custom`: format_rate = 1.0, content_rate = 0.8095, both_rate = 0.8095
  - `after_custom`: format_rate = 1.0, content_rate = 0.9048, both_rate = 0.9048
- Discussion of when fine-tuning is and is not suitable:
  - "Suitable": For training a model to adopt a strictly defined response format (like JSON schema), a specific tone, and to repeat structured, predictable domain language (like FAQ contents).
  - "Not Suitable": For imparting hard, factual truth boundaries or preventing hallucinations on questions that lie outside the context (ungrounded inputs). For that, a search-based system (RAG) is far more robust.

- Update Lecture 02 answers
