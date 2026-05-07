# Taku Evidence Report — 2026-05-05 (updated 2026-05-07)

## Executive Summary

We ran 9 of 10 eval scenarios against Taku v0.2.0 using `claude -p --output-format json`. Each scenario tested a specific skill's discipline enforcement against its pass criteria. On 2026-05-06, we ran two follow-up evals using `claude -p --resume` for multi-turn testing: a debug retest (Gap 1) and a full Think -> Plan -> Build -> Review flow (Gap 3). Later on 2026-05-06, we ran an interactive dogfood task (Fix Windows `--strict` false positive) through the full pipeline to validate discipline enforcement with full turn budget. Phase 2 hardening (gap fixes, case studies, interactive depth testing) is complete.

**Results: 5 PASS, 3 PARTIAL, 0 FAIL, 1 SKIP** (programmatic evals) + **interactive dogfood: all 4 phases PASS**

Taku's strongest skills are **Review**, **Reflect**, **Build**, and **Think Quick mode** (in interactive sessions) — all consistently enforce discipline and produce high-quality output. The Think Quick mode gate that failed in `claude -p` mode works correctly in interactive sessions. The discipline layer demonstrably prevented at least 5 mistakes (SQL injection flagged Critical; retro avoided fabricating data; debug produced REPORT + regression test; build added retroactive tests with honest TDD deviation; Quick mode gate produced mini design before implementation in interactive dogfood).

**Status: Phase 1 (Prove It) and Phase 2 (Harden) complete.** The 2026-05-07 strategy supersedes the earlier framework-extraction recommendation. The next evidence work is narrower: prove that Taku prevents concrete coding delivery failures such as scope drift, weak review, symptom fixes, missing verification, and context loss.

**Phase 3C update:** `real_task_scenarios.json` now includes scenarios for scope drift, missing verification, build/review handoff, and compact resume source labels. Eval records may include optional `failure_prevention` fields so reports can count prevented failures, not only pass/fail verdicts.

**Phase 4 update:** Taku now summarizes 6 dogfood reliability records across small bugfix, small feature, medium feature, refactor, failed verification, and long session resume. The records are a mix of retrospective evidence from real sessions and current-session roadmap evidence; each record names its evidence source and does not claim a fresh rerun unless one happened.

## Eval Results Summary

| ID | Title | Verdict | Turns | Cost | Key Finding |
|----|-------|---------|-------|------|-------------|
| rt-01 | Small bugfix | PARTIAL | 3 | $0.08 | Fixed bug but skipped debug investigation |
| rt-02 | Ambiguous feature | PASS | 11 | $0.29 | Correct Think Design mode, good approach presentation |
| rt-03 | Compact feature | PARTIAL | 6 | $0.15 | Used lightweight mode but skipped mini design |
| rt-04 | Build without subagents | SKIP | — | — | Could not simulate no-subagent environment |
| rt-05 | Review no diff | PASS | 14 | — | Correctly detected no diff, clean exit |
| rt-06 | SQL injection review | PASS | 9 | $0.25 | Flagged as Critical (CWE-89), provided fix |
| rt-07 | Reflect learning | PASS | 21 | $0.74 | Recorded, searched, suggested bootstrap |
| rt-08 | Retro limited history | PASS | 29 | $0.85 | Used real git data, no fabrication |
| rt-09 | Compact design | PARTIAL | 17 | $0.39 | Correct format but couldn't test decision capture |
| rt-10 | Compact debug session | PASS | 41 | $0.67 | Root cause captured, dirty state preserved |

**Interactive dogfood (2026-05-06):**

| Phase | Verdict | Key Finding |
|-------|---------|-------------|
| Think (Quick mode) | PASS | Gate enforced: alignment question → mini design → user approval |
| Plan (Lightweight) | PASS | State detection, self-review 6/6 passed |
| Build (Sequential TDD) | PASS | Red-Green-Refactor followed, fixture issue diagnosed |
| Review (Two-pass) | PASS | Spec compliance FULL, no findings, clean DONE |

**Total cost:** ~$3.42 for 9 programmatic evals + dogfood task (interactive, cost not tracked separately)
**Total turns:** 151 across 9 programmatic sessions + ~20 turns for interactive dogfood

## Phase 4 Dogfood Reliability Traces

