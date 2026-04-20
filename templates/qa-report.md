# QA Report Template

> Fill this out after running `/taku-qa`. One report per QA session.

## Report Metadata

- **Date:** YYYY-MM-DD
- **Branch:** feature/branch-name
- **Base:** main
- **QA Tier:** QUICK / STANDARD / EXHAUSTIVE
- **Tester:** agent / manual
- **URL:** https://staging.example.com

## Health Score

```
Score: N/10
```

| Score | Meaning |
|-------|---------|
| 10 | No issues found |
| 8-9 | Minor issues only, all auto-fixed |
| 6-7 | Some important issues, all fixed |
| 4-5 | Critical issues found, fixed with caveats |
| 0-3 | Critical issues, some unresolved — DO NOT SHIP |

## Findings

### Finding 1

| Field | Value |
|-------|-------|
| **Severity** | Critical / Important / Minor |
| **Description** | What is broken |
| **Repro Steps** | 1. Navigate to X 2. Click Y 3. Observe Z |
| **Expected** | What should happen |
| **Actual** | What actually happens |
| **Screenshot** | `.taku/qa/screenshots/finding-1.png` or N/A |
| **Status** | Fixed / Open / Won't Fix |

### Finding 2

| Field | Value |
|-------|-------|
| **Severity** | Critical / Important / Minor |
| **Description** | What is broken |
| **Repro Steps** | 1. Navigate to X 2. Click Y 3. Observe Z |
| **Expected** | What should happen |
| **Actual** | What actually happens |
| **Screenshot** | `.taku/qa/screenshots/finding-2.png` or N/A |
| **Status** | Fixed / Open / Won't Fix |

<!-- Add more findings as needed -->

## Summary

- **Total findings:** N
- **Critical:** N (N fixed, N open)
- **Important:** N (N fixed, N open)
- **Minor:** N (N fixed, N open)
- **Auto-fixed:** N

## Recommendations

1. [Specific recommendation based on findings]
2. [Specific recommendation based on findings]
3. [Specific recommendation based on findings]

## Console Errors

```
[paste critical console errors found during QA]
```

## Performance

| Metric | Value | Baseline | Status |
|--------|-------|----------|--------|
| Page load | Xs | Ys | PASS / DEGRADED |
| Time to interactive | Xs | Ys | PASS / DEGRADED |
| Largest contentful paint | Xs | Ys | PASS / DEGRADED |

## Verdict

**SHIP / DON'T SHIP / SHIP WITH CONCERNS**

[One-sentence justification]
