---
name: taku
version: 0.2.0
description: >
  Invoke for ANY development task — new feature, bug fix, refactor, API endpoint,
  CLI tool, web app, library, infrastructure, or "build me X". If code will be
  written, tests will run, or a PR will be created, this is the entry point.
  Also triggers on "start a sprint", "plan this feature", "review my code",
  "ship this", "let's think through this idea", or any request that implies
  building software. Do NOT answer directly — route through the sprint pipeline.
---

# Taku — Cross-Platform Development Sprint Framework

A structured sprint pipeline: **Think → Plan → Build → Review → Test → Reflect**.

This file is the **orchestrator**. It doesn't do the work — it determines which skills to invoke, in what order, based on project state and task type. Every sub-skill is a focused, composable file under `skills/`.

---

## 1. Pre-Flight (Run Once Per Session)

### Platform Detection

- `exec`/`read`/`write` available → **OpenClaw**. Read `platform/openclaw.md`.
- `Bash`/`Read`/`Write` available → **Claude Code**. Use tools natively.

### Capability Detection

Check enhanced capabilities. Store as session state. Missing = skip, don't block.

| Capability | Check | Enables |
|------------|-------|---------|
| Image gen | image_generate tool | `/taku-think` design system previews |

### Project State Detection

```bash
[ -f DESIGN.md ] && echo "HAS_DESIGN" || echo "NO_DESIGN"
[ -f PLAN.md ] && echo "HAS_PLAN" || echo "NO_PLAN"
git status --porcelain 2>/dev/null | head -5
git log --oneline -5 2>/dev/null
```

### Depth-Tier Detection

Assess project complexity. This determines skill intensity for the entire sprint.

```bash
FILE_COUNT=$(git ls-files 2>/dev/null | wc -l)
CHANGED_FILES=$(git diff --name-only HEAD~1 2>/dev/null | wc -l)
DIRS_TOUCHED=$(git diff --name-only HEAD~1 2>/dev/null | xargs -I{} dirname {} 2>/dev/null | sort -u | wc -l)
```

| Tier | Criteria | Behavior |
|------|----------|----------|
| **Lightweight** | <50 files OR single-file change (1 dir touched) | Skip plan-review. Use sequential build by default. |
| **Standard** | 50-500 files, moderate scope | Full pipeline. |
| **Deep** | >500 files OR cross-cutting change (3+ dirs touched) | Full pipeline plus: architecture diagram mandatory. |

**Auto-reclassification:** If scope expands mid-sprint (e.g., a "simple bugfix" touches 6 files across 3 modules), escalate one tier. Log: `DEPTH ESCALATION: Lightweight → Standard (reason: scope expanded to N files across M modules)`.

Store as `DEPTH_TIER` session state. All phase routing reads this value.

---

## 2. Task Classification

Before routing, classify the task. This determines which phases to run.

### Task Types

| Type | Trigger Phases | Typical Request |
|------|---------------|-----------------|
| **feature** | THINK → PLAN → BUILD → REVIEW → TEST → REFLECT | "Build me a user dashboard" |
| **bugfix** | TEST (debug) → BUILD → REVIEW | "The login form doesn't work" |
| **refactor** | REVIEW → BUILD → TEST | "Clean up the auth module" |
| **hotfix** | BUILD (skip review for critical) | "Production is down, fix it now" |
| **review** | REVIEW only | "Review my PR" |
| **idea** | THINK only | "I have an idea for..." |

### Classification Rules

- Contains "bug", "broken", "error", "crash", "doesn't work" → **bugfix**
- Contains "urgent", "production down", "emergency", "hotfix" → **hotfix**
- Contains "refactor", "clean up", "reorganize", "improve" → **refactor**
- Contains "review", "PR", "look at this code" → **review**
- Contains "idea", "thinking about", "what if", "should we" → **idea**
- Everything else → **feature**

### Scope Mode

After classifying the task type, declare a scope mode. This governs how aggressively the agent handles scope throughout the sprint.

| Mode | When | Posture |
|------|------|---------|
| **expand** | New feature, greenfield, or the plan feels too small for the problem | Push scope up. Ask "what would make this 10x better?" Suggest adjacent improvements. Must justify each expansion with user value — no gold-plating. |
| **shape** | Adding to existing system, moderate change | Hold the baseline. Surface options one at a time for the user to choose. Every addition needs explicit user approval. |
| **hold** | Bug fix, hotfix, or tight-constraint change | Scope locked. Implement exactly what's needed. Any deviation requires stopping and asking. |
| **cut** | Plan is too large, or depth-tier mismatch | Strip to the minimum that solves the real problem. List every cut with one-line justification. User approves the cuts. |

**Auto-selection:** feature + greenfield → `expand` | feature + existing → `shape` | bugfix/hotfix → `hold` | refactor → `shape` | review → `hold` | idea → `expand`

The user can override the auto-selected mode at any time.

**Scope mode per phase:**
- **THINK:** `expand` = deep exploration, `hold` = skip THINK (bugfix)
- **PLAN:** `expand` = run all reviews, `hold` = skip reviews, write plan directly
- **BUILD:** `expand` = suggest improvements, `hold` = implement exactly, no suggestions
- **REVIEW/TEST:** All modes = full discipline (quality is non-negotiable)
- **REFLECT:** `expand` = deep retro, `hold` = quick learn only

---

## 3. Phase Orchestrations

Each phase has a **specific skill sequence**. Follow the sequence in order. Each skill's output feeds into the next.

### THINK Phase

**Entry:** No DESIGN.md, or user explicitly asks to rethink.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ /taku-think                         │
│ Auto-selects mode:                  │
│   Quick   — simple, clear path      │
│   Design  — feature with choices    │
│   Explore — idea-stage validation   │
│ Output: DESIGN.md or mini design    │
│ Gate: User must explicitly approve  │
└─────────────────────────────────────┘
```

**Rules:**
- If task type is `idea` → use Explore mode, then stop (ask user if they want to continue)
- If task type is `bugfix`/`hotfix`/`refactor` → **skip THINK entirely**
- Hard gate: no code until design is approved
- Design System mode activates only for UI-heavy projects (keyword-triggered)

**→ On completion: route to PLAN phase**

### PLAN Phase

**Entry:** DESIGN.md exists and approved. PLAN.md does not exist.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ /taku-plan                          │
│ Auto-detects step:                  │
│   Step 1: scope + architecture      │
│           review (load reference)   │
│   Step 2: design review (UI only)   │
│           (load reference)          │
│   Step 3: write PLAN.md             │
│ Output: PLAN.md                     │
│ Gate: Self-review checklist        │
└─────────────────────────────────────┘
```

**Rules:**
- `/taku-plan` auto-detects which step to start from based on project state
- Scope + architecture review runs by default (skip only for trivial plans)
- Design review is conditional: skip if project has no UI component
- Self-review checklist is mandatory — if it fails, revise the plan

**→ On completion: route to BUILD phase**

### BUILD Phase

**Entry:** PLAN.md exists and approved. Code not yet implemented.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ /taku-build                         │
│ Pre-check: worktree setup if needed │
│   (load references/worktrees.md)    │
│ Auto-selects execution mode:        │
│   Parallel — 5+ tasks, subagents    │
│   Sequential — 1-3 tasks, in-loop   │
│ TDD enforced (load references/)     │
│ 2-stage review per task             │
│ Dispatches subagents per task       │
└──────────────┬──────────────────────┘
               │ all tasks done
               ▼
         (auto-route to REVIEW)
```

**Rules:**
- `/taku-build` auto-selects mode: parallel (5+ tasks, subagents available) or sequential (1-3 tasks)
- User can override mode at any time
- TDD is enforced inside both modes via `references/tdd.md`
- Worktree isolation is optional — use when feature needs a clean sandbox
- After BUILD completes, **automatically route to REVIEW** — don't wait for user to ask

**→ On completion: auto-route to REVIEW phase**

### REVIEW Phase

**Entry:** Code implemented. Not yet reviewed.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ /taku-review                        │
│ Reads: git diff                     │
│ Auto-fixes: Critical + Important    │
│ Two-pass: Critical → Informational  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Gate: All Critical findings fixed?  │
│ If NO → back to BUILD, fix, re-run │
│ If YES → proceed                    │
└──────────────┬──────────────────────┘
               │
               ▼
         (auto-route to TEST)
```

**Rules:**
- `/taku-review` is always run — it's the minimum
- **Critical findings block progress.** Fix them before moving to TEST.
- Important findings: fix if possible, note if not
- After all reviews pass, **automatically route to TEST**

**→ On completion: auto-route to TEST phase**

### TEST Phase

**Entry:** Code reviewed. Ready for testing.

```
┌─────────────────────────────────────┐
│ Run full test suite                 │
│ Execute project's test command      │
│ Collect pass/fail results           │
└──────────────┬──────────────────────┘
               │
         ┌─────┴──────┐
         │ failures?  │
         └─────┬──────┘
           yes │       │ no
               ▼       ▼
┌──────────────────┐  ┌──────────────────────┐
│ /taku-debug      │  │ All tests pass       │
│ Root cause       │  │ → auto-route REFLECT │
│ investigation    │  └──────────────────────┘
└──────────────────┘
```

**Rules:**
- Run the project's full test suite
- **If tests fail:** invoke `/taku-debug` for systematic root cause investigation
- **Iron Law:** No completion claims without fresh verification evidence. "It should work" is not a completion statement. Run the command, read the output, then claim the result.
- `/taku-debug` is also invoked on-demand at any phase when encountering unexpected behavior

