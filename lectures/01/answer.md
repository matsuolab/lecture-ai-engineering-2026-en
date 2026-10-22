# Lecture 01 Answers

## Exercises

- Model's answer to the course-specific question (the 3 homework levels; a summary is fine):
I ran the uv run python -m app.ask "What is a lecNN-start tag in the AIE2026 course?" 3 times and it gave the following outputs 

1."In the context of the **AIE2026** course (Artificial Intelligence Engineering 2026), a **`lecNN-start` tag** (where "NN" represents a two-digit number, such as `lec01-start`, `lec05-start`, etc.) is a **code marker or metadata tag** used within the course's instructional materials, codebase, or version-controlled repositories (like GitHub)."

2."Based on the naming convention, **`lecNN-start`** is a marker used in course materials (likely in code repositories, Jupyter notebooks, or version control commits) for the **AIE2026** course."

3."Based on the context of academic courses and digital learning platforms (such asCanvas, Moodle, or custom university portals), a tag like **`lecNN-start`** (where "NN" represents a two-digit number, such as `lec01-start`, `lec02-start`, etc.) is typically a **metadata marker, HTML anchor, or system tag** used in course materials for the **AIE2026** course."

- What you noticed when comparing it with the correct meaning in the glossary:
The correct meaning in the glossary is:
 "A Git tag on the starting code for each lecture's exercises in the AIE2026 course repository (for example, lec03-start). Even if you have not finished the previous lecture, creating a branch from this tag lets you start the current lecture's exercises."

 Whereas the bare LLM hallucinated and guessed what the lecNN-start tag could be based on the "AIE" which it attributed to AI Engineering and guessed that it is a code marker for the start of a lecture on Github for the first guess.

 The second generation was more vague than the first but inline with Github and version control, falling short of the correct meaning in the glossary 

 The third guess was way off but close to the nauture of lecNN-start tag , explaining it as an html tag as compared to it being correctly a git tag at the start of the lecture.

- Token counts displayed (input / output):
First run:input_tokens=19 output_tokens=401
Second run:input_tokens=19 output_tokens=349
Third run: input_tokens=19 output_tokens=400

## Homework

- Level attempted: Basic
- What you did:
I ran uv run python -m app.ask --temperature 0.0 "What is LoRA"
      uv run python -m app.ask --temperature 0.7 "What is LoRA"
      uv run python -m app.ask --temperature 1.0 "What is LoRA"
- Results:

The first low temp base LLM run described it as :

"**LoRA** stands for **Low-Rank Adaptation**. It is a popular and efficient technique used in machine learning—specifically in the field of Large Language Models (LLMs) and Generative AI—to **fine-tune** massive pre-trained models with a fraction of the computing power and time usually required."

The Second mid-high:
"**LoRA** stands for **Low-Rank Adaptation**. It is a popular and efficient technique used in machine learning—specifically in the field of Large Language Models (LLMs) and Generative AI—to **fine-tune** massive models with a fraction of the computational power and time usually required."

The Third Highest Temp output:

"**LoRA** stands for **Low-Rank Adaptation**. It is a popular and efficient technique used in machine learning—specifically in the field of Large Language Models (LLMs) and image generation models (like Stable Diffusion)—to **fine-tune** existing models much faster and with significantly less computing power than traditional methods."



- Observations and questions:
The low temperature and mid temperature runs had similar answers , phrasing and vocabulary word for word showing consistency and stability with the Retrieval Augmented Generation in the bare LLM's publicly retrieval data.

The third run differed from the low and mid outputs , it was the same answer and meaning but with different wording , phrasing and vocabulary showing some form of "creativity" on the High Temperature run specifically these comparative parts 

Run 1 and 2 (low to mid temperature): Generative AI—to **fine-tune** massive models with a fraction of the computational power and time usually required.

Run 3 (High Temperature):"image generation models (like Stable Diffusion)—to **fine-tune** existing models much faster and with significantly less computing power than traditional methods." 

Note Run 1 and 2 use "Generative AI", "farction of the computational power and time usually required" compared with run 3 respectively: "image generation models  (like Stable Diffusion; even giving an example), "much faster and with significantly less computing power than traditional methods"

