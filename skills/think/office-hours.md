---
name: taku-office-hours
description: >
  Invoke when the user describes a new product idea, asks "is this worth building",
  says "help me think through this", or wants to brainstorm before code. Proactively
  trigger on any request that implies building something that doesn't exist yet.
  Two modes: Startup (hard questions, demand validation) and Builder (enthusiastic
  design partner). Saves a design doc. Use before /taku-plan or /taku-brainstorm.
---

# Taku Office Hours

Two modes for turning rough ideas into sharp designs. Startup mode applies YC-grade
forcing questions. Builder mode is an enthusiastic design partner. Both produce a
design document — neither writes code.

Why this exists: most failed products fail because nobody asked hard questions early.
The cost of this skill is 10-20 minutes. The cost of building the wrong thing is weeks.

## Pre-Flight

1. Read project context: CLAUDE.md, README.md, recent git log
2. Determine mode (ask the user):

> What's your goal with this?
> A) Building a startup or intrapreneurship project
> B) Hackathon, side project, open source, or learning

Startup/intrapreneurship → **Startup mode**. Everything else → **Builder mode**.

## Mode 1: Startup — The Six Forcing Questions

Ask these **one at a time**. Push until answers are specific, evidence-based, and
slightly uncomfortable. Comfort means the thinking isn't deep enough.

### Q1: Demand Reality

**Ask:** "What's the strongest evidence that someone actually wants this? Not interest,
not waitlist signups — what behavior proves real demand?"

**Why this matters:** Interest is free. Behavior is truth. If nobody would scramble if
this disappeared tomorrow, there's no product here.

**Push until you hear:** Specific behavior — someone paying, someone expanding usage,
someone building their workflow around it, someone who'd have to scramble if you vanished.

**Red flags:** "People say it's interesting." "500 waitlist signups." "VCs are excited." None of these are demand.

### Q2: Status Quo

**Ask:** "What are your users doing right now to solve this problem, even badly? What
does that workaround cost them?"

**Why this matters:** The status quo is your real competitor. Not another startup, not
a big company — the spreadsheet-and-Slack workaround your user already lives with.
If "nothing" is the current solution, the problem probably isn't painful enough.

**Push until you hear:** A specific workflow, hours wasted, dollars lost, tools duct-taped together.

### Q3: Desperate Specificity

**Ask:** "Name the actual human who needs this most. What's their title? What gets them
promoted? What gets them fired?"

**Why this matters:** You can't email a category. "Healthcare enterprises" is a filter,
not a person. Specificity is the only currency in product thinking.

**Push until you hear:** A name, a role, a specific consequence if the problem isn't solved.

### Q4: Narrowest Wedge

**Ask:** "What's the smallest possible version someone would pay real money for — this
week, not after you build the platform?"

**Why this matters:** Narrow beats wide, early. The smallest version someone will pay
for this week is more valuable than the full platform vision. Wedge first, expand
from strength.

**Push until you hear:** One feature, one workflow, something shippable in days.

### Q5: Observation & Surprise

**Ask:** "Have you sat down and watched someone use this without helping them? What did
they do that surprised you?"

**Why this matters:** Users do things products weren't designed for. That's often the
real product trying to emerge. Surveys lie, demos are theater, observation is truth.

**Push until you hear:** A specific surprise that contradicted assumptions.

### Q6: Future-Fit

**Ask:** "If the world looks different in 3 years, does your product become more
essential or less?"

**Why this matters:** A rising tide lifts all competitors equally. "AI keeps getting
better" is not a product thesis. You need a specific claim about why YOUR product
gets more valuable as the world changes.

**Push until you hear:** A specific claim about how users' world changes and why that
change makes this product more essential.

### Smart Routing

Not every session needs all six questions. Based on product stage:

- Pre-product (idea, no users) → Q1, Q2, Q3
- Has users (not paying) → Q2, Q4, Q5
- Has paying customers → Q4, Q5, Q6
- Pure engineering/infra → Q2, Q4 only

If earlier answers already cover a later question, skip it.

### Escape Hatch

If the user pushes back ("just do it", "skip the questions"):
- Ask the 2 most critical remaining questions for their stage, then proceed.
- If they push back a second time, respect it and move on.
- If they provide a fully formed plan with real evidence, skip to premise challenge.

## Mode 2: Builder — Design Partner

You're an enthusiastic collaborator. Riff on ideas, suggest cool combinations, find the
most exciting version of what they're building.

### Questions (ask one at a time)

- **What's the coolest version of this?** What would make someone say "whoa"?
- **Who would you show this to?** What makes them say "whoa"?
- **What's the fastest path to something you can actually use?**
- **What existing thing is closest, and how is yours different?**
- **What would you add with unlimited time?** The 10x version.

Skip questions already answered by the user's initial description.

If the user says "just do it" or provides a fully formed plan → skip to alternatives generation.

## Premise Challenge (both modes)

Before proposing solutions, challenge the premises:

1. Is this the right problem? Could a different framing be simpler or more impactful?
2. What happens if we do nothing? Real pain or hypothetical?
3. What existing code already partially solves this?
4. For new deliverables: how will users get it? Code without distribution is dead code.

Present premises for user agreement. If they disagree, revise and loop.

## Alternatives Generation

Produce 2-3 approaches:
- One **minimal viable** (fewest files, smallest diff, ships fastest)
- One **ideal architecture** (best long-term trajectory)
- One **creative/lateral** (different framing, if one exists)

For each: summary, effort (S/M/L), risk, pros, cons. Recommend one.

## Output

Save session notes to `.taku/office-hours-{date}.md`:

```markdown
# Office Hours — {date}

## Mode
Startup | Builder

## Demand Evidence
{from Q1}

## Status Quo
{from Q2}

## Target User & Wedge
{from Q3 + Q4}

## Premises
{agreed premises}

## Approaches
### A: {name}
{summary, effort, risk, pros, cons}
### B: {name}
...

## Recommended Approach
{choice + rationale}

## Open Questions
{unresolved items}

## Next Steps
{one concrete action the user should take}
```

## Handoff

After saving notes:
- Recommend `/taku-brainstorm` to refine the chosen approach into a full DESIGN.md
- Or `/taku-plan` if the design is already clear enough to plan
