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
| Browser QA | `which gstack` OR browser tool | `/taku-qa`, `/taku-visual-review` |
| Cross-model | `which codex` OR multi-model support | `/taku-cross-review` |
| Image gen | image_generate tool | `/taku-brainstorm` design system previews |

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
| **Lightweight** | <50 files OR single-file change (1 dir touched) | Skip plan-review, skip security full scan (phases 1-5 only), skip visual-review. Use sequential build by default. |
| **Standard** | 50-500 files, moderate scope | Full pipeline with all optional skills when capabilities allow. |
| **Deep** | >500 files OR cross-cutting change (3+ dirs touched) | Full pipeline plus: architecture diagram mandatory, exhaustive QA tier, comprehensive security audit. |

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
│ Step 1: /taku-office-hours         │
│ (if feature type or idea type)      │
│ Output: .taku/office-hours.md      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 2: /taku-brainstorm          │
│ Reads: office-hours output          │
│ Output: DESIGN.md                   │
│ Gate: User must explicitly approve  │
└──────────────┬──────────────────────┘
               │ approved
               ▼
┌─────────────────────────────────────┐
│ Step 3 (optional): /taku-brainstorm│
│ Design system mode for UX-heavy   │
│ projects. Reads: DESIGN.md        │
│ Appends: Design system section    │
└─────────────────────────────────────┘
```

**Rules:**
- If task type is `idea` → run office-hours only, then stop (ask user if they want to continue)
- If task type is `bugfix`/`hotfix`/`refactor` → **skip THINK entirely**
- office-hours output feeds into brainstorming as context
- brainstorming's HARD GATE means the agent CANNOT proceed to PLAN without user approval

**→ On completion: route to PLAN phase**

### PLAN Phase

**Entry:** DESIGN.md exists and approved. PLAN.md does not exist.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ Step 1: /taku-plan-review         │
│ Reads: DESIGN.md                    │
│ Modes: scope review + architecture  │
│ Output: review notes + diagrams     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 2: /taku-design-review        │
│ (only if project has UI)           │
│ Reads: DESIGN.md                    │
│ Output: design dimension scores     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 3: /taku-plan                │
│ Reads: DESIGN.md + all reviews      │
│ Output: PLAN.md                     │
│ Gate: Self-review checklist        │
└─────────────────────────────────────┘
```

**Rules:**
- `/taku-plan-review` runs both scope and architecture modes by default
- `/taku-design-review` is conditional: skip if project has no UI component
- `/taku-plan` reads ALL review outputs to produce a comprehensive plan
- Self-review checklist in `/taku-plan` is mandatory — if it fails, revise the plan

**→ On completion: route to BUILD phase**

### BUILD Phase

**Entry:** PLAN.md exists and approved. Code not yet implemented.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ Step 0: /taku-worktree            │
│ (create isolated workspace)        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 1: /taku-build               │
│ Reads: PLAN.md                      │
│ Internally uses: /taku-tdd        │
│ Dispatches subagents per task      │
│ 2-stage review per task            │
│ Parallel for independent tasks     │
└──────────────┬──────────────────────┘
               │ all tasks done
               ▼
         (auto-route to REVIEW)
```

**Alternative path:**
```
┌─────────────────────────────────────┐
│ Step 1: /taku-build (sequential)   │
│ (sequential mode, user in the loop) │
│ Reads: PLAN.md                      │
│ Internally uses: /taku-tdd        │
└──────────────┬──────────────────────┘
               │
               ▼
         (auto-route to REVIEW)
```

**Rules:**
- `/taku-build` auto-selects mode: parallel (5+ tasks, subagents available) or sequential (1-3 tasks)
- User can override mode at any time
- TDD is enforced inside both modes — `/taku-tdd` is called by the build skill
- After BUILD completes, **automatically route to REVIEW** — don't wait for user to ask

**→ On completion: auto-route to REVIEW phase**

### REVIEW Phase

**Entry:** Code implemented. Not yet reviewed.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ Step 1: /taku-review              │
│ Reads: git diff                     │
│ Auto-fixes: Critical + Important    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 2: /taku-cross-review        │
│ (if cross-model capability)        │
│ Reads: git diff                     │
│ Cross-model analysis                │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 3: /taku-visual-review       │
│ (if browser capability + has UI)   │
│ Before/after screenshots            │
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
- `/taku-cross-review` is optional but recommended (skip if no capability)
- `/taku-visual-review` is conditional: only for projects with UI + browser capability
- **Critical findings block progress.** Fix them before moving to TEST.
- Important findings: fix if possible, note if not
- After all reviews pass, **automatically route to TEST**

**→ On completion: auto-route to TEST phase**

### TEST Phase

**Entry:** Code reviewed. Not yet tested.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ Step 1: /taku-qa                  │
│ (if browser capability)            │
│ Tier: auto-select based on scope   │
│ Fix loop: test → fix → verify      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 2: /taku-cso                 │
│ (security audit)                   │
│ 14-phase scan                       │
│ Gate: 8/10 confidence              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 3: /taku-verify              │
│ Evidence-based completion gate      │
│ Run verification commands           │
│ Show output                         │
└──────────────┬──────────────────────┘
               │
               ▼
         (auto-route to REFLECT)
```

