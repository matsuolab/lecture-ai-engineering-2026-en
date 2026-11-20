# Lecture 02 Answers

## Exercises

- Model and settings used (from `config` in `result.json`):
- Did you run training yourself (`executed_training_myself`): Yes / No (how far you ran the notebook: )
- Before training: `format_rate` = / `content_rate` =
- After training: `format_rate` = / `content_rate` =
- Questions that regressed:
- Failures remaining after training and their types (assertion without evidence / evasion through a confirmation request despite evidence being present / broken format):
- Results of knowledge questions (section 6; classification before → after training) and observations:
- What changed and what stayed the same with training:

## Homework

- Level attempted: Basic
- Settings or data changed: Changed only `num_train_epochs`, from 20 (original) to 10. `lr`, `lora_r`, seed, and data were identical. I restarted the session and ran from the top for each run.
- Results (comparison tables or numbers):

  | Setting | `format_rate` | `content_rate` | `both_rate` | Final loss | Train time |
  |---|---:|---:|---:|---:|---:|
  | Before training | 0.952 | 0.381 | 0.381 | — | — |
  | 10 epochs | 1.000 | 0.905 (19/21) | 0.905 | 0.0665 (step 20) | 99 s (20 steps) |
  | 20 epochs (original) | 1.000 | 0.952 (20/21) | 0.952 | 0.0148 (step 40) | 207 s (40 steps) |

  Neither run had regressions. Both fixed the format, taking `format_rate` from 0.952 before training to 1.000 after. Content accuracy rose from 0.381 to 0.905 with 10 epochs and 0.952 with 20. The longer run reduced the final loss from 0.0665 to 0.0148 and took about twice as long, for one extra correct test question out of 21. A one-question gap could be run-to-run noise because GPU training is not perfectly reproducible, so I cannot claim 20 epochs is clearly better. The loss was already low at 10 epochs, and most of the gain came early.

  In both runs, the model asserted the regular deadline with `needs_review: false` for "When is the final assignment deadline for this course?", a question the FAQ does not answer. The 20-epoch model reproduced the training wording more exactly: "Confirmation from the course organizers" instead of "from the instructor" for the instructor-name question. More epochs made the output more consistent but did not teach the model to judge whether the FAQ contains evidence. I ran both training runs on a T4; I checked the scores in `result.json` and the loss and time in the section 4 output. I did not verify which test question differs between runs because I have not checked the `eval_after` detail files.
- Discussion of when fine-tuning is and is not suitable: Fine-tuning fitted well here for learning a fixed output format and wording: 14 examples and under 4 minutes took format compliance to 100%. It is not suitable when the model must know changing facts or judge whether evidence exists, such as deadlines. Retrieval or putting the source in the prompt is better for those cases because the source can be updated without retraining and answers can cite where the information came from. A sensible combination is to fine-tune for format and style and use retrieval for facts.
