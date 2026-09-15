#!/usr/bin/env python3
"""Convert cpp-course markdown docs to self-contained HTML."""

from pathlib import Path
import markdown

DOCS = Path("/workspace/cpp-course/docs")
OUT = Path("/workspace/cpp-course/html")

CSS = """
:root {
  --bg: #f7f4ef;
  --fg: #1c1b19;
  --muted: #5c574f;
  --accent: #0b6e4f;
  --code-bg: #ebe6dc;
  --border: #d4cdc0;
  --table-head: #e2dccd;
}
* { box-sizing: border-box; }
html { font-size: 17px; scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: "Source Han Sans SC", "Noto Sans SC", "PingFang SC",
               "Microsoft YaHei", sans-serif;
  color: var(--fg);
  background:
    radial-gradient(1200px 600px at 10% -10%, #e8f2ec 0%, transparent 55%),
    radial-gradient(900px 500px at 100% 0%, #f0e8d8 0%, transparent 50%),
    var(--bg);
  line-height: 1.7;
}
.wrap {
  max-width: 880px;
  margin: 0 auto;
  padding: 2.5rem 1.25rem 4rem;
}
header.doc-head {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--accent);
}
header.doc-head .series {
  color: var(--accent);
  font-size: 0.85rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 600;
}
h1, h2, h3, h4 {
  font-family: "Source Han Serif SC", "Noto Serif SC", "Songti SC", serif;
  line-height: 1.35;
  font-weight: 700;
}
h1 { font-size: 2rem; margin: 0.4rem 0 0.6rem; }
h2 {
  font-size: 1.45rem;
  margin-top: 2.2rem;
  padding-left: 0.6rem;
  border-left: 4px solid var(--accent);
}
h3 { font-size: 1.15rem; margin-top: 1.6rem; color: #163a2c; }
h4 { font-size: 1.02rem; margin-top: 1.2rem; }
p, li { color: var(--fg); }
a { color: var(--accent); }
hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 2rem 0;
}
blockquote {
  margin: 1rem 0;
  padding: 0.6rem 1rem;
  border-left: 3px solid var(--accent);
  background: rgba(11, 110, 79, 0.06);
  color: var(--muted);
}
code {
  font-family: "JetBrains Mono", "Fira Code", Consolas, monospace;
  font-size: 0.88em;
  background: var(--code-bg);
  padding: 0.12em 0.35em;
  border-radius: 4px;
}
pre {
  background: #1e2430;
  color: #e8ecf1;
  padding: 1rem 1.1rem;
  border-radius: 8px;
  overflow-x: auto;
  line-height: 1.55;
  box-shadow: 0 8px 24px rgba(30, 36, 48, 0.18);
}
pre code {
  background: transparent;
  color: inherit;
  padding: 0;
  font-size: 0.86rem;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0 1.5rem;
  font-size: 0.95rem;
}
th, td {
  border: 1px solid var(--border);
  padding: 0.55rem 0.7rem;
  text-align: left;
  vertical-align: top;
}
th { background: var(--table-head); }
tr:nth-child(even) td { background: rgba(255,255,255,0.45); }
ul, ol { padding-left: 1.4rem; }
li + li { margin-top: 0.25rem; }
img { max-width: 100%; height: auto; }
footer {
  margin-top: 3rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
  color: var(--muted);
  font-size: 0.9rem;
}
nav.toc {
  background: rgba(255,255,255,0.55);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.9rem 1.1rem;
  margin: 1.2rem 0 2rem;
}
nav.toc strong { display: block; margin-bottom: 0.4rem; color: var(--accent); }
@media (max-width: 640px) {
  html { font-size: 16px; }
  h1 { font-size: 1.55rem; }
  .wrap { padding: 1.5rem 1rem 3rem; }
}
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>{css}</style>
</head>
<body>
  <div class="wrap">
    <header class="doc-head">
      <div class="series">C++ 课程讲义 · 优化版</div>
    </header>
    <article>
{body}
    </article>
    <footer>
      <p>由原 day_01～day_09 讲义去重整理 · 建议配合 Markdown 源文件学习</p>
    </footer>
  </div>
</body>
</html>
"""


def md_to_html(md_text: str) -> str:
    return markdown.markdown(
        md_text,
        extensions=[
            "fenced_code",
            "tables",
            "toc",
            "sane_lists",
            "nl2br",
        ],
        extension_configs={"toc": {"permalink": False}},
    )


def extract_title(md_text: str, fallback: str) -> str:
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = sorted(DOCS.glob("*.md"))
    if not files:
        raise SystemExit(f"No markdown files in {DOCS}")

    for path in files:
        text = path.read_text(encoding="utf-8")
        title = extract_title(text, path.stem)
        body = md_to_html(text)
        html = TEMPLATE.format(title=title, css=CSS, body=body)
        out = OUT / f"{path.stem}.html"
        out.write_text(html, encoding="utf-8")
        print(f"wrote {out} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
