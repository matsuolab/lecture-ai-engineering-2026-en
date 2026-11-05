"""Lecture 01 Advanced homework: latency and token counts across models and questions.

Run from the repo root (so `app` is importable):
    uv run python bench.py

Writes bench_results.csv and prints a markdown table to paste into lectures/01/answer.md.
"""
import csv
import statistics as st
import time

from google import genai
from google.genai import errors

from app.config import api_error_message, get_api_key

# model -> (runs per question, seconds to sleep after each request)
# 15 req/min -> >= 4s apart. 5 req/min -> >= 12s apart. Stronger model has ~10-20 req/day.
MODELS = {
    "gemini-3.5-flash-lite": (3, 5.0),
    "gemini-3.8-flash": (2, 13.0),
}

QUESTIONS = {
    "general": "What is LoRA?",
    "course": "What are the 3 homework levels in the AIE2026 course?",
    "short": "Explain overfitting in one sentence.",
}

RETRY_CODES = {429, 503}
MAX_ATTEMPTS = 2  # retries also consume daily quota, keep it low

client = genai.Client(api_key=get_api_key())


def call(model: str, prompt: str) -> dict:
    err = ""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        t0 = time.perf_counter()
        try:
            r = client.models.generate_content(model=model, contents=prompt)
        except errors.APIError as e:
            err = str(e.code)
            print("   ", api_error_message(e.code, str(e.message)[:100]))
            if e.code not in RETRY_CODES or attempt == MAX_ATTEMPTS:
                break
            time.sleep(30)
            continue
        dt = time.perf_counter() - t0
        u = r.usage_metadata
        return {
            "latency_s": round(dt, 2),
            "in_tokens": u.prompt_token_count or 0,
            "out_tokens": u.candidates_token_count or 0,
            "thought_tokens": getattr(u, "thoughts_token_count", None) or 0,
            "attempts": attempt,
            "error": "",
        }
    return {"latency_s": None, "in_tokens": None, "out_tokens": None,
            "thought_tokens": None, "attempts": MAX_ATTEMPTS, "error": err}


rows = []
for model, (runs, gap) in MODELS.items():
    for qname, q in QUESTIONS.items():
        for i in range(1, runs + 1):
            print(f"{model} | {qname} | run {i}")
            rows.append({"model": model, "question": qname, "run": i, **call(model, q)})
            time.sleep(gap)

with open("bench_results.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

print("\n| model | question | n_ok | latency mean (min-max) s | in tok | out tok | thought tok | max sequential req/min |")
print("|---|---|---|---|---|---|---|---|")
for model in MODELS:
    for qname in QUESTIONS:
        ok = [r for r in rows if r["model"] == model and r["question"] == qname and not r["error"]]
        if not ok:
            print(f"| {model} | {qname} | 0 | - | - | - | - | - |")
            continue
        lat = [r["latency_s"] for r in ok]
        mean = lambda k: round(st.mean(r[k] for r in ok), 1)
        print(
            f"| {model} | {qname} | {len(ok)} | {st.mean(lat):.2f} ({min(lat):.2f}-{max(lat):.2f}) "
            f"| {mean('in_tokens')} | {mean('out_tokens')} | {mean('thought_tokens')} "
            f"| {60 / st.mean(lat):.1f} |"
        )

fails = [r for r in rows if r["error"]]
print(f"\nfailed calls: {len(fails)} / {len(rows)}", [(r['model'], r['question'], r['error']) for r in fails])