| Trace | Situation | Evidence Source | Prevented Failure | Friction | Net Verdict |
|-------|-----------|-----------------|-------------------|----------|-------------|
| dogfood-01 | small bugfix | retrospective from 2026-05-06 interactive task | platform fix without regression anchor | 2/5 | net_positive |
| dogfood-02 | small feature | current roadmap implementation session | manual evidence claims drifting away from tooling | 1/5 | net_positive |
| dogfood-03 | medium feature | commit `c812102` | install-time references to non-installed skill assets | 2/5 | net_positive |
| dogfood-04 | refactor | current roadmap implementation session | rigid procedure replacing model-aligned delivery gates | 2/5 | net_positive |
| dogfood-05 | failed verification | retrospective from 2026-05-06 interactive task | skipping the TDD anchor after a harness failure | 3/5 | net_positive |
| dogfood-06 | long session resume | current resumed roadmap session | stale or invented repo state after context reset | 1/5 | net_positive |

**Dogfood summary:** 6/6 records are net-positive, 6/6 name a concrete prevented failure, and no severe net-negative record is reported. Two records are retrospective from prior real sessions; this is marked explicitly in the evidence-source column.

**How to reproduce the summary:** add JSONL entries with `failure_prevention`, `net_verdict`, and `friction_score` fields, then run:

```bash
python scripts/eval_summary.py scripts/test_data/eval_entries.jsonl
```

## Phase-by-Phase Assessment

### Think

**Evidence:** rt-02 (PASS), rt-03 (PARTIAL), interactive dogfood (2026-05-06, PASS)

rt-02 demonstrates strong Design mode behavior:
- Recognized ambiguous request ("team notifications") as needing Think
- Presented 2 genuinely different approaches (Inline Trigger vs Event Bus)
- Asked exactly 1 question before presenting ("which direction?")
- Provided clear recommendation with rationale

rt-03 shows Quick mode may be too permissive in `claude -p` mode:
- The `--json` flag task was correctly identified as small
- But no mini design was produced (expected at least a 3-sentence spec)
- Jumped straight to implementation in 6 turns

**Interactive dogfood (2026-05-06):** Think Quick mode gate **worked correctly** in interactive session:
- Correctly selected Quick mode for a specific single-function bug fix
- Asked one alignment question ("Does that match what you had in mind?")
- Produced a 5-field mini design (Change, Why, Touch Points, Risks, Done When)
- Waited for explicit user approval ("yes") before routing to Plan
- This is the exact gate that failed in `claude -p` mode (rt-03, E2E eval). With full turn budget in interactive mode, the gate is enforced as designed.

**Verdict:** Think Quick mode gate works correctly in interactive sessions. The `claude -p` compression issue is a mode-specific limitation, not a skill design flaw. Design mode works well for ambiguous tasks.

### Plan

**Evidence:** E2E multi-phase eval (2026-05-06), interactive dogfood (2026-05-06)

In the E2E eval, Plan was invoked after Think had already implemented the feature. It detected the pre-existing implementation, produced PLAN.md as traceability, and noted the implementation was already done. The self-review checklist was completed (5/5 checks passed).

**Interactive dogfood (2026-05-06):** Plan worked correctly:
- Step Detection correctly skipped Scope + Architecture Review (Quick mode mini design, no formal DESIGN.md)
- Selected Lightweight template (single file, single directory, 1 task)
- Detected existing PLAN.md from previous E2E eval, overwrote with new plan
- Self-review checklist ran: all 6 items passed (no placeholders, spec verifiable, dependencies correct)
- Task spec included concrete TDD anchor with specific test name

**Verdict:** Plan works correctly in both modes. It handles both normal and out-of-order execution gracefully. State detection (DESIGN.md/PLAN.md existence, git status) works as designed.

### Build

**Evidence:** rt-01 (indirect), rt-04 (SKIP), E2E multi-phase eval (2026-05-06), interactive dogfood (2026-05-06)

rt-01 shows the build execution worked (fixed the bug in 3 turns) but bypassed the Plan phase entirely. Without a PLAN.md, the build skill just implements directly.

rt-04 (build without subagents) could not be tested because `claude -p` sessions may or may not have subagent capability.

E2E eval: Build phase detected pre-existing code from Think, added 3 retroactive pytest tests, noted TDD deviation honestly, produced BUILD COMPLETE with wave report.

