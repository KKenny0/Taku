---
name: forge-verify
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

### 2. RUN
Execute the FULL command. Fresh, complete, no shortcuts.
- Not a partial run
- Not a cached result
- Not "I ran it earlier"

### 3. READ
Read the FULL output. Check exit code. Count failures.
- Don't skim. Read every line of relevant output.
- Note the exact pass/fail counts.

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
