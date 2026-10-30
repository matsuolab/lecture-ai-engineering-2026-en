# Lecture 01 Answers

## Exercises

- Model's answer to the course-specific question (the 3 homework levels; a summary is fine):
Question: What are the 3 homework levels in the AIE2026 course?
Answer: I do not have access to the specific details or syllabus for the "AIE2026" course,as it is not part of my standard training data or refers to a private/custom curriculum. 

Could you please provide more context or paste the relevant excerpt from your course syllabus? Once you provide that, I'd be happy to help you find or organize the information!

- What you noticed when comparing it with the correct meaning in the glossary:
The model doesn't have access to the course materials, so it can't answer questions that require context from those materials. The Gemini API doesn't automatically retrieve that information. However, for general questions like “What is LoRA?”, it can answer because it already has general knowledge about the topic from its training.

- Token counts you displayed (input / output):
Input=18 Output=79

## Homework

- Level attempted: Implementation 

- What you did: I tried to compare between 3 models, Gemini 2.5, Gemini 3.5 Lite and Gemini 3.8. I also added some codes to show the temperature, model, input, output tokens and also the response time for ease of analysis. I also tried to make it interactive with the help of coding agent. Tried 3.7 as well but 503 error.

- Results:

## Model Comparison Results

| Model | Temperature | Input Tokens | Output Tokens | Response Time |
|---|---:|---:|---:|---|
| Gemini 2.5 Flash | 0.2 | 1,037 | 2,306 | 12.29 s |
| Gemini 2.5 Flash | 0.9 | 1,120 | 2,575 | 13.36 s |
| Gemini 3.5 Flash-Lite | 0.2 | 660 | 666 | 3.05 s |
| Gemini 3.5 Flash-Lite | 0.9 | 682 | 688 | 3.03 s |
| Gemini 3.8 Flash | — | — | — | Failed: 503 — Model busy |

- Observations and questions:
Gemini 3.5 Flash-Lite
Very similar responses. Output tokens increased from 660 to 682 (+22 tokens, 3.3%). Both answers had almost the same structure and level of detail. Fast and concise. Changing temperature made little noticeable difference.

Gemini 2.5 Flash
More noticeable variation. Output tokens increased from 1,037 to 1,120 (+83 tokens, 8%). The answer at 0.9 included a longer analogy and more explanations. More detailed and technical. Higher temperature made the answer more descriptive, but also longer.

1. Gemini 2.5 Flash at 0.2: Gives a clear, organized, and more technical answer.

2. Gemini 2.5 Flash at 0.9: Gives more examples and analogies, but the answer may be too long.

3. Gemini 3.5 Flash-Lite at 0.2 or 0.9: Gives shorter answers and responds faster, with little difference between the two temperature settings.