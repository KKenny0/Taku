---
name: taku-review
description: Use after implementation is complete. Triggers after /taku-build or /taku-build (sequential mode). Analyzes diffs for security issues, bugs, and code quality. Run when asked to "review this", "check my diff", "code review", or before shipping. Proactively invoke when the user is about to merge or land code changes.
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

Read commit messages and any plan file (PLAN.md, .taku/*.md). Compare stated intent against files changed.

- **Scope creep:** files changed unrelated to intent
- **Missing requirements:** intent items not addressed in the diff

Output:
```
Scope Check: [CLEAN / DRIFT DETECTED / REQUIREMENTS MISSING]
Intent: <1-line summary>
Delivered: <1-line summary>
```

This is informational, not a gate. Continue to Step 3b.

**Why scope check before code review:** If the diff includes unrelated changes, reviewing those wastes effort. If requirements are missing, no amount of code review will catch them. Scope check focuses the code review on the right surface area.

## Step 3b: Spec Compliance Check

If PLAN.md exists, verify that the implementation matches the plan's specs — not just that the right files were touched, but that the right behavior was built.

Read each task's **Spec** and **TDD anchor** from PLAN.md. For each spec assertion, search the diff for corresponding implementation:

- **MATCHED** — Spec assertion has implementing code and a test
- **MISSING** — Spec assertion not addressed in the diff
- **DIFFERENT** — Implementation exists but contradicts the spec

Output:
```
Spec Compliance: [FULL / PARTIAL / DRIFT]
  Task 1: N/N specs matched
  Task 2: N/N specs matched [MISSING: ...] [DIFFERENT: ...]
```

MISSING or DIFFERENT items are promoted to Critical in Step 5. This check ensures the review catches behavioral drift even when code quality is high.

**Why spec compliance matters:** A scope check verifies the right files were touched. A code review verifies the code is well-written. But neither catches the case where well-written code implements the wrong behavior — a function that returns 401 when the spec says 403, or a cache that stores data the spec says should expire. Spec compliance closes this gap.

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

**Why Critical first, separate pass:** Critical findings change code. If you review everything at once, you risk flagging code that will be rewritten by a Critical fix. Pass 1 identifies what must change; fix those first; then Pass 2 reviews the remaining diff with fresh eyes.

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

**Why explicit confidence:** Low-confidence findings waste reviewer time and erode trust. A finding at 3/10 is speculation — it belongs in an appendix, not in the main review. The confidence score forces honest assessment and helps the developer prioritize which findings to investigate first.

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
- Never commit, push, or create PRs. Focus on reviewing, not shipping.
- Verify your claims. Cite specific lines. Never say "probably fine."

## Known Pitfalls

**Auto-fixing without understanding the full context.** The diff showed a SQL query with string concatenation. The reviewer auto-fixed it with parameterized queries. The fix broke the application because the query was dynamically constructed across three functions — the parameterized version couldn't handle the dynamic table name.

*What went wrong:* The Critical auto-fix was applied based on a pattern match without understanding how the code actually used the query. "SQL injection risk" was the correct pattern, but the fix was wrong for this specific usage.

*Prevention:* Auto-fix Critical and Important findings, but verify the fix compiles and tests pass immediately after. If the fix breaks something, read the surrounding context before re-fixing. Pattern matching catches issues; understanding context produces correct fixes.

**Flagging issues already addressed later in the diff.** The reviewer flagged a missing null check on line 45. But line 62 in the same diff added a null-safe wrapper that handles it. The finding was correct in isolation but wrong in context.

*What went wrong:* The Important Rule says "Read the FULL diff before commenting." The reviewer processed the diff linearly, flagging issues as they appeared, rather than reading the entire diff first.

*Prevention:* Step 5 (Two-Pass Review) applies checks to the FULL diff, not line by line. Read everything first. Then review. A finding in the first half of the diff may be addressed in the second half.

**Nit-finding explosion drowning real issues.** The review produced 47 findings: 2 Critical, 3 Important, 6 Minor, and 36 Nits about naming conventions, comment style, and formatting. The 5 real findings were buried in noise. The developer fixed all 36 Nits first (easy wins) and missed one Critical.

*What went wrong:* The reviewer treated every style observation as a finding. Nit severity exists to de-prioritize these, but 36 of them still dominated the output.

*Prevention:* "Only flag real problems. Skip anything that's fine." Nits should be rare — mention 2-3 at most in passing, not catalogued. If the code style is consistently different from your preference, make ONE note about the pattern, not 36 individual findings. The signal-to-noise ratio determines whether the review is useful.
