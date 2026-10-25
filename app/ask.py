"""Lecture 01: a script that asks a bare LLM a single question.

Usage:
    uv run python -m app.ask "What is LoRA?"
    uv run python -m app.ask            # Ask a course-specific question if none is supplied

A "bare" call with no tools or conversation history.
Check that, when asked about course-specific information, it either says "I don't know"
or gives a plausible general answer (which differs from the actual course).
(In Lecture 03, improve it by making an agent that can search the glossary.)
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# A course-specific question. The correct answer is in homework-levels in data/glossary.json
DEFAULT_QUESTION = "What are the 3 homework levels in the AIE2026 course?"

def _normalize_history(conversation_history):
    """Convert a simple list of dicts into the message format expected by the Gemini API."""
    if not conversation_history:
        return []

    normalized = []
    for message in conversation_history:
        if isinstance(message, dict):
            role = message.get("role", "user")
            content = message.get("content")
            if content is None and "parts" in message:
                parts = message["parts"]
                content = " ".join(
                    part.get("text", "") if isinstance(part, dict) else str(part)
                    for part in parts
                )
            normalized.append({"role": role, "parts": [{"text": str(content)}]})
        else:
            normalized.append({"role": "user", "parts": [{"text": str(message)}]})
    return normalized

def ask(question: str, conversation_history=None) -> str:
    """Ask a question with optional conversation history."""

    import time
    client = genai.Client(api_key=get_api_key())
    start = time.perf_counter()
    #response = client.models.generate_content(model=MODEL, contents=question)
    history = _normalize_history(conversation_history)
    if history:
        payload = history + [{"role": "user", "parts": [{"text": question}]}]
    else:
        payload = question

    response = client.models.generate_content(model=MODEL, contents=payload)

    elapsed = time.perf_counter() - start
    # TODO(Lecture 01 exercise): use response.usage_metadata to
    #   display input and output token counts (you may ask Copilot)
    usage = getattr(response, "usage_metadata", None)
    if usage is not None:
        input_tokens = getattr(usage, "prompt_token_count", 0)
        output_tokens = getattr(usage, "candidates_token_count", 0)
        print(f"[tokens] input={input_tokens}, output={output_tokens}")

    print(f"[time] {elapsed:.2f} seconds")
    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask a bare LLM a question")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Ask follow-up questions while preserving conversation history",
    )
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    
    if args.interactive:
        print("[mode] interactive conversation")
        history = []
        while True:
            try:
                user_input = input("You: ").strip()
            except EOFError:
                print()
                break

            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break
            if not user_input:
                print("Please enter a question.")
                continue

            response = ask(user_input, history)
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})
            print(f"Assistant: {response}\n")
        return

    print(f"[question] {args.question}\n")
    try:
        print(ask(args.question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
