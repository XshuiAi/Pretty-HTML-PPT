# Optional PPTX Export

Use this reference only when the user explicitly needs a `.pptx` handoff. HTML remains the primary delivery format because browser interactions, live editing, web motion, and responsive behavior cannot be reproduced fully in PowerPoint.

## Enable The Exporter

PPTX support is optional so normal HTML decks remain lightweight:

```bash
python3 scripts/copy_template.py <style-slug> /absolute/output/dir --pptx-export
```

For an existing HTML deck:

```bash
python3 scripts/inject_pptx_export.py /absolute/output/dir/index.html
```

Validate an enabled deck with:

```bash
python3 scripts/validate_deck.py /absolute/output/dir --require-pptx-export
```

The exporter is self-contained and bundles pinned copies of PptxGenJS 4.0.1, html-to-image 1.11.13, and JSZip 3.10.1. License files and notices live in `runtime/vendor/`.

## Two Modes

### High-Fidelity PPTX

Each HTML page is rendered to a high-resolution image and fitted proportionally onto a 16:9 PowerPoint slide. Use this mode for projection, review, archiving, and visual consistency. Objects inside the slide image are not individually editable.

### Editable-Text PPTX

The exporter captures the visual background with primary text hidden, then recreates headings, paragraphs, lists, quotes, table cells, captions, and inserted text boxes as PowerPoint text objects. Use this mode when recipients need to revise the main wording.

Complex decoration, SVG/WebGL output, charts, icons, pseudo-elements, and special display typography remain part of the background image. Browser and PowerPoint font engines wrap text differently, so editable-text export is a practical handoff, not a pixel-identical reconstruction.

## Font And Asset Rules

- Use fonts that exist on the recipient's computer for editable body text.
- Keep brand lettering, unusual display type, icons, and complex visual labels in the background image.
- Keep local images beside the deck and verify they load before exporting.
- Cross-origin images without suitable access headers can block browser capture; download approved assets locally when necessary.
- Speaker notes are included in both modes when the page contains `.speaker-notes` or `[data-speaker-notes]`.

## Verification

After export:

1. Open the PPTX in PowerPoint or WPS.
2. Check the first, middle, and last slide for cropping and aspect-ratio fit.
3. In editable-text mode, click several headings and paragraphs to confirm they are native text boxes.
4. Check font substitution and line wrapping on the intended presentation computer.
5. Confirm speaker notes exist on slides that supplied them.
