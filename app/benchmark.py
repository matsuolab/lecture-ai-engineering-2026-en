"""Run from the course repository root: uv run python benchmark.py.

Writes results.csv (raw), summary.csv (successful-call averages), results.json
(raw results, answers and experiment settings). No automatic retries.
"""

import argparse
import csv
import json
import platform
import sys
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from statistics import mean, median
from time import perf_counter, sleep

DEFAULT_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-3.1-flash-lite",
]
DEFAULT_QUESTIONS = [
    "What is LoRA? Answer in one sentence.",
    "Compare LoRA with full fine-tuning. Answer in at most 200 words.",
    "What are the 3 homework levels in the AIE2026 course?",
]
TOKEN_FIELDS = {
    "input_tokens": "prompt_token_count",
    "output_tokens": "candidates_token_count",
    "thinking_tokens": "thoughts_token_count",
    "cached_input_tokens": "cached_content_token_count",
    "total_tokens": "total_token_count",
}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def measure(client, model, question, question_id, run):
    row = {
        "timestamp_utc": utc_now(), "model": model,
        "question_id": question_id, "question": question, "run": run,
        "status": "error", "http_code": None, "error": "",
        "elapsed_s": None, "answer": "", "finish_reason": "",
        "response_model_version": "",
        **{name: None for name in TOKEN_FIELDS},
    }
    start = perf_counter()
    try:
        response = client.models.generate_content(model=model, contents=question)
    except Exception as exc:
        row["elapsed_s"] = perf_counter() - start
        row["http_code"] = getattr(exc, "code", None)
        row["error"] = f"{type(exc).__name__}: {exc}"
        return row

    # Stop before extracting metadata, reading text or writing files.
    row["elapsed_s"] = perf_counter() - start
    row["status"] = "ok"
    row["response_model_version"] = getattr(response, "model_version", None)
    usage = response.usage_metadata
    for name, attribute in TOKEN_FIELDS.items():
        row[name] = getattr(usage, attribute, None)
    row["answer"] = response.text or ""
    candidates = response.candidates or []
    if candidates:
        reason = candidates[0].finish_reason
        row["finish_reason"] = getattr(reason, "value", str(reason))
    return row


def summarize(rows):
    summary = []
    pairs = dict.fromkeys((r["model"], r["question_id"]) for r in rows)
    for model, question_id in pairs:
        group = [r for r in rows if (r["model"], r["question_id"]) == (model, question_id)]
        successful = [r for r in group if r["status"] == "ok"]
        item = {
            "model": model, "question_id": question_id,
            "question": group[0]["question"], "attempted": len(group),
            "successful": len(successful), "failed": len(group) - len(successful),
            "mean_elapsed_s": mean(r["elapsed_s"] for r in successful) if successful else None,
            "median_elapsed_s": median(r["elapsed_s"] for r in successful) if successful else None,
        }
        for field in TOKEN_FIELDS:
            values = [r[field] for r in successful if r[field] is not None]
            item[f"mean_{field}"] = mean(values) if values else None
            item[f"samples_{field}"] = len(values)
        summary.append(item)
    return summary


