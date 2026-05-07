# Taku Final Goal Roadmap

> Branch: `feature/winning-strategy-roadmap`
> Baseline: `c812102 feat: implement Taku winning strategy roadmap`
> Status: Phase 4-10 implementation in progress

## North Star

Taku should become a coding delivery harness that gets lighter as models improve
while preserving the gates that prevent expensive delivery failures.

Target positioning:

> Taku = disciplined coding delivery harness for agentic software work.

The core question for every serious coding task:

> Did Taku prevent at least one real delivery failure?

## Current State

Phase 3 is complete in the baseline commit:

- [x] Installed skills are self-contained and expose exactly 7 commands.
- [x] Build/Review/Debug/Compact/Think were hardened around failure
      prevention.
- [x] Eval scenarios include scope drift, missing verification,
      build/review handoff, and compact resume source labels.
- [x] `python scripts/validate_taku.py`, `python scripts/validate_taku.py
      --strict`, and `python -m pytest scripts` passed at Phase 3 close.

Remaining Phase 3 caveats:

- `DESIGN.md` is ignored by `.gitignore`; release evidence should decide
  separately whether it is force-tracked.
- Some evidence/tooling assets existed locally but were not included in the
  Phase 3 commit because the user asked to commit only the staged set.

## Roadmap

### Phase 4 - Proof of Delivery Reliability

- [x] Adopt relevant evidence assets under `evals/` and `scripts/`.
- [x] Add dogfood evidence template fields for prevented failure, friction
      score, raw-prompting comparison, and net verdict.
- [x] Summarize 6 dogfood reliability records from existing real sessions and
      the current long-running roadmap session.
- [x] Summarize dogfood outcomes in `evals/evidence-report.md` and
      `CASE_STUDIES.md`.
- [x] Make failure-prevention summary tooling part of the tracked script suite.

Acceptance:

- At least 4/6 traces show net benefit.
- At least 3 traces name a concrete prevented delivery failure.
- No trace records a severe "Taku made it worse" outcome.

### Phase 5 - Build/Review Product Core

- [x] Standardize Build output around `BUILD PREFLIGHT`, `BUILD UPDATE`, and
      `BUILD COMPLETE`.
- [x] Make the Build ledger compact and reviewable: task slug, files, TDD
      anchor, status, deviation, and verification evidence.
- [x] Standardize Review output around `HARD STOPS`, `CONCERNS`, and `SUMMARY`.
- [x] Ensure Review hard stops cover scope drift, missing requirements,
      missing verification, and critical bug/security issues.
- [x] Add eval coverage for approved deviations and Build/Review handoff.

### Phase 6 - Public Proof Packaging

- [x] Rewrite README positioning so failure prevention is the first story.
- [x] Demote six-phase workflow from headline to mechanism.
- [x] Rework `CASE_STUDIES.md` into an evidence wall with 5 case studies.
- [x] Map public claims to eval, dogfood, or case-study evidence.

### Phase 7 - Adoption-Ready Product Shape

- [x] Keep the public slash-command surface fixed at 7 commands.
- [x] Add first-run smoke checklist to README.
- [x] Extend validator checks for exact skills, local references, eval
      coverage, compact source-label vocabulary, and README claim drift.
- [x] Document that root `templates/` are authoring copies, not runtime
      dependencies.

### Phase 8 - Harness De-Rigidity

- [x] Audit each skill through the categories Failure gate, Evidence
      requirement, Output contract, Known pitfall, Procedure, and Model
      workaround.
- [x] Keep gates and output contracts; move or remove procedure-heavy wording
      where it no longer protects delivery quality.
- [x] Keep public interfaces unchanged.
- [x] Run validator and script tests after the lean pass.

Target skill shapes:

- Think: minimum necessary design constraints.
- Plan: executable Build contract, not architecture essay.
- Build: auditable implementation, not executor micromanagement.
- Review: ship/no-ship judgment, not long critique.
- Debug: proven root cause, not process theater.
- Compact: resume without false certainty.
- Reflect: preserve only high-quality long-term learnings.

### Phase 9 - Comparative Positioning

- [x] Add concise positioning against broad engineering habit suites such as
      Waza.
- [x] State when not to use Taku.
- [x] State when Taku is the better fit.
- [x] Avoid new writing/read/health skills.

### Phase 10 - Evidence-Backed v1

- [x] Keep v1 criteria explicit in public docs and evidence report.
- [x] Maintain at least 12-14 eval scenarios.
- [x] Maintain at least 6 dogfood reliability records in the evidence report.
- [x] Maintain at least 5 failure-prevention case studies.
- [x] Keep README claims traceable to evidence.

## Implementation Guardrails

- Do not commit `.taku/**`, `.claude/**`, `scripts/__pycache__/**`,
  `docs/**`, or `tests/**`.
- Do not commit `Run-Claude-Code-programmatically.md` or
  `scripts/config_loader.py`.
- Do not add protocol/domain-pack work.
- Do not add writing/read/health skills.
- Keep all installed skills self-contained.

## Validation Checklist

- [x] `python scripts/validate_taku.py`
- [x] `python scripts/validate_taku.py --strict`
- [x] `python -m pytest scripts`
- [x] `python -m json.tool evals/real_task_scenarios.json`
- [x] `rg` check for forbidden installed-skill runtime references
- [x] `rg` check for protocol/domain-pack drift (remaining matches are guardrails or reflect bootstrap terminology)
- [x] `npx skills add KKenny0/Taku -l`
- [x] `npx skills add . -l`

## Notes

Dogfood traces are evidence records, not marketing claims. When a trace is
retrospective, it must say so. Do not fabricate command output or claim a task
was freshly rerun unless the command was actually observed.
