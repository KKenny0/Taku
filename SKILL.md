---
name: forge
version: 0.2.0
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
| Browser QA | `which gstack` OR browser tool | `/forge-qa`, `/forge-visual-review` |
| Cross-model | `which codex` OR multi-model support | `/forge-cross-review` |
| GitHub | `which gh` && `gh auth status` | `/forge-ship`, `/forge-deploy` |
| Image gen | image_generate tool | `/forge-design` previews |

### Project State Detection

```bash
[ -f DESIGN.md ] && echo "HAS_DESIGN" || echo "NO_DESIGN"
[ -f PLAN.md ] && echo "HAS_PLAN" || echo "NO_PLAN"
git status --porcelain 2>/dev/null | head -5
git log --oneline -5 2>/dev/null
```

---

## 2. Task Classification

Before routing, classify the task. This determines which phases to run.

### Task Types

| Type | Trigger Phases | Typical Request |
|------|---------------|-----------------|
| **feature** | THINK → PLAN → BUILD → REVIEW → TEST → SHIP → REFLECT | "Build me a user dashboard" |
| **bugfix** | TEST (debug) → BUILD → REVIEW → SHIP | "The login form doesn't work" |
| **refactor** | REVIEW → BUILD → TEST → SHIP | "Clean up the auth module" |
| **hotfix** | BUILD → SHIP (skip review for critical) | "Production is down, fix it now" |
| **review** | REVIEW only | "Review my PR" |
| **ship** | SHIP only | "Ship this branch" |
| **idea** | THINK only | "I have an idea for..." |

### Classification Rules

- Contains "bug", "broken", "error", "crash", "doesn't work" → **bugfix**
- Contains "urgent", "production down", "emergency", "hotfix" → **hotfix**
- Contains "refactor", "clean up", "reorganize", "improve" → **refactor**
- Contains "review", "PR", "look at this code" → **review**
- Contains "ship", "deploy", "merge", "release" → **ship**
- Contains "idea", "thinking about", "what if", "should we" → **idea**
- Everything else → **feature**

---

## 3. Phase Orchestrations

Each phase has a **specific skill sequence**. Follow the sequence in order. Each skill's output feeds into the next.

### THINK Phase

**Entry:** No DESIGN.md, or user explicitly asks to rethink.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ Step 1: /forge-office-hours         │
│ (if feature type or idea type)      │
│ Output: .forge/office-hours.md      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 2: /forge-brainstorm          │
│ Reads: office-hours output          │
│ Output: DESIGN.md                   │
│ Gate: User must explicitly approve  │
└──────────────┬──────────────────────┘
               │ approved
               ▼
┌─────────────────────────────────────┐
│ Step 3 (optional): /forge-design   │
│ (only for visual/UX-heavy projects)│
│ Reads: DESIGN.md                    │
│ Appends: Design system section     │
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
│ Step 1: /forge-ceo-review          │
│ Reads: DESIGN.md                    │
│ Mode: auto-select scope mode        │
│ Output: design review notes         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 2: /forge-eng-review          │
│ Reads: DESIGN.md + ceo-review notes │
│ Output: architecture notes          │
│ Creates: Mermaid diagrams           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 3: /forge-design-review        │
│ (only if project has UI)           │
│ Reads: DESIGN.md                    │
│ Output: design dimension scores     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 4: /forge-plan                │
│ Reads: DESIGN.md + all reviews      │
│ Output: PLAN.md                     │
│ Gate: Self-review checklist        │
└─────────────────────────────────────┘
```

**Rules:**
- All three reviews feed their output into `/forge-plan` as context
- `/forge-design-review` is conditional: skip if project has no UI component
- `/forge-plan` reads ALL review outputs to produce a comprehensive plan
- Self-review checklist in `/forge-plan` is mandatory — if it fails, revise the plan

**→ On completion: route to BUILD phase**

### BUILD Phase

**Entry:** PLAN.md exists and approved. Code not yet implemented.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ Step 0: /forge-worktree            │
│ (create isolated workspace)        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 1: /forge-build               │
│ Reads: PLAN.md                      │
│ Internally uses: /forge-tdd        │
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
│ Step 1: /forge-exec                │
│ (sequential, user in the loop)     │
│ Reads: PLAN.md                      │
│ Internally uses: /forge-tdd        │
└──────────────┬──────────────────────┘
               │
               ▼
         (auto-route to REVIEW)
```

