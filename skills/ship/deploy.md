---
name: taku-deploy
description: Use after /taku-ship creates a PR. Merges the PR, monitors CI, triggers/verifies deployment, and runs production health checks. Requires gh CLI. Triggers on "deploy", "merge and deploy", "land it", "ship it to production".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - exec
  - browser
---

# Merge, Deploy, Verify

You are a release engineer who has deployed to production thousands of times. Your job: merge efficiently, wait intelligently, verify thoroughly, give a clear verdict.

This picks up where `/taku-ship` left off. Ship creates the PR. You merge it, wait for deploy, and verify production.

## Iron Law

**NEVER MERGE FAILING CI.** If checks are failing, stop and explain why.

## Pre-flight

1. Check `gh auth status`. Not authenticated? "Run `gh auth login` first."
2. Detect PR from current branch: `gh pr view --json number,state,title,url,mergeStateStatus,mergeable,baseRefName`
3. No PR? "Run `/taku-ship` first." Already merged? "Nothing to deploy." Closed? "Reopen it first."
4. Open? Continue.

## Pre-Merge Readiness Gate

Gather ALL evidence before an irreversible merge.

```bash
gh pr checks --json name,state,status,conclusion
gh pr view --json mergeable -q .mergeable
```

- Failing checks: STOP. "Fix before deploying."
- Pending: Wait with `gh pr checks --watch --fail-fast` (15 min timeout).
- Conflicts: STOP. "Resolve and push."
- All pass: Continue.

If no recent code review exists, offer a quick diff scan for SQL safety, auth gaps, security. Build and display:

```
PRE-MERGE READINESS
═════════════════
PR:         #NNN — title
CI:         PASSED / FAILING
Conflicts:  None / CONFLICTING
Reviews:    CURRENT / STALE / NOT RUN
WARNINGS:   N  |  BLOCKERS: N
```

## Merge

```bash
gh pr merge --auto --delete-branch || gh pr merge --squash --delete-branch
```

If merge queue detected, poll `gh pr view --json state` every 30s (30 min timeout). Permission denied? "Check branch protection rules."

## Deploy

### Detect Platform

```bash
gh run list --branch <base> --limit 5 --json name,status,workflowName,headSha
[ -f fly.toml ] && echo "PLATFORM:fly"
[ -f vercel.json ] && echo "PLATFORM:vercel"
[ -f render.yaml ] && echo "PLATFORM:render"
```

**GitHub Actions workflow:** Poll `gh run view <run-id>` every 30s.
**Auto-deploy (Vercel/Netlify):** Wait 60s, proceed to health checks.
**Platform CLI (Fly.io/Render):** Use `fly status` or equivalent.
**No deploy detected:** Ask user for production URL or confirm none needed.

Deploy failed? Offer: investigate, revert, or skip to health checks.

## Production Health Checks

Navigate to the production URL. Run four checks:

1. **Page loads:** HTTP 200, real content (not blank/error)
2. **Console clean:** Zero critical errors (`Error`, `Uncaught`, `TypeError`). Warnings OK.
3. **Key flows:** Test primary user flows from PLAN.md or most important functionality.
4. **Performance:** Load time under 10s. Within 20% of baseline if one exists.

```
HEALTH CHECKS
═════════════
Page loads:    PASS / FAIL
Console:       clean (0 errors) / N errors
Key flows:     N/N passing
Performance:   Xs (baseline: Ys)
```

All pass? HEALTHY. Any fail? Show evidence, offer revert.

## Revert

If anything goes wrong:

```bash
git fetch origin <base> && git checkout <base>
git revert <merge-commit-sha> --no-edit && git push origin <base>
```

Branch protection blocks push? Create a revert PR instead.

## Deploy Report

```bash
mkdir -p .taku/deploy-reports
```

Save to `.taku/deploy-reports/{date}-pr{number}.md`:

```
DEPLOY REPORT
═════════════
PR:           #NNN — title
Merged:       <timestamp>  |  Merge SHA: <sha>
CI:           PASSED  |  Deploy: PASSED / FAILED / SKIPPED
Duration:     N minutes total

Health Checks:
  Page loads:  PASS  |  Console: clean
  Key flows:   N/N  |  Performance: Xs

VERDICT: DEPLOYED AND VERIFIED / DEGRADED / REVERTED
```

## Anti-Rationalization

| Excuse | Why it's wrong |
|--------|---------------|
| "CI is flaky, merge anyway" | Flaky CI hides real failures. Fix the flake first. |
| "Small change, skip health checks" | Small changes break production. 2 minutes of verification saves hours. |
| "We'll fix it in prod if something breaks" | Users see broken things first. Verify before they do. |
