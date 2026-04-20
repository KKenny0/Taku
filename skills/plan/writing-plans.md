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

**Why fine-grained steps:** A step that says "Implement the feature and write tests" is unverifiable. The implementer can do it in any order, skip verification, or batch unrelated changes. Fine-grained steps make each verification explicit: write test → verify it fails → implement → verify it passes → commit. Each step produces a checkable result.

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

## Known Pitfalls

**Plan references types or functions not defined in any task.** Task 3 calls `UserStore.findById()` but no task defines `UserStore`. The implementer either creates a stub (wrong implementation) or asks for clarification (delay).

*What went wrong:* Tasks were written independently without cross-referencing type signatures and function names. Each task looked complete in isolation but the plan had broken references between tasks.

*Prevention:* Self-review checklist item 3 exists for this: "Do types, method signatures, and names match across tasks?" Read through all tasks sequentially and verify that every function, type, or class referenced in one task is defined in another. `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a build error.

**TDD ordering violated — code step before test step.** Task 5 lists "Step 1: Implement the validation function" then "Step 2: Write tests for validation." The implementer wrote the function, then wrote tests that pass against it — proving nothing about correctness.

*What went wrong:* Plan author treated testing as a post-implementation verification step rather than a design step. Tests written after code are biased toward the implementation.

*Prevention:* Self-review checklist item 4 checks TDD ordering. Every code step must have a preceding test step. The test must fail first (proving it tests the right thing), then the code makes it pass. If you catch yourself writing "implement X, then test X," rewrite as "write failing test for X, then implement X to pass."

**Placeholder code masquerading as detail.** "Add appropriate error handling" — the implementer adds a generic try-catch that swallows errors. "Handle edge cases" — the implementer adds a single `if (input)` check. The plan looked complete but the instructions were too vague to execute correctly.

*What went wrong:* The plan author didn't have a concrete implementation in mind but wrote the step as if they did. "Appropriate" and "handle" are placeholders dressed up as instructions.

*Prevention:* The No Placeholders section explicitly lists these as plan failures. Every step must include actual code blocks. If you can't write the error handling code, the design isn't detailed enough. Go back to the design phase, don't push ambiguity into the plan.

**Plan is too large for one sprint.** 22 tasks, each with 5-7 steps. Total: ~130 steps. The plan looked comprehensive. In practice, context limits were hit at task 14. The second half of the plan was executed with degraded context, producing lower quality code.

*What went wrong:* The scope check (at the end of the plan) should have flagged this earlier. 130 steps is not one plan — it's three plans.

*Prevention:* If the plan exceeds 15 tasks, suggest decomposition. Each plan should produce working, testable software on its own. Split by subsystem or by dependency layer. Three focused plans beat one comprehensive plan that can't be fully loaded into context.

## Execution Handoff

After saving, offer the choice:

"Plan saved to `PLAN.md`. Two execution options:

1. **Subagent-Driven** (/taku-build) — parallel subagents per task, automatic review, faster iteration
2. **Sequential** (/taku-build (sequential mode)) — execute in this session, checkpoints between tasks, you stay in the loop

Which approach?"
