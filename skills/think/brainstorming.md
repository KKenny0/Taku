---
name: taku-brainstorm
description: >
  Invoke before ANY creative or implementation work — new feature, component,
  API, refactor, or behavioral change. This is the design-first gate. Do NOT
  write code, scaffold projects, or invoke implementation skills until the user
  approves the design. Also handles design system creation (brand identity,
  typography, color, spacing, layout). Triggers on "build me X", "add a feature
  for", "let's design", "how should we implement", "design system", "brand",
  "visual identity", "design tokens", or any request that implies building.
---

# Taku Brainstorm — Socratic Design Refinement

Turn ideas into validated designs through structured dialogue. One question at a
time. No code until the user approves.

## Why the Design-First Gate?

Code written without a design is expensive code. Every "quick implementation" that
skips design ends up rewritten, patched, or abandoned. The design phase costs
minutes. Rewrites cost days. This gate exists because the most common failure mode
in software isn't bad code — it's building the wrong thing well.

## Hard Gate

No implementation skill is invoked, no code is written, no project is scaffolded,
until the design is presented and the user explicitly approves it. This applies to
every project regardless of perceived simplicity.

**"This is too simple to need a design"** — that's where unexamined assumptions cause
the most wasted work. A todo list, a single utility, a config change: all of them
benefit from 3 minutes of thinking. The design can be short. But present it and get
approval.

## 9-Step Checklist

Complete these in order. Do not skip steps.

### 1. Explore Project Context

Read the codebase before asking questions. You can't design in a vacuum.

- Read CLAUDE.md, README.md, package.json (or equivalent)
- Check recent commits: what's changed lately?
- Map the area the user wants to touch: which files, which modules, which patterns?
- Check for existing design docs (DESIGN.md, `.taku/office-hours-*.md`)

**Why:** Understanding the existing structure prevents proposing patterns that conflict
with established conventions. It also reveals reusable code you might not know about.

### 2. Scope Assessment

Before diving into questions, assess size:

