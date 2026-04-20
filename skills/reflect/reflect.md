---
name: taku-reflect
description: >
  Two-mode reflection skill. Learn mode (default): record patterns, pitfalls,
  preferences, and discoveries across sessions. Search and prune the knowledge
  base. Retro mode: weekly engineering retrospective with commit analysis, metrics,
  team breakdowns, and trend tracking. Triggers on "what have we learned", "show
  learnings", "add learning", "weekly retro", "what did we ship", "engineering
  retrospective".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Reflect — Learn + Retrospective

Two modes: quick learning capture (default) and weekly retrospective.

## Mode Selection

- **Learn** (default): "what have we learned", "add learning", "show learnings", "prune learnings"
- **Retro**: "weekly retro", "what did we ship", "retrospective", or `--retro` flag

---

## Learn Mode

Capture what you learn so future sessions don't repeat the same mistakes.

### Storage

Learnings live in `.taku/learnings/{project-slug}.jsonl`. Each line:

```json
{"timestamp":"2026-03-30T19:00:00Z","type":"pattern","context":"What we were doing","learning":"What we learned","action":"What to do differently","confidence":"high"}
```

### Types

- **pattern** — A reusable approach that worked well
- **pitfall** — A mistake to avoid
- **preference** — A user-stated preference or convention
- **discovery** — A non-obvious insight about the codebase

### Confidence

- **high** — Verified by testing or user confirmation
- **medium** — Observed pattern, likely correct
- **low** — Hypothesis, needs validation

### Operations

**ADD:** Gather type, context, learning, action, confidence. Append to JSONL.

**SEARCH:** `grep -i "QUERY" .taku/learnings/{slug}.jsonl`. Present matches grouped by type.

**PRUNE:** Check file existence, contradictions, staleness (30 days). Present each flagged entry for review: Remove / Keep / Update.

**EXPORT:** Convert to markdown. Offer to append to CLAUDE.md or save as separate file.

### Auto-Capture

Other Taku skills log learnings automatically. When /taku-review, /taku-reflect, or /taku-cso discovers a non-obvious pattern or pitfall, they append to the learnings file.

---

## Retro Mode

Analyze what the team shipped, how the work happened, and where to improve. Evidence-based, specific, candid.

### Arguments

- `/taku-reflect` — learn mode (default)
- `/taku-reflect --retro` — last 7 days
- `/taku-reflect --retro 14d` — last 14 days
- `/taku-reflect --retro 30d` — last 30 days

### Step 1: Gather Raw Data

```bash
git config user.name && git config user.email
git log origin/<base> --since="<window>" --format="%H|%aN|%ae|%ai|%s" --shortstat
git log origin/<base> --since="<window>" --format="COMMIT:%H|%aN" --numstat
git log origin/<base> --since="<window>" --format="" --name-only | grep -v '^$' | sort | uniq -c | sort -rn
git shortlog origin/<base> --since="<window>" -sn --no-merges
```

### Step 2: Compute Metrics

Summary: commits, contributors, PRs, insertions, deletions, net LOC, test LOC ratio, active days, sessions, avg LOC/session-hr.

Per-author leaderboard sorted by commits.

### Step 3: Time & Session Patterns

Hourly histogram. Detect sessions (45-min gap). Classify: Deep (50+ min), Medium (20-50), Micro (<20).

### Step 4: Work Patterns

Commit type breakdown by conventional prefix. Flag fix ratio > 50%. Hotspot analysis: top 10 files. Flag files changed 5+ times.

### Step 5: Team Member Analysis

For each contributor: commits, LOC, test ratio, areas, biggest ship.
**Praise** (anchored in commits): 1-2 things. **Growth area** (framed as investment): 1 thing.

### Step 6: Week-over-Week Trends

Load prior retro from `.taku/retros/`. Compare key metrics.

### Step 7: Narrative

Output: Summary table + trends, Time & sessions, Your week + team, Top 3 Wins + 3 Improvements + 3 Habits.

### Step 8: Save

Save to `.taku/retros/{date}.md`. Append trends to `.taku/retros/trends.jsonl`.

---

## Anti-Rationalization

| Excuse | Why it's wrong |
|--------|---------------|
| "I'll remember this" | You won't. Next session starts fresh. Write it down. |
| "This is too obvious to log" | Obvious now. Not obvious in 3 weeks after 50 other sessions. |
| "We didn't do much this week" | Even small weeks have patterns worth examining. |
| "Retros waste time" | 5 minutes of reflection saves hours of repeated mistakes. |
