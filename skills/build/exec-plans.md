---
name: forge-exec
description: Use for sequential plan execution when the user wants to stay in the loop or subagent system is unavailable. Alternative to /forge-build.
---

# Sequential Plan Execution

## Overview

Execute `PLAN.md` task by task in the current session, with checkpoints between tasks for review.

**Announce:** "I'm using /forge-exec to implement this plan."

**Why sequential:** Sometimes you want to see each task as it happens — catch issues in real-time, provide guidance, or the subagent system simply isn't available. This trades speed for control.

## When to Use vs /forge-build

| Factor | /forge-exec (this) | /forge-build |
|--------|-------------------|-------------|
| User wants to stay in loop | ✅ | ❌ |
| Small project (1-3 tasks) | ✅ | Overkill |
| No subagent support | ✅ | ❌ |
| Large project (5+ tasks) | Slow | ✅ |
| Parallel tasks available | ❌ Sequential only | ✅ Parallel |

## The Process

### Step 1: Load and Review

1. Read `PLAN.md`
2. Review critically — identify questions or concerns
3. Raise concerns with the user before starting
4. No concerns? Create task tracking and proceed

### Step 2: Execute Tasks

For each task:

1. Mark as in_progress
2. Follow each step exactly (the plan has bite-sized steps)
3. Follow `/forge-tdd` for all code steps (test first, verify fail, implement, verify pass)
4. Run verifications as specified
5. Commit as specified
6. Mark as completed

### Step 3: Checkpoints

After each task, briefly summarize:
- What was done
- Test results
- Any deviations from the plan

This gives the user a natural pause point to intervene if needed.

### Step 4: Complete

After all tasks:
1. Run full test suite
2. Announce completion
3. Route to REVIEW phase or `/forge-finish`

## When to Stop

Stop immediately when:
- Hit a blocker (missing dependency, test fails, unclear instruction)
- Plan has critical gaps
- Verification fails repeatedly

Ask for help rather than guessing. Don't force through blockers.

## Key Reminders

- Follow plan steps exactly — don't skip or reorder
- Run every verification command — don't assume "it probably works"
- Follow `/forge-tdd` for all code changes
- Never start on main/master without explicit user consent
- Stop and ask when stuck — guessing wastes more time than asking
