#!/usr/bin/env python3
"""Inject XiaoShui Pretty PPT browser edit mode into an HTML deck.

Enhanced edition — supports text editing on all visible elements,
image / video replacement, and insert-new-media via the toolbar.
"""

from __future__ import annotations

import argparse
from pathlib import Path


START = "<!-- XIAOSHUI_PPT_EDIT_MODE_START -->"
END = "<!-- XIAOSHUI_PPT_EDIT_MODE_END -->"

SNIPPET = r'''
<!-- XIAOSHUI_PPT_EDIT_MODE_START -->
<style id="xiaoshui-edit-style">
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

  /* Toast */
  .xs-toast {
    position: fixed;
    z-index: 2147483647;
    right: 14px;
    top: 62px;
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
    display: block;
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
  .xs-modal .xs-file-upload:hover {
    border-color: #2563eb;
    background: #f0f4ff;
  }
  .xs-modal .xs-file-upload input { display: none; }

  @media print {
    .xs-edit-toolbar, .xs-toast, .xs-media-badge, .xs-modal-mask { display: none !important; }
  }
</style>
<script id="xiaoshui-edit-script">
(() => {
  const STORE_KEY = "xiaoshui-ppt-edits:" + location.pathname;

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
    ".xs-media-badge"
  ].join(",");

  /* ── Blacklist: parent tags whose children should NOT get contenteditable ── */
  const blacklistParents = new Set(["svg", "canvas", "video", "audio", "script", "style",
    "button", "nav", "input", "textarea", "select"]);

  /* ── State ── */
  let editing = false;
  let toastTimer = null;
  let currentTextEl = null;

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
      .filter(el => !el.closest(".xs-media-wrapper") && !el.closest(".xs-modal-mask"));
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
    try { return JSON.parse(localStorage.getItem(STORE_KEY) || "{}"); } catch { return {}; }
  }
  function writeStore(data) {
    localStorage.setItem(STORE_KEY, JSON.stringify(data));
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

  /* ── Restore ── */
  function restoreAll() {
    const data = readStore();
    getTextCandidates().forEach(el => {
      const v = data[el.dataset.xsEditId];
      if (v !== undefined) {
        if (typeof v === "string") {
          el.innerHTML = v;
        } else {
          if (v.html !== undefined) el.innerHTML = v.html;
          if (v.fontSize) el.style.fontSize = v.fontSize;
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
  }

  /* ── Save ── */
  function saveAll() {
    ensureIds();
    const data = {};
    getTextCandidates().forEach(el => {
      data[el.dataset.xsEditId] = {
        html: el.innerHTML,
        fontSize: el.style.fontSize || ""
      };
    });
    getMediaCandidates().forEach(el => {
      const src = (el.tagName === "VIDEO")
        ? ((el.querySelector("source") || el).src || "")
        : el.src;
      if (src) data[el.dataset.xsEditId] = src;
    });
    writeStore(data);
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
    updateFontControls();
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

  function updateFontControls() {
    const input = document.querySelector("[data-xs-font-size]");
    const buttons = document.querySelectorAll("[data-xs-font-minus], [data-xs-font-plus], [data-xs-font-reset]");
    if (!input) return;
    const el = getCurrentTextEl();
    input.disabled = !editing || !el;
    buttons.forEach(btn => { btn.disabled = !editing || !el; });
    input.value = el ? String(getFontPx(el)) : "";
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
    store[el.dataset.xsEditId] = {
      html: el.innerHTML,
      fontSize: el.style.fontSize || ""
    };
    writeStore(store);
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
    const store = readStore();
    store[el.dataset.xsEditId] = {
      html: el.innerHTML,
      fontSize: ""
    };
    writeStore(store);
    toast("字号已恢复为模板默认值");
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
      + '<input type="url" class="xs-new-url" placeholder="https://...">'
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
    mask.querySelector(".xs-btn-cancel").addEventListener("click", closeModal);
    mask.querySelector(".xs-btn-apply").addEventListener("click", apply);
    mask.querySelector("#xsFileInput").addEventListener("change", () => {
      const f = mask.querySelector("#xsFileInput").files[0];
      if (f) mask.querySelector(".xs-new-url").placeholder = f.name;
    });
    mask.querySelector(".xs-new-url").addEventListener("keydown", (e) => {
      if (e.key === "Enter") apply();
    });
    setTimeout(() => mask.querySelector(".xs-new-url").focus(), 120);
  }

  /* ── Insert image ── */
  function openInsertModal() {
    const mask = document.createElement("div");
    mask.className = "xs-modal-mask is-open";
    mask.innerHTML = '<div class="xs-modal">'
      + '<h3>插入图片</h3>'
      + '<label>图片地址 (URL)</label>'
      + '<input type="url" class="xs-new-url" placeholder="https://...">'
      + '<label style="margin-top:14px;">图片说明 (alt)</label>'
      + '<input type="text" class="xs-new-alt" placeholder="图片描述文字">'
      + '<div class="xs-file-upload" id="xsFileUpload">'
      + '  或 点击上传本地图片'
      + '  <input type="file" id="xsFileInput" accept="image/*">'
      + '</div>'
      + '<div class="xs-modal-actions">'
      + '  <button class="xs-btn-cancel">取消</button>'
      + '  <button class="xs-btn-primary xs-btn-apply">插入</button>'
      + '</div>'
      + '</div>';
    document.body.appendChild(mask);

    const closeModal = () => { mask.remove(); };
    const apply = () => {
      const newUrl = mask.querySelector(".xs-new-url").value.trim();
      const alt = mask.querySelector(".xs-new-alt").value.trim();
      const fileInput = mask.querySelector("#xsFileInput");
      const file = fileInput.files[0];

      const doInsert = (url) => {
        const img = document.createElement("img");
        img.src = url;
        if (alt) img.alt = alt;
        img.style.maxWidth = "100%";
        img.style.display = "block";
        img.style.margin = "12px 0";
        img.dataset.xsEditId = "m" + Date.now();

        const active = document.activeElement;
        if (active && active.isContentEditable && active !== document.body) {
          active.appendChild(img);
        } else {
          const lastSlide = document.querySelector(".slide-card:last-of-type, .deck-section:last-of-type, main");
          if (lastSlide) lastSlide.appendChild(img);
          else document.body.appendChild(img);
        }

        const store = readStore();
        store[img.dataset.xsEditId] = url;
        writeStore(store);
        toast("图片已插入，Cmd+S 保存");
      };

      if (file) {
        const reader = new FileReader();
        reader.onload = () => doInsert(reader.result);
        reader.readAsDataURL(file);
      } else if (newUrl) {
        doInsert(newUrl);
      } else {
        toast("请输入图片地址或选择文件");
        return;
      }
      closeModal();
    };

    mask.addEventListener("click", (e) => { if (e.target === mask) closeModal(); });
    mask.querySelector(".xs-btn-cancel").addEventListener("click", closeModal);
    mask.querySelector(".xs-btn-apply").addEventListener("click", apply);
    mask.querySelector("#xsFileInput").addEventListener("change", () => {
      const f = mask.querySelector("#xsFileInput").files[0];
      if (f) mask.querySelector(".xs-new-url").placeholder = f.name;
    });
    mask.querySelector(".xs-new-url").addEventListener("keydown", (e) => {
      if (e.key === "Enter") apply();
    });
    setTimeout(() => mask.querySelector(".xs-new-url").focus(), 120);
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

  /* ── Export ── */
  function exportHtml() {
    saveAll();
    const clone = document.documentElement.cloneNode(true);
    clone.querySelectorAll("[contenteditable], [spellcheck]").forEach(el => {
      el.removeAttribute("contenteditable");
      el.removeAttribute("spellcheck");
    });
    clone.querySelectorAll(".xs-edit-toolbar, .xs-toast, .xs-media-wrapper, .xs-media-badge, .xs-modal-mask")
      .forEach(el => el.remove());
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
    a.download = (document.title || "xiaoshui-pretty-ppt").replace(/[\\/:*?"<>|]+/g, "-") + "-edited.html";
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
    bar.className = "xs-edit-toolbar";
    bar.setAttribute("data-no-edit", "true");
    bar.innerHTML = [
      '<button type="button" data-xs-edit-toggle>编辑</button>',
      '<span class="xs-sep"></span>',
      '<span class="xs-font-control" title="先点选文字，再调整字号">',
      '  <label for="xsFontSizeInput">字号</label>',
      '  <button type="button" data-xs-font-minus title="减小字号">A-</button>',
      '  <input id="xsFontSizeInput" type="number" min="8" max="160" step="1" data-xs-font-size disabled>',
      '  <button type="button" data-xs-font-plus title="增大字号">A+</button>',
      '  <button type="button" data-xs-font-reset title="恢复模板默认字号">默认</button>',
      '</span>',
      '<span class="xs-sep"></span>',
      '<button type="button" data-xs-edit-save>保存</button>',
      '<button type="button" data-xs-edit-export>导出 HTML</button>',
      '<button type="button" data-xs-edit-reset>重置</button>',
      '<span class="xs-sep"></span>',
      '<button type="button" data-xs-edit-insert-img title="插入一张图片到光标位置">➕ 插入图片</button>'
    ].join("");
    document.body.appendChild(bar);
    bar.querySelector("[data-xs-edit-toggle]").addEventListener("click", () => toggleEdit());
    bar.querySelector("[data-xs-edit-save]").addEventListener("click", saveAll);
    bar.querySelector("[data-xs-edit-export]").addEventListener("click", exportHtml);
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
    bar.querySelector("[data-xs-edit-insert-img]").addEventListener("click", () => {
      if (!editing) { toast("请先点击「编辑」进入编辑模式"); return; }
      openInsertModal();
    });
  }

  document.addEventListener("focusin", (event) => {
    const el = fontTargetFromEventTarget(event.target);
    if (el) setCurrentTextEl(el);
  });

  document.addEventListener("click", (event) => {
    const el = fontTargetFromEventTarget(event.target);
    if (el) setCurrentTextEl(el);
  });

  /* ── Keyboard ── */
  document.addEventListener("keydown", (event) => {
    const key = event.key.toLowerCase();
    if (key === "e" && !event.metaKey && !event.ctrlKey && !event.altKey) {
      const tag = document.activeElement?.tagName?.toLowerCase();
      if (tag !== "input" && tag !== "textarea") toggleEdit();
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
})();
</script>
<!-- XIAOSHUI_PPT_EDIT_MODE_END -->
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
        description="Inject browser edit mode into a XiaoShui Pretty PPT deck."
    )
    parser.add_argument("html", help="Path to index.html or another HTML file")
    args = parser.parse_args()
    inject_edit_mode(Path(args.html))
    print(Path(args.html).expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
