---
name: forge-finish
description: Use when implementation on a branch is done. Verify tests, present 4 options (merge/PR/keep/discard), handle cleanup. Triggers after all tasks in PLAN.md are complete or when the user says "I'm done with this branch".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Branch Completion

Guide completion of development work by verifying tests, presenting clear options, and handling the chosen workflow.

## Step 1: Verify Tests (Hard Gate)

Run the project's test suite before presenting any options:

```bash
npm test 2>/dev/null || pytest 2>/dev/null || cargo test 2>/dev/null || go test ./...
```

If tests fail:
```
Tests failing (N failures). Must fix before completing:

<show failures>

Cannot proceed until tests pass.
```

Stop. Do not proceed to Step 2. The hard gate protects against shipping broken code.

If tests pass: note the counts and continue.

## Step 2: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask the user to confirm which branch this split from.

## Step 3: Present Options

Present exactly these 4 options. Keep them concise.

```
Implementation complete. Tests pass. What would you like to do?

1. Merge to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

No explanations, no extra options. Four choices, clear and simple.

## Step 4: Execute Choice

### Option 1: Merge Locally

```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
<test command>  # verify tests on merged result
git branch -d <feature-branch>
```

Then cleanup worktree (Step 5).

### Option 2: Push and Create PR

```bash
git push -u origin <feature-branch>
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Or GitLab equivalent with `glab mr create`.

Keep the branch (don't cleanup worktree yet). The PR is open.

### Option 3: Keep As-Is

Report: "Keeping branch <name>."

Don't cleanup worktree. The user will handle it later.

### Option 4: Discard

Confirm first:
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>

Type 'discard' to confirm.
```

Wait for exact typed confirmation. If confirmed:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then cleanup worktree (Step 5).

## Step 5: Cleanup Worktree

Only for Options 1 and 4:

```bash
git worktree list | grep $(git branch --show-current)
```

If the branch is in a worktree:
```bash
git worktree remove <worktree-path>
```

Option 2 (PR) and Option 3 (keep) preserve the worktree.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Delete Branch |
|--------|-------|------|---------------|---------------|
| 1. Merge locally | Yes | No | No | Yes |
| 2. Create PR | No | Yes | Yes | No |
| 3. Keep as-is | No | No | Yes | No |
| 4. Discard | No | No | No | Yes (force) |

## Common Mistakes

**Skipping test verification:** Merge broken code, create failing PR. Always verify tests first.

**Automatic worktree cleanup for PR:** Remove the worktree when the user still needs it. Only cleanup for Options 1 and 4.

**No confirmation for discard:** Accidentally delete work. Require typed "discard" confirmation.

**Merging without re-testing:** The merge might introduce conflicts that break tests. Always run tests on the merged result.

## Red Flags

Never:
- Proceed with failing tests
- Merge without verifying tests on the result
- Delete work without confirmation
- Force-push without explicit request