def write_csv(path, rows):
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def save(output, metadata, rows):
    payload = {"experiment": metadata, "results": rows, "summary": summarize(rows)}
    temporary = output / "results.json.tmp"
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(output / "results.json")
    write_csv(output / "results.csv", rows)
    write_csv(output / "summary.csv", payload["summary"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--interval", type=float, default=15,
                        help="Minimum seconds between request starts, across all models")
    parser.add_argument("--timeout", type=float, default=120, help="HTTP timeout in seconds")
    parser.add_argument("--questions-file", type=Path,
                        help="Optional JSON file containing a list of question strings")
    parser.add_argument("--output", type=Path, default=Path("benchmark_results"))
    args = parser.parse_args()
    if args.repeats < 1 or args.interval < 0 or args.timeout <= 0:
        parser.error("Use repeats >= 1, interval >= 0 and timeout > 0.")
    questions = DEFAULT_QUESTIONS
    if args.questions_file:
        questions = json.loads(args.questions_file.read_text(encoding="utf-8"))
        if not isinstance(questions, list) or not questions or any(
            not isinstance(q, str) or not q.strip() for q in questions
        ):
            parser.error("The questions file must contain a nonempty JSON list of strings.")
    models = list(dict.fromkeys(args.models))

    try:
        from google import genai
        from google.genai import types
        from config import get_api_key
    except ImportError as exc:
        parser.exit(1, f"Import error: {exc}\nRun from the course repository root with uv run python benchmark.py.\n")

    client = genai.Client(
        api_key=get_api_key(),
        http_options=types.HttpOptions(
            timeout=int(args.timeout * 1000),
            retry_options=types.HttpRetryOptions(attempts=1),
        ),
    )
    # A new folder per execution prevents overwriting earlier measurements.
    output = args.output / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    output.mkdir(parents=True, exist_ok=False)
    metadata = {
        "started_utc": utc_now(), "models": models, "questions": questions,
        "repeats": args.repeats, "interval_s": args.interval,
        "timeout_s": args.timeout, "python_version": platform.python_version(),
        "google_genai_version": version("google-genai"),
        "generation_config": "Model defaults; no tools or conversation history",
        "http_attempts_per_call": 1, "warmup_calls": 0,
        "latency_definition": "Wall time around generate_content, including network/service time",
        "state": "running", "disabled_models": {},
    }
    rows, disabled = [], set()
    last_start = None
    total = len(models) * len(questions) * args.repeats
    print(f"Planned calls: {total}. Results: {output.resolve()}", flush=True)
    save(output, metadata, rows)
    try:
        # Alternate models, rotating the first model each round to reduce order bias.
        for run in range(1, args.repeats + 1):
            offset = (run - 1) % len(models)
            order = models[offset:] + models[:offset]
            for question_id, question in enumerate(questions, start=1):
                for model in order:
                    if model in disabled:
                        continue
                    if last_start is not None:
                        sleep(max(0, args.interval - (perf_counter() - last_start)))
                    print(f"[{len(rows) + 1}/{total}] {model} | Q{question_id} | run {run}", flush=True)
                    last_start = perf_counter()
                    row = measure(client, model, question, question_id, run)
                    rows.append(row)
                    # Stop requests to an unavailable or quota-limited model.
                    # No retries: failed-call latency must not enter successful averages.
                    if str(row["http_code"]) in {"400", "401", "403", "404", "429"}:
                        disabled.add(model)
                        metadata["disabled_models"][model] = row["error"]
                    save(output, metadata, rows)
                    if row["status"] == "ok":
                        print(f"  {row['elapsed_s']:.3f}s | input={row['input_tokens']} | "
                              f"output={row['output_tokens']} | thinking={row['thinking_tokens']} | "
                              f"total={row['total_tokens']}", flush=True)
                    else:
                        print(f"  ERROR: {row['error']}", flush=True)
                        if model in disabled:
                            print("  Remaining calls to this model skipped. See results.json.", flush=True)
        metadata["state"] = "finished_with_skips" if disabled else "finished"
    except KeyboardInterrupt:
        metadata["state"] = "interrupted"
        print("\nInterrupted. Completed measurements have been preserved.", flush=True)
    finally:
        metadata["ended_utc"] = utc_now()
        save(output, metadata, rows)
        client.close()
    successful = sum(r["status"] == "ok" for r in rows)
    print(f"\nSuccessful: {successful}; failed: {len(rows) - successful}; "
          f"not completed: {total - len(rows)}.")
    print(f"Send results.json for analysis: {output / 'results.json'}")
    return 0 if successful == total else 1


if __name__ == "__main__":
    sys.exit(main())
