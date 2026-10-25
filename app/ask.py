"""Lecture 01: a script that asks a bare LLM a single question.

Usage:
    uv run python -m app.ask "What is LoRA?"
    uv run python -m app.ask            # Ask a course-specific question if none is supplied
    uv run python -m app.ask --interactive "What is LoRA?"

A "bare" call with no tools or conversation history.
Check that, when asked about course-specific information, it either says "I don't know"
or gives a plausible general answer (which differs from the actual course).
(In Lecture 03, improve it by making an agent that can search the glossary.)
"""

import argparse
import time

from google import genai
from google.genai import errors, types

from app.config import MODEL, TEMPERATURE, api_error_message, get_api_key

# A course-specific question. The correct answer is in homework-levels in data/glossary.json
DEFAULT_QUESTION = "What are the 3 homework levels in the AIE2026 course?"


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    start = time.perf_counter()
    response = client.models.generate_content(
        model=MODEL,
        contents=question,
        config=types.GenerateContentConfig(
            temperature=TEMPERATURE,
        ),
    )
    elapsed = time.perf_counter() - start

    usage = response.usage_metadata
    print(
        f"[response] time={elapsed:.2f}s "
        f"input_tokens={usage.prompt_token_count or 0} "
        f"output_tokens={usage.candidates_token_count or 0} "
        f"total_tokens={usage.total_token_count or 0}"
    )

    return response.text


def ask_follow_up(chat, question: str) -> str:
    """Send a question through an existing chat so earlier turns remain available."""
    start = time.perf_counter()
    response = chat.send_message(message=question)
    elapsed = time.perf_counter() - start

    usage = response.usage_metadata
    print(
        f"[response] time={elapsed:.2f}s "
        f"input_tokens={usage.prompt_token_count or 0} "
        f"output_tokens={usage.candidates_token_count or 0} "
        f"total_tokens={usage.total_token_count or 0}"
    )

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask a bare LLM a question")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Continue asking follow-up questions while preserving chat history",
    )
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print(f"[temperature] {TEMPERATURE}")
    try:
        if not args.interactive:
            print(f"[question] {args.question}\n")
            print(ask(args.question))
            return

        client = genai.Client(api_key=get_api_key())
        chat = client.chats.create(
            model=MODEL,
            config=types.GenerateContentConfig(temperature=TEMPERATURE),
        )
        question = args.question
        while question:
            print(f"[question] {question}\n")
            print(ask_follow_up(chat, question))
            try:
                question = input("\nFollow-up (Enter to quit): ").strip()
            except EOFError:
                break
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
