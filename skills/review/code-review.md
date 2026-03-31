---
name: forge-review
description: Use after implementation is complete. Triggers after /forge-build or /forge-exec. Analyzes diffs for security issues, bugs, and code quality. Run when asked to "review this", "check my diff", "code review", or before shipping. Proactively invoke when the user is about to merge or land code changes.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
---

# Pattern-Based Code Review

Analyze the current branch's diff against the base branch for structural issues that tests don't catch. Fix-first, not read-only.

## Step 1: Detect Base Branch

```bash
git remote get-url origin 2>/dev/null
git branch --show-current
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||'
```

Detect platform (GitHub/GitLab/unknown) and determine the base branch. If no PR exists, use the default branch. Print the base branch name for all subsequent steps.

## Step 2: Check Branch

1. If on the base branch: "Nothing to review, you're on the base branch." Stop.
2. Fetch and diff: `git fetch origin <base> --quiet && git diff origin/<base> --stat`
3. If no diff: stop with the same message.

## Step 3: Scope Drift Check

Read commit messages and any plan file (PLAN.md, .forge/*.md). Compare stated intent against files changed.

- **Scope creep:** files changed unrelated to intent
- **Missing requirements:** intent items not addressed in the diff

Output:
```
Scope Check: [CLEAN / DRIFT DETECTED / REQUIREMENTS MISSING]
Intent: <1-line summary>
Delivered: <1-line summary>
```

This is informational, not a gate. Continue to Step 4.

## Step 4: Get the Diff

```bash
git fetch origin <base> --quiet
git diff origin/<base>
```

Read the full diff. This is your review input.

## Step 5: Two-Pass Review

Apply these check categories in two passes.

### Pass 1 — Critical

These are bugs that blow up in production:

**SQL injection risk**
- String concatenation or interpolation in SQL queries
- Missing parameterized queries
- Raw SQL without sanitization

**LLM trust boundary**
- User input passed directly to LLM prompts without sanitization
- No output validation after LLM response
- Prompt injection vectors (user-controlled system prompts)

**Conditional side effects**
- Mutations hidden in ternaries, short-circuits, or optional chaining
- Side effects in conditionals that only execute sometimes
- `&&` used for side effects (e.g., `condition && mutate()`)

**Auth gaps**
- Missing auth checks on routes or API endpoints
- Overly permissive scopes or wildcard permissions
- Auth bypasses in error paths

**Race conditions**
- Shared mutable state without locks
- Read-modify-write without atomic operations
- Concurrent access to non-thread-safe resources

### Pass 2 — Informational

These degrade quality over time:

**Resource leaks**
- Unclosed connections, file handles, or streams
- Missing cleanup in error paths
- Event listeners not removed on unmount

**Error handling**
- Swallowed errors (empty catch blocks)
- Missing error paths for async operations
- Errors that return undefined instead of meaningful values

**Type safety**
- `any` casts that hide bugs
- Missing null/undefined checks after optional access
- Type assertions that override the compiler

### Confidence Scores

Every finding includes confidence (1-10):

| Score | Meaning | Display |
|-------|---------|---------|
| 9-10 | Verified with code evidence | Show normally |
| 7-8 | Strong pattern match | Show normally |
| 5-6 | Could be false positive | Show with caveat |
| 3-4 | Suspicious but may be fine | Appendix only |
| 1-2 | Speculation | Report only if Critical |

Format: `[SEVERITY] (confidence: N/10) file:line — description`

### Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **Critical** | Exploitable or data-loss bug | Auto-fix immediately |
| **Important** | Real bug, production impact | Auto-fix immediately |
| **Minor** | Code quality, no immediate impact | Flag for awareness |
| **Nit** | Style, naming, convention | Mention in passing |

## Step 6: Fix-First Review

Every finding gets action.

### 6a: Auto-fix Critical and Important

Apply the fix directly. Output one line per fix:
`[AUTO-FIXED] [file:line] Problem → what you did`

Commit auto-fixes atomically:
```bash
git add <fixed-files> && git commit -m "fix: code review auto-fixes"
```

### 6b: Batch-ask about Minor findings

If Minor findings remain, present in one batch:

```
N minor issues found:

1. [MINOR] file:line — description
   Fix: recommendation
   → A) Fix  B) Skip

RECOMMENDATION: Fix because...
```

### 6c: Apply user-approved fixes

Apply fixes where user chose "Fix." Commit separately.

## Step 7: Output Summary

```
Pre-Landing Review: N issues (X auto-fixed, Y asked, Z skipped)
  Critical: N  Important: N  Minor: N  Nit: N
```

If no issues: "Pre-Landing Review: No issues found."

## Important Rules

- Read the FULL diff before commenting. Don't flag issues already addressed.
- Be terse. One line problem, one line fix.
- Only flag real problems. Skip anything that's fine.
- Never commit, push, or create PRs. That's /forge-ship's job.
- Verify your claims. Cite specific lines. Never say "probably fine."
