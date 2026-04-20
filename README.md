# Taku 琢

**Structured AI-assisted development — from idea to shipped code.**

Taku combines the best of [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent and [gstack](https://github.com/garrytan/gstack) by Garry Tan into a unified skill pack for Claude Code and OpenClaw.

## Why Taku

> 如切如磋，如琢如磨 — 《诗经·卫风·淇奥》

Taku (琢) means to carve jade — to reveal the shape that was always inside the stone. Software development works the same way: you don't forge code by adding material, you carve it by removing what doesn't belong.

| Stage | Chinese | Pipeline Phase | What Happens |
|-------|---------|----------------|-------------|
| 切 | Cut | Think | Cut through ambiguity — force clarity before code |
| 磋 | Grind | Plan | Grind the problem into concrete, executable tasks |
| 琢 | Carve | Build → Review → Test | Carve the solution, then inspect and verify |
| 磨 | Polish | Ship → Reflect | Polish to production grade, learn from the process |

## The Sprint Pipeline

A structured 7-phase pipeline that turns ideas into shipped, tested, reviewed code:

```
Think → Plan → Build → Review → Test → Ship → Reflect
```

Each phase has dedicated skills with iron-clad rules, anti-rationalization guards, and evidence-based gates. The agent can't skip steps, can't fake completions, and can't rationalize shortcuts.

### Phase Skills

| Phase | Skill | What Happens |
|-------|-------|-------------|
| **Think** | `/taku-office-hours` | 6 forcing questions reframe your product before you write code |
| | `/taku-brainstorm` | Socratic design refinement — no code until you approve the design |
| | `/taku-design` | Build a complete design system from scratch |
| **Plan** | `/taku-ceo-review` | Rethink the problem, find the 10-star product |
| | `/taku-eng-review` | Lock in architecture, data flow, edge cases |
| | `/taku-design-review` | Rate design dimensions 0–10, fix what's weak |
| | `/taku-plan` | Bite-sized tasks with exact file paths, TDD steps |
| **Build** | `/taku-build` | Subagent-driven development with parallel sprint support |
| | `/taku-exec` | Sequential plan execution with checkpoints |
| | `/taku-tdd` | RED-GREEN-REFACTOR enforcement |
| **Review** | `/taku-review` | Pattern-based code review with auto-fix |
| | `/taku-cross-review` | Second opinion from a different AI model |
| | `/taku-visual-review` | Before/after visual QA with screenshots |
| **Test** | `/taku-qa` | Test → find bugs → fix → verify with health scoring |
| | `/taku-cso` | 14-phase security audit with OWASP + STRIDE |
| | `/taku-debug` | 4-phase root cause investigation |
| | `/taku-verify` | Evidence-based completion — no "should work" without proof |
| **Ship** | `/taku-ship` | Full pipeline: test → review → version → changelog → push → PR |
| | `/taku-deploy` | Merge → CI → deploy → verify production health |
| **Reflect** | `/taku-retro` | Weekly retrospective with trend tracking |
| | `/taku-learn` | Persistent learning across sessions |

## Philosophy

- **No code without design.** The agent must understand WHY before HOW.
- **No production code without a failing test.** TDD is not optional.
- **No fixes without root cause.** Three failed fixes → stop and question architecture.
- **No completion claims without evidence.** "It should work" is not a completion statement.
- **No rationalization.** Red flag tables and iron laws catch every shortcut excuse.

## Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | Primary | Canonical format. Install via plugin marketplace or manual. |
| OpenClaw | Supported | Adapter layer translates tool calls. Install as skill pack. |

## Installation

### Claude Code

```bash
# Via plugin marketplace (coming soon)
/plugin install taku

# Manual
git clone https://github.com/KKenny0/Taku.git ~/.claude/skills/taku
```

### OpenClaw

```bash
# Coming soon via ClawhHub
openclaw skills install taku
```

## Credits

Taku is built on the shoulders of two exceptional projects:

- **[Superpowers](https://github.com/obra/superpowers)** by [Jesse Vincent](https://github.com/obra) — A complete software development workflow for coding agents. The discipline-first approach (TDD enforcement, systematic debugging, evidence-based completion) forms Taku's backbone.

- **[gstack](https://github.com/garrytan/gstack)** by [Garry Tan](https://github.com/garrytan) — A sprint process with 25+ skills covering everything from YC office hours to browser QA to security audits. The product thinking, QA methodology, and parallel sprint architecture are deeply influential.

Both projects are MIT licensed. Taku inherits that license.

## License

MIT
