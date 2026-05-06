<p align="center">
  <img src="logo.png" alt="Taku 琢" width="180" />
</p>

<h1 align="center">Taku 琢</h1>

<p align="center"><strong>Engineering habits for coding agents that keep scope, context, and quality under control.</strong></p>

<p align="center">
  <a href="README.zh.md">中文 README</a>
  ·
  <a href="#quick-install">Quick Install</a>
  ·
  <a href="#core-workflow">Core Workflow</a>
  ·
  <a href="#faq">FAQ</a>
</p>

<p align="center">
  <code>Scope Control</code> &nbsp;
  <code>TDD Build</code> &nbsp;
  <code>Real Diff Review</code> &nbsp;
  <code>Root Cause Debugging</code> &nbsp;
  <code>Context Compact</code>
</p>

<p align="center">
  <img src="assets/taku-six-phase-sprint.png" alt="Taku six-phase sprint: Think, Plan, Build, Review, Debug, and Reflect, with verification as the evidence gate" />
</p>

> 如切如磋，如琢如磨 — Remove ambiguity until the shape is correct.

Taku is a set of workflow skills for Claude Code / coding agents that decompose real engineering tasks into Think → Plan → Build → Review → Verify → Reflect, with `/taku-compact` for long-task context control.

> **Status:** Beta workflow, validated through 9 eval scenarios + interactive dogfood (5 PASS, 3 PARTIAL, 0 FAIL). Taku is opinionated and useful for structured agentic coding, but host capabilities differ. When a platform lacks subagents, Taku keeps the same wave plan and executes those waves sequentially.

## Why Taku

The most common failures when using coding agents:

- **Scope drift** — requirements silently expand during implementation
- **Weak review** — code "looks fine" but trust-boundary bugs and conditional side effects are missed
- **Random patching** — the AI keeps changing code until the output changes, then calls it solved
- **Context loss** — the agent forgets earlier decisions and constraints in long tasks
- **Long-term memory pollution** — the agent writes low-quality "learnings" that add noise to future tasks

Taku solves these with a structured six-phase workflow.

## 30-Second Overview

```text
Request → Think → Plan → Build → Review → Verify → Reflect
                       (pass)         ↑       ↓
                       done           └── Debug ──┘ (fail)
```

Typical flow:

1. `/taku-think` — clarify the request, frame the problem
2. `/taku-plan` — generate executable tasks with dependency graph
3. `/taku-build` — implement in sequential / parallel / hybrid mode with TDD
4. `/taku-review` — inspect the diff before shipping
5. **Verify** — run checks; if they fail, `/taku-debug` investigates from root cause
6. `/taku-reflect` — only when something is worth preserving

> **Verify vs Debug:** Verification is a quality gate. `/taku-debug` is the skill used when that gate fails or behavior is already broken. There is no separate `/taku-test`.
>
> **Context Control:** During long tasks, debugging, review, design discussion, or research, use `/taku-compact` to create a recoverable active-work brief. It is not a seventh phase and does not write long-term memory.

## Quick Install

```bash
# Install all Taku skills globally
npx skills add KKenny0/Taku -g --all

# Update after upstream changes
npx skills update -g
```

After installation, start a new session and type `/taku-` to confirm commands are discovered:

```text
/taku-think  /taku-plan  /taku-build  /taku-review
/taku-debug  /taku-reflect  /taku-compact
```

Recommended: run the validator after install to confirm the skill pack, slash commands, and eval scenarios are available:

```bash
python3 scripts/validate_taku.py --install
```

Add `--strict` to also check that referenced scripts exist and are executable: `python3 scripts/validate_taku.py --strict`

You can also install individual skills: `npx skills add KKenny0/Taku -g --skill taku-think`

## First Run

Start with a small Quick-mode task:

```text
/taku-think Add a --version flag to the existing CLI. It should print the package version and avoid changing other command behavior.
```

Expected shape:

1. `/taku-think` uses Quick mode and states a mini design
2. You approve the mini design
3. `/taku-plan` writes a compact plan or the agent proceeds inline when appropriate
4. `/taku-build` implements with a test anchor, then routes to review and verification

## Core Workflow

| Phase | Command | Use it when | Main output |
|-------|---------|-------------|-------------|
| Think | `/taku-think` | Request is ambiguous or still idea-stage | Clarified scope, design decisions in `DESIGN.md` |
| Plan | `/taku-plan` | Design is approved, need executable tasks | Spec-based `PLAN.md` with dependency graph |
| Build | `/taku-build` | `PLAN.md` is ready | Implemented code with tests, build progress visibility |
| Review | `/taku-review` | Before shipping | Diff review findings, scope drift check |
| Debug | `/taku-debug` | Checks fail or behavior breaks | Root cause investigation, targeted fix |
| Reflect | `/taku-reflect` | A pattern or lesson is worth preserving | Approved learnings, optional retro report |

