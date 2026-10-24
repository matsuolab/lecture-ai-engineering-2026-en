# Lecture 01 Answers

## Exercises

- Model's answer to the course-specific question (the 3 homework levels; a summary is fine):
- What you noticed when comparing it with the correct meaning in the glossary:
- Token counts you displayed (input / output):

## Homework

### Level attempted: Advanced, Implementation and Basic.
### What you did:

#### Basic:
I used three models: gemini-3.5-flash, gemini-3.5-flash-lite and gemma-4-26b-a4b-it (A different free model)

Question => "Q2 Compare LoRA with full fine-tuning. Answer in at most 200 words."

#### Advanced:
I tested two Gemini models using three questions, with three attempts per model/question pair: 18 calls were made where 13 were successfull, and 5 were failures.

Models used: `gemini-3.5-flash-lite` and `gemini-3.8-flash`.

Timing: `perf_counter()` around `generate_content`, measuring time until the complete response arrives. Network and service time are included; client construction, pacing waits, and file writing are excluded.

Questions: 
Q1 What is LoRA? Answer in one sentence.
Q2 Compare LoRA with full fine-tuning. Answer in at most 200 words.
Q3 What are the 3 homework levels in the AIE2026 course?

### Results:

#### Basic:

Flash: relied more on comparison and covering resources, storage, performance and catastrophic forgetting. It mainly enumerated ideas and concepts.

Flash-lite: Provided a comparison between the two models and 

Gamma: Provided a full in depth explanation between LoRa and Fine-Tuning, providing more details about its implementation.

In other words, each model explained the same concept through different strategies and different level of depth.


#### Advanced:
The table reports means and medians for successful responses only. All token columns are mean counts per successful response. N/R means not reported.


| Question | Model | Successes / attempts | Mean time (s) | Median time (s) | Input tokens | Output tokens | Thinking tokens | Total tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Q1 | `gemini-3.5-flash-lite` | 3/3 | 4.04 | 4.11 | 11.00 | 39.67 | N/R | 50.67 |
| Q1 | `gemini-3.8-flash` | 1/3 | 65.84 | 65.84 | 11.00 | 47.00 | 450.00 | 508.00 |
| Q2 | `gemini-3.5-flash-lite` | 3/3 | 4.01 | 4.12 | 20.00 | 242.33 | N/R | 262.33 |
| Q2 | `gemini-3.8-flash` | 2/3 | 65.61 | 65.61 | 20.00 | 241.00 | 528.50 | 789.50 |
| Q3 | `gemini-3.5-flash-lite` | 3/3 | 3.42 | 4.52 | 18.00 | 128.00 | N/R | 146.00 |
| Q3 | `gemini-3.8-flash` | 1/3 | 50.53 | 50.53 | 18.00 | 302.00 | 1475.00 | 1795.00 |

### Observations and questions:

#### Basic:

The model choice affected how the ideas were presented, elaborated, depth of the explanation and even the strategy on how the question was answered.


#### Advanced:
#### Response time and reliability:

In this experiment, gemini-3.8-flash had fewer successful responses and higher mean response times than gemini-3.5-flash-lite for every question. Its successful-response means were approximately 14.8–16.4 times higher. The sample was small and unequal because of failures, so these results do not establish a general speed ranking.

#### Token usage:

Flash reported higher mean total token counts for every question and reported additional thinking tokens. Flash-Lite did not report thinking-token counts, so I cannot conclude that it used fewer thinking tokens. For Q2, output lengths were very similar (242.33 versus 241.00 tokens), despite the large timing difference. Thinking may have contributed to Flash's latency, but this experiment cannot isolate its effect from network and service conditions. Google's troubleshooting guide notes that thinking can increase latency and token usage.

#### Answer consistency:

Flash-Lite admitted uncertainty about the course in two runs but invented a course structure in another. Flash's only successful course-specific answer also invented details despite reporting 1,475 thinking tokens. More detailed responses and additional thinking tokens did not guarantee course-specific accuracy.

#### Failures:

Flash returned four 503 errors explicitly reporting high demand and one 504 deadline error after approximately 119.73 seconds. These failure durations were excluded from successful-response averages. Missing token counts for failed calls were treated as unknown rather than zero.

#### Questions:
- Perhaps gemini-flash performed worse because due to some limitation found in free tier?
- Could there be a limit to how much tokens are spent on thinking for the free-tier?
- Perhaps I picked a worse model for what I'm trying to accomplish?
