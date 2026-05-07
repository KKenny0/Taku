# Taku Real-Task Evaluation

This directory holds a small manual regression suite for Taku behavior. It is not a benchmark and it does not require a separate runner. The point is to pressure-test the core workflow and bonus utility skills against realistic prompts and record where the instructions still drift.

## Suite

`real_task_scenarios.json` contains scenarios with:

- `prompt` — the user request to run in a disposable repo or branch
- `expected_phase_route` — the intended Taku phase or utility path
- `expected_artifacts` — files, reports, or summaries that should exist
- `pass_criteria` — observable behavior that must happen
- `observed_failure_mode` — update this after a manual run
- `failure_prevention_focus` — optional note describing the concrete delivery
  failure this scenario is meant to prevent

## How To Run

1. Create or choose a disposable repo with enough structure for the scenario.
2. Paste the scenario `prompt` into the target agent session.
3. Let Taku route the work using the current core workflow and utility skills.
4. Compare the result with `expected_phase_route`, `expected_artifacts`, and `pass_criteria`.
5. Record whether Taku prevented the target failure, not just whether the output looked good.
6. Update `observed_failure_mode` with the concrete miss, or `Passed on YYYY-MM-DD: <short note>`.

Keep observations specific. "Bad output" is not useful; "Skipped `/taku-debug` and patched before root-cause investigation" is useful. Prefer failure-prevention language: "Blocked unapproved scope drift before merge" is stronger evidence than "Review was thorough."

## Validation

The repository validator checks that this suite exists, has at least six scenarios, uses stable IDs, and covers every core Taku phase:

```bash
python3 scripts/validate_taku.py
```
