# Lecture 1 Homework

**Level:** Implementation

## What I did
I modified `app/ask.py` so it can hold a conversation. I added a `chat()`
function and a `--chat` flag. It creates a chat session with
`client.chats.create(model=MODEL)` and loops, reading questions with `input()`
and sending them with `session.send_message()`. The session stores earlier
turns, so follow-up questions have context. Typing `exit` or `quit` ends it.
The original single-question mode still works unchanged.

## Results
I ran `uv run python -m app.ask --chat`.
- Turn 1: "What is LoRA?" -> The model gave a long explanation of Low-Rank
  Adaptation, covering why fine-tuning is expensive and why LoRA is popular.
- Turn 2: "Explain it in one sentence." -> The model understood that "it"
  meant LoRA and replied with a one-sentence summary (freeze the original
  model, train only a tiny set of new weights). So the conversation history
  works.

`uv run pytest -q`: 11 passed.

## Model used
gemini-3.5-flash-lite (default, `AIE_MODEL` not set)

## Notes
I tested it myself before submitting.