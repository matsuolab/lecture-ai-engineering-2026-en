# English exercise corpus review

Review date: 2026-11-19. Canonical source: Japanese `data/rag_data/lectures.json` at commit `1ce722c2816b70ef62891a6378b2478af555e3fd`, preserved locally in `source-documents.json`.

## Deliverables and completeness

- `lec03-exercise.json`: all 26 canonical pages, one section, every original page ID and page number retained. All 26 uploaded English exercise slides are mapped once, in their true presentation order.
- `lec04-exercise.json`: all 23 canonical pages, one section, every original page ID and page number retained. Twenty uploaded English slides are mapped once; canonical pages 3 and 9 are section dividers and page 23 is a logo, newly translated from the Japanese source because no matching English slide exists.
- Separate `lec03-exercise-provenance.json` and `lec04-exercise-provenance.json` preserve every actual uploaded filename/slide mapping, original text hashes, canonical text hashes, source commit, removed boilerplate, and before/after corrections. The main lecture's `provenance.json` is untouched.
- `build_exercises.py` reproduces these outputs; `exercise-validation.json` records the structural checks and current output hashes.

All 49 Japanese canonical pages and all semantically mapped English slides were read. Every Japanese uploaded slide's visible text matches the corresponding canonical page after ignoring whitespace, bullet glyphs, and repeated institutional copyright. Explicit source transcriptions of logos and the evaluation screenshot are translated separately; unseen screenshot content was not inferred.

## Actual source mappings

Lecture 3 English source:
`day3/Lecture 3 - AI Agents/Exercises and Homework/pptx/Lecture 3 Exercises and Homework - AI Agents_en.pptx`, slides 1–26 → canonical 1–26. The alternative English deck was checked for the new page 2 warning; it omits it too.

Lecture 3 Japanese source:
`day3/第3回 演習・宿題：学習支援エージェントを作る.pptx`, slides 1–26.

Lecture 4 English source:
`day4/Lecture_4_Exercise_Homework.pptx`.

| Canonical Japanese pages | Actual English slides |
| --- | --- |
| 1–2 | 1–2 |
| 3 | None; new translation of section divider |
| 4–8 | 3–7 |
| 9 | None; new translation of section divider |
| 10–22 | 8–20 |
| 23 | None; new translation of explicit logo transcription |

Uploaded English slide 21 is an extra summary absent from the canonical Japanese source. It was excluded and was not falsely mapped to the closing Japanese logo. Canonical page numbers must not be used as English physical slide numbers without this mapping.

Lecture 4 Japanese source:
`day4/第4回 演習・宿題：評価セットを作り、LLM に採点させる.pptx`, slides 1–23.

## Corrections and intentional localizations

There are 12 documented corrections/localizations in Lecture 3 and 24 in Lecture 4. Full before/after text is in the page-level provenance.

Lecture 3:

- Page 1 restores the source's explicit logo transcription.
- Page 2 restores the latest source's `Sync fork → Update branch` and `Discard commits` warning, including the alternative `lec03-start` workflow reference. Both English decks omit this addition.
- Page 6 restores the qualifier that using **only** unrelated questions is insufficient to test whether the model asks for confirmation or asserts.
- Page 13 retains the uploaded English deck's operational `lecture-ai-engineering-2026-en.git` URL. Pages 14, 15, 18 and 19 document the already-localized question prompts, commit message and comment; code flags, tool fields, arguments, IDs, and paths stay intact.
- Page 16 restores the truncated `INSTRUCTIONS` and `search_glossary` docstring using the complete reviewed English counterparts in the existing English course repository. No instructional policy is omitted. The source's historical “around line 31” is retained; the current code file has moved since the lecture. The docstring ellipsis is expanded from the actual existing English code, and closing quotes are restored for readability.
- Pages 17 and 23 restore Python indentation lost in slide text extraction without filling in the learner's implementation.
- Page 21 changes “and” to “or” because the source permits editing either `INSTRUCTIONS` or docstrings and requires comparing one change at a time.

Lecture 4:

- Page 1 restores the source's 40-minute duration and logo transcription. The uploaded English-only date, instructor and tagline are not carried into a canonical cover where they are absent.
- Pages 3, 9 and 23 are faithful new translations of unmatched canonical pages, not fabricated English-slide mappings.
- Page 4 restores “based on guesses” to avoid overstating the grounding instruction; page 6 avoids the English-only absolute “never” about `.gitignore` behavior.
- Pages 8 and 11 localize the lecture marker to `Lecture N`, as the actual English rubric and code do. Page 12 uses the existing English dataset's spelling-variation example “What's low-ra?” and removes the obsolete assertion that questions and answers are Japanese.
- Page 13 uses the English course repository for the operational fetch URL; all branches, tags, flags and file paths remain unchanged.
- Page 14 removes the obsolete Japanese-only UI claim, uses the localized `Unsure` label, and restores the entire explicit screenshot transcription, including LoRA, PEFT, Lecture 2, and Pass (1)/Fail (0).
- Page 15 translates the complete output example, preserving every fraction, count, coverage value, case ID, verdict, reason, and output path. It preserves the distinction between actual grading and `--model test`. It corrects the inherited claim “Clarity agrees least” to the source's “Clarity agreement is low”: the displayed Grounding 8/9 is slightly below Clarity 9/10.
- Page 16 translates both complete rubric excerpts, preserving the `grounding` key, `pass`/`fail`/`unsure`, the 1–2-line policy change, removal from unresolved issues, 1 → 0 review count, the alternative fail policy, and the fallback when there are zero unsure cases. English rubric terminology is consistent with the published repository.
- Pages 17 and 18 localize the human-readable commit message and the actual English “Invalid judgment format” error label.
- Page 19 restores the requirement to consult a paper or official page. Page 21 restores GPQA's four choices, the distinction between expert authors and two **other** validators, the validation role of SWE-bench's 93 developers, and both τ²-bench grading elements (scenarios and final state).
- Page 22 removes the extra English-only requirement to submit through the same PR; the source requires the same `answer.md` file but does not impose that PR choice.

## Verification and limits

- JSON decoding, all 49 unique canonical IDs, order, page numbers, nonempty titles/bodies, and one-use mappings pass. Japanese uploaded slide alignment with the pinned source is checked directly.
- No Japanese script remains in the English retrieval bodies. Original Japanese source text and uploaded files remain intact for provenance.
- All source API names, model IDs (`gemini-3.1-flash-lite`, `gemini-3.5-flash-lite`, `gemini-3.5-flash`), command flags, code paths, branch/tag names, error/status values, numbers, and substantive caveats were reviewed. Only operational repository URLs and natural-language examples/labels are intentionally localized.
- Source page 10 of Lecture 4 says to label four criteria, while pages 8 and 14 show five human labels including the separately code-checked lecture marker. This source wording is preserved rather than silently rewritten. Four criteria are judged by the LLM; the fifth is checked by code.
- Source quantitative benchmark claims and product versions are translated as teaching content, not independently updated or fact-checked against live services.
- Repeated copyright/restriction boilerplate is removed only from retrieval bodies. Explicit logo transcriptions required by the canonical source remain present.
- No teaching commands were executed. No course repository, DB, embeddings, API, git commit, push, or deployment was modified by this preparation. Retrieval accuracy and native-speaker approval remain unmeasured; these are complete reviewed text inputs, not a claim of end-to-end DB quality.
