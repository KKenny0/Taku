---
name: taku-think
description: >
  Clarify ambiguous development requests, new feature ideas, product/design choices,
  and idea-stage work before planning. Three adaptive modes: Quick (small clear
  changes → fast alignment), Design (feature requests → architecture + DESIGN.md),
  Explore (new ideas → forcing questions before committing). Triggers on "add a
  feature", "I have an idea", "should we build", "let's design", "设计一下",
  "需求分析", "我有个想法", or when the user describes a desired end state but
  implementation choices or success criteria are not yet settled. Also handles
  design system creation. Bug fixes and refactors use `/taku-debug` or
  `/taku-review` directly unless they need fresh design decisions.
---

# Taku Think — Adaptive Design Thinking

Three modes adapt to request complexity. No ceremony for simple requests. Full rigor for complex ones. Hard gate always: no implementation until the selected design path is approved.

## Mode Selection

Analyze both **what the user says** and **how mature the request is**. Don't rely on keywords alone.

**Quick** — when ALL are true:
- The request names specific files, modules, or functions to change
- The implied action is singular: add, rename, fix, or rewire one thing
- The user's framing includes constraints or success criteria (explicit or clearly implied)
- No architectural decision is needed — there's one obvious place to put the code

**Design** — the default for feature work:
- The request names a feature area (e.g. "settings page", "notifications") rather than specific files
- The "how" is ambiguous: data model, component structure, or integration points are open
- Multiple modules or services are involved, and their boundaries need defining

**Explore** — for idea-stage thinking:
- The request has no success criteria — the user can't yet describe what "done" looks like
- The framing is a question: "should we build", "what if", "I'm thinking about"
- Product/market concerns dominate: who needs this, is there demand, what's the wedge

**Edge case — "Build me a SaaS platform":** The user said "build" but the request is idea-stage (no constraints, no feature list, no success criteria). This is Explore, not Design. The signal is request maturity, not phrasing.

**Edge case — "I have an idea for a caching layer":** Sounds like Explore, but the user has a specific technical concept with implied constraints. This is Design. The signal is specificity, not phrasing.

When in doubt, default to **Design**. Quick mode should feel obviously right — if you're debating whether it qualifies, it doesn't.

---

## Quick Mode

For requests where full design process is wasteful. Not "no thinking" — right-sized thinking.

### Flow

1. **One alignment question.** Summarize your understanding and ask if it's correct.
   > "I'm planning to [X]. That means touching [files/areas]. Does that match what you had in mind?"

2. **User confirms.** If they correct you, adjust and re-confirm.

3. **Write a mini design** using this template. Either append to DESIGN.md as a new section, or write directly into PLAN.md if the change is small enough that design and plan are the same thing:

   - **Change:** One sentence describing what to change
   - **Why:** One sentence on motivation
   - **Touch Points:** Files/modules affected
   - **Risks:** Most likely thing to get wrong
   - **Done When:** How to verify completion

4. **Go.** Route to `/taku-plan` (or proceed to build if plan already exists).

### What Quick Mode is NOT

- Not skipping design entirely — you still state what you'll do and get approval
- Not for "I'll just figure it out while coding" — that's the anti-pattern
- Not for requests where multiple implementation paths exist — if you can imagine two reasonable approaches, it's not Quick

**Why Quick Mode exists:** Full design process on a logout button is wasteful. But zero thinking on a logout button is how you forget session invalidation. Quick mode is the senior engineer's instinct: quick mental check, then execute.

---

## Design Mode

For feature requests that need architectural thought. The core Taku design flow.

### Pre-Flight

1. Read project context: CLAUDE.md, README.md, package.json (or equivalent)
2. Check recent commits: what's changed lately?
3. Map the area the user wants to touch: files, modules, patterns
4. Check for existing design docs (DESIGN.md, `.taku/office-hours-*.md`)

### Clarifying Questions

Ask **one at a time**. Prefer multiple choice when possible. Focus on:

- **Purpose:** What problem does this solve? For whom?
- **Constraints:** Performance? Compatibility? Time?
- **Success criteria:** What does "done" look like?

Skip questions the user already answered in their initial request. If they gave a thorough description, move on.

**Hard cap:** Maximum 2 clarifying questions per session. If you have enough information to form a conservative but executable design, stop asking and present the design.

### Propose 2-3 Approaches

Present distinct options with trade-offs:

```
Approach A: {name} (recommended)
  Summary: 1-2 sentences
  Effort:  S/M/L
  Risk:    Low/Med/High
  Pros:    2-3 bullets
  Cons:    2-3 bullets
  Why not: 1-2 sentences explaining why you're not recommending this

Approach B: {name}
  ...
```

