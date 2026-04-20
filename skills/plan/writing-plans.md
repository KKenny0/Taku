---
name: taku-plan
description: Use when the user has an approved design and needs to turn it into an executable plan. Triggers after /taku-brainstorm or /taku-plan-review.
---

# Writing Implementation Plans

## Overview

Write implementation plans that a zero-context engineer can execute flawlessly. Every task has exact file paths, complete code, and verification steps. No guesswork, no placeholders, no "you figure it out."

**Announce:** "I'm using /taku-plan to create the implementation plan."

**Why this matters:** A plan with gaps means the implementer either guesses (bugs) or asks questions (delays). Both waste time. A complete plan means the implementer just executes — fast and correct.

## Prerequisites

- Approved `DESIGN.md` exists at project root
- Reviews completed (CEO review, eng review, or equivalent)
- Read the design doc thoroughly before writing a single task

## File Structure Mapping

Before writing tasks, map every file that will be created or modified:

- Design units with clear boundaries and well-defined interfaces
- Prefer smaller, focused files — easier to reason about, more reliable edits
- Files that change together should live together (split by responsibility, not layer)
- In existing codebases, follow established patterns

This structure drives task decomposition. Each task produces self-contained changes.

## Task Granularity

Each step is one action (2-5 minutes):

- "Write the failing test" → step
- "Run it to verify it fails" → step
- "Write minimal implementation" → step
- "Run tests to verify pass" → step
- "Commit" → step

## Plan Document Header

Every plan starts with:

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** Use /taku-build (subagent-driven) or /taku-build (sequential mode) (sequential) to implement this plan.

**Goal:** [One sentence]

**Architecture:** [2-3 sentences]

**Tech Stack:** [Key technologies]

---
```

## Task Structure

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

## No Placeholders — Ever

These are plan failures. Never write them:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — tasks may be read out of order)
- Steps describing what to do without showing how (code blocks required)
- References to types, functions, or methods not defined in any task

## Self-Review Checklist

After writing the complete plan, run this against the design doc:

**1. Spec coverage:** Can you point every requirement to a specific task? List any gaps.

**2. Placeholder scan:** Search for red-flag patterns (TBD, TODO, "appropriate", "similar to"). Fix them.

**3. Type consistency:** Do types, method signatures, and names match across tasks? `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

**4. TDD ordering:** Does every code step have a preceding test step?

**5. Verification completeness:** Does every task end with a verifiable command and expected output?

Find issues? Fix inline. No re-review needed — just fix and move on.

## Scope Check

If the design covers multiple independent subsystems, suggest breaking into separate plans. Each plan should produce working, testable software on its own.

## Output

Save to `PLAN.md` at project root (or user-specified location).

## Execution Handoff

After saving, offer the choice:

"Plan saved to `PLAN.md`. Two execution options:

1. **Subagent-Driven** (/taku-build) — parallel subagents per task, automatic review, faster iteration
2. **Sequential** (/taku-build (sequential mode)) — execute in this session, checkpoints between tasks, you stay in the loop

Which approach?"
