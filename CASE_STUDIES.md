# Taku Failure-Prevention Case Studies

Taku is useful when it prevents real delivery failures, not when it produces
longer process artifacts. These case studies map public claims to eval or
dogfood evidence.

## Evidence Map

| Claim | Case | Evidence |
|-------|------|----------|
| Review blocks critical delivery risk before nits | SQL injection hard stop | `rt-06`, evidence report dogfood-03 |
| Completion needs verification evidence | Missing verification blocked | `rt-12`, evidence report dogfood-05 |
| Debug fixes root cause, not symptoms | Symptom fix avoided | `rt-01`, evidence report dogfood-01 |
| Build keeps scope reviewable | Ledger catches deviation | `rt-13`, evidence report dogfood-03 |
| Compact resumes without invented truth | Source-labeled resume | `rt-14`, evidence report dogfood-06 |

## Case 1: SQL Injection Is a Hard Stop

**Failure risk:** a search endpoint builds a SQL `WHERE` clause from user input
and review treats it as a suggestion.

**Without Taku:** the agent might bury the SQL issue under style comments or
label it as a medium-severity recommendation.

**With Taku:** `/taku-review` checks critical patterns first. String-built SQL
from user input is a hard stop, not a nit. The review output must place the
finding under `HARD STOPS` and withhold ship-ready status until the risk is
removed or explicitly accepted by the user.

**Evidence:** `rt-06-review-critical-issue` and the existing evidence report
show SQL injection flagged as Critical with a fix recommendation.

## Case 2: Missing Verification Blocks Completion

**Failure risk:** the build summary says "tests pass" without command output.

**Without Taku:** the review may accept the completion claim and ship unverified
code.

**With Taku:** `/taku-review` treats missing verification evidence as a hard
stop when the implementation claims completion. The final summary separates
observed evidence from residual risk.

**Evidence:** `rt-12-review-missing-verification` tests this directly.
the dogfood-05 record in `evals/evidence-report.md` shows the same principle in
a real TDD failure: verification failure triggered investigation instead of a
confidence claim.

## Case 3: Debug Avoids Symptom Fixes

**Failure risk:** a bug gets patched at the crash site while the underlying
configuration or data-flow failure remains.

**Without Taku:** the agent changes the nearest line that makes the error
disappear.

**With Taku:** `/taku-debug` requires root-cause evidence before the fix and a
regression anchor after the diagnosis. The point is not to perform a long ritual;
the point is to prove the failure path.

**Evidence:** `rt-01-small-root-cause-bugfix` and
the dogfood-01 record in `evals/evidence-report.md` shows the root-cause and
regression-test gate.

## Case 4: Build Ledger Catches Deviations

**Failure risk:** Build deviates from the plan and Review cannot tell whether
the deviation was approved.

**Without Taku:** progress state is lost between implementation and review, so
scope drift looks like ordinary code churn.

**With Taku:** `/taku-build` keeps a compact task ledger with stable slugs,
files, TDD anchors, deviations, and verification evidence. `/taku-review` reads
that ledger before judging scope drift.

**Evidence:** `rt-13-build-review-handoff-ledger` covers the handoff, and
the dogfood-03 record in `evals/evidence-report.md` shows install-safety scope
preserved across a multi-directory implementation.

## Case 5: Compact Resumes Without Invented Truth

**Failure risk:** after a long or resumed task, the agent treats mixed memory,
chat decisions, failed commands, and file state as equally certain.

**Without Taku:** the resumed session may rely on stale context and start
editing against the wrong branch or wrong assumptions.

**With Taku:** `/taku-compact` uses strict source labels: `file`, `git`, `tool`,
`user`, `inferred`, and `unknown`. It keeps reflect candidates separate from
long-term learnings and does not turn session state into durable truth.

**Evidence:** `rt-14-compact-resume-source-labels` covers the expected behavior.
the dogfood-06 record in `evals/evidence-report.md` records the current roadmap
session resumed from a recap, then confirmed git and file state before editing.

## v1 Evidence Bar

Taku v1 should not ship because the prompts are polished. It should ship when
the evidence is strong enough:

- 7 installed skills, no new public commands.
- 12-14 real-task eval scenarios.
- 6 dogfood reliability records.
- 5 failure-prevention case studies.
- README claims trace to eval, dogfood, or this case-study file.
- Build/Review remain the clearest product core.

Full evidence report: [`evals/evidence-report.md`](evals/evidence-report.md).
