---
name: taku-guard
description: >
  Execution reliability expert. ALWAYS invoke this skill after any coding skill
  completes its work. Do not accept completed work without running this guard
  first. Use this skill to audit step execution and catch silent omissions.
---

# Taku Guard - Silent Omission Audit

Guard audits completed agent work. It does not redo the task; it checks whether
the claimed work left visible evidence.

Rule labels: `[IRON LAW]` is non-negotiable; `[GUIDANCE]` is a strong default.

[IRON LAW] Do not accept a completion claim without visible evidence: command
output, file diff, explicit step marker, or a concrete explanation of why no
audit is possible.

## Inputs

Use current conversation context first. If the user passes an argument such as
`/taku-guard build`, treat it as the skill or workflow under audit.

- Recent chat messages and completion claims
- Recent command output visible in the session
- `git diff --stat`, `git diff`, and `git diff --cached`
- The invoked skill's `SKILL.md`, when identifiable

If no skill can be identified, skip the step audit and still run the evidence
gate against claims and diffs.

## Pass 1 - Step Audit

When an invoked skill is identifiable:

1. Read that skill's `SKILL.md`.
2. Extract required steps from numbered lists and `## Step N` headings.
3. For each required step, look for visible output in the session.
4. Mark each step as `visible`, `missing`, or `not-applicable`.

Visible output means a reader can inspect evidence that the step happened. Silent
internal reasoning is not evidence.

[GUIDANCE] If a step is conditional, mark it `not-applicable` only when the
condition is visibly false or the previous agent explicitly bounded it.

## Pass 2 - Evidence Gate

Scan the final response and recent messages for completion claims such as:

- tests pass
- no errors
- verified
- fixed
- implemented
- reviewed
- ready

For each claim, find supporting evidence:

- Test, lint, typecheck, build, or import command output
- Diff evidence showing the relevant file changes
- Reproduction output for a bug fix
- Review findings or explicit no-findings rationale for review work

Flag every claim that lacks supporting evidence. Evidence must be specific
enough that another agent can re-check it.

## Pass 3 - Omission Self-Audit

Combine Pass 1 and Pass 2 findings, then answer this forced question:

```text
What step was most likely skipped?
```

[IRON LAW] Give a specific best-guess answer and reasoning. Do not answer
`none`, `unclear`, or `not enough information` unless the no-auditable-work edge
case applies.

Prefer the likely skipped step that has the highest delivery risk: missing
verification, missing root-cause proof, missing diff review, missing scope
check, or missing user-visible sanity check.

## No Auditable Work Edge Case

Return `VERDICT: NO_AUDITABLE_WORK` only when all of these are true:

1. No file changes are visible.
2. No command output is available.
3. No completion claim can be checked.
4. No invoked `SKILL.md` can be identified.

Briefly explain why the session cannot be audited. Do not mark it incomplete.

## Output Format

Always use this report shape:

```text
GUARD REPORT
- Skill audited: [name | unknown]
- Steps with visible output: [count]/[count]
- Steps with no output: [count] ([step labels, or none])
- Completion claims without evidence: [count] ([claims, or none])
- Likely omission: [specific skipped step and reasoning]
VERDICT: COMPLETE | INCOMPLETE | NO_AUDITABLE_WORK - [one sentence]
```

Use `COMPLETE` only when every required step has evidence and every completion
claim is supported. Use `INCOMPLETE` when any required step or claim lacks
evidence.

## Hard Stops

- Do not run broad fixes while auditing.
- Do not invent command output.
- Do not treat plans, intentions, or internal reasoning as execution evidence.
- Do not hide uncertainty; put it in the likely-omission reasoning.
