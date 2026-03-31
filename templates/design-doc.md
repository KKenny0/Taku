# Design Document: {PROJECT_NAME}

> **Date:** {YYYY-MM-DD}
> **Status:** Draft
> **Author:** {author}

---

## Problem Statement

What problem does this solve? Who has it? What happens if they don't get a solution?

Describe the pain clearly. Not "users need X" but "when a user tries to do Y, they hit Z, which costs them W."

## Proposed Solution

How does this solve the problem? What's the approach?

Describe the solution at a high level. What does the user experience look like after this is built? What's the core mechanic?

## Key Decisions and Trade-offs

| Decision | Chose | Alternative | Why |
|----------|-------|-------------|-----|
| {decision} | {choice} | {alternative} | {reasoning} |

Document the non-obvious choices. Why this architecture, not that one? Why this library, not the popular one? These decisions are the most valuable part of the design doc for future readers.

## Architecture Overview

```
<Component A> → <Component B> → <Component C>
      ↕              ↕
  <Database>    <External API>
```

How do the pieces fit together? What are the main components and how do they communicate?

## User Stories / Acceptance Criteria

### {User Story 1}

**As a** {role}, **I want to** {action}, **so that** {benefit}.

**Acceptance criteria:**
- [ ] {criterion 1}
- [ ] {criterion 2}

### {User Story 2}

...

## Non-Goals

What we are NOT building. This is as important as what we are building.

- {Not building X because Y}
- {Not supporting Z because W}

Prevents scope creep and sets clear boundaries for reviewers.

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {risk} | High/Med/Low | High/Med/Low | {what we'll do about it} |

Be honest about what could go wrong. A risk table with no "High" items is probably incomplete.

## Open Questions

- {Question} — needs resolution before: {phase}
- {Question} — blocked by: {dependency}

List what's still unknown. These need answers before implementation starts or at specific milestones.
