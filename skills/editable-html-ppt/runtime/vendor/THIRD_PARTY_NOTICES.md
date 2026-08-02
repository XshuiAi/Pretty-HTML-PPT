# Third-party browser export dependencies

- `pptxgenjs-4.0.1.min.js` — PptxGenJS 4.0.1, MIT License. See `pptxgenjs-LICENSE`.
- `html-to-image-1.11.13.js` — html-to-image 1.11.13, MIT License. See `html-to-image-LICENSE`.
- `jszip-3.10.1.min.js` — JSZip 3.10.1, MIT License. See `jszip-LICENSE`.

These pinned browser bundles are inlined only when `scripts/inject_edit_mode.py`
prepares an editable deck. They enable offline, local PPTX export without a CDN
or a server-side upload.
