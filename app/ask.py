"""Lecture 01: a script that asks a bare LLM a question.

Usage:
    uv run python -m app.ask "What is LoRA?"
    uv run python -m app.ask            # Ask a course-specific question if none is supplied
    uv run python -m app.ask --chat     # Interactive mode with conversation history

A "bare" call with no tools. In --chat mode, history is kept so you can ask follow-ups.
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# A course-specific question. The correct answer is in homework-levels in data/glossary.json
DEFAULT_QUESTION = "What are the 3 homework levels in the AIE2026 course?"


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(model=MODEL, contents=question)

    # TODO(Lecture 01 exercise): use response.usage_metadata to
    #   display input and output token counts (you may ask Copilot)

    return response.text


def chat(first_question: str | None = None) -> None:
    """Interactive loop that keeps the conversation history between turns."""
    client = genai.Client(api_key=get_api_key())
    # A chat session stores every question and answer and resends them each turn.
    session = client.chats.create(model=MODEL)

    print("Chat mode. Type 'exit' or 'quit' to stop.\n")
    pending = first_question
    while True:
        if pending is not None:
            question, pending = pending, None
            print(f"you> {question}")
        else:
            try:
                question = input("you> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            break

        response = session.send_message(question)
        print(f"\n{response.text}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask a bare LLM a question")
    parser.add_argument("question", nargs="?", default=None)
    parser.add_argument(
        "--chat", action="store_true", help="interactive mode that keeps history"
    )
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        if args.chat:
            chat(args.question)
        else:
            question = args.question or DEFAULT_QUESTION
            print(f"[question] {question}\n")
            print(ask(question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()