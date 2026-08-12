(() => {
  const root = document.documentElement;
  const state = {
    open: false,
    index: 0,
    startedAt: 0,
    elapsedBeforeStart: 0,
    running: false,
    fullscreen: false,
    detached: false,
    presenterRefresh: null,
    talkTimerTick: null,
  };
  let presenterWindow = null;

  const slideSelector = document.querySelector("[data-slide]")
    ? "[data-slide]"
    : "section[id], header[id], article[id]";
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
      .shui-presenter-overlay.is-detached { display: none !important; }
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
          <button type="button" data-shui-presenter-popout>独立窗口</button>
          <button type="button" data-shui-presenter-fullscreen>全屏放映</button>
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
    overlay.querySelector("[data-shui-presenter-popout]").addEventListener("click", openPresenterWindow);
    overlay.querySelector("[data-shui-presenter-fullscreen]").addEventListener("click", startFullscreenPresentation);
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
      updateNotes(event.currentTarget.textContent);
    });
  }

  function updateNotes(value) {
    ensureNotesElement(slides[state.index]).textContent = value;
    renderPresenterWindow();
  }

  function presenterWindowMarkup() {
    return [
      '<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8">',
      '<meta name="viewport" content="width=device-width,initial-scale=1.0">',
      '<title>Pretty HTML PPT · 演讲者窗口</title><style>',
      ':root{color-scheme:dark;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif}',
      '*{box-sizing:border-box}body{margin:0;min-height:100vh;background:#171717;color:#f8fafc}',
      '.app{display:grid;grid-template-rows:auto auto minmax(0,1fr) auto;min-height:100vh}',
      'header{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:15px 18px;border-bottom:1px solid #343434;background:#202020}',
      'header strong{font-size:14px}.hint{margin-top:3px;color:#a3a3a3;font-size:12px}',
      '.actions{display:flex;gap:8px;flex-wrap:wrap}.actions button,.timer-actions button{border:1px solid #4a4a4a;border-radius:6px;background:#292929;color:#fff;padding:7px 10px;font-weight:700;cursor:pointer}',
      '.actions button:hover,.timer-actions button:hover{background:#373737}',
      '.section{padding:18px;border-bottom:1px solid #343434}.label{margin:0 0 8px;color:#a3a3a3;font-size:11px;font-weight:800;letter-spacing:.09em}',
      '.next{margin:0;font-size:24px;line-height:1.2}.notes-wrap{min-height:0;display:grid;grid-template-rows:auto minmax(0,1fr)}',
      '.notes-wrap .label{padding:16px 18px 0}.notes{min-height:0;overflow:auto;padding:10px 18px 18px;font-size:18px;line-height:1.65;white-space:pre-wrap;outline:none}',
      '.notes:focus{background:#1f1f1f}.footer{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:#343434}',
      '.metric{padding:14px 16px;background:#202020}.metric span{display:block;color:#a3a3a3;font-size:11px;font-weight:800;letter-spacing:.08em}.metric b{display:block;margin-top:5px;font-size:20px}',
      '.timer-actions{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}.timer-actions button{padding:5px 8px;font-size:12px}',
      '</style></head><body><main class="app"><header><div><strong>演讲者窗口</strong><div class="hint">把主窗口投到大屏，这个窗口留在自己的屏幕</div></div><div class="actions">',
      '<button type="button" onclick="window.opener.__shuiPrettyPresenter.control(\'prev\')">上一页</button>',
      '<button type="button" onclick="window.opener.__shuiPrettyPresenter.control(\'next\')">下一页</button>',
      '<button type="button" onclick="window.opener.__shuiPrettyPresenter.control(\'fullscreen\')">主窗口全屏</button>',
      '<button type="button" onclick="window.opener.__shuiPrettyPresenter.control(\'close\')">结束</button>',
      '</div></header><section class="section"><p class="label">下一页</p><p class="next" data-presenter-next></p></section>',
      '<section class="notes-wrap"><p class="label">本页演讲稿</p><div class="notes" data-presenter-notes contenteditable="true" spellcheck="false"></div></section>',
      '<footer class="footer"><div class="metric"><span>页码</span><b data-presenter-count></b></div><div class="metric"><span>计时</span><b data-presenter-timer>00:00</b><div class="timer-actions">',
      '<button type="button" onclick="window.opener.__shuiPrettyPresenter.control(\'start\')">开始</button>',
      '<button type="button" onclick="window.opener.__shuiPrettyPresenter.control(\'pause\')">暂停</button>',
      '<button type="button" onclick="window.opener.__shuiPrettyPresenter.control(\'reset\')">重置</button>',
      '</div></div></footer></main><script>document.querySelector("[data-presenter-notes]").addEventListener("input",function(){window.opener.__shuiPrettyPresenter.notes(this.textContent)})</scr' + 'ipt></body></html>'
    ].join("");
  }

  function renderPresenterWindow() {
    if (!presenterWindow || presenterWindow.closed) {
      presenterWindow = null;
      if (state.detached) close();
      return false;
    }
    const doc = presenterWindow.document;
    const current = slides[state.index];
    const next = slides[Math.min(slides.length - 1, state.index + 1)];
    doc.title = `演讲者窗口 · ${titleOf(current)}`;
    doc.querySelector("[data-presenter-next]").textContent =
      next === current ? "演讲结束" : titleOf(next);
    const notes = doc.querySelector("[data-presenter-notes]");
    if (doc.activeElement !== notes) notes.textContent = notesOf(current);
    doc.querySelector("[data-presenter-count]").textContent = `${state.index + 1}/${slides.length}`;
    doc.querySelector("[data-presenter-timer]").textContent = timerText();
    return true;
  }

  function openPresenterWindow() {
    if (!presenterWindow || presenterWindow.closed) {
      presenterWindow = window.open(
        "",
        "pretty-html-ppt-presenter",
        "popup=yes,width=480,height=760,resizable=yes"
      );
      if (!presenterWindow) {
        window.alert("浏览器拦截了演讲者窗口，请允许此页面打开弹窗后再试。");
        return false;
      }
      presenterWindow.document.open();
      presenterWindow.document.write(presenterWindowMarkup());
      presenterWindow.document.close();
    }
    state.detached = true;
    document.querySelector(".shui-presenter-overlay")?.classList.add("is-detached");
    root.classList.remove("shui-presenter-is-open");
    renderPresenterWindow();
    presenterWindow.focus();
    return true;
  }

  function startFullscreenPresentation() {
    state.fullscreen = true;
    document.querySelector(".shui-presenter-overlay")?.classList.add("is-detached");
    root.classList.remove("shui-presenter-is-open");
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen?.().catch(() => {
        state.fullscreen = false;
        if (!state.detached) {
          document.querySelector(".shui-presenter-overlay")?.classList.remove("is-detached");
          root.classList.add("shui-presenter-is-open");
        }
      });
    }
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
    renderPresenterWindow();
  }

  function open() {
    ensureStyles();
    ensureDom();
    state.open = true;
    state.detached = false;
    document.querySelector(".shui-presenter-overlay").classList.remove("is-detached");
    document.querySelector(".shui-presenter-overlay").classList.add("is-open");
    root.classList.add("shui-presenter-is-open");
    update();
    clearInterval(state.presenterRefresh);
    state.presenterRefresh = setInterval(update, 1000);
  }

  function close() {
    const wasFullscreen = state.fullscreen;
    state.fullscreen = false;
    state.detached = false;
    state.open = false;
    document.querySelector(".shui-presenter-overlay")?.classList.remove("is-open", "is-detached");
    root.classList.remove("shui-presenter-is-open");
    if (presenterWindow && !presenterWindow.closed) presenterWindow.close();
    presenterWindow = null;
    clearInterval(state.presenterRefresh);
    state.presenterRefresh = null;
    if (wasFullscreen && document.fullscreenElement) {
      document.exitFullscreen?.().catch(() => {});
    }
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

  document.addEventListener("fullscreenchange", () => {
    if (document.fullscreenElement || !state.fullscreen) return;
    state.fullscreen = false;
    if (state.open && !state.detached) {
      document.querySelector(".shui-presenter-overlay")?.classList.remove("is-detached");
      root.classList.add("shui-presenter-is-open");
    }
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
  window.__shuiPrettyPresenter = {
    control(action) {
      const actions = {
        prev: () => move(-1),
        next: () => move(1),
        start: () => { startTimer(); update(); },
        pause: () => { pauseTimer(); update(); },
        reset: () => { resetTimer(); update(); },
        fullscreen: startFullscreenPresentation,
        close,
      };
      actions[action]?.();
    },
    notes: updateNotes,
  };
  ensureDom();
})();
