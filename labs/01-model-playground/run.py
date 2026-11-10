"""Lab 01: Model playground.

Runs the same release-note summary task on several models and temperatures, and logs each
summary with its tokens, cost and latency to outputs/results.csv.

Usage:
    python run.py                 # every model in MODELS
    python run.py --models gpt-6-luna

Keys come from the environment (OPENAI_API_KEY, OPENROUTER_API_KEY), never from this file.
"""
import argparse
import csv
import json
import os
import time
from pathlib import Path

from openai import OpenAI

HERE = Path(__file__).parent
DATA = HERE / "data" / "release_notes.json"
OUT = HERE / "outputs" / "results.csv"

# Prices in USD per 1M tokens (input, output), standard tier.
# Source: OpenAI API pricing page, read 2026-11-10.
# "settings" is the list of temperatures to run; None means the model's default.
# The GPT-6 family and GPT-5.5 reject any temperature but the default, so they get
# 3 repeat runs at default to measure consistency; gpt-5.4-mini gets the temperature test.
MODELS = {
    "gpt-6-luna": {"provider": "openai", "price": (0.10, 0.50), "settings": [None, None, None]},
    "gpt-6-sol": {"provider": "openai", "price": (2.00, 10.00), "settings": [None, None, None]},
    "gpt-5.4-mini": {"provider": "openai", "price": (0.75, 4.50), "settings": [0.0, 0.7, 1.0]},
}

PROVIDERS = {
    "openai": {"base_url": None, "key_env": "OPENAI_API_KEY"},
    "openrouter": {"base_url": "https://openrouter.ai/api/v1", "key_env": "OPENROUTER_API_KEY"},
}

SYSTEM_PROMPT = """You summarize software release notes for a busy product manager.
Rules:
- At most 5 bullets, plain language, readable in 30 seconds.
- Put breaking changes and behavior changes first, labeled "Breaking:" or "Behavior change:".
- Only state what the release notes say. Do not add changes, reasons or impact that are not there.
- Leave out commit hashes, PR numbers and contributor names."""


def client_for(provider):
    cfg = PROVIDERS[provider]
    return OpenAI(api_key=os.environ.get(cfg["key_env"], "missing"), base_url=cfg["base_url"])


def summarize(client, model, temperature, notes):
    start = time.perf_counter()
    extra = {} if temperature is None else {"temperature": temperature}
    resp = client.chat.completions.create(
        model=model,
        **extra,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Release notes:\n\n{notes}"},
        ],
    )
    latency = time.perf_counter() - start
    return resp.choices[0].message.content.strip(), resp.usage, latency


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=list(MODELS))
    args = ap.parse_args()

    notes = json.loads(DATA.read_text())
    OUT.parent.mkdir(exist_ok=True)
    new_file = not OUT.exists()
    with OUT.open("a", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["run_id", "note_id", "project", "category", "model", "setting",
                        "summary", "input_tokens", "output_tokens", "cost_usd", "latency_s"])
        for model in args.models:
            cfg = MODELS[model]
            client = client_for(cfg["provider"])
            for i, t in enumerate(cfg["settings"], start=1):
                setting = f"run{i}" if t is None else f"t{t}"
                for n in notes:
                    summary, usage, latency = summarize(client, model, t, n["release_notes"])
                    p_in, p_out = cfg["price"]
                    cost = (usage.prompt_tokens * p_in + usage.completion_tokens * p_out) / 1e6
                    run_id = f"{n['id']}|{model}|{setting}"
                    w.writerow([run_id, n["id"], n["project"], n["category"], model, setting, summary,
                                usage.prompt_tokens, usage.completion_tokens, f"{cost:.6f}",
                                f"{latency:.2f}"])
                    f.flush()
                    print(f"{run_id:45s} {usage.completion_tokens:4d} tok  ${cost:.5f}  {latency:.1f}s")


if __name__ == "__main__":
    main()
