# Pastel Blockfolio

Pastel Blockfolio is a polished HTML style for tutorial and case-study pages. It feels like a design portfolio page mixed with a visual workflow board.

## Use When

- The page explains a process, before/after change, tool workflow, tutorial, or self-media case.
- The user wants a page that feels designed, friendly, and high-impact without looking corporate.
- The content benefits from visual blocks, labels, cards, comparison panels, and a strong hero.

## Avoid When

- The page must feel formal, institutional, luxury, dark, or minimal.
- The content is a dense dashboard or operational SaaS tool.
- The user needs a neutral business report.

## Visual DNA

- Background: off-white paper `#f7f7f4`
- Ink: near-black `#111111`
- Accents:
  - pastel pink `#ffd8e6`
  - mint green `#bff0c9`
  - sticky yellow `#fff06a`
  - hot pink line `#ff8fc7`
- Typography: heavy sans for headings, compact readable body text.
- Shapes: thick black borders, square corners, slight rotations, hard shadows, sticky-note labels.
- Layout: sticky top nav, strong hero, slide-like sections, comparison image/card, process blocks, tabs, palette board, script/title chips.

## Required Components

1. Hero with a clear literal headline and a self-owned visual panel.
2. Section rhythm using `Part 01`, `Part 02`, etc. or equivalent labels.
3. At least one structured visual component: comparison panel, flow cards, table, tabs, palette board, or script card.
4. Motion should be subtle: reveal on scroll, hover lift, progress bar, tilt cards only when it helps.
5. Mobile must stack cleanly with no horizontal overflow.

## Copyright Safety

Do not directly reuse external reference screenshots as page imagery unless the user owns them or explicitly approves. Extract reusable elements instead:

- color palette
- spacing rhythm
- border weight
- card/grid structure
- sticker or note motif
- typography mood

Build fresh diagrams, abstract UI boards, or generated/self-owned images.

## Implementation Notes

- Do not use viewport-width font scaling directly. Use `clamp()` with reasonable min/max.
- Keep letter spacing at `0` except small uppercase eyebrow labels.
- Keep desktop sections near one-screen height when the page is presentation-like.
- On mobile, allow natural scrolling instead of forcing `100vh` sections.
- If deploying, rewrite asset paths so the publish directory is self-contained.
