---
name: forge
version: 0.1.0
description: >
  Invoke for ANY development task — new feature, bug fix, refactor, API endpoint,
  CLI tool, web app, library, infrastructure, or "build me X". If code will be
  written, tests will run, or a PR will be created, this is the entry point.
  Also triggers on "start a sprint", "plan this feature", "review my code",
  "ship this", "let's think through this idea", or any request that implies
  building software. Do NOT answer directly — route through the sprint pipeline.
---

# Forge — Cross-Platform Development Sprint Framework

A structured sprint pipeline: **Think → Plan → Build → Review → Test → Ship → Reflect**.

This file is the router. It does NOT do the work — it detects where you are in the sprint and loads the right sub-skill. Every sub-skill is a focused, composable file under `skills/`.

## Why a Router?

Without routing, you get ad-hoc answers that skip critical steps. The router ensures
every feature starts with understanding WHY (not just HOW), every change gets reviewed,
and every ship is verified. The cost is a few minutes of structure. The payoff is code
that works, has tests, and doesn't come back to haunt you.

## Pre-Flight Checks

Run these once per session before routing.

### Platform Detection

Determine which platform adapter to use:

```bash
# OpenClaw: has exec, read, write, browser tools
# Claude Code: has Bash, Read, Write, Task tools
# Auto-detect by checking which tool names are available
```

- If `exec`/`read`/`write` are available → **OpenClaw platform**. Read `platform/openclaw.md` for tool mapping.
- If `Bash`/`Read`/`Write` are available → **Claude Code platform**. Use tools natively.

### Enhanced Capability Detection

Check what extra power is available. Missing capabilities don't block the sprint — they just skip optional skills.

```bash
# Browser QA capability
which gstack 2>/dev/null && echo "BROWSER_CLI: ready" || echo "BROWSER_CLI: none"
# Also check for native browser tool (OpenClaw)

# Cross-model review
which codex 2>/dev/null && echo "CODEX: ready" || echo "CODEX: none"

# GitHub integration
which gh 2>/dev/null && gh auth status 2>/dev/null && echo "GH_CLI: ready" || echo "GH_CLI: none"

# Image generation
# Check for image_generate tool availability
```

Store results as session state. When a skill requires a missing capability, skip it and tell the user why.

### Project State Detection

Check the working directory for sprint artifacts:

```bash
# Design exists?
[ -f DESIGN.md ] && echo "HAS_DESIGN" || echo "NO_DESIGN"

# Plan exists?
[ -f PLAN.md ] && echo "HAS_PLAN" || echo "NO_PLAN"

# Uncommitted changes?
git status --porcelain 2>/dev/null | head -5

# Open PRs?
gh pr list --state open --json number,title 2>/dev/null | head -5
```

## Routing Logic

Check project state in this exact order. The first match determines the phase.

```
1. No DESIGN.md exists           → THINK phase
2. DESIGN.md exists, no PLAN.md  → PLAN phase
3. PLAN.md exists, not done      → BUILD phase
4. Code exists, not reviewed     → REVIEW phase
5. Reviewed, not tested          → TEST phase
6. Tested, not shipped           → SHIP phase
7. Shipped                       → REFLECT phase
```

### Phase: THINK (no DESIGN.md)

Goal: Turn a rough idea into a validated design.

Read `skills/think/office-hours.md` for the 6 forcing questions that expose demand reality.
Read `skills/think/brainstorming.md` for Socratic design refinement with a hard no-code-until-approved gate.

**When to use which:**
- Product idea, startup thinking, "is this worth building" → office-hours first
- Feature design, architecture decisions, implementation planning → brainstorming

**Terminal state:** `DESIGN.md` written at project root and approved by user.

### Phase: PLAN (has DESIGN.md, no PLAN.md)

Goal: Transform design into an executable plan with exact file paths, complete code, and TDD steps.

Read `skills/plan/writing-plans.md` for bite-sized task creation.
Read `skills/plan/ceo-review.md` for strategic scope review (optional but recommended).
Read `skills/plan/eng-review.md` for architecture and edge case locking.

**Terminal state:** `PLAN.md` written at project root.

### Phase: BUILD (has PLAN.md, not implemented)

Goal: Implement the plan with TDD discipline.

Read `skills/build/subagent-dev.md` for parallel subagent-per-task execution (default).
Read `skills/build/exec-plans.md` for sequential in-session execution (small projects).
Read `skills/build/tdd.md` for RED-GREEN-REFACTOR enforcement.

**Terminal state:** All tasks implemented, each reviewed.

### Phase: REVIEW (code exists, not reviewed)

Goal: Catch bugs that pass compilation but blow up in production.

Read `skills/review/code-review.md` for pattern-based diff analysis.
Read `skills/review/cross-model.md` for second-opinion review (requires codex CLI or multi-model support).
Read `skills/review/visual-review.md` for before/after visual QA (requires browser tool).

**Terminal state:** All findings addressed.

### Phase: TEST (reviewed, not tested)

Goal: Verify everything works. Find what the reviews missed.

Read `skills/test/qa.md` for browser-based testing (requires browser tool).
Read `skills/test/verify.md` for evidence-based completion gate.
Read `skills/test/debug.md` for root cause investigation when something breaks.

**Terminal state:** QA report generated, all critical findings fixed.

### Phase: SHIP (tested, not shipped)

Goal: Get code to production, verified and documented.

Read `skills/ship/ship.md` for the full shipping pipeline.
Read `skills/ship/finish-branch.md` for branch completion options.
Read `skills/ship/document-release.md` for post-ship doc sync.

**Terminal state:** PR merged or branch shipped, docs updated.

### Phase: REFLECT (shipped)

Goal: Learn from what was built. Get better over time.

Read `skills/reflect/retro.md` for weekly retrospective with trend tracking.
Read `skills/reflect/learn.md` for persistent learning across sessions.

**Terminal state:** Retro report generated, learnings recorded.

## Slash Command Mapping

Every sub-skill supports direct invocation:

| Command | Skill | Phase |
|---------|-------|-------|
| `/forge-office-hours` | Office hours — 6 forcing questions | THINK |
| `/forge-brainstorm` | Socratic design refinement | THINK |
| `/forge-ceo-review` | Strategic scope review | PLAN |
| `/forge-eng-review` | Architecture & edge cases | PLAN |
| `/forge-design-review` | Design dimension scoring | PLAN |
| `/forge-plan` | Write implementation plan | PLAN |
| `/forge-build` | Subagent-per-task execution | BUILD |
| `/forge-exec` | Sequential plan execution | BUILD |
| `/forge-tdd` | RED-GREEN-REFACTOR | BUILD |
| `/forge-review` | Pattern-based code review | REVIEW |
| `/forge-cross-review` | Cross-model second opinion | REVIEW |
| `/forge-visual-review` | Before/after visual QA | REVIEW |
| `/forge-qa` | Browser-based testing | TEST |
| `/forge-verify` | Evidence-based completion gate | TEST |
| `/forge-debug` | Root cause investigation | TEST |
| `/forge-ship` | Full shipping pipeline | SHIP |
| `/forge-finish` | Branch completion | SHIP |
| `/forge-docs` | Post-ship doc sync | SHIP |
| `/forge-retro` | Weekly retrospective | REFLECT |
| `/forge-learn` | Persistent learning | REFLECT |

## Sprint Artifacts

| Phase | File | Purpose |
|-------|------|---------|
| THINK | `DESIGN.md` | Validated design document |
| THINK | `.forge/office-hours-{date}.md` | Raw session notes |
| PLAN | `PLAN.md` | Bite-sized implementation tasks |
| BUILD | Source files | Implemented code + tests |
| REVIEW | `.forge/reviews/code-review-{date}.md` | Review findings |
| TEST | `.forge/qa/{date}.md` | QA report |
| SHIP | GitHub PR | Merged changes |
| REFLECT | `.forge/retros/{date}.md` | Retro report |

## Anti-Rationalization

Common excuses for skipping the pipeline and why they cost more than they save:

| Excuse | Why it's wrong |
|--------|---------------|
| "This is too small to need a design" | Small changes break production too. The design can be 3 sentences, but write it. |
| "I already know the fix" | You thought you knew the last three fixes too. Investigate first. |
| "Tests will slow me down" | Tests slow you down once. Bugs slow you down forever. |
| "I'll add tests later" | You won't. Write them now. |
| "This is just a quick hack" | There are no quick hacks in production. Only permanent liabilities. |

## Completion Status

Report status when a phase completes:
- **DONE** — All steps completed, evidence provided
- **DONE_WITH_CONCERNS** — Completed, issues to know about
- **BLOCKED** — Cannot proceed, state what's blocking
- **NEEDS_CONTEXT** — Missing information, state exactly what
