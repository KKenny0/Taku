---
name: taku-cross-review
description: >
  Get a second opinion from a different AI model on your diff. Three modes:
  REVIEW (pass/fail gate), CHALLENGE (adversarial, try to break the code),
  CONSULT (freeform Q&A with session continuity). Use when asked to "second opinion",
  "cross review", "challenge my code", or when you want an independent check before
  shipping. Enhanced dep: codex CLI (Claude Code) or multi-model sessions_spawn (OpenClaw).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Cross-Model Second Opinion

One model reviewing its own work is a conflict of interest. This skill gets a different AI model to look at your diff and deliver its honest assessment. Overlapping findings between models are high-confidence. Unique findings from either model get investigated, not blindly implemented.

Why this matters: every model has blind spots. Two models with different training data and architectures will catch different classes of bugs. The overlap is where you find the real problems.

## Enhanced Capability Check

```bash
# Claude Code: check for codex CLI
which codex 2>/dev/null && echo "CODEX: ready" || echo "CODEX: not found"

# OpenClaw: check for multi-model support (sessions_spawn with model param)
# This is platform-dependent — detected by the router
```

If neither capability is available: "Cross-model review requires codex CLI or multi-model sessions_spawn. Skipping. Run `/taku-review` for single-model review instead." Stop.

## Step 1: Detect Mode

Parse the user's input:

1. `/taku-cross-review review [instructions]` or no mode specified with a diff present — **REVIEW mode** (Step 2)
2. `/taku-cross-review challenge [focus-area]` — **CHALLENGE mode** (Step 3)
3. `/taku-cross-review consult [question]` or `/taku-cross-review [anything else]` — **CONSULT mode** (Step 4)

If no diff exists and mode isn't specified: ask what they want to review.

## Step 2: REVIEW Mode — Pass/Fail Gate

Send the diff to an external model for independent review with a pass/fail verdict.

**OpenClaw:**
```
sessions_spawn(
  model: "openai/gpt-4o",
  task: "Review this diff. Focus on: security issues, logic bugs, error handling,
  race conditions, and resource leaks. Rate each finding [P1] (critical, must fix)
  or [P2] (important, should fix). End with a verdict: PASS or FAIL.
  <diff content>"
)
```

**Claude Code:**
```bash
TMPERR=$(mktemp /tmp/codex-err-XXXXXX.txt)
cd "$(git rev-parse --show-toplevel)"
codex review "Review this diff for security issues, logic bugs, error handling,
race conditions, and resource leaks. Rate each finding [P1] or [P2].
End with verdict: PASS or FAIL." --base <base> 2>"$TMPERR"
```

### Gate Verdict

- Output contains `[P1]` → **FAIL**. Critical findings must be addressed.
- No `[P1]` markers → **PASS**. Review is clear.

### Cross-Model Comparison

If `/taku-review` was already run in this session, compare findings:

```
CROSS-MODEL ANALYSIS:
  Both found: [overlapping findings — high confidence, must fix]
  Only external found: [unique findings — investigate, don't blindly implement]
  Only local found: [unique findings — lower confidence, still valid]
  Agreement rate: X% (N/M total unique findings overlap)
```

**Rule:** Overlapping findings are high confidence. Implement them. Unique findings from either model get investigated — verify they're real before acting on them.

**Why overlapping = high confidence:** Two models with different architectures, training data, and biases independently flagged the same issue. The probability of a false positive drops dramatically when two independent observers agree. This is the core value of cross-model review — the intersection is where the real bugs live.

## Step 3: CHALLENGE Mode — Adversarial Review

Tell the external model to actively try to break the code. This catches edge cases that a normal review misses.

**OpenClaw:**
```
sessions_spawn(
  model: "openai/gpt-4o",
  task: "Review the changes on this branch. Your job is to find every way this code
  will fail in production. Think like an attacker and a chaos engineer.
  Find edge cases, race conditions, security holes, resource leaks, failure modes,
  and silent data corruption. Be adversarial. No compliments — just the problems.
  <diff content>"
)
```

