#!/usr/bin/env python3
"""Build index.html from the frozen evaluation inputs; no network or install step.

Uses the already installed Markdown 3.5.2 and Pygments 2.17.2 packages.
Run: python rust-intro/build-reader.py
"""
import base64
import hashlib
import html
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

import markdown
from pygments.formatters import HtmlFormatter

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "_test" / "astra-6"


class ReaderHTML(HTMLParser):
    """Allow only inert document markup; embed local images and namespace anchors."""

    tags = set("h1 h2 h3 h4 h5 h6 p ul ol li dl dt dd blockquote strong em b i code pre div span a img hr br table thead tbody tr th td sup sub del".split())
    void = {"img", "hr", "br"}

    def __init__(self, candidate):
        super().__init__(convert_charrefs=True)
        self.candidate = candidate
        self.output = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.tags:
            raise ValueError(f"Unsupported HTML tag: {tag}")
        attrs = dict(attrs)
        if tag == "img":
            source = (INPUTS / self.candidate / attrs["src"]).resolve()
            if not source.is_relative_to((INPUTS / self.candidate / "assets").resolve()):
                raise ValueError(f"Image outside candidate assets: {source}")
            if source.suffix != ".svg":
                raise ValueError(f"Unsupported image format: {source}")
            raw = source.read_bytes()
            svg = ET.fromstring(raw)
            for node in svg.iter():
                if node.tag.rsplit("}", 1)[-1] in {"script", "foreignObject"}:
                    raise ValueError(f"Active SVG content: {source}")
                for key, value in node.attrib.items():
                    key = key.rsplit("}", 1)[-1].lower()
                    if key.startswith("on") or (key in {"href", "src"} and not value.startswith("#")):
                        raise ValueError(f"Active SVG attribute: {source}")
            encoded = base64.b64encode(raw).decode()
            alt = html.escape(attrs.get("alt", "Diagram"), quote=True)
            _, _, width, height = svg.attrib["viewBox"].split()
            self.output.append(
                f'<button class="figure" type="button" aria-label="Expand diagram: {alt}">'
                f'<img src="data:image/svg+xml;base64,{encoded}" alt="{alt}" '
                f'width="{float(width):g}" height="{float(height):g}" loading="lazy">'
                '<span class="figure-hint">Expand diagram <span aria-hidden="true">↗</span></span></button>'
            )
            return
        clean = {}
        for key, value in attrs.items():
            if key in {"class", "title"}:
                clean[key] = value
            elif key == "id":
                clean[key] = f"{self.candidate}-{value}"
            elif tag == "a" and key == "href":
                if value.startswith("#"):
                    clean[key] = f"#{self.candidate}-{value[1:]}"
                elif urlsplit(value).scheme in {"https", "http"}:
                    clean[key] = value
                    clean["rel"] = "noreferrer noopener"
                else:
                    raise ValueError(f"Unsupported link: {value}")
            elif tag in {"th", "td"} and key == "style" and re.fullmatch(r"text-align: (left|right|center);", value):
                clean[key] = value
            else:
                raise ValueError(f"Unsupported attribute: {tag}.{key}")
        if tag == "table":
            self.output.append('<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable table">')
        rendered = "".join(f' {k}="{html.escape(v, quote=True)}"' for k, v in clean.items())
        self.output.append(f"<{tag}{rendered}>")

    def handle_endtag(self, tag):
        if tag not in self.void:
            self.output.append(f"</{tag}>")
        if tag == "table":
            self.output.append("</div>")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.void:
            self.handle_endtag(tag)

    def handle_data(self, data):
        self.output.append(html.escape(data))


