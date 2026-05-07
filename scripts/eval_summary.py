#!/usr/bin/env python3
"""Summarize Taku eval and dogfood entries from a JSONL file.

Usage:
    python scripts/eval_summary.py [path]

If no path is given, reads from test_data/eval_entries.jsonl.
Prints verdict counts, total cost, failure-prevention counts, and optional
dogfood friction / net-verdict fields.
"""
import json
import sys
from collections import Counter
from pathlib import Path


def load_entries(path: str | Path) -> list[dict]:
    """Read JSONL file and return list of parsed entries."""
    entries = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def summarize(entries: list[dict]) -> None:
    verdicts = Counter(e.get("verdict", "UNKNOWN") for e in entries)
    total_cost = sum(e.get("cost", 0) for e in entries)
    prevention_modes: Counter[str] = Counter()
    net_verdicts: Counter[str] = Counter()
    friction_scores: list[float] = []

    failures_prevented = 0
    for entry in entries:
        failure_prevention = entry.get("failure_prevention")
        if isinstance(failure_prevention, dict) and failure_prevention.get("prevented") is True:
            failures_prevented += 1
            mode = failure_prevention.get("failure_mode") or "unspecified"
            prevention_modes[str(mode)] += 1

        if "net_verdict" in entry:
            net_verdicts[str(entry["net_verdict"])] += 1

        friction_score = entry.get("friction_score")
        if isinstance(friction_score, (int, float)):
            friction_scores.append(float(friction_score))

    print(f"Total entries: {len(entries)}")
    print(f"Total cost: ${total_cost:.2f}")
    print(f"Failures prevented: {failures_prevented}")
    for verdict, count in verdicts.most_common():
        print(f"  {verdict}: {count}")
    if prevention_modes:
        print("Failure modes prevented:")
        for mode, count in prevention_modes.most_common():
            print(f"  {mode}: {count}")
    if net_verdicts:
        print("Net dogfood verdicts:")
        for verdict, count in net_verdicts.most_common():
            print(f"  {verdict}: {count}")
    if friction_scores:
        average = sum(friction_scores) / len(friction_scores)
        print(f"Average friction score: {average:.1f}/5")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        path = Path(__file__).parent / "test_data" / "eval_entries.jsonl"
    entries = load_entries(path)
    summarize(entries)
