---
name: forge-tdd
description: Use whenever writing implementation code. Triggers during /forge-build, /forge-exec, or when the user starts implementing a feature.
---

# Test-Driven Development

## Overview

Write the test first. Watch it fail. Write the minimal code to pass it. Refactor.

**Core principle:** If you didn't watch the test fail, you don't know it tests the right thing.

## Why TDD Prevents Bugs

Tests written after code pass immediately — proving nothing. You might test the wrong thing, test implementation instead of behavior, or miss edge cases entirely.

Test-first forces you to see the test fail first, proving it actually catches the bug you're about to fix. This single discipline prevents an entire class of defects: code that "should work" but doesn't.

**Order matters:**
- Tests-after answer "What does this do?" — biased by your implementation
- Tests-first answer "What should this do?" — driven by requirements

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before the test? Delete it. Not "save as reference," not "adapt while writing tests." Delete it completely and start fresh from tests.

## RED-GREEN-REFACTOR Cycle

### RED — Write Failing Test

One minimal test. Clear name. Real code (no mocks unless unavoidable).

```python
def test_retries_failed_operations_three_times():
    attempts = 0
    def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError("fail")
        return "success"

    result = retry_operation(operation)
    assert result == "success"
    assert attempts == 3
```

### Verify RED — Watch It Fail

Run the test. Confirm:
- It fails (not errors out)
- Failure message matches expectations (missing function, not typo)
- It fails because the feature doesn't exist yet

Test passes immediately? Wrong test — it's verifying existing behavior. Delete and rewrite.

### GREEN — Minimal Code

Write the simplest code that makes the test pass. No extra features, no "while I'm here" improvements.

```python
def retry_operation(fn, max_retries=3):
    for i in range(max_retries):
        try:
            return fn()
        except Exception:
            if i == max_retries - 1:
                raise
```

### Verify GREEN — Watch It Pass

Run all tests. Confirm:
- New test passes
- All existing tests still pass
- Output is clean (no warnings, no skips)

### REFACTOR — Clean Up

Remove duplication, improve names, extract helpers. Keep tests green. No new behavior.

## Anti-Rationalization Table

| Excuse | Why it's wrong |
|--------|---------------|
| "Too simple to test" | Simple code breaks too. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what did I build?" Tests-first = "what should I build?" |
| "Already manually tested" | Ad-hoc testing has no record, can't re-run, easy to forget cases. |
| "Deleting X hours of work is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll unconsciously adapt it. That's testing after. Delete means delete. |
| "Need to explore the design first" | Fine — throw away exploration, start fresh with TDD. |
| "Test is hard to write" | Hard to test = hard to use. The test is telling you something. |
| "TDD will slow me down" | TDD is faster than debugging in production. Always. |
| "This is different because..." | It's not. |

Any of these running through your head? Stop. Delete the code. Write the test first.

## When TDD Doesn't Apply

Ask your human partner for these cases:
- Throwaway prototypes
- Generated code
- Pure configuration files

Everything else gets a test first.

## Good Tests

- **Minimal:** One behavior per test. "and" in the name? Split it.
- **Clear:** Name describes the expected behavior, not the implementation.
- **Shows intent:** Demonstrates the desired API surface.

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for the expected reason
- [ ] Wrote minimal code to pass
- [ ] All tests pass with clean output
- [ ] Edge cases and error paths covered

## Debugging Integration

Found a bug? Write a failing test that reproduces it first. Follow the TDD cycle. The test proves the fix works and prevents regression.

Never fix a bug without a test.
