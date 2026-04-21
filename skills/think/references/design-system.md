# Design System Mode (UI-Heavy Projects)

A sub-mode within Design mode. Only activates when the user says "design system", "brand identity", "visual identity", "design tokens", or the project explicitly needs aesthetic direction. For most backend/CLI/API projects, this section never triggers.

## Phase 1: Product Context

Gather: target audience, core emotion (trust/speed/delight/calm), competitive set (3-5 products), anti-patterns (what to avoid), constraints (dark mode, RTL, accessibility).

## Phase 2: Competitive Research

For each competitor: one thing done well (steal the principle), one thing done poorly (avoid the trap).

## Phase 3: Full Proposal

- **Aesthetic direction:** Specific, not "clean and modern"
- **Typography:** No Inter/Roboto/system-ui as primary. Name exact typeface. Define size scale, heading/body contrast ratio ≥ 1.5x, line heights
- **Color system:** CSS custom properties. Dark mode variants. WCAG AA contrast (4.5:1 body, 3:1 large text)
- **Spacing scale:** Base unit (4px or 8px), defined scale (4/8/12/16/24/32/48/64/96)
- **Layout grid:** Columns, gutters, max-width
- **Motion:** Duration scale (150/300/500ms), easing curves, prefers-reduced-motion

## Phase 4: SAFE/RISK Breakdown

Classify every design decision. If 3+ are RISK, simplify.

## Phase 5: Preview (Optional)

If image generation available: component showcase and sample page. Skip if unavailable.

## Phase 6: Output

Append `## Design System` section to DESIGN.md with all tokens. No placeholders.