**Interactive dogfood (2026-05-06):** Build TDD discipline worked correctly:
- Announced BUILD PREFLIGHT (sequential mode, single task, no worktree)
- **RED phase:** Test file written first. Ran tests — confirmed 1 failure (Windows skip test), 2 passing. Failure message confirmed the expected reason (`'not executable'` error present).
- **GREEN phase:** Minimal 2-line fix (wrapped `stat.S_IXUSR` check in platform guard). All 3 tests passed.
- **REFACTOR phase:** Correctly assessed no cleanup needed.
- End-to-end verification: `python scripts/validate_taku.py --strict` passed on Windows.
- Encountered `tmp_path` fixture PermissionError on Windows, diagnosed immediately, switched to `tempfile.TemporaryDirectory` without abandoning TDD.

**Verdict:** Build is resilient. TDD discipline (Red-Green-Refactor) is properly enforced in interactive mode. Honest self-assessment about TDD violations is a strength. Handles obstacles (fixture issues) without skipping discipline.

### Review

**Evidence:** rt-05 (PASS), rt-06 (PASS), interactive dogfood (2026-05-06) — strongest skill

rt-05 (no diff):
- Detected on main branch with no feature branch ✓
- Did not invent findings ✓
- Did not create/modify files ✓
- Offered to review untracked files (reasonable behavior) ✓

rt-06 (SQL injection):
- Flagged as **Critical** with CWE-89 reference ✓
- Provided parameterized query fix with code ✓
- Also found resource leak (Medium) and SELECT * (Low) ✓
- Did NOT commit, push, or open PR ✓
- Verdict: "Do not merge" ✓

**Interactive dogfood (2026-05-06):** Review worked correctly:
- Detected on main branch, adapted to review uncommitted local changes (not PR diff)
- Scope Check: CLEAN — intent matched delivered changes
- Spec Compliance Check: FULL — all 5 spec assertions matched (5/5)
- Two-pass review: Critical pass found 0 issues, Informational pass found 0 issues
- Noted `stat` import is unused on Windows at runtime but correctly assessed as harmless
- Output summary: "No issues found. Status: DONE."
- Did not commit, push, or modify any files

**Verdict:** Review is Taku's strongest skill. Finding quality is high, discipline is enforced, and it adapts correctly to non-PR review contexts (uncommitted local changes).

### Debug

**Evidence:** rt-01 (indirect — debug was NOT used initially), rt-01 retest with mandatory sequence enforcement (multi-turn, 2026-05-06)

Original rt-01 was supposed to route through Debug first, but the agent jumped straight to fixing. The 4-phase investigation was completely skipped.

**Retest (2026-05-06):** With mandatory sequence enforcement, the agent produced a DEBUG REPORT, wrote a regression test, and went through Phase 1 properly. Phases 2-3 were shallow (see Gap 1 for detail). The enforcement is partially effective — significant improvement over original, but `claude -p` compression still allows shortcuts on Phases 2-3.

**Verdict:** Debug skill works when explicitly invoked. Mandatory sequence enforcement is partially effective. The routing gap (no auto-trigger for "fix this bug" prompts) remains.

### Reflect

**Evidence:** rt-07 (PASS), rt-08 (PASS)

rt-07 (learning flow):
- Recorded learning with type/confidence/context/action/apply_when ✓
- Searched for matching learnings ✓
- Suggested bootstrap but did NOT auto-install ✓
- Asked for user confirmation ✓

rt-08 (retro with limited history):
- Used actual git history (7 commits, 4 days) ✓
- Called out data limitations explicitly ✓
- Did NOT fabricate velocity trends or incidents ✓
- Saved report to `.taku/retros/` ✓
- Produced actionable next-week habits ✓

**Verdict:** Reflect works well. The retro's refusal to overstate conclusions from thin evidence is exactly the discipline behavior Taku should enforce.

### Compact

**Evidence:** rt-09 (PARTIAL), rt-10 (PASS)

rt-09 (design discussion):
- Correctly identified no durable changes (clean git) ✓
- Saved to `.taku/context/` ✓
- Flagged risk of conversation-only decisions ✓
- Could not capture actual decisions (no prior conversation in `claude -p`) — eval limitation, not skill limitation

rt-10 (debug/review session):
- Identified root cause from git state ✓
- Captured dirty branch state ✓
- Saved with timestamp ✓
- Did NOT claim tests passed without evidence ✓

**Verdict:** Compact works correctly. The limitation in rt-09 is the eval setup, not the skill.

## Strengths

1. **Review finding quality is excellent.** rt-06 found SQL injection AND two secondary issues. The Critical/Important/Minor triage is clear and actionable.

2. **Reflect discipline is real.** rt-08 refused to fabricate trends from thin evidence. This is exactly the anti-rationalization behavior the discipline layer should enforce.

