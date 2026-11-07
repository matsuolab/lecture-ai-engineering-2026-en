"""Lecture 01: ask a bare LLM a question, or continue a chat with history.

Usage:
    uv run python -m app.ask "What is LoRA?"
    uv run python -m app.ask            # Ask a course-specific question if none is supplied
    uv run python -m app.ask --chat     # Ask follow-up questions with conversation history

A "bare" call with no tools or conversation history.
Check that, when asked about course-specific information, it either says "I don't know"
or gives a plausible general answer (which differs from the actual course).
(In Lecture 03, improve it by making an agent that can search the glossary.)
"""

import argparse
import time

from google import genai
from google.genai import errors
from google.genai import types

from app.config import MODEL, api_error_message, get_api_key

# A course-specific question. The correct answer is in homework-levels in data/glossary.json
DEFAULT_QUESTION = "What are the 3 homework levels in the AIE2026 course?"


def ask(question: str, temperature: float | None = None) -> str:
    client = genai.Client(api_key=get_api_key())
    started = time.perf_counter()
    if temperature is None:
        response = client.models.generate_content(model=MODEL, contents=question)
    else:
        response = client.models.generate_content(
            model=MODEL,
            contents=question,
            config=types.GenerateContentConfig(temperature=temperature),
        )
    _print_metrics(response, time.perf_counter() - started)

    return response.text


def _print_metrics(response: types.GenerateContentResponse, elapsed: float) -> None:
    usage = response.usage_metadata
    if usage is None:
        input_tokens = output_tokens = "unavailable"
    else:
        input_tokens = usage.prompt_token_count
        output_tokens = usage.candidates_token_count
        input_tokens = "unavailable" if input_tokens is None else input_tokens
        output_tokens = "unavailable" if output_tokens is None else output_tokens
    print(
        f"[metrics] elapsed={elapsed:.2f}s "
        f"input_tokens={input_tokens} output_tokens={output_tokens}"
    )


def chat(temperature: float | None = None, first_question: str | None = None) -> None:
    client = genai.Client(api_key=get_api_key())
    config = (
        types.GenerateContentConfig(temperature=temperature)
        if temperature is not None
        else None
    )
    conversation = client.chats.create(model=MODEL, config=config)
    # Reuse this session so the SDK includes earlier turns in each follow-up.
    question = first_question

    print("[chat] Type 'quit' or 'exit' to finish.")
    while True:
        if question is None:
            try:
                question = input("You: ")
            except EOFError:
                print()
                return
        if question.strip().lower() in {"quit", "exit"}:
            return
        if not question.strip():
            question = None
            continue

        started = time.perf_counter()
        response = conversation.send_message(question)
        print(f"Assistant: {response.text}")
        _print_metrics(response, time.perf_counter() - started)
        question = None


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask a bare LLM a question")
    parser.add_argument("question", nargs="?")
    parser.add_argument(
        "--chat",
        action="store_true",
        help="Continue asking follow-up questions while retaining conversation history",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        help="Set generation temperature for repeatability experiments",
    )
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        if args.chat:
            chat(temperature=args.temperature, first_question=args.question)
        else:
            question = args.question or DEFAULT_QUESTION
            print(f"[question] {question}\n")
            if args.temperature is not None:
                print(f"[temperature] {args.temperature}")
            print(ask(question, temperature=args.temperature))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
