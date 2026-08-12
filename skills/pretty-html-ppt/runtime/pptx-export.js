(() => {
  if (window.__prettyHtmlPptxExportLoaded) return;
  window.__prettyHtmlPptxExportLoaded = true;

  const PPTX_WIDE = { width: 13.333, height: 7.5 };
  let exporting = false;
  let toastTimer = null;

  function toast(message) {
    let node = document.querySelector(".xs-pptx-toast");
    if (!node) {
      node = document.createElement("div");
      node.className = "xs-pptx-toast";
      document.body.appendChild(node);
    }
    node.textContent = message;
    node.classList.add("is-visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => node.classList.remove("is-visible"), 2200);
  }

  function deckSlides() {
    const selector = document.querySelector("[data-slide]")
      ? "[data-slide]"
      : "main > section, main > article, section[id], article[id]";
    return [...document.querySelectorAll(selector)]
      .filter((slide, index, all) => all.indexOf(slide) === index)
      .filter((slide) => !slide.closest(".shui-presenter-overlay, .xs-edit-toolbar, .xs-pptx-toolbar"))
      .filter((slide) => {
        const rect = slide.getBoundingClientRect();
        return rect.width > 32 && rect.height > 32;
      });
  }

  function safeFilename(editableText) {
    const base = (document.title || "pretty-html-ppt")
      .replace(/[\\/:*?"<>|]+/g, "-")
      .replace(/\s+/g, " ")
      .trim();
    return `${base}${editableText ? "-editable-text" : ""}.pptx`;
  }

  async function waitForAssets(slides) {
    await document.fonts?.ready;
    const images = slides.flatMap((slide) => [...slide.querySelectorAll("img")]);
    await Promise.all(images.map((image) => image.complete
      ? image.decode?.().catch(() => undefined)
      : new Promise((resolve) => {
          image.addEventListener("load", resolve, { once: true });
          image.addEventListener("error", resolve, { once: true });
        })));
  }

  function noteFor(slide) {
    return (slide.querySelector("[data-speaker-notes], .speaker-notes")?.textContent || "").trim();
  }

  function cssColorToHex(value) {
    const rgba = String(value || "").match(/rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/i);
    if (rgba) {
      return rgba.slice(1).map((part) => Number(part).toString(16).padStart(2, "0")).join("").toUpperCase();
    }
    const hex = String(value || "").match(/^#([0-9a-f]{6})$/i);
    return hex ? hex[1].toUpperCase() : "111827";
  }

  function alignment(value) {
    const normalized = String(value || "").toLowerCase();
    if (["center", "justify", "right"].includes(normalized)) return normalized;
    return normalized === "end" ? "right" : "left";
  }

  function textCandidates(slide) {
    const selector = "h1,h2,h3,p,li,blockquote,td,th,dt,dd,figcaption,caption,.xs-inserted-text-content";
    return [...slide.querySelectorAll(selector)].filter((element) => {
      if (element.closest("[data-speaker-notes], .speaker-notes, [data-no-edit], .xs-edit-toolbar, .xs-pptx-toolbar")) return false;
      if (element.querySelector(selector)) return false;
      const rect = element.getBoundingClientRect();
      const style = getComputedStyle(element);
      const text = (element.innerText || element.textContent || "").trim();
      return Boolean(text)
        && rect.width >= 24
        && rect.height >= 10
        && (parseFloat(style.fontSize) || 0) >= 11
        && style.display !== "none"
        && style.visibility !== "hidden";
    });
  }

  function fittedSlideBox(rect) {
    const scale = Math.min(PPTX_WIDE.width / rect.width, PPTX_WIDE.height / rect.height);
    const width = rect.width * scale;
    const height = rect.height * scale;
    return {
      x: (PPTX_WIDE.width - width) / 2,
      y: (PPTX_WIDE.height - height) / 2,
      width,
      height,
    };
  }

  function textEntry(element, slideRect, box) {
    const rect = element.getBoundingClientRect();
    const style = getComputedStyle(element);
    const pxToPt = box.width * 72 / slideRect.width;
    const fontSize = Math.max(8, Math.min(96, (parseFloat(style.fontSize) || 16) * pxToPt));
    const fontFace = String(style.fontFamily || "").split(",")[0].trim().replace(/^['"]|['"]$/g, "");
    const text = (element.innerText || element.textContent || "").replace(/\u00a0/g, " ").trim();
    const lineHeightPx = parseFloat(style.lineHeight);
    return {
      text,
      options: {
        x: box.x + Math.max(0, (rect.left - slideRect.left) / slideRect.width * box.width),
        y: box.y + Math.max(0, (rect.top - slideRect.top) / slideRect.height * box.height),
        w: Math.max(.05, rect.width / slideRect.width * box.width),
        h: Math.max(.05, rect.height / slideRect.height * box.height),
        fontFace,
        fontSize,
        color: cssColorToHex(style.color),
        bold: Number.parseInt(style.fontWeight, 10) >= 600 || style.fontWeight === "bold",
        italic: style.fontStyle === "italic",
        align: alignment(style.textAlign),
        valign: "top",
        margin: 0,
        lineSpacing: Number.isFinite(lineHeightPx) ? Math.max(fontSize, lineHeightPx * pxToPt) : undefined,
        breakLine: false,
      },
    };
  }

  async function captureSlide(slide, rect) {
    const background = getComputedStyle(slide).backgroundColor;
    return window.htmlToImage.toPng(slide, {
      pixelRatio: Math.min(3, Math.max(2, window.devicePixelRatio || 1)),
      cacheBust: false,
      backgroundColor: background === "rgba(0, 0, 0, 0)" ? "#ffffff" : background,
      width: Math.round(rect.width),
      height: Math.round(rect.height),
      style: {
        transform: "none",
        width: `${Math.round(rect.width)}px`,
        height: `${Math.round(rect.height)}px`,
        minWidth: "0",
        minHeight: "0",
        margin: "0",
        boxSizing: "border-box",
      },
      filter: (node) => !node.classList?.contains("xs-insert-controls")
        && !node.classList?.contains("xs-insert-resize")
        && !node.classList?.contains("xs-inserted-text-controls")
        && !node.classList?.contains("xs-media-badge")
        && !node.classList?.contains("shui-talk-timer-dock"),
    });
  }

  async function exportPptx(editableText = false) {
    if (exporting) return;
    if (!window.PptxGenJS || !window.htmlToImage?.toPng) {
      toast("PPTX 导出组件未加载，请刷新后重试");
      return;
    }
    const slides = deckSlides();
    if (!slides.length) return toast("未找到可导出的页面");

    exporting = true;
    const button = document.querySelector(editableText ? "[data-xs-pptx-editable]" : "[data-xs-pptx-fidelity]");
    const originalLabel = button?.textContent || "";
    if (button) button.disabled = true;
    document.body.classList.add("xs-pptx-exporting");
    try {
      await waitForAssets(slides);
      const pptx = new window.PptxGenJS();
      pptx.layout = "LAYOUT_WIDE";
      pptx.author = "Pretty HTML PPT";
      pptx.company = "Pretty HTML PPT";
      pptx.subject = editableText ? "HTML deck with editable main text" : "High-fidelity HTML deck export";
      pptx.title = document.title || "Pretty HTML PPT";
      pptx.lang = document.documentElement.lang || "zh-CN";

      for (let index = 0; index < slides.length; index += 1) {
        if (button) button.textContent = `${index + 1}/${slides.length}`;
        const source = slides[index];
        const rect = source.getBoundingClientRect();
        const box = fittedSlideBox(rect);
        const editable = editableText ? textCandidates(source) : [];
        const entries = editable.map((element) => textEntry(element, rect, box)).filter((entry) => entry.text);
        editable.forEach((element) => element.classList.add("xs-pptx-text-hidden"));
        let image;
        try {
          image = await captureSlide(source, rect);
        } finally {
          editable.forEach((element) => element.classList.remove("xs-pptx-text-hidden"));
        }
        const target = pptx.addSlide();
        target.background = { color: "FFFFFF" };
        target.addImage({ data: image, x: box.x, y: box.y, w: box.width, h: box.height });
        entries.forEach((entry) => target.addText(entry.text, entry.options));
        const notes = noteFor(source);
        if (notes) target.addNotes(notes);
      }

      if (button) button.textContent = "生成文件";
      await pptx.writeFile({ fileName: safeFilename(editableText), compression: true });
      toast(editableText ? "已导出可编辑文本 PPTX" : "已导出高保真 PPTX");
    } catch (error) {
      console.error("Pretty HTML PPT PPTX export failed", error);
      toast("导出失败，请检查本地图片或字体后重试");
    } finally {
      document.body.classList.remove("xs-pptx-exporting");
      exporting = false;
      if (button) {
        button.disabled = false;
        button.textContent = originalLabel;
      }
    }
  }

  function buildToolbar() {
    if (document.querySelector(".xs-pptx-toolbar")) return;
    const toolbar = document.createElement("div");
    toolbar.className = "xs-pptx-toolbar";
    toolbar.setAttribute("data-no-edit", "true");
    toolbar.innerHTML = [
      '<button type="button" data-xs-pptx-toggle aria-expanded="false">PPTX 导出</button>',
      '<div class="xs-pptx-actions">',
      '  <button type="button" data-xs-pptx-fidelity>高保真 PPTX</button>',
      '  <button type="button" data-xs-pptx-editable>可编辑文本 PPTX</button>',
      '</div>',
    ].join("");
    document.body.appendChild(toolbar);
    toolbar.querySelector("[data-xs-pptx-toggle]").addEventListener("click", (event) => {
      const open = toolbar.classList.toggle("is-open");
      event.currentTarget.setAttribute("aria-expanded", String(open));
    });
    toolbar.querySelector("[data-xs-pptx-fidelity]").addEventListener("click", () => exportPptx(false));
    toolbar.querySelector("[data-xs-pptx-editable]").addEventListener("click", () => exportPptx(true));
  }

  window.PrettyHtmlPptExport = { highFidelity: () => exportPptx(false), editableText: () => exportPptx(true) };
  buildToolbar();
})();