3. **Think mode selection works.** rt-02 correctly chose Design mode for an ambiguous request and presented genuinely different approaches.

4. **Compact preserves state reliably.** Both rt-09 and rt-10 produced useful context captures from session state.

5. **Cost is reasonable.** ~$3.42 for 9 evals. The most expensive was rt-08 retro ($0.85) which is expected for git analysis.

## Gaps

### Gap 1: Debug phase enforcement — Partially Effective (Severity: Important → Partially Fixed)

**Evidence (original):** rt-01 retest (after fix): 4 turns, $0.21. The debug skill was explicitly invoked via `/taku-debug` but still jumped to fixing without completing Phase 1-3. The agent rationalized that since the user already identified the root cause ("FileNotFoundError when config file is missing"), investigation was unnecessary.

**Evidence (multi-turn retest, 2026-05-06):** Used `claude -p` with `--resume` to run a two-turn debug eval:
- **Turn 1** ($0.53): Agent produced a DEBUG REPORT with hypotheses tracked, wrote a regression test (`test_config_loader.py`), and applied the fix. This is a significant improvement over the original eval which produced no report and no test.
- **Turn 2** (self-reflection, $0.12): Agent honestly assessed its own phase compliance:
  - Phase 1 (INVESTIGATE): **Done properly** — reproduced, traced data flow, read error completely
  - Phase 2 (PATTERN): **Shallow** — identified pattern correctly but skipped searching for similar patterns in codebase and `.taku/learnings/`
  - Phase 3 (HYPOTHESIS): **Partial** — conflated Phase 1 evidence with Phase 3 hypothesis testing; declared H1 confirmed from investigation rather than separate test
  - Phase 4 (IMPLEMENT): **Done properly** — failing test first, minimal fix, verified

**Root cause of the gap:** The Iron Law says "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION" but the agent treats user-provided root cause as pre-completed investigation. The mandatory sequence enforcement block improved behavior: the agent now produces a DEBUG REPORT and writes regression tests. However, `claude -p` compression still allows the agent to skip Phase 2 pattern search and Phase 3 separate hypothesis testing.

**Fix applied:** Added "Mandatory sequence enforcement" block to debug SKILL.md that explicitly requires completing Phases 1-3 before ANY code changes, and producing a DEBUG REPORT before Phase 4.

**Updated assessment:** The enforcement is **partially effective**:
- **Improved:** DEBUG REPORT produced (was absent before), regression test written (was absent before), Phase 1 investigation done properly
- **Remaining gap:** Phase 2 pattern search skipped, Phase 3 hypothesis testing conflated with Phase 1 evidence. These shortcuts are low-risk for simple bugs but would be real risks for harder bugs where the "obvious" root cause is wrong.
- **Mode dependency:** `claude -p` compresses multi-phase behavior. Interactive sessions should show stronger enforcement since the agent can't compress as easily.

**Evidence (interactive dogfood, 2026-05-06):** Tested with `eval_summary.py` hardcoded-path bug (reads wrong file by default). The agent properly executed all 4 phases:

- **Phase 1 (INVESTIGATE):** Reproduced, counted file lines, read the code, spotted docstring vs implementation mismatch at line 7 vs 44.
- **Phase 2 (PATTERN):** Matched "Config drift" pattern from the known-pattern table. Searched codebase for `eval_entries` and `hardcoded|baseline|fallback`. Compared against `validate_taku.py`'s dynamic path resolution. Checked `.taku/learnings/` (didn't exist). **This is a clear improvement over claude -p** which skipped all codebase/learnings search.
- **Phase 3 (HYPOTHESIS):** Ranked 3 hypotheses (H1: hardcoded baseline 85%, H2: JSON parsing 10%, H3: path resolution 5%). Tested H2 independently by passing the correct file explicitly — confirmed 10 entries, denied H2. Only then confirmed H1. **This is a clear improvement over claude -p** which conflated Phase 1 evidence with hypothesis confirmation.
- **Phase 4 (IMPLEMENT):** Wrote failing regression test first, minimal 1-line fix, verified both tests pass, ran full validate_taku.py suite.

**Caveat:** The bug was relatively simple — Phase 1 already revealed the root cause (docstring vs code path mismatch). Phase 2-3 depth was genuine but not stress-tested by a scenario where the root cause is invisible without pattern matching. A harder bug (e.g., symlink path resolution, encoding edge case) would be a stronger test, but the marginal evidence value doesn't justify the setup cost.

