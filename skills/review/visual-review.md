---
name: taku-visual-review
description: >
  Before/after visual QA. Navigate live sites with the browser tool, take before
  screenshots, identify visual issues, fix in source code, take after screenshots,
  verify each fix. Checks spacing, typography, color, layout, responsive behavior,
  and AI slop patterns. Enhanced dep: browser tool (REQUIRED — skill will not run
  without it). Use when asked to "visual QA", "check the design", "design review",
  or "does this look right".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Before/After Visual QA

You are a senior product designer AND a frontend engineer. Navigate the live site, find visual issues, fix them in source code, and verify each fix with before/after screenshots.

## Enhanced Capability Check

**Browser tool is REQUIRED.** Without it, this skill cannot function.

```bash
# Claude Code: check for browse binary
which gstack 2>/dev/null && echo "BROWSER: ready" || echo "BROWSER: not found"

# OpenClaw: browser tool is available natively
```

If browser is unavailable: "Visual review requires the browser tool. Install gstack browse or use OpenClaw with browser support. Run `/taku-review` for code-only review instead." Stop.

## Step 1: Setup

### 1a. Check for DESIGN.md

Read DESIGN.md or design-system.md if it exists. All visual judgments are calibrated against the project's stated design system. Deviations are higher severity.

### 1b. Check working tree

```bash
git status --porcelain
```

If dirty: "Working tree has uncommitted changes. Visual review needs a clean tree for atomic commits per fix." Offer: commit, stash, or abort.

### 1c. Create output directory

```bash
mkdir -p .taku/visual-review/screenshots
```

### 1d. Navigate to target

Get the URL from user input, or detect the running app on common ports (3000, 4000, 8080).

## Step 2: Baseline Audit

Navigate to the target. Take a full-page screenshot.

### Check Areas

For each page in scope, evaluate:

**Spacing** — Consistent padding/margins? Using a scale (4px/8px base) or arbitrary values? Related items grouped, distinct sections separated?

**Typography** — Font count <= 3? Heading hierarchy has no skipped levels? Line-height 1.5x body? Measure 45-75 chars per line? Body text >= 16px? No blacklisted fonts (Papyrus, Comic Sans, Impact)?

**Color** — Palette coherent (<= 12 non-gray colors)? WCAG AA contrast (4.5:1 body, 3:1 large)? Semantic colors consistent? Dark mode surfaces use elevation, not just inversion?

**Layout** — Grid consistent at all breakpoints? Nothing floating outside the grid? Max content width set? No horizontal scroll on mobile?

**Responsive** — Mobile layout makes design sense (not just stacked desktop)? Touch targets >= 44px? No horizontal scroll on any viewport? Text readable without zooming on mobile?

**AI Slop Detection** — Scan for: purple gradients, 3-column feature grid, icons in colored circles, centered everything, uniform bubbly border-radius, decorative blobs, emoji as design elements, colored left-borders, generic hero copy, cookie-cutter section rhythm.

### Per-Finding Severity

- **High:** Breaks first impression, hurts user trust, or creates confusion
- **Medium:** Reduces polish, felt subconsciously by users
- **Polish:** Separates good from great, nice-to-have

## Step 3: Fix Loop

For each fixable finding, in severity order:

**Why severity order:** High-severity findings affect users' first impression and trust. Fixing a high-severity issue might change the layout enough that a lower-severity issue resolves itself (or changes position). Fix the big problems first, then reassess the small ones.

### 3a. Take Before Screenshot

```
browser(action: navigate, url: <affected-url>)
browser(action: screenshot, path: .taku/visual-review/screenshots/finding-NNN-before.png)
```

### 3b. Fix in Source Code

Find the source file (CSS, component, template). Make the **minimal fix**. Prefer CSS-only changes. Do NOT refactor surrounding code or add features.

### 3c. Atomic Commit

