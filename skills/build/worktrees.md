---
name: taku-worktree
description: >
  Use when starting feature work that needs isolation from the current workspace —
  creates isolated git worktrees with auto-detected project setup and baseline test
  verification. Triggers on "create a worktree", "new branch workspace", "isolated
  environment", "start a feature branch", or when build-phase work needs a clean
  sandbox before making changes.
---

# taku-worktree — Git Worktree Isolation

Git worktrees let you work on multiple branches simultaneously without switching. One workspace per feature. No context pollution. No stash juggling. No "wait, I was in the middle of something."

## Why This Matters

Branch switching kills flow. You have uncommitted work, dependencies installed, test state cached. Switching branches means redoing all of that. Worktrees give each feature its own directory, its own node_modules, its own lockfile state. Switch instantly. Never lose context.

## Directory Selection

Follow this priority:

1. **Existing directory:** Check for `.worktrees/` or `worktrees/`. If both exist, `.worktrees/` wins.
2. **CLAUDE.md preference:** `grep -i "worktree" CLAUDE.md` — if specified, use it.
3. **Ask the user:** If neither exists, offer `.worktrees/` (project-local, hidden) or a global location.

## Safety: Verify gitignore

Before creating a project-local worktree, verify the directory is ignored:

```bash
git check-ignore -q .worktrees 2>/dev/null
```

If NOT ignored, fix it immediately:

```bash
echo ".worktrees/" >> .gitignore
git add .gitignore && git commit -m "chore: add .worktrees/ to gitignore"
```

Why: Unignored worktree contents get tracked by git. That pollutes `git status` and risks committing worktree artifacts. Fix it now or regret it later.

## Creation Steps

### 1. Detect project type

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. Create the worktree

```bash
git worktree add ".worktrees/$BRANCH_NAME" -b "$BRANCH_NAME"
cd ".worktrees/$BRANCH_NAME"
```

### 3. Auto-detect and install dependencies

```bash
[ -f package.json ] && npm install
[ -f Cargo.toml ] && cargo build
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f pyproject.toml ] && poetry install
[ -f go.mod ] && go mod download
```

Don't hardcode. Detect from project files. If none match, skip dependency install.

### 4. Run baseline tests

Run the project's test suite. If tests fail before you've changed anything, that's a pre-existing problem. Report it and ask whether to proceed.

```bash
npm test        # or cargo test, pytest, go test ./...
```

If tests pass: report the count. "Worktree ready. 47 tests, 0 failures."

If tests fail: show the output. Ask the user. Don't silently proceed with a broken baseline.

### 5. Report

```
Worktree: .worktrees/<branch-name>
Tests: <N> passing, <M> failing
Ready to implement: <feature-name>
```

## Cleanup

When the feature is done and merged:

```bash
git worktree remove ".worktrees/$BRANCH_NAME"
git branch -d "$BRANCH_NAME"
```

If the branch isn't merged yet and you want to keep it, just remove the worktree:

```bash
git worktree remove ".worktrees/$BRANCH_NAME"
```

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|------------|-----|
| Skip gitignore check | Worktree contents tracked by git | Always `git check-ignore` before creating |
| Proceed with failing tests | Can't tell new bugs from old | Report failures, get permission |
| Hardcode setup commands | Breaks on different projects | Auto-detect from project files |
| Never clean up worktrees | Disk usage grows, stale branches | Remove worktree after merge |

## Completion

Status: DONE when worktree is created, dependencies installed, and baseline tests pass. DONE_WITH_CONCERNS if baseline tests fail but user chose to proceed. BLOCKED if git worktree setup fails.