**Rules:**
- `/forge-build` is the default (parallel, fast)
- Use `/forge-exec` when: project is small (1-3 tasks), user wants to stay in loop, subagents unavailable
- TDD is enforced inside both — `/forge-tdd` is called by the build skill, not separately
- After BUILD completes, **automatically route to REVIEW** — don't wait for user to ask

**→ On completion: auto-route to REVIEW phase**

### REVIEW Phase

**Entry:** Code implemented. Not yet reviewed.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ Step 1: /forge-review              │
│ Reads: git diff                     │
│ Auto-fixes: Critical + Important    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 2: /forge-cross-review        │
│ (if cross-model capability)        │
│ Reads: git diff                     │
│ Cross-model analysis                │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 3: /forge-visual-review       │
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
- `/forge-review` is always run — it's the minimum
- `/forge-cross-review` is optional but recommended (skip if no capability)
- `/forge-visual-review` is conditional: only for projects with UI + browser capability
- **Critical findings block progress.** Fix them before moving to TEST.
- Important findings: fix if possible, note if not
- After all reviews pass, **automatically route to TEST**

**→ On completion: auto-route to TEST phase**

### TEST Phase

**Entry:** Code reviewed. Not yet tested.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ Step 1: /forge-qa                  │
│ (if browser capability)            │
│ Tier: auto-select based on scope   │
│ Fix loop: test → fix → verify      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 2: /forge-cso                 │
│ (security audit)                   │
│ 14-phase scan                       │
│ Gate: 8/10 confidence              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 3: /forge-verify              │
│ Evidence-based completion gate      │
│ Run verification commands           │
│ Show output                         │
└──────────────┬──────────────────────┘
               │
               ▼
         (auto-route to SHIP)
```

**Rules:**
- `/forge-qa` is conditional: requires browser capability. Without it, rely on unit tests + verify
- `/forge-cso` is recommended for all features. For bugfixes, run a lighter scan (phases 1-5, 10 only)
- `/forge-verify` is always run — it's the final evidence gate
- **If QA health score < 4: DO NOT SHIP.** Go back to BUILD to fix critical issues.
- **If verify fails: DO NOT SHIP.** Fix and re-verify.
- `/forge-debug` is invoked on-demand within this phase if something breaks during QA

**→ On completion: auto-route to SHIP phase**

### SHIP Phase

**Entry:** All tests pass. All reviews clear. Ready to ship.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ Step 1: /forge-ship                │
│ Pipeline: sync → test → review →   │
│ version → changelog → push → PR     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 2: /forge-deploy              │
│ (if deploy capability)             │
│ Merge → CI → deploy → health check │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 3: /forge-docs                │
│ Post-ship doc sync                  │
│ Cross-reference diff with docs      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 4: /forge-finish              │
│ 4 options: merge/PR/keep/discard   │
│ Cleanup worktree                    │
└─────────────────────────────────────┘
```

**Rules:**
- `/forge-ship` is always run
- `/forge-deploy` is conditional: requires deploy platform detection
- `/forge-docs` is always run after ship
- `/forge-finish` is always run to clean up

