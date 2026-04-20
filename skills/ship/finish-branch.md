---
name: taku-finish
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

**Why this is a hard gate:** All four completion options (merge, PR, keep, discard) assume the code works. Presenting options before verifying tests invites the user to choose a merge path for broken code. The test gate prevents this by refusing to proceed until the code is verified.

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

## Known Pitfalls

**Merging without testing the merge result.** Tests passed on the feature branch. The merge to main introduced a conflict that was auto-resolved incorrectly. The merged result had broken imports. Nobody noticed because "tests passed on the branch."

*What went wrong:* Step 4 Option 1 says to run tests on the MERGED result, not just the branch. This step was skipped because the branch tests passed.

*Prevention:* Always run tests after merge, before deleting the branch. If tests fail on the merged result, you still have the branch as a reference point. Once the branch is deleted, debugging the merge conflict is much harder.

**Accidental worktree cleanup when PR is still open.** The user chose Option 2 (create PR). The script then cleaned up the worktree because the cleanup logic was triggered by the "done" flag. The PR was open, code was pushed, but the local worktree was gone. The user needed to make a follow-up commit based on reviewer feedback.

*What went wrong:* Quick Reference table says Option 2 (PR) preserves the worktree. The cleanup was triggered incorrectly.

*Prevention:* Worktree cleanup only happens for Options 1 (merge locally) and 4 (discard). Options 2 (PR) and 3 (keep as-is) must NOT trigger cleanup. Double-check the option before running `git worktree remove`.

**Discarding without reading what's being lost.** The user said "discard this." The confirmation showed "This will permanently delete: branch feat/auth, 12 commits." The user typed "discard." What the confirmation didn't show: 3 of those 12 commits contained utility functions that other branches were depending on via cherry-picks. Those commits were now lost.

*What went wrong:* The discard confirmation lists commits but doesn't check if those commits have been referenced or cherry-picked elsewhere.

*Prevention:* Before showing the discard confirmation, check: `git branch --contains <commit>` for each commit. If any commit appears on another branch, note it in the confirmation: "Warning: 3 commits are also present on branch X." The user can then make an informed decision rather than discovering the dependency later.
