---
name: taku-write-skill
description: >
  Use when creating new skills, editing existing skills, or verifying skills work
  before deployment. Triggers on "write a skill", "create a skill", "edit this skill",
  "is this skill correct", "test this skill", or when the reflect phase needs to
  codify a learned pattern into reusable documentation.
---

# taku-write-skill — TDD for Documentation

Writing skills IS test-driven development applied to process documentation. You write test cases (pressure scenarios), watch them fail (baseline behavior), write the skill, watch them pass (agents comply), and refactor (close loopholes).

## Why This Matters

Untested skills have issues. Always. An untested skill is an untested function — you're deploying it to production and hoping for the best. 15 minutes of testing saves hours of debugging broken agent behavior.

## Skill Types

Choose the right type before writing:

### TECHNIQUE
Concrete method with steps to follow. Examples: condition-based-waiting, root-cause-tracing, image-compression. The skill teaches HOW to do something specific.

### PATTERN
Way of thinking about a problem. Examples: flatten-with-flags, test-invariants, subtract-the-obvious. The skill teaches a mental model, not a procedure.

### REFERENCE
API docs, syntax guides, tool documentation. The skill is a lookup table. Examples: CLIs, library APIs, configuration formats.

## SKILL.md Structure

```yaml
---
name: skill-name-with-hyphens
description: >
  Use when [specific triggering conditions]. Third person. No workflow summary.
  Include symptoms, error messages, and contexts that signal this skill applies.
---

# Skill Name

## Overview
What is this? Core principle in 1-2 sentences.

## When to Use
Bullet list with symptoms and use cases.

## Core Pattern
Before/after comparison or step-by-step process.

## Quick Reference
Table or bullets for scanning.

## Common Mistakes
What goes wrong + fixes.

## Anti-Rationalization (for discipline skills)
Red flags table. Spirit vs letter clause.
```

### Description Field: Claude Search Optimization

The description is how future agents find your skill. It's the most important field.

**Rules:**
- Start with "Use when..." to focus on triggering conditions
- Include specific error messages, symptoms, and contexts
- NEVER summarize the skill's workflow or process
- Why: If the description says "run X then Y," the agent may follow the summary instead of reading the full skill. The description is a trigger, not a tutorial.

```yaml
# BAD: Summarizes workflow — agent follows summary instead of reading skill
description: Use when debugging — add logs, trace data flow, fix root cause

# GOOD: Triggering conditions only — agent reads the skill for the actual process
description: Use when encountering any bug, test failure, or unexpected behavior
```

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

Write the skill before testing? Delete it. Start over. Edit without testing? Same violation. No exceptions.

## RED-GREEN-REFACTOR for Skills

### RED: Write Failing Test (Baseline)

Run a pressure scenario WITHOUT the skill. Use a subagent so it starts fresh.

- Give it a task that should trigger the skill
- Document exactly what it does wrong: choices made, rationalizations used, steps skipped
- Capture the verbatim excuses: "this is simple enough," "I'll test after," "the spirit matters more than the letter"

This is watching the test fail. You MUST see what agents naturally do before writing the skill.

### GREEN: Write Minimal Skill

Write the skill that addresses those specific failures. Nothing more.

- Address each rationalization from the baseline with an explicit counter
- Don't add content for hypothetical cases you didn't observe
- Keep it under 500 lines. If it's longer, split into skill + supporting file

Run the same scenarios WITH the skill. Agent should now comply.

### REFACTOR: Close Loopholes

Agent found a new rationalization? Add an explicit counter. Re-test. Repeat until bulletproof.

## Anti-Rationalization (for discipline-enforcing skills)

Skills that enforce rules (TDD, systematic debugging, verification) need extra protection. Agents are smart and will find loopholes under pressure.

### Spirit vs Letter Clause

Add this early in the skill:

> **Violating the letter of the rules is violating the spirit of the rules.**

This cuts off the entire class of "I'm following the spirit" rationalizations.

### Rationalization Table

Capture every excuse from baseline testing:

```markdown
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "It's about spirit not ritual" | The ritual IS the safeguard. |
| "This is different because..." | Every bug is "different." The process still applies. |
```

### Red Flags List

```markdown
## Red Flags — STOP and Start Over

- [List specific behaviors that indicate violation]
- [Each one maps to a rationalization from the table]

**All of these mean: Stop. Return to the beginning.**
```

## Common Mistakes

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| No failing test first | Don't know if skill teaches the right thing | Run baseline before writing |
| Description summarizes workflow | Agent follows summary, skips skill body | Describe triggers only |
| Multiple language examples | Dilutes quality, increases maintenance | One excellent example |
| Narrative storytelling | Not reusable | Principles and patterns |
| No anti-rationalization | Agents find loopholes under pressure | Red flags table + spirit clause |
| Batch-creating skills without testing | Each one may have issues | Test EACH skill before moving on |

## Completion

Checklist:
- [ ] Baseline test run WITHOUT skill (RED)
- [ ] Skill written addressing specific failures (GREEN)
- [ ] Same scenarios pass WITH skill
- [ ] New rationalizations identified and plugged (REFACTOR)
- [ ] YAML frontmatter: name (hyphens only), description (triggering conditions)
- [ ] Under 500 lines
- [ ] One excellent example (not multi-language)

Status: DONE when all checklist items are complete. DONE_WITH_CONCERNS if rationalizations remain unaddressed. BLOCKED if baseline testing is skipped.
