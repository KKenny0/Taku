# OpenClaw Platform Adapter

Tool mapping for running Taku skills on OpenClaw. Claude Code uses Bash/Read/Write/Edit natively and does not need this adapter.

## Core Tool Mapping

| Claude Code Tool | OpenClaw Equivalent | Notes |
|-----------------|--------------------|-------|
| `Bash` | `exec` | `exec(command: "git status")` |
| `Read` | `read` | `read(file: "src/index.ts")` |
| `Write` | `write` | `write(file: "src/index.ts", content: ...)` |
| `Edit` | `edit` | `edit(file: "src/index.ts", oldText: ..., newText: ...)` |
| `WebSearch` | `web_search` | `web_search(query: "...")` |
| `WebFetch` | `web_fetch` | `web_fetch(url: "...")` |
| `Grep` | `exec("grep ...")` | Use exec with grep/find/rg |
| `Glob` | `exec("find ...")` or `exec("glob ...")` | Use exec with find/glob |
| `Task` / `Agent` | `sessions_spawn` | See Subagents section |
| `AskUserQuestion` | Direct reply to user | Ask in natural language, wait for response |

## Subagents

Claude Code dispatches sub-agents with `Task(...)`. OpenClaw uses `sessions_spawn`:

```
sessions_spawn(task: "Implement the login feature per PLAN.md task #3", model: "default")
```

**Model selection** (when multi-model is available):
- Mechanical tasks (rename, config, boilerplate) → cheapest/fast model
- Standard implementation → default model
- Architecture, complex review → most capable model

**Cross-model review:**
```
sessions_spawn(task: "Review this diff for bugs: <diff>", model: "openai/gpt-4o")
```

## Browser

Two options for browser automation on OpenClaw:

### Option 1: Native browser tool (preferred)

```yaml
# Navigate
browser(action: navigate, url: "http://localhost:3000")

# Snapshot (accessibility tree for analysis)
browser(action: snapshot, targetId: "...")

# Screenshot (visual capture)
browser(action: screenshot, path: "/tmp/screenshot.png")

# Interact (click, type, select)
browser(action: act, request: { kind: "click", ref: "e12" })
browser(action: act, request: { kind: "type", ref: "e12", text: "hello" })
browser(action: act, request: { kind: "press", key: "Enter" })
```

### Option 2: gstack browse binary (fallback)

```bash
# If gstack CLI is installed
exec(command: "$B goto http://localhost:3000")
exec(command: "$B snapshot")
exec(command: "$B screenshot /tmp/screenshot.png")
exec(command: "$B click 'Submit'")
```

### Option 3: Claude Code via gstack

```bash
Bash("$B goto http://localhost:3000")
Bash("$B snapshot")
Bash("$B screenshot /tmp/screenshot.png")
Bash("$B click 'Submit'")
```

## Git & GitHub

```bash
# Git operations
exec(command: "git status")
exec(command: "git diff --stat")
exec(command: "git log --oneline -10")
exec(command: "git add -A && git commit -m 'message'")
exec(command: "git push origin feature-branch")

# GitHub CLI
exec(command: "gh pr create --title '...' --body '...'")
exec(command: "gh pr list --state open")
exec(command: "gh pr merge 123 --squash")
exec(command: "gh auth status")
```

## Codex CLI

For cross-model review via OpenAI Codex (if installed):

```bash
# Check availability
exec(command: "which codex")

# Run review
exec(command: "codex exec 'Review this diff for bugs and security issues' -C /path/to/repo -s read-only")
```

## Image Generation

```yaml
# Native tool
image_generate(prompt: "...", size: "1024x1024")

# Via gstack design binary (fallback)
exec(command: "$D variants --brief '...' --count 3 --output-dir /tmp/designs/")
```

## File Conventions

- Sprint artifacts go in `.taku/` (gitignored)
- Design docs at project root: `DESIGN.md`, `PLAN.md`
- Reviews: `.taku/reviews/{type}-{date}.md`
- QA reports: `.taku/qa/{date}.md`
- Retros: `.taku/retros/{date}.md`
- Learnings: `.taku/learnings/{project}.jsonl`

## Setup Check

Run at sprint start to detect capabilities:

```bash
# Browser
exec(command: "which gstack 2>/dev/null && echo 'BROWSER_CLI: ready' || echo 'BROWSER_CLI: none'")

# Codex
exec(command: "which codex 2>/dev/null && echo 'CODEX: ready' || echo 'CODEX: none'")

# GitHub
exec(command: "which gh 2>/dev/null && gh auth status 2>/dev/null && echo 'GH: ready' || echo 'GH: none'")

# Project state
exec(command: "[ -f DESIGN.md ] && echo 'HAS_DESIGN' || echo 'NO_DESIGN'")
exec(command: "[ -f PLAN.md ] && echo 'HAS_PLAN' || echo 'NO_PLAN'")
```