One must be **minimal viable** (fewest files, smallest diff, ships fastest). One must be **ideal architecture** (best long-term). If you can't find a genuinely different third option, two is fine — two real options beat three fake ones.

### Present Design

Once an approach is chosen, present the design:

- Architecture overview
- Component breakdown and data flow
- Error handling strategy
- Testing strategy

Scale depth to complexity: a few sentences for moderate changes, a paragraph per section for complex ones.

### Write DESIGN.md

Save the approved design to `DESIGN.md` at the project root. Use `templates/design-doc.md` as the scaffold, then adapt it to the template matching the project's depth-tier (detected in SKILL.md pre-flight; if unknown, use Standard). The skill rules override the template if they differ.

**Lightweight tier** (for small, focused changes):

- Problem statement
- Recommended approach with rationale
- Touch points: files and modules affected
- Risks
- Done when: success criteria

**Standard / Deep tier** (default; for anything cross-module or architecturally significant):

- Problem statement
- Recommended approach with rationale
- Architecture and component breakdown
- Data flow
- Error handling
- Testing strategy
- Success criteria
- Open questions (if any — no TBD allowed)

### Self-Review

Before showing the user, check:
1. **Placeholder scan:** Any TBD, TODO, "standard approach", "handle appropriately"? Replace with specifics.
2. **Internal consistency:** Do sections contradict each other?
3. **Scope check:** Focused enough for one plan, or needs splitting?

Fix issues inline. No formal process — just verify your own work.

### User Approval

> "Design written to DESIGN.md. Review it and let me know if you want changes before we create the implementation plan."

Wait for approval. The written spec is the contract between design and build. No code until approved.

---

## Explore Mode

For idea-stage exploration. Ask hard questions before committing to build. Two sub-modes:

**Startup** — building a product or intrapreneurship project. Ask forcing questions.

**Builder** — hackathon, side project, open source, learning. Be an enthusiastic design partner.

### Startup Mode: Forcing Questions

Ask **one at a time**. Push until answers are specific and evidence-based.

| # | Question | What to listen for |
|---|----------|--------------------|
| Q1 | What's the strongest evidence someone actually wants this? (Not interest — behavior) | Specific behavior: paying, expanding usage, building workflow around it |
| Q2 | What are users doing right now to solve this? What does that workaround cost? | Specific workflow, hours wasted, tools duct-taped together |
| Q3 | Name the actual human who needs this most. What gets them fired? | A name, a role, a specific consequence |
| Q4 | What's the smallest version someone would pay for this week? | One feature, one workflow, shippable in days |
| Q5 | Have you watched someone use this without helping? What surprised you? | A specific surprise that contradicted assumptions |
| Q6 | If the world changes in 3 years, does this become more or less essential? | A specific claim about why this product gets more valuable |

**Smart Routing:** Not every session needs all six.

- Pre-product (idea, no users) → Q1, Q2, Q3
- Has users (not paying) → Q2, Q4, Q5
- Has paying customers → Q4, Q5, Q6
- Pure engineering/infra → Q2, Q4 only
- Feature idea ("should we build X?") → Q1, Q4, Q2

If earlier answers already cover a later question, skip it.

**Escape Hatch:** If the user says "just do it" or pushes back:
1. First pushback → ask the 2 most critical remaining questions, then proceed
2. Second pushback → respect it and move on
3. If they provide a fully formed plan with evidence → skip to alternatives

### Builder Mode: Design Partner

You're an enthusiastic collaborator. Riff on ideas, suggest combinations, find the most exciting version.

Questions (ask one at a time, skip already-answered):
- What's the coolest version of this? What would make someone say "whoa"?
- Who would you show this to first?
- What's the fastest path to something you can actually use?
- What existing thing is closest, and how is yours different?
- What would you add with unlimited time?

If the user says "just do it" → skip to alternatives.

### Premise Challenge (both sub-modes)

Before proposing solutions:

1. Is this the right problem? Could a different framing be simpler?
2. What happens if we do nothing? Real pain or hypothetical?
3. What existing code already partially solves this?

Present premises for user agreement. If they disagree, revise.

### Alternatives

Produce 2-3 approaches:
- One **minimal viable** (fewest files, smallest diff)
- One **ideal architecture** (best long-term)
- One **creative/lateral** (if one exists)

For each: summary, effort (S/M/L), risk, pros, cons. Recommend one.

### Output

Save session notes to `.taku/explore-{date}.md`:

```markdown
# Explore — {date}

## Mode
Startup | Builder

## Key Insights
{from questions}

## Premises
{agreed premises}

## Approaches
### A: {name}
{summary, effort, risk, pros, cons}
### B: {name}
...

## Recommended
{choice + rationale}

## Open Questions
{unresolved items}
```

### Handoff

