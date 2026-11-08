# Lecture 01 Answers

**Model used:** Gemini 3.5 Flash Lite

## Exercises

### Model's answer to the course-specific question (the 3 homework levels; a summary is fine):

I tested the model three times using different temperatures (0.2, 0.8, and 0.5).

- **Temperature 0.2:** The model said it did not know the specific "3 Lists" for AIE2026 and asked for more information about the course.
- **Temperature 0.8:** The model gave several possible interpretations, including productivity lists, Python data structures, and prompt engineering lists.
- **Temperature 0.5:** The model suggested other interpretations, such as prompt engineering components, machine learning datasets, and AI ethics categories.

None of the responses correctly identified the three homework levels: **Basic, Implementation, and Advanced**.

### What you noticed when comparing it with the correct meaning in the glossary:

The correct answer was Basic, Implementation, and Advanced.

The model did not know the course-specific meaning and tried to guess based on general AI knowledge.

At temperature 0.2, the response was more cautious and asked for clarification. At temperatures 0.8 and 0.5, the model generated longer answers with more assumptions.

I learned that AI can produce convincing explanations even when it does not have the correct information. Higher temperatures do not necessarily produce more accurate answers.

### Token counts you displayed (input / output):

| Temperature | Input | Output | Total |
|---|---:|---:|---:|
| 0.2 | 19 | 205 | 224 |
| 0.8 | 19 | 445 | 464 |
| 0.5 | 19 | 615 | 634 |

The input tokens stayed the same, but the output tokens increased across the three tests.

## Homework

- **Level attempted:** Basic
- **What you did:** I used Gemini 3.5 Flash Lite to ask about the three homework levels in AIE2026. I tested the same question with three different temperatures: 0.2, 0.8, and 0.5. I initially wanted to change the model but the model was busy and thus unavailable. Finally, I compared the answers and recorded the token usage.
- **Results:** All three responses failed to identify the correct homework levels. Temperature 0.2 produced the shortest response (205 output tokens), while temperature 0.5 produced the longest response (615 output tokens).
- **Observations and questions:** I noticed that changing the temperature affected the responses, but none were correct. The model sometimes made assumptions instead of simply saying it did not know. I wonder whether providing the course glossary as context would help the model answer more accurately.