---
name: taku-build
description: >
  Use when the user has an approved plan and wants to implement it. Supports two
  modes: subagent/parallel (default, dispatches one agent per task) and sequential
  (step-by-step with checkpoints). Auto-selects based on task count and subagent
  availability. Triggers after /taku-plan or when the user says "build this",
  "implement the plan", "start coding".
---

# Build — Parallel or Sequential Execution

Execute PLAN.md tasks. Two modes, auto-selected.

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

**Announce:** "I'm using /taku-build (parallel mode) to execute this plan."

**Why subagents:** Fresh context per task means no pollution from earlier work. The implementer sees exactly what it needs. This preserves your context for coordination and review.

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

Parse each task in PLAN.md to identify dependencies:
1. **Read all tasks** — extract file lists from each task's "Files:" section
2. **Build DAG** — task A depends on task B if A modifies files B creates/depends on
3. **Topological sort** — identify waves of independent tasks
4. **Label each task** — `parallel-ready` or `blocked-by: [task IDs]`

### Model Selection

| Task Type | Model | Why |
|-----------|-------|-----|
| Mechanical (1-2 files, complete spec) | Fast/cheap | Clear instructions, no judgment needed |
| Integration (multi-file, cross-cutting) | Standard | Needs to understand how pieces fit |
| Architecture (design decisions, broad impact) | Powerful | Requires deep reasoning |

Most implementation tasks are mechanical when the plan is well-specified.

### Subagent Context Format

Every subagent receives structured context. Build this from the plan:

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
- Follow /taku-tdd: test first, then implement
- Commit after each passing test
- If blocked, report BLOCKED with reason
- Do NOT modify files outside the list above
```

### Parallel Dispatch

For each wave of independent tasks:
1. **Prepare context** for each task
2. **Dispatch all tasks in the wave** simultaneously
3. **Wait** — results arrive push-based
4. **Process each result**

### Status Handling

- **DONE** → Proceed to spec compliance review
- **DONE_WITH_CONCERNS** → Read concerns, address correctness issues, proceed
- **NEEDS_CONTEXT** → Provide missing information, re-dispatch
- **BLOCKED** → Assess: context problem → provide more; reasoning → better model; task too large → re-plan; plan wrong → escalate to human

**Never** ignore an escalation or retry with no changes.

### Two-Stage Review

After each task:

**Stage 1: Spec Compliance** — Does implementation match the plan? All criteria met? Nothing extra or missing?

**Stage 2: Code Quality** — Well-built? Naming, structure, coverage, edge cases.

Fix issues between stages. Don't proceed to Stage 2 until Stage 1 passes.

### Reconciliation (After Parallel Wave)

1. Check for file conflicts between parallel tasks
2. Run integration tests
3. Verify task boundaries (no task leaked into another's files)

---

## Sequential Mode

Execute PLAN.md task by task with checkpoints.

**Announce:** "I'm using /taku-build (sequential mode) to execute this plan."

**Why sequential:** See each task as it happens — catch issues in real-time, provide guidance, or subagents aren't available. Trades speed for control.

### Step 1: Load and Review

1. Read PLAN.md
2. Review critically — identify questions or concerns
3. Raise concerns with the user before starting
4. No concerns? Create task tracking and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly
3. Follow /taku-tdd for all code steps
4. Run verifications as specified
5. Commit as specified
6. Mark as completed

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
- Follow /taku-tdd for all code changes
- Stop and ask when stuck

## When to Stop

Stop immediately when: blocker hit, plan has critical gaps, verification fails repeatedly.
Ask for help rather than guessing.

## Completion

After all tasks: run full test suite, route to REVIEW phase (/taku-review) or offer branch completion (/taku-finish).
