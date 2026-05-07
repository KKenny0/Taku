"""Regression test for eval_summary.py default path bug."""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "eval_summary.py"


def test_default_path_reads_current_entries():
    """Default (no-args) should read eval_entries.jsonl, not baseline."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    assert "Total entries: 10" in result.stdout, (
        f"Expected 10 entries with default path, got:\n{result.stdout}"
    )


def test_explicit_path_works():
    """Explicit path should work correctly."""
    entries_path = Path(__file__).parent / "test_data" / "eval_entries.jsonl"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(entries_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    assert "Total entries: 10" in result.stdout


def test_failure_prevention_summary():
    """Optional failure_prevention records should be counted when present."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    assert "Failures prevented: 5" in result.stdout


def test_failure_prevention_details_and_dogfood_fields():
    """Optional dogfood evidence fields should be summarized when present."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    assert "Failure modes prevented:" in result.stdout
    assert "weak review missed critical issue: 1" in result.stdout
    assert "Net dogfood verdicts:" in result.stdout
    assert "net_positive: 4" in result.stdout
    assert "Average friction score: 1.8/5" in result.stdout


if __name__ == "__main__":
    test_explicit_path_works()
    print("PASS: explicit path works")
    try:
        test_default_path_reads_current_entries()
        print("PASS: default path reads current entries")
    except AssertionError:
        print("FAIL: default path reads current entries (expected — bug not yet fixed)")