def build():
    key = (ROOT / "EVALUATION-KEY.md").read_text()
    entries = re.findall(r"^\| (\w+) \| ([^ |]+) \| `[^`]+` \|$", key, re.M)
    hashes = dict(re.findall(r"^\| `([^`]+)` \| `([0-9a-f]{64})` \|$", key, re.M))
    for name, digest in hashes.items():
        if hashlib.sha256((INPUTS / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f"Frozen input changed: {name}")
    articles, outlines, options = [], [], []
    for index, (code, model) in enumerate(entries):
        source = (INPUTS / code / "output.md").read_text()
        md = markdown.Markdown(
            extensions=["fenced_code", "tables", "toc", "codehilite"],
            extension_configs={"codehilite": {"guess_lang": False}, "toc": {"toc_depth": "2"}},
        )
        rendered = md.convert(source)
        parser = ReaderHTML(code)
        parser.feed(rendered)
        parser.close()
        document = "".join(parser.output)
        toc = ReaderHTML(code)
        toc.feed(md.toc)
        toc.close()
        hidden = " hidden" if index else ""
        words = len(source.split())
        diagrams = len(list((INPUTS / code / "assets").glob("*.svg")))
        label = html.escape(model, quote=True)
        options.append(f'<option value="{code}">{label}</option>')
        outlines.append(f'<nav class="outline" data-entry="{code}" aria-label="Sections in {label}"{hidden}>{"".join(toc.output)}</nav>')
        articles.append(
            f'<article id="{code}" data-entry="{code}" aria-label="{label}"{hidden}>'
            f'<div class="entry-meta"><span class="entry-name">{label}</span>'
            f'<span>{words:,} words · {diagrams} diagram{"s" if diagrams != 1 else ""}</span></div>'
            f'{document}<footer class="article-end"><span>End of {label}</span>'
            '<a href="#top">Back to top ↑</a></footer></article>'
        )
    result = TEMPLATE.replace("@@HIGHLIGHT@@", HtmlFormatter(style="native").get_style_defs(".codehilite"))
    result = result.replace("@@OPTIONS@@", "\n".join(options))
    result = result.replace("@@OUTLINES@@", "\n".join(outlines))
    result = result.replace("@@ARTICLES@@", "\n".join(articles))
    (ROOT / "index.html").write_text(result)
    print(f"Built {ROOT / 'index.html'} ({len(result.encode()):,} bytes; {len(entries)} entries)")


TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'; script-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Rust, eight ways — a reading room</title>
<style>
:root { color-scheme: light; --paper:#fff; --ink:#253041; --muted:#647084; --line:#e1e6ee; --accent:#285ac2; --wash:#eef3fa; --card:#f8fafc; --sans:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; --mono:"SFMono-Regular",Consolas,"Liberation Mono",monospace; }
* { box-sizing:border-box; }
[hidden] { display:none !important; }
html { scroll-padding-top:110px; }
body { margin:0; background:var(--paper); color:var(--ink); font-family:var(--sans); }
a { color:var(--accent); text-decoration-thickness:1px; text-underline-offset:3px; }
button, select, summary { font:inherit; }
button, select { color:var(--ink); }
button { cursor:pointer; }
a, button, select, summary { -webkit-tap-highlight-color:transparent; }
:focus-visible { outline:3px solid var(--accent); outline-offset:4px; }
.skip { position:fixed; top:-100px; left:20px; z-index:10; padding:12px; background:var(--card); }
.skip:focus { top:12px; }
.topbar { position:sticky; top:0; z-index:3; background:var(--paper); border-bottom:1px solid var(--line); }
.topbar-inner { max-width:1320px; margin:auto; min-height:78px; padding:12px 40px; display:flex; align-items:center; gap:28px; }
.brand { color:var(--ink); text-decoration:none; font-size:16px; font-weight:650; white-space:nowrap; letter-spacing:-.4px; }
.brand span { display:inline-grid; place-items:center; width:32px; height:32px; margin-right:10px; background:var(--wash); border-radius:7px; font:600 18px var(--mono); color:var(--accent); }
.controls { display:flex; align-items:center; gap:14px; margin-left:auto; font-size:13px; }
.controls label { color:var(--muted); }
select { background:var(--card); border:1px solid var(--line); border-radius:7px; padding:10px 28px 10px 12px; max-width:300px; cursor:pointer; }
.progress { height:2px; background:var(--accent); transform:scaleX(0); transform-origin:left; }
/* Equal side tracks center the article, independently of the left outline. */
.layout { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,780px) minmax(0,1fr); gap:32px; padding:32px 32px 70px; align-items:start; }
aside { position:sticky; top:106px; width:min(220px,100%); justify-self:end; max-height:calc(100vh - 130px); overflow:auto; scrollbar-width:thin; padding:6px 10px 16px 0; }
.side-title { text-transform:uppercase; font-size:10px; font-weight:700; color:var(--muted); letter-spacing:1.6px; margin-bottom:17px; }
.outline ul { list-style:none; padding:0; margin:0; }
.outline li { margin:0; }
.outline a { display:block; color:var(--muted); text-decoration:none; font-size:12px; line-height:1.55; padding:6px 10px; border-left:2px solid transparent; }
.outline a:hover, .outline a[aria-current] { color:var(--accent); background:var(--wash); border-left-color:var(--accent); }
/* Skip the article title in the outline, but keep its section children. */
.outline > .toc > ul > li > a { display:none; }
main { grid-column:2; min-width:0; }
article { font:17px/1.85 var(--sans); overflow-wrap:break-word; }
.entry-meta { display:flex; flex-wrap:wrap; gap:10px 18px; align-items:center; font:12px/1.6 var(--sans); color:var(--muted); padding:6px 0 2px; }
.entry-name { color:var(--accent); font-weight:650; letter-spacing:.4px; }
article h1 { font-size:clamp(28px,3.4vw,36px); line-height:1.3; font-weight:650; letter-spacing:-1px; margin:24px 0 29px; text-wrap:balance; }
article h2 { font:650 25px/1.4 var(--sans); letter-spacing:-.6px; margin:60px 0 22px; padding-top:27px; border-top:1px solid var(--line); }
article h3 { font:650 19px/1.5 var(--sans); letter-spacing:-.2px; margin:32px 0 16px; }
article h4 { font:650 17px/1.5 var(--sans); }
article p { margin:0 0 22px; }
article li { margin:6px 0; padding-left:3px; }
article ul, article ol { padding-left:25px; margin:18px 0 25px; }
article strong { font-weight:700; }
article hr { margin:40px 0; border:0; border-top:1px solid var(--line); }
article blockquote { border-left:3px solid var(--accent); padding:6px 0 6px 23px; margin:30px 0; color:var(--muted); }
article blockquote p:last-child { margin-bottom:0; }
code { font-family:var(--mono); font-size:.81em; background:var(--wash); padding:.12em .28em; border-radius:3px; overflow-wrap:anywhere; }
pre { font:14px/1.75 var(--mono); tab-size:4; white-space:pre; overflow:auto; padding:24px 26px; border:1px solid #303e52; border-radius:9px; background:#182231; color:#e8edf5; }
pre code { font:inherit; background:none; padding:0; border:0; overflow-wrap:normal; }
.codehilite { margin:24px 0 30px; border-radius:9px; }
.codehilite pre { margin:0; }
/* Use the empty right margin; the left margin belongs to the section outline. */
.codehilite, article > pre { width:max-content; min-width:100%; max-width:calc(100% + max(0px, (100vw - 780px) / 2 - 40px)); }
@@HIGHLIGHT@@
.codehilite { background:#182231; }
.codehilite .c, .codehilite .c1, .codehilite .cm, .codehilite .cs { color:#a3b0c2; }
.codehilite .err { border:none; }
.table-scroll { overflow-x:auto; margin:28px 0 32px; border:1px solid var(--line); border-radius:8px; background:var(--card); }
table { border-collapse:collapse; font:13px/1.65 var(--sans); width:100%; min-width:500px; }
th { font-weight:650; text-align:left; background:var(--wash); }
th, td { padding:13px 15px; vertical-align:top; border-bottom:1px solid var(--line); }
tr:last-child td { border-bottom:0; }
table code { font-size:.92em; }
.figure { display:block; position:relative; width:100%; padding:12px 12px 32px; border:1px solid var(--line); border-radius:9px; background:#fff; margin:30px 0; text-align:center; }
.figure img { display:block; width:100%; height:auto; }
.figure-hint { position:absolute; right:13px; bottom:7px; font:11px/1.4 var(--sans); color:#647084; }
.figure:hover { border-color:var(--accent); box-shadow:0 4px 16px #00000008; }
.article-end { display:flex; justify-content:space-between; gap:20px; border-top:1px solid var(--line); margin-top:60px; padding-top:25px; color:var(--muted); font:12px var(--sans); }
.pager { display:flex; justify-content:space-between; align-items:center; gap:20px; margin-top:35px; }
.pager button { background:var(--card); border:1px solid var(--line); padding:12px 16px; border-radius:7px; font-size:13px; }
.pager button:disabled { opacity:.4; cursor:default; }
#position { color:var(--muted); font-size:12px; white-space:nowrap; }
dialog { max-width:calc(100vw - 40px); width:1400px; max-height:90vh; border:1px solid var(--line); border-radius:10px; padding:0; color:var(--ink); background:var(--card); box-shadow:0 20px 100px #0006; }
dialog::backdrop { background:#111827b8; }
.dialog-head { display:flex; align-items:center; justify-content:space-between; gap:20px; padding:16px 20px; border-bottom:1px solid var(--line); font-size:13px; }
.dialog-head button { border:1px solid var(--line); border-radius:6px; padding:7px 12px; background:var(--paper); }
.diagram-view { overflow:auto; max-height:calc(90vh - 75px); padding:20px; background:white; }
.diagram-view img { display:block; max-width:none; min-width:100%; height:auto; }
@media (prefers-color-scheme:dark) {
 :root { color-scheme:dark; --paper:#111827; --ink:#e5eaf2; --muted:#a6b2c4; --line:#334155; --accent:#9bbcff; --wash:#202e44; --card:#182231; }
}
@media (max-width:1150px) {
 .layout { display:block; max-width:844px; margin:auto; padding:32px 32px 50px; }
 aside { position:static; width:100%; max-height:none; padding:0 0 24px; }
 aside .side-title { display:none; }
 .outline { max-height:170px; overflow:auto; border:1px solid var(--line); border-radius:7px; padding:10px; }
 .topbar-inner { padding:12px 28px; }
}
@media (max-width:720px) {
 .topbar-inner { flex-wrap:wrap; gap:10px; padding:12px 20px; }
 .brand { width:100%; font-size:14px; }
 .brand span { width:25px; height:25px; font-size:17px; }
 .controls { margin:0; width:100%; justify-content:space-between; gap:8px; }
 select { flex:1; min-width:0; max-width:100%; }
 .layout { display:block; padding:24px 20px 40px; }
 .outline a { font-size:12px; padding:5px 10px; }
 article h1 { font-size:28px; }
 article h2 { font-size:23px; margin-top:42px; }
 article { font-size:17px; }
 pre { padding:18px; font-size:12px; }
 .figure { padding:6px 6px 28px; }
 html { scroll-padding-top:150px; }
 dialog { max-width:calc(100vw - 20px); }
}
@media print {
 .topbar, aside, .pager, .figure-hint, .article-end { display:none; }
 body { background:white; color:black; }
 .layout { display:block; max-width:none; padding:0; }
 article { font-size:11pt; }
 pre { white-space:pre-wrap; }
 .codehilite, article > pre { width:100%; max-width:100%; }
 article h2 { break-after:avoid; }
 .figure, pre { break-inside:avoid; }
 .table-scroll { overflow:visible; }
 table { min-width:0; }
}
</style>
</head>
<body>
<a class="skip" href="#reading">Skip to introduction</a>
<header class="topbar">
 <div class="topbar-inner">
  <a class="brand" href="#top"><span aria-hidden="true">r</span>Rust, eight ways</a>
  <div class="controls">
   <label for="candidate">Reading</label>
   <select id="candidate" aria-label="Choose an introduction">@@OPTIONS@@</select>
  </div>
 </div>
 <div class="progress" aria-hidden="true"></div>
</header>
<div class="layout" id="top">
 <aside>
  <div class="side-title">In this introduction</div>
  @@OUTLINES@@
 </aside>
 <main id="reading" tabindex="-1">
  @@ARTICLES@@
  <div class="pager" aria-label="Introduction navigation">
   <button id="previous" type="button">← Previous</button>
   <span id="position" aria-live="polite">1 of 8</span>
   <button id="next" type="button">Next introduction →</button>
  </div>
 </main>
</div>
<dialog id="diagram" aria-labelledby="diagram-title">
 <div class="dialog-head"><span id="diagram-title">Diagram</span><button id="close-diagram" type="button">Close ×</button></div>
 <div class="diagram-view" tabindex="0" role="region" aria-label="Enlarged diagram, scroll to inspect"><img id="diagram-image" alt=""></div>
</dialog>
<noscript><p style="padding:20px">Enable JavaScript to switch between introductions and enlarge diagrams. The first introduction is readable without it.</p></noscript>
<script>
'use strict';
const select = document.querySelector('#candidate');
const articles = [...document.querySelectorAll('article')];
const outlines = [...document.querySelectorAll('.outline')];
const codes = articles.map(a => a.id);
const options = [...select.options];
const previous = document.querySelector('#previous');
const next = document.querySelector('#next');
let current = codes[0];
const positions = new Map();
const titleFor = code => options.find(o => o.value === code).textContent;

function selectEntry(code, restore = true) {
  if (!codes.includes(code)) return;
  if (code !== current) positions.set(current, window.scrollY);
  current = code;
  articles.forEach(a => a.hidden = a.id !== code);
  outlines.forEach(n => n.hidden = n.dataset.entry !== code);
  select.value = code;
  const index = codes.indexOf(code);
  previous.disabled = index === 0;
  next.disabled = index === codes.length - 1;
  document.querySelector('#position').textContent = `${index + 1} of ${codes.length}`;
  document.title = `${titleFor(code)} — Rust, eight ways`;
  if (restore) window.scrollTo(0, positions.get(code) || 0);
  updateProgress();
}
function navigate(code) {
  // Avoid the browser's anchor jump before saving the previous reading position.
  history.pushState(null, '', '#' + code);
  selectEntry(code);
}
function followHash() {
  const fragment = decodeURIComponent(location.hash.slice(1));
  const code = codes.find(c => fragment === c || fragment.startsWith(c + '-'));
  if (code) {
    selectEntry(code, fragment === code);
    if (fragment !== code) document.getElementById(fragment)?.scrollIntoView();
  } else if (fragment === 'top') window.scrollTo(0, 0);
}
select.addEventListener('change', () => navigate(select.value));
previous.addEventListener('click', () => navigate(codes[codes.indexOf(current) - 1]));
next.addEventListener('click', () => navigate(codes[codes.indexOf(current) + 1]));
window.addEventListener('hashchange', followHash);
window.addEventListener('popstate', followHash);
function updateProgress() {
  const article = document.getElementById(current);
  const start = article.getBoundingClientRect().top + window.scrollY;
  const distance = Math.max(1, article.offsetHeight - window.innerHeight + 100);
  const fraction = Math.min(1, Math.max(0, (window.scrollY - start + 100) / distance));
  document.querySelector('.progress').style.transform = `scaleX(${fraction})`;
  const headings = [...article.querySelectorAll('h2')];
  const active = headings.filter(h => h.getBoundingClientRect().top <= 160).at(-1);
  document.querySelectorAll(`.outline[data-entry="${current}"] a`).forEach(a => {
    if (active && a.hash === '#' + active.id) a.setAttribute('aria-current', 'location');
    else a.removeAttribute('aria-current');
  });
}
let scheduled = false;
window.addEventListener('scroll', () => {
  if (scheduled) return;
  scheduled = true;
  requestAnimationFrame(() => { updateProgress(); scheduled = false; });
}, { passive: true });
window.addEventListener('resize', updateProgress);
const dialog = document.querySelector('#diagram');
const image = document.querySelector('#diagram-image');
document.querySelectorAll('.figure').forEach(button => button.addEventListener('click', () => {
  const source = button.querySelector('img');
  image.src = source.src;
  image.alt = source.alt;
  image.style.width = `${Math.max(source.naturalWidth, 1000)}px`;
  document.querySelector('#diagram-title').textContent = source.alt;
  dialog.showModal();
}));
document.querySelector('#close-diagram').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
// Preformatted blocks need keyboard focus for horizontal scrolling.
document.querySelectorAll('pre').forEach(pre => {
  pre.tabIndex = 0;
  pre.setAttribute('aria-label', 'Code example');
});
selectEntry(current, false);
followHash();
</script>
</body>
</html>
'''

if __name__ == "__main__":
    build()
