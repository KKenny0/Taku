---
name: taku-build
description: >
  Execute an approved implementation plan. Two execution modes: subagent/parallel
  (default for 5+ tasks, dispatches one agent per task) and sequential (step-by-step
  with checkpoints). TDD enforced on all code. Optional worktree isolation for
  feature branches. Triggers after /taku-plan, or on "build this", "implement the plan",
  "start coding", "run the plan", "execute tasks". Also handles worktree setup on
  "create a worktree", "isolated environment", "new branch workspace".
---

# Taku Build — Parallel or Sequential Execution

Execute PLAN.md tasks. Two modes, auto-selected.

## Pre-Build Check

Before starting implementation:

1. **PLAN.md exists?** If not, route to `/taku-plan`.
2. **Worktree needed?** If the feature needs isolation from current workspace, set up a worktree first. Full process in `references/worktrees.md`.
3. **Load TDD rules.** All code follows test-first discipline. Full cycle in `references/tdd.md`. The iron law: no production code without a failing test first.

---

## Mode Selection

| Factor | Subagent (parallel) | Sequential |
|--------|-------------------|------------|
| Task count | 5+ tasks | 1-3 tasks |
| Subagent support | Available | Unavailable or user prefers |
| User wants to watch | No | Yes |
| Independent tasks | Yes → big speedup | No speedup |
| Large project | Best fit | Slow but safe |

**Default:** Subagent if 5+ tasks and subagents available. Sequential otherwise.

**Override:** User can specify "parallel" or "sequential" at any time.

---

## Subagent Mode (Parallel)

Execute PLAN.md by dispatching subagents — one per task, with two-stage review after each. Independent tasks run in parallel. Dependent tasks run sequentially.

**Announce:** "Using /taku-build (parallel mode)."

### Core Loop

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

### Dependency Analysis

Parse each task in PLAN.md:
1. **Read all tasks** — extract file lists from each task's "Files:" section
2. **Build DAG** — task A depends on task B if A modifies files B creates/depends on
3. **Topological sort** — identify waves of independent tasks
4. **Label each task** — `parallel-ready` or `blocked-by: [task IDs]`

If any file appears in more than one task, mark those tasks as dependent — they must run sequentially.

### Model Selection

| Task Type | Model | Why |
|-----------|-------|-----|
| Mechanical (1-2 files, complete spec) | Fast/cheap | Clear instructions, no judgment needed |
| Integration (multi-file, cross-cutting) | Standard | Needs to understand how pieces fit |
| Architecture (design decisions, broad impact) | Powerful | Requires deep reasoning |

### Subagent Context Format

Every subagent receives structured context built from the plan:

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
{exact_code_from_plan}

### Tests to write
{test_code_from_plan}

### Verification
- Run: `{command}`
- Expected: `{output}`

### Constraints
- Follow TDD: test first, then implement (see references/tdd.md)
- Commit after each passing test
- If blocked, report BLOCKED with reason
- Do NOT modify files outside the list above
```

For dependent tasks, include relevant code from completed tasks in the context. Reference exact file paths and line numbers. The implementer should never guess at interfaces.

### Status Handling

- **DONE** → Proceed to spec compliance review
- **DONE_WITH_CONCERNS** → Read concerns, address correctness issues, proceed
- **NEEDS_CONTEXT** → Provide missing information, re-dispatch
- **BLOCKED** → Assess: context problem → provide more; reasoning → better model; task too large → re-plan; plan wrong → escalate to human

**Never** ignore an escalation or retry with no changes.

DONE_WITH_CONCERNS always requires reading the concerns. Address correctness issues immediately. If concerns are non-critical (style, naming), note and proceed.

### Two-Stage Review

After each task:

**Stage 1: Spec Compliance** — Does implementation match the plan? All criteria met? Nothing extra or missing?

**Stage 2: Code Quality** — Well-built? Naming, structure, coverage, edge cases.

Fix issues between stages. Don't proceed to Stage 2 until Stage 1 passes.

### Reconciliation (After Parallel Wave)

1. Check for file conflicts between parallel tasks
2. Run integration tests
3. Verify task boundaries (no task leaked into another's files)

Reconciliation is never optional. After every parallel wave, always check for conflicts before dispatching the next wave.

---

## Sequential Mode

Execute PLAN.md task by task with checkpoints.

**Announce:** "Using /taku-build (sequential mode)."

### Step 1: Load and Review

1. Read PLAN.md
2. Review critically — identify questions or concerns
3. Raise concerns with the user before starting
4. No concerns? Create task tracking and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly
3. Follow TDD for all code steps (load `references/tdd.md` for cycle details)
4. Run verifications as specified
5. Commit as specified
6. Mark as completed

If a step seems wrong, raise it before deviating — don't silently adapt.

### Step 3: Checkpoints

After each task, briefly summarize: what was done, test results, deviations.

### Step 4: Complete

After all tasks: run full test suite, announce completion, route to REVIEW phase.

---

## Shared Rules (Both Modes)

**Don't:**
- Dispatch multiple subagents that modify the same files
- Let subagents read the plan file (provide full text in context)
- Skip either review stage
- Accept "close enough" on spec compliance
- Ignore escalations

**Do:**
- Answer subagent questions clearly
- Re-review after every fix
- Provide complete context upfront
- Follow TDD for all code changes
- Stop and ask when stuck

## When to Stop

Stop immediately when: blocker hit, plan has critical gaps, verification fails repeatedly.
Ask for help rather than guessing.

## Completion

After all tasks: run full test suite, route to REVIEW phase (`/taku-review`).

---

## Known Pitfalls

**Parallel subagents modifying the same file.** Both subagents wrote to `utils/auth.py` simultaneously. One commit overwrote the other silently.

*Prevention:* During Dependency Analysis, grep all tasks' file lists for duplicates. Any file in more than one task → mark dependent, run sequentially.

**Subagent received partial context.** Task 4 referenced a `UserStore` from Task 2, but the subagent only got Task 4's description. It invented its own `UserStore` with different signatures.

*Prevention:* For dependent tasks, include relevant code from completed tasks in context. Reference exact file paths and line numbers.

**Skipping reconciliation between waves.** Three parallel tasks completed. Next wave started without checking. Two had added imports to the same file — combined result had duplicate imports and circular dependency.

*Prevention:* Reconciliation is never optional. Always check for conflicts between waves.