**Claude Code:**
```bash
cd "$(git rev-parse --show-toplevel)"
codex exec "Review the changes on this branch against the base branch.
Your job is to find ways this code will fail in production.
Think like an attacker and a chaos engineer. Find edge cases, race conditions,
security holes, resource leaks, failure modes. Be adversarial." \
  -C . -s read-only --json
```

Present the output under a clear header. Do not editorialize. The adversarial model speaks for itself.

## Step 4: CONSULT Mode — Freeform Q&A

Ask the external model anything about the codebase. Supports follow-up questions.

**OpenClaw:**
```
sessions_spawn(
  model: "openai/gpt-4o",
  task: "<user's question>. Context: <relevant code or plan content>"
)
```

**Claude Code:**
```bash
cd "$(git rev-parse --show-toplevel)"
codex exec "<user's question>" -C . -s read-only --json
```

For plan reviews: read the plan file yourself and embed its full content in the prompt. Codex runs sandboxed and cannot access paths outside the repo.

## Step 5: Present and Synthesize

### Output Format

Present the external model's output verbatim. Then add your own synthesis:

```
EXTERNAL MODEL SAYS:
════════════════════════════════════════════════════════════
<full output, not truncated>
════════════════════════════════════════════════════════════
MODE: <REVIEW|CHALLENGE|CONSULT>
VERDICT: <PASS|FAIL|N/A> (REVIEW mode only)
```

### Synthesis Rules

1. **Present output verbatim.** Do not summarize or truncate before showing.
2. **Add your commentary AFTER.** If you disagree with a finding, say so and why.
3. **Flag skill-file rabbit holes.** If the external model appears to have read skill/config files instead of source code, warn the user.
4. **User decides.** External model recommendations are suggestions, not decisions. Present them. The user acts.

## Anti-Rationalization

| Excuse | Why it's wrong |
|--------|---------------|
| "The first review was thorough enough" | Two models with different blind spots catch different bugs. The cost is minutes. |
| "The external model doesn't know our context" | It doesn't need full context to find logic bugs and security holes. |
| "I'll just implement what it says" | Verify first. External models can be wrong too. Overlapping findings are the only auto-fix zone. |
| "This is too small for cross-model review" | Small changes break production. The review catches what single-model review misses. |

## Known Pitfalls

**Blindly implementing all external model findings.** The external model flagged 8 issues. All 8 were implemented without verification. 3 were genuine bugs, 2 were false positives (the external model didn't understand the framework convention), and 3 were style preferences that conflicted with the project's existing patterns. The "fixes" introduced 2 regressions.

*What went wrong:* Synthesis Rules say: "Unique findings from either model get investigated — verify they're real before acting on them." This rule was ignored in favor of "the external model found it, so it must be real."

*Prevention:* Only overlapping findings (both models agree) get auto-implemented. Unique findings must be verified against the actual codebase before acting. If the external model doesn't understand the framework, its architecture suggestions will be wrong for this project.

**Truncating the external model's output.** The external model produced 200 lines of review. The coordinator summarized it as "5 findings, all minor." The actual output contained a critical security finding buried in paragraph 4 that was lost in the summary.

*What went wrong:* Synthesis Rule 1 says "Present output verbatim." The coordinator summarized for brevity and dropped the most important finding.

*Prevention:* Present the full external model output before adding your commentary. If it's long, use collapsible sections — but include everything. Your summary comes AFTER the full output, never instead of it.

**External model reads skill files instead of source code.** The external model's output referenced "SKILL.md configuration" and commented on prompt engineering patterns. It didn't review the actual application code — it read the skills framework files and reviewed those instead.

*What went wrong:* The diff sent to the external model included skill files alongside source code. The model prioritized the more unusual files (skill definitions) over the routine application code.

*Prevention:* Synthesis Rule 3 says "Flag skill-file rabbit holes." If the external model's findings reference skill files, config files, or documentation instead of source code, warn the user and re-run with a more focused diff that excludes non-source files.
