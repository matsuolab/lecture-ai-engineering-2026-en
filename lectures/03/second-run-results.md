[model] gemini-3.5-flash-lite
                 pydantic-ai v2.57.0 • Python 3.14.2
      / \
     /   \       agent: target • model: google:gemini-3.5-flash-lite • tools: 2 • capabilities: 0
   /___.___\
  /    |    \    observability: off — see every model and tool call live, with cost
/      |      \    set it up free with Logfire and a GitHub login: https://pydantic.dev/ai-setup.md
`---.._|_..---'    or use any OpenTelemetry backend: https://pydantic.dev/docs/ai/logfire/#otel

                 goes away once observability is on — or PYDANTIC_AI_NO_BANNER=1
Based on the course glossary:

* **LoRA (Low-Rank Adaptation):** A Parameter-Efficient Fine-Tuning (PEFT) method that freezes the pretrained model weights, represents weight updates as a low-rank product of two small matrices, and trains only those small matrices. This significantly reduces the number of trainable parameters and saves adapters in small files.
* **QLoRA:** An extension that saves even more memory by quantizing the base-model weights (for example, down to 4 bits) before applying LoRA. This allows you to run and fine-tune much larger models on smaller GPUs.

To think about how they work together: imagine LoRA as the strategy for *which* parameters to train (the small adapter matrices), while QLoRA adds a memory-saving compression step (quantization) to the base model weights *before* applying that strategy. 

Lecture 02

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "A PEFT method that freezes pretrained weights, represents weight updates …
[usage] RunUsage(cost=Decimal('0.0008099'), details={'text_prompt_tokens': 983}, input_text_tokens=983, input_tokens=983, output_tokens=206, requests=2, tool_calls=1)
[model] gemini-3.5-flash-lite
                 pydantic-ai v2.57.0 • Python 3.14.2
      / \
     /   \       agent: target • model: google:gemini-3.5-flash-lite • tools: 2 • capabilities: 0
   /___.___\
  /    |    \    observability: off — see every model and tool call live, with cost
/      |      \    set it up free with Logfire and a GitHub login: https://pydantic.dev/ai-setup.md
`---.._|_..---'    or use any OpenTelemetry backend: https://pydantic.dev/docs/ai/logfire/#otel

                 goes away once observability is on — or PYDANTIC_AI_NO_BANNER=1
In Lecture 03, you will learn about **AI Agents**. The main topics and aims include:

- **The Agent Structure:** Understanding that an AI agent's basic structure consists of a "model + loop + tools."
- **Tools & The Agent Loop:** How an LLM calls tools, examines results, and decides its next action, as well as the cost of the agent loop (latency, charges, and rate limits).
- **Harnesses & Frameworks:** Exploring concepts like harnesses (such as Claude Code or Pi) and frameworks like Pydantic AI and ADK.
- **Guardrails & Human-in-the-Loop:** Managing risks with operations that are difficult to undo by restricting permissions or requiring human confirmation.
- **Hands-on Exercises:** Building and running your own learning support agent that uses tools with Pydantic AI, tracking tool calls and arguments, and adding a new tool.

Lecture 03

--- trace ---
[tool call]   get_lecture_summary({'lecture': 3})
[tool return] get_lecture_summary -> # Lecture 03 AI Agents

## Aims

- Understand that an AI agent's basic structure is "model + loop + tools"
- Build and r…
[usage] RunUsage(cost=Decimal('0.0008624'), details={'text_prompt_tokens': 1108}, input_text_tokens=1108, input_tokens=1108, output_tokens=212, requests=2, tool_calls=1)
[model] gemini-3.5-flash-lite
                 pydantic-ai v2.57.0 • Python 3.14.2
      / \
     /   \       agent: target • model: google:gemini-3.5-flash-lite • tools: 2 • capabilities: 0
   /___.___\
  /    |    \    observability: off — see every model and tool call live, with cost
/      |      \    set it up free with Logfire and a GitHub login: https://pydantic.dev/ai-setup.md
`---.._|_..---'    or use any OpenTelemetry backend: https://pydantic.dev/docs/ai/logfire/#otel

                 goes away once observability is on — or PYDANTIC_AI_NO_BANNER=1
The term "quantum banana optimization" was not found in the glossary. Please check its spelling or provide more context, and I will be happy to help you look it up!

--- trace ---
[tool call]   search_glossary({'query': 'quantum banana optimization'})
[tool return] search_glossary -> The term 'quantum banana optimization' was not found in the glossary.…
[usage] RunUsage(cost=Decimal('0.0003531'), details={'text_prompt_tokens': 727}, input_text_tokens=727, input_tokens=727, output_tokens=54, requests=2, tool_calls=1)