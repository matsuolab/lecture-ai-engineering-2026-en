@yuri-sl ➜ /workspaces/lecture-ai-engineering-2026-en (lecture-3) $ uv run python -m app.agent --trace "What is the difference between LoRA and QLoRA?"
uv run python -m app.agent --trace "What will we learn in Lecture 03?"
uv run python -m app.agent --trace "What is quantum banana optimization?"

[model] gemini-3.5-flash-lite
                 pydantic-ai v2.57.0 • Python 3.14.2
      / \
     /   \       agent: target • model: google:gemini-3.5-flash-lite • tools: 2 • capabilities: 0
   /___.___\
  /    |    \    observability: off — see every model and tool call live, with cost
/      |      \    set it up free with Logfire and a GitHub login: https://pydantic.dev/ai-setup.md
`---.._|_..---'    or use any OpenTelemetry backend: https://pydantic.dev/docs/ai/logfire/#otel

                 goes away once observability is on — or PYDANTIC_AI_NO_BANNER=1
To understand the difference, it helps to think about how both methods handle the underlying model's weights during fine-tuning:

* **LoRA (Low-Rank Adaptation):** This method freezes the pretrained base model weights and introduces small, trainable low-rank matrices (adapters) to approximate the weight updates. While it drastically reduces the number of trainable parameters, the base model itself is typically kept in its original precision (e.g., FP16 or BF16) in memory.
* **QLoRA (Quantized Low-Rank Adaptation):** This builds on top of LoRA by additionally *quantizing* the base model weights down to a lower precision (such as 4-bit). By compressing the base model, QLoRA significantly reduces the memory footprint required to hold the model, allowing much larger models to be fine-tuned on resource-constrained hardware (like smaller GPUs) while still using LoRA adapters for the actual training.

To explore this further, think about this question: *If the base model is compressed to 4-bit in QLoRA, how do you think the gradients are computed during training to ensure the model still learns effectively?*

Lecture 02

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "A PEFT method that freezes pretrained weights, represents weight updates …
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "A method that saves memory by quantizing base-model weights to, for exam…
[usage] RunUsage(cost=Decimal('0.0010475'), details={'text_prompt_tokens': 1125}, input_text_tokens=1125, input_tokens=1125, output_tokens=284, requests=2, tool_calls=2)
[model] gemini-3.5-flash-lite
                 pydantic-ai v2.57.0 • Python 3.14.2
      / \
     /   \       agent: target • model: google:gemini-3.5-flash-lite • tools: 2 • capabilities: 0
   /___.___\
  /    |    \    observability: off — see every model and tool call live, with cost
/      |      \    set it up free with Logfire and a GitHub login: https://pydantic.dev/ai-setup.md
`---.._|_..---'    or use any OpenTelemetry backend: https://pydantic.dev/docs/ai/logfire/#otel

                 goes away once observability is on — or PYDANTIC_AI_NO_BANNER=1
In Lecture 03, you will explore **AI Agents**, covering:

- The basic structure of an AI agent: **model + loop + tools**.
- How agents use tool descriptions and argument types to decide their actions in a loop.
- The trade-offs and costs associated with the agent loop (such as response time, API charges, and rate limits).
- Concepts like harnesses (e.g., Pi), frameworks (like Pydantic AI and ADK), and guardrails/Human-in-the-loop for safe operations.

In the exercises, you'll try building and running a learning support agent that uses tools with Pydantic AI, inspect tool calls, and even add a new tool yourself! Think about how giving an LLM the ability to "search" or run code changes the way it handles tasks compared to a single-turn prompt.

Lecture 03

--- trace ---
[tool call]   get_lecture_summary({'lecture': 3})
[tool return] get_lecture_summary -> # Lecture 03 AI Agents

## Aims

- Understand that an AI agent's basic structure is "model + loop + tools"
- Build and r…
[usage] RunUsage(cost=Decimal('0.0008116'), details={'text_prompt_tokens': 1022}, input_text_tokens=1022, input_tokens=1022, output_tokens=202, requests=2, tool_calls=1)
[model] gemini-3.5-flash-lite
                 pydantic-ai v2.57.0 • Python 3.14.2
      / \
     /   \       agent: target • model: google:gemini-3.5-flash-lite • tools: 2 • capabilities: 0
   /___.___\
  /    |    \    observability: off — see every model and tool call live, with cost
/      |      \    set it up free with Logfire and a GitHub login: https://pydantic.dev/ai-setup.md
`---.._|_..---'    or use any OpenTelemetry backend: https://pydantic.dev/docs/ai/logfire/#otel

                 goes away once observability is on — or PYDANTIC_AI_NO_BANNER=1
It is not in the glossary.

--- trace ---
[tool call]   search_glossary({'query': 'quantum banana optimization'})
[tool return] search_glossary -> The term 'quantum banana optimization' was not found in the glossary.…
[usage] RunUsage(cost=Decimal('0.0002573'), details={'text_prompt_tokens': 641}, input_text_tokens=641, input_tokens=641, output_tokens=26, requests=2, tool_calls=1)