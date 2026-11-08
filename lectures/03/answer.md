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