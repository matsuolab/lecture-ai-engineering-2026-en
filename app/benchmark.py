"""Lecture 01 advanced homework: compare response time and token counts.

Usage (from the repository root):
    uv run python -m app.benchmark                 # 2 models x 3 questions x 3 trials = 18 requests
    uv run python -m app.benchmark --trials 2      # fewer requests if you hit rate limits
    uv run python -m app.benchmark --sleep 8       # wait longer between requests

Outputs:
    lectures/01/results.csv   every single trial (successes and failures)
    lectures/01/answers.md    the answer text from trial 1 of each model/question (for quality comparison)
"""

import argparse
import csv
import statistics
import time
from pathlib import Path

from google.genai import errors

from app.ask import ask_with_metrics

MODELS = ["gemini-3.6-flash", "gemini-3.5-flash-lite"]

# Questions are identical for every model so differences come from the model, not the question.
QUESTIONS = {
    "Q1-short": "What does LoRA stand for?",
    "Q2-explain": "Explain what LoRA is and why it is used when fine-tuning large language models.",
    "Q3-reasoning": (
        "A student has a single free-tier Colab T4 GPU (16 GB memory) and wants to adapt a 7B-parameter "
        "language model to answer questions about a small, specialised course. They are choosing between "
        "full fine-tuning and LoRA. Compare the two approaches in terms of GPU memory, training time, "
        "risk of overfitting on a small dataset, and the size of the files that must be stored afterwards. "
        "Then recommend one approach and justify your choice step by step."
    ),
}

OUT_DIR = Path("lectures/01")
FIELDS = [
    "model", "question_id", "trial", "success", "error",
    "elapsed_s", "input_tokens", "output_tokens", "thought_tokens", "total_tokens",
]


def run(trials: int, sleep_s: float) -> tuple[list[dict], dict]:
    rows, answers = [], {}
    total = len(MODELS) * len(QUESTIONS) * trials
    n = 0
    for model in MODELS:
        for qid, question in QUESTIONS.items():
            for trial in range(1, trials + 1):
                n += 1
                row = {"model": model, "question_id": qid, "trial": trial}
                try:
                    r = ask_with_metrics(question, model=model)
                    row.update(success=True, error="", **{k: r[k] for k in FIELDS if k in r})
                    if trial == 1:
                        answers[(model, qid)] = r["text"]
                except errors.APIError as e:
                    row.update(success=False, error=f"{e.code}: {str(e.message)[:80]}")
                except Exception as e:  # keep the experiment going on unexpected failures
                    row.update(success=False, error=f"{type(e).__name__}: {str(e)[:80]}")
                rows.append(row)
                status = "OK" if row["success"] else f"FAILED ({row['error']})"
                print(f"[{n}/{total}] {model} {qid} trial {trial}: {status}")
                if n < total:
                    time.sleep(sleep_s)  # stay under the free-tier requests-per-minute limit
    return rows, answers


def summarize(rows: list[dict]) -> None:
    print("\n=== Averages (successful trials only) ===")
    print(f"{'model':<24}{'question':<14}{'ok/n':<7}{'time(s)':<10}{'in tok':<9}{'out tok':<9}")
    for model in MODELS:
        for qid in QUESTIONS:
            group = [r for r in rows if r["model"] == model and r["question_id"] == qid]
            ok = [r for r in group if r["success"]]

            def avg(key):
                vals = [r[key] for r in ok if r.get(key) is not None]
                return f"{statistics.mean(vals):.2f}" if vals else "n/a"

            print(f"{model:<24}{qid:<14}{len(ok)}/{len(group):<5}{avg('elapsed_s'):<10}"
                  f"{avg('input_tokens'):<9}{avg('output_tokens'):<9}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark models and questions")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--sleep", type=float, default=5.0, help="seconds between requests")
    args = parser.parse_args()

    rows, answers = run(args.trials, args.sleep)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    with open(OUT_DIR / "answers.md", "w", encoding="utf-8") as f:
        for (model, qid), text in answers.items():
            f.write(f"## {model} / {qid}\n\n{text}\n\n")

    summarize(rows)
    print(f"\nSaved {OUT_DIR / 'results.csv'} and {OUT_DIR / 'answers.md'}")


if __name__ == "__main__":
    main()