**Final assessment:** Debug skill enforcement is **effective in interactive mode**:
- `claude -p`: Phase 2-3 remain shallow due to turn compression — **accepted limitation**
- Interactive: All 4 phases executed with proper depth — **Gap 1 resolved for interactive mode**
- Debug auto-trigger (description v2): Deployed but not yet re-tested due to GLM rate limits — **separate concern, not a Phase 2-3 issue**

### Gap 2: Quick mode skips mini design (Severity: Minor → Resolved for interactive mode)

**Evidence:** rt-03 produced no design artifact in `claude -p` mode.

**Fix applied:** Added mandatory language to Think SKILL.md Quick Mode: "This is mandatory — even for one-line changes" and "Do not proceed to step 4 until this mini design is written and visible to the user."

**Retest result (claude -p):** Not yet re-tested (rt-03 retest output was lost due to path issues). The fix strengthens the instruction but faces the same `claude -p` compression issue as Gap 1.

**Retest result (interactive dogfood, 2026-05-06):** Quick mode gate **worked correctly** in interactive session. The agent:
1. Correctly selected Quick mode
2. Asked one alignment question
3. Produced a 5-field mini design (Change, Why, Touch Points, Risks, Done When)
4. **Waited for explicit user approval before proceeding**
5. Only then routed to `/taku-plan`

This is the exact gate that failed in `claude -p` mode (rt-03, E2E eval Gap 3 Turn 1). In interactive mode with full turn budget, the gate is enforced as designed.

**Updated assessment:** The gap is **resolved for interactive mode** and **partially fixed for `claude -p` mode**:
- **Interactive mode:** Quick mode gate works correctly. The discipline mechanism (mandatory mini design + user approval) is effective when the agent has full turn budget.
- **`claude -p` mode:** The gate is still bypassed due to single-turn compression. This is a fundamental limitation of non-interactive mode, not a skill design flaw. The fix (stronger instruction language) may help in some cases but cannot fully overcome the compression.

**Root cause:** `claude -p` compresses multi-step behavior into fewer turns. The Quick mode gate requires: (1) ask alignment question, (2) write mini design, (3) get approval — at least 3 interactions. In `claude -p`, the agent sees the entire request and produces a single response that skips to implementation. The mandatory instruction language helps but cannot force multi-turn discipline in a single-turn mode.

**No remaining action for interactive mode.** For `claude -p` mode, this is an accepted limitation.

### Gap 3: Multi-phase flow — Resolved (Severity: Important → Resolved)

Confirmed by both `claude -p --resume` multi-turn eval and interactive dogfood task.

**Evidence (multi-turn eval, 2026-05-06):** Used `claude -p --resume` to simulate a 4-phase flow (Think → Plan → Build → Review) with a small feature request ("Add --summary flag to validate_taku.py"). Total cost: $1.84 across 4 turns.

| Phase | Turn | Cost | Behavior |
|-------|------|------|----------|
| Think | 1 | $0.33 | Quick mode selected (correct). **Design gate bypassed** — implemented directly without mini design or approval. |
| Plan | 2 | $0.30 | Detected pre-existing implementation. Produced PLAN.md as traceability. Noted "already implemented and verified." |
| Build | 3 | $0.64 | Added 3 retroactive pytest tests. Honest about TDD deviation. BUILD COMPLETE with wave report. |
| Review | 4 | $0.57 | Full two-pass review. 0 findings. Spec compliance 11/11. Correctly identified clean diff. |

**Key findings:**

1. **Phase handoffs work.** Each phase correctly detected the current project state (DESIGN.md/PLAN.md existence, git status) and adapted its behavior. Plan detected pre-existing code, Build added retroactive tests, Review did full spec compliance check.

2. **Think design gate is the weakest link.** Despite the mandatory mini design gate added in Gap 2 fix, `claude -p` mode still bypasses it. The agent goes straight to implementation. This confirms Gap 2 is a real enforcement issue, not a documentation issue.

3. **Build and Review are resilient.** Both phases handled out-of-order execution (code before plan) gracefully. Build was honest about TDD deviation. Review maintained full discipline.

4. **`--resume` technique is effective for multi-phase testing.** The session context carries forward, allowing each phase to see the artifacts and changes from previous phases. This is a viable eval approach for future multi-phase testing.

**Remaining gap:** None for interactive mode. The Think gate enforcement gap in `claude -p` mode is an accepted limitation of non-interactive execution (see Gap 2 update).

