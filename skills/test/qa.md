---
name: taku-qa
description: >
  Full QA with fix loop (default) or findings-only report (--report-only). Test
  a web application, find bugs, fix them (or just report them). Three tiers:
  QUICK (5 min), STANDARD (15 min), EXHAUSTIVE (30+ min). Produces health scores,
  before/after evidence, and ship-readiness summary. Enhanced dep: browser tool
  (REQUIRED for web QA). Use when asked to "qa", "test this", "find bugs",
  "test and fix", "just report bugs", "qa report only", or "test but don't fix".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Full QA with Fix Loop

You are a QA engineer AND a bug-fix engineer. Test web applications like a real user — click everything, fill every form, check every state. When you find bugs, fix them in source code with atomic commits, then re-verify. Produce a structured report with health scoring.

## Enhanced Capability Check

**Browser tool is REQUIRED for web QA.**

```bash
# Claude Code
which gstack 2>/dev/null && echo "BROWSER: ready" || echo "BROWSER: not found"
# OpenClaw: browser tool available natively
```

If unavailable: "QA requires the browser tool. Install gstack browse or use OpenClaw with browser support." Stop.

## Step 1: Setup

### 1a. Parse Parameters

| Parameter | Default | Override |
|-----------|---------|----------|
| Target URL | auto-detect | `https://myapp.com`, `localhost:3000` |
| Tier | Standard | `--quick`, `--exhaustive` |
| Scope | Full app | `Focus on billing page` |
| Auth | None | `Sign in as user@example.com` |

### 1b. Tier Selection

- **QUICK (5 min):** Homepage + top 5 navigation targets. Fix critical + high severity only. Smoke test.
- **STANDARD (15 min):** Systematic exploration of all reachable pages. Fix critical + high + medium.
- **EXHAUSTIVE (30+ min):** Every page, every interaction flow, error paths, edge cases. Fix everything.

### 1c. Check working tree

```bash
git status --porcelain
```

If dirty: offer commit, stash, or abort. QA needs a clean tree for atomic commits.

### 1d. Create output directory

```bash
mkdir -p .taku/qa/screenshots
```

### 1e. Diff-aware mode (automatic on feature branches)

If no URL given and on a feature branch:
1. `git diff main...HEAD --name-only` — what changed
2. Map changed files to affected pages/routes
3. Detect running app on common ports (3000, 4000, 8080)
4. Test each affected page

## Step 2: Test (Phases 1-6)

### Phase 1: Navigate

```
browser(action: navigate, url: <target>)
browser(action: screenshot, path: .taku/qa/screenshots/initial.png)
```

Check console for errors. Map navigation structure.

### Phase 2: Authenticate (if needed)

Navigate to login, fill credentials, verify login succeeded.

### Phase 3: Explore

Visit pages systematically. At each page:

1. **Visual scan** — screenshot, check for layout issues
2. **Interactive elements** — click buttons, links, controls
3. **Forms** — fill and submit. Test empty, invalid, edge cases
4. **Navigation** — check all paths in and out
5. **States** — empty, loading, error, overflow
6. **Console** — check for JS errors after every interaction
7. **Responsive** — check mobile viewport if relevant

**Quick mode:** Homepage + top 5 targets only. Check: loads? Errors? Broken links?

### Phase 4: Document Issues

Document each issue **immediately** when found.

For each issue:
- **Severity:** Critical / High / Medium / Low
- **Category:** Visual / Functional / UX / Content / Performance / Accessibility / Console
- **Description:** What's wrong
- **Repro steps:** Exact steps to reproduce
- **Expected vs Actual:** What should happen vs what happens
- **Screenshot:** Evidence (mandatory)

### Phase 5: Health Score

Compute the health score (0-10) using the rubric below.

### Phase 6: Baseline

Record the baseline health score before any fixes.

## Health Score Rubric

