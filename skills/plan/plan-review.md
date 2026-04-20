---
name: taku-plan-review
description: >
  Use when a plan needs review before implementation. Two modes: scope review
  (challenging premises, identifying blind spots, deciding scope) and architecture
  review (data flow, edge cases, test coverage, feasibility). Default: run both
  in sequence. Use --scope for strategic review only, --arch for architecture only.
  Triggers on "review this plan", "scope check", "architecture review", "should we
  build this", "is this plan buildable", "what could go wrong", or when the plan
  phase needs validation before implementation.
---

# Plan Review — Scope + Architecture

A two-phase review that catches strategic mistakes before they become expensive implementation mistakes, then validates technical architecture before code is written.

## Why This Matters

Engineers optimize for completeness. Plans accumulate scope like barnacles — every edge case, every "nice to have." The result: a 3-week project that should have been 3 days. And plans look solid until you trace the data flow and realize the auth token doesn't propagate to the background worker.

This review catches both problems. Strategic review challenges premises (changing scope during planning costs nothing; during implementation, everything). Architecture review catches hidden assumptions and race conditions before they become bugs.

## Mode Selection

- **Both** (default): Run scope review first, then architecture review
- **--scope**: Strategic scope review only
- **--arch**: Architecture review only
- Auto-detect: "should we build this" / "is this too much" → scope; "data flow" / "edge cases" / "architecture" → arch

---

## Scope Review Mode

A CEO doesn't care about your class hierarchy. A CEO cares about whether you're building the right thing, for the right people, at the right time.

### The Four Scope Modes

After reviewing the plan, pick ONE mode:

**EXPANSION:** The plan is too small. The problem is bigger than what's proposed.
- When: The plan addresses a symptom, not the root cause. Partial solutions will need to be redone.
- Action: Identify what's missing. Propose the full scope. Estimate the delta.

**SELECTIVE EXPANSION:** The plan is mostly right but misses 1-2 high-leverage additions.
- When: 80% correct, but a small addition would unlock a much larger use case.
- Action: Name the additions. Explain the leverage. Don't gold-plate.

**HOLD SCOPE:** The plan is well-scoped. Ship it.
- When: Solves a clear problem, scope is bounded, expansion adds complexity without proportional value.
- Action: Validate. Note what's explicitly NOT being done and why.

**REDUCTION:** The plan is too big. Cut scope.
- When: Multiple unrelated problems, speculative features, or more than 3 new concepts.
- Action: Identify core value. Cut everything that doesn't serve it. Be ruthless.

### Scope Review Process

**Step 1: Read the plan.** Note stated goal, approach, scope.

**Step 2: Challenge premises.** For each premise:
1. Is this problem real? Who told you? Top-3 pain point or assumption?
2. Is this the right solution? Simpler approaches for 80% of the problem?
3. Who benefits? Name the specific user in context. If you can't, the plan lacks clarity.
4. What's the cost of being wrong? How much work wasted if assumptions fail?

**Step 3: Identify blind spots:**
- Distribution: How do users actually get this?
- Feedback loop: How will you know if it works? First-week signal?
- Dependencies: What external systems/people does this depend on?
- Opportunity cost: What are you NOT building by building this?

**Step 4: Scope decision.** Present:
```
SCOPE REVIEW: [MODE]
Reasoning: [why]
Proposed changes: [specific items]
Risk if ignored: [what happens without this review]
```

**Step 5: Document.** Append `## Plan Review — Scope` section to the design doc.

---

## Architecture Review Mode

An engineering manager doesn't let you write code until the plan survives technical scrutiny.

### Step 1: Architecture Assessment

Read the plan. For each component:
- **Component boundaries:** Clear responsibilities? Each module does one thing?
- **Dependency graph:** What depends on what? Where's the coupling? ASCII diagram.
- **Data flow:** Trace critical path. Input → transform → store → output. Where does data get lost, duplicated, or stale?
- **Scaling:** Bottleneck? Single point of failure? N+1 query?

Produce ASCII architecture diagram if warranted. Trivial change? Say so and skip.

### Step 2: Data Flow Diagram

Draw the data path for the primary user flow. Annotate:
- Where errors can occur
- Where data transforms
- Where state changes (side effects, external calls)
- Where caching happens (and what invalidates it)

Every arrow is a potential failure point. Every junction is a potential race condition.

### Step 3: Edge Case Analysis

| Component | Happy Path | Edge Cases |
|-----------|-----------|------------|
| [component] | [expected] | [what can go wrong] |

Cover: empty input, max input, concurrent access, timeout at each boundary, invalid state.

### Step 4: Test Plan

Map every code path to a test. Mark: **[TESTED]**, **[GAP]**, **[REGRESSION]**.
Quality: ★★★ behavior + edges + errors, ★★ happy path, ★ smoke test.
Mark E2E-worthy flows with `[→E2E]`.

### Step 5: Failure Mode Analysis

For each new code path, one realistic production failure:
```
Path: [function]
Failure: [what breaks]
Test exists? [yes/no]
Error handling? [yes/no]
User sees? [what]
→ CRITICAL GAP: [assessment]
```

Any failure with no test AND no error handling AND silent UX = critical gap.

---

## Completion

Update the plan with findings from both reviews. Append sections to the design doc.

Status: DONE when reviews complete and critical gaps addressed. DONE_WITH_CONCERNS if gaps remain but user chose to proceed. BLOCKED if plan is too vague.
