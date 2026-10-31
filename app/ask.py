"""Lecture 01: 単発の質問と、会話履歴付きチャット。"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key


DEFAULT_QUESTION = "What are the 3 homework levels in the AIE2026 course?"


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(
        model=MODEL,
        contents=question,
    )
    return response.text or ""


def chat() -> None:
    client = genai.Client(api_key=get_api_key())
    session = client.chats.create(model=MODEL)

    print("会話を始めます。終了するときは exit と入力してください。")

    while True:
        question = input("\nあなた：").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        response = session.send_message(question)
        print(f"\nAI：{response.text or '回答がありませんでした。'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask an LLM a question")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument(
        "--chat",
        action="store_true",
        help="会話履歴付きチャットを開始する",
    )
    args = parser.parse_args()

    print(f"[model] {MODEL}")

    try:
        if args.chat:
            chat()
        else:
            print(f"[question] {args.question}\n")
            print(ask(args.question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)
    except (KeyboardInterrupt, EOFError):
        print("\n会話を終了します。")


if __name__ == "__main__":
    main()