```
10 — No issues found. Ship it.
 8-9 — Minor issues only, all fixed. Ship with confidence.
 6-7 — Some important issues, all fixed. Ship with caveats documented.
 4-5 — Critical issues found, fixed but with risk. DO NOT SHIP without manual review.
 0-3 — Critical issues, some unresolved. DO NOT SHIP.
```

**Scoring method:** Start at 10. Deduct:
- Critical issue: -3
- High issue: -2
- Medium issue: -1
- Low issue: -0.5

Add back 1 point for each issue that was successfully fixed and verified.

## Step 3: Fix Loop (Triage + Fix + Verify)

### 3a. Triage

Sort by severity. Fix based on tier:
- **Quick:** Critical + High only. Defer medium/low.
- **Standard:** Critical + High + Medium. Defer low.
- **Exhaustive:** Everything.

### 3b. For Each Fixable Issue

**Locate source:**
```bash
# Grep for error messages, component names, route definitions
```

**Fix:**
- Read the source, understand context
- Make the **minimal fix**
- Do NOT refactor surrounding code

**Commit:**
```bash
git add <only-changed-files>
git commit -m "fix(qa): ISSUE-NNN — short description"
```

One commit per fix.

**Re-verify:**
```
browser(action: navigate, url: <affected-url>)
browser(action: screenshot, path: .taku/qa/screenshots/issue-NNN-after.png)
```

Check console. Verify the fix works. No regressions.

**Classify:**
- **verified:** fix confirmed, no new errors
- **best-effort:** applied but couldn't fully verify
- **reverted:** regression → `git revert HEAD` → mark as deferred

### 3c. Self-Regulation

Every 5 fixes, evaluate:
- Revert count? → slow down
- Touching unrelated files? → stop and ask
- Hard cap: 50 fixes per session

## Step 4: Final QA

After all fixes:
1. Re-test all affected pages
2. Compute final health score
3. If final score is WORSE than baseline: WARN prominently

## Step 5: Report

Write to `.taku/qa/qa-report-{date}.md`:

- Health score: baseline → final
- Issues found by severity and category
- Fixes applied (verified / best-effort / reverted / deferred)
- Before/after screenshot pairs
- PR summary: "QA found N issues, fixed M, health score X → Y."
- Ship readiness assessment based on final health score

## Important Rules

1. **Repro is everything.** Every issue needs a screenshot.
2. **Verify before documenting.** Retry to confirm it's not a fluke.
3. **Never include credentials.** Write `[REDACTED]` for passwords.
4. **Write incrementally.** Document each issue as you find it.
5. **Test like a user.** Realistic data, complete workflows.
6. **Check console after every interaction.** Silent JS errors are still bugs.
7. **Depth over breadth.** 5-10 well-evidenced issues > 20 vague descriptions.
8. **One commit per fix.** Never bundle.
9. **Revert on regression.** Immediately.
10. **Never refuse to use the browser.** The user asked for QA. Open the browser.

## Report-Only Mode (--report-only)

Use `--report-only` when you want a bug report without code changes. Trigger phrases: "just report bugs", "qa report only", "test but don't fix".

**In report-only mode:**
- Test everything as normal (Steps 1-2)
- Document every issue with severity, repro steps, expected vs actual, screenshot
- Compute health score
- **NEVER fix bugs.** Find and document only. Do not edit source files.
- **NEVER read source code.** Test as a user, not a developer.
- Produce the same structured report

For full test-fix-verify loop, use default mode (no flag).

## Anti-Rationalization

| Excuse | Why it's wrong |
|--------|---------------|
| "I already tested it while building" | You tested the happy path. QA tests the broken paths. |
| "The test suite passes, it's fine" | Tests verify what you thought to test. QA finds what you didn't think of. |
| "This bug is too minor to fix" | Log it. If it's below your tier threshold, defer it — don't ignore it. |
| "I'll just note the bugs and fix them later" | You won't. Fix them now while the context is fresh. |
| "The browser is slow, let me just review the code" | Users don't review code. They click buttons. Test what they experience. |
