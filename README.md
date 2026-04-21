<p align="center">
  <img src="logo.svg" alt="Taku 琢" width="180" />
</p>

<h1 align="center">Taku 琢</h1>

<p align="center"><strong>A disciplined sprint system for AI-assisted software delivery.</strong></p>

<p align="center">
  Think clearly. Plan concretely. Build with TDD. Review the diff. Debug the root cause. Capture what mattered.
</p>

Taku is a structured development workflow for coding agents. It turns vague prompts and overconfident code generation into a repeatable sprint:

```text
Think -> Plan -> Build -> Review -> Test -> Reflect
```

This repository is the current `v0.2.0` skill pack. It includes:

- a top-level orchestrator in `SKILL.md`
- six focused phase skills under `skills/`
- an OpenClaw adapter in `platform/openclaw.md`
- reusable sprint templates in `templates/`
- promo assets in `promo/`

Taku is opinionated on purpose. It is built to prevent the failure modes that make AI-generated code expensive:

- coding before the problem is actually understood
- skipping tests because the implementation "looks right"
- treating debugging as random patching
- reviewing too late, or not reviewing the diff at all
- claiming completion without evidence

> 如切如磋，如琢如磨
>
> Taku means "to carve and polish jade". The point is not to generate more output. The point is to remove ambiguity until the shape is correct.

## Why Taku

Most AI coding workflows optimize for speed of output. Taku optimizes for speed to a reliable result.

Instead of one giant prompt, Taku gives the agent a sprint structure:

- **Think** when the request is still ambiguous
- **Plan** before touching code in non-trivial work
- **Build** against explicit tasks, with TDD and optional parallel execution
- **Review** against the actual diff, not hand-wavy intent
- **Test** by investigating root cause instead of thrashing
- **Reflect** only when there is something worth preserving

The result is a workflow that feels closer to a strong engineering lead than a code autocomplete tool.

## Current Shape

The repository has been simplified around six entry skills:

| Phase | Command | Current focus |
|------|------|------|
| Think | `/taku-think` | Adaptive design thinking with Quick, Design, and Explore modes |
| Plan | `/taku-plan` | Scope review, architecture review, UI design review, then executable `PLAN.md` |
| Build | `/taku-build` | Sequential or subagent-based execution with TDD and optional worktree isolation |
| Review | `/taku-review` | Diff-based code review with scope drift checks and fix-first posture |
| Test | `/taku-debug` | 4-phase root cause investigation for bugs, regressions, and failures |
| Reflect | `/taku-reflect` | Learning capture, retro, and skill codification when explicitly invoked |

This is not a bag of unrelated prompts. The skills are designed to hand work off from one phase to the next.

## What Makes It Different

### 1. It scales the process to the task

`/taku-think` is not blindly heavyweight. It auto-selects:

- **Quick** for clearly bounded changes
- **Design** for normal feature work
- **Explore** for idea-stage requests that are still too vague to implement

You get rigor when it matters, and less ceremony when it does not.

### 2. It treats planning as executable work

`/taku-plan` does more than write bullets. It forces:

- scope review before implementation
- architecture review before code spreads across modules
- UI design review only when there is actually UI
- tasks small enough to execute and verify

The goal is not a pretty plan. The goal is a plan the agent can actually land.

### 3. It makes build execution explicit

`/taku-build` supports two real modes:

- **Sequential** when the task is small or tightly coupled
- **Parallel** when tasks are independent and subagents can safely split the work

That means Taku can stay tight for small changes and still accelerate larger sprints.

### 4. It does not confuse "review" with "looks fine to me"

`/taku-review` reads the diff, checks base branch drift, and looks for failure patterns that tests often miss:

- unsafe query construction
- trust-boundary mistakes around LLM usage
- conditional side effects
- missing error handling
- scope drift between intent and delivery

### 5. It forces debugging discipline

The test phase is represented by `/taku-debug`, because in real projects the hard part is rarely "run more tests". The hard part is finding the concrete failure path.

Taku's debug flow is evidence-first:

1. investigate
2. pattern-match
3. rank hypotheses
4. verify the actual root cause

That prevents the most common AI bugfix loop: changing things until the output changes and calling it solved.

### 6. It keeps long-term memory under control

`/taku-reflect` is manual by design. Taku does not continuously write "learnings" just because something happened once.

Only user-approved patterns, pitfalls, preferences, and discoveries get preserved.

## Repository Layout

```text
Taku/
├── SKILL.md              # Main orchestrator, version 0.2.0
├── README.md
├── DESIGN.md             # Historical design doc; useful context, not the source of truth for latest messaging
├── logo.svg
├── skills/
│   ├── think/
│   ├── plan/
│   ├── build/
│   ├── review/
│   ├── test/
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
|------|------|------|
| Claude Code | Primary target | Canonical `SKILL.md` format and slash-command workflow |
| OpenClaw | Adapter included | Tool mapping documented in `platform/openclaw.md` |

The method is cross-platform even when the tooling details differ.

## Installation

### Claude Code

```bash
git clone https://github.com/KKenny0/Taku.git ~/.claude/skills/taku
```

Expose each phase as its own slash command:

```bash
# macOS / Linux
for phase in think plan build review test reflect; do
  ln -s ~/.claude/skills/taku/skills/$phase ~/.claude/skills/taku-$phase
done
```

```powershell
# Windows PowerShell
foreach ($phase in @("think","plan","build","review","test","reflect")) {
  New-Item -ItemType Junction `
    -Path "$env:USERPROFILE\.claude\skills\taku-$phase" `
    -Target "$env:USERPROFILE\.claude\skills\taku\skills\$phase"
}
```

Recommended entry points:

- `/taku-think` when the request is still fuzzy
- `/taku-plan` when design is approved and buildable tasks are needed
- `/taku-build` when `PLAN.md` is ready
- `/taku-review` before shipping
- `/taku-debug` when something breaks
- `/taku-reflect` when a pattern is worth saving

### OpenClaw

Use the same repository as a skill pack, then follow the adapter notes in `platform/openclaw.md` for tool mapping and capability checks.

## Who This Is For

Taku fits teams or individuals who already know that raw code generation is not the bottleneck.

It is a strong fit when you want:

- more deterministic agent behavior on real engineering tasks
- better control over scope expansion
- explicit TDD and verification gates
- a way to split larger implementations without losing review discipline
- a reusable sprint shape across projects

It is a poor fit if you want "just write something fast and we will sort it out later". Taku is optimized for reliability and leverage, not maximum prompt minimalism.

## Inspiration

Taku stands on two strong foundations:

- **[Superpowers](https://github.com/obra/superpowers)** by [Jesse Vincent](https://github.com/obra): engineering discipline, TDD enforcement, systematic debugging, and evidence-based completion
- **[gstack](https://github.com/garrytan/gstack)** by [Garry Tan](https://github.com/garrytan): sprint thinking, product pressure-testing, QA methodology, and parallel execution patterns

Taku is not a clone of either. It is a narrower, more opinionated synthesis around a six-phase sprint.

## Roadmap Direction

The current repo already has the core sprint spine in place. The obvious next layer is not "more commands", but sharper execution quality:

- tighter handoff contracts between phases
- stronger review/test coverage for real-world repo changes
- better packaging and distribution ergonomics
- clearer examples of how to use Taku inside active product work

## License

MIT
