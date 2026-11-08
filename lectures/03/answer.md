# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
- Tool calls shown by `--trace` (tool names and arguments):
- Number of LLM calls for one question (`requests`):
- Tool added and the description in its docstring:

## Homework

- Level attempted: Basic 
- What you did: compare 4 experiments, change INSTRUCTIONS, docstring and compare
- Results:
The experiment tried to change INSTRUCTIONS or a docstring and compare.

| **Experiment** | **Agent instruction** | **Tool docstring** | **Tool calls** |
|---|---|---|---:|
| 1. Original baseline | Present | One term | 1 |
| 2. Remove instruction | Removed | One term | 2 |
| 3. Change docstring | Removed | Several terms | 1 |
| 4. Restore instruction | Present | Several terms | 1 |

**Experiment 1**

Configuration:

- Agent instruction: Present
- Docstring: Put only one term to look up in query

```text
[tool call] search_glossary({'query': 'LoRA'})

[tool return] search_glossary -> LoRA definition

[usage] requests=2, tool_calls=1
```

Agent followed the instruction to check the glossary before answering. But only searched for LoRA, even when the user's questions is both LoRA and QLoRA. Instruction does not guarantee that all glossary terms will be searched individually. It only encourages tool usage, while the model still chooses what to search for.

**Experiment 2**

Configuration:

- Agent instruction: Removed
- Docstring: Put only one term to look up in query

```text
[tool call] search_glossary({'query': 'LoRA'})
[tool call] search_glossary({'query': 'QLoRA'})

[usage] requests=2, tool_calls=2
```

Even after removing the instruction that explicitly tells the agent to search the glossary, the agent still decided to use search_glossary. But it made two separate calls:

1. Search for LoRA.
2. Search for QLoRA.

Removing an instruction does not remove the behavior it encourage. The model can still infer the best tool usage from the tool's description and user's question.

**Experiment 3**

Configuration:

- Agent instruction: Removed
- Docstring: Put several terms to look up in query

```text
[tool call] search_glossary({'query': 'LoRA, QLoRA'})

[tool return] search_glossary -> LoRA definition

[usage] requests=2, tool_calls=1
```

The agent only made 1 call, combining both terms into a single query. LLM interpret as permission to combine multiple terms.

Note that only change the tool description, not the python. There's no code that splits a comma-separated query into individual terms. ("LoRA, QLoRA") -> processed as one normalized string. So it still the result only returned LoRA, as the python code is the one that determines what the tool can do (does not change the tool functionality).

**Experiment 4**

Configuration:

- Agent instruction: Present
- Docstring: Put several terms to look up in query

```text
[tool call] search_glossary({'query': 'LoRA, QLoRA'})

[tool return] search_glossary -> LoRA definition

[usage] requests=2, tool_calls=1
```

Agent still made only one call. Docstring tells model several terms can be included in 1 query. But again the code didn't handle how to process comma-separated values.

Recommended approach though to be able to search both LoRA and QLoRA is with experiment 2, no code changes, safe approach and wont change the existing logic.

- Observations and questions:
  - Agent instructions and tool docstrings influence how the LLM decides to use tools.
  - Changing the docstring affects how the query is formulated, but does not change the actual Python functionality.
  - Separate tool calls are the most practical way to retrieve multiple terms without modifying the existing code.
  - **Question:** How can we make the agent consistently search for all terms mentioned in a question?

AI was used to assist with wording, while the experimental procedure,results and interpretations were manually verified and checked by me.