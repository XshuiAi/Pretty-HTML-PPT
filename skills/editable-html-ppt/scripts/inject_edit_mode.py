#!/usr/bin/env python3
"""Inject Editable HTML PPT browser edit mode into an existing HTML deck.

Enhanced edition — supports text editing on all visible elements,
image / video replacement, and insert-new-media via the toolbar.
"""

from __future__ import annotations

import argparse
from pathlib import Path


START = "<!-- EDITABLE_HTML_PPT_EDIT_MODE_START -->"
END = "<!-- EDITABLE_HTML_PPT_EDIT_MODE_END -->"
LEGACY_START = "<!-- PRETTY_HTML_PPT_EDIT_MODE_START -->"
LEGACY_END = "<!-- PRETTY_HTML_PPT_EDIT_MODE_END -->"
PPTX_VENDOR_PLACEHOLDER = "__EDITABLE_HTML_PPT_PPTX_VENDOR__"

SNIPPET = r'''
<!-- EDITABLE_HTML_PPT_EDIT_MODE_START -->
__EDITABLE_HTML_PPT_PPTX_VENDOR__
<style id="editable-html-ppt-edit-style">
  .xs-edit-toolbar {
    position: fixed;
    z-index: 2147483647;
    top: 14px;
    right: 14px;
    display: grid;
    gap: 8px;
    padding: 10px;
    border-radius: 12px;
    border: 1px solid rgba(17, 24, 39, 0.14);
    background: rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(14px);
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.16);
    color: #111827;
    font: 12px/1.3 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
  }
  .xs-edit-toolbar:not(.xs-collapsed) {
    top: 58px;
    width: min(356px, calc(100vw - 28px));
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    grid-template-areas:
      "header"
      "type"
      "actions"
      "output";
    align-items: stretch;
    gap: 4px;
    padding: 7px;
  }
  .xs-edit-toolbar:not(.xs-collapsed).xs-toast-active {
    top: var(--xs-toast-offset, 58px);
  }
  .xs-edit-toolbar.xs-collapsed {
    padding: 0;
    border: 0;
    background: transparent;
    box-shadow: none;
    backdrop-filter: none;
  }
  .xs-edit-toolbar.xs-collapsed .xs-toolbar-header {
    gap: 0;
    padding: 0;
    border: 0;
  }
  .xs-edit-toolbar.xs-collapsed > :not(.xs-toolbar-header) {
    display: none !important;
  }
  .xs-edit-toolbar.xs-collapsed .xs-toolbar-session > :not([data-xs-edit-toggle]) { display: none !important; }
  .xs-edit-toolbar button {
    appearance: none;
    border: 1px solid rgba(17, 24, 39, 0.16);
    background: #fff;
    color: #111827;
    padding: 4px 6px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
    transition: background 120ms ease, transform 120ms ease;
  }
  .xs-edit-toolbar button:hover { background: #f3f4f6; transform: translateY(-1px); }
  .xs-edit-toolbar .xs-history-button {
    min-width: 32px;
    padding: 4px 8px;
    font-size: 18px;
    line-height: 1;
  }
  .xs-edit-toolbar button.xs-active {
    background: #111827;
    color: #fff;
    border-color: #111827;
  }
  .xs-edit-toolbar.xs-collapsed [data-xs-edit-toggle] {
    min-width: 58px;
    min-height: 38px;
    padding: 9px 12px;
    border-radius: 999px;
    box-shadow: 0 8px 22px rgba(17, 24, 39, 0.12);
    font-weight: 800;
  }
  .xs-toolbar-group {
    display: flex;
    align-items: center;
    min-width: 0;
    gap: 5px;
  }
  .xs-toolbar-header {
    grid-area: header;
    display: flex;
    align-items: center;
    min-width: 0;
    gap: 4px;
    padding-bottom: 4px;
    border-bottom: 1px solid rgba(17, 24, 39, 0.09);
    cursor: grab;
  }
  .xs-toolbar-header:active { cursor: grabbing; }
  .xs-edit-toolbar.xs-toolbar-dragging { user-select: none; }
  .xs-toolbar-session { gap: 4px; }
  .xs-toolbar-type {
    grid-area: type;
    display: grid;
    grid-template-columns: minmax(0, 1fr) 1px minmax(0, 1fr);
    align-items: center;
    gap: 4px;
    padding: 4px 5px;
    border: 1px solid rgba(17, 24, 39, 0.09);
    border-radius: 8px;
    background: rgba(248, 250, 252, .5);
  }
  .xs-toolbar-actions,
  .xs-toolbar-output {
    flex-wrap: nowrap;
    align-content: center;
    padding: 4px 5px;
    border: 1px solid rgba(17, 24, 39, 0.09);
    border-radius: 8px;
    background: rgba(248, 250, 252, .5);
  }
  .xs-toolbar-actions { grid-area: actions; }
  .xs-toolbar-output { grid-area: output; }
  .xs-toolbar-label {
    flex: 0 0 auto;
    color: #6b7280;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .08em;
    line-height: 1;
    margin-right: 1px;
  }
  .xs-toolbar-type-divider {
    width: 1px;
    align-self: stretch;
    background: rgba(17, 24, 39, 0.12);
  }
  .xs-toolbar-group .xs-font-control { min-width: 0; }
  .xs-toolbar-output [data-xs-edit-save] { margin-right: 0; }
  @media (max-width: 460px) {
    .xs-edit-toolbar:not(.xs-collapsed) {
      width: min(356px, calc(100vw - 20px));
    }
  }
  @media (max-width: 390px) {
    .xs-toolbar-type {
      grid-template-columns: 1fr;
    }
    .xs-toolbar-type-divider { display: none; }
    .xs-toolbar-type .xs-font-control:last-child { border-top: 1px solid rgba(17, 24, 39, .09); padding-top: 6px; }
    .xs-toolbar-actions,
    .xs-toolbar-output { flex-wrap: wrap; }
    .xs-toolbar-label { flex-basis: 100%; }
  }
  .xs-edit-toolbar .xs-font-control {
    display: inline-flex;
    align-items: center;
    gap: 2px;
  }
  .xs-edit-toolbar .xs-font-control button {
    padding: 3px 5px;
  }
  .xs-edit-toolbar .xs-font-control label {
    color: #4b5563;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
  }
  .xs-edit-toolbar .xs-font-control input {
    width: 40px;
    height: 26px;
    border: 1px solid rgba(17, 24, 39, 0.16);
    border-radius: 5px;
    background: #fff;
    color: #111827;
    font: 12px/1.3 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
    text-align: center;
  }
  .xs-edit-toolbar .xs-font-control input:disabled,
  .xs-edit-toolbar button:disabled {
    opacity: .45;
    cursor: not-allowed;
    transform: none;
  }

  /* Editing highlights */
  .xs-editing [contenteditable="true"] {
    outline: 1.5px dashed rgba(37, 99, 235, 0.72) !important;
    outline-offset: 3px !important;
    cursor: text !important;
    transition: outline-color 140ms ease;
  }
  .xs-editing [contenteditable="true"]:hover {
    outline-color: rgba(37, 99, 235, 0.95) !important;
  }
  .xs-editing [contenteditable="true"]:focus {
    outline: 2px solid rgba(37, 99, 235, 0.95) !important;
    outline-offset: 4px !important;
    background: rgba(37, 99, 235, 0.03);
  }
  .xs-editing [contenteditable="true"].xs-text-frame-selected {
    outline: 2px solid rgba(255, 79, 154, 0.95) !important;
    outline-offset: 5px !important;
  }
  .xs-editing [contenteditable="true"].xs-text-frame-selected::after {
    content: "";
    position: absolute;
    right: -8px;
    bottom: -8px;
    width: 12px;
    height: 12px;
    border: 2px solid #fff;
    border-radius: 50%;
    background: #ff4f9a;
    box-shadow: 0 2px 8px rgba(17, 24, 39, .2);
    pointer-events: none;
  }
  .xs-editing [contenteditable="true"].xs-text-frame-edge {
    cursor: grab !important;
  }
  .xs-editing [contenteditable="true"].xs-text-frame-dragging {
    cursor: grabbing !important;
  }
  .xs-inserted-text {
    position: absolute;
    z-index: 81;
    min-width: 120px;
    min-height: 28px;
    margin: 0;
    padding: 4px 6px;
    color: inherit;
    outline: none;
    overflow: hidden;
  }
  .xs-editing .xs-inserted-text { background: rgba(255, 255, 255, .56); }
  .xs-object-hidden { visibility: hidden !important; pointer-events: none !important; }

  /* Media replace badges */
  .xs-media-badge {
    position: absolute;
    top: 6px;
    right: 6px;
    z-index: 100;
    display: none;
    padding: 4px 8px;
    border-radius: 4px;
    background: rgba(17, 24, 39, 0.85);
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    pointer-events: auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.22);
  }
  .xs-editing .xs-media-badge { display: block; }
  .xs-media-badge:hover { background: #111827; }

  .xs-media-wrapper {
    position: relative;
    display: inline-block;
    pointer-events: auto;
  }

  /* Inserted image canvas */
  .xs-inserted-frame {
    position: absolute;
    z-index: 60;
    display: block;
    width: min(320px, 36vw);
    min-width: 120px;
    max-width: calc(100% - 32px);
    border-radius: 10px;
    box-shadow: 0 18px 44px rgba(17, 24, 39, 0.16);
    touch-action: none;
  }
  .xs-inserted-frame img {
    display: block;
    width: 100%;
    height: auto;
    border-radius: inherit;
    pointer-events: none;
  }
  .xs-editing .xs-inserted-frame {
    outline: 1.5px dashed rgba(37, 99, 235, 0.72);
    outline-offset: 4px;
    cursor: grab;
  }
  .xs-editing .xs-inserted-frame.is-selected {
    outline: 2px solid rgba(255, 79, 154, 0.95);
    box-shadow: 0 20px 54px rgba(255, 79, 154, 0.22);
  }
  .xs-insert-controls {
    position: absolute;
    left: 50%;
    bottom: calc(100% + 8px);
    z-index: 2;
    display: none;
    gap: 4px;
    padding: 5px;
    border: 1px solid rgba(17, 24, 39, 0.14);
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.96);
    box-shadow: 0 10px 28px rgba(17, 24, 39, 0.14);
    transform: translateX(-50%);
    white-space: nowrap;
  }
  .xs-editing .xs-inserted-frame.is-selected .xs-insert-controls {
    display: inline-flex;
  }
  .xs-insert-controls button {
    appearance: none;
    border: 0;
    border-radius: 999px;
    background: transparent;
    color: #111827;
    padding: 5px 7px;
    font: 700 11px/1 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
    cursor: pointer;
  }
  .xs-insert-controls button:hover {
    background: #f3f4f6;
  }
  .xs-insert-controls button[data-xs-delete] {
    color: #b91c1c;
  }
  .xs-insert-controls button[data-xs-delete]:hover {
    background: #fee2e2;
  }
  .xs-insert-resize {
    position: absolute;
    right: -9px;
    bottom: -9px;
    z-index: 3;
    display: none;
    width: 18px;
    height: 18px;
    border: 2px solid #fff;
    border-radius: 999px;
    background: #ff4f9a;
    box-shadow: 0 4px 12px rgba(17, 24, 39, .2);
    cursor: nwse-resize;
  }
  .xs-editing .xs-inserted-frame.is-selected .xs-insert-resize {
    display: block;
  }
  .xs-snap-guide {
    position: absolute;
    z-index: 59;
    display: none;
    pointer-events: none;
    background: rgba(255, 79, 154, .72);
  }
  .xs-snap-guide.is-visible { display: block; }
  .xs-snap-guide.x { height: 1px; left: 0; right: 0; }
  .xs-snap-guide.y { width: 1px; top: 0; bottom: 0; }

  /* Toast */
  .xs-toast {
    position: fixed;
    z-index: 2147483647;
    right: 14px;
    top: 10px;
    padding: 8px 12px;
    border-radius: 6px;
    background: rgba(17, 24, 39, 0.92);
    color: #fff;
    font: 12px/1.3 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
    opacity: 0;
    transform: translateY(-6px);
    transition: opacity .2s ease, transform .2s ease;
    pointer-events: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.18);
  }
  .xs-toast.is-visible { opacity: 1; transform: translateY(0); }

  /* Media replace modal */
  .xs-modal-mask {
    position: fixed;
    inset: 0;
    z-index: 2147483647;
    display: none;
    align-items: center;
    justify-content: center;
    background: rgba(17, 24, 39, 0.55);
    backdrop-filter: blur(3px);
  }
  .xs-modal-mask.is-open { display: flex; }
  .xs-modal {
    width: min(440px, 92vw);
    padding: 24px;
    border-radius: 10px;
    background: #fff;
    box-shadow: 0 20px 48px rgba(0,0,0,0.22);
    font: 13px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
    color: #111827;
  }
  .xs-modal h3 {
    margin: 0 0 16px;
    font-size: 16px;
    font-weight: 800;
  }
  .xs-modal label {
    display: block;
    margin-bottom: 6px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #6b7280;
  }
  .xs-modal input[type="text"],
  .xs-modal input[type="url"],
  .xs-modal textarea {
    width: 100%;
    padding: 8px 10px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font: 13px/1.4 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: #111827;
    background: #f9fafb;
    transition: border-color 140ms ease;
    box-sizing: border-box;
  }
  .xs-modal input:focus,
  .xs-modal textarea:focus {
    outline: none;
    border-color: #2563eb;
    background: #fff;
  }
  .xs-modal .xs-modal-actions {
    display: flex;
    gap: 8px;
    justify-content: flex-end;
    margin-top: 18px;
  }
  .xs-modal .xs-modal-actions button {
    padding: 7px 16px;
    border-radius: 6px;
    border: 1px solid #d1d5db;
    background: #fff;
    cursor: pointer;
    font-size: 12px;
    font-weight: 700;
    transition: background 120ms ease;
  }
  .xs-modal .xs-modal-actions button:hover { background: #f3f4f6; }
  .xs-modal .xs-modal-actions button.xs-btn-primary {
    background: #111827;
    color: #fff;
    border-color: #111827;
  }
  .xs-modal .xs-modal-actions button.xs-btn-primary:hover {
    background: #1f2937;
  }
  .xs-modal .xs-file-upload {
    display: grid;
    gap: 6px;
    place-items: center;
    padding: 14px;
    border: 2px dashed #d1d5db;
    border-radius: 8px;
    text-align: center;
    cursor: pointer;
    color: #6b7280;
    font-size: 12px;
    margin-top: 8px;
    transition: border-color 140ms ease, background 140ms ease;
  }
  .xs-modal .xs-file-upload:hover,
  .xs-modal .xs-file-upload.is-dragover {
    border-color: #2563eb;
    background: #f0f4ff;
  }
  .xs-modal .xs-file-upload strong {
    color: #111827;
    font-size: 14px;
  }
  .xs-modal .xs-file-upload span {
    color: #6b7280;
    font-size: 12px;
  }
  .xs-modal details {
    margin-top: 14px;
    border-top: 1px solid #e5e7eb;
    padding-top: 12px;
  }
  .xs-modal summary {
    cursor: pointer;
    color: #374151;
    font-size: 12px;
    font-weight: 800;
  }
  .xs-modal .xs-file-upload input { display: none; }
  .xs-pptx-editable-text-hidden,
  .xs-pptx-editable-text-hidden * {
    color: transparent !important;
    -webkit-text-fill-color: transparent !important;
    text-shadow: none !important;
  }

  @media print {
    .xs-edit-toolbar, .xs-toast, .xs-media-badge, .xs-modal-mask, .xs-insert-controls, .xs-insert-resize, .xs-snap-guide { display: none !important; }
  }
</style>
<script id="editable-html-ppt-edit-script">
(() => {
  const STORE_KEY = "editable-html-ppt-edits:" + location.pathname;
  const LEGACY_STORE_KEY = "pretty-html-ppt-edits:" + location.pathname;

  /* ── Selectors ── */
  const textSelector = [
    "h1", "h2", "h3", "h4", "h5", "h6",
    "p", "li", "blockquote", "td", "th", "figcaption", "caption",
    "span", "a", "label", "strong", "em", "small", "code", "dt", "dd",
    "summary", "legend", "pre",
    "[data-editable]", ".editable", "[data-xs-inserted-text]"
  ].join(",");

  const blockedSelector = [
    "script", "style", "svg", "canvas", "video", "audio",
    "button", "nav", "input", "textarea", "select", "option",
    "[data-no-edit]", ".xs-edit-toolbar", ".xs-toast", ".xs-modal-mask",
    ".xs-media-badge", ".xs-insert-controls", ".xs-snap-guide"
  ].join(",");

  /* ── Blacklist: parent tags whose children should NOT get contenteditable ── */
  const blacklistParents = new Set(["svg", "canvas", "video", "audio", "script", "style",
    "button", "nav", "input", "textarea", "select"]);

  /* ── State ── */
  let editing = false;
  let toastTimer = null;
  let currentTextEl = null;
  let currentImageFrame = null;
  let currentVisualSelection = false;
  let insertedFrameCounter = 0;
  let insertedTextCounter = 0;
  let toolbarDrag = null;

  /* ── Helpers ── */
  function isTextNodeEmpty(el) {
    const t = (el.textContent || "").replace(/[\s ​‌‍﻿]/g, "");
    return t.length === 0;
  }
  function isOnlyChildren(el) {
    for (const child of el.children) {
      if (textSelector.split(",").some(s => child.matches(s.trim()))) return false;
    }
    return true;
  }
  function hasBlockParent(el) {
    let p = el.parentElement;
    while (p) {
      if (blacklistParents.has(p.tagName.toLowerCase())) return true;
      if (p.closest && p.closest(blockedSelector)) return true;
      p = p.parentElement;
    }
    return false;
  }

  function getTextCandidates() {
    return [...document.querySelectorAll(textSelector)]
      .filter(el => !el.closest(blockedSelector))
      .filter(el => !hasBlockParent(el))
      .filter(el => !isTextNodeEmpty(el))
      .filter(el => isOnlyChildren(el));
  }

  function isTextCandidate(el) {
    return !!el
      && el.matches?.(textSelector)
      && !el.closest(blockedSelector)
      && !hasBlockParent(el)
      && !isTextNodeEmpty(el)
      && isOnlyChildren(el);
  }

  function getMediaCandidates() {
    return [...document.querySelectorAll("img, video")]
      .filter(el => !el.closest(blockedSelector))
      .filter(el => !el.closest(".xs-media-wrapper") && !el.closest(".xs-modal-mask") && !el.closest(".xs-inserted-frame"));
  }

  /* ── ID assignment ── */
  function ensureIds() {
    getTextCandidates().forEach((el, i) => {
      if (!el.dataset.xsEditId) el.dataset.xsEditId = "t" + i;
    });
    getMediaCandidates().forEach((el, i) => {
      if (!el.dataset.xsEditId) el.dataset.xsEditId = "m" + i;
    });
  }

  /* ── Store ── */
  function readStore() {
    try {
      const raw = localStorage.getItem(STORE_KEY) || localStorage.getItem(LEGACY_STORE_KEY) || "{}";
      return JSON.parse(raw);
    } catch { return {}; }
  }
  function writeStore(data) {
    localStorage.setItem(STORE_KEY, JSON.stringify(data));
  }

  /* ── Session history ── */
  const VISUAL_STORE_KEY = "editable-html-ppt-layers:v1:" + location.pathname;
  const LEGACY_VISUAL_STORE_KEY = "pretty-html-ppt-layers:v1:" + location.pathname;
  const HISTORY_LIMIT = 50;
  const history = { entries: [], index: -1, applying: false, inputTimer: null };

  function cloneData(value) {
    return JSON.parse(JSON.stringify(value || {}));
  }

  function readVisualStore() {
    try {
      const raw = localStorage.getItem(VISUAL_STORE_KEY) || localStorage.getItem(LEGACY_VISUAL_STORE_KEY) || "{}";
      return JSON.parse(raw);
    } catch {
      return {};
    }
  }

  function collectMainState() {
    ensureIds();
    const data = {};
    getTextCandidates().forEach(el => {
      data[el.dataset.xsEditId] = textRecord(el);
    });
    getMediaCandidates().forEach(el => {
      const src = (el.tagName === "VIDEO")
        ? ((el.querySelector("source") || el).src || "")
        : el.src;
      if (src) data[el.dataset.xsEditId] = src;
    });
    data.__xsInsertedFrames = collectInsertedFrames();
    data.__xsInsertedTextFrames = collectInsertedTextFrames();
    data.__xsHiddenTextIds = collectHiddenTextIds();
    return data;
  }

  function historySnapshot() {
    return {
      main: collectMainState(),
      visual: cloneData(readVisualStore()),
    };
  }

  function sameSnapshot(left, right) {
    return JSON.stringify(left) === JSON.stringify(right);
  }

  function updateHistoryButtons() {
    const undo = document.querySelector("[data-xs-history-undo]");
    const redo = document.querySelector("[data-xs-history-redo]");
    if (undo) undo.disabled = history.index <= 0 || history.applying;
    if (redo) redo.disabled = history.index < 0 || history.index >= history.entries.length - 1 || history.applying;
  }

  function initializeHistory() {
    history.entries = [historySnapshot()];
    history.index = 0;
    updateHistoryButtons();
  }

  function commitHistory(label) {
    if (history.applying) return;
    const snapshot = historySnapshot();
    writeStore(snapshot.main);
    const current = history.entries[history.index];
    if (current && sameSnapshot(current, snapshot)) return;
    history.entries.splice(history.index + 1);
    history.entries.push(snapshot);
    if (history.entries.length > HISTORY_LIMIT) history.entries.shift();
    history.index = history.entries.length - 1;
    updateHistoryButtons();
  }

  function scheduleTextHistory() {
    if (history.applying) return;
    clearTimeout(history.inputTimer);
    history.inputTimer = setTimeout(() => commitHistory("文字修改"), 650);
  }

  function flushTextHistory() {
    if (!history.inputTimer) return;
    clearTimeout(history.inputTimer);
    history.inputTimer = null;
    commitHistory("文字修改");
  }

  function applyTextRecord(el, record) {
    const value = typeof record === "string" ? { html: record } : (record || {});
    if (value.html !== undefined) el.innerHTML = value.html;
    el.style.fontSize = value.fontSize || "";
    el.style.lineHeight = value.lineHeight || "";
    ["left", "top", "width", "height", "maxWidth", "maxHeight", "position", "display", "zIndex"].forEach(key => {
      el.style[key] = "";
    });
    applyTextFrameStyle(el, value.frame);
  }

  function applyHistorySnapshot(snapshot) {
    if (!snapshot) return;
    history.applying = true;
    clearTimeout(history.inputTimer);
    history.inputTimer = null;
    try {
      const main = cloneData(snapshot.main);
      document.querySelectorAll(".xs-inserted-frame, [data-xs-inserted-text]").forEach(node => node.remove());
      currentTextEl = null;
      ensureIds();
      getTextCandidates().forEach(el => applyTextRecord(el, main[el.dataset.xsEditId]));
      applyHiddenTextRecords(main);
      getMediaCandidates().forEach(el => {
        const value = main[el.dataset.xsEditId];
        if (!value) return;
        if (el.tagName === "IMG") el.src = value;
        else if (el.tagName === "VIDEO") {
          const source = el.querySelector("source");
          if (source) source.src = value; else el.src = value;
          el.load?.();
        }
      });
      currentImageFrame = null;
      writeStore(main);
      localStorage.setItem(VISUAL_STORE_KEY, JSON.stringify(snapshot.visual || {}));
      restoreInsertedFrames(main);
      restoreInsertedTextFrames(main);
      document.dispatchEvent(new CustomEvent("xs-edit:history-apply"));
    } finally {
      history.applying = false;
      updateHistoryButtons();
    }
  }

  function undoHistory() {
    flushTextHistory();
    if (history.index <= 0) {
      toast("没有可撤销的操作");
      return;
    }
    history.index -= 1;
    applyHistorySnapshot(history.entries[history.index]);
    toast("已撤销上一步操作");
  }

  function redoHistory() {
    flushTextHistory();
    if (history.index >= history.entries.length - 1) {
      toast("没有可恢复的操作");
      return;
    }
    history.index += 1;
    applyHistorySnapshot(history.entries[history.index]);
    toast("已恢复上一步操作");
  }

  function clearHistory() {
    clearTimeout(history.inputTimer);
    history.inputTimer = null;
    history.entries = [];
    history.index = -1;
    updateHistoryButtons();
  }

  /* ── Toast ── */
  function toast(msg) {
    let node = document.querySelector(".xs-toast");
    if (!node) {
      node = document.createElement("div");
      node.className = "xs-toast";
      document.body.appendChild(node);
    }
    node.textContent = msg;
    node.classList.add("is-visible");
    const toolbar = document.querySelector(".xs-edit-toolbar");
    if (toolbar && !toolbar.classList.contains("xs-collapsed")) {
      const gap = 12;
      const minimumTop = 10;
      const toolbarRect = toolbar.getBoundingClientRect();
      const toastTop = toolbarRect.top - node.offsetHeight - gap;
      if (toolbar.dataset.xsToolbarPositioned === "true" && toastTop >= minimumTop) {
        node.style.top = Math.round(toastTop) + "px";
      } else if (toolbar.dataset.xsToolbarPositioned === "true") {
        node.style.top = minimumTop + "px";
        if (toolbar.dataset.xsToastOriginalTop === undefined) {
          toolbar.dataset.xsToastOriginalTop = toolbar.style.top;
        }
        toolbar.style.top = Math.ceil(node.offsetHeight + gap + minimumTop) + "px";
      } else {
        node.style.removeProperty("top");
        toolbar.style.setProperty("--xs-toast-offset", Math.ceil(node.offsetHeight + gap + minimumTop) + "px");
        toolbar.classList.add("xs-toast-active");
      }
    }
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      node.classList.remove("is-visible");
      node.style.removeProperty("top");
      if (toolbar?.dataset.xsToastOriginalTop !== undefined) {
        toolbar.style.top = toolbar.dataset.xsToastOriginalTop;
        delete toolbar.dataset.xsToastOriginalTop;
      }
      toolbar?.classList.remove("xs-toast-active");
      toolbar?.style.removeProperty("--xs-toast-offset");
    }, 1800);
  }

  function nextFrameId() {
    insertedFrameCounter += 1;
    return "m" + Date.now() + "-" + insertedFrameCounter;
  }

  function nextTextBoxId() {
    insertedTextCounter += 1;
    return "it" + Date.now() + "-" + insertedTextCounter;
  }

  function textFrameStyle(el) {
    const frame = {
      left: el.style.left || "",
      top: el.style.top || "",
      width: el.style.width || "",
      height: el.style.height || "",
      maxWidth: el.style.maxWidth || "",
      maxHeight: el.style.maxHeight || "",
      position: el.style.position || "",
      display: el.style.display || "",
      zIndex: el.style.zIndex || ""
    };
    return Object.values(frame).some(Boolean) ? frame : undefined;
  }

  function applyTextFrameStyle(el, frame) {
    if (!frame || typeof frame !== "object") return;
    ["left", "top", "width", "height", "maxWidth", "maxHeight", "position", "display", "zIndex"].forEach((key) => {
      if (frame[key] !== undefined) el.style[key] = frame[key];
    });
  }

  function textRecord(el) {
    return {
      html: el.innerHTML,
      fontSize: el.style.fontSize || "",
      lineHeight: el.style.lineHeight || "",
      frame: textFrameStyle(el)
    };
  }

  function persistTextFrame(el) {
    ensureIds();
    const store = readStore();
    store[el.dataset.xsEditId] = textRecord(el);
    writeStore(store);
  }

  function collectHiddenTextIds() {
    ensureIds();
    return getTextCandidates()
      .filter(el => el.classList.contains("xs-object-hidden"))
      .map(el => el.dataset.xsEditId)
      .filter(Boolean);
  }

  function applyHiddenTextRecords(data) {
    const hiddenIds = new Set(Array.isArray(data.__xsHiddenTextIds) ? data.__xsHiddenTextIds : []);
    getTextCandidates().forEach(el => {
      const hidden = hiddenIds.has(el.dataset.xsEditId);
      el.classList.toggle("xs-object-hidden", hidden);
      if (hidden) el.setAttribute("aria-hidden", "true");
      else el.removeAttribute("aria-hidden");
    });
  }

  function hideTextObject(el) {
    if (!isTextCandidate(el)) return false;
    el.classList.add("xs-object-hidden");
    el.setAttribute("aria-hidden", "true");
    currentTextEl = null;
    updateFontControls();
    commitHistory("删除文字对象");
    toast("文字对象已删除，可用撤销恢复");
    return true;
  }

  /* ── Restore ── */
  function restoreAll() {
    const data = readStore();
    document.querySelectorAll(".xs-inserted-frame, [data-xs-inserted-text]").forEach(node => node.remove());
    currentTextEl = null;
    getTextCandidates().forEach(el => {
      const v = data[el.dataset.xsEditId];
      if (v !== undefined) {
        if (typeof v === "string") {
          el.innerHTML = v;
        } else {
          if (v.html !== undefined) el.innerHTML = v.html;
          if (v.fontSize !== undefined) el.style.fontSize = v.fontSize;
          if (v.lineHeight !== undefined) el.style.lineHeight = v.lineHeight;
          applyTextFrameStyle(el, v.frame);
        }
      }
    });
    applyHiddenTextRecords(data);
    getMediaCandidates().forEach(el => {
      const v = data[el.dataset.xsEditId];
      if (v !== undefined) {
        if (el.tagName === "IMG") el.src = v;
        else if (el.tagName === "VIDEO") {
          const srcEl = el.querySelector("source");
          if (srcEl) srcEl.src = v; else el.src = v;
        }
      }
    });
    restoreInsertedFrames(data);
    restoreInsertedTextFrames(data);
  }

  /* ── Save ── */
  function saveAll() {
    writeStore(collectMainState());
    toast("已保存到本机浏览器");
  }

  /* ── Toggle editing ── */
  function enterEdit() {
    editing = true;
    document.body.classList.add("xs-editing");
    getTextCandidates().forEach(el => {
      el.setAttribute("contenteditable", "true");
      el.setAttribute("spellcheck", "false");
    });
    attachTextFrameEvents();
    attachMediaBadges();
    updateToggleBtn();
    updateFontControls();
    toast("编辑模式已开启 — 点文字修改；拖上边框移动，拖右/下边框调整尺寸");
  }

  function exitEdit() {
    editing = false;
    document.body.classList.remove("xs-editing");
    getTextCandidates().forEach(el => {
      el.removeAttribute("contenteditable");
      el.removeAttribute("spellcheck");
      el.classList.remove("xs-text-frame-selected");
      el.classList.remove("xs-text-frame-edge");
      el.classList.remove("xs-text-frame-dragging");
    });
    removeMediaBadges();
    updateToggleBtn();
    updateFontControls();
    toast("编辑模式已关闭");
  }

  function toggleEdit(force) {
    if (typeof force === "boolean") {
      force ? enterEdit() : exitEdit();
    } else {
      editing ? exitEdit() : enterEdit();
    }
  }

  function collapseEdit() {
    if (editing) exitEdit();
    setToolbarExpanded(false);
  }

  function setToolbarExpanded(expanded) {
    const bar = document.querySelector(".xs-edit-toolbar");
    if (!bar) return;
    if (expanded) {
      bar.classList.remove("xs-collapsed");
      return;
    }
    toolbarDrag = null;
    bar.classList.add("xs-collapsed");
    bar.classList.remove("xs-toolbar-dragging", "xs-toast-active");
    delete bar.dataset.xsToolbarPositioned;
    delete bar.dataset.xsToastOriginalTop;
    bar.style.removeProperty("left");
    bar.style.removeProperty("top");
    bar.style.removeProperty("right");
    bar.style.removeProperty("--xs-toast-offset");
  }

  function clampToolbarPosition(bar, left, top) {
    const rect = bar.getBoundingClientRect();
    const margin = 8;
    return {
      left: Math.round(Math.max(margin, Math.min(left, Math.max(margin, window.innerWidth - rect.width - margin)))),
      top: Math.round(Math.max(margin, Math.min(top, Math.max(margin, window.innerHeight - rect.height - margin))))
    };
  }

  function applyToolbarPosition(bar, position) {
    if (!bar || !Number.isFinite(position?.left) || !Number.isFinite(position?.top)) return false;
    const next = clampToolbarPosition(bar, position.left, position.top);
    bar.style.right = "auto";
    bar.style.left = next.left + "px";
    bar.style.top = next.top + "px";
    bar.dataset.xsToolbarPositioned = "true";
    return true;
  }

  function resetToolbarPosition(bar) {
    delete bar.dataset.xsToolbarPositioned;
    bar.style.removeProperty("left");
    bar.style.removeProperty("top");
    bar.style.removeProperty("right");
    toast("编辑窗口已恢复默认位置");
  }

  function enableToolbarDrag(bar) {
    const header = bar.querySelector(".xs-toolbar-header");
    if (!header) return;
    header.addEventListener("pointerdown", (event) => {
      if (event.button !== 0 || event.target.closest("button, input, select, textarea, label")) return;
      const rect = bar.getBoundingClientRect();
      toolbarDrag = {
        startX: event.clientX,
        startY: event.clientY,
        left: rect.left,
        top: rect.top
      };
      bar.classList.add("xs-toolbar-dragging");
      header.setPointerCapture?.(event.pointerId);
      event.preventDefault();
    });
    header.addEventListener("pointermove", (event) => {
      if (!toolbarDrag) return;
      applyToolbarPosition(bar, {
        left: toolbarDrag.left + event.clientX - toolbarDrag.startX,
        top: toolbarDrag.top + event.clientY - toolbarDrag.startY
      });
    });
    const finishDrag = () => {
      if (!toolbarDrag) return;
      toolbarDrag = null;
      bar.classList.remove("xs-toolbar-dragging");
    };
    header.addEventListener("pointerup", finishDrag);
    header.addEventListener("pointercancel", finishDrag);
    header.addEventListener("dblclick", (event) => {
      if (!event.target.closest("button, input, select, textarea, label")) resetToolbarPosition(bar);
    });
    window.addEventListener("resize", () => {
      if (bar.dataset.xsToolbarPositioned === "true") {
        const rect = bar.getBoundingClientRect();
        applyToolbarPosition(bar, { left: rect.left, top: rect.top });
      }
    });
  }

  function updateToggleBtn() {
    const btn = document.querySelector("[data-xs-edit-toggle]");
    if (btn) {
      btn.textContent = editing ? "退出编辑" : "编辑";
      btn.classList.toggle("xs-active", editing);
    }
  }

  /* ── Font size controls ── */
  function fontTargetFromEventTarget(target) {
    const el = target?.closest?.(textSelector);
    return isTextCandidate(el) ? el : null;
  }

  function setCurrentTextEl(el) {
    if (!isTextCandidate(el)) return;
    currentTextEl = el;
    currentImageFrame = null;
    currentVisualSelection = false;
    document.dispatchEvent(new Event("xs-edit:clear-visual-selection"));
    if (editing) {
      document.querySelectorAll(".xs-text-frame-selected").forEach(item => {
        if (item !== el) item.classList.remove("xs-text-frame-selected");
      });
      el.classList.add("xs-text-frame-selected");
    }
    updateFontControls();
  }

  function prepareTextFrame(el) {
    const styles = window.getComputedStyle(el);
    if (styles.position === "static") el.style.position = "relative";
    if (styles.display === "inline") el.style.display = "inline-block";
    // A template may cap a heading with max-width. Resizing a selected frame
    // must override that visual cap instead of stopping at the template limit.
    el.style.maxWidth = "none";
    el.style.maxHeight = "none";
    el.style.zIndex = "80";
    setCurrentTextEl(el);
  }

  function textFrameEdge(el, event) {
    const rect = el.getBoundingClientRect();
    const gutter = 12;
    const nearTop = event.clientY - rect.top <= gutter;
    const nearLeft = event.clientX - rect.left <= gutter;
    const nearRight = rect.right - event.clientX <= gutter;
    const nearBottom = rect.bottom - event.clientY <= gutter;
    const isMove = nearTop && !nearLeft && !nearRight;
    const isResize = nearLeft || nearRight || nearBottom;
    return { nearLeft, nearRight, nearBottom, isMove, isResize, active: isMove || isResize };
  }

  function attachTextFrameEvents() {
    getTextCandidates().forEach((el) => {
      if (el.dataset.xsTextFrameReady === "true") return;
      el.dataset.xsTextFrameReady = "true";
      el.addEventListener("pointermove", (event) => {
        if (!editing || el.classList.contains("xs-text-frame-dragging")) return;
        el.classList.toggle("xs-text-frame-edge", textFrameEdge(el, event).active);
      });
      el.addEventListener("pointerleave", () => {
        el.classList.remove("xs-text-frame-edge");
      });
      el.addEventListener("pointerdown", (event) => {
        if (!editing || event.button !== 0) return;
        const edge = textFrameEdge(el, event);
        if (!edge.active) return;

        event.preventDefault();
        event.stopPropagation();
        prepareTextFrame(el);
        el.classList.add("xs-text-frame-dragging");
        const startX = event.clientX;
        const startY = event.clientY;
        const startLeft = Number.parseFloat(el.style.left) || 0;
        const startTop = Number.parseFloat(el.style.top) || 0;
        const rect = el.getBoundingClientRect();
        const startWidth = rect.width;
        const startHeight = rect.height;
        el.setPointerCapture?.(event.pointerId);

        const move = (moveEvent) => {
          const dx = moveEvent.clientX - startX;
          const dy = moveEvent.clientY - startY;
          if (edge.isMove) {
            el.style.left = Math.round(startLeft + dx) + "px";
            el.style.top = Math.round(startTop + dy) + "px";
            return;
          }
          if (edge.nearLeft) {
            const width = Math.max(80, startWidth - dx);
            el.style.width = Math.round(width) + "px";
            el.style.left = Math.round(startLeft + startWidth - width) + "px";
          } else if (edge.nearRight) {
            el.style.width = Math.round(Math.max(80, startWidth + dx)) + "px";
          }
          if (edge.nearBottom) {
            el.style.height = Math.round(Math.max(24, startHeight + dy)) + "px";
          }
        };
        const up = () => {
          el.removeEventListener("pointermove", move);
          el.removeEventListener("pointerup", up);
          el.removeEventListener("pointercancel", up);
          el.classList.remove("xs-text-frame-dragging");
          el.classList.remove("xs-text-frame-edge");
          persistTextFrame(el);
          commitHistory(edge.isMove ? "文本位置" : "文本框尺寸");
          toast(edge.isMove ? "文本位置已更新，导出 HTML 后会保留" : "文本框尺寸已更新，导出 HTML 后会保留");
        };
        el.addEventListener("pointermove", move);
        el.addEventListener("pointerup", up);
        el.addEventListener("pointercancel", up);
      });
      el.addEventListener("input", () => {
        if (editing) scheduleTextHistory();
      });
      el.addEventListener("blur", () => {
        flushTextHistory();
      });
    });
  }

  function getCurrentTextEl() {
    if (isTextCandidate(document.activeElement)) return document.activeElement;
    if (isTextCandidate(currentTextEl)) return currentTextEl;
    return null;
  }

  function getFontPx(el) {
    const size = window.getComputedStyle(el).fontSize;
    const value = Number.parseFloat(size);
    return Number.isFinite(value) ? Math.round(value) : 16;
  }

  function getLineHeight(el) {
    const styles = window.getComputedStyle(el);
    const fontSize = Number.parseFloat(styles.fontSize) || 16;
    const lineHeight = Number.parseFloat(styles.lineHeight);
    const value = Number.isFinite(lineHeight) ? lineHeight / fontSize : 1.2;
    return Math.round(value * 10) / 10;
  }

  function updateFontControls() {
    const input = document.querySelector("[data-xs-font-size]");
    const buttons = document.querySelectorAll("[data-xs-font-minus], [data-xs-font-plus], [data-xs-font-reset], [data-xs-line-minus], [data-xs-line-plus], [data-xs-line-reset]");
    const lineInput = document.querySelector("[data-xs-line-height]");
    const deleteObjectButton = document.querySelector("[data-xs-edit-delete-text]");
    if (!input || !lineInput) return;
    const el = getCurrentTextEl();
    input.disabled = !editing || !el;
    lineInput.disabled = !editing || !el;
    buttons.forEach(btn => { btn.disabled = !editing || !el; });
    const hasSelection = Boolean(
      currentVisualSelection
      || currentImageFrame?.isConnected
      || getCurrentTextEl()
    );
    if (deleteObjectButton) deleteObjectButton.disabled = !editing || !hasSelection;
    input.value = el ? String(getFontPx(el)) : "";
    lineInput.value = el ? String(getLineHeight(el)) : "";
  }

  function applyFontSize(px) {
    if (!editing) {
      toast("请先点击「编辑」进入编辑模式");
      return;
    }
    const el = getCurrentTextEl();
    if (!el) {
      toast("请先点选一段文字，再调整字号");
      updateFontControls();
      return;
    }
    const value = Math.max(8, Math.min(160, Math.round(px)));
    el.style.fontSize = value + "px";
    setCurrentTextEl(el);
    const store = readStore();
    store[el.dataset.xsEditId] = textRecord(el);
    writeStore(store);
    commitHistory("字号调整");
    toast("字号已调整，按 S 保存或导出 HTML");
  }

  function changeFontSize(delta) {
    const el = getCurrentTextEl();
    if (!el) {
      toast("请先点选一段文字，再调整字号");
      updateFontControls();
      return;
    }
    applyFontSize(getFontPx(el) + delta);
  }

  function resetFontSize() {
    const el = getCurrentTextEl();
    if (!el) {
      toast("请先点选一段文字，再重置字号");
      updateFontControls();
      return;
    }
    el.style.fontSize = "";
    setCurrentTextEl(el);
    const store = readStore();
    store[el.dataset.xsEditId] = textRecord(el);
    writeStore(store);
    commitHistory("字号重置");
    toast("字号已恢复为模板默认值");
  }

  function applyLineHeight(value) {
    if (!editing) {
      toast("请先点击「编辑」进入编辑模式");
      return;
    }
    const el = getCurrentTextEl();
    if (!el) {
      toast("请先点选一段文字，再调整行距");
      updateFontControls();
      return;
    }
    const normalized = Math.max(0.8, Math.min(3, Math.round(value * 10) / 10));
    el.style.lineHeight = String(normalized);
    setCurrentTextEl(el);
    const store = readStore();
    store[el.dataset.xsEditId] = textRecord(el);
    writeStore(store);
    commitHistory("行距调整");
    toast("行距已调整，按 S 保存或导出 HTML");
  }

  function changeLineHeight(delta) {
    const el = getCurrentTextEl();
    if (!el) {
      toast("请先点选一段文字，再调整行距");
      updateFontControls();
      return;
    }
    applyLineHeight(getLineHeight(el) + delta);
  }

  function resetLineHeight() {
    const el = getCurrentTextEl();
    if (!el) {
      toast("请先点选一段文字，再重置行距");
      updateFontControls();
      return;
    }
    el.style.lineHeight = "";
    setCurrentTextEl(el);
    const store = readStore();
    store[el.dataset.xsEditId] = textRecord(el);
    writeStore(store);
    commitHistory("行距重置");
    toast("行距已恢复为模板默认值");
  }

  /* ── Media badges ── */
  function attachMediaBadges() {
    getMediaCandidates().forEach(el => {
      if (el.parentElement?.classList?.contains("xs-media-wrapper")) return;
      const wrapper = document.createElement("span");
      wrapper.className = "xs-media-wrapper";
      wrapper.style.display = el.style.display || "inline-block";
      el.parentNode.insertBefore(wrapper, el);
      wrapper.appendChild(el);
      const badge = document.createElement("span");
      badge.className = "xs-media-badge";
      badge.textContent = el.tagName === "IMG" ? "替换图片" : "替换视频";
      badge.addEventListener("click", (e) => {
        e.stopPropagation();
        e.preventDefault();
        openMediaModal(el);
      });
      wrapper.appendChild(badge);
    });
  }

  function removeMediaBadges() {
    document.querySelectorAll(".xs-media-badge").forEach(b => b.remove());
    document.querySelectorAll(".xs-media-wrapper").forEach(w => {
      const parent = w.parentElement;
      while (w.firstChild) parent.insertBefore(w.firstChild, w);
      parent.removeChild(w);
    });
  }

  /* ── Media modal ── */
  function openMediaModal(el) {
    const isImg = el.tagName === "IMG";
    const currentSrc = isImg ? el.src : ((el.querySelector("source") || el).src || "");

    const mask = document.createElement("div");
    mask.className = "xs-modal-mask is-open";
    mask.innerHTML = '<div class="xs-modal">'
      + '<h3>' + (isImg ? '替换图片' : '替换视频') + '</h3>'
      + '<label>当前地址</label>'
      + '<input type="text" class="xs-current-url" value="' + escapeHtml(currentSrc) + '" readonly style="color:#6b7280;font-size:11px;">'
      + '<label style="margin-top:14px;">新地址 (URL)</label>'
      + '<input type="url" class="xs-new-url" aria-label="新媒体地址，示例 https://example.com/file.png">'
      + '<div class="xs-file-upload" id="xsFileUpload">'
      + '  或 点击上传本地文件'
      + '  <input type="file" id="xsFileInput" accept="' + (isImg ? 'image/*' : 'video/*') + '">'
      + '</div>'
      + '<div class="xs-modal-actions">'
      + '  <button class="xs-btn-cancel">取消</button>'
      + '  <button class="xs-btn-primary xs-btn-apply">确认替换</button>'
      + '</div>'
      + '</div>';
    document.body.appendChild(mask);

    const closeModal = () => { mask.remove(); };
    const apply = () => {
      const newUrl = mask.querySelector(".xs-new-url").value.trim();
      const fileInput = mask.querySelector("#xsFileInput");
      const file = fileInput.files[0];

      const doReplace = (url) => {
        if (el.tagName === "IMG") {
          el.src = url;
        } else {
          const source = el.querySelector("source");
          if (source) source.src = url; else el.src = url;
          el.load();
        }
        ensureIds();
        const store = readStore();
        store[el.dataset.xsEditId] = url;
        writeStore(store);
        commitHistory("替换媒体");
        toast("已替换，按 S 保存");
      };

      if (file) {
        const reader = new FileReader();
        reader.onload = () => doReplace(reader.result);
        reader.readAsDataURL(file);
      } else if (newUrl) {
        doReplace(newUrl);
      } else {
        toast("请输入新地址或选择文件");
        return;
      }
      closeModal();
    };

    mask.addEventListener("click", (e) => {
      if (e.target === mask) closeModal();
    });
    const fileInput = mask.querySelector("#xsFileInput");
    mask.querySelector(".xs-btn-cancel").addEventListener("click", closeModal);
    mask.querySelector(".xs-btn-apply").addEventListener("click", apply);
    mask.querySelector("#xsFileUpload").addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", () => {
      const f = fileInput.files[0];
      if (f) mask.querySelector(".xs-new-url").title = f.name;
    });
    mask.querySelector(".xs-new-url").addEventListener("keydown", (e) => {
      if (e.key === "Enter") apply();
    });
    setTimeout(() => mask.querySelector(".xs-new-url").focus(), 120);
  }

  /* ── Inserted image positioning ── */
  function slideContainers() {
    const slides = [...document.querySelectorAll("[data-slide], section[id], article[id]")]
      .filter((slide, index, all) => all.indexOf(slide) === index);
    return slides.length ? slides : [...document.querySelectorAll("main")];
  }

  function activeSlideContainer() {
    const slides = slideContainers();
    if (!slides.length) return document.body;
    const viewportCenter = window.innerHeight / 2;
    const centered = slides.find(slide => {
      const rect = slide.getBoundingClientRect();
      return rect.top <= viewportCenter && rect.bottom >= viewportCenter;
    });
    if (centered) return centered;
    return slides
      .map(slide => {
        const rect = slide.getBoundingClientRect();
        const visible = Math.max(0, Math.min(rect.bottom, window.innerHeight) - Math.max(rect.top, 0));
        return { slide, visible };
      })
      .sort((a, b) => b.visible - a.visible)[0]?.slide || slides[0];
  }

  function slideContainerFor(node) {
    return node?.closest?.("[data-slide], section[id], article[id], main")
      || activeSlideContainer()
      || document.body;
  }

  function prepareImageCanvas(container) {
    if (!container || container === document.body) return document.body;
    const style = window.getComputedStyle(container);
    if (style.position === "static") container.style.position = "relative";
    return container;
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function frameMetrics(frame) {
    const parent = frame.parentElement || document.body;
    const parentRect = parent.getBoundingClientRect();
    const rect = frame.getBoundingClientRect();
    return { parent, parentRect, rect };
  }

  function widthThatFitsParent(frame, targetWidth) {
    const img = frame.querySelector("img");
    const { parentRect } = frameMetrics(frame);
    const maxByParent = Math.max(140, parentRect.width - 56);
    let next = Math.min(targetWidth, maxByParent);
    if (img?.naturalWidth && img?.naturalHeight) {
      const maxHeight = Math.max(180, parentRect.height - 84);
      const maxByHeight = maxHeight * img.naturalWidth / img.naturalHeight;
      next = Math.min(next, Math.max(120, maxByHeight));
    }
    return Math.round(next);
  }

  function fitFrameToParent(frame) {
    const { parentRect, rect } = frameMetrics(frame);
    if (!parentRect.width || !parentRect.height || !rect.width) return;
    const fitted = widthThatFitsParent(frame, rect.width);
    if (fitted && fitted < rect.width) frame.style.width = fitted + "px";
  }

  function ensureSnapGuides(parent) {
    let x = parent.querySelector(":scope > .xs-snap-guide.x");
    let y = parent.querySelector(":scope > .xs-snap-guide.y");
    if (!x) {
      x = document.createElement("span");
      x.className = "xs-snap-guide x";
      x.setAttribute("data-no-edit", "true");
      parent.appendChild(x);
    }
    if (!y) {
      y = document.createElement("span");
      y.className = "xs-snap-guide y";
      y.setAttribute("data-no-edit", "true");
      parent.appendChild(y);
    }
    return { x, y };
  }

  function hideSnapGuides(parent) {
    parent?.querySelectorAll?.(":scope > .xs-snap-guide").forEach(guide => guide.classList.remove("is-visible"));
  }

  function collectInsertedFrames() {
    const slides = slideContainers();
    return [...document.querySelectorAll(".xs-inserted-frame")].map(frame => {
      const img = frame.querySelector("img");
      return {
        id: frame.dataset.xsEditId || "",
        parentIndex: Math.max(0, slides.indexOf(frame.parentElement)),
        src: img?.src || "",
        alt: img?.alt || "",
        style: {
          left: frame.style.left || "",
          top: frame.style.top || "",
          width: frame.style.width || "",
          zIndex: frame.style.zIndex || ""
        }
      };
    }).filter(item => item.src);
  }

  function persistInsertedFrames(historyLabel = "") {
    const store = readStore();
    store.__xsInsertedFrames = collectInsertedFrames();
    writeStore(store);
    if (historyLabel) commitHistory(historyLabel);
  }

  function restoreInsertedFrames(data) {
    const frames = Array.isArray(data.__xsInsertedFrames) ? data.__xsInsertedFrames : [];
    if (!frames.length) return;
    const slides = slideContainers();
    frames.forEach(item => {
      if (!item?.src) return;
      if (item.id && document.querySelector('.xs-inserted-frame[data-xs-edit-id="' + CSS.escape(item.id) + '"]')) return;
      const parent = slides[item.parentIndex] || activeSlideContainer();
      createInsertedFrame(item.src, item.alt || "插入图片", parent, {
        id: item.id,
        style: item.style || {},
        restored: true
      });
    });
  }

  /* ── Inserted text boxes ── */
  function collectInsertedTextFrames() {
    const slides = slideContainers();
    return [...document.querySelectorAll("[data-xs-inserted-text]")].map(box => ({
      id: box.dataset.xsEditId || "",
      parentIndex: Math.max(0, slides.indexOf(box.parentElement)),
      html: box.innerHTML,
      style: {
        left: box.style.left || "",
        top: box.style.top || "",
        width: box.style.width || "",
        height: box.style.height || "",
        fontSize: box.style.fontSize || "",
        lineHeight: box.style.lineHeight || "",
        zIndex: box.style.zIndex || ""
      }
    })).filter(item => item.id);
  }

  function createInsertedTextBox(parent, options = {}) {
    if (!parent) return null;
    const box = document.createElement("div");
    box.className = "xs-inserted-text";
    box.dataset.xsInsertedText = "true";
    box.dataset.xsEditId = options.id || nextTextBoxId();
    box.innerHTML = options.html || "输入文字";
    const style = options.style || {};
    box.style.left = style.left || "12%";
    box.style.top = style.top || "46%";
    box.style.width = style.width || "34%";
    box.style.height = style.height || "";
    box.style.fontSize = style.fontSize || "30px";
    box.style.lineHeight = style.lineHeight || "1.35";
    box.style.zIndex = style.zIndex || "81";
    parent.appendChild(box);
    if (editing) {
      box.setAttribute("contenteditable", "true");
      box.setAttribute("spellcheck", "false");
      attachTextFrameEvents();
      prepareTextFrame(box);
    }
    return box;
  }

  function restoreInsertedTextFrames(data) {
    const boxes = Array.isArray(data.__xsInsertedTextFrames) ? data.__xsInsertedTextFrames : [];
    if (!boxes.length) return;
    const slides = slideContainers();
    boxes.forEach(item => {
      if (!item?.id || document.querySelector('[data-xs-inserted-text][data-xs-edit-id="' + CSS.escape(item.id) + '"]')) return;
      const parent = slides[item.parentIndex] || activeSlideContainer();
      createInsertedTextBox(parent, { id: item.id, html: item.html || "输入文字", style: item.style || {} });
    });
  }

  function insertTextBox() {
    if (!editing) {
      toast("请先点击「编辑」进入编辑模式");
      return;
    }
    const box = createInsertedTextBox(activeSlideContainer());
    if (!box) {
      toast("未找到可编辑页面");
      return;
    }
    commitHistory("插入文本框");
    box.focus({ preventScroll: true });
    toast("文本框已插入，可直接输入、拖动或调整尺寸");
  }

  function deleteCurrentTextBox() {
    const box = getCurrentTextEl();
    if (!editing || !box?.matches?.("[data-xs-inserted-text]")) {
      toast("请先选中要删除的插入文本框");
      return;
    }
    box.remove();
    currentTextEl = null;
    updateFontControls();
    commitHistory("删除文本框");
    toast("文本框已删除，可用撤销恢复");
  }

  function deleteSelectedObject() {
    if (!editing) {
      toast("请先点击「编辑」进入编辑模式");
      return;
    }
    if (currentImageFrame?.isConnected) {
      deleteFrame(currentImageFrame);
      return;
    }
    const text = getCurrentTextEl();
    if (text?.matches?.("[data-xs-inserted-text]")) {
      deleteCurrentTextBox();
      return;
    }
    if (text && hideTextObject(text)) return;
    const detail = { handled: false };
    document.dispatchEvent(new CustomEvent("xs-edit:delete-selected-object", { cancelable: true, detail }));
    if (detail.handled) {
      toast("对象已删除，可用撤销恢复");
      return;
    }
    toast("请先选中要删除的文字、图片、图标或结构线");
  }

  function nearest(value, anchors, threshold = 18) {
    let best = { value, snapped: false };
    let distance = threshold + 1;
    anchors.forEach(anchor => {
      const diff = Math.abs(value - anchor);
      if (diff < distance && diff <= threshold) {
        distance = diff;
        best = { value: anchor, snapped: true };
      }
    });
    return best;
  }

  function snapPosition(frame, left, top) {
    const { parent, parentRect, rect } = frameMetrics(frame);
    const pad = 24;
    const maxLeft = Math.max(pad, parentRect.width - rect.width - pad);
    const maxTop = Math.max(pad, parentRect.height - rect.height - pad);
    const xAnchors = [pad, (parentRect.width - rect.width) / 2, maxLeft];
    const yAnchors = [pad, (parentRect.height - rect.height) / 2, maxTop];
    const snappedX = nearest(clamp(left, pad, maxLeft), xAnchors);
    const snappedY = nearest(clamp(top, pad, maxTop), yAnchors);
    const guides = ensureSnapGuides(parent);
    guides.y.style.left = Math.round(snappedX.value + rect.width / 2) + "px";
    guides.x.style.top = Math.round(snappedY.value + rect.height / 2) + "px";
    guides.y.classList.toggle("is-visible", snappedX.snapped);
    guides.x.classList.toggle("is-visible", snappedY.snapped);
    return { left: snappedX.value, top: snappedY.value };
  }

  function placeFrame(frame, placement) {
    const { parentRect, rect } = frameMetrics(frame);
    const pad = 28;
    const maxLeft = Math.max(pad, parentRect.width - rect.width - pad);
    const maxTop = Math.max(pad, parentRect.height - rect.height - pad);
    const positions = {
      left: { left: pad, top: Math.max(pad, (parentRect.height - rect.height) / 2) },
      center: { left: Math.max(pad, (parentRect.width - rect.width) / 2), top: Math.max(pad, (parentRect.height - rect.height) / 2) },
      right: { left: maxLeft, top: Math.max(pad, (parentRect.height - rect.height) / 2) },
      bottom: { left: Math.max(pad, (parentRect.width - rect.width) / 2), top: maxTop },
    };
    const pos = positions[placement] || positions.right;
    frame.style.left = Math.round(pos.left) + "px";
    frame.style.top = Math.round(pos.top) + "px";
    selectFrame(frame);
    persistInsertedFrames("图片位置");
  }

  function selectFrame(frame) {
    document.querySelectorAll(".xs-inserted-frame.is-selected").forEach(item => {
      if (item !== frame) item.classList.remove("is-selected");
    });
    currentTextEl = null;
    currentVisualSelection = false;
    document.dispatchEvent(new Event("xs-edit:clear-visual-selection"));
    currentImageFrame = frame;
    frame.classList.add("is-selected");
    frame.focus?.({ preventScroll: true });
    updateFontControls();
  }

  function deleteFrame(frame) {
    if (!frame?.classList?.contains("xs-inserted-frame")) return;
    const parent = frame.parentElement;
    frame.remove();
    hideSnapGuides(parent);
    if (currentImageFrame === frame) currentImageFrame = null;
    persistInsertedFrames("删除图片");
    updateFontControls();
    toast("图片已删除");
  }

  function arrangeInsertedBatch(frames) {
    const liveFrames = frames.filter(frame => frame?.isConnected);
    if (liveFrames.length <= 1) return;
    const parent = liveFrames[0].parentElement;
    if (!parent) return;
    const parentRect = parent.getBoundingClientRect();
    const pad = 34;
    const count = liveFrames.length;
    const columns = Math.min(count, 3);
    const widthRatio = count === 2 ? 0.28 : 0.22;
    liveFrames.forEach((frame, index) => {
      const col = index % columns;
      const row = Math.floor(index / columns);
      const targetWidth = widthThatFitsParent(frame, parentRect.width * widthRatio);
      frame.style.width = targetWidth + "px";
      const rect = frame.getBoundingClientRect();
      const available = Math.max(0, parentRect.width - pad * 2 - rect.width);
      const left = columns === 1 ? (parentRect.width - rect.width) / 2 : pad + (available * col / Math.max(1, columns - 1));
      const topBase = Math.max(pad, parentRect.height * 0.26);
      const top = topBase + row * Math.min(160, rect.height * .32);
      frame.style.left = Math.round(clamp(left, pad, Math.max(pad, parentRect.width - rect.width - pad))) + "px";
      frame.style.top = Math.round(clamp(top, pad, Math.max(pad, parentRect.height - rect.height - pad))) + "px";
    });
    selectFrame(liveFrames[liveFrames.length - 1]);
    persistInsertedFrames("图片排列");
  }

  function attachFrameEvents(frame) {
    if (frame.dataset.xsFrameReady === "true") return;
    frame.dataset.xsFrameReady = "true";
    frame.tabIndex = 0;
    frame.addEventListener("click", (event) => {
      if (!editing) return;
      event.stopPropagation();
      selectFrame(frame);
    });
    frame.addEventListener("pointerdown", (event) => {
      if (!editing || event.target.closest(".xs-insert-controls") || event.target.closest(".xs-insert-resize")) return;
      event.preventDefault();
      selectFrame(frame);
      const { parentRect, rect } = frameMetrics(frame);
      const offsetX = event.clientX - rect.left;
      const offsetY = event.clientY - rect.top;
      frame.setPointerCapture?.(event.pointerId);
      const move = (moveEvent) => {
        const pos = snapPosition(
          frame,
          moveEvent.clientX - parentRect.left - offsetX,
          moveEvent.clientY - parentRect.top - offsetY
        );
        frame.style.left = Math.round(pos.left) + "px";
        frame.style.top = Math.round(pos.top) + "px";
      };
      const up = () => {
        hideSnapGuides(frame.parentElement);
        frame.removeEventListener("pointermove", move);
        frame.removeEventListener("pointerup", up);
        frame.removeEventListener("pointercancel", up);
        persistInsertedFrames("图片位置");
        toast("图片位置已更新，导出 HTML 后会保留");
      };
      frame.addEventListener("pointermove", move);
      frame.addEventListener("pointerup", up);
      frame.addEventListener("pointercancel", up);
    });

    frame.querySelectorAll("[data-xs-place]").forEach(button => {
      button.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        placeFrame(frame, button.dataset.xsPlace);
      });
    });

    frame.querySelectorAll("[data-xs-size]").forEach(button => {
      button.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        const { parentRect } = frameMetrics(frame);
        const ratio = Number(button.dataset.xsSize || .34);
        frame.style.width = widthThatFitsParent(frame, parentRect.width * ratio) + "px";
        placeFrame(frame, "right");
      });
    });

    frame.querySelector("[data-xs-delete]")?.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      deleteFrame(frame);
    });

    const resize = frame.querySelector(".xs-insert-resize");
    resize?.addEventListener("pointerdown", (event) => {
      if (!editing) return;
      event.preventDefault();
      event.stopPropagation();
      selectFrame(frame);
      const startX = event.clientX;
      const startWidth = frame.getBoundingClientRect().width;
      const { parentRect } = frameMetrics(frame);
      resize.setPointerCapture?.(event.pointerId);
      const move = (moveEvent) => {
        const next = clamp(startWidth + (moveEvent.clientX - startX), 120, Math.max(160, parentRect.width - 48));
        frame.style.width = Math.round(next) + "px";
      };
      const up = () => {
        resize.removeEventListener("pointermove", move);
        resize.removeEventListener("pointerup", up);
        resize.removeEventListener("pointercancel", up);
        persistInsertedFrames("图片尺寸");
        toast("图片尺寸已更新，导出 HTML 后会保留");
      };
      resize.addEventListener("pointermove", move);
      resize.addEventListener("pointerup", up);
      resize.addEventListener("pointercancel", up);
    });
  }

  function createInsertedFrame(url, alt, container, options = {}) {
    const parent = prepareImageCanvas(container);
    const frame = document.createElement("figure");
    frame.className = "xs-inserted-frame";
    frame.dataset.xsInsertedImage = "true";
    frame.dataset.xsEditId = options.id || nextFrameId();
    frame.innerHTML = [
      '<div class="xs-insert-controls" data-no-edit="true" aria-label="图片位置控制">',
      '  <button type="button" data-xs-place="left">左</button>',
      '  <button type="button" data-xs-place="center">居中</button>',
      '  <button type="button" data-xs-place="right">右</button>',
      '  <button type="button" data-xs-place="bottom">置底</button>',
      '  <button type="button" data-xs-size="0.24">小</button>',
      '  <button type="button" data-xs-size="0.36">中</button>',
      '  <button type="button" data-xs-size="0.52">大</button>',
      '  <button type="button" data-xs-delete title="删除这张图片">删</button>',
      '</div>',
      '<img alt="' + escapeHtml(alt || "插入图片") + '">',
      '<span class="xs-insert-resize" data-no-edit="true" aria-hidden="true"></span>'
    ].join("");
    const img = frame.querySelector("img");
    img.addEventListener("load", () => {
      fitFrameToParent(frame);
      if (!options.restored) placeFrame(frame, "right");
      persistInsertedFrames();
    }, { once: true });
    img.src = url;
    parent.appendChild(frame);
    if (options.style) {
      if (options.style.left) frame.style.left = options.style.left;
      if (options.style.top) frame.style.top = options.style.top;
      if (options.style.width) frame.style.width = options.style.width;
      if (options.style.zIndex) frame.style.zIndex = options.style.zIndex;
    }
    attachFrameEvents(frame);
    if (options.restored) {
      requestAnimationFrame(() => {
        fitFrameToParent(frame);
        selectFrame(frame);
      });
    } else {
      requestAnimationFrame(() => {
        fitFrameToParent(frame);
        placeFrame(frame, "right");
        if (options.offsetIndex) {
          const left = parseFloat(frame.style.left || "0") - options.offsetIndex * 22;
          const top = parseFloat(frame.style.top || "0") + options.offsetIndex * 22;
          const pos = snapPosition(frame, left, top);
          frame.style.left = Math.round(pos.left) + "px";
          frame.style.top = Math.round(pos.top) + "px";
          hideSnapGuides(frame.parentElement);
        }
        persistInsertedFrames();
      });
    }
    return frame;
  }

  /* ── Insert image ── */
  function openInsertModal() {
    const mask = document.createElement("div");
    mask.className = "xs-modal-mask is-open";
    mask.innerHTML = '<div class="xs-modal">'
      + '<h3>插入图片</h3>'
      + '<p style="margin:0 0 14px;color:#6b7280;font-size:12px;">把图片拖进来，或点击选择本地图片。支持一次选择多张；插入后可拖动、吸附、调大小和删除。</p>'
      + '<div class="xs-file-upload" id="xsFileUpload">'
      + '  <strong>把图片拖到这里</strong>'
      + '  <span>或点击选择本地图片，可多选</span>'
      + '  <input type="file" id="xsFileInput" accept="image/*" multiple>'
      + '</div>'
      + '<details>'
      + '  <summary>高级：使用图片链接</summary>'
      + '  <label style="margin-top:12px;">图片地址 (URL)</label>'
      + '  <input type="url" class="xs-new-url" aria-label="图片地址，示例 https://example.com/image.png">'
      + '</details>'
      + '<div class="xs-modal-actions">'
      + '  <button class="xs-btn-cancel">取消</button>'
      + '  <button class="xs-btn-primary xs-btn-apply">插入</button>'
      + '</div>'
      + '</div>';
    document.body.appendChild(mask);

    const closeModal = () => { mask.remove(); };
    const fileUpload = mask.querySelector("#xsFileUpload");
    const fileInput = mask.querySelector("#xsFileInput");
    const currentSlide = activeSlideContainer();

    const readFileAsDataUrl = (file) => new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = () => reject(reader.error || new Error("图片读取失败"));
      reader.readAsDataURL(file);
    });

    const insertFiles = async (files) => {
      const images = [...files].filter(file => file.type.startsWith("image/"));
      if (!images.length) {
        toast("请选择图片文件");
        return false;
      }
      const frames = [];
      for (let index = 0; index < images.length; index += 1) {
        const file = images[index];
        const url = await readFileAsDataUrl(file);
        frames.push(createInsertedFrame(url, file.name || "插入图片", currentSlide, { offsetIndex: index }));
      }
      if (frames.length > 1) {
        window.setTimeout(() => arrangeInsertedBatch(frames), 360);
      }
      toast(images.length === 1 ? "图片已插入，可拖动或删除" : "已插入 " + images.length + " 张图片");
      return true;
    };

    const insertUrl = (url) => {
      if (!url) return false;
      createInsertedFrame(url, "插入图片", currentSlide);
      toast("图片已插入，可拖动或删除");
      return true;
    };

    const apply = async () => {
      const newUrl = mask.querySelector(".xs-new-url").value.trim();
      const files = fileInput.files;
      try {
        if (files.length) {
          if (!await insertFiles(files)) return;
        } else if (!insertUrl(newUrl)) {
          toast("请拖入图片、选择本地图片，或在高级里填图片链接");
          return;
        }
      } catch {
        toast("图片读取失败，请换一张再试");
        return;
      }
      closeModal();
    };

    mask.addEventListener("click", (e) => { if (e.target === mask) closeModal(); });
    mask.querySelector(".xs-btn-cancel").addEventListener("click", closeModal);
    mask.querySelector(".xs-btn-apply").addEventListener("click", apply);
    fileUpload.addEventListener("click", () => fileInput.click());
    fileUpload.addEventListener("dragover", (event) => {
      event.preventDefault();
      fileUpload.classList.add("is-dragover");
    });
    fileUpload.addEventListener("dragleave", () => {
      fileUpload.classList.remove("is-dragover");
    });
    fileUpload.addEventListener("drop", async (event) => {
      event.preventDefault();
      fileUpload.classList.remove("is-dragover");
      try {
        if (await insertFiles(event.dataTransfer.files)) closeModal();
      } catch {
        toast("图片读取失败，请换一张再试");
      }
    });
    fileInput.addEventListener("change", async () => {
      try {
        if (await insertFiles(fileInput.files)) closeModal();
      } catch {
        toast("图片读取失败，请换一张再试");
      }
    });
    mask.querySelector(".xs-new-url").addEventListener("keydown", (e) => {
      if (e.key === "Enter") apply();
    });
  }

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;").replace(/'/g, "&#039;");
  }

  /* ── Reset ── */
  function resetAll() {
    localStorage.removeItem(STORE_KEY);
    localStorage.removeItem(LEGACY_STORE_KEY);
    document.dispatchEvent(new Event("xs-edit:reset"));
    clearHistory();
    toast("已清除本机修改，刷新后恢复模板内容");
  }

  /* ── Export ── */
  function exportHtml() {
    saveAll();
    const clone = document.documentElement.cloneNode(true);
    clone.querySelectorAll("[contenteditable], [spellcheck]").forEach(el => {
      el.removeAttribute("contenteditable");
      el.removeAttribute("spellcheck");
    });
    clone.querySelectorAll(".xs-edit-toolbar, .xs-toast, .xs-media-wrapper, .xs-media-badge, .xs-modal-mask, .xs-insert-controls, .xs-insert-resize, .xs-snap-guide, .xs-layer-overlay, #xs-layer-overlay-style")
      .forEach(el => el.remove());
    clone.querySelectorAll(".xs-inserted-frame").forEach(frame => {
      frame.classList.remove("is-selected");
      frame.removeAttribute("tabindex");
      delete frame.dataset.xsFrameReady;
    });
    // Unwrap media wrappers in clone
    clone.querySelectorAll(".xs-media-wrapper").forEach(w => {
      const p = w.parentElement;
      while (w.firstChild) p.insertBefore(w.firstChild, w);
      p.removeChild(w);
    });
    clone.querySelector("body")?.classList.remove("xs-editing");
    const html = "<!doctype html>\n" + clone.outerHTML;
    const blob = new Blob([html], { type: "text/html;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = (document.title || "editable-html-ppt").replace(/[\\/:*?"<>|]+/g, "-") + "-edited.html";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    toast("已导出 HTML 文件");
  }

  /* ── High-fidelity PPTX export ── */
  let pptxExporting = false;
  const PPTX_WIDE = { width: 13.333, height: 7.5 };

  function deckSlidesForPptx() {
    const selector = document.querySelector("[data-slide]") ? "[data-slide]" : ".slide";
    return [...document.querySelectorAll(selector)].filter(slide => {
      if (slide.closest(".shui-presenter-overlay, .xs-edit-toolbar")) return false;
      const rect = slide.getBoundingClientRect();
      return rect.width > 32 && rect.height > 32;
    });
  }

  function safePptxFilename(editableText = false) {
    return (document.title || "editable-html-ppt")
      .replace(/[\\/:*?"<>|]+/g, "-")
      .replace(/\\s+/g, " ")
      .trim() + (editableText ? "-可编辑文本" : "") + ".pptx";
  }

  async function waitForSlideAssets(slides) {
    await document.fonts?.ready;
    const images = slides.flatMap(slide => [...slide.querySelectorAll("img")]);
    await Promise.all(images.map(image => image.complete
      ? image.decode?.().catch(() => undefined)
      : new Promise(resolve => {
          image.addEventListener("load", resolve, { once: true });
          image.addEventListener("error", resolve, { once: true });
        })
    ));
  }

  function noteForPptx(slide) {
    return (slide.querySelector("[data-speaker-notes], .speaker-notes")?.textContent || "").trim();
  }

  function cssColorToHex(value) {
    const match = String(value || "").match(/rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/i);
    if (!match) return "111827";
    return match.slice(1).map(part => Number(part).toString(16).padStart(2, "0")).join("").toUpperCase();
  }

  function pptxAlignment(value) {
    const normalized = String(value || "").toLowerCase();
    if (normalized === "center" || normalized === "justify" || normalized === "right") return normalized;
    if (normalized === "end") return "right";
    return "left";
  }

  function pptxTextValue(text) {
    const lines = text.split(/\r?\n/);
    if (lines.length === 1) return text;
    return lines.map((line, index) => ({
      text: line || " ",
      options: index < lines.length - 1 ? { breakLine: true } : {},
    }));
  }

  function primaryTextCandidatesForPptx(slide) {
    const selector = "h1,h2,h3,p,li,blockquote,td,th,dt,dd,figcaption,caption,[data-xs-inserted-text]";
    return [...slide.querySelectorAll(selector)].filter(el => {
      if (el.closest("[data-speaker-notes], .speaker-notes, [data-no-edit], .xs-edit-toolbar")) return false;
      if (el.querySelector(selector)) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      const fontSize = parseFloat(style.fontSize) || 0;
      const text = (el.innerText || el.textContent || "").trim();
      return Boolean(text) && rect.width >= 24 && rect.height >= 10 && fontSize >= 11 && style.visibility !== "hidden";
    });
  }

  function pptxTextEntry(el, slideRect) {
    const rect = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    const pxToPt = 72 / 96;
    const fontSize = Math.max(8, Math.min(96, (parseFloat(style.fontSize) || 16) * pxToPt));
    const fontFace = String(style.fontFamily || "").split(",")[0].trim().replace(/^['\"]|['\"]$/g, "");
    const text = (el.innerText || el.textContent || "").replace(/\u00a0/g, " ").trim();
    const lineHeightPx = parseFloat(style.lineHeight);
    return {
      text,
      value: pptxTextValue(text),
      options: {
        x: Math.max(0, (rect.left - slideRect.left) / slideRect.width * PPTX_WIDE.width),
        y: Math.max(0, (rect.top - slideRect.top) / slideRect.height * PPTX_WIDE.height),
        w: Math.max(0.05, rect.width / slideRect.width * PPTX_WIDE.width),
        h: Math.max(0.05, rect.height / slideRect.height * PPTX_WIDE.height),
        fontFace,
        fontSize,
        color: cssColorToHex(style.color),
        bold: Number.parseInt(style.fontWeight, 10) >= 600 || style.fontWeight === "bold",
        italic: style.fontStyle === "italic",
        align: pptxAlignment(style.textAlign),
        valign: "top",
        margin: 0,
        lineSpacing: Number.isFinite(lineHeightPx) ? Math.max(fontSize, lineHeightPx * pxToPt) : undefined,
        paraSpaceAfter: 0,
        paraSpaceBefore: 0,
      },
    };
  }

  async function captureSlidePng(slide, rect, backgroundColor) {
    return window.htmlToImage.toPng(slide, {
      pixelRatio: Math.min(3, Math.max(2, window.devicePixelRatio || 1)),
      cacheBust: false,
      backgroundColor: backgroundColor === "rgba(0, 0, 0, 0)" ? "#ffffff" : backgroundColor,
      width: Math.round(rect.width),
      height: Math.round(rect.height),
      // html-to-image clones the node into a new viewport. Preserve the
      // measured slide size and remove auto margins so responsive rules
      // such as `width: 88vw; margin: 0 auto` cannot create a blank strip.
      style: {
        transform: "none",
        width: Math.round(rect.width) + "px",
        height: Math.round(rect.height) + "px",
        minWidth: "0",
        minHeight: "0",
        margin: "0",
        boxSizing: "border-box",
      },
      filter: node => !node.classList?.contains("xs-insert-controls")
        && !node.classList?.contains("xs-insert-resize")
        && !node.classList?.contains("xs-media-badge"),
    });
  }

  async function exportPptx(editableText = false) {
    if (pptxExporting) return;
    if (!window.PptxGenJS || !window.htmlToImage?.toPng) {
      toast("PPTX 导出组件未加载，请刷新后重试");
      return;
    }
    const slides = deckSlidesForPptx();
    if (!slides.length) {
      toast("未找到可导出的幻灯片");
      return;
    }

    pptxExporting = true;
    const button = document.querySelector(editableText
      ? "[data-xs-edit-export-editable-pptx]"
      : "[data-xs-edit-export-pptx]");
    const buttonLabel = editableText ? "PPTX（可编辑文本）" : "导出 PPTX";
    if (button) { button.disabled = true; button.textContent = "正在导出…"; }
    const wasEditing = document.body.classList.contains("xs-editing");
    try {
      saveAll();
      document.body.classList.remove("xs-editing");
      document.body.classList.add("xs-pptx-exporting");
      await waitForSlideAssets(slides);

      const pptx = new window.PptxGenJS();
      pptx.layout = "LAYOUT_WIDE";
      pptx.author = "Editable HTML PPT";
      pptx.company = "Editable HTML PPT";
      pptx.subject = editableText
        ? "HTML presentation export with editable main text"
        : "High-fidelity HTML presentation export";
      pptx.title = document.title || "Editable HTML PPT";
      pptx.lang = document.documentElement.lang || "zh-CN";

      for (let index = 0; index < slides.length; index += 1) {
        if (button) button.textContent = "渲染 " + (index + 1) + "/" + slides.length;
        const slide = slides[index];
        const rect = slide.getBoundingClientRect();
        const backgroundColor = getComputedStyle(slide).backgroundColor;
        const sourceText = editableText ? primaryTextCandidatesForPptx(slide) : [];
        const textEntries = sourceText.map(el => pptxTextEntry(el, rect)).filter(entry => entry.text);
        sourceText.forEach(el => el.classList.add("xs-pptx-editable-text-hidden"));
        let data;
        try {
          data = await captureSlidePng(slide, rect, backgroundColor);
        } finally {
          sourceText.forEach(el => el.classList.remove("xs-pptx-editable-text-hidden"));
        }
        const pptSlide = pptx.addSlide();
        pptSlide.background = { color: "FFFFFF" };
        pptSlide.addImage({ data, x: 0, y: 0, w: PPTX_WIDE.width, h: PPTX_WIDE.height });
        textEntries.forEach(entry => pptSlide.addText(entry.value, entry.options));
        const notes = noteForPptx(slide);
        if (notes) pptSlide.addNotes(notes);
      }

      if (button) button.textContent = "生成文件…";
      await pptx.writeFile({ fileName: safePptxFilename(editableText), compression: true });
      toast(editableText
        ? "已导出 " + slides.length + " 页可编辑文本 PPTX（含演讲稿备注）"
        : "已导出 " + slides.length + " 页 PPTX（含演讲稿备注）");
    } catch (error) {
      console.error("Pretty HTML PPT PPTX export failed", error);
      toast("PPTX 导出失败：请确认图片可本地访问后重试");
    } finally {
      document.body.classList.remove("xs-pptx-exporting");
      if (wasEditing) document.body.classList.add("xs-editing");
      pptxExporting = false;
      if (button) { button.disabled = false; button.textContent = buttonLabel; }
    }
  }

  /* ── Toolbar ── */
  function buildToolbar() {
    if (document.querySelector(".xs-edit-toolbar")) return;
    const bar = document.createElement("div");
    bar.className = "xs-edit-toolbar xs-collapsed";
    bar.setAttribute("data-no-edit", "true");
    bar.innerHTML = [
      '<div class="xs-toolbar-header">',
      '  <div class="xs-toolbar-group xs-toolbar-session">',
      '    <button type="button" data-xs-edit-toggle>编辑</button>',
      '    <button type="button" class="xs-history-button" data-xs-history-undo title="撤销上一步（⌘/Ctrl + Z）" aria-label="撤销上一步" disabled>↶</button>',
      '    <button type="button" class="xs-history-button" data-xs-history-redo title="恢复下一步（⌘/Ctrl + Shift + Z）" aria-label="恢复下一步" disabled>↷</button>',
      '  </div>',
      '</div>',
      '<div class="xs-toolbar-type">',
      '  <span class="xs-font-control" title="先点选文字，再调整字号">',
      '  <label for="xsFontSizeInput">字号</label>',
      '  <button type="button" data-xs-font-minus title="减小字号">A-</button>',
      '  <input id="xsFontSizeInput" type="number" min="8" max="160" step="1" data-xs-font-size disabled>',
      '  <button type="button" data-xs-font-plus title="增大字号">A+</button>',
      '  <button type="button" data-xs-font-reset title="恢复模板默认字号">默认</button>',
      '</span>',
      '  <span class="xs-toolbar-type-divider" aria-hidden="true"></span>',
      '  <span class="xs-font-control" title="先点选文字，再调整行距">',
      '  <label for="xsLineHeightInput">行距</label>',
      '  <button type="button" data-xs-line-minus title="减小行距">−</button>',
      '  <input id="xsLineHeightInput" type="number" min="0.8" max="3" step="0.1" data-xs-line-height disabled>',
      '  <button type="button" data-xs-line-plus title="增大行距">+</button>',
      '  <button type="button" data-xs-line-reset title="恢复模板默认行距">默认</button>',
      '</span>',
      '</div>',
      '<div class="xs-toolbar-group xs-toolbar-actions">',
      '  <span class="xs-toolbar-label">页面操作</span>',
      '  <button type="button" data-xs-edit-insert-text title="插入可编辑文本框到当前页面">＋ 文本</button>',
      '  <button type="button" data-xs-edit-delete-text title="删除当前选中的对象；可用撤销恢复" disabled>删除</button>',
      '  <button type="button" data-xs-edit-insert-img title="插入一张图片到当前页面">＋ 图片</button>',
      '  <button type="button" data-xs-edit-reset>重置</button>',
      '</div>',
      '<div class="xs-toolbar-group xs-toolbar-output">',
      '  <span class="xs-toolbar-label">保存与导出</span>',
      '  <button type="button" data-xs-edit-save>保存</button>',
      '  <button type="button" data-xs-edit-export-pptx title="按当前视觉效果导出含演讲稿备注的 PPTX">导出 PPTX</button>',
      '  <button type="button" data-xs-edit-export-editable-pptx title="将主体文字导出为可编辑 PowerPoint 文本框">可编辑 PPTX</button>',
      '</div>'
    ].join("");
    document.body.appendChild(bar);
    enableToolbarDrag(bar);
    bar.querySelector("[data-xs-edit-toggle]").addEventListener("click", () => {
      if (bar.classList.contains("xs-collapsed")) {
        setToolbarExpanded(true);
        toggleEdit(true);
      } else if (editing) {
        collapseEdit();
      } else {
        toggleEdit(true);
      }
    });
    bar.querySelector("[data-xs-history-undo]").addEventListener("click", undoHistory);
    bar.querySelector("[data-xs-history-redo]").addEventListener("click", redoHistory);
    bar.querySelector("[data-xs-edit-save]").addEventListener("click", saveAll);
    bar.querySelector("[data-xs-edit-export-pptx]").addEventListener("click", () => exportPptx(false));
    bar.querySelector("[data-xs-edit-export-editable-pptx]").addEventListener("click", () => exportPptx(true));
    bar.querySelector("[data-xs-edit-reset]").addEventListener("click", resetAll);
    bar.querySelector("[data-xs-font-minus]").addEventListener("click", () => changeFontSize(-2));
    bar.querySelector("[data-xs-font-plus]").addEventListener("click", () => changeFontSize(2));
    bar.querySelector("[data-xs-font-reset]").addEventListener("click", resetFontSize);
    bar.querySelector("[data-xs-font-size]").addEventListener("change", (event) => {
      const value = Number.parseFloat(event.target.value);
      if (Number.isFinite(value)) applyFontSize(value);
    });
    bar.querySelector("[data-xs-font-size]").addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        const value = Number.parseFloat(event.target.value);
        if (Number.isFinite(value)) applyFontSize(value);
      }
    });
    bar.querySelector("[data-xs-line-minus]").addEventListener("click", () => changeLineHeight(-0.1));
    bar.querySelector("[data-xs-line-plus]").addEventListener("click", () => changeLineHeight(0.1));
    bar.querySelector("[data-xs-line-reset]").addEventListener("click", resetLineHeight);
    bar.querySelector("[data-xs-line-height]").addEventListener("change", (event) => {
      const value = Number.parseFloat(event.target.value);
      if (Number.isFinite(value)) applyLineHeight(value);
    });
    bar.querySelector("[data-xs-line-height]").addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        const value = Number.parseFloat(event.target.value);
        if (Number.isFinite(value)) applyLineHeight(value);
      }
    });
    bar.querySelector("[data-xs-edit-insert-img]").addEventListener("click", () => {
      if (!editing) { toast("请先点击「编辑」进入编辑模式"); return; }
      openInsertModal();
    });
    bar.querySelector("[data-xs-edit-insert-text]").addEventListener("click", insertTextBox);
    bar.querySelector("[data-xs-edit-delete-text]").addEventListener("click", deleteSelectedObject);
    updateHistoryButtons();
  }

  document.addEventListener("focusin", (event) => {
    const el = fontTargetFromEventTarget(event.target);
    if (el) setCurrentTextEl(el);
  });

  document.addEventListener("click", (event) => {
    const el = fontTargetFromEventTarget(event.target);
    if (el) setCurrentTextEl(el);
    if (editing && !event.target.closest(".xs-inserted-frame")) {
      document.querySelectorAll(".xs-inserted-frame.is-selected").forEach(frame => frame.classList.remove("is-selected"));
      currentImageFrame = null;
      updateFontControls();
    }
  });

  document.addEventListener("xs-edit:selection-change", (event) => {
    currentVisualSelection = event.detail?.kind === "visual";
    if (currentVisualSelection) {
      currentTextEl = null;
      currentImageFrame = null;
    }
    updateFontControls();
  });

  document.addEventListener("xs-edit:history-commit", (event) => {
    commitHistory(event.detail?.label || "图层调整");
  });

  document.addEventListener("xs-edit:request-exit", () => {
    if (editing) collapseEdit();
  });

  /* ── Keyboard ── */
  document.addEventListener("keydown", (event) => {
    const key = event.key.toLowerCase();
    const tag = document.activeElement?.tagName?.toLowerCase();
    const typing = tag === "input" || tag === "textarea" || tag === "select" || document.activeElement?.isContentEditable;
    if (editing && !typing && (currentImageFrame || currentTextEl || currentVisualSelection) && (key === "delete" || key === "backspace")) {
      event.preventDefault();
      deleteSelectedObject();
      return;
    }
    if (editing && !typing && (event.metaKey || event.ctrlKey) && key === "z") {
      event.preventDefault();
      if (event.shiftKey) redoHistory(); else undoHistory();
      return;
    }
    if (editing && !typing && event.ctrlKey && !event.metaKey && key === "y") {
      event.preventDefault();
      redoHistory();
      return;
    }
    /* E enters edit mode; R and Esc exit. E never toggles while editing. */
    if (!editing && !typing && key === "e" && !event.metaKey && !event.ctrlKey && !event.altKey) {
      event.preventDefault();
      if (document.documentElement.classList.contains("shui-presenter-is-open")) {
        window.__shuiPrettyPresenter?.control("close");
      }
      setToolbarExpanded(true);
      enterEdit();
    }
    if (editing && !typing && key === "s" && !event.altKey) {
      event.preventDefault();
      saveAll();
      return;
    }
    if ((key === "r" || key === "escape") && editing) {
      if (document.querySelector(".xs-modal-mask.is-open")) return;
      event.preventDefault();
      collapseEdit();
    }
  });

  /* ── Init ── */
  ensureIds();
  restoreAll();
  buildToolbar();
  document.querySelectorAll(".xs-inserted-frame").forEach(attachFrameEvents);
  initializeHistory();
})();
</script>
<style id="xs-layer-overlay-style">
  .xs-layer-overlay {
    position: fixed;
    z-index: 2147483600;
    display: none;
    border: 1.5px dashed rgba(37, 99, 235, .9);
    border-radius: 4px;
    background: rgba(37, 99, 235, .035);
    pointer-events: none;
    box-sizing: border-box;
  }
  .xs-layer-overlay.is-visible { display: block; }
  .xs-layer-overlay.is-selected {
    border: 2px solid rgba(255, 79, 154, .95);
    background: rgba(255, 79, 154, .045);
    pointer-events: none;
  }
  .xs-layer-overlay.is-selected::after {
    content: "";
    position: absolute;
    right: -7px;
    bottom: -7px;
    width: 11px;
    height: 11px;
    border: 2px solid #fff;
    border-radius: 50%;
    background: #ff4f9a;
    box-shadow: 0 2px 8px rgba(17, 24, 39, .24);
  }
  .xs-layer-handle {
    position: absolute;
    z-index: 1;
    display: none;
    pointer-events: auto;
    touch-action: none;
  }
  .xs-layer-overlay.is-selected .xs-layer-handle { display: block; }
  .xs-layer-handle-top {
    top: -6px;
    left: 10px;
    right: 10px;
    height: 12px;
    cursor: grab;
  }
  .xs-layer-handle-left {
    top: 10px;
    bottom: 10px;
    left: -6px;
    width: 12px;
    cursor: ew-resize;
  }
  .xs-layer-handle-right {
    top: 10px;
    right: -6px;
    bottom: 10px;
    width: 12px;
    cursor: ew-resize;
  }
  .xs-layer-handle-bottom {
    right: 10px;
    bottom: -6px;
    left: 10px;
    height: 12px;
    cursor: ns-resize;
  }
  .xs-layer-overlay.is-selected.xs-layer-dragging .xs-layer-handle-top { cursor: grabbing; }
  .xs-layer-overlay.is-structural-line .xs-layer-handle-bottom { display: none !important; }
  .xs-layer-overlay.is-structural-line .xs-layer-handle-left,
  .xs-layer-overlay.is-structural-line .xs-layer-handle-right {
    top: -6px;
    bottom: -6px;
  }
  .xs-structural-line {
    position: absolute;
    z-index: 1;
    display: block;
    pointer-events: none;
    transform-origin: 50% 50%;
  }
</style>
<script id="editable-html-ppt-layer-script">
(() => {
  const STORE_KEY = "editable-html-ppt-layers:v1:" + location.pathname;
  const LEGACY_STORE_KEY = "pretty-html-ppt-layers:v1:" + location.pathname;
  const ignored = ".xs-edit-toolbar, .xs-toast, .xs-modal-mask, .xs-layer-overlay, .shui-presenter-overlay, .shui-talk-timer-dock, [data-no-edit], script, style";
  const textTags = new Set(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "blockquote", "td", "th", "figcaption", "caption", "a", "span", "em", "strong", "small"]);
  const visualClass = /(icon|logo|badge|chip|tag|label|number|page|year|metric|chart|diagram|shape|line|marker|rail|card|panel)/i;
  const state = { active: false, candidates: [], selected: null, hover: null, overlay: null, drag: null };
  const structuralBorderStyles = new Map();

  function readStore() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY) || localStorage.getItem(LEGACY_STORE_KEY) || "{}"); }
    catch { return {}; }
  }
  function writeStore(value) { localStorage.setItem(STORE_KEY, JSON.stringify(value)); }
  function hash(value) { let h = 5381; for (let i = 0; i < value.length; i += 1) h = (h * 33) ^ value.charCodeAt(i); return "l" + (h >>> 0).toString(36); }
  function pathOf(el) {
    const parts = [];
    let node = el;
    while (node && node !== document.body) {
      const siblings = [...node.parentElement.children].filter(item => item.tagName === node.tagName);
      parts.unshift(node.tagName.toLowerCase() + ":" + siblings.indexOf(node));
      node = node.parentElement;
    }
    return parts.join("/");
  }
  function keyFor(el, pseudo) { return hash(pathOf(el) + "|" + pseudo); }
  function isVisible(el) {
    const style = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) > 0 && rect.width > 2 && rect.height > 2;
  }
  function isTextManaged(el) {
    return textTags.has(el.tagName.toLowerCase()) && !visualClass.test(el.className || "") && !el.closest(".meta");
  }
  function isBorderOnlyStyle(style) {
    const hasBorder = [style.borderTopWidth, style.borderRightWidth, style.borderBottomWidth, style.borderLeftWidth]
      .some(value => parseFloat(value) > 0);
    const hasFill = style.backgroundColor !== "transparent" && style.backgroundColor !== "rgba(0, 0, 0, 0)";
    return hasBorder && !hasFill && style.backgroundImage === "none" && style.boxShadow === "none";
  }
  function hasManagedDescendant(el) {
    return [...el.querySelectorAll("h1, h2, h3, h4, h5, h6, p, li, blockquote, td, th, figcaption, caption, a, span, em, strong, small")]
      .some(child => isVisible(child) && isTextManaged(child) && (child.textContent || "").trim());
  }
  function structuralBorderEdges(el) {
    const style = getComputedStyle(el);
    if (!isBorderOnlyStyle(style) || !hasManagedDescendant(el)) return [];
    return ["top", "right", "bottom", "left"].filter(edge => parseFloat(style["border" + edge[0].toUpperCase() + edge.slice(1) + "Width"]) > 0);
  }
  function structuralBorderInfo(el, edge, key) {
    const style = getComputedStyle(el);
    const prefix = "border" + edge[0].toUpperCase() + edge.slice(1);
    const previous = structuralBorderStyles.get(key);
    const width = parseFloat(style[prefix + "Width"]);
    const color = style[prefix + "Color"];
    const validColor = color && color !== "transparent" && color !== "rgba(0, 0, 0, 0)";
    const info = {
      edge,
      width: Number.isFinite(width) && width > 0 ? width : (previous?.width || 1),
      color: validColor ? color : (previous?.color || "currentColor"),
      style: style[prefix + "Style"] || previous?.style || "solid",
    };
    structuralBorderStyles.set(key, info);
    return info;
  }
  function pseudoVisible(el, pseudo) {
    const style = getComputedStyle(el, pseudo);
    const hasContent = style.content && style.content !== "none" && style.content !== "normal";
    const hasSurface = style.backgroundImage !== "none" || parseFloat(style.borderTopWidth) > 0 || parseFloat(style.borderRightWidth) > 0 || style.boxShadow !== "none";
    return hasContent || hasSurface;
  }
  function directVisible(el) {
    const tag = el.tagName.toLowerCase();
    if (["img", "video", "audio", "svg", "canvas", "iframe", "table"].includes(tag) || el.getAttribute("role") === "img") return true;
    if (tag === "b" && el.closest(".meta")) return true;
    const style = getComputedStyle(el);
    if (isBorderOnlyStyle(style) && hasManagedDescendant(el)) return false;
    if (visualClass.test(el.className || "")) return true;
    const hasSurface = style.backgroundImage !== "none" || parseFloat(style.borderTopWidth) > 0 || style.boxShadow !== "none";
    return hasSurface && !isTextManaged(el) && !el.matches("[data-slide], .slide, main, body, html");
  }
  function pseudoRect(el, pseudo) {
    const owner = el.getBoundingClientRect();
    const style = getComputedStyle(el, pseudo);
    const width = parseFloat(style.width) || owner.width;
    const height = parseFloat(style.height) || owner.height;
    const left = parseFloat(style.left);
    const right = parseFloat(style.right);
    const top = parseFloat(style.top);
    const bottom = parseFloat(style.bottom);
    return {
      left: owner.left + (Number.isFinite(left) ? left : (Number.isFinite(right) ? owner.width - right - width : 0)),
      top: owner.top + (Number.isFinite(top) ? top : (Number.isFinite(bottom) ? owner.height - bottom - height : 0)),
      width, height,
    };
  }
  function transformedPseudoRect(rect, record) {
    if (!record) return rect;
    const sx = Number(record.sx) || 1;
    const sy = Number(record.sy) || 1;
    const x = Number(record.x) || 0;
    const y = Number(record.y) || 0;
    return {
      left: rect.left + x - (rect.width * (sx - 1) / 2),
      top: rect.top + y - (rect.height * (sy - 1) / 2),
      width: rect.width * sx,
      height: rect.height * sy,
    };
  }
  function rectOf(candidate) {
    if (!candidate.pseudo) return candidate.el.getBoundingClientRect();
    return transformedPseudoRect(pseudoRect(candidate.el, candidate.pseudo), readStore()[candidate.key]);
  }
  function structuralRect(candidate) {
    const owner = candidate.el.getBoundingClientRect();
    const { edge, width } = candidate.structuralBorder;
    if (edge === "top") return { left: owner.left, top: owner.top, width: owner.width, height: width };
    if (edge === "right") return { left: owner.left + owner.width - width, top: owner.top, width, height: owner.height };
    if (edge === "bottom") return { left: owner.left, top: owner.top + owner.height - width, width: owner.width, height: width };
    return { left: owner.left, top: owner.top, width, height: owner.height };
  }
  function visualRectOf(candidate) {
    if (!candidate.structuralBorder) return rectOf(candidate);
    return transformedPseudoRect(structuralRect(candidate), readStore()[candidate.key]);
  }
  function contains(rect, x, y) { return x >= rect.left && x <= rect.left + rect.width && y >= rect.top && y <= rect.top + rect.height; }
  function styleOf(candidate) { return getComputedStyle(candidate.el, candidate.pseudo || null); }
  function borderOnly(candidate) {
    return isBorderOnlyStyle(styleOf(candidate));
  }
  function hitCandidate(candidate, x, y) {
    const rect = visualRectOf(candidate);
    if (!contains(rect, x, y) || !borderOnly(candidate)) return contains(rect, x, y);
    const style = styleOf(candidate);
    const gutter = 10;
    return (parseFloat(style.borderTopWidth) > 0 && y - rect.top <= gutter)
      || (parseFloat(style.borderRightWidth) > 0 && (rect.left + rect.width) - x <= gutter)
      || (parseFloat(style.borderBottomWidth) > 0 && (rect.top + rect.height) - y <= gutter)
      || (parseFloat(style.borderLeftWidth) > 0 && x - rect.left <= gutter);
  }
  function ensureAnchor(candidate) {
    if (!candidate.el.dataset.xsLayerAnchor) candidate.el.dataset.xsLayerAnchor = candidate.key;
    candidate.anchor = candidate.el.dataset.xsLayerAnchor;
  }
  function scan() {
    const items = [];
    document.querySelectorAll("*").forEach(el => {
      if (el.closest(ignored) || !isVisible(el)) return;
      const edges = structuralBorderEdges(el);
      if (edges.length) {
        edges.forEach(edge => {
          const key = keyFor(el, "structural-border-" + edge);
          items.push({ el, pseudo: "", key, structuralBorder: structuralBorderInfo(el, edge, key) });
        });
      } else if (directVisible(el)) items.push({ el, pseudo: "", key: keyFor(el, "element") });
      ["::before", "::after"].forEach(pseudo => {
        if (pseudoVisible(el, pseudo)) items.push({ el, pseudo, key: keyFor(el, pseudo) });
      });
    });
    const unique = new Map();
    items.forEach(item => { if (!unique.has(item.key)) unique.set(item.key, item); });
    state.candidates = [...unique.values()];
    state.candidates.forEach(ensureAnchor);
  }
  function overrideStyle() {
    let style = document.getElementById("xs-layer-overrides");
    if (!style) { style = document.createElement("style"); style.id = "xs-layer-overrides"; document.head.appendChild(style); }
    return style;
  }
  function renderOverrides() {
    const store = readStore();
    const existing = overrideStyle();
    document.querySelectorAll(".xs-structural-line").forEach(line => line.remove());
    if (!Object.keys(store).length) {
      existing.textContent = "";
      return;
    }
    const rules = [];
    state.candidates.forEach(candidate => {
      const record = store[candidate.key];
      if (!record) return;
      const selector = '[data-xs-layer-anchor="' + CSS.escape(candidate.anchor) + '"]' + candidate.pseudo;
      if (candidate.structuralBorder) {
        const property = "border-" + candidate.structuralBorder.edge + "-color";
        rules.push(selector + "{" + property + ":transparent !important;position:relative;}");
        if (record.hidden) return;
        const line = document.createElement("span");
        const owner = candidate.el.getBoundingClientRect();
        const rect = structuralRect(candidate);
        const { color, style, width } = candidate.structuralBorder;
        line.className = "xs-structural-line";
        line.setAttribute("data-no-edit", "true");
        line.dataset.xsStructuralLine = candidate.key;
        line.style.left = Math.round(rect.left - owner.left) + "px";
        line.style.top = Math.round(rect.top - owner.top) + "px";
        line.style.width = Math.max(1, Math.round(rect.width)) + "px";
        line.style.height = Math.max(1, Math.round(rect.height)) + "px";
        line.style.background = color;
        if (style && style !== "solid") {
          const direction = ["top", "bottom"].includes(candidate.structuralBorder.edge) ? "90deg" : "0deg";
          line.style.backgroundImage = "repeating-linear-gradient(" + direction + "," + color + " 0 4px,transparent 4px 7px)";
        }
        line.style.transform = "translate(" + (record.x || 0) + "px," + (record.y || 0) + "px) scale(" + (record.sx || 1) + "," + (record.sy || 1) + ")";
        candidate.el.appendChild(line);
        return;
      }
      if (record.hidden) {
        rules.push(selector + (candidate.pseudo
          ? "{content:none !important;opacity:0 !important;}"
          : "{visibility:hidden !important;pointer-events:none !important;}"));
        return;
      }
      rules.push(selector + '{translate:' + (record.x || 0) + 'px ' + (record.y || 0) + 'px;scale:' + (record.sx || 1) + ' ' + (record.sy || 1) + ';transform-origin:50% 50%;}');
    });
    existing.textContent = rules.join("\n");
  }
  function ensureOverlay() {
    if (state.overlay) return state.overlay;
    const node = document.createElement("div");
    node.className = "xs-layer-overlay";
    node.setAttribute("data-no-edit", "true");
    ["top", "left", "right", "bottom"].forEach(edge => {
      const handle = document.createElement("div");
      handle.className = "xs-layer-handle xs-layer-handle-" + edge;
      handle.dataset.xsLayerHandle = edge;
      handle.addEventListener("pointerdown", beginDrag);
      node.appendChild(handle);
    });
    document.body.appendChild(node);
    state.overlay = node;
    return node;
  }
  function placeOverlay(candidate, selected) {
    const node = ensureOverlay();
    if (!candidate) { node.className = "xs-layer-overlay"; return; }
    const rect = visualRectOf(candidate);
    if (rect.width < 3 || rect.height < 3) { node.className = "xs-layer-overlay"; return; }
    node.style.left = Math.round(rect.left) + "px";
    node.style.top = Math.round(rect.top) + "px";
    node.style.width = Math.round(rect.width) + "px";
    node.style.height = Math.round(rect.height) + "px";
    node.className = "xs-layer-overlay is-visible" + (selected ? " is-selected" : "") + (candidate.structuralBorder ? " is-structural-line" : "");
  }
  function candidateAt(x, y) {
    const hits = document.elementsFromPoint(x, y).filter(el => !el.closest(ignored));
    const candidates = state.candidates.filter(candidate => {
      return hitCandidate(candidate, x, y)
        && (candidate.structuralBorder || hits.includes(candidate.el) || candidate.pseudo || (hits[0] && candidate.el.contains(hits[0])));
    });
    candidates.sort((a, b) => (visualRectOf(a).width * visualRectOf(a).height) - (visualRectOf(b).width * visualRectOf(b).height));
    return candidates[0] || null;
  }
  function select(candidate) {
    document.querySelectorAll(".xs-text-frame-selected").forEach(item => item.classList.remove("xs-text-frame-selected"));
    if (document.activeElement?.isContentEditable) document.activeElement.blur();
    state.selected = candidate;
    state.hover = candidate;
    placeOverlay(candidate, true);
    document.dispatchEvent(new CustomEvent("xs-edit:selection-change", { detail: { kind: "visual" } }));
  }
  function clearSelection() {
    state.selected = null;
    state.hover = null;
    placeOverlay(null, false);
    document.dispatchEvent(new CustomEvent("xs-edit:selection-change", { detail: { kind: "none" } }));
  }
  function edgeAt(event) {
    const handle = event.target.closest("[data-xs-layer-handle]")?.dataset.xsLayerHandle;
    return { move: handle === "top", left: handle === "left", right: handle === "right", bottom: handle === "bottom" };
  }
  function beginDrag(event) {
    if (!state.selected || event.button !== 0) return;
    const edge = edgeAt(event);
    if (!edge.move && !edge.left && !edge.right && !edge.bottom) return;
    event.preventDefault();
    event.stopPropagation();
    const current = readStore()[state.selected.key] || { x: 0, y: 0, sx: 1, sy: 1 };
    const rect = state.overlay.getBoundingClientRect();
    state.drag = { edge, startX: event.clientX, startY: event.clientY, rect, current };
    state.overlay.classList.add("xs-layer-dragging");
    state.overlay.setPointerCapture?.(event.pointerId);
    state.overlay.addEventListener("pointermove", dragMove);
    state.overlay.addEventListener("pointerup", endDrag, { once: true });
    state.overlay.addEventListener("pointercancel", endDrag, { once: true });
  }
  function dragMove(event) {
    if (!state.drag || !state.selected) return;
    const { edge, startX, startY, rect, current } = state.drag;
    const dx = event.clientX - startX;
    const dy = event.clientY - startY;
    const next = { ...current };
    if (edge.move) { next.x = Math.round((current.x || 0) + dx); next.y = Math.round((current.y || 0) + dy); }
    else {
      if (edge.left || edge.right) next.sx = Math.max(.1, Number(((rect.width + (edge.left ? -dx : dx)) / rect.width).toFixed(3)) * (current.sx || 1));
      if (edge.bottom) next.sy = Math.max(.1, Number(((rect.height + dy) / rect.height).toFixed(3)) * (current.sy || 1));
    }
    const store = readStore(); store[state.selected.key] = next; writeStore(store); renderOverrides(); placeOverlay(state.selected, true);
  }
  function endDrag() {
    const changed = Boolean(state.drag);
    state.overlay?.removeEventListener("pointermove", dragMove);
    state.overlay?.classList.remove("xs-layer-dragging");
    state.drag = null;
    if (changed) document.dispatchEvent(new CustomEvent("xs-edit:history-commit", { detail: { label: "图层调整" } }));
  }
  function activate() { state.active = true; scan(); renderOverrides(); }
  function deactivate() { state.active = false; clearSelection(); }
  function sync() { document.body.classList.contains("xs-editing") ? activate() : deactivate(); }
  document.addEventListener("pointermove", event => {
    if (!state.active || state.drag || event.target.closest(".xs-layer-overlay")) return;
    if (event.target.closest('[contenteditable="true"]')) {
      if (!state.selected) placeOverlay(null, false);
      return;
    }
    const candidate = candidateAt(event.clientX, event.clientY);
    if (state.selected) { placeOverlay(state.selected, true); return; }
    state.hover = candidate;
    placeOverlay(candidate, false);
  }, true);
  document.addEventListener("pointerdown", event => {
    if (!state.active || event.target.closest(ignored) || event.target.closest(".xs-layer-overlay")) return;
    if (event.target.closest('[contenteditable="true"]')) {
      clearSelection();
      return;
    }
    const candidate = candidateAt(event.clientX, event.clientY);
    if (!candidate) return clearSelection();
    select(candidate);
    event.preventDefault();
    event.stopPropagation();
  }, true);
  document.addEventListener("focusin", event => {
    if (state.active && event.target?.isContentEditable) clearSelection();
  }, true);
  document.addEventListener("xs-edit:reset", () => {
    localStorage.removeItem(STORE_KEY);
    localStorage.removeItem(LEGACY_STORE_KEY);
    renderOverrides();
    clearSelection();
  });
  document.addEventListener("xs-edit:history-apply", () => {
    scan();
    renderOverrides();
    clearSelection();
  });
  document.addEventListener("xs-edit:clear-visual-selection", clearSelection);
  document.addEventListener("xs-edit:delete-selected-object", event => {
    if (!state.selected) return;
    const store = readStore();
    store[state.selected.key] = { ...(store[state.selected.key] || {}), hidden: true };
    writeStore(store);
    renderOverrides();
    clearSelection();
    if (event.detail) event.detail.handled = true;
    event.preventDefault();
    document.dispatchEvent(new CustomEvent("xs-edit:history-commit", { detail: { label: "删除图层对象" } }));
  });
  new MutationObserver(sync).observe(document.body, { attributes: true, attributeFilter: ["class"] });
  scan();
  renderOverrides();
  sync();
})();
</script>
<!-- EDITABLE_HTML_PPT_EDIT_MODE_END -->
'''