- If the request describes multiple independent subsystems ("build a platform with
  chat, file storage, billing, and analytics"), flag this immediately.
- Help decompose into sub-projects: what are the independent pieces, how do they relate,
  what order should they be built?
- Brainstorm the first sub-project through the full design flow. Each sub-project gets
  its own design → plan → implementation cycle.

**Why:** A single design doc for a platform-sized project produces a plan nobody can
execute. Decomposition turns the impossible into a sequence of possible.

### 3. Ask Clarifying Questions

Ask **one at a time**. Prefer multiple choice when possible. Focus on:

- **Purpose:** What problem does this solve? For whom?
- **Constraints:** Performance? Compatibility? Time? Budget?
- **Success criteria:** What does "done" look like concretely?

Only one question per message. If a topic needs more exploration, break it into
multiple questions across multiple messages.

**Why:** One question at a time lets the user think deeply about each dimension rather
than producing shallow answers to a list. Multiple choice reduces cognitive load.

### 4. Propose 2-3 Approaches

Present distinct options with trade-offs:

```
Approach A: {name}
  Summary: 1-2 sentences
  Effort:  S/M/L
  Risk:    Low/Med/High
  Pros:    2-3 bullets
  Cons:    2-3 bullets

Approach B: {name}
  ...

Approach C: {name} (if a meaningfully different path exists)
  ...
```

One must be the **minimal viable** approach. One must be the **ideal architecture**.
Lead with your recommendation and explain why.

**Why:** Forced alternatives prevent premature commitment to the first idea that feels
good. The trade-off analysis surfaces risks early when they're cheap to address.

### 5. Present Design in Sections

Once an approach is chosen, present the design piece by piece:

- Architecture overview
- Component breakdown and data flow
- Error handling strategy
- Testing strategy

Present each section and ask "does this look right?" before continuing. Scale depth
to complexity: a few sentences for simple changes, up to a paragraph for nuanced ones.

**Why:** Incremental validation catches misunderstandings early. Getting approval section
by section is faster than rewriting an entire rejected design.

### 6. Design for Isolation

Ensure each component has:
- One clear purpose
- Well-defined interfaces
- Ability to be understood and tested independently

If you can't answer "what does this do, how do you use it, what does it depend on?"
without reading internals, the boundaries need work.

**Why:** Isolated components are easier to build, test, debug, and change. When a file
grows large, it's usually doing too much — split it.

### 7. Write Design Doc

Save the approved design to `DESIGN.md` at the project root. Include:

- Problem statement
- Recommended approach with rationale
- Architecture and component breakdown
- Data flow
- Error handling
- Testing strategy
- Success criteria
- Open questions

### 8. Spec Self-Review

After writing, review your own doc:

1. **Placeholder scan:** Any TBD, TODO, incomplete sections? Fix them.
2. **Internal consistency:** Do sections contradict each other?
3. **Scope check:** Focused enough for one implementation plan, or does it need decomposition?
4. **Ambiguity check:** Could any requirement be interpreted two ways? Pick one.

Fix issues inline. No need for a formal second review — just fix and move on.

### 9. User Reviews Spec

Ask the user to review the written DESIGN.md:

> "Design written to DESIGN.md. Please review it and let me know if you want changes
> before we create the implementation plan."

Wait for approval. If changes are requested, make them and re-review.

**Why:** The written spec is the contract between the design phase and the build phase.
Getting explicit approval prevents "but I thought you meant..." disagreements later.

## Terminal State

Once the design is approved, invoke `/taku-plan` to create the implementation plan.
Do NOT invoke any implementation skill directly. The plan is the bridge between design
and code.

## Key Principles

- **One question at a time** — don't overwhelm
- **Multiple choice preferred** — easier to answer
- **YAGNI ruthlessly** — cut unnecessary features from all designs
- **Explore alternatives** — always propose 2-3 before settling
- **Incremental validation** — get approval at each stage
- **Be flexible** — go back and clarify when something doesn't make sense

## Design System Mode

When the user says "design system", "brand identity", "visual identity", "design tokens", or the project needs aesthetic direction, switch to design system mode. This produces a concrete specification the implementer can build from.

### Phase 1: Product Context

Gather: target audience, core emotion (trust/speed/delight/calm), competitive set (3-5 products), anti-patterns (what to avoid), constraints (dark mode, RTL, accessibility). Use AskUserQuestion with concrete options.

### Phase 2: Competitive Research

Use web_search to study competitors. For each: one thing done well (steal the principle), one thing done poorly (avoid the trap).

### Phase 3: Full Design Proposal

Produce: aesthetic direction (specific, not "clean and modern"), typography (no Inter/Roboto/system-ui as primary), color system (CSS custom properties with WCAG AA contrast), spacing scale, layout grid, motion (durations, easing, prefers-reduced-motion).

### Phase 4: SAFE/RISK Breakdown

Classify every design decision. If 3+ are RISK, simplify.

### Phase 5: Preview (Optional)

If image generation available: component showcase and sample page. Skip if unavailable.

### Phase 6: Write to DESIGN.md

Append `## Design System` section with all tokens. No placeholders, no TBD.

## Known Pitfalls

**Presenting one approach and calling it three.** "Approach A: Use React. Approach B: Use React with hooks. Approach C: Use React with hooks and TypeScript." All three are the same approach with minor variations. The user has no real choice and the trade-off analysis is theater.

*What went wrong:* The skill says "2-3 distinct options with trade-offs." The keyword is *distinct*. Variations on the same architecture aren't alternatives — they're implementation details.

*Prevention:* One approach must be minimal viable (fewest files, smallest diff). One must be ideal architecture. If a third exists, it must approach the problem from a genuinely different angle (different data model, different framework, different mental model). If you can't find three genuinely different approaches, present two. Two real options beat three fake ones.

**Skipping the design-first gate for "obvious" features.** "Add a logout button" seems too simple for a design. But the design questions reveal: Should it invalidate server sessions or just clear local state? Should it show a confirmation? What happens to in-flight requests? These answers change the implementation significantly.

*What went wrong:* "This is too simple to need a design" is literally the first entry in the anti-rationalization table. It was rationalized anyway.

*Prevention:* The Hard Gate applies to every project regardless of perceived simplicity. The design CAN be short — a few sentences answering the key questions. But present it and get approval. A 3-minute design for a logout button prevents a 3-hour debate about session invalidation strategy.

**Writing DESIGN.md with TBD sections.** The design was approved verbally but the written doc had "Error handling: TBD" and "Testing strategy: standard approach." During implementation, the developer interpreted "standard approach" as no tests at all.

*What went wrong:* Step 7 (Write Design Doc) was rushed. Step 8 (Spec Self-Review) was skipped. The placeholder scan would have caught these.

*Prevention:* Step 8's placeholder scan is mandatory. After writing DESIGN.md, search for TBD, TODO, "appropriate", "standard", and "handle". Every instance must be replaced with a concrete decision. A design doc with TBDs is a design doc that hasn't been written yet.

## Anti-Rationalization

| Excuse | Why it's wrong |
|--------|---------------|
| "This is too simple for a design doc" | Simple projects are where unexamined assumptions waste the most time |
| "I already know what to build" | You thought you knew the last three times too |
| "The user just wants code" | The user wants working code. Design is how you get there |
| "I'll figure out the details while coding" | That's called refactoring in circles |
| "Let me just prototype it" | A prototype without a design is an experiment without a hypothesis |
