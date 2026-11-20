# Lecture 01 — Answers and Experiment Report

## 1. Exercises

### 1.1 Course-Specific Question: What Are the Three Homework Levels?

I asked the LLM about the three homework levels in the AIE2026 course across three runs, using two different models.

**Run 1 — `gemini-3.5-flash-lite`**

The model stated that it did not have access to the specific details of the AIE2026 course.

**Run 2 — `gemini-3.5-flash`**

The model suggested possible homework structures, such as Core/Challenge/Stretch, Bronze/Silver/Gold, and Beginner/Intermediate/Advanced. These suggestions did not match the course's actual definitions.

**Run 3 — `gemini-3.5-flash-lite`**

The model suggested categories such as Basic/Guided, Intermediate/Applied, and Advanced/Open-ended. These suggestions were also inconsistent with the course glossary.

**Correct answer from `data/glossary.json`:**

1. **Basic:** Review lecture content.
2. **Implementation:** Write your own code.
3. **Advanced:** Research and experimentation.

### 1.2 What Does a `lecNN-start` Tag Mean?

The three runs produced different responses:

- **Run 1 — `gemini-3.5-flash-lite`:** The model gave a speculative explanation involving course materials and Git markers.
- **Run 2 — `gemini-3.5-flash`:** The model correctly identified the tag as a Git tag marking the starting code for a lecture's exercises.
- **Run 3 — `gemini-3.5-flash-lite`:** The model stated that it did not know the specific course terminology.

According to `data/glossary.json`, a `lecNN-start` tag marks the starting code for a lecture's exercises. Creating a branch from this tag allows students to start the current lecture without having to finish previous lectures first.

### 1.3 What Will We Learn in Lecture 02?

- **Run 1 — `gemini-3.5-flash-lite`:** The model stated that it did not know the course syllabus.
- **Run 2 — `gemini-3.5-flash`:** The model suggested possible topics from different types of AI courses but could not confirm the actual AIE2026 syllabus.
- **Run 3 — `gemini-3.5-flash-lite`:** The model again stated that it did not know the specific course schedule.

The responses did not establish what would actually be taught in Lecture 02. The experiment demonstrates the limitation of asking a bare LLM a course-specific question without supplying relevant course information.

### 1.4 Token Counting

The token-counting feature was implemented in `app/ask.py` using `response.usage_metadata`.

The script retrieves:

- `prompt_token_count` — the number of input tokens.
- `candidates_token_count` — the number of output tokens.

It also handles cases in which usage metadata is unavailable.

**Test question:** What is LoRA?

**Model:** `gemini-3.5-flash-lite`

**Observed terminal output:**

@vanshikavs-tech ➜ /workspaces/lecture-ai-engineering-2026-en (main) $ uv run python -m app.ask "What is LoRA?"
[model] gemini-3.5-flash-lite
[question] What is LoRA?

[input tokens] 6
[output tokens] 797

**Result:** The script successfully displayed the input and output token counts.

---

## 2. Homework — Basic Level

### 2.1 Work Completed

I ran four questions three times each, using the default model `gemini-3.5-flash-lite` and the alternative model `gemini-3.5-flash`.

The questions covered:

1. The meaning of LoRA.
2. The three homework levels in AIE2026.
3. The meaning of a `lecNN-start` tag.
4. The topics planned for Lecture 02.

I compared the responses across runs and checked the course-specific definitions against `data/glossary.json`.

### 2.2 Results Summary

| Question | Run 1: Flash Lite | Run 2: Flash | Run 3: Flash Lite |
|---|---|---|---|
| What is LoRA? | Detailed explanation of Low-Rank Adaptation | Explained Low-Rank Adaptation and also discussed wireless communication | Detailed explanation with additional technical information |
| What are the three homework levels? | Admitted it did not know | Suggested incorrect possible structures | Suggested incorrect possible structures |
| What is a `lecNN-start` tag? | Gave a speculative explanation | Correctly identified the Git tag's purpose | Admitted it did not know the specific terminology |
| What will we learn in Lecture 02? | Admitted it did not know the syllabus | Suggested possible topics without confirming the syllabus | Admitted it did not know the syllabus |

### 2.3 Observations

**1. Course-specific knowledge is limited.**

The models did not consistently know the AIE2026 course terminology or syllabus. Without access to the relevant course information, they sometimes admitted that they did not know the answer.

**2. Plausible answers are not always correct.**

For the homework-level question, Runs 2 and 3 generated plausible category names that did not match the actual definitions in the glossary.

**3. Responses vary across models and runs.**

Changing the model affected the detail, scope, and accuracy of the responses. Repeating questions with the same default model also produced different answers.

**4. General questions may receive broader answers.**

All three runs explained LoRA as Low-Rank Adaptation. However, the second run also discussed LoRa wireless communication, illustrating how a model may interpret a term in more than one context.

**5. Source verification improves reliability.**

Comparing the model's responses with `data/glossary.json` made it possible to distinguish the correct course-specific definitions from unsupported suggestions.

### 2.4 Conclusion

This experiment demonstrated that a bare LLM can answer general questions but may struggle with information specific to a course. It may acknowledge missing information or generate plausible but incorrect answers. Its responses can also vary between models and repeated runs.

Providing relevant course context, such as the glossary and syllabus, would help improve the reliability of course-specific answers. Token counting also provides a useful way to observe the input and output usage of an LLM request.

---

## 3. Token Counting Experiment — Summary

| Item | Result |
|---|---|
| Script modified | `app/ask.py` |
| Model tested | `gemini-3.5-flash-lite` |
| Test question | What is LoRA? |
| Input tokens | 6 |
| Output tokens | 797 |
| Status | Successfully tested |

**Final result:** The Basic-level experiment and token-counting implementation were completed. The responses were compared across three runs, and course-specific claims were checked against the supplied glossary.