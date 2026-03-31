---
name: forge-build
description: Use when the user has an approved plan and wants to implement it. Triggers after /forge-plan. Supports parallel sprint execution.
---

# Subagent-Driven Development + Parallel Sprints

## Overview

Execute `PLAN.md` by dispatching subagents — one per task, with two-stage review after each. Independent tasks run in parallel. Dependent tasks run sequentially.

**Announce:** "I'm using /forge-build to execute this plan."

**Why subagents:** Fresh context per task means no pollution from earlier work. The implementer sees exactly what it needs — no more, no less. This preserves your context for coordination and review.

## When to Use

- Have an approved `PLAN.md`
- Tasks are well-defined (exact file paths, complete code)
- Want fast iteration with automatic review gates

**Alternative:** `/forge-exec` for sequential execution when you want to stay in the loop or subagents aren't available.

## Core Loop

```
Read PLAN.md
    → Parse tasks, build dependency DAG
    → Group: independent tasks (parallel) vs dependent tasks (sequential)
    → Dispatch independent tasks in parallel
    → Wait for completion (push-based)
    → Reconcile: check conflicts, run integration tests
    → Dispatch next wave of now-unblocked tasks
    → Repeat until all tasks complete
    → Final integration review
    → Route to REVIEW phase
```

## Dependency Analysis

Parse each task in PLAN.md to identify dependencies:

1. **Read all tasks** — extract file lists from each task's "Files:" section
2. **Build DAG** — task A depends on task B if A modifies files B creates/depends on
3. **Topological sort** — identify waves of independent tasks
4. **Label each task** — `parallel-ready` or `blocked-by: [task IDs]`

If all tasks are independent, everything runs in parallel. If all are sequential, it degrades gracefully to one-at-a-time.

## Model Selection

Use the least powerful model that can handle the task:

| Task Type | Model | Why |
|-----------|-------|-----|
| Mechanical (1-2 files, complete spec) | Fast/cheap | Clear instructions, no judgment needed |
| Integration (multi-file, cross-cutting) | Standard | Needs to understand how pieces fit |
| Architecture (design decisions, broad impact) | Powerful | Requires deep reasoning |

Most implementation tasks are mechanical when the plan is well-specified.

## Subagent Context Format

Every subagent receives structured context. Build this from the plan — don't make the subagent read the plan file.

```markdown
## Task Context

### Task: {task_name}
**From plan:** PLAN.md
**Priority:** {high|medium|low}
**Model recommendation:** {fast|standard|powerful}

### What to implement
{task_description_from_plan}

### Files to modify
- Create: `{exact_path}`
- Modify: `{exact_path}:{line_range}`
- Test: `{exact_path}`

### Code to write
```{language}
{exact_code_from_plan}
```

### Tests to write
```{language}
{test_code_from_plan}
```

### Verification
- Run: `{command}`
- Expected: `{output}`

### Constraints
- Follow /forge-tdd: test first, then implement
- Commit after each passing test
- If blocked, report BLOCKED with reason
- Do NOT modify files outside the list above
```

## Parallel Dispatch

For each wave of independent tasks:

1. **Prepare context** for each task (extract from plan, build structured markdown)
2. **Dispatch all tasks in the wave** simultaneously
3. **Wait** — results arrive push-based (don't poll)
4. **Process each result** (see status handling below)

## Status Handling

Implementer subagents report one of four statuses:

### DONE
Proceed to spec compliance review.

### DONE_WITH_CONCERNS
The implementer completed the work but flagged doubts. Read the concerns before proceeding:
- Correctness or scope concerns → address before review
- Observations ("this file is getting large") → note, proceed to review

### NEEDS_CONTEXT
The implementer needs information not in the context. Provide the missing context and re-dispatch. Don't just tell it to try again — give it the actual information.

### BLOCKED
The implementer cannot complete the task. Assess:
1. Context problem → provide more context, re-dispatch with same model
2. Reasoning insufficient → re-dispatch with more capable model
3. Task too large → break into smaller pieces, re-plan
4. Plan itself is wrong → escalate to the human

**Never** ignore an escalation or retry the same model with no changes.

## Two-Stage Review

After each task completes (whether DONE or DONE_WITH_CONCERNS):

### Stage 1: Spec Compliance

Does the implementation match what the plan asked for?
- All acceptance criteria met?
- Nothing extra added?
- Nothing missing?

If issues found → implementer fixes → re-review. Don't proceed to stage 2 until spec is clean.

### Stage 2: Code Quality

Now that the spec is met, is the implementation well-built?
- Code quality, naming, structure
- Test coverage
- Edge cases handled
- No magic numbers, no dead code

If issues found → implementer fixes → re-review.

## Reconciliation (After Parallel Wave)

When multiple tasks complete in parallel:

1. **Check for file conflicts** — did two tasks modify the same file?
   - No conflicts → proceed
   - Conflicts → manually merge, run tests, verify
2. **Run integration tests** — do the parallel pieces work together?
3. **Verify task boundaries** — did any task leak into another's files?

If reconciliation finds issues, fix them before proceeding to the next wave.

## Sequential Fallback

When tasks have dependencies:

1. Execute the blocking task first
2. Wait for it to complete + pass review
3. Now the dependent task is unblocked — add it to the next parallel wave

If a single long dependency chain exists, it runs fully sequential. That's fine — the parallel speedup comes from independent branches.

## Red Flags

**Don't:**
- Dispatch multiple subagents that modify the same files
- Let subagents read the plan file (provide full text in context)
- Skip either review stage
- Proceed with open review issues
- Accept "close enough" on spec compliance
- Start code quality review before spec compliance passes
- Ignore subagent questions or escalations

**Do:**
- Answer subagent questions clearly before letting them proceed
- Re-review after every fix (don't assume the fix worked)
- Provide complete context upfront (reduces back-and-forth)

## Completion

After all tasks complete:

1. Run full test suite
2. Dispatch final integration review (checks cross-task consistency)
3. Route to REVIEW phase (/forge-review) or offer branch completion (/forge-finish)

## Integration Notes

- Requires: `/forge-plan` (creates the plan), `/forge-tdd` (subagents follow TDD)
- Alternative: `/forge-exec` (sequential execution)
- Post-build: `/forge-review` (code review), `/forge-verify` (evidence gate), `/forge-finish` (branch completion)
