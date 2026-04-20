---
name: taku-ship
description: Use when code is reviewed and tested, ready to ship. Runs the full pipeline: sync, test, review, version, changelog, push, PR, and documentation sync. Invoke when the user says "ship", "deploy", "push", "create a PR", or indicates code is ready. Proactively invoke when the user asks about deploying or wants to push code.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Full Shipping Pipeline

Run straight through. The user said /taku-ship, which means DO IT. Output the PR URL at the end.

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

**Why sync before testing:** Your feature branch tests pass against a snapshot of the base. But the base has moved forward since you branched. If tests fail on the merged result, you want to know now — not after the PR is created and CI fails publicly.

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

**Why auto-decide with conservative default:** Version bumps are a common source of analysis paralysis. The rules are simple enough to automate: when in doubt, PATCH. An undersold MINOR is easy to correct later; an oversold MINOR erodes consumer trust immediately.

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

**Why this ordering:** Each commit must be independently valid. Infrastructure must exist before models can use it. Models must exist before controllers can reference them. VERSION + CHANGELOG last because they describe everything that came before. This ordering means `git bisect` always lands on a compilable, testable state.

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

🤖 Generated with Taku
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
- The goal: user says /taku-ship, next thing they see is the PR URL.

## Known Pitfalls

**Bumping MINOR when it should be PATCH.** A branch with 30 line changes — all bug fixes — was classified as MINOR because the branch started with `feat/`. Downstream consumers saw the version bump and expected new features. The changelog listed only fixes. Trust was eroded.

*What went wrong:* Branch name convention overrode the actual change content. The auto-decide logic used the branch prefix as a signal without cross-checking the diff.

*Prevention:* When in doubt, PATCH. The semver reference explicitly states this. A premature MINOR is harder to undo than a late MINOR. Always verify the bump level against what actually changed, not just the branch name.

**Skipping the verification gate after review fixes.** Tests passed in Step 3. Review in Step 4 found 2 issues and auto-fixed them. Step 8 (Verification Gate) was skipped because "the fixes were minor." The fixes introduced an import cycle that broke the build.

*What went wrong:* Any code change after testing invalidates the test result. "Minor" fixes can introduce major problems — especially import changes, type changes, or dependency adjustments.

*Prevention:* Step 8 is conditional but never optional when code changed. If Step 4 applied fixes, Step 8 MUST re-run tests. No exceptions. The 2 minutes of re-testing saves the embarrassment of a broken build on the PR.

**CHANGELOG missing commits.** The CHANGELOG listed 4 bullet points. The diff contained 9 commits. Two bug fixes and a config change were invisible in the changelog. Users who upgraded missed critical information about the config change.

*What went wrong:* The changelog was written from the diff summary alone, without cross-checking against the commit log.

*Prevention:* Step 6 requires cross-checking: "every commit maps to at least one bullet point." Read `git log <base>..HEAD --oneline` AND the diff. If a commit isn't represented in the changelog, add it. This is the most commonly skipped sub-step and the most important one.

**Committing everything in one monolithic commit.** 15 files changed across models, controllers, views, and tests — all committed together as "feat: add user dashboard." Now a bisect lands on this commit and the developer has to read 15 files to find the regression.

*What went wrong:* Step 7's commit grouping was skipped in favor of speed. One massive commit is easier to create but much harder to debug later.

*Prevention:* Group commits logically: infrastructure first, then models with tests, then controllers with tests, then VERSION + CHANGELOG. Each commit must be independently valid. This takes 5 extra minutes and saves hours during bisect.

## Step 11: Documentation Sync

After PR creation, sync all project docs with what was shipped.

**Diff analysis:** `git diff <base>...HEAD --stat` to understand scope. Discover docs: `find . -maxdepth 2 -name "*.md" | sort`.

**Per-file audit:** Cross-reference each doc against the diff. Auto-update factual corrections (paths, counts, table entries). Ask user for narrative changes, section removals, or large rewrites.

**CHANGELOG polish:** NEVER clobber entries. Polish wording only. Use Edit, never Write, on CHANGELOG.md. Lead with what users can DO.

**Cross-doc consistency:** README features match CLAUDE.md? ARCHITECTURE matches CONTRIBUTING? CHANGELOG version matches VERSION file?

**TODO/FIXME cleanup:** Scan diff for TODO/FIXME/HACK. Check if open items are completed by the diff.

**Commit:** `git commit -m "docs: update project documentation for vX.Y.Z"`. Push.
