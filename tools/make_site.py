#!/usr/bin/env python3
"""Turn the handbook and its picture pages into a static site for GitHub Pages.

Input:  a folder holding one sub-folder per page, each with the page saved as index.html.
        The handbook and the picture pages are recognised by their <title>.
Output: index.html (the handbook) and explainers/<slug>.html (the picture pages), written to
        the repository root.

What it changes, and nothing else:
  - gives each page a normal document head (language, charset, title, description);
  - points the handbook's picture-page links at explainers/<slug>.html in place of the private
    hosted copies;
  - adds one line at the foot of each picture page linking back to its handbook page.

usage: python3 tools/make_site.py <input-folder>
"""
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HANDBOOK = "DS/ML Learning Handbook"
PRIVATE = re.compile(r"https://claude\.ai/(?:code/)?artifact/[A-Za-z0-9-]+")
LEAD = re.compile(r'\n<title>([^<]*)</title>\n(<link rel="stylesheet" href="[^"]+">)\n')


def slug(title):
    s = html.unescape(title).lower().replace("'", "").replace("’", "")
    s = re.sub(r"^the\s+", "", s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def split(path):
    """Return (wrapper base style, title, fonts link, rest of body)."""
    s = open(path, encoding="utf8").read()
    head, body = s.split("<body>", 1)
    base = re.search(r"<style>.*?</style>", head, re.S).group(0)
    m = LEAD.match(body)
    if not m:
        raise SystemExit(f"{path}: page does not start with a title and a fonts link")
    rest = body[m.end():]
    end = rest.rindex("</body>")
    return base, html.unescape(m.group(1)), m.group(2), rest[:end].rstrip() + "\n"


def page(title, desc, base, fonts, body):
    e = lambda t: html.escape(t, quote=True)
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
            f"<title>{e(title)}</title>\n<meta name=\"description\" content=\"{e(desc)}\">\n"
            f"<meta property=\"og:title\" content=\"{e(title)}\">\n"
            f"<meta property=\"og:description\" content=\"{e(desc)}\">\n"
            f"{base}\n{fonts}\n</head>\n<body>\n{body}</body>\n</html>\n")


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    files = sorted(glob.glob(os.path.join(sys.argv[1], "*", "index.html")))
    parts = {}
    for f in files:
        base, title, fonts, body = split(f)
        parts[title] = (base, fonts, body)
    if HANDBOOK not in parts:
        raise SystemExit("handbook page not found")

    base, fonts, hb = parts.pop(HANDBOOK)
    data = json.loads(re.search(r'<script type="application/json" id="hb-data">(.*?)</script>', hb, re.S).group(1))
    # picture page title -> the handbook pages that link to it
    owners = {}
    for p in data["pages"]:
        if p.get("ex"):
            owners.setdefault(p["ex"][0], []).append(p)

    missing = sorted(set(owners) - set(parts))
    unused = sorted(set(parts) - set(owners))
    if missing:
        raise SystemExit(f"handbook links to picture pages that were not supplied: {missing}")

    # 1. handbook: swap each private link for the page inside this site
    swapped = 0
    for name, ps in owners.items():
        target = f"explainers/{slug(name)}.html"
        for url in {p["ex"][1] for p in ps}:
            swapped += hb.count(url)
            hb = hb.replace(url, target)
    left = PRIVATE.findall(hb)
    if left:
        raise SystemExit(f"private links still in the handbook: {sorted(set(left))}")
    desc = (f"{len(data['pages'])} concept pages on statistics, experimentation, causal inference, machine learning, "
            "SQL, product cases and data engineering. Each starts with a problem, hides every answer until you ask, "
            "and ends with an interview ladder.")
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf8").write(page(HANDBOOK, desc, base, fonts, hb))

    # 2. picture pages
    os.makedirs(os.path.join(ROOT, "explainers"), exist_ok=True)
    made = []
    for name, (base, fonts, body) in sorted(parts.items()):
        if PRIVATE.search(body):
            raise SystemExit(f"{name}: private link in a picture page")
        ps = owners.get(name, [])
        links = " · ".join(f'<a href="../#{p["slug"]}" style="color:inherit">{html.escape(p["title"])}</a>' for p in ps)
        back = (f'<p class="foot">Full page in the <a href="../" style="color:inherit">DS/ML Learning Handbook</a>'
                + (f": {links}" if links else "") + "</p>\n")
        n = body.count('<p class="foot">')
        if n != 1:
            raise SystemExit(f"{name}: expected one foot line, found {n}")
        body = re.sub(r'(<p class="foot">.*?</p>\n)', lambda m: m.group(1) + back, body, count=1, flags=re.S)
        sub = re.search(r'<p class="sub">([^<]*)</p>', body)
        desc = (html.unescape(sub.group(1)) + " " if sub else "") + "A picture story and a hands-on toy from the DS/ML Learning Handbook."
        out = f"explainers/{slug(name)}.html"
        open(os.path.join(ROOT, out), "w", encoding="utf8").write(page(name, desc, base, fonts, body))
        made.append((name, out, [p["title"] for p in ps]))

    print(f"handbook: {len(data['pages'])} pages, {swapped} private links swapped")
    for name, out, ps in made:
        print(f"  {out}  <-  {name}  ({', '.join(ps) or 'not linked from the handbook'})")
    if unused:
        print("WARN picture pages not linked from the handbook:", unused)


if __name__ == "__main__":
    main()
