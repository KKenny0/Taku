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

**Why wave-based dispatch:** Full parallelism (all tasks at once) creates massive reconciliation complexity. Pure sequential wastes time on independent tasks. Wave-based dispatch gets the best of both: independent tasks run together, dependent tasks wait for their prerequisites. Each wave is small enough to reconcile cleanly.

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

**Why two stages:** Spec compliance and code quality are independent concerns. Code can be beautiful but wrong (matches nothing in the plan). Code can be correct but fragile (meets spec but has poor structure). Checking both at once conflates the issues. Stage 1 first ensures you built the right thing; Stage 2 ensures you built it well.

### Reconciliation (After Parallel Wave)

1. Check for file conflicts between parallel tasks
2. Run integration tests
3. Verify task boundaries (no task leaked into another's files)

**Why reconciliation matters:** Each parallel task works in isolation. They don't know about each other's changes. Without reconciliation, conflicting imports, duplicate definitions, and crossed dependencies accumulate silently until the final integration — where they're much harder to untangle. Catch conflicts wave-by-wave while the context is fresh.

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

**Why follow each step exactly:** Plans are written to be executable without judgment calls. If a step seems wrong, raise it before deviating — don't silently adapt. Silent deviations mean the plan and reality diverge, making later steps unreliable.

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

## Known Pitfalls

**Parallel subagents modifying the same file.** The plan listed overlapping file paths across two independent tasks. Both subagents wrote to `utils/auth.py` simultaneously. One commit overwrote the other's changes silently.

*What went wrong:* Dependency analysis didn't catch the overlap because both tasks listed the file under "modify" rather than "create."

*Prevention:* During Dependency Analysis, grep all tasks' file lists for duplicates. If any file appears in more than one task, mark those tasks as dependent — they must run sequentially.

**Subagent received partial context.** The plan's Task 4 referenced a `UserStore` interface defined in Task 2, but the subagent context only included Task 4's description. The subagent invented its own `UserStore` with different method signatures.

*What went wrong:* The context format included task description but not the actual code from prior tasks.

*Prevention:* For dependent tasks, include the relevant code from completed tasks in the subagent context. Reference exact file paths and line numbers. The implementer should never guess at interfaces.

**Skipping reconciliation between waves.** Three parallel tasks completed successfully. The next wave started immediately without checking for conflicts. Two tasks had added imports to the same file — the combined result had duplicate imports and a circular dependency.

*What went wrong:* Eager to maintain speed, reconciliation was treated as optional.

*Prevention:* Reconciliation is never optional. After every parallel wave, always check for file conflicts and run integration tests before dispatching the next wave.

**Accepting "DONE_WITH_CONCERNS" without reading concerns.** A subagent reported DONE_WITH_CONCERNS. The coordinator moved on. The concern was a partially implemented error handler that returned `undefined` for three error cases.

*What went wrong:* The status handler treated DONE_WITH_CONCERNS as a soft pass instead of reading and addressing the concerns.

*Prevention:* DONE_WITH_CONCERNS always requires reading the concerns. Address correctness issues immediately. If concerns are non-critical (style, naming), note and proceed. If concerns affect behavior, fix before moving on.

## When to Stop

Stop immediately when: blocker hit, plan has critical gaps, verification fails repeatedly.
Ask for help rather than guessing.

## Completion

After all tasks: run full test suite, route to REVIEW phase (/taku-review) or offer branch completion (/taku-finish).
