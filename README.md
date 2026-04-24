<p align="center">
  <img src="logo.png" alt="Taku 琢" width="180" />
</p>

<h1 align="center">Taku 琢</h1>

<p align="center"><strong>A disciplined sprint system for AI-assisted software delivery.</strong></p>

<p align="center">
  Think clearly. Plan concretely. Build with TDD. Review the diff. Debug the root cause. Capture what mattered.
</p>

<p align="center">
  Taku helps coding agents ship reliable software through a structured six-phase sprint:
  clarify the problem, produce an executable plan, build with visible structure,
  review the actual diff, verify with evidence, and debug from root cause when checks fail.
</p>

> 如切如磋，如琢如磨
>
> Taku means "to carve and polish jade". The point is not to generate more output. The point is to remove ambiguity until the shape is correct.

## Contents

- [Quick Start](#quick-start)
- [Core Workflow](#core-workflow)
- [What Makes It Different](#what-makes-it-different)
- [Before / After](#before--after)
- [Installation](#installation)
- [Repository Layout](#repository-layout)
- [Who This Is For](#who-this-is-for)
- [FAQ](#faq)
- [Inspiration](#inspiration)
- [Roadmap Direction](#roadmap-direction)

## Quick Start

```text
Request → Think → Plan → Build → Review → Verify → Reflect
                       (pass)         ↑       ↓
                       done           └── Debug ──┘ (fail)
```

Typical flow for a real task:

1. `/taku-think` — clarify the request, frame the problem
2. `/taku-plan` — generate executable tasks with dependency graph
3. `/taku-build` — implement in sequential / parallel / hybrid mode with TDD
4. `/taku-review` — inspect the diff before shipping
5. Verify — run checks; if they fail, `/taku-debug` investigates from root cause
6. `/taku-reflect` — only when something is worth preserving

> **Verify vs Debug:** Verification is a gate in the workflow. `/taku-debug` is the skill used when that gate fails or behavior is already broken. There is no separate `/taku-test`.

### Example Sprint

**Task:** Add retry-safe webhook delivery tracking

- **Think** — clarify idempotency boundary, define failure modes, identify required observability
- **Plan** — add delivery status model, persist attempt metadata, define retry policy, add integration tests
- **Build** — implement storage changes, add retry coordinator, add tests
- **Review** — inspect diff for state transition bugs, confirm no scope drift
- **Verify / Debug** — run tests, reproduce failed paths, confirm root cause before patching

## Core Workflow

The repository is organized around six focused phase skills:

| Phase | Command | Use it when | Main output |
|-------|---------|-------------|-------------|
| Think | `/taku-think` | Request is ambiguous or still idea-stage | Clarified scope, design decisions in `DESIGN.md` |
| Plan | `/taku-plan` | Design is approved, need executable tasks | Spec-based `PLAN.md` with dependency graph |
| Build | `/taku-build` | `PLAN.md` is ready | Implemented code with tests, build progress visibility |
| Review | `/taku-review` | Before shipping | Diff review findings, scope drift check |
| Debug | `/taku-debug` | Checks fail or behavior breaks | Root cause investigation, targeted fix |
| Reflect | `/taku-reflect` | A pattern or lesson is worth preserving | Approved learnings, optional retro report |

The skills are designed to hand work off from one phase to the next. `/taku-think` auto-selects Quick, Design, or Explore mode based on task complexity — you get rigor when it matters, less ceremony when it does not.

## What Makes It Different

### 1. It scales the process to the task

`/taku-think` is not blindly heavyweight. It auto-selects:

- **Quick** for clearly bounded changes
- **Design** for normal feature work
- **Explore** for idea-stage requests that are still too vague to implement

### 2. It treats planning as executable work

`/taku-plan` does more than write bullets. It forces:

- scope review before implementation
- architecture review before code spreads across modules
- UI design review only when there is actually UI
- spec-based tasks with dependency annotations and TDD anchors
- execution hints that advise the build agent on mode and wave grouping

Review artifacts (scope assessment, architecture diagrams, edge cases) go to `DESIGN.md`. `PLAN.md` stays pure execution content — goal, tasks, dependency graph. The build agent reads the plan's contract header and knows exactly what's required vs. optional.

### 3. It makes build execution explicit

`/taku-build` owns the execution decision and continues directly into BUILD once the plan is self-reviewed and still within the approved scope.

It supports three execution shapes:

- **Sequential** when the task is small or tightly coupled
- **Parallel** when tasks are independent and subagents can safely split the work
- **Hybrid** when execution is best expressed as waves: waves run in order, while tasks inside a wave may run in parallel

### 4. It does not confuse "review" with "looks fine to me"

`/taku-review` reads the diff, checks base branch drift, and looks for failure patterns that tests often miss:

- unsafe query construction
- trust-boundary mistakes around LLM usage
- conditional side effects
- missing error handling
- scope drift between intent and delivery

### 5. It keeps verification and debugging distinct

The fifth phase is a verification gate, not a second planning phase and not a vague "do some QA" instruction. The orchestrator runs the required checks. `/taku-debug` exists for the branch where those checks fail or behavior is already broken.

Taku's debug flow is evidence-first:

1. investigate
2. pattern-match
3. rank hypotheses
4. verify the actual root cause

That prevents the most common AI bugfix loop: changing things until the output changes and calling it solved.

### 6. It keeps long-term memory under control

`/taku-reflect` is manual by design. Taku does not continuously write "learnings" just because something happened once.

On the first successful reflect run for a project, it can also suggest bootstrapping a short learnings-discovery note into `AGENTS.md` and/or `CLAUDE.md` so non-Taku sessions know to consult `.taku/learnings/...` before non-trivial work.

Only user-approved patterns, pitfalls, preferences, and discoveries get preserved.

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

## Installation

### Claude Code

```bash
git clone https://github.com/KKenny0/Taku.git ~/.claude/skills/taku
```

Expose each phase as its own slash command:

```bash
# macOS / Linux
for phase in think plan build review debug reflect; do
  ln -s ~/.claude/skills/taku/skills/$phase ~/.claude/skills/taku-$phase
done
```

```powershell
# Windows PowerShell
foreach ($phase in @("think","plan","build","review","debug","reflect")) {
  New-Item -ItemType Junction `
    -Path "$env:USERPROFILE\.claude\skills\taku-$phase" `
    -Target "$env:USERPROFILE\.claude\skills\taku\skills\$phase"
}
```

After linking, your skills directory should expose commands like `taku-think`, `taku-plan`, `taku-build`, `taku-review`, `taku-debug`, `taku-reflect`.

#### First Run

After installation, start with:

- `/taku-think` for an ambiguous request
- `/taku-plan` for a scoped feature that needs executable tasks
- `/taku-build` only when `PLAN.md` is ready

### Migration Note

Older repo layouts used `skills/test/`, which caused two problems:

- the installed slash command could become `/taku-test` even though the actual skill name was `taku-debug`
- the phase semantics blurred verification and debugging into one label

The layout now uses `skills/debug/`. If you installed an older copy, recreate the symlink or junction so it points at `skills/debug/` and exposes `/taku-debug`.

### OpenClaw

Use the same repository as a skill pack, then follow the adapter notes in `platform/openclaw.md` for tool mapping and capability checks.

## Repository Layout

```text
Taku/
├── SKILL.md              # Main orchestrator, version 0.2.0
├── README.md
├── DESIGN.md             # Historical design doc; useful context, not the source of truth for latest messaging
├── logo.png
├── skills/
│   ├── think/
│   ├── plan/
│   ├── build/
│   ├── review/
│   ├── debug/
│   └── reflect/
├── platform/
│   └── openclaw.md
├── templates/
│   ├── design-doc.md
│   ├── plan.md
│   └── retro-report.md
└── promo/
    ├── wechat-carousel.md
    ├── x-thread.md
    └── zhihu-article.md
```

## Platform Status

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | Primary target | Canonical `SKILL.md` format and slash-command workflow |
| OpenClaw | Adapter included | Tool mapping documented in `platform/openclaw.md` |

The method is cross-platform even when the tooling details differ.

## Who This Is For

Taku fits teams or individuals who already know that raw code generation is not the bottleneck.

It is a strong fit when you want:

- more deterministic agent behavior on real engineering tasks
- better control over scope expansion
- explicit TDD and verification gates
- a way to split larger implementations without losing review discipline
- a reusable sprint shape across projects

It is a poor fit if you want "just write something fast and we will sort it out later". Taku is optimized for reliability and leverage, not maximum prompt minimalism.

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

Taku is not a clone of either. It is a narrower, more opinionated synthesis around a six-phase sprint.

## Roadmap Direction

The current repo already has the core sprint spine in place. The obvious next layer is not "more commands", but sharper execution quality:

- tighter handoff contracts between phases
- more explicit BUILD scheduling and wave visibility during long-running execution
- stronger review/test coverage for real-world repo changes
- better packaging and distribution ergonomics
- clearer examples of how to use Taku inside active product work

## License

MIT
