# Implementation Plan: {PLAN_NAME}

> **Date:** {YYYY-MM-DD}
> **Design:** [DESIGN.md]({path/to/DESIGN.md})
> **Status:** In Progress

---

## Tasks

### Task 1: {TASK_NAME}

**Complexity:** Low / Medium / High
**Depends on:** None / Task N
**Files to modify:**
- `{exact/path/to/file}`

**Test to write:**
```{language}
{complete test code — no placeholders}
```

**Implementation:**
```{language}
{complete implementation code — no placeholders}
```

**Verification:**
- Run: `{exact command}`
- Expected: `{exact expected output}`

---

### Task 2: {TASK_NAME}

...

---

## Dependency Graph

```
Task 1 → Task 2 → Task 4
Task 1 → Task 3 ↗
Task 5 (independent)
```

Tasks with no dependencies can run in parallel. Dependencies are directional (A → B means A must complete before B starts).

## Task Summary

| # | Task | Complexity | Depends On | Status |
|---|------|-----------|------------|--------|
| 1 | {name} | Low | — | Pending |
| 2 | {name} | Medium | Task 1 | Pending |
| 3 | {name} | High | Task 1 | Pending |
| 4 | {name} | Medium | Task 2, 3 | Pending |
| 5 | {name} | Low | — | Pending |

## Self-Review Checklist

Before starting implementation, verify:

- [ ] Every task has exact file paths (no "the relevant file")
- [ ] No placeholders or TBDs in any code block
- [ ] Every task has a verification step with expected output
- [ ] Test steps come before implementation steps (TDD)
- [ ] Dependencies between tasks are explicit
- [ ] No task is larger than 5 minutes of focused work
