---
name: taku-design-review
description: >
  Use when a plan has UI/UX components that need design quality scoring — aesthetic,
  typography, color, spacing, layout, motion, responsiveness, accessibility, and
  content hierarchy. Triggers on "design review", "does this look good", "rate the
  design", "design critique", or when plan-phase UI decisions need evaluation.
---

# taku-design-review — Design Dimension Scoring

A design review that scores, not opines. Each dimension gets a number, an explanation of what perfection looks like, and a specific fix to close the gap.

## Why This Matters

"Looks good" is not a design review. Neither is "I don't like the color." Design quality is measurable across specific dimensions. This skill forces that measurement, explains the gap between current and ideal, and produces actionable fixes the implementer can apply.

## The 9 Dimensions

Rate each 0-10. For anything below 8, explain what a 10 looks like and write the specific fix into the plan.

### 1. Aesthetic (0-10)
Does the design have a coherent visual personality, or does it look like a template?

**What a 10 looks like:** Every visual choice serves the product's identity. No element feels generic or borrowed. The design is recognizable as THIS product, not "a SaaS app."

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 2. Typography (0-10)
Are type choices intentional? Hierarchy, weight, size, spacing, line height — all specified?

**What a 10 looks like:** Exact typeface named for primary and secondary. Size scale defined. Heading/body contrast ratio >= 1.5x. Line height specified for body (1.5-1.6) and headings (1.1-1.2). No default system fonts as identity font.

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 3. Color (0-10)
Is the color system complete with tokens, dark mode, and WCAG AA contrast?

**What a 10 looks like:** All colors defined as CSS variables. Dark mode variants specified. Contrast ratios verified (4.5:1 for body text, 3:1 for large text). Accent color used sparingly, not everywhere. No purple-on-white defaults.

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 4. Spacing (0-10)
Is there a consistent spacing scale, or are values arbitrary?

**What a 10 looks like:** Base unit defined (4px or 8px). Spacing scale: 4/8/12/16/24/32/48/64/96. All padding, margins, and gaps use values from this scale. No magic numbers like `margin: 17px`.

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 5. Layout (0-10)
Does the layout have intentional structure, or is it "stuff on a page"?

**What a 10 looks like:** Grid system defined (columns, gutters, max-width). Each section has one clear purpose. Visual hierarchy guides the eye: primary content first, secondary second, tertiary third. No competing focal points.

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 6. Motion (0-10)
Is animation intentional and performant, or absent/indiscriminate?

**What a 10 looks like:** Transition durations defined (150/300/500ms). Easing curves specified. Animations serve hierarchy (drawing attention, indicating state change), not decoration. `prefers-reduced-motion` respected. Nothing animates just because it can.

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 7. Responsiveness (0-10)
Is each viewport intentionally designed, or is mobile just "stacked columns"?

**What a 10 looks like:** Breakpoints defined with layout behavior per breakpoint (not "responsive"). Mobile layout designed separately, not just desktop squished. Touch targets >= 44px. Navigation adapts (not just hamburger). Images resize appropriately.

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 8. Accessibility (0-10)
Can everyone use this, or is it designed for one specific user profile?

**What a 10 looks like:** Keyboard navigation works for all interactions. ARIA landmarks defined. Screen reader tested (logical heading order, alt text, form labels). Color contrast meets WCAG AA. Focus states visible. No content conveyed by color alone.

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 9. Content Hierarchy (0-10)
Does the user know what to look at first, second, third?

**What a 10 looks like:** Every screen has clear visual hierarchy. One primary action per view. Headings are scannable without reading body text. Information is layered: essential first, details on demand. Empty states designed (warm, helpful, actionable).

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

## Output Format

```
DESIGN REVIEW SCORECARD
═══════════════════════════════════════════
Dimension          | Score | What 10 Looks Like           | Fix
───────────────────|───────|──────────────────────────────|─────────────
Aesthetic          |  N/10 | ...                          | ...
Typography         |  N/10 | ...                          | ...
Color              |  N/10 | ...                          | ...
Spacing            |  N/10 | ...                          | ...
Layout             |  N/10 | ...                          | ...
Motion             |  N/10 | ...                          | ...
Responsiveness     |  N/10 | ...                          | ...
Accessibility      |  N/10 | ...                          | ...
Content Hierarchy  |  N/10 | ...                          | ...
═══════════════════════════════════════════
OVERALL: N/10
```

For dimensions scoring 8+, a brief note is fine. For dimensions below 8, the fix must be specific enough for the implementer to act on without asking questions.

## Completion

Append a `## Design Review` section to the design doc with the scorecard and all fixes.

If overall score is 8+: "Design is implementation-ready. Run taku-visual-review after implementation for visual QA."

If overall score is below 8: "Design needs revision. Address the fixes above before proceeding to build."

Status: DONE when all 9 dimensions are scored and fixes are written into the plan. DONE_WITH_CONCERNS if the user deferred fixes. BLOCKED if no design exists to review.
