---
name: taku-review-collab
description: >
  Two-mode review collaboration skill. Dispatch mode: send a structured review
  packet to a fresh-context reviewer subagent, then act on feedback. Receive mode:
  process incoming code review with 6-step protocol (Read, Understand, Verify,
  Evaluate, Respond, Implement) — never agree without verifying. Auto-detects
  mode based on context. Triggers on "request review", "get a review", "received
  feedback", "process review", "review my changes".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Review Collaboration — Dispatch + Receive

Two modes for handling code reviews. Dispatch sends a review to a fresh-context reviewer. Receive processes incoming feedback with technical rigor.

## Mode Detection

- About to send for review / "request review" / "get a review" → **Dispatch**
- Just received feedback / "process review" / "review feedback" → **Receive**
- Default: Dispatch

---

## Dispatch Mode

Review early, review often. The reviewer gets precisely crafted context — never your session's history.

### When to Dispatch

**Mandatory:** after each task in /taku-build, after major features, before merging.
**Optional:** when stuck, before refactoring, after fixing complex bugs.

### Step 1: Gather Context

Build the review packet. Do not skip any of these.

**1a. Git SHAs:**
```bash
BASE_SHA=$(git merge-base HEAD $(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||') 2>/dev/null || git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)
```

**1b. What was implemented:** Read PLAN.md or recent commit messages.

**1c. Requirements:** Read DESIGN.md for relevant sections.

**1d. Test results:** Run the test suite. Capture pass/fail counts.

**1e. Specific concerns:** Note areas of uncertainty.

### Step 2: Dispatch Reviewer

Send structured context to a fresh subagent:
- What was implemented
- Requirements
- Base and head SHAs
- Test results
- Specific concerns
- Ask for: correctness, edge cases, error handling, security, test coverage
- Rating: Critical / Important / Minor
- Assessment: APPROVE / APPROVE_WITH_CONCERNS / REQUEST_CHANGES

### Step 3: Act on Feedback

**Critical** → Fix immediately. Re-run tests. Re-review if non-trivial.
**Important** → Fix before next task. Break into own task if large.
**Minor** → Log. Fix if time permits. Don't block progress.
**Disagree** → Push back with technical reasoning. Reference code, tests, or requirements. Escalate to user if unresolved.

### Step 4: Record Outcome

Save to `.taku/reviews/`: what was reviewed, findings, fixes, pushbacks, assessment.

---

## Receive Mode

Code review requires technical evaluation, not emotional performance. Verify before implementing.

### The 6-Step Protocol

**1. READ** — Absorb the full feedback. Don't start fixing until you've read everything.

**2. UNDERSTAND** — Restate each finding in your own words. Can't restate it? Ask for clarification.

**Why restate:** If you can't explain a finding in your own words, you don't understand it well enough to evaluate it. Restating forces comprehension before judgment.

**3. VERIFY** — Is this finding technically correct for THIS codebase?
- Does the suggested fix apply here?
- Would it break existing functionality?
- Is the current implementation intentional (compatibility, legacy, documented tradeoff)?

**4. EVALUATE** — YAGNI check: does the codebase actually use what the reviewer wants improved? Priority: blocks current task? Affects user-facing behavior? Or just style?

**5. RESPOND** — For each finding:
- Correct → Fix it. State what changed. No gratitude performance.
- Unclear → Ask. Don't guess.
- Wrong → Push back with technical reasoning.
- Debatable → Present the tradeoff, let the user decide.

**6. IMPLEMENT** — Order: blocking issues first, then simple fixes, then complex fixes. Test after each fix.

### Forbidden Responses

NEVER: "You're absolutely right!" (verify first), "Great point!" (state requirement instead), "Let me implement that now" (verify first), batch fixes without testing.

INSTEAD: State the technical requirement, push back with reasoning, fix and show result, ask clarifying questions.

### When to Push Back

Push back when: finding is technically incorrect, reviewer lacks context, suggestion adds unused functionality (YAGNI), fix would break existing tests, suggestion conflicts with DESIGN.md.

If you pushed back and were wrong: state correction factually, fix it. No apology needed.

---

## Integration with Taku Pipeline

After /taku-build: review each task as it completes.
Before completing: final review gate, all critical and important findings resolved.

## Anti-Rationalization

| Excuse | Why it's wrong |
|--------|---------------|
| "Simple enough to skip review" | Simple code has subtle bugs. Review takes minutes. Bug takes hours. |
| "Reviewer doesn't understand our architecture" | Explain it in the context packet. Confused reviewer = insufficient context. |
| "I already checked it myself" | You wrote it. You have blind spots. That's the point. |
| "The reviewer is probably right" | Probably is not verification. Check the code. |
| "I'll implement it all to be safe" | Blind implementation introduces regressions. Verify first. |

## Known Pitfalls

**Agreeing with every piece of feedback without verifying.** The reviewer sent 5 findings. The implementer responded "You're absolutely right!" to all 5 and implemented every suggestion. Finding #3 was wrong — the "missing null check" was actually a validated enum with no null possibility. The unnecessary check added complexity.

*What went wrong:* The Forbidden Responses section says never say "You're absolutely right!" before verifying. The 6-Step Protocol (Read, Understand, VERIFY, Evaluate, Respond, Implement) was compressed into Read → Implement.

*Prevention:* The VERIFY step exists between understanding and responding. For each finding, check: is this technically correct for THIS codebase? Does the suggested fix apply here? Would it break existing functionality? Only after verification should you respond.

**Sending insufficient context in the dispatch packet.** The dispatch packet included the diff and commit messages but not the DESIGN.md requirements. The reviewer flagged a "missing feature" that was actually a deliberate scope exclusion documented in DESIGN.md. Time was wasted on a non-issue.

*What went wrong:* Step 1 (Gather Context) was incomplete. The requirements (DESIGN.md) were skipped because "the diff speaks for itself."

*Prevention:* The dispatch packet must include all five elements: git SHAs, what was implemented, requirements, test results, and specific concerns. If you skip requirements, the reviewer can't distinguish a bug from a deliberate exclusion.

**Implementing all fixes in one batch without testing between.** Three findings were received. All three fixes were applied in one editing session, then tests were run. Two tests failed. Which fix broke them? All three touched overlapping code. Now you're debugging your own fixes.

*What went wrong:* Step 6 of the Receive Protocol says: "Order: blocking issues first, then simple fixes, then complex fixes. Test after each fix." All three were batched.

*Prevention:* Fix one finding, run tests, verify. Then fix the next. This takes longer per-finding but produces a clean, debuggable history. If fixes conflict, you discover it one fix at a time, not three at once.
