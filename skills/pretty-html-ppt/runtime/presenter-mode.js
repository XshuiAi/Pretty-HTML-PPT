(() => {
  const root = document.documentElement;
  const state = {
    open: false,
    index: 0,
    startedAt: 0,
    elapsedBeforeStart: 0,
    running: false,
    presenterRefresh: null,
    talkTimerTick: null,
  };

  const slideSelector = "[data-slide], section[id], header[id], article[id]";
  const slides = [...document.querySelectorAll(slideSelector)]
    .filter((slide) => !slide.closest(".shui-presenter-overlay"))
    .filter((slide) => {
      const rect = slide.getBoundingClientRect();
      return rect.width > 0 && rect.height > 0;
    });

  if (!slides.length || window.__shuiPresenterModeLoaded) return;
  window.__shuiPresenterModeLoaded = true;

  function titleOf(slide) {
    const title = slide.querySelector("[data-slide-title], h1, h2, h3");
    return (title?.textContent || slide.getAttribute("aria-label") || "Untitled slide").trim();
  }

  function summaryOf(slide) {
    const explicit = slide.querySelector("[data-slide-summary]");
    if (explicit) return explicit.textContent.trim();
    const copy = slide.querySelector("p, li");
    return (copy?.textContent || "").trim();
  }

  function notesOf(slide) {
    const notes = notesElement(slide);
    return (notes?.textContent || "No speaker notes for this slide.").trim();
  }

  function notesElement(slide) {
    return slide.querySelector("[data-speaker-notes], .speaker-notes");
  }

  function ensureNotesElement(slide) {
    let notes = notesElement(slide);
    if (!notes) {
      notes = document.createElement("aside");
      notes.className = "speaker-notes";
      slide.appendChild(notes);
    }
    return notes;
  }

  function formatTime(ms) {
    const total = Math.max(0, Math.floor(ms / 1000));
    const minutes = String(Math.floor(total / 60)).padStart(2, "0");
    const seconds = String(total % 60).padStart(2, "0");
    return `${minutes}:${seconds}`;
  }

  function elapsedMs() {
    return state.elapsedBeforeStart + (state.running ? Date.now() - state.startedAt : 0);
  }

  function renderTalkTimer() {
    const text = formatTime(elapsedMs());
    document.querySelectorAll("[data-shui-talk-timer-display], [data-shui-presenter-timer]")
      .forEach((node) => { node.textContent = text; });
    document.querySelectorAll("[data-shui-talk-timer]")
      .forEach((node) => node.classList.toggle("is-running", state.running));
    document.dispatchEvent(new CustomEvent("shui-talk-timer:update", {
      detail: { elapsed: elapsedMs(), running: state.running, text },
    }));
  }

  const internalDeckTimer = {
    start() {
      if (state.running) return;
      state.running = true;
      state.startedAt = Date.now();
      clearInterval(state.talkTimerTick);
      state.talkTimerTick = setInterval(renderTalkTimer, 250);
      renderTalkTimer();
    },
    pause() {
      if (!state.running) return;
      state.elapsedBeforeStart = elapsedMs();
      state.running = false;
      clearInterval(state.talkTimerTick);
      state.talkTimerTick = null;
      renderTalkTimer();
    },
    reset() {
      state.elapsedBeforeStart = 0;
      state.startedAt = state.running ? Date.now() : 0;
      renderTalkTimer();
    },
    elapsed: elapsedMs,
    isRunning: () => state.running,
    format: formatTime,
    render: renderTalkTimer,
  };

  function deckTimer() {
    return window.ShuiDeckTimer || internalDeckTimer;
  }

  function timerText() {
    const external = deckTimer();
    if (external?.elapsed) {
      const elapsed = external.elapsed();
      return external.format ? external.format(elapsed) : formatTime(elapsed);
    }
    return formatTime(elapsedMs());
  }

  function startTimer() {
    const external = deckTimer();
    if (external?.start) {
      external.start();
      return;
    }
    if (state.running) return;
    state.running = true;
    state.startedAt = Date.now();
  }

  function pauseTimer() {
    const external = deckTimer();
    if (external?.pause) {
      external.pause();
      return;
    }
    if (!state.running) return;
    state.elapsedBeforeStart = elapsedMs();
    state.running = false;
  }

  function resetTimer() {
    const external = deckTimer();
    if (external?.reset) {
      external.reset();
      return;
    }
    state.elapsedBeforeStart = 0;
    state.startedAt = state.running ? Date.now() : 0;
  }

  function ensureStyles() {
    if (document.getElementById("shui-presenter-style")) return;
    const style = document.createElement("style");
    style.id = "shui-presenter-style";
    style.textContent = `
      .speaker-notes, [data-speaker-notes] { display: none !important; }
      .shui-presenter-overlay {
        position: fixed;
        inset: 0;
        z-index: 2147483600;
        display: none;
        grid-template-rows: auto minmax(0, 1fr);
        background: #111;
        color: #f8fafc;
        font: 14px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }
      .shui-presenter-overlay.is-open { display: grid; }
      .shui-presenter-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        padding: 12px 16px;
        border-bottom: 1px solid rgba(255, 255, 255, .14);
        background: rgba(255, 255, 255, .06);
      }
      .shui-presenter-topbar strong { font-size: 13px; letter-spacing: .04em; text-transform: uppercase; }
      .shui-presenter-actions { display: flex; align-items: center; gap: 8px; }
      .shui-presenter-actions button {
        border: 1px solid rgba(255, 255, 255, .22);
        background: rgba(255, 255, 255, .08);
        color: #fff;
        padding: 7px 10px;
        border-radius: 4px;
        cursor: pointer;
      }
      .shui-presenter-actions button:hover { background: rgba(255, 255, 255, .16); }
      .shui-presenter-grid {
        display: grid;
        grid-template-columns: minmax(0, 1.15fr) minmax(320px, .85fr);
        gap: 14px;
        min-height: 0;
        padding: 14px;
      }
      .shui-presenter-panel {
        min-width: 0;
        min-height: 0;
        border: 1px solid rgba(255, 255, 255, .14);
        background: rgba(255, 255, 255, .06);
        overflow: hidden;
      }
      .shui-presenter-current {
        display: flex;
        flex-direction: column;
      }
      .shui-presenter-preview-frame {
        flex: 1;
        min-height: 0;
        display: grid;
        place-items: center;
        padding: 20px;
      }
      .shui-presenter-card {
        width: min(760px, 100%);
        aspect-ratio: 16 / 9;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 48px;
        border: 1px solid rgba(255, 255, 255, .2);
        background: #fff;
        color: #111827;
        box-shadow: 0 30px 80px rgba(0, 0, 0, .35);
      }
      .shui-presenter-card h2 {
        margin: 0;
        font-size: clamp(30px, 4vw, 56px);
        line-height: 1.02;
      }
      .shui-presenter-card p {
        max-width: 680px;
        margin: 18px 0 0;
        color: #4b5563;
        font-size: clamp(15px, 1.6vw, 20px);
      }
      .shui-presenter-sidebar {
        display: grid;
        grid-template-rows: auto minmax(0, 1fr) auto;
      }
      .shui-presenter-section {
        padding: 18px;
        border-bottom: 1px solid rgba(255, 255, 255, .12);
      }
      .shui-presenter-section h3 {
        margin: 0 0 10px;
        color: rgba(255, 255, 255, .62);
        font-size: 12px;
        letter-spacing: .08em;
        text-transform: uppercase;
      }
      .shui-presenter-next-title {
        margin: 0;
        color: #fff;
        font-size: 22px;
        line-height: 1.18;
      }
      .shui-presenter-notes {
        min-height: 0;
        overflow: auto;
        color: #f8fafc;
        font-size: 20px;
        line-height: 1.55;
      }
      [data-shui-presenter-notes] {
        min-height: 160px;
        padding: 10px 12px;
        border: 1px solid transparent;
        border-radius: 4px;
        white-space: pre-wrap;
      }
      [data-shui-presenter-notes]:focus {
        outline: none;
        border-color: rgba(255, 255, 255, .28);
        background: rgba(255, 255, 255, .08);
      }
      .shui-presenter-meta {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 8px;
        padding: 14px 18px;
      }
      .shui-presenter-meta div {
        padding: 10px;
        background: rgba(255, 255, 255, .08);
      }
      .shui-presenter-meta span {
        display: block;
        color: rgba(255, 255, 255, .58);
        font-size: 11px;
        letter-spacing: .06em;
        text-transform: uppercase;
      }
      .shui-presenter-meta b {
        display: block;
        margin-top: 4px;
        font-size: 18px;
      }
      .shui-presenter-timer-controls {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 8px;
      }
      .shui-presenter-timer-controls button {
        border: 1px solid rgba(255, 255, 255, .2);
        border-radius: 999px;
        background: rgba(255, 255, 255, .08);
        color: #fff;
        padding: 5px 8px;
        font: 700 11px/1 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        cursor: pointer;
      }
      .shui-presenter-timer-controls button:hover { background: rgba(255, 255, 255, .16); }
      .shui-talk-timer-dock {
        position: fixed;
        right: 18px;
        bottom: 82px;
        z-index: 2147483500;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 8px;
        color: var(--ink, #111827);
        font: 13px/1.3 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }
      .shui-talk-timer-trigger,
      .shui-talk-timer-controls button {
        appearance: none;
        border: 1px solid var(--line, rgba(17, 24, 39, .18));
        background: var(--surface, rgba(255, 255, 255, .96));
        color: var(--ink, #111827);
        cursor: pointer;
      }
      .shui-talk-timer-trigger {
        min-width: 58px;
        padding: 9px 12px;
        border-radius: 999px;
        box-shadow: 0 10px 30px rgba(17, 24, 39, .12);
        font-weight: 800;
      }
      .shui-talk-timer-panel {
        display: none;
        width: 218px;
        padding: 14px;
        border: 1px solid var(--line, rgba(17, 24, 39, .18));
        border-radius: 8px;
        background: var(--surface, rgba(255, 255, 255, .98));
        box-shadow: 0 18px 50px rgba(17, 24, 39, .14);
      }
      .shui-talk-timer-dock.is-open .shui-talk-timer-panel { display: block; }
      .shui-talk-timer-heading {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        color: var(--muted, #6b7280);
        font-size: 11px;
        font-weight: 800;
      }
      .shui-talk-timer-time {
        display: block;
        margin-top: 7px;
        font-size: 34px;
        font-weight: 850;
        line-height: 1;
        letter-spacing: 0;
      }
      .shui-talk-timer-controls {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 6px;
        margin-top: 12px;
      }
      .shui-talk-timer-controls button {
        min-height: 30px;
        padding: 6px 7px;
        border-radius: 4px;
        font: 750 11px/1 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }
      .shui-talk-timer-controls [data-shui-talk-timer-start] {
        border-color: var(--pink, var(--accent, #111827));
        background: var(--pink, var(--accent, #111827));
        color: #fff;
      }
      .shui-talk-timer-dock.is-running [data-shui-talk-timer-start] { opacity: .56; }
      .shui-presenter-is-open .shui-talk-timer-dock { display: none; }
      @media (max-width: 860px) {
        .shui-presenter-grid { grid-template-columns: 1fr; }
        .shui-presenter-sidebar { grid-template-rows: auto auto auto; }
        .shui-presenter-notes { max-height: 220px; }
        .shui-talk-timer-dock { right: 12px; bottom: 72px; }
      }
      @media print {
        .shui-presenter-overlay,
        .shui-talk-timer-dock { display: none !important; }
      }
    `;
    document.head.appendChild(style);
  }

  function ensureTimerDom() {
    if (document.querySelector("[data-shui-talk-timer]")) return;
    const dock = document.createElement("div");
    dock.className = "shui-talk-timer-dock";
    dock.setAttribute("data-shui-talk-timer", "true");
    dock.setAttribute("data-no-edit", "true");
    dock.innerHTML = `
      <button class="shui-talk-timer-trigger" type="button" data-shui-talk-timer-toggle aria-expanded="false">计时</button>
      <div class="shui-talk-timer-panel" role="group" aria-label="演讲计时">
        <div class="shui-talk-timer-heading"><span>演讲计时</span><span>Talk Timer</span></div>
        <strong class="shui-talk-timer-time" data-shui-talk-timer-display>00:00</strong>
        <div class="shui-talk-timer-controls">
          <button type="button" data-shui-talk-timer-start>开始</button>
          <button type="button" data-shui-talk-timer-pause>暂停</button>
          <button type="button" data-shui-talk-timer-reset>重置</button>
        </div>
      </div>
    `;
    document.body.appendChild(dock);
    dock.querySelector("[data-shui-talk-timer-toggle]").addEventListener("click", (event) => {
      const open = !dock.classList.contains("is-open");
      dock.classList.toggle("is-open", open);
      event.currentTarget.setAttribute("aria-expanded", String(open));
    });
    dock.querySelector("[data-shui-talk-timer-start]").addEventListener("click", startTimer);
    dock.querySelector("[data-shui-talk-timer-pause]").addEventListener("click", pauseTimer);
    dock.querySelector("[data-shui-talk-timer-reset]").addEventListener("click", resetTimer);
    renderTalkTimer();
  }

  function ensureDom() {
    ensureTimerDom();
    if (document.querySelector(".shui-presenter-overlay")) return;

    const overlay = document.createElement("div");
    overlay.className = "shui-presenter-overlay";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Presenter mode");
    overlay.setAttribute("data-no-edit", "true");
    overlay.innerHTML = `
      <div class="shui-presenter-topbar">
        <strong>Presenter Mode</strong>
        <div class="shui-presenter-actions">
          <button type="button" data-shui-presenter-prev>Prev</button>
          <button type="button" data-shui-presenter-next>Next</button>
          <button type="button" data-shui-presenter-close>Close</button>
        </div>
      </div>
      <div class="shui-presenter-grid">
        <div class="shui-presenter-panel shui-presenter-current">
          <div class="shui-presenter-preview-frame">
            <div class="shui-presenter-card">
              <h2 data-shui-presenter-title></h2>
              <p data-shui-presenter-summary></p>
            </div>
          </div>
        </div>
        <aside class="shui-presenter-panel shui-presenter-sidebar">
          <div class="shui-presenter-section">
            <h3>Next</h3>
            <p class="shui-presenter-next-title" data-shui-presenter-next-title></p>
          </div>
          <div class="shui-presenter-section shui-presenter-notes">
            <h3>Speaker Notes</h3>
            <div data-shui-presenter-notes contenteditable="true" spellcheck="false"></div>
          </div>
          <div class="shui-presenter-meta">
            <div><span>Slide</span><b data-shui-presenter-count></b></div>
            <div>
              <span>Talk Timer</span>
              <b data-shui-presenter-timer>00:00</b>
              <div class="shui-presenter-timer-controls">
                <button type="button" data-shui-presenter-timer-start>Start</button>
                <button type="button" data-shui-presenter-timer-pause>Pause</button>
                <button type="button" data-shui-presenter-timer-reset>Reset</button>
              </div>
            </div>
            <div><span>Shortcut</span><b>P / Esc</b></div>
          </div>
        </aside>
      </div>
    `;
    document.body.appendChild(overlay);

    overlay.querySelector("[data-shui-presenter-close]").addEventListener("click", close);
    overlay.querySelector("[data-shui-presenter-prev]").addEventListener("click", () => move(-1));
    overlay.querySelector("[data-shui-presenter-next]").addEventListener("click", () => move(1));
    overlay.querySelector("[data-shui-presenter-timer-start]").addEventListener("click", () => {
      startTimer();
      update();
    });
    overlay.querySelector("[data-shui-presenter-timer-pause]").addEventListener("click", () => {
      pauseTimer();
      update();
    });
    overlay.querySelector("[data-shui-presenter-timer-reset]").addEventListener("click", () => {
      resetTimer();
      update();
    });
    overlay.querySelector("[data-shui-presenter-notes]").addEventListener("input", (event) => {
      ensureNotesElement(slides[state.index]).textContent = event.currentTarget.textContent;
    });
  }

  function update() {
    const overlay = document.querySelector(".shui-presenter-overlay");
    if (!overlay) return;
    const current = slides[state.index];
    const next = slides[Math.min(slides.length - 1, state.index + 1)];

    overlay.querySelector("[data-shui-presenter-title]").textContent = titleOf(current);
    overlay.querySelector("[data-shui-presenter-summary]").textContent = summaryOf(current);
    overlay.querySelector("[data-shui-presenter-next-title]").textContent =
      next === current ? "End of deck" : titleOf(next);
    const notesTarget = overlay.querySelector("[data-shui-presenter-notes]");
    if (document.activeElement !== notesTarget) {
      notesTarget.textContent = notesOf(current);
    }
    overlay.querySelector("[data-shui-presenter-count]").textContent =
      `${state.index + 1}/${slides.length}`;
    overlay.querySelector("[data-shui-presenter-timer]").textContent =
      timerText();
  }

  function open() {
    ensureStyles();
    ensureDom();
    state.open = true;
    document.querySelector(".shui-presenter-overlay").classList.add("is-open");
    root.classList.add("shui-presenter-is-open");
    update();
    clearInterval(state.presenterRefresh);
    state.presenterRefresh = setInterval(update, 1000);
  }

  function close() {
    state.open = false;
    document.querySelector(".shui-presenter-overlay")?.classList.remove("is-open");
    root.classList.remove("shui-presenter-is-open");
    clearInterval(state.presenterRefresh);
    state.presenterRefresh = null;
  }

  function toggle() {
    state.open ? close() : open();
  }

  function move(delta) {
    state.index = Math.max(0, Math.min(slides.length - 1, state.index + delta));
    slides[state.index].scrollIntoView({ behavior: "smooth", block: "start" });
    update();
  }

  function visibleIndex() {
    let best = 0;
    let bestDistance = Infinity;
    slides.forEach((slide, index) => {
      const distance = Math.abs(slide.getBoundingClientRect().top);
      if (distance < bestDistance) {
        bestDistance = distance;
        best = index;
      }
    });
    return best;
  }

  window.addEventListener("scroll", () => {
    if (state.open) return;
    state.index = visibleIndex();
  }, { passive: true });

  document.addEventListener("shui-talk-timer:update", () => {
    if (state.open) update();
  });

  document.addEventListener("keydown", (event) => {
    const key = event.key.toLowerCase();
    const tag = document.activeElement?.tagName?.toLowerCase();
    if (tag === "input" || tag === "textarea" || document.activeElement?.isContentEditable) return;

    if (key === "p" && !event.metaKey && !event.ctrlKey && !event.altKey) {
      event.preventDefault();
      state.index = visibleIndex();
      toggle();
    }
    if (key === "escape" && state.open) {
      event.preventDefault();
      close();
    }
    if (state.open && (key === "arrowright" || key === "pagedown")) {
      event.preventDefault();
      move(1);
    }
    if (state.open && (key === "arrowleft" || key === "pageup")) {
      event.preventDefault();
      move(-1);
    }
  });

  ensureStyles();
  if (!window.ShuiDeckTimer) window.ShuiDeckTimer = internalDeckTimer;
  ensureDom();
})();
