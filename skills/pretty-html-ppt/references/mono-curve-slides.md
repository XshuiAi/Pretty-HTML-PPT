# Mono Curve Slides（墨线白稿）

## Use When

Use this style for HTML web PPT decks that should feel like a clean presentation deck arranged inside a digital gallery: video update pages, product walkthroughs, course notes, proposal summaries, lightweight case studies, or slide-by-slide tutorials.

## Visual Language

- Page background: cool grey, close to `#9B9BA3` or `#A3A1A8`.
- Main surfaces: white 16:9 cards with restrained shadow and thin grey borders.
- Typography: handwritten or marker-like display headings paired with compact neutral sans-serif metadata. Use local font stacks only unless the project explicitly allows web fonts.
- Color: mostly black and white. Use soft red/yellow/blue/green washes only as small atmospheric highlights or data blocks.
- Decoration: thin wandering SVG curve lines, compact black marker bars, small slide labels, understated page numbers.
- Composition: keep generous blank space. Let each section feel like a slide, not a dense dashboard.

## Component Grammar

- `.stage`: grey outer canvas with centered content.
- `.slide-card`: 16:9 white canvas. Use for hero, chapter slides, video slides, and detail slides.
- `.script-title`: handwritten display headline.
- `.micro-label`: small uppercase or compact metadata label.
- `.marker-bar`: short black horizontal bar for emphasis or section rhythm.
- `.curve-line`: absolute SVG or border-like linework. Keep it thin and irregular.
- `.color-wash`: blurred, low-opacity color accent. Never use as a full gradient background.
- `.slide-grid`: gallery grid of smaller 16:9 cards.
- `.focus-viewer`: modal-like overlay or expanded view for a selected slide.

## Interaction Rules

- Add pointer-responsive tilt to slide cards, capped around `2deg` and `6px` lift.
- Add scroll reveals, but keep motion calm and paper-like.
- Add one line-drawing or slow curve movement effect; avoid busy looping decoration.
- Make the hero slide visibly interactive on first load. Include immediate line drawing, subtle drifting accents, and 2-3 clickable explanation points so users understand the page is interactive before opening any gallery card.
- Let slide thumbnails be clickable. Clicking should focus or enlarge the selected slide, preserve that slide's own visual elements, and add small interactive explanation points rather than replacing it with a generic empty detail page.
- Use a progress rail or numbered slide markers when there are multiple cards.
- Support `prefers-reduced-motion` by disabling tilt, animation, and smooth scrolling.

## Layout Rules

- Use 16:9 aspect ratio for slide cards: `aspect-ratio: 16 / 9`.
- On desktop, show one large hero slide followed by a grid of slide cards.
- On mobile, keep cards full width and preserve aspect ratio; reduce large handwritten headings so text does not overflow.
- Avoid nested cards. A slide can contain inner text blocks, but not another decorative card.
- Do not use direct screenshots from reference decks unless the user owns them or explicitly approves usage.

## Good Fit

- "Make a webpage from this product update video in a clean slide-deck style."
- "Turn these notes into a presentation-like HTML gallery."
- "Create a minimal black-and-white HTML tutorial page with a few soft color accents."

## Avoid

- Heavy gradients, glow effects, bokeh blobs, complex icon decoration, dense admin panels, crowded cards, or full-page marketing hero layouts.