`/taku-think` auto-selects Quick, Design, or Explore mode based on task complexity — rigor when it matters, less ceremony when it does not.

### Bonus Utility Skills

| Skill | Command | Use it when | Main output |
|-------|---------|-------------|-------------|
| Compact | `/taku-compact` | Context-heavy work, handoff, resume, debugging, review, design, or research | Recoverable compact brief with source tags, unknowns, retrieval hints, and next step |

`/taku-compact` supports `resume`, `handoff`, `debug`, `review`, `design`, and `research` modes. It only preserves active task context; long-term learnings still require user-approved `/taku-reflect`.

## What Makes It Different

### 1. It scales the process to the task

`/taku-think` auto-selects process intensity: Quick (small changes), Design (normal features), Explore (vague ideas) — no one-size-fits-all heavyweight flow.

### 2. It treats planning as executable work

`/taku-plan` does more than write bullets. It forces scope review, architecture review, and UI design review (only when there is actually UI), then produces spec-based tasks with dependency annotations, TDD anchors, and execution hints.

Review artifacts go to `DESIGN.md`. `PLAN.md` stays pure execution — goal, tasks, dependency graph. The build agent reads the plan's contract header and knows exactly what's required vs. optional.

### 3. It makes build execution explicit

`/taku-build` owns execution decisions with three shapes: Sequential (small or tightly coupled), Parallel (independent tasks, host supports subagents), and Hybrid (wave-organized). It proceeds directly to BUILD once the plan is self-reviewed and within approved scope.

### 4. It does not confuse "review" with "looks fine to me"

`/taku-review` reads the actual diff, checks base branch drift, and looks for failure patterns tests often miss: unsafe query construction, trust-boundary mistakes, conditional side effects, missing error handling, and scope drift.

### 5. It keeps verification and debugging distinct

The fifth phase is a verification gate, not a second planning phase. When checks fail, `/taku-debug` is evidence-first: investigate → pattern-match → rank hypotheses → verify root cause. This prevents the common AI bugfix loop of changing code until the output changes.

### 6. It keeps long-term memory under control

`/taku-reflect` is manual by design. Only user-approved patterns, pitfalls, preferences, and discoveries get preserved. `.taku/learnings/*.jsonl` is canonical, managed by `skills/reflect/scripts/learnings.py`.

### 7. It keeps active context recoverable

`/taku-compact` scans durable sources, git evidence, and session state before producing a structured brief. The brief marks whether claims came from project files, git, the current conversation, or inference. When evidence is missing, it must say `unknown`.

### Common Failure Patterns

| Common failure | How Taku handles it |
|---|---|
| Scope silently drifts during implementation | `/taku-plan` forces scope review; build checks drift |
| Review is superficial, hidden bugs are missed | `/taku-review` reads real diffs, checks trust-boundary and risk patterns |
| AI patches randomly without finding root cause | `/taku-debug` ranks hypotheses, verifies root cause before fixing |
| Long-task context bloats or gets lost | `/taku-compact` writes a recoverable active-work brief |
| Agent writes low-quality "learnings" continuously | `/taku-reflect` is manual, only preserves approved content |

## Before / After

**Without Taku:**

- vague prompt → fast code generation
- hidden scope drift
- weak or no review
- broken verification
- random debugging patches

**With Taku:**

- framed request → explicit plan
- visible execution mode with wave progress
- diff review before shipping
- evidence-based verification
- root-cause debugging

## Case Studies

> 9 eval scenarios + interactive dogfood: 5 PASS, 3 PARTIAL, 0 FAIL, 1 SKIP. Three concrete failures Taku's discipline prevented: [View Case Studies](CASE_STUDIES.md)

## When to Use Which Command

| Your situation | Suggested entry point |
|---|---|
| Small change, clear boundary | `/taku-think` Quick mode → `/taku-build` |
| Ambiguous request | `/taku-think` |
| Scoped feature, needs task breakdown | `/taku-plan` |
| `PLAN.md` is ready | `/taku-build` |
| Ready to ship | `/taku-review` |
| Tests fail or behavior is broken | `/taku-debug` |
| Long task, need to hand off or resume | `/taku-compact` |
| Want to capture learnings or do a retro | `/taku-reflect` |

## Installation Details

### Individual Skill Install

```bash
# List available skills
npx skills add KKenny0/Taku -l

# Install specific skill(s)
npx skills add KKenny0/Taku -g --skill taku-think
```

| Parameter | Purpose |
|-----------|---------|
| `-g` | Global install to `~/.claude/skills/` (recommended). Without this, installs to `.claude/skills/` in the current project |
| `--all` | Install all skills in the repository |
| `--skill <name>` | Install a specific skill. Can be repeated |
| `-l` | List available skills without installing |