def pptx_vendor_scripts() -> str:
    """Inline pinned browser dependencies so exported HTML stays self-contained."""
    vendor_dir = Path(__file__).resolve().parents[1] / "runtime" / "vendor"
    assets = (
        ("html-to-image-1.11.13.js", "editable-html-ppt-html-to-image"),
        ("jszip-3.10.1.min.js", "editable-html-ppt-jszip"),
        ("pptxgenjs-4.0.1.min.js", "editable-html-ppt-pptxgenjs"),
    )
    tags: list[str] = []
    for filename, script_id in assets:
        source_path = vendor_dir / filename
        if not source_path.is_file():
            raise FileNotFoundError(f"Missing bundled PPTX export dependency: {source_path}")
        source = source_path.read_text(encoding="utf-8")
        tags.append(
            f'<script id="{script_id}">\n'
            + source.replace("</script>", "<\\/script>")
            + "\n</script>"
        )
    return "\n".join(tags)


def build_snippet() -> str:
    return SNIPPET.replace(PPTX_VENDOR_PLACEHOLDER, pptx_vendor_scripts())


def inject_edit_mode(index_path: Path) -> bool:
    index_path = index_path.expanduser().resolve()
    if not index_path.exists():
        raise FileNotFoundError(f"Missing HTML file: {index_path}")

    html = index_path.read_text(encoding="utf-8", errors="replace")

    snippet = build_snippet()

    # Upgrade legacy Pretty HTML PPT injections rather than running two editors.
    if LEGACY_START in html and LEGACY_END in html:
        before, rest = html.split(LEGACY_START, 1)
        _, after = rest.split(LEGACY_END, 1)
        html = before + after

    # Replace existing injected block if present.
    if START in html and END in html:
        before, rest = html.split(START, 1)
        _, after = rest.split(END, 1)
        html = before + snippet.strip() + after
    elif "</body>" in html.lower():
        body_at = html.lower().rfind("</body>")
        html = html[:body_at] + "\n" + snippet + "\n" + html[body_at:]
    else:
        html = html + "\n" + snippet + "\n"

    index_path.write_text(html, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inject browser edit mode into an existing HTML PPT deck."
    )
    parser.add_argument("html", help="Path to index.html or another HTML file")
    args = parser.parse_args()
    inject_edit_mode(Path(args.html))
    print(Path(args.html).expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
