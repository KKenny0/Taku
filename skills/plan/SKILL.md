---
name: taku-plan
description: >
  Turn an approved design into an executable implementation plan. Three-step pipeline:
  scope + architecture review → design review (UI only) → plan writing. Auto-detects
  which step to start from based on project state. Invoke when DESIGN.md exists and
  is approved. Triggers on "write the plan", "create implementation plan", "plan this",
  "review this plan", "scope check", "architecture review", "design review",
  "is this plan buildable", "what could go wrong", or after /taku-think completes.
---

# Taku Plan — Review + Plan Pipeline

Three steps, run in sequence. Each gate must pass before the next.

## Step Detection

Check project state to determine where to start:

1. **DESIGN.md exists but not reviewed** → Start from Step 1 (Scope + Architecture Review)
2. **Design reviewed, UI project, design review not done** → Start from Step 2 (Design Review)
3. **All reviews done or not needed** → Go to Step 3 (Write Plan)

Announce which step you're starting from.

---

## Step 1: Scope + Architecture Review

Run when the design hasn't been through strategic and technical review. Catches scope mistakes (cheap to fix now, expensive later) and architecture gaps before code is written.

Full process in `references/plan-review.md`. Load it and follow the instructions.

Quick summary:
- **Scope review:** Challenge premises, identify blind spots, pick a scope mode (EXPANSION / SELECTIVE EXPANSION / HOLD / REDUCTION)
- **Architecture review:** Component boundaries, data flow, edge cases, failure modes, test mapping
- Default: run both in sequence. Auto-detect scope-only or arch-only from phrasing.

If review produces critical gaps → stop and address them with the user before proceeding.

---

## Step 2: Design Review (UI Projects Only)

Only for projects with UI/UX components. Skip entirely for CLI, API, backend, infra.

Scores 9 dimensions (aesthetic, typography, color, spacing, layout, motion, responsiveness, accessibility, content hierarchy). Each gets 0-10, with specific fixes for anything below 8.

Full process in `references/design-review.md`. Load it and follow the instructions.

Skip when: no UI, or project uses an existing design system without customization.

---

## Step 3: Write the Plan

### Prerequisites

- Approved `DESIGN.md` exists
- Reviews completed (scope, architecture, design — as applicable)
- Read the design doc thoroughly before writing a single task

### File Structure Mapping

Before writing tasks, map every file that will be created or modified:

- Design units with clear boundaries and well-defined interfaces
- Prefer smaller, focused files — easier to reason about, more reliable edits
- Files that change together should live together (split by responsibility, not layer)
- In existing codebases, follow established patterns

### Task Granularity

Each step is one action (2-5 minutes):

- "Write the failing test" → step
- "Run it to verify it fails" → step
- "Write minimal implementation" → step
- "Run tests to verify pass" → step
- "Commit" → step

**Why fine-grained steps:** A step that says "Implement the feature and write tests" is unverifiable. Fine-grained steps make each verification explicit: write test → verify it fails → implement → verify it passes → commit.

### Plan Document Header

Every plan starts with:

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** Use /taku-build or /taku-build (sequential) to implement this plan.

**Goal:** [One sentence]

**Architecture:** [2-3 sentences]

**Tech Stack:** [Key technologies]

---
```

### Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

### No Placeholders — Ever

These are plan failures:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — tasks may be read out of order)
- Steps describing what to do without showing how (code blocks required)
- References to types, functions, or methods not defined in any task

### Self-Review Checklist

After writing the complete plan, run this against the design doc:

1. **Spec coverage:** Can you point every requirement to a specific task? List any gaps.
2. **Placeholder scan:** Search for TBD, TODO, "appropriate", "similar to". Fix them.
3. **Type consistency:** Do types, method signatures, and names match across tasks?
4. **TDD ordering:** Does every code step have a preceding test step?
5. **Verification completeness:** Does every task end with a verifiable command and expected output?

Find issues? Fix inline.

### Scope Check

If the design covers multiple independent subsystems, suggest breaking into separate plans. If the plan exceeds 15 tasks, decompose by subsystem or dependency layer.

### Output

Save to `PLAN.md` at project root (or user-specified location).

### Execution Handoff

After saving:

"Plan saved to `PLAN.md`. Two execution options:

1. **Subagent-Driven** (/taku-build) — parallel subagents per task
2. **Sequential** (/taku-build sequential) — execute in this session

Which approach?"

---

## Known Pitfalls

**Skipping reviews because the plan "looks simple."** The design was a 2-page doc for "add notifications." Scope review found it touched 4 subsystems, required a new queue service, and had implications for the mobile app. "Simple" plans hide complexity in assumptions.

*Prevention:* Step detection is state-based, not subjective. If DESIGN.md hasn't been reviewed, run reviews.

**Plan references types or functions not defined in any task.** Task 3 calls `UserStore.findById()` but no task defines `UserStore`.

*Prevention:* Self-review checklist item 3. Read through all tasks sequentially and verify every reference has a definition.

**TDD ordering violated — code step before test step.** The implementer wrote the function, then wrote tests that pass against it — proving nothing.

*Prevention:* Self-review checklist item 4. Every code step must have a preceding test step.

**Plan exceeds 15 tasks / 130+ steps.** Context limits were hit at task 14. The second half produced degraded quality.

*Prevention:* Scope check. Each plan produces working, testable software. Split by subsystem or dependency layer.
