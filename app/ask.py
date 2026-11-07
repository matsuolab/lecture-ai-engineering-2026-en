"""Lecture 01: a script that asks a bare LLM a single question.

Usage:
    uv run python -m app.ask "What is LoRA?"
    uv run python -m app.ask            # Ask a course-specific question if none is supplied
    uv run python -m app.ask --chat     # Interactive chat retaining conversation history

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


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(model=MODEL, contents=question)

    # Display input and output token counts using usage_metadata
    if response.usage_metadata:
        usage = response.usage_metadata
        print(f"[tokens] input: {usage.prompt_token_count}, output: {usage.candidates_token_count}\n")

    return response.text


def chat_loop(initial_question: str | None = None) -> None:
    """Lecture 01 Homework (Implementation): multi-turn chat retaining conversation history."""
    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)

    print("[chat mode] Type 'exit', 'quit', or press Ctrl+C to stop.\n")

    first_turn = True
    while True:
        try:
            if first_turn and initial_question:
                prompt = initial_question
                first_turn = False
                print(f"You: {prompt}")
            else:
                prompt = input("You: ").strip()
                if not prompt:
                    continue
                if prompt.lower() in ("exit", "quit"):
                    print("Exiting chat.")
                    break

            response = chat.send_message(prompt)
            if response.usage_metadata:
                usage = response.usage_metadata
                print(f"[tokens] input: {usage.prompt_token_count}, output: {usage.candidates_token_count}")
            print(f"AI: {response.text}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting chat.")
            break
        except errors.APIError as e:
            print(api_error_message(e.code, e.message))
            raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask a bare LLM a question")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument("--chat", "-c", action="store_true", help="Start an interactive chat session retaining conversation history")
    args = parser.parse_args()

    print(f"[model] {MODEL}")

    if args.chat:
        chat_loop(initial_question=args.question)
        return

    question = args.question or DEFAULT_QUESTION
    print(f"[question] {question}\n")
    try:
        print(ask(question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
