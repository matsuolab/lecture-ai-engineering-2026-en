"""Lecture 01: a script that asks a bare LLM a single question.

Usage:
    uv run python -m app.ask "What is LoRA?"
    uv run python -m app.ask            # Ask a course-specific question if none is supplied

A "bare" call with no tools or conversation history.
Check that, when asked about course-specific information, it either says "I don't know"
or gives a plausible general answer (which differs from the actual course).
(In Lecture 03, improve it by making an agent that can search the glossary.)

Advanced homework additions:
    - response time measured with a monotonic timer (time.perf_counter)
    - token counts read from response.usage_metadata (never guessed from characters)
"""

import argparse
import time

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# A course-specific question. The correct answer is in homework-levels in data/glossary.json
DEFAULT_QUESTION = "What are the 3 homework levels in the AIE2026 course?"


def ask_with_metrics(question: str, model: str = MODEL) -> dict:
    """Send one question and return the answer together with timing and token metrics."""
    client = genai.Client(api_key=get_api_key())

    # perf_counter is monotonic: it never jumps backwards if the system clock changes.
    start = time.perf_counter()
    response = client.models.generate_content(model=model, contents=question)
    elapsed = time.perf_counter() - start

    usage = response.usage_metadata  # may be None, and individual fields may be None
    input_tokens = getattr(usage, "prompt_token_count", None)
    output_tokens = getattr(usage, "candidates_token_count", None)
    total_tokens = getattr(usage, "total_token_count", None)
    # Thinking models can report hidden reasoning tokens separately.
    thought_tokens = getattr(usage, "thoughts_token_count", None)

    # If the API gives no total, compute it: total = input + output.
    if total_tokens is None and input_tokens is not None and output_tokens is not None:
        total_tokens = input_tokens + output_tokens

    return {
        "model": model,
        "elapsed_s": elapsed,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "thought_tokens": thought_tokens,
        "total_tokens": total_tokens,
        "text": response.text,
    }


def ask(question: str) -> str:
    """Backward-compatible helper: return only the answer text."""
    return ask_with_metrics(question)["text"]


def _fmt(value) -> str:
    return "n/a" if value is None else str(value)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask a bare LLM a question")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print(f"[question] {args.question}\n")
    try:
        result = ask_with_metrics(args.question)
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)

    print(result["text"])
    print()
    print(f"[response time] {result['elapsed_s']:.2f} s")
    print(f"[input tokens]  {_fmt(result['input_tokens'])}")
    print(f"[output tokens] {_fmt(result['output_tokens'])}")
    if result["thought_tokens"]:
        print(f"[thought tokens] {result['thought_tokens']}")
    print(f"[total tokens]  {_fmt(result['total_tokens'])}")


if __name__ == "__main__":
    main()