**→ On completion: auto-route to REFLECT phase**

### REFLECT Phase

**Entry:** Code tested and verified.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ /taku-reflect (learn mode)         │
│ Record: patterns, pitfalls,         │
│ preferences from this sprint       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ /taku-reflect --retro (optional)   │
│ (run weekly or per sprint)         │
│ Git log analysis, trends            │
└─────────────────────────────────────┘
```

**Rules:**
- Learn mode runs after every sprint (quick — record key learnings)
- Retro mode runs weekly or on explicit request (heavier — full analysis)
- REFLECT is optional — ask user if they want to run it

---

## 4. Auto-Progression Rules

The sprint **auto-progresses** between phases. The agent should NOT wait for the user to say "now review" or "now test" — it should proactively move to the next phase.

### Auto-Progress Triggers

| From | To | Trigger |
|------|----|---------|
| THINK | PLAN | User approves DESIGN.md |
| PLAN | BUILD | PLAN.md written and self-reviewed |
| BUILD | REVIEW | All tasks in PLAN.md marked DONE |
| REVIEW | TEST | All Critical findings fixed |
| TEST | REFLECT | Test suite passes |

### Pause Points (require user action)

| Phase | Pause Condition | What to Ask |
|-------|----------------|-------------|
| THINK | After brainstorming | "I've drafted DESIGN.md. Review and approve to proceed, or tell me what to change." |
| PLAN | After writing-plans | "PLAN.md is ready. Review the tasks. Type 'go' to start building." |
| REVIEW | Critical findings | "Found {N} critical issues. Fixing now..." (auto-fix, no pause) |

### Exception Handling

| Exception | Action |
|-----------|--------|
| Review finds Critical issues | Fix in BUILD, re-run REVIEW (loop max 3 times, then ask user) |
| Tests fail | Invoke /taku-debug, fix root cause, re-run tests (loop max 3 times, then ask user) |
| Build BLOCKED | Report what's blocking, ask user for context |
| Build NEEDS_CONTEXT | Answer questions, re-dispatch |
| 3 consecutive phase loops | Stop, present status to user, ask for direction |

---

## 5. Sprint Status Reporting

At any point, the agent can report sprint status:

```
SPRINT STATUS
═════════════
Task type: feature
Current phase: BUILD (3/6 tasks complete)
  ✓ think — DESIGN.md approved
  ✓ planning — PLAN.md written (8 tasks)
  → building — in progress (task 4: user authentication)
  ○ review — pending
  ○ test — pending
  ○ reflect — pending

Artifacts:
  DESIGN.md ✓
  PLAN.md ✓
  .taku/explore-2026-03-30.md ✓
```

Use this format when the user asks "where are we?" or "what's the status?"

---

## 6. Full Sprint Flow (feature type, all capabilities)

This is the complete sequence for a greenfield feature with all capabilities available:

```
/taku-think (Quick/Design/Explore)
  → DESIGN.md approved
    → /taku-plan (review + plan writing)
      → PLAN.md
        → /taku-build (parallel or sequential, TDD enforced)
          → /taku-review
            → /taku-debug (if tests fail)
              → /taku-reflect
```

**Shortcuts by task type:**

| Type | Flow |
|------|------|
| bugfix | `/taku-debug` → `/taku-build` → `/taku-review` |
| hotfix | `/taku-build` (skip review for urgency) |
| refactor | `/taku-review` → `/taku-build` → `/taku-review` |
| review | `/taku-review` |
| idea | `/taku-think` (Explore mode) → (ask user if they want to continue) |

---

## 7. Slash Command Quick Reference

| Command | Phase | Description |
|---------|-------|-------------|
| `/taku-think` | THINK | Adaptive Quick/Design/Explore |
| `/taku-plan` | PLAN | Scope review → design review → write plan |
| `/taku-build` | BUILD | Parallel or sequential execution, TDD enforced |
| `/taku-review` | REVIEW | Code review with auto-fix |
| `/taku-debug` | TEST | Root cause investigation |
| `/taku-reflect` | REFLECT | Learn + retro + write skill |

---

## Anti-Rationalization

| Excuse | Why it's wrong |
|--------|---------------|
| "This is too small to need a design" | Small changes break production too. The design can be 3 sentences. |
| "I already know the fix" | You thought you knew the last three fixes too. |
| "Tests will slow me down" | Tests slow you down once. Bugs slow you down forever. |
| "I'll add tests later" | You won't. |
| "This is just a quick hack" | There are no quick hacks in production. |
| "Skip review, it's fine" | The bugs you catch in review are the ones that cost the most in production. |
| "We can skip testing" | You can. You'll regret it. |
| "It should work" | Run the verification. Confidence is not evidence. |
