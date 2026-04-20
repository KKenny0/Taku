---
name: taku-debug
description: >
  Use when encountering any bug, test failure, or unexpected behavior — systematic
  root cause investigation with 4 phases. Triggers on "debug this", "fix this bug",
  "why is this broken", "investigate this error", "it was working yesterday", or
  any troubleshooting where the cause is unknown. ALWAYS invoke this skill instead
  of proposing fixes directly.
---

# taku-debug — 4-Phase Root Cause Investigation

Random fixes create new bugs. Systematic investigation finds root causes. This skill merges the best of Superpowers' systematic debugging with gstack's investigate workflow into a unified 4-phase process.

## The Iron Law

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

Every fix that doesn't address root cause makes the next bug harder to find. If you haven't completed Phase 1 (INVESTIGATE), you cannot propose fixes. Period.

Violating the letter of this process is violating the spirit of debugging.

## The 4 Phases

### Phase 1: INVESTIGATE

Gather context before forming any hypothesis. This is evidence collection, not problem-solving.

1. **Read the error.** Stack traces, error messages, log output. Read them completely. Line numbers, file paths, error codes — all of it. The error message usually contains the answer.

2. **Reproduce consistently.** What are the exact steps? Does it happen every time? If not reproducible, gather more data. Don't guess at intermittent bugs.

3. **Check recent changes.**
   ```bash
   git log --oneline -20 -- <affected-files>
   git diff HEAD~1 -- <affected-files>
   ```
   Was this working before? What changed? A regression means the root cause is in the diff.

4. **Trace data flow backward.** Where does the bad value originate? What called this function with the bad value? Keep tracing up until you find the source. Fix at source, not at symptom.

5. **Gather evidence in multi-component systems.** When the system has layers (API → service → database), add diagnostic logging at each boundary. Run once. See WHERE it breaks. Then investigate THAT layer.

Output: **Root cause hypothesis** — a specific, testable claim about what is wrong and why.

### Phase 2: PATTERN

Match the bug against known patterns before proposing solutions.

| Pattern | Signature | Where to look |
|---------|-----------|---------------|
| Race condition | Intermittent, timing-dependent | Shared state, concurrent access |
| Null propagation | TypeError, NoMethodError | Missing guards on optional values |
| State corruption | Inconsistent data, partial updates | Transactions, callbacks, hooks |
| Integration failure | Timeout, unexpected response | API boundaries, service calls |
| Config drift | Works locally, fails elsewhere | Env vars, feature flags, secrets |
| Stale cache | Shows old data | Redis, CDN, browser cache |

Also check:
- Working examples in the same codebase — what does the same thing correctly?
- TODOS.md for related known issues
- Git log for prior fixes in the same area. Recurring bugs in the same files are an architectural smell, not a coincidence.

If the pattern isn't obvious, search the web for "{framework} {error type}" (sanitize first: strip hostnames, IPs, file paths, customer data).

### Phase 3: HYPOTHESIS

Form hypotheses ranked by likelihood. Test them one at a time.

1. **Rank hypotheses:**
   ```
   H1 (80%): Token expires between redirect and callback
   H2 (15%): CORS header missing on callback endpoint
   H3 (5%): Browser caches stale auth response
   ```

   Ranking forces you to think about probability, not just possibility. Test the most likely hypothesis first.

2. **Test minimally.** One variable at a time. The smallest change that confirms or denies the hypothesis. Add a log statement, an assertion, or a debug output. Run the reproduction.

3. **If confirmed:** Proceed to Phase 4 (IMPLEMENT).

4. **If denied:** Move to the next hypothesis. Before forming a new one, return to Phase 1 and gather more evidence. Don't guess.

5. **3-strike rule:** If 3 hypotheses fail, STOP. This is not a failed hypothesis — this is a wrong architecture or a fundamentally misunderstood system. Present options:
   - Continue investigating with a new theory
   - Escalate for human review
   - Add instrumentation and wait for the next occurrence

**Red flags — if you catch yourself thinking any of these, STOP:**
- "Quick fix for now, investigate later"
- "Just try changing X and see what happens"
- "Add multiple changes at once, run tests"
- Proposing solutions before tracing data flow
- "One more fix attempt" after 2+ failures

### Phase 4: IMPLEMENT

Fix the root cause, not the symptom.

1. **Write a failing test first.** The simplest reproduction of the bug as an automated test. If no test framework exists, write a one-off script. The test MUST fail before the fix.

2. **Implement the minimal fix.** One change. One root cause addressed. No "while I'm here" refactoring. No bundled improvements.

3. **Verify the fix.** Test passes? Full suite passes? Original bug scenario resolved?

4. **Blast radius check.** If the fix touches more than 5 files, stop and ask. A bug fix that large usually means you're fixing the wrong thing.

5. **Run the full test suite.** Paste the output. No regressions.

## Output: Debug Report

```
DEBUG REPORT
═════════════════════════════════════════
Symptom:         [what the user observed]
Root cause:      [what was actually wrong]
Hypotheses:      [H1: confirmed, H2: denied, H3: untested]
Fix:             [what changed, file:line references]
Evidence:        [test output, reproduction showing fix works]
Regression test: [file:line of new test]
Status:          DONE | DONE_WITH_CONCERNS | BLOCKED
═════════════════════════════════════════
```

## Status

- **DONE** — Root cause found, fix applied, regression test written, all tests pass.
- **DONE_WITH_CONCERNS** — Fixed but can't fully verify (intermittent bug, requires staging).
- **BLOCKED** — Root cause unclear after 3 hypotheses. Escalated.