After saving notes, offer the user a path forward:
- **If the idea survived questioning and a specific feature emerged:** proceed to Design mode to produce DESIGN.md
- **If the idea needs more exploration:** stop here. The user has session notes to think with.
- **If the design is already clear enough:** skip to `/taku-plan`

---

## Hard Gate

This applies to ALL modes, including Quick.

No implementation skill is invoked, no code is written, no project is scaffolded, until the design is presented and the user explicitly approves it.

For Quick mode, "design" can be 3-5 sentences. For Design mode, it's DESIGN.md. For Explore mode, the gate applies when transitioning to build.

"This is too simple to need a design" — that's where unexamined assumptions cause the most wasted work. The design can be short. But present it and get approval.

## Think Outcomes

Every think session ends with one of:

- **Proceed to Plan** — Design approved, ready for `/taku-plan`
- **Proceed to Design** — (Explore only) Idea validated, needs full Design mode before planning
- **Need More Information** — Blocking unknowns prevent a decision. List what's needed and stop.
- **Do Not Build Yet** — After exploration, the right answer is to wait. Record why in explore notes or DESIGN.md.

Not every think session leads to code. "Do Not Build Yet" is a valid, disciplined outcome.

## Think → Plan Handoff

Before routing to `/taku-plan`, verify ALL of these exist:

- **Approved design:** DESIGN.md approved by user, or Quick mode mini design confirmed
- **Recommended approach:** One chosen approach with rationale — not just a list of options
- **Resolved open questions:** Every open question is either answered or explicitly recorded as an accepted unknown
- **Success criteria:** Concrete, testable definition of "done"
- **Scope boundaries:** What's in scope and what's deliberately out of scope

If any are missing, resolve them before handing off. The plan skill cannot fill design gaps.

---

## Scope Assessment

Before any mode's main flow, check scope:

- If the request describes multiple independent subsystems ("build a platform with chat, storage, billing, and analytics"), flag it immediately
- Decompose into sub-projects: what's independent, how do they relate, what order?
- Run the chosen mode on the first sub-project. Each gets its own design → plan → build cycle

---

## Anti-Rationalization

| Excuse | Why it's wrong |
|--------|---------------|
| "This is too simple for a design" | Simple requests are where unexamined assumptions waste the most time. The design can be 3 sentences. |
| "I already know what to build" | You thought you knew the last three times too. |
| "The user just wants code" | The user wants working code. Design is how you get there. |
| "I'll figure it out while coding" | That's called refactoring in circles. |
| "Skip the questions, just build" | The Escape Hatch handles this — ask the 2 most critical, then proceed. Not zero. |
| "Quick mode means no thinking" | Quick mode means right-sized thinking. No thinking is how logout buttons forget session invalidation. |

## Known Pitfalls

**Quick mode applied to something that isn't quick.** "Add a settings page" sounds simple. Quick mode was used. The "settings page" turned out to need: per-user settings, admin overrides, audit logging, migration from env vars, and a new database table. The 3-sentence design missed all of it.

*Prevention:* Quick mode requires ALL conditions to be true: specific change, single implementation path, no architectural decisions. If you can imagine two reasonable approaches, it's Design mode. "Add a settings page" has multiple approaches — Design. "Add a dark mode toggle to the header" has one — Quick.

**Presenting one approach as three options.** "Approach A: Use React. Approach B: Use React with hooks. Approach C: Use React with hooks and TypeScript." All three are the same approach. The user has no real choice.

*Prevention:* One approach must be minimal viable. One must be ideal architecture. If a third exists, it must approach the problem from a genuinely different angle. Two real options beat three fake ones.

**Asking all six forcing questions regardless of context.** A solo engineer building an internal tool got the full startup interrogation. The session felt like a VC pitch for a tool that didn't need one. The engineer abandoned the session.

*Prevention:* Use Smart Routing. Pre-product → Q1, Q2, Q3. Has users → Q2, Q4, Q5. Pure engineering → Q2, Q4. If earlier answers cover later questions, skip them. Six questions every session is a process failure.

**Writing DESIGN.md with TBD sections.** The design was approved verbally but the written doc had "Error handling: TBD." During implementation, "TBD" was interpreted as "no error handling."

*Prevention:* Self-review catches this. After writing, search for TBD, TODO, "appropriate", "standard", "handle". Every instance must be replaced with a concrete decision. A design doc with TBDs hasn't been written yet.

---

## Design System Mode (UI-Heavy Projects)

Only activates on keywords: "design system", "brand identity", "visual identity", "design tokens". For backend/CLI/API projects, skip entirely.

Full workflow (6 phases: product context → competitive research → proposal → SAFE/RISK breakdown → preview → output) is in `references/design-system.md`. Load it when triggered.
