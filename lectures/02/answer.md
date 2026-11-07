# Lecture 02 Answers

## Exercises

- Model and settings used (from `config` in `result.json`):
  - Base Model: `Qwen/Qwen3.5-0.8B` (Revision: `2fc06364715b967f1860aea9cf38778875588b17`)
  - LoRA settings: r = 32, alpha = 32, lr = 0.0002, num_train_epochs = 20
- Did you run training yourself (`executed_training_myself`): Yes
- Before training: `format_rate` = 1.0 / `content_rate` = 0.8095
- After training: `format_rate` = 1.0 / `content_rate` = 0.9048 
- Questions that regressed: None (`[]`)
- Failures remaining after training and their types (assertion without evidence / evasion through a confirmation request despite evidence being present / broken format):
  - A few ungrounded questions (where `needs_review: true` was expected) still failed because the model made assertions instead of requesting confirmation (assertion without evidence).
- Results of knowledge questions (section 6; classification before → after training) and observations:
  - "When is the final assignment deadline for this course?": asserted → asserted
  - "What is the instructor's name?": asserted → asserted
  - "What is the topic of the next lecture?": asserted → asserted
  - "When is the assignment deadline?" (Control): asserted → asserted
  - "Observation": The base model already formatting JSON perfectly. LoRA training styled the answers to copy the FAQ style but did not teach the model to refuse ungrounded real-world knowledge questions, continuing to output 'asserted' for facts absent from the context.
- What changed and what stayed the same with training:
  - "Changed": Wording style matches the new custom Python Coding Club FAQ perfectly.
  - "Stayed the same": The base model already had a 1.0 format rate, which remained at 1.0. Its tendency to hallucinate answers on ungrounded/knowledge-base questions also stayed the same.
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
