#!/usr/bin/env python3
"""Inject Pretty HTML PPT browser edit mode into an HTML deck.

Enhanced edition — supports text editing on all visible elements,
image / video replacement, and insert-new-media via the toolbar.
"""

from __future__ import annotations

import argparse
from pathlib import Path


START = "<!-- PRETTY_HTML_PPT_EDIT_MODE_START -->"
END = "<!-- PRETTY_HTML_PPT_EDIT_MODE_END -->"

SNIPPET = r'''
<!-- PRETTY_HTML_PPT_EDIT_MODE_START -->
<style id="pretty-html-ppt-edit-style">
  .xs-edit-toolbar {
    position: fixed;
    z-index: 2147483647;
    top: 14px;
    right: 14px;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    padding: 8px 10px;
    border-radius: 8px;
    border: 1px solid rgba(17, 24, 39, 0.14);
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(14px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    color: #111827;
    font: 12px/1.3 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
  }
  .xs-edit-toolbar.xs-dragging { user-select: none; cursor: grabbing; }
  .xs-edit-toolbar:not(.xs-collapsed) {
    top: 72px;
    width: min(390px, calc(100vw - 28px));
    align-items: center;
  }
  .xs-edit-toolbar.xs-collapsed {
    padding: 0;
    border: 0;
    background: transparent;
    box-shadow: none;
    backdrop-filter: none;
  }
  .xs-edit-toolbar.xs-collapsed > :not([data-xs-edit-toggle]) {
    display: none !important;
  }
  .xs-edit-toolbar button {
    appearance: none;
    border: 1px solid rgba(17, 24, 39, 0.16);
    background: #fff;
    color: #111827;
    padding: 6px 10px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
    transition: background 120ms ease, transform 120ms ease;
  }
  .xs-edit-toolbar button:hover { background: #f3f4f6; transform: translateY(-1px); }
  .xs-edit-toolbar button.xs-active {
    background: #111827;
    color: #fff;
    border-color: #111827;
  }
  .xs-edit-toolbar.xs-collapsed [data-xs-edit-toggle] {
    border-radius: 999px;
    box-shadow: 0 8px 22px rgba(17, 24, 39, 0.12);
  }
  .xs-edit-toolbar .xs-sep {
    width: 1px;
    background: rgba(17, 24, 39, 0.12);
    margin: 0 2px;
  }
  .xs-edit-toolbar .xs-font-control {
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }
  .xs-edit-toolbar .xs-font-control label {
    color: #4b5563;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
  }
  .xs-edit-toolbar .xs-font-control input {
    width: 52px;
    height: 28px;
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
  .xs-toolbar-drag {
    display: inline-grid;
    place-items: center;
    min-width: 26px;
    color: #6b7280;
    cursor: grab;
    touch-action: none;
    user-select: none;
    font-weight: 800;
  }
  .xs-toolbar-drag:active { cursor: grabbing; }

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
  .xs-editing .xs-object-selected {
    outline: 2px solid rgba(255, 79, 154, 0.95) !important;
    outline-offset: 4px !important;
  }

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

  /* Inserted text boxes */
  .xs-inserted-text-frame {
    position: absolute;
    z-index: 61;
    width: min(420px, 46vw);
    min-width: 160px;
    min-height: 56px;
    padding: 14px 16px;
    border: 1px solid rgba(17, 24, 39, .12);
    border-radius: 8px;
    background: rgba(255, 255, 255, .92);
    box-shadow: 0 14px 36px rgba(17, 24, 39, .12);
    box-sizing: border-box;
  }
  .xs-inserted-text-content {
    min-height: 1.4em;
    color: #111827;
    font: 600 24px/1.4 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    overflow-wrap: anywhere;
  }
  .xs-editing .xs-inserted-text-frame {
    outline: 1.5px dashed rgba(37, 99, 235, .72);
    outline-offset: 3px;
  }
  .xs-editing .xs-inserted-text-frame.is-selected {
    outline: 2px solid rgba(255, 79, 154, .95);
  }
  .xs-inserted-text-controls {
    position: absolute;
    left: 0;
    bottom: calc(100% + 7px);
    display: none;
    align-items: center;
    gap: 4px;
    padding: 5px;
    border: 1px solid rgba(17, 24, 39, .14);
    border-radius: 999px;
    background: rgba(255, 255, 255, .97);
    box-shadow: 0 10px 28px rgba(17, 24, 39, .14);
  }
  .xs-editing .xs-inserted-text-frame.is-selected .xs-inserted-text-controls { display: inline-flex; }
  .xs-inserted-text-controls button {
    appearance: none;
    border: 0;
    border-radius: 999px;
    background: transparent;
    color: #111827;
    padding: 5px 8px;
    font: 700 11px/1 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
    cursor: pointer;
  }
  .xs-inserted-text-controls button:hover { background: #f3f4f6; }
  .xs-inserted-text-controls [data-xs-text-drag] { cursor: grab; }
  .xs-inserted-text-controls [data-xs-text-delete] { color: #b91c1c; }
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
    bottom: 14px;
    padding: 8px 12px;
    border-radius: 6px;
    background: rgba(17, 24, 39, 0.92);
    color: #fff;
    font: 12px/1.3 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
    opacity: 0;
    transform: translateY(6px);
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

  @media print {
    .xs-edit-toolbar, .xs-toast, .xs-media-badge, .xs-modal-mask, .xs-insert-controls, .xs-insert-resize, .xs-inserted-text-controls, .xs-snap-guide { display: none !important; }
  }
</style>
<script id="pretty-html-ppt-edit-script">
(() => {
  const STORE_KEY = "pretty-html-ppt-edits:" + location.pathname;
  const STORE_VERSION = 2;
  const HISTORY_LIMIT = 20;

  /* ── Selectors ── */
  const textSelector = [
    "h1", "h2", "h3", "h4", "h5", "h6",
    "p", "li", "blockquote", "td", "th", "figcaption", "caption",
    "span", "a", "label", "strong", "em", "small", "code", "dt", "dd",
    "summary", "legend", "pre",
    "[data-editable]", ".editable"
  ].join(",");

  const blockedSelector = [
    "script", "style", "svg", "canvas", "video", "audio",
    "button", "nav", "input", "textarea", "select", "option",
    "[data-no-edit]", ".xs-edit-toolbar", ".xs-toast", ".xs-modal-mask",
    ".xs-media-badge", ".xs-insert-controls", ".xs-inserted-text-frame", ".xs-snap-guide"
  ].join(",");

  /* ── Blacklist: parent tags whose children should NOT get contenteditable ── */
  const blacklistParents = new Set(["svg", "canvas", "video", "audio", "script", "style",
    "button", "nav", "input", "textarea", "select"]);

  /* ── State ── */
  let editing = false;
  let toastTimer = null;
  let currentTextEl = null;
  let currentImageFrame = null;
  let insertedFrameCounter = 0;
  let insertedTextCounter = 0;
  let historyApplying = false;
  let historyTimer = null;
  const undoStack = [];
  const redoStack = [];

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
      const parsed = JSON.parse(localStorage.getItem(STORE_KEY) || "{}");
      if (parsed && parsed.version === STORE_VERSION && parsed.data && typeof parsed.data === "object") {
        return parsed.data;
      }
      // Version 1 stored the edit map directly. Keep reading it until the next save migrates it.
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch { return {}; }
  }
  function writeStore(data) {
    localStorage.setItem(STORE_KEY, JSON.stringify({ version: STORE_VERSION, data }));
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
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => node.classList.remove("is-visible"), 1800);
  }

  function nextFrameId() {
    insertedFrameCounter += 1;
    return "m" + Date.now() + "-" + insertedFrameCounter;
  }

  function nextTextFrameId() {
    insertedTextCounter += 1;
    return "x" + Date.now() + "-" + insertedTextCounter;
  }

  /* ── Restore ── */
  function restoreAll(sourceData) {
    const data = sourceData || readStore();
    document.querySelectorAll('[data-xs-edit-id][data-xs-hidden="true"]').forEach(el => {
      el.style.removeProperty("display");
      delete el.dataset.xsHidden;
    });
    getTextCandidates().forEach(el => {
      const v = data[el.dataset.xsEditId];
      if (v !== undefined) {
        if (typeof v === "string") {
          el.innerHTML = v;
        } else {
          if (v.html !== undefined) el.innerHTML = v.html;
          if (v.fontSize) el.style.fontSize = v.fontSize;
          else el.style.removeProperty("font-size");
          if (v.lineHeight) el.style.lineHeight = v.lineHeight;
          else el.style.removeProperty("line-height");
        }
      }
    });
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
    const hiddenIds = Array.isArray(data.__xsHiddenIds) ? data.__xsHiddenIds : [];
    hiddenIds.forEach(id => {
      const el = document.querySelector('[data-xs-edit-id="' + CSS.escape(id) + '"]');
      if (!el) return;
      el.style.display = "none";
      el.dataset.xsHidden = "true";
    });
    restoreInsertedFrames(data);
    restoreInsertedTextFrames(data);
  }

  /* ── Save ── */
  function saveAll() {
    const data = captureStoreData();
    writeStore(data);
    toast("已保存到本机浏览器");
    commitHistory("保存");
  }

  /* ── Toggle editing ── */
  function enterEdit() {
    editing = true;
    document.body.classList.add("xs-editing");
    getTextCandidates().forEach(el => {
      el.setAttribute("contenteditable", "true");
      el.setAttribute("spellcheck", "false");
    });
    document.querySelectorAll(".xs-inserted-text-content").forEach(el => {
      el.setAttribute("contenteditable", "true");
      el.setAttribute("spellcheck", "false");
    });
    attachMediaBadges();
    updateToggleBtn();
    updateFontControls();
    toast("编辑模式已开启 — 点任意文字即可修改，点图片/视频可替换");
  }

  function exitEdit() {
    editing = false;
    document.body.classList.remove("xs-editing");
    getTextCandidates().forEach(el => {
      el.removeAttribute("contenteditable");
      el.removeAttribute("spellcheck");
    });
    document.querySelectorAll(".xs-inserted-text-content").forEach(el => {
      el.removeAttribute("contenteditable");
      el.removeAttribute("spellcheck");
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

  function setToolbarExpanded(expanded) {
    const bar = document.querySelector(".xs-edit-toolbar");
    if (!bar) return;
    bar.classList.toggle("xs-collapsed", !expanded);
  }

  function makeToolbarDraggable(bar) {
    const handle = bar.querySelector("[data-xs-toolbar-drag]");
    if (!handle) return;
    handle.addEventListener("pointerdown", event => {
      if (bar.classList.contains("xs-collapsed")) return;
      event.preventDefault();
      const rect = bar.getBoundingClientRect();
      const offsetX = event.clientX - rect.left;
      const offsetY = event.clientY - rect.top;
      bar.classList.add("xs-dragging");
      handle.setPointerCapture?.(event.pointerId);
      const move = moveEvent => {
        const left = clamp(moveEvent.clientX - offsetX, 8, Math.max(8, window.innerWidth - bar.offsetWidth - 8));
        const top = clamp(moveEvent.clientY - offsetY, 8, Math.max(8, window.innerHeight - bar.offsetHeight - 8));
        bar.style.left = Math.round(left) + "px";
        bar.style.top = Math.round(top) + "px";
        bar.style.right = "auto";
      };
      const up = () => {
        bar.classList.remove("xs-dragging");
        handle.removeEventListener("pointermove", move);
        handle.removeEventListener("pointerup", up);
        handle.removeEventListener("pointercancel", up);
      };
      handle.addEventListener("pointermove", move);
      handle.addEventListener("pointerup", up);
      handle.addEventListener("pointercancel", up);
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
    const inserted = target?.closest?.(".xs-inserted-text-content");
    if (inserted) return inserted;
    const el = target?.closest?.(textSelector);
    return isTextCandidate(el) ? el : null;
  }

  function isEditableTextTarget(el) {
    return isTextCandidate(el) || !!el?.classList?.contains("xs-inserted-text-content");
  }

  function setCurrentTextEl(el) {
    if (!isEditableTextTarget(el)) return;
    document.querySelectorAll(".xs-object-selected").forEach(item => {
      if (item !== el) item.classList.remove("xs-object-selected");
    });
    currentTextEl = el;
    el.classList.add("xs-object-selected");
    updateFontControls();
  }

  function getCurrentTextEl() {
    if (isEditableTextTarget(document.activeElement)) return document.activeElement;
    if (isEditableTextTarget(currentTextEl)) return currentTextEl;
    return null;
  }

  function getFontPx(el) {
    const size = window.getComputedStyle(el).fontSize;
    const value = Number.parseFloat(size);
    return Number.isFinite(value) ? Math.round(value) : 16;
  }

  function updateFontControls() {
    const input = document.querySelector("[data-xs-font-size]");
    const lineInput = document.querySelector("[data-xs-line-height]");
    const buttons = document.querySelectorAll("[data-xs-font-minus], [data-xs-font-plus], [data-xs-font-reset], [data-xs-line-minus], [data-xs-line-plus], [data-xs-line-reset]");
    const deleteButton = document.querySelector("[data-xs-delete-object]");
    if (!input) return;
    const el = getCurrentTextEl();
    input.disabled = !editing || !el;
    if (lineInput) lineInput.disabled = !editing || !el;
    buttons.forEach(btn => { btn.disabled = !editing || !el; });
    if (deleteButton) deleteButton.disabled = !editing || (!el && !currentImageFrame);
    input.value = el ? String(getFontPx(el)) : "";
    if (lineInput) lineInput.value = el ? String(getLineHeight(el)) : "";
  }

  function persistTextElement(el) {
    if (el.closest(".xs-inserted-text-frame")) {
      persistInsertedTextFrames();
      return;
    }
    const store = readStore();
    store[el.dataset.xsEditId] = {
      html: el.innerHTML,
      fontSize: el.style.fontSize || "",
      lineHeight: el.style.lineHeight || ""
    };
    writeStore(store);
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
    persistTextElement(el);
    commitHistory("调整字号");
    toast("字号已调整，Cmd+S 保存或导出 HTML");
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
    persistTextElement(el);
    commitHistory("恢复字号");
    toast("字号已恢复为模板默认值");
  }

  function getLineHeight(el) {
    const computed = window.getComputedStyle(el);
    const fontSize = Number.parseFloat(computed.fontSize) || 16;
    const lineHeight = Number.parseFloat(computed.lineHeight);
    return Number.isFinite(lineHeight) ? Number((lineHeight / fontSize).toFixed(2)) : 1.4;
  }

  function applyLineHeight(value) {
    if (!editing) return toast("请先点击「编辑」进入编辑模式");
    const el = getCurrentTextEl();
    if (!el) return toast("请先点选一段文字，再调整行距");
    const next = Math.max(.8, Math.min(3, Number(value.toFixed(2))));
    el.style.lineHeight = String(next);
    persistTextElement(el);
    updateFontControls();
    commitHistory("调整行距");
    toast("行距已调整");
  }

  function changeLineHeight(delta) {
    const el = getCurrentTextEl();
    if (!el) return toast("请先点选一段文字，再调整行距");
    applyLineHeight(getLineHeight(el) + delta);
  }

  function resetLineHeight() {
    const el = getCurrentTextEl();
    if (!el) return toast("请先点选一段文字，再恢复行距");
    el.style.removeProperty("line-height");
    persistTextElement(el);
    updateFontControls();
    commitHistory("恢复行距");
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
        commitHistory(isImg ? "替换图片" : "替换视频");
        toast("已替换，Cmd+S 保存");
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
    const slides = [...document.querySelectorAll("[data-slide], main > section, main > article, section[id], article[id]")]
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
    return node?.closest?.("[data-slide], main > section, main > article, section[id], article[id], main")
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

  function captureStoreData() {
    ensureIds();
    const data = {};
    getTextCandidates().forEach(el => {
      data[el.dataset.xsEditId] = {
        html: el.innerHTML,
        fontSize: el.style.fontSize || "",
        lineHeight: el.style.lineHeight || ""
      };
    });
    [...document.querySelectorAll('img[data-xs-edit-id], video[data-xs-edit-id]')].forEach(el => {
      const src = el.tagName === "VIDEO"
        ? ((el.querySelector("source") || el).src || "")
        : el.src;
      if (src) data[el.dataset.xsEditId] = src;
    });
    data.__xsInsertedFrames = collectInsertedFrames();
    data.__xsInsertedTextFrames = collectInsertedTextFrames();
    data.__xsHiddenIds = [...document.querySelectorAll('[data-xs-edit-id][data-xs-hidden="true"]')]
      .map(el => el.dataset.xsEditId)
      .filter(Boolean);
    return data;
  }

  function snapshotString(data = captureStoreData()) {
    return JSON.stringify(data);
  }

  function updateHistoryControls() {
    const undo = document.querySelector("[data-xs-undo]");
    const redo = document.querySelector("[data-xs-redo]");
    if (undo) undo.disabled = undoStack.length <= 1;
    if (redo) redo.disabled = redoStack.length === 0;
  }

  function commitHistory(label = "编辑") {
    if (historyApplying) return;
    clearTimeout(historyTimer);
    const next = snapshotString();
    if (undoStack[undoStack.length - 1] === next) return updateHistoryControls();
    undoStack.push(next);
    if (undoStack.length > HISTORY_LIMIT) undoStack.shift();
    redoStack.length = 0;
    updateHistoryControls();
    document.dispatchEvent(new CustomEvent("pretty-html-ppt:history", { detail: { label } }));
  }

  function scheduleHistory(label) {
    clearTimeout(historyTimer);
    historyTimer = setTimeout(() => commitHistory(label), 450);
  }

  function applyHistorySnapshot(serialized) {
    historyApplying = true;
    try {
      const data = JSON.parse(serialized);
      document.querySelectorAll(".xs-inserted-frame, .xs-inserted-text-frame").forEach(el => el.remove());
      currentImageFrame = null;
      currentTextEl = null;
      restoreAll(data);
      writeStore(data);
      if (editing) {
        document.querySelectorAll(".xs-inserted-text-content").forEach(el => {
          el.setAttribute("contenteditable", "true");
          el.setAttribute("spellcheck", "false");
        });
      }
    } finally {
      historyApplying = false;
      updateFontControls();
      updateHistoryControls();
    }
  }

  function undoEdit() {
    if (undoStack.length <= 1) return toast("已经是最早一步");
    redoStack.push(undoStack.pop());
    applyHistorySnapshot(undoStack[undoStack.length - 1]);
    toast("已撤销");
  }

  function redoEdit() {
    if (!redoStack.length) return toast("没有可恢复的操作");
    const next = redoStack.pop();
    undoStack.push(next);
    applyHistorySnapshot(next);
    toast("已恢复");
  }

  function persistInsertedFrames() {
    const store = readStore();
    store.__xsInsertedFrames = collectInsertedFrames();
    writeStore(store);
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

  function collectInsertedTextFrames() {
    const slides = slideContainers();
    return [...document.querySelectorAll(".xs-inserted-text-frame")].map(frame => {
      const content = frame.querySelector(".xs-inserted-text-content");
      return {
        id: frame.dataset.xsEditId || "",
        parentIndex: Math.max(0, slides.indexOf(frame.parentElement)),
        html: content?.innerHTML || "",
        style: {
          left: frame.style.left || "",
          top: frame.style.top || "",
          width: frame.style.width || "",
          zIndex: frame.style.zIndex || "",
          fontSize: content?.style.fontSize || "",
          lineHeight: content?.style.lineHeight || ""
        }
      };
    });
  }

  function persistInsertedTextFrames() {
    const store = readStore();
    store.__xsInsertedTextFrames = collectInsertedTextFrames();
    writeStore(store);
  }

  function selectTextFrame(frame) {
    document.querySelectorAll(".xs-inserted-text-frame.is-selected").forEach(item => {
      if (item !== frame) item.classList.remove("is-selected");
    });
    document.querySelectorAll(".xs-inserted-frame.is-selected").forEach(item => item.classList.remove("is-selected"));
    currentImageFrame = null;
    frame.classList.add("is-selected");
    const content = frame.querySelector(".xs-inserted-text-content");
    if (content) setCurrentTextEl(content);
  }

  function deleteTextFrame(frame) {
    if (!frame?.classList?.contains("xs-inserted-text-frame")) return;
    frame.remove();
    currentTextEl = null;
    persistInsertedTextFrames();
    commitHistory("删除文本框");
    updateFontControls();
    toast("文本框已删除");
  }

  function attachTextFrameEvents(frame) {
    if (frame.dataset.xsTextFrameReady === "true") return;
    frame.dataset.xsTextFrameReady = "true";
    const content = frame.querySelector(".xs-inserted-text-content");
    frame.addEventListener("click", event => {
      if (!editing) return;
      event.stopPropagation();
      selectTextFrame(frame);
    });
    content?.addEventListener("input", () => {
      persistInsertedTextFrames();
      scheduleHistory("编辑文本框");
    });
    frame.querySelector("[data-xs-text-delete]")?.addEventListener("click", event => {
      event.preventDefault();
      event.stopPropagation();
      deleteTextFrame(frame);
    });
    const dragHandle = frame.querySelector("[data-xs-text-drag]");
    dragHandle?.addEventListener("pointerdown", event => {
      if (!editing) return;
      event.preventDefault();
      event.stopPropagation();
      selectTextFrame(frame);
      const { parentRect, rect } = frameMetrics(frame);
      const offsetX = event.clientX - rect.left;
      const offsetY = event.clientY - rect.top;
      dragHandle.setPointerCapture?.(event.pointerId);
      const move = moveEvent => {
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
        dragHandle.removeEventListener("pointermove", move);
        dragHandle.removeEventListener("pointerup", up);
        dragHandle.removeEventListener("pointercancel", up);
        persistInsertedTextFrames();
        commitHistory("移动文本框");
      };
      dragHandle.addEventListener("pointermove", move);
      dragHandle.addEventListener("pointerup", up);
      dragHandle.addEventListener("pointercancel", up);
    });
  }

  function createInsertedTextFrame(container, options = {}) {
    const parent = prepareImageCanvas(container || activeSlideContainer());
    const frame = document.createElement("div");
    frame.className = "xs-inserted-text-frame";
    frame.dataset.xsEditId = options.id || nextTextFrameId();
    frame.innerHTML = [
      '<div class="xs-inserted-text-controls" data-no-edit="true">',
      '  <button type="button" data-xs-text-drag title="拖动文本框">移动</button>',
      '  <button type="button" data-xs-text-delete title="删除文本框">删除</button>',
      '</div>',
      '<div class="xs-inserted-text-content">双击这里输入文字</div>'
    ].join("");
    const style = options.style || {};
    frame.style.left = style.left || "8%";
    frame.style.width = style.width || "min(420px, 46vw)";
    if (style.zIndex) frame.style.zIndex = style.zIndex;
    const content = frame.querySelector(".xs-inserted-text-content");
    content.innerHTML = options.html || "双击这里输入文字";
    if (style.fontSize) content.style.fontSize = style.fontSize;
    if (style.lineHeight) content.style.lineHeight = style.lineHeight;
    if (editing) {
      content.setAttribute("contenteditable", "true");
      content.setAttribute("spellcheck", "false");
    }
    parent.appendChild(frame);
    if (style.top) {
      frame.style.top = style.top;
    } else {
      const parentRect = parent.getBoundingClientRect();
      const maxTop = Math.max(28, parentRect.height - frame.getBoundingClientRect().height - 28);
      frame.style.top = Math.round(clamp(-parentRect.top + window.innerHeight * .28, 28, maxTop)) + "px";
    }
    attachTextFrameEvents(frame);
    if (!options.restored) {
      selectTextFrame(frame);
      persistInsertedTextFrames();
      commitHistory("插入文本框");
      requestAnimationFrame(() => content.focus({ preventScroll: true }));
    }
    return frame;
  }

  function restoreInsertedTextFrames(data) {
    const frames = Array.isArray(data.__xsInsertedTextFrames) ? data.__xsInsertedTextFrames : [];
    const slides = slideContainers();
    frames.forEach(item => {
      if (item.id && document.querySelector('.xs-inserted-text-frame[data-xs-edit-id="' + CSS.escape(item.id) + '"]')) return;
      createInsertedTextFrame(slides[item.parentIndex] || activeSlideContainer(), {
        id: item.id,
        html: item.html || "",
        style: item.style || {},
        restored: true
      });
    });
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
    const visibleCenterTop = clamp(-parentRect.top + window.innerHeight / 2 - rect.height / 2, pad, maxTop);
    const visibleBottomTop = clamp(-parentRect.top + window.innerHeight - rect.height - 40, pad, maxTop);
    const positions = {
      left: { left: pad, top: visibleCenterTop },
      center: { left: Math.max(pad, (parentRect.width - rect.width) / 2), top: visibleCenterTop },
      right: { left: maxLeft, top: visibleCenterTop },
      bottom: { left: Math.max(pad, (parentRect.width - rect.width) / 2), top: visibleBottomTop },
    };
    const pos = positions[placement] || positions.right;
    frame.style.left = Math.round(pos.left) + "px";
    frame.style.top = Math.round(pos.top) + "px";
    selectFrame(frame);
    persistInsertedFrames();
  }

  function selectFrame(frame) {
    document.querySelectorAll(".xs-inserted-frame.is-selected").forEach(item => {
      if (item !== frame) item.classList.remove("is-selected");
    });
    document.querySelectorAll(".xs-inserted-text-frame.is-selected, .xs-object-selected").forEach(item => item.classList.remove("is-selected", "xs-object-selected"));
    currentTextEl = null;
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
    persistInsertedFrames();
    commitHistory("删除图片");
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
    persistInsertedFrames();
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
        persistInsertedFrames();
        commitHistory("移动图片");
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
        commitHistory("调整图片尺寸");
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
        persistInsertedFrames();
        commitHistory("调整图片尺寸");
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
      if (!options.restored) commitHistory("插入图片");
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
    toast("已清除本机修改，刷新后恢复模板内容");
  }

  function deleteSelectedObject() {
    if (currentImageFrame?.isConnected) return deleteFrame(currentImageFrame);
    const textFrame = currentTextEl?.closest?.(".xs-inserted-text-frame");
    if (textFrame) return deleteTextFrame(textFrame);
    const el = getCurrentTextEl();
    if (!el?.dataset?.xsEditId) return toast("请先点选要删除的文字或对象");
    el.style.display = "none";
    el.dataset.xsHidden = "true";
    currentTextEl = null;
    const store = captureStoreData();
    writeStore(store);
    commitHistory("删除对象");
    updateFontControls();
    toast("对象已隐藏，可用撤销恢复");
  }

  /* ── Export ── */
  function exportHtml() {
    saveAll();
    const clone = document.documentElement.cloneNode(true);
    clone.querySelectorAll("[contenteditable], [spellcheck]").forEach(el => {
      el.removeAttribute("contenteditable");
      el.removeAttribute("spellcheck");
    });
    clone.querySelectorAll(".xs-edit-toolbar, .xs-toast, .xs-media-wrapper, .xs-media-badge, .xs-modal-mask, .xs-insert-controls, .xs-insert-resize, .xs-inserted-text-controls, .xs-snap-guide")
      .forEach(el => el.remove());
    clone.querySelectorAll(".xs-inserted-frame").forEach(frame => {
      frame.classList.remove("is-selected");
      frame.removeAttribute("tabindex");
      delete frame.dataset.xsFrameReady;
    });
    clone.querySelectorAll(".xs-inserted-text-frame").forEach(frame => {
      frame.classList.remove("is-selected");
      delete frame.dataset.xsTextFrameReady;
    });
    clone.querySelectorAll(".xs-object-selected").forEach(el => el.classList.remove("xs-object-selected"));
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
    a.download = (document.title || "pretty-html-ppt").replace(/[\\/:*?"<>|]+/g, "-") + "-edited.html";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    toast("已导出 HTML 文件");
  }

  /* ── Toolbar ── */
  function buildToolbar() {
    if (document.querySelector(".xs-edit-toolbar")) return;
    const bar = document.createElement("div");
    bar.className = "xs-edit-toolbar xs-collapsed";
    bar.setAttribute("data-no-edit", "true");
    bar.innerHTML = [
      '<button type="button" data-xs-edit-toggle>编辑</button>',
      '<span class="xs-toolbar-drag" data-xs-toolbar-drag title="拖动工具栏">⋮⋮</span>',
      '<button type="button" data-xs-undo title="撤销最近一步" disabled>↶</button>',
      '<button type="button" data-xs-redo title="恢复最近撤销" disabled>↷</button>',
      '<span class="xs-sep"></span>',
      '<span class="xs-font-control" title="先点选文字，再调整字号">',
      '  <label for="xsFontSizeInput">字号</label>',
      '  <button type="button" data-xs-font-minus title="减小字号">A-</button>',
      '  <input id="xsFontSizeInput" type="number" min="8" max="160" step="1" data-xs-font-size disabled>',
      '  <button type="button" data-xs-font-plus title="增大字号">A+</button>',
      '  <button type="button" data-xs-font-reset title="恢复模板默认字号">默认</button>',
      '</span>',
      '<span class="xs-font-control" title="先点选文字，再调整行距">',
      '  <label for="xsLineHeightInput">行距</label>',
      '  <button type="button" data-xs-line-minus title="减小行距">−</button>',
      '  <input id="xsLineHeightInput" type="number" min="0.8" max="3" step="0.1" data-xs-line-height disabled>',
      '  <button type="button" data-xs-line-plus title="增大行距">+</button>',
      '  <button type="button" data-xs-line-reset title="恢复模板默认行距">默认</button>',
      '</span>',
      '<span class="xs-sep"></span>',
      '<button type="button" data-xs-edit-save>保存</button>',
      '<button type="button" data-xs-edit-export>导出 HTML</button>',
      '<button type="button" data-xs-edit-reset>重置</button>',
      '<span class="xs-sep"></span>',
      '<button type="button" data-xs-edit-insert-text title="在当前页面插入独立文本框">＋文本</button>',
      '<button type="button" data-xs-edit-insert-img title="插入一张图片到当前页面">＋图片</button>',
      '<button type="button" data-xs-delete-object title="删除当前选中对象" disabled>删除</button>',
      '<button type="button" data-xs-edit-collapse title="收起工具栏">收起</button>'
    ].join("");
    document.body.appendChild(bar);
    bar.querySelector("[data-xs-edit-toggle]").addEventListener("click", () => {
      if (bar.classList.contains("xs-collapsed")) {
        setToolbarExpanded(true);
        toggleEdit(true);
      } else {
        toggleEdit();
      }
    });
    bar.querySelector("[data-xs-edit-save]").addEventListener("click", saveAll);
    bar.querySelector("[data-xs-edit-export]").addEventListener("click", exportHtml);
    bar.querySelector("[data-xs-edit-reset]").addEventListener("click", resetAll);
    bar.querySelector("[data-xs-font-minus]").addEventListener("click", () => changeFontSize(-2));
    bar.querySelector("[data-xs-font-plus]").addEventListener("click", () => changeFontSize(2));
    bar.querySelector("[data-xs-font-reset]").addEventListener("click", resetFontSize);
    bar.querySelector("[data-xs-undo]").addEventListener("click", undoEdit);
    bar.querySelector("[data-xs-redo]").addEventListener("click", redoEdit);
    bar.querySelector("[data-xs-line-minus]").addEventListener("click", () => changeLineHeight(-.1));
    bar.querySelector("[data-xs-line-plus]").addEventListener("click", () => changeLineHeight(.1));
    bar.querySelector("[data-xs-line-reset]").addEventListener("click", resetLineHeight);
    bar.querySelector("[data-xs-delete-object]").addEventListener("click", deleteSelectedObject);
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
    bar.querySelector("[data-xs-line-height]").addEventListener("change", event => {
      const value = Number.parseFloat(event.target.value);
      if (Number.isFinite(value)) applyLineHeight(value);
    });
    bar.querySelector("[data-xs-edit-insert-text]").addEventListener("click", () => {
      if (!editing) return toast("请先点击「编辑」进入编辑模式");
      createInsertedTextFrame(activeSlideContainer());
    });
    bar.querySelector("[data-xs-edit-insert-img]").addEventListener("click", () => {
      if (!editing) { toast("请先点击「编辑」进入编辑模式"); return; }
      openInsertModal();
    });
    bar.querySelector("[data-xs-edit-collapse]").addEventListener("click", () => {
      if (editing) exitEdit();
      setToolbarExpanded(false);
    });
    makeToolbarDraggable(bar);
    updateHistoryControls();
  }

  document.addEventListener("focusin", (event) => {
    const el = fontTargetFromEventTarget(event.target);
    if (el) setCurrentTextEl(el);
  });

  document.addEventListener("input", event => {
    const el = fontTargetFromEventTarget(event.target);
    if (!editing || !el) return;
    scheduleHistory("编辑文字");
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

  /* ── Keyboard ── */
  document.addEventListener("keydown", (event) => {
    const key = event.key.toLowerCase();
    const tag = document.activeElement?.tagName?.toLowerCase();
    const typing = tag === "input" || tag === "textarea" || tag === "select" || document.activeElement?.isContentEditable;
    if (editing && !typing && (event.metaKey || event.ctrlKey) && key === "z") {
      event.preventDefault();
      event.shiftKey ? redoEdit() : undoEdit();
      return;
    }
    if (editing && !typing && (event.metaKey || event.ctrlKey) && key === "y") {
      event.preventDefault();
      redoEdit();
      return;
    }
    if (editing && currentImageFrame && !typing && (key === "delete" || key === "backspace")) {
      event.preventDefault();
      deleteFrame(currentImageFrame);
      return;
    }
    if (editing && !typing && (key === "delete" || key === "backspace") && getCurrentTextEl()) {
      event.preventDefault();
      deleteSelectedObject();
      return;
    }
    /* E enters edit mode; Esc exits. E never toggles while editing. */
    if (!editing && !typing && key === "e" && !event.metaKey && !event.ctrlKey && !event.altKey) {
      event.preventDefault();
      setToolbarExpanded(true);
      enterEdit();
    }
    if (key === "s" && (event.metaKey || event.ctrlKey)) {
      if (editing) { event.preventDefault(); saveAll(); }
    }
    if (key === "escape" && editing) {
      if (document.querySelector(".xs-modal-mask.is-open")) return;
      exitEdit();
    }
  });

  /* ── Init ── */
  ensureIds();
  restoreAll();
  buildToolbar();
  document.querySelectorAll(".xs-inserted-frame").forEach(attachFrameEvents);
  document.querySelectorAll(".xs-inserted-text-frame").forEach(attachTextFrameEvents);
  undoStack.push(snapshotString());
  updateHistoryControls();
})();
</script>
<!-- PRETTY_HTML_PPT_EDIT_MODE_END -->
'''


def inject_edit_mode(index_path: Path) -> bool:
    index_path = index_path.expanduser().resolve()
    if not index_path.exists():
        raise FileNotFoundError(f"Missing HTML file: {index_path}")

    html = index_path.read_text(encoding="utf-8", errors="replace")

    # Replace existing injected block if present
    if START in html and END in html:
        before, rest = html.split(START, 1)
        _, after = rest.split(END, 1)
        html = before + SNIPPET.strip() + after
    elif "</body>" in html.lower():
        body_at = html.lower().rfind("</body>")
        html = html[:body_at] + "\n" + SNIPPET + "\n" + html[body_at:]
    else:
        html = html + "\n" + SNIPPET + "\n"

    index_path.write_text(html, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inject browser edit mode into a Pretty HTML PPT deck."
    )
    parser.add_argument("html", help="Path to index.html or another HTML file")
    args = parser.parse_args()
    inject_edit_mode(Path(args.html))
    print(Path(args.html).expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
