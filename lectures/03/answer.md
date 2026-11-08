# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
- Tool calls shown by `--trace` (tool names and arguments):
- Number of LLM calls for one question (`requests`):
- Tool added and the description in its docstring:

## Homework

- Level attempted: Basic / Implementation / Advanced
- What you did:
- Results:
- Observations and questions:

### Basic:
#### What was done:
    1. I ran questions using the original instructions.
    2. Changed one instruction or docstring.
    3. Ran the same questions again.
    4. Compared tool names, argumetns, returned information and final answers.

#### Results:
##### Questions with original instructions
    I started by running these questions:
    ```
    uv run python -m app.agent --trace "What is the difference between LoRA and QLoRA?"
    uv run python -m app.agent --trace "What will we learn in Lecture 03?"
    uv run python -m app.agent --trace "What is quantum banana optimization?"
    ```
    
    Here's a summary of what was done by each call:
    | Question | Tools called | LLM requests | Observation |
    |---|---|---:|---|
    | LoRA versus QLoRA | `search_glossary("LoRA")`, `search_glossary("QLoRA")` | 2 | Already searches each term separately |
    | Lecture 03 content | `get_lecture_summary(3)` | 2 | Selects the appropriate tool |
    | Unknown term | `search_glossary("quantum banana optimization")` | 2 | Reports that the term is absent instead of inventing an answer |
##### Changed instruction / docstring
    In app/agent.py I changed the line:
    ```
    - End your answer by indicating the relevant session (Lecture NN).
    ```

    to:
    ```
    - When a glossary search finds no match, explicitly say that the term was not found and ask the learner to check its spelling or provide more context. Do not assign a lecture number without supporting evidence.
    - Otherwise, end your answer by indicating the relevant session (Lecture NN).
    ```
##### Results from the second run:
    After doing the changes above, I achieved the following results:
    | Question | First run | Second run | Finding |
    |---|---|---|---|
    | LoRA versus QLoRA | Two glossary calls | One glossary call for `LoRA` | Tool usage changed |
    | Lecture 03 content | `get_lecture_summary(3)` | Same call | Tool selection stayed consistent |
    | Unknown term | Reported absence | Reported absence and requested clarification | Matches the new instruction |

##### Conclusion

The revised instruction improved the response when a term was absent from the glossary: the agent asked the learner to check the spelling or provide more context, giving a useful next step without inventing an answer.

Tool selection remained consistent for the lecture-summary and unknown-term questions. For the LoRA comparison, glossary calls decreased from two to one, while all questions still required two LLM requests. This shows that tool calls and LLM requests are different measures.

Because I ran each question only once per instruction version, I cannot confidently attribute every difference to the instruction change. Repeating the experiment would help distinguish a consistent effect from normal model variation.



### Implementation:
#### What was done:

I added a `save_log(topic: str, summary: str)` tool in `app/tools.py` to save learning records as JSON files in `learning_log/`. Each record contains the topic, a summary, and an automatically generated UTC timestamp. The tool rejects empty or whitespace-only topics and summaries.

In `app/agent.py`, I registered the tool with `requires_approval=True` and added an instruction to use it when the learner explicitly asks to save a record. I also added handling for `DeferredToolRequests`: the program displays the proposed content and asks for confirmation before executing the tool. It resumes the agent with the user's decision through `DeferredToolResults`, preserving the message history.

#### Results:

The agent receives manual confirmation from the user if learning results should be saved. After the action is confirmed a record JSON is created containing the following info:

```json
{
  "topic": "LoRA",
  "summary": "I learned that LoRA freezes the base weights and trains small adapter matrices.",
  "created_at": "2026-11-08T13:50:23.510420+00:00"
}
```

Also, automated tests using temporary directories were added  and `TestModel` to check the following behavior:

| Scenario | Expected and verified result |
|---|---|
| Direct tool execution with valid content | A JSON file contains the supplied topic and summary and a creation timestamp. |
| Empty or whitespace-only input | The tool returns a validation message without creating a file. |
| Approval pending | No file is created before the decision. |
| Approval granted | A learning record is created. |
| Approval denied | No learning record is created. |

Also the existing base-tool test was  updated to call only `search_glossary` and `get_lecture_summary`, leaving approval behavior to the new tests.

#### Observations and conclusion:

During the first manual trial, an incorrect validation condition rejected nonempty content. Correcting the condition allowed an approved call to save the record successfully.

Approval is enforced by the program through `requires_approval=True`. The automated tests verify that pending and denied calls do not write files, while an approved call does.