**Rules:**
- `/taku-qa` is conditional: requires browser capability. Without it, rely on unit tests + verify
- `/taku-cso` is recommended for all features. For bugfixes, run a lighter scan (phases 1-5, 10 only)
- `/taku-verify` is always run — it's the final evidence gate
- **If QA health score < 4: DO NOT PROCEED.** Go back to BUILD to fix critical issues.
- **If verify fails: DO NOT PROCEED.** Fix and re-verify.
- `/taku-debug` is invoked on-demand within this phase if something breaks during QA

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
| TEST | REFLECT | Health score ≥ 4 AND verify passes |

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
| QA health score < 4 | Fix in BUILD, re-run TEST (loop max 3 times, then ask user) |
| Verify fails | Fix in BUILD, re-run verify (loop max 3 times, then ask user) |
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
  ✓ office-hours — done
  ✓ brainstorming — DESIGN.md approved
  ✓ planning — PLAN.md written (8 tasks)
  → building — in progress (task 4: user authentication)
  ○ review — pending
  ○ test — pending
  ○ reflect — pending

Artifacts:
  DESIGN.md ✓
  PLAN.md ✓
  .taku/office-hours-2026-03-30.md ✓
```

Use this format when the user asks "where are we?" or "what's the status?"

---

## 6. Full Sprint Flow (feature type, all capabilities)

This is the complete sequence for a greenfield feature with all capabilities available:

```
/taku-office-hours
  → /taku-brainstorm → DESIGN.md approved
    → /taku-plan-review → /taku-design-review → /taku-plan → PLAN.md
      → /taku-worktree
        → /taku-build (parallel or sequential, TDD enforced)
          → /taku-review → /taku-cross-review → /taku-visual-review
            → /taku-qa → /taku-cso → /taku-verify
                → /taku-reflect
```

**Shortcuts by task type:**

| Type | Flow |
|------|------|
| bugfix | `/taku-debug` → `/taku-build` → `/taku-review` |
| hotfix | `/taku-build` (skip review for urgency) |
| refactor | `/taku-review` → `/taku-build` → `/taku-review` |
| review | `/taku-review` → `/taku-cross-review` (optional) |
| idea | `/taku-office-hours` → (ask user if they want to continue) |

---

## 7. Slash Command Quick Reference

| Command | Phase | Skill |
|---------|-------|-------|
| `/taku-office-hours` | THINK | 6 forcing questions |
| `/taku-brainstorm` | THINK | Socratic design + design system |
| `/taku-plan-review` | PLAN | Scope + architecture review |
| `/taku-design-review` | PLAN | Design scoring |
| `/taku-plan` | PLAN | Write plan |
| `/taku-build` | BUILD | Parallel or sequential execution |
| `/taku-tdd` | BUILD | RED-GREEN-REFACTOR |
| `/taku-worktree` | BUILD | Workspace isolation |
| `/taku-review` | REVIEW | Code review |
| `/taku-cross-review` | REVIEW | Cross-model opinion |
| `/taku-visual-review` | REVIEW | Visual QA |
| `/taku-review-collab` | REVIEW | Dispatch/receive review |
| `/taku-qa` | TEST | Browser QA (with --report-only) |
| `/taku-cso` | TEST | Security audit |
| `/taku-debug` | TEST | Root cause |
| `/taku-verify` | TEST | Evidence gate |
| `/taku-reflect` | REFLECT | Learn + retro |
| `/taku-write-skill` | META | Create new skill |

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
| "We can skip QA" | You can. You'll regret it. |