```bash
git add <only-changed-files>
git commit -m "style(visual): FINDING-NNN — short description"
```

One commit per fix. Never bundle.

### 3d. Take After Screenshot

```
browser(action: navigate, url: <affected-url>)
browser(action: screenshot, path: .taku/visual-review/screenshots/finding-NNN-after.png)
```

### 3e. Verify

- Does the fix resolve the finding?
- Any new visual regressions?
- Console clean?

Classify: **verified** (confirmed), **best-effort** (applied but couldn't fully verify), **reverted** (regression detected, `git revert HEAD`).

### 3f. Self-Regulation

Every 5 fixes, evaluate:
- Any reverts? → slow down
- Touching unrelated files? → stop
- Hard cap: 30 fixes per session

## Step 4: Report

Write the report to `.taku/visual-review/visual-review-{date}.md`:

- Total findings by severity
- Fixes applied (verified / best-effort / reverted / deferred)
- Before/after screenshot pairs for each fix
- Deferred findings with reasons
- Summary suitable for PR description

## Important Rules

1. **Think like a designer, not a QA engineer.** You care whether things feel right and look intentional.
2. **Every finding needs a screenshot.** No exceptions.
3. **CSS-first.** Prefer styling changes over structural changes.
4. **Revert on regression.** If a fix makes things worse, revert immediately.
5. **One commit per fix.** Atomic changes, clear history.
6. **Never read source code for the initial audit.** Evaluate the rendered site. Only read source to fix.

## Anti-Rationalization

| Excuse | Why it's wrong |
|--------|---------------|
| "The design is fine, it's functional" | Users judge quality visually in 50ms. Functional but ugly loses trust. |
| "AI slop patterns are just trendy" | They signal "no human designer was involved." Users notice. |
| "I'll fix the layout later" | You won't. Fix it now while the context is fresh. |
| "The screenshot looks fine to me" | Take the screenshot anyway. Your memory of how it looked is unreliable. |

## Known Pitfalls

**Evaluating source code before seeing the rendered page.** The reviewer started by reading CSS and component files, identified "spacing issues" in the code, and made fixes. When the page was actually rendered, the spacing was correct — the CSS values looked wrong in code but produced the right visual result due to flexbox behavior.

*What went wrong:* Important Rule 6 says "Never read source code for the initial audit. Evaluate the rendered site." The reviewer let code analysis bias their visual judgment.

*Prevention:* The initial audit (Step 2) is purely visual. Navigate to the page, take a screenshot, evaluate what you SEE. Only read source code when you need to fix a finding. Your eyes are the testing tool here, not the code.

**Making structural changes when CSS-only fixes would work.** A spacing issue between sections was caused by inconsistent margins. Instead of fixing the margins (CSS-only), the reviewer restructured the component hierarchy (moving elements between parent containers). The restructure fixed the spacing but broke the responsive layout.

*What went wrong:* Important Rule 3 says "CSS-first. Prefer styling changes over structural changes." The reviewer jumped to restructuring because the CSS fix wasn't immediately obvious.

*Prevention:* Always try the CSS fix first. If a margin, padding, or gap adjustment solves the visual issue, stop there. Only restructure when the CSS fix is genuinely impossible (e.g., the DOM order doesn't support the desired visual layout). Structural changes have a much higher regression risk.

**Exceeding the fix cap and burning out.** 45 visual findings were identified. The reviewer fixed all 45 in one session. By fix #30, reverts were happening on 40% of fixes due to regression cascades. The final page looked worse than the initial audit.

*What went wrong:* Self-regulation (Step 3f) says "Hard cap: 30 fixes per session. Every 5 fixes, evaluate." Neither the cap nor the periodic evaluation was respected.

*Prevention:* Stop at 30 fixes. Revert count climbing? Slow down at 5, stop at 10. Better to ship with 15 verified fixes than 45 fixes where half introduced regressions. Deferred findings go into the report for a follow-up session.
