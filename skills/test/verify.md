---
name: taku-verify
description: Use before claiming any task is complete. Enforces evidence-based completion — no 'should work' without running the verification command. Triggers before commits, PRs, task completion, or any positive status claim.
---

# Evidence-Based Completion Gate

Claiming work is complete without verification is dishonesty, not efficiency.

## The Iron Law

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE**

If you haven't run the verification command in this message, you cannot claim it passes.

## The 5-Step Gate

Before claiming any status or expressing satisfaction:

### 1. IDENTIFY
What command proves this claim? Not "a test", the exact command.
- Tests pass → `npm test` or `pytest` or `cargo test`
- Linter clean → `eslint .` or `ruff check .`
- Build succeeds → `npm run build` or `go build ./...`
- Bug fixed → the specific test that reproduces the bug

**Why identify the exact command:** "Run the tests" is vague. Which test file? Which test runner? With what flags? The exact command eliminates ambiguity and makes the verification reproducible.

### 2. RUN
Execute the FULL command. Fresh, complete, no shortcuts.
- Not a partial run
- Not a cached result
- Not "I ran it earlier"

**Why fresh and full:** Cached results hide changes. Partial runs miss failures in untested files. "Earlier" runs predate the code you're verifying now. Only a fresh, full run produces trustworthy evidence.

### 3. READ
Read the FULL output. Check exit code. Count failures.
- Don't skim. Read every line of relevant output.
- Note the exact pass/fail counts.

**Why read the full output:** Test suites report failures at the bottom. Skimming the green dots at the top gives false confidence. The exit code is the ground truth — if it's non-zero, something failed regardless of how the output looks.

### 4. VERIFY
Does the output confirm the claim?
- **NO:** State the actual status with evidence. Stop.
- **YES:** Proceed to step 5.

### 5. CLAIM
Only now can you state the result, with the evidence attached.

Skipping any step is lying, not verifying.

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Full test output showing 0 failures | "Should pass", previous run |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, "looks good" |
| Bug fixed | Test reproducing bug now passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |

## Red Flags — STOP

- Using "should", "probably", "seems to", "I believe"
- Expressing satisfaction before verification ("Done!", "Perfect!")
- About to commit/push/PR without verification
- Trusting agent success reports without independent check
- Relying on partial verification
- Thinking "just this once"

## Anti-Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Should work now" | Run the verification |
| "I'm confident" | Confidence is not evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter is not a compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion is not an excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so the rule doesn't apply" | Spirit over letter |

## Why This Matters

From real failure patterns:
- "I don't believe you" — trust broken when claims don't match reality
- Undefined functions shipped — would crash at runtime
- Missing requirements shipped — incomplete features in production
- Time wasted on false completion, then redirect, then rework

## When To Apply

Always before:
- Any success/completion claim
- Any positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

The rule applies to exact phrases, paraphrases, synonyms, implications, and any communication suggesting completion or correctness.

## Regression Tests (Red-Green)

When writing a regression test, verify the red-green cycle:
1. Write test → Run → MUST FAIL with the expected error
2. Write fix → Run → MUST PASS
3. Revert fix → Run → MUST FAIL AGAIN
4. Restore fix → Run → MUST PASS

Skipping the re-verify step means you don't know if the test actually catches the regression.

## The Bottom Line

Run the command. Read the output. Then claim the result. No shortcuts.

## Known Pitfalls

**Claiming "tests pass" based on a previous run.** Tests ran 30 minutes ago and passed. Code changed since then (review fixes, dependency updates, config changes). The completion claim says "all tests pass" but the claim is based on stale evidence.

*What went wrong:* The Iron Law says "If you haven't run the verification command in this message, you cannot claim it passes." The previous run was in a different message, before changes were made.

*Prevention:* RUN (Step 2) requires executing the FULL command, fresh, right now. Not "I ran it earlier." Not "they passed before the changes." If code changed, re-run. This is the most commonly violated step and the most important one.

**Reading partial output and extrapolating.** The test output showed 145 passing tests before scrolling past the visible terminal. The bottom line said "Test run completed." The developer claimed all tests pass. 3 tests actually failed, but they were scrolled off-screen in the output.

*What went wrong:* READ (Step 3) says "Read the FULL output. Check exit code." The output was skimmed, not read. The exit code wasn't checked.

*Prevention:* Always check the exit code (`echo $?`). Always read the summary line that shows pass/fail/skip counts. If the output is long, scroll to the end first — that's where the summary is. "145 passed, 3 failed" at the bottom tells you more than 145 green dots at the top.

**Trusting an agent's "success" report without independent verification.** A subagent reported "Task complete, all tests pass." The coordinator marked the task DONE and moved on. The subagent's test run had actually failed — it ran a different test file than the one that contained the relevant tests.

*What went wrong:* Common Failures table says "Agent completed" requires "VCS diff shows changes," not "Agent reports success." The coordinator trusted the agent's self-assessment.

*Prevention:* After any agent completes, run the verification yourself. Don't trust the agent's report of success. Check the diff. Run the test suite. Agents have context limits and can misidentify which tests are relevant to their task.