Which begs the question from me of

 1. Why, despite the difference between temperatures 0.0 and 0.7, did the first two runs give nearly identical answers?
 2. How does a higher temperature affect the model's word choices? I understand it affects token sampling, but what made the third response differ from the first two?




- Level attempted: Implementation

- What I did: 

Added a chat history feature through a loop with a quitting feature for memory sake  to `app/ask.py`, using one Gemini chat session so follow-up questions retain the earlier conversation. Also added yhe temperature and response-time/token reporting.

- Results:
 Tested with “What is LoRA?” followed by “When was it created?” without addressing a certain subject , I was ambiguous on what I was asking to reallly make sure that it now has context of the previous conversation. The second response used the first answer's context. The first turn reported time lapsed=2.62s input_tokens=5 output_tokens=556.
- Verification: "uv run pytest -q" passes all 14 tests, including tests for token/timing output and reusing a chat session for follow-up questions.


- Level attempted: Advanced
- What I did: Measured response time and input/output tokens for 3 questions, using the same model (`gemini-3.5-flash-lite`) at temperatures 0.0, 0.7, and 1.0. 


- Results and observations: 
Temp 0.0

1. [question]: What is LoRA?
[metrics] elapsed=32.12s input_tokens=6 output_tokens=629

2. [question] What are the 3 homework levels in the AIE2026 course?
[metrics] elapsed=23.81s input_tokens=18 output_tokens=69

3. [question] What is a lecNN-start tag in the AIE2026 course?
[metrics] elapsed=26.19s input_tokens=19 output_tokens=371

Temp:0.7
[question] What is LoRA?
[metrics] elapsed=12.52s input_tokens=6 output_tokens=692

[question] What are the 3 homework levels in the AIE2026 course?
[metrics] elapsed=11.71s input_tokens=18 output_tokens=72

[question] What is a lecNN-start tag in the AIE2026 course?
[metrics] elapsed=13.94s input_tokens=19 output_tokens=560

Temp:1.0
[question] What is LoRA?
[metrics] elapsed=88.96s input_tokens=6 output_tokens=713

[question] What is a lecNN-start tag in the AIE2026 course?
[metrics] elapsed=32.76s input_tokens=19 output_tokens=301

[question] What are the 3 homework levels in the AIE2026 course?
[metrics] elapsed=23.64s input_tokens=18 output_tokens=153

Time taken for a response stayed constant for each question Temperature type. For the base LLM temperature 0.0 the response time was in the range 23.81,26.19 and 32.12 .

Then for the 0.7 temperature the response time decreased compared with the 0.0 runs. The three responses ranged from 11.71s to 13.94s.

At temperature 1.0, response times varied substantially: 88.96s for LoRA, 32.76s for the lecNN-start question, and 23.64s for the homework-level question. The LoRA response was the slowest measurement overall. The three questions were asked in a different order at temperature 1.0, so these results are individual observations rather than a controlled timing comparison.

Output token counts also varied. For LoRA, output increased from 629 tokens at temperature 0.0 to 692 at 0.7 and 713 at 1.0. The course-specific questions did not show the same pattern: homework-level answers used 69, 72, and 153 output tokens, while lecN-start answers used 371, 560, and 301. Thus, higher temperature did not consistently produce more tokens across all questions.

The input token counts stayed the same for each question at every temperature (6 for LoRA, 18 for homework levels, and 19 for lecNN-start), as the prompts were unchanged. Response time did not follow a consistent pattern: the 0.7 runs were faster than the 0.0 runs in this sample, but the 1.0 LoRA run took much longer while the other two 1.0 runs were closer to their earlier times. Temperature alone cannot be concluded to cause these timing differences; network and service variability may also contribute, and three measurements per setting are a small sample.

For free-tier limits, each run is a separate  request, and longer prompts or answers use more tokens. This set of nine requests completed, but it does not reveal the account's exact request or token quota. If a rate-limit message appears, wait before retrying as the course instructions recommend.