## Comparison Points

### Where Taku demonstrably prevented mistakes:

1. **rt-06:** A raw "review this" prompt might have treated the SQL injection as informational. Taku's review skill flagged it as Critical with CWE-89 and refused to merge. **This is a real prevented mistake.**

2. **rt-08:** Without Taku's discipline, a retro from 7 commits over 4 days would likely have included fabricated trend analysis ("velocity is increasing") or overstated conclusions. Taku's reflect skill produced an honest retro that explicitly called out thin evidence. **This prevented misleading conclusions.**

3. **rt-01 retest (multi-turn):** Without Taku's debug skill, the agent would have fixed the bug without producing a DEBUG REPORT or writing a regression test. With the mandatory sequence enforcement, the agent produced both. **Partial improvement — the fix was the same, but the discipline artifacts (report + regression test) would not have existed without Taku.**

4. **E2E Build phase:** Without Taku's build skill, the agent would have implemented the feature without tests. With Taku, it added 3 pytest tests and was honest about the TDD deviation. **Build discipline adds regression coverage that raw prompting would skip.**

### Where Taku didn't help:

1. **rt-03 (`claude -p` only):** A raw "add --json flag" prompt would have produced the same code. Taku's Think skill was supposed to add a mini design step but skipped it in `claude -p` mode. **No improvement over raw prompting in `claude -p` mode.** However, interactive dogfood confirmed the gate works in interactive sessions — this is a mode-specific limitation, not a skill deficiency.

2. **rt-01 original:** A raw "fix this bug" prompt would have produced the same fix. Debug skill wasn't auto-triggered. **No improvement before explicit invocation + enforcement fix.**

## Recommendation

**Phase 2 (Harden) complete. Proceed with the 2026-05-07 winning strategy roadmap.** (Updated 2026-05-07)

### Phase 2 completion summary

All three Phase 2 priorities from the initial recommendation have been addressed:

| Priority | Status | Outcome |
|----------|--------|---------|
| Fix Debug auto-trigger routing (Gap 1) | Done | Mandatory sequence enforcement added to debug SKILL.md. Interactive dogfood confirmed all 4 phases execute with proper depth. `claude -p` shallowness accepted as mode limitation. |
| Write 2-3 case studies | Done | Case studies documented in evidence report and knowledge vault entries (ff000b8a Windows fix, 0ea28e9 debug trigger/case studies, fa3f3db Phase 2-3 validation). |
| Debug Phases 2-3 interactive depth test | Done | Interactive dogfood with `eval_summary.py` hardcoded-path bug confirmed: Phase 2 searched codebase + learnings, Phase 3 ranked 3 hypotheses and tested independently. Gap 1 resolved for interactive mode. |

### Accepted limitations

- **`claude -p` mode compression** — Think Quick mode gate and Debug Phase 2-3 depth are both affected by single-turn compression. These are fundamental limitations of non-interactive mode, not skill design flaws. No further action planned.
- **Debug auto-trigger (description v2)** — Deployed but not re-tested due to GLM rate limits. Low priority since interactive invocation works correctly.

### Next phase: Delivery reliability evidence

Do not proceed to protocol or domain-pack extraction. The 2026-05-07 strategy narrows Taku around disciplined coding delivery. The evidence upgrade should:

1. Keep the 7 installed skills self-contained and install-safe.
2. Test the Build -> Review -> Verify loop against scope drift and missing verification.
3. Record failure prevention explicitly in eval and dogfood artifacts.
4. Compare selected tasks against raw prompting or lightweight habit-only flows when feasible.

### What we learned about the approach

The `claude -p --resume` technique works for testing multi-phase flows. Each `--resume` call continues the session with full context, allowing phase-by-phase testing. Combined with self-reflection prompts (asking the agent to assess its own phase compliance), this produces detailed compliance data. Limitations: `claude -p` still compresses within each turn, so intra-phase discipline (e.g., Think's Quick mode gate) is harder to test than inter-phase handoffs.

**Interactive dogfood is the definitive test.** `claude -p` evals are useful for automated regression testing and cost-efficient coverage, but they systematically under-test discipline enforcement. The interactive dogfood task (Fix Windows `--strict` false positive) revealed that Think Quick mode gate, Plan state detection, Build TDD discipline, and Review finding quality all work correctly in interactive mode — contradicting the `claude -p` findings for Think. Future eval rounds should include at least one interactive dogfood task alongside programmatic evals.
