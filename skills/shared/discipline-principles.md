# Taku Shared Discipline Principles

This file is the canonical reference for principles shared across Taku skills.
It is not a protocol spec, framework API, or process template.

## Design Direction

Taku is a coding-agent engineering discipline pack. Its value is not telling a
strong model every mechanical step to take. Its value is preserving the
judgment traps and quality gates that remain useful as models improve.

Prefer principles over procedures:

- Keep the "why" stable.
- Let the local skill choose the "how" when multiple good paths exist.
- Make mandatory constraints rare, explicit, and durable.
- Keep skill bodies focused; move repeated discipline language here.

## Rule Labels

Use these labels only when they clarify how strict a rule is.

### [IRON LAW]

A rule that protects Taku's core correctness guarantees and should not relax
just because the model seems capable.

Use for constraints such as:

- no implementation before an approved design path
- no production code without a failing test anchor when code is being written
- no bug fix before root cause investigation
- no completion claim without fresh verification evidence
- no long-term memory write without explicit user approval

An iron law should be rare. If a skill has more than one or two, either the
skill is over-constrained or the rule belongs in this shared file.

### [GUIDANCE]

A strong default that helps most runs but may be adapted when context justifies
it. Guidance should become lighter as the host model becomes more capable.

Use for:

- preferred phase order
- recommended review shape
- execution mode selection heuristics
- formatting and artifact conventions
- budget checks and escalation thresholds

When adapting guidance, state the reason briefly and preserve the underlying
principle.

## Durable Principles

### Evidence Before Claims

Do not claim something is done, tested, reviewed, reproduced, or compacted
without evidence from files, git, tool output, logs, or explicit user input.
When evidence is missing, say `unknown`, `not_established`, or `not_run`.

### Root Cause Before Fix

For broken behavior, first bound the failure path. A patch that changes the
symptom without explaining why the symptom occurred is not a Taku-quality fix.

### Scope Before Motion

Before non-trivial work, name the intended change surface and the acceptance
criteria. This can be a full design, a plan, or a compact mini design for small
work.

### Anti-Rationalization

Taku skills should intercept common shortcuts before the agent explains them
away. Good anti-rationalization text names the tempting excuse, why it is wrong,
and what to do instead.

### Shared Completion Vocabulary

Use the same completion statuses across phase skills:

- `DONE`: complete, verified enough for the phase, no blocking concerns
- `DONE_WITH_CONCERNS`: complete, but non-blocking risks or gaps remain
- `BLOCKED`: external input, missing context, or unresolved failure prevents
  responsible progress

Do not invent new completion statuses unless a local integration requires them.

## What Not To Extract

Do not move phase-specific procedures here just because they repeat a pattern.
Debug's investigation phases, Review's pass structure, Build's execution modes,
and Think's mode selection are local skill behavior. This file holds the shared
discipline behind those behaviors.
