---
name: forge-ship
description: Use when code is reviewed and tested, ready to ship. Runs the full pipeline: sync, test, review, version, changelog, push, PR. Invoke when the user says "ship", "deploy", "push", "create a PR", or indicates code is ready. Proactively invoke when the user asks about deploying or wants to push code.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Full Shipping Pipeline

Run straight through. The user said /forge-ship, which means DO IT. Output the PR URL at the end.

Only stop for:
- On the base branch (abort)
- Merge conflicts that can't be auto-resolved
- Test failures
- Review findings that need user judgment
- MINOR or MAJOR version bump needed

Never stop for:
- Uncommitted changes (always include them)
- Commit message approval (auto-commit)
- CHANGELOG content (auto-generate from diff)

## Step 1: Pre-flight

1. Check current branch. If on the base branch: "Ship from a feature branch." Stop.
2. `git status` and `git diff <base>...HEAD --stat` to understand scope.
3. Check if prior review exists. If not, note that ship will run its own review in Step 4.

## Step 2: Sync with Base

Fetch and merge the base branch so tests run against the merged state:

```bash
git fetch origin <base> && git merge origin/<base> --no-edit
```

If merge conflicts: try auto-resolve for simple cases (VERSION, CHANGELOG ordering). If complex: stop and show conflicts.

## Step 3: Run Tests

Detect and run the project's test suite:

```bash
# Auto-detect and run
npm test 2>/dev/null || pytest 2>/dev/null || cargo test 2>/dev/null || go test ./...
```

Check pass/fail. If failures:
- **In-branch failures** (your changes broke it): stop. Fix before shipping.
- **Pre-existing failures** (not your changes): ask the user whether to fix now, skip, or create an issue.

If all pass: note the counts and continue.

## Step 4: Review Diff

Run `git diff origin/<base>` and review for:
- SQL injection, LLM trust boundary violations
- Conditional side effects, auth gaps
- Resource leaks, race conditions
- Swallowed errors, type safety issues

Auto-fix Critical and Important findings. Batch-ask about Minor findings.

If fixes were applied: commit them, re-run tests, then continue.

## Step 5: Version Bump

1. Read the current `VERSION` file (format: `MAJOR.MINOR.PATCH`)
2. Auto-decide bump level:
   - **PATCH:** < 50 lines changed, no new features
   - **MINOR:** New features, new routes, 50+ lines, or branch starts with `feat/`
   - **MAJOR:** Breaking changes or milestones (ask the user)
3. Write the new version. Bumping a digit resets all to its right.

## Step 6: Update CHANGELOG

1. Read `git log <base>..HEAD --oneline` for all commits
2. Read `git diff <base>...HEAD` for what actually changed
3. Group commits by theme (features, fixes, cleanup, infra)
4. Write CHANGELOG entry with:
   - `## [X.Y.Z] - YYYY-MM-DD`
   - Sections: Added, Changed, Fixed, Removed
   - Lead with what users can now do, not implementation details
5. Cross-check: every commit maps to at least one bullet point

## Step 7: Commit

Group changes into logical, bisectable commits:

1. **Infrastructure first:** migrations, config, routes
2. **Models and services:** with their tests
3. **Controllers and views:** with their tests
4. **VERSION + CHANGELOG:** always the final commit

Each commit must be independently valid. No broken imports, no missing dependencies.

```bash
git commit -m "chore: bump version and changelog (vX.Y.Z)"
```

## Step 8: Verification Gate

Before pushing, re-verify if code changed after Step 3's test run.

- If code changed (review fixes, etc.): re-run the test suite
- If the project has a build step: run it
- "Should work now" is not verification. Run the command.

If tests fail here: stop. Do not push.

## Step 9: Push

```bash
git push -u origin <branch-name>
```

## Step 10: Create PR

### If GitHub:
```bash
gh pr create --base <base> --title "<type>: <summary>" --body "$(cat <<'EOF'
## Summary
<grouped commit summary>

## Test Results
<test output summary>

## Review
<review findings or "No issues found">

## Test Plan
- [ ] <verification steps>

🤖 Generated with Forge
EOF
)"
```

### If GitLab:
```bash
glab mr create -b <base> -t "<type>: <summary>" -d "<body>"
```

### If neither CLI available:
Print the branch name and remote URL. Instruct the user to create the PR manually.

Output the PR/MR URL.

## Pre-Ship Checklist

Before Step 9, verify:
- [ ] All tests pass (fresh run, not cached)
- [ ] Code reviewed (Step 4 findings addressed)
- [ ] VERSION bumped
- [ ] CHANGELOG updated (every commit represented)
- [ ] No TODO/FIXME/HACK in new code
- [ ] No debug logging in new code (`console.log`, `print()`, `debug!`)
- [ ] No broken imports or missing dependencies
- [ ] Commits are bisectable (each independently valid)

## Semantic Versioning Reference

| Change Type | Bump | Examples |
|-------------|------|----------|
| Bug fix, no API change | PATCH | Fix crash, correct calculation |
| New feature, backward compatible | MINOR | New endpoint, new parameter |
| Breaking change | MAJOR | Remove endpoint, change response format |
| Docs, tests, config only | PATCH | Update README, add tests |

When in doubt, PATCH. It's easier to bump MINOR later than to undo a premature MAJOR.

## Important Rules

- Never skip tests. If they fail, stop.
- Never force push. Use regular `git push` only.
- Never push without fresh verification evidence.
- The goal: user says /forge-ship, next thing they see is the PR URL.