### Alternative: git clone

```bash
git clone https://github.com/KKenny0/Taku.git ~/.claude/skills/taku
```

Expose each skill as its own slash command:

```bash
# macOS / Linux
for skill in think plan build review debug reflect compact; do
  ln -s ~/.claude/skills/taku/skills/$skill ~/.claude/skills/taku-$skill
done
```

```powershell
# Windows PowerShell
foreach ($skill in @("think","plan","build","review","debug","reflect","compact")) {
  New-Item -ItemType Junction `
    -Path "$env:USERPROFILE\.claude\skills\taku-$skill" `
    -Target "$env:USERPROFILE\.claude\skills\taku\skills\$skill"
}
```

### Migration Note

Older repo layouts used `skills/test/`, which caused the slash command to become `/taku-test`. The layout now uses `skills/debug/`. If you installed an older copy, recreate the symlink or junction pointing to `skills/debug/` to expose `/taku-debug`.

### OpenClaw

Use the same repository as a skill pack, then follow the adapter notes in `platform/openclaw.md` for tool mapping and capability checks.

## Repository Layout

```text
Taku/
├── README.md
├── logo.png
├── evals/
│   ├── README.md
│   └── real_task_scenarios.json
├── scripts/
│   └── validate_taku.py  # Self-checks for this skill pack
├── skills/
│   ├── think/
│   ├── plan/
│   ├── build/
│   ├── review/
│   ├── debug/
│   ├── reflect/
│   └── compact/
├── platform/
│   └── openclaw.md
├── templates/
│   ├── design-doc.md
│   ├── plan.md
│   ├── compact-brief.md
│   └── retro-report.md
```

## Platform Status

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | Primary target | Canonical `SKILL.md` format and slash-command workflow |
| OpenClaw | Adapter included | Tool mapping documented in `platform/openclaw.md` |

The method is cross-platform. Subagent-based parallelism is capability-dependent; without it, `/taku-build` preserves wave visibility and runs wave tasks sequentially.

## Validation

Run the built-in self-check before publishing changes:

```bash
python3 scripts/validate_taku.py
```

The default validator also checks the real-task evaluation suite in `evals/`. Those scenarios are manual regression tests for routing and artifacts, not a synthetic benchmark. Use them when changing phase instructions, install behavior, or README claims.

## Who This Is For

Taku fits teams or individuals who already know that raw code generation is not the bottleneck.

Strong fit when you want:

- more deterministic agent behavior on real engineering tasks
- better control over scope expansion
- explicit TDD and verification gates
- a way to split larger implementations without losing review discipline
- reusable engineering habits across projects
- recoverable context briefs during long tasks, debugging, review, or research

Poor fit if you want "just write something fast and sort it out later". Taku is optimized for reliability and leverage.

## FAQ

**Do I need all six phases every time?**

No. Small, clearly bounded changes may only need `/taku-think` (Quick mode) and `/taku-build`. The workflow scales to the task.

**Can I use Taku for small tasks?**

Yes. `/taku-think` in Quick mode is lightweight. You only enter heavier phases when the task actually warrants them.

**Is this only for Claude Code?**

No. An OpenClaw adapter is included. The method is platform-agnostic; only the tool-mapping layer differs.

**Why is there no `/taku-test`?**

Verification is built into the workflow as a gate. When checks fail, `/taku-debug` handles root cause investigation. A separate test skill would blur the line between "run checks" and "investigate failures".

**Do I need `DESIGN.md` and `PLAN.md` for every change?**

No. They are produced by `/taku-think` and `/taku-plan` when the task warrants them. Quick-mode tasks skip the heavy artifacts.

## Inspiration

Taku stands on two strong foundations:

- **[Superpowers](https://github.com/obra/superpowers)** by [Jesse Vincent](https://github.com/obra): engineering discipline, TDD enforcement, systematic debugging, and evidence-based completion
- **[gstack](https://github.com/garrytan/gstack)** by [Garry Tan](https://github.com/garrytan): sprint thinking, product pressure-testing, QA methodology, and parallel execution patterns

Taku is not a clone of either. It is a narrower, more opinionated synthesis around a six-phase workflow and reusable agent habits.

## Roadmap

- **Phase 1 — Prove It** ✅ Done. 9/10 eval scenarios + interactive dogfood validated core discipline mechanisms.
- **Phase 2 — Harden** ✅ Done. Fixed identified gaps, wrote case studies, validated debug Phase 2-3 interactive depth.
- **Phase 3 — Framework Extraction** 🔜 Next. Extract core discipline patterns from coding skills, define Taku Protocol v0.1.
- **Phase 4 — Domain Expansion** Expand to other domains based on real demand signals.

## License

MIT
