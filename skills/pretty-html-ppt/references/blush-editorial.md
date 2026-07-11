# Blush Editorial

## Character

Blush Editorial is a warm, spacious editorial system for content-rich brand pages. It borrows general design methods from premium lifestyle publishing: decisive headlines, clear vertical chapters, quiet white surfaces, selective bright color, and short feedback loops. Never copy third-party logos, copy, illustrations, photography, or distinctive compositions.

## Best Fit

Use it for:
- product, tool, creator, or resource recommendations
- branded tutorials and content collections
- comparative explainers with a small number of important entries
- editorial landing pages where scanning and reading matter equally

Avoid it for dense admin dashboards, complex data tables, terminal-like tools, or highly playful children-focused experiences.

## Design Tokens

```css
:root {
  --canvas: #fff5ed;
  --surface: #ffffff;
  --ink: #101012;
  --muted: #5d585b;
  --pink: #ff4f9a;
  --pink-soft: #ffe3ef;
  --surface-tint: #fff8fb;
  --line: #e9ded9;
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --content: 1180px;
  --space-section: clamp(72px, 10vw, 136px);
  --ease-out: cubic-bezier(.2, .8, .2, 1);
}
```

No gradients, glow, dark blue/slate dominance, decorative blobs, eye icons, meaningless arcs, or ornamental wave lines.

## Typography

- Use a modern system sans stack. Do not depend on a remote font for the page to work.
- Display title: `clamp(48px, 7vw, 92px)`, `700-800`, line-height `0.96-1.02`.
- Section title: `clamp(32px, 4vw, 56px)`, line-height near `1.05`.
- Item title: `clamp(26px, 3vw, 42px)`.
- Body: `16-19px`, line-height `1.65-1.8`, color `--muted`.
- Letter spacing remains `0`; never use negative tracking.
- On mobile, reduce title size through breakpoint-specific fixed/clamp bounds, not viewport-width-only scaling.

## Required Page Grammar

1. A slim reading-progress line and compact sticky chapter navigation may sit at the top.
2. The hero contains a small pink pill, strong title, short subtitle, and a compact metric/status label aligned to the right on desktop.
3. Core entries run vertically, one full-width white row per item.
4. Each `.feature-row` contains:
   - `.item-index`
   - `.category-pill`
   - `.letter-mark`
   - item name and one-sentence positioning
   - detailed description
   - exactly three `.capability-item` entries when the source supports them
   - `.scene-chip` or a concise suitable-use block
5. Follow the core entries with one full-width bright-pink `.section-band`.
6. Put secondary recommendations in a two-column `.secondary-grid`; each card still explains purpose and capabilities.
7. Mobile becomes a single column with no horizontal overflow.

## Components

- `.page-shell`: max-width wrapper with generous side padding.
- `.eyebrow-pill`: compact pink or pale-pink category label.
- `.metric-chip`: small status/data label; never a decorative badge cloud.
- `.chapter-nav`: sticky, horizontally scrollable chapter links with one active state.
- `.feature-row`: white editorial content surface with 1px border and restrained 14-20px radius.
- `.item-index`: bright-pink two-digit number.
- `.letter-mark`: 36-44px circular mark, black on pale pink or white on pink.
- `.capability-list`: three compact capability rows separated by hairlines.
- `.details-toggle`: text button for optional supporting detail; it must expose `aria-expanded`.
- `.filter-control`: segmented content filter with `aria-pressed`; use only when categories help readers compare.
- `.floating-meta`: one compact, meaningful hero module that may use a slow ambient float.
- `.section-band`: full-width pink chapter divider with black or white text chosen for contrast.
- `.secondary-card`: white card with purpose, capability summary, and use case.
- `.button`: pill-like action may be round, but ordinary content containers stay within 8-20px radius.

## Interaction And Motion

Use interaction to clarify reading state, not decorate empty space.

### Required

- Reading progress: a 3px top line grows with document scroll.
- Scroll reveal: content enters once with `opacity: 0 -> 1` and `translateY(16px) -> 0` over `450-600ms`.
- Active chapter: IntersectionObserver updates the corresponding `.chapter-nav` link.
- Row hover (pointer devices): border shifts toward pink, background may move to `--surface-tint`, and the row lifts no more than 2px. Do not add a shadow.
- Rich card hover (pointer devices): content cards may use a pointer-driven tilt capped at `1.2deg` and `4px` lift. Reset immediately on pointer leave and never apply it to long text containers on mobile.
- Capability response: capability rows may shift 4px and invert their numbered marker on hover or keyboard focus.
- Button hover: background/color change in `100-180ms`; a trailing arrow may translate 3-4px.
- Expandable detail: `.details-toggle` reveals a compact panel using opacity and grid-row/height. Keep the trigger state accessible.
- Content filtering: category controls update `aria-pressed`, animate matching rows in place, and announce the visible result count through an `aria-live` region.
- Focus: all links and controls receive a visible 2px outline with offset.

### Optional

- A segmented filter may show/hide core entries when the content naturally has categories.
- A secondary-card carousel is acceptable only on narrow mobile layouts and only with user controls. Do not auto-advance.
- Number or letter marks may scale from `0.94` to `1` during reveal.
- One hero metadata module may float vertically by 4-6px over 4-6 seconds. Pause it on hover/focus and do not apply ambient motion to the main reading cards.

### Prohibited

- parallax, looping marquee text, bouncing springs, large rotations, cursor followers, autoplay carousels, scroll hijacking, or attention-seeking ambient motion
- motion that changes layout dimensions unexpectedly
- hiding essential content behind hover-only behavior

### Reduced Motion

Under `@media (prefers-reduced-motion: reduce)`, disable smooth scrolling, transforms, reveal transitions, and progress animation. Content must remain immediately visible.

## Responsive Rules

- Desktop feature row: metadata rail plus flexible content columns.
- Below roughly `820px`: stack row areas, keep index/category/letter marks in a compact metadata strip.
- Below roughly `640px`: one-column hero and secondary grid; chapter navigation stays horizontally scrollable.
- Use `minmax(0, 1fr)`, `overflow-wrap: anywhere`, and stable button dimensions to prevent collisions.
- The longest title, label, and capability sentence must remain inside its parent at 360px viewport width.

## Adaptation Rules

- Preserve the supplied content hierarchy before styling it.
- If the source has fewer than three capabilities, do not invent claims; change the component count.
- If no data label exists, use a useful content descriptor such as reading time or update date, or omit it.
- Images are optional. When used, they must show the actual subject and have rights-safe provenance.
- Keep the page independently readable with JavaScript disabled; only enhancement behavior may depend on JS.

## Verification

- Validate at desktop and 360-390px mobile widths.
- Confirm no horizontal overflow, clipping, overlap, missing focus state, or invisible content with JavaScript disabled.
- Confirm expansion controls update `aria-expanded`.
- Confirm reduced-motion mode removes transforms and nonessential animation.
- Confirm no third-party brand assets or copied page content remain in the deliverable.
