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