**→ On completion: route to REFLECT phase (or stop if user doesn't want retro)**

### REFLECT Phase

**Entry:** Code shipped.

**Skill Sequence:**

```
┌─────────────────────────────────────┐
│ Step 1: /forge-learn               │
│ Record: patterns, pitfalls,         │
│ preferences from this sprint       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Step 2: /forge-retro               │
│ (run weekly or per sprint)         │
│ Git log analysis, trends            │
└─────────────────────────────────────┘
```

**Rules:**
- `/forge-learn` runs after every sprint (quick — record key learnings)
- `/forge-retro` runs weekly or on explicit request (heavier — full analysis)
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
| TEST | SHIP | Health score ≥ 4 AND verify passes |
| SHIP | REFLECT | Ship/deploy complete |

### Pause Points (require user action)

| Phase | Pause Condition | What to Ask |
|-------|----------------|-------------|
| THINK | After brainstorming | "I've drafted DESIGN.md. Review and approve to proceed, or tell me what to change." |
| PLAN | After writing-plans | "PLAN.md is ready. Review the tasks. Type 'go' to start building." |
| REVIEW | Critical findings | "Found {N} critical issues. Fixing now..." (auto-fix, no pause) |
| SHIP | Before pushing | "About to push and create PR. Confirm?" |

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
Current phase: BUILD (3/7 tasks complete)
  ✓ office-hours — done
  ✓ brainstorming — DESIGN.md approved
  ✓ planning — PLAN.md written (8 tasks)
  → building — in progress (task 4: user authentication)
  ○ review — pending
  ○ test — pending
  ○ ship — pending
  ○ reflect — pending

Artifacts:
  DESIGN.md ✓
  PLAN.md ✓
  .forge/office-hours-2026-03-30.md ✓
```

Use this format when the user asks "where are we?" or "what's the status?"

---

## 6. Full Sprint Flow (feature type, all capabilities)

This is the complete sequence for a greenfield feature with all capabilities available:

```
/forge-office-hours
  → /forge-brainstorm → DESIGN.md approved
    → /forge-ceo-review → /forge-eng-review → /forge-design-review → /forge-plan → PLAN.md
      → /forge-worktree
        → /forge-build (parallel subagents, TDD enforced)
          → /forge-review → /forge-cross-review → /forge-visual-review
            → /forge-qa → /forge-cso → /forge-verify
              → /forge-ship → /forge-deploy → /forge-docs → /forge-finish
                → /forge-learn → /forge-retro
```

**Shortcuts by task type:**

| Type | Flow |
|------|------|
| bugfix | `/forge-debug` → `/forge-build` → `/forge-review` → `/forge-ship` |
| hotfix | `/forge-build` → `/forge-ship` (skip review for urgency) |
| refactor | `/forge-review` → `/forge-build` → `/forge-review` → `/forge-ship` |
| review | `/forge-review` → `/forge-cross-review` (optional) |
| ship | `/forge-ship` → `/forge-docs` → `/forge-finish` |
| idea | `/forge-office-hours` → (ask user if they want to continue) |

---

## 7. Slash Command Quick Reference

| Command | Phase | Skill |
|---------|-------|-------|
| `/forge-office-hours` | THINK | 6 forcing questions |
| `/forge-brainstorm` | THINK | Socratic design |
| `/forge-design` | THINK | Design system creation |
| `/forge-ceo-review` | PLAN | Strategic scope |
| `/forge-eng-review` | PLAN | Architecture |
| `/forge-design-review` | PLAN | Design scoring |
| `/forge-plan` | PLAN | Write plan |
| `/forge-build` | BUILD | Parallel subagents |
| `/forge-exec` | BUILD | Sequential execution |
| `/forge-tdd` | BUILD | RED-GREEN-REFACTOR |
| `/forge-worktree` | BUILD | Workspace isolation |
| `/forge-review` | REVIEW | Code review |
| `/forge-cross-review` | REVIEW | Cross-model opinion |
| `/forge-visual-review` | REVIEW | Visual QA |
| `/forge-qa` | TEST | Browser QA |
| `/forge-qa-report` | TEST | Findings only |
| `/forge-cso` | TEST | Security audit |
| `/forge-debug` | TEST | Root cause |
| `/forge-verify` | TEST | Evidence gate |
| `/forge-ship` | SHIP | Ship pipeline |
| `/forge-deploy` | SHIP | Deploy + verify |
| `/forge-finish` | SHIP | Branch completion |
| `/forge-docs` | SHIP | Doc sync |
| `/forge-retro` | REFLECT | Weekly retro |
| `/forge-learn` | REFLECT | Learning persistence |
| `/forge-write-skill` | META | Create new skill |

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
| "We can ship without QA" | You can. You'll regret it. |
