---
name: taku-build
description: >
  Execute an approved implementation plan. Three execution modes: sequential,
  parallel, and hybrid wave-based execution. The agent chooses the mode and
  continues immediately, while still honoring explicit user overrides. TDD is
  enforced on all code. Optional worktree isolation for feature branches. Triggers
  after /taku-plan, or on "build this", "implement the plan", "start coding",
  "run the plan", "execute tasks". Also handles worktree setup on
  "create a worktree", "isolated environment", "new branch workspace".
---

# Taku Build — Autonomous Execution

Execute PLAN.md tasks. Choose the execution mode yourself and continue immediately.

## Pre-Build Check

Before starting implementation:

1. **PLAN.md exists?** If not, route to `/taku-plan`.
2. **Read the Build Agent Contract.** If PLAN.md has a `Build Agent Contract` block in its header, follow it: read Required fields first, reference Optional fields from `DESIGN.md` as needed, skip review artifacts.
3. **Check Execution Hints.** If PLAN.md has an `Execution Hints` section, use it as a starting recommendation for mode selection. You own the final decision and may override.
4. **Worktree needed?** If the feature needs isolation from current workspace, set up a worktree first. Full process in `references/worktrees.md`.
5. **Load TDD rules.** All code follows test-first discipline. Full cycle in `references/tdd.md`. The iron law: no production code without a failing test first.

---

## Mode Selection

Mode selection is agent-owned.

- Choose the execution mode yourself and continue immediately.
- Do not ask the user to choose a mode unless the user explicitly requests an override, or the choice would change risk/cost in a way that needs product input.
- The user may override the mode at any time.
- Always explain the chosen mode in one short reason statement.
- For hybrid and multi-task parallel runs, expose execution waves so the user can see which `wave-slug` contains which `task-slug` values.

| Mode | Use When | Shape |
|------|----------|-------|
| Sequential | Tasks are tightly coupled, each step depends on the latest result, or conflict/rework risk is high | End-to-end in order |
| Parallel | Most tasks are independent and boundaries are clear | One or more parallel waves |
| Hybrid | The plan is best executed in waves: waves depend on earlier waves, but tasks inside a wave can run in parallel | Sequential waves with parallel work inside each wave |

### Execution Waves

When tasks are grouped into waves:

1. Prefer existing identifiers from the plan.
2. If the plan has no wave IDs, generate stable `wave-1`, `wave-2`, `wave-3` style slugs from the dependency grouping.
3. Reuse plan task IDs when available. Otherwise, derive stable kebab-case `task-slug` values from task titles.
4. Keep the same wave and task slugs for the full BUILD lifecycle.

Before execution, announce the schedule in this shape:

```text
BUILD PREFLIGHT
- Mode: hybrid
- Reason: work is best executed in 3 waves
- Waves:
  - wave-1: [task-slug-a, task-slug-b]
  - wave-2: [task-slug-c, task-slug-d]
  - wave-3: [task-slug-e]
- Worktree: not needed
- TDD: enabled
- Next: start wave-1
```

During execution, report wave progress in this shape:

```text
BUILD UPDATE
- Completed: wave-1
- Tasks: [task-slug-a, task-slug-b]
- Result: tests passed
- Next: start wave-2
```

After execution, summarize completed waves in this shape:

```text
BUILD COMPLETE
- Executed waves:
  - wave-1: [task-slug-a, task-slug-b]
  - wave-2: [task-slug-c, task-slug-d]
  - wave-3: [task-slug-e]
- Next: REVIEW
```

---

## Parallel Mode

Execute PLAN.md by dispatching subagents. Independent tasks run in parallel, with reconciliation after each wave.

**Announce:** Use the BUILD PREFLIGHT format and show the parallel wave layout.

### Core Loop

```
Read PLAN.md
    → Parse tasks, build dependency DAG
    → Group tasks into execution waves
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
5. **Assign slugs** — every wave gets a `wave-slug`; every task gets a stable `task-slug`

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
**Depends on:** {task_ids or "none"}

### Files to modify
- Create: `{exact_path}`
- Modify: `{exact_path}:{line_range}`
- Test: `{exact_path}`

### Spec
{spec_from_plan}

### TDD Anchor
{tdd_anchor_from_plan}

### Verification
- Run tests for TDD anchor
- Expected: all assertions pass

### Constraints
- Follow TDD: write the anchor test first, then implement (see references/tdd.md)
- Commit after each passing test
- If blocked, report BLOCKED with reason
- Do NOT modify files outside the list above
```

For dependent tasks, include relevant specs and file paths from completed tasks in the context. The implementer should never guess at interfaces.

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

## Hybrid Mode

Use hybrid mode when the plan is best executed in waves.

- Waves themselves run sequentially because later waves depend on earlier ones.
- Within a wave, independent tasks may run in parallel.
- Choose hybrid when full parallelism creates too much conflict or uncertainty, but full sequential execution would be unnecessarily slow.

**Announce:** Use the BUILD PREFLIGHT format and show every planned wave with its `wave-slug` and `task-slug` list.

### Hybrid Loop

```
Read PLAN.md
    → Parse tasks, build dependency DAG
    → Partition the plan into execution waves
    → Run wave-1
    → Reconcile and report wave-1 completion
    → Run next unblocked wave
    → Repeat until all waves complete
    → Final integration review
    → Route to REVIEW phase
```

Use the same dependency and reconciliation rules as parallel mode. The difference is scheduling: waves are the first-class unit, and each wave may contain either parallel work or a single sequential task.

---

## Sequential Mode

Execute PLAN.md task by task with checkpoints.

**Announce:** Use a concise BUILD PREFLIGHT. You may omit the wave list, or present the full run as `wave-1` when that helps the user track progress.

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

After each task, briefly summarize: what was done, test results, deviations. If you are presenting the run as a single wave, keep the `wave-slug` stable across updates.

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
- Show the chosen mode and execution waves before starting
- Keep `wave-slug` and `task-slug` values stable in every progress update
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
