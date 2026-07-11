# One Dot Cinnabar（一点丹红）

## Use When

Use this style for formal presentation-like HTML web PPT decks: work reports, job debriefs, project reviews, executive briefings, business proposals, course frameworks, document summaries, and image/text/video-rich report pages.

## Visual Language

- Background: warm grey outer canvas, close to `#E7DFDC`.
- Slide surface: white or off-white paper texture, close to `#FBFAF7`, with a restrained shadow.
- Accent: cinnabar red, close to `#D8242F` or `#C91F2D`. Use it only for dots, section numbers, rules, chart highlights, and active states.
- Text: graphite black `#222222`, secondary grey `#707070`, faint grey `#D8D4D0`.
- Structure: 16:9 slide sections, report grid, thin red vertical lines, small English page labels, large pale numbers, black-and-white media blocks.
- Avoid full red backgrounds except small emphasis cards. Avoid festive, party-government, or cheap template styling.

## Component Grammar

- `.deck-shell`: page-level viewport container.
- `.report-slide`: one full presentation section. Use for cover, contents, chapter, metrics, image-text, timeline, media, and closing pages.
- `.section-dot`: single cinnabar dot before important headings.
- `.red-rule`: fine cinnabar line for page rhythm.
- `.page-label`: small uppercase metadata in the upper right.
- `.jump-select`, `.presenter-control`, and `.jump-panel`: precise slide navigation for formal presentations. Keep jump controls outside the main cover composition; use a small presenter control or topbar selector instead of placing a large "quick navigation" card on the cover.
- `.content-nav`: contents/navigation panel with active state.
- `.report-card`: restrained white content block; use sparingly.
- `.metric-row`, `.bar-chart`, `.donut-set`, `.timeline`: formal data components.
- `.time-node[data-detail-target]`: a timeline or agenda item that opens a dedicated detail slide when the source content is substantial.
- `.time-node[data-inline-note]`: a timeline or agenda item that expands a short note in the current slide when the source content is brief.
- `.evidence-toggle`: a small click target that opens extra proof/notes inside the slide.
- `.media-frame`: placeholder for future images, charts, screenshots, or video.

## Interaction Rules

- Keep motion minimal and presentation-like.
- Support vertical wheel navigation and keyboard navigation between slides.
- Support precise slide selection for formal review scenarios, such as a leader asking to jump directly to page 7.
- Add active state to contents/navigation items.
- Use slide entrance motion: small vertical translation, fade, and red rule drawing.
- Allow click-to-expand details for evidence notes or document excerpts.
- Animate charts only when a slide becomes active.
- Support `prefers-reduced-motion` by disabling smooth scrolling and animations.
- Do not use playful floating objects, large hover tilt, glowing gradients, or decorative particles.

## Content Intake Rules

When the user supplies documents, text, images, screenshots, charts, or videos:

- Read the material first and identify content type: cover info, agenda, chapter headings, claims, data, proof, images, screenshots, and closing statement.
- Map formal text into slide sections instead of dumping it into one long page.
- Put screenshots or photos into `.media-frame`, usually black-and-white or low-saturation unless the user asks to preserve color.
- Put numeric content into `metric-row`, `bar-chart`, or `donut-set`.
- Put process content into `timeline`.
- Put long supporting paragraphs behind `evidence-toggle` so slides stay clean.
- Split dense agenda/timeline items into dedicated `.report-slide` detail pages when they contain multiple paragraphs, images, videos, charts, or evidence. Keep brief items inline with an expandable note.
- Preserve source meaning, but compress on-slide copy into presentation-readable text.

## Layout Rules

- Desktop: keep each `.report-slide` close to a 16:9 presentation surface, centered in a grey stage.
- Keep cover pages externally presentable. Do not show instructional UI copy such as "quickly locate slides" inside the cover; place that function in a discreet presenter control.
- Mobile: convert slides into single-column report sections; do not force tiny unreadable 16:9 cards.
- Keep red usage below roughly 15% of the page.
- Do not let Chinese text overflow buttons, number blocks, or cards.

## Good Fit

- "Turn this report document into a formal HTML presentation page."
- "Make an executive briefing from these notes, images, and charts."
- "Use a restrained Chinese red report style for this project review."

## Avoid

- Casual self-media layouts, playful stickers, oversized decorative cards, heavy animations, full-screen red hero panels, and random icon grids.
