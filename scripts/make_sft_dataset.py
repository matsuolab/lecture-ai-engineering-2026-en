"""Lecture 02 homework (Advanced): create Q&A data (JSONL) for SFT from the glossary.

Usage:
    uv run python scripts/make_sft_dataset.py > glossary_sft.jsonl

Upload the resulting file to Colab and use it as LoRA training data.
Try adding question variations, asking about aliases, or holding out a subset for validation.
"""

import json
import sys
from pathlib import Path

GLOSSARY = Path(__file__).resolve().parent.parent / "data" / "glossary.json"
TEMPLATES = ["What is {term}?", "Briefly explain {term}."]


def main() -> None:
    terms = json.loads(GLOSSARY.read_text(encoding="utf-8"))["terms"]
    for t in terms:
        for template in TEMPLATES:
            record = {
                "messages": [
                    {"role": "user", "content": template.format(term=t["term"])},
                    {"role": "assistant", "content": t["definition"]},
                ]
            }
            sys.stdout.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
