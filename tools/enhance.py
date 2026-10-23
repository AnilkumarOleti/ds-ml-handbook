#!/usr/bin/env python3
"""Add the in-repository layer to a freshly built index.html.

make_site.py runs this automatically after it writes index.html, so everything below survives a
rebuild of the handbook from its outside sources. It can also be run by hand:

    python3 tools/enhance.py            # enhance index.html in place
    python3 tools/enhance.py --check    # report what it would do, write nothing

What it does, in order:
  1. Adds the extra concept pages in extra/pages/*.html. Each file starts with a one-line
     <!--meta {...}--> header (slug, code, title, lede, keywords). The page joins the handbook's
     data: its position follows the section order, and its self-tests and interview rungs are
     read from the page itself, so they appear in the mixed self-test, the question index,
     the review queue and the mock interview without being listed twice.
  2. Turns every "@slug" cross-reference in page text and in the self-test data into a link to
     that page, named by its title. An @slug that names no page stops the build.
  3. Adds the extra labs (extra/labs.js) and the study layer (extra/study.js, extra/study.css):
     saved attempts, progress marks, a spaced review queue, a timed mock interview, study plans,
     a notes page and a print layout.
  4. Adds four small hooks to the handbook's own script so the study layer can add views and
     react to page changes. Each hook is a literal replacement that must match exactly once,
     so a change in the builder's output stops the build here instead of breaking the site.

Running it twice is safe: an already enhanced file is left as it is.
"""
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRA = os.path.join(ROOT, "extra")
MARK = "<!-- enhanced: tools/enhance.py -->"
REF = re.compile(r"@([a-z]\d-[a-z0-9-]+)")

# literal replacements in the handbook's app script: (find, replace)
HOOKS = [
    ("else if(name==='questions')questions();else{cur='';home()}",
     "else if(name==='questions')questions();else if(HB.views&&HB.views[name])HB.views[name](view);else{cur='';home()}"),
    ("    setNav(cur);\n",
     "    setNav(cur);if(HB.onroute)HB.onroute(cur,view);\n"),
    ("document.getElementById('parts').replaceChildren(el(out));",
     "document.getElementById('parts').replaceChildren(el(out));if(HB.onlist)HB.onlist();"),
    ("HB.start=function(){route(location.hash.replace(/^#/,''))};",
     "HB.start=function(){route(location.hash.replace(/^#/,''))};HB.route=route;HB.D=D;HB.by=by;HB.mountLab=mountLab;"),
]


def text(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()


def read_page(path):
    s = open(path, encoding="utf8").read()
    m = re.match(r"<!--meta (\{.*?\})-->\n", s, re.S)
    if not m:
        raise SystemExit(f"{path}: must start with <!--meta {{...}}-->")
    meta = json.loads(m.group(1))
    for k in ("slug", "code", "title", "lede"):
        if not meta.get(k):
            raise SystemExit(f"{path}: meta needs {k}")
    return meta, s[m.end():].strip() + "\n"


def harvest(slug, body):
    """Self-test items and interview rungs, read from the page the way the builder reads them."""
    quiz, ladder = [], []
    sections = re.split(r'<section class="sec" id="s(\d+)">', body)
    for i in range(1, len(sections), 2):
        n, sec = int(sections[i]), sections[i + 1]
        if 2 <= n <= 9:
            for q in re.finditer(r'<div class="q"><p>(.*?)</p>\s*<details class="reveal"><summary>.*?</summary>'
                                 r'<div class="reveal-body">(.*?)</div>\s*</details>\s*</div>', sec, re.S):
                qq = re.sub(r'<span class="why">Why\?</span>', "", q.group(1)).strip()
                quiz.append({"s": slug, "n": n, "q": qq, "a": q.group(2).strip()})
        if n == 10:
            rail = re.search(r'<div class="rail">(.*?)</div>\s*</div>', sec, re.S)
            chips = lambda s: [c.lower() for c in re.findall(r'<span class="chip">([^<]+)</span>', s)]
            default = chips(rail.group(1)) if rail else []
            for r in re.finditer(r'<div class="rung"><div class="rung-head"><span class="label">Rung (\d) [^<]*</span>(.*?)</div>\s*'
                                 r'<p class="ask">(.*?)</p>', sec, re.S):
                roles = " ".join(chips(r.group(2)) or default)
                ladder.append({"s": slug, "r": int(r.group(1)), "roles": roles, "q": text(r.group(3))})
    return quiz, ladder


def main():
    check = "--check" in sys.argv[1:]
    path = os.path.join(ROOT, "index.html")
    h = open(path, encoding="utf8").read()
    if MARK in h:
        print("enhance: index.html is already enhanced, nothing to do")
        return

    dm = re.search(r'(<script type="application/json" id="hb-data">)(.*?)(</script>)', h, re.S)
    data = json.loads(dm.group(2))
    secs = list(data["secs"])

    # 1. extra pages
    added = []
    for f in sorted(glob.glob(os.path.join(EXTRA, "pages", "*.html"))):
        meta, body = read_page(f)
        slug, code = meta["slug"], meta["code"]
        if code not in data["secs"]:
            raise SystemExit(f"{f}: unknown section {code}")
        if any(p["slug"] == slug for p in data["pages"]) or f'id="pg-{slug}"' in h:
            raise SystemExit(f"{f}: slug {slug} is already in the handbook")
        quiz, ladder = harvest(slug, body)
        if len(ladder) != 5:
            raise SystemExit(f"{f}: expected 5 interview rungs, found {len(ladder)}")
        find = " ".join([meta["title"], meta["lede"], meta.get("keywords", "")] + [x["q"] for x in ladder]).lower()
        entry = {"slug": slug, "code": code, "title": meta["title"], "lede": meta["lede"], "find": find}
        # position: after the last page whose section comes at or before this one
        rank = secs.index(code)
        at = 0
        for i, p in enumerate(data["pages"]):
            if secs.index(p["code"]) <= rank:
                at = i + 1
        data["pages"].insert(at, entry)
        order = {p["slug"]: i for i, p in enumerate(data["pages"])}
        data["quiz"] = sorted(data["quiz"] + quiz, key=lambda x: order[x["s"]])
        data["ladder"] = sorted(data["ladder"] + ladder, key=lambda x: (order[x["s"]], x["r"]))
        h = h.replace(dm.group(1), f'<template id="pg-{slug}">{body}</template>\n\n' + dm.group(1), 1)
        added.append((code, meta["title"], len(quiz), len(ladder)))

    # 1b. inserts into existing pages: extra/inserts/*.html, header <!--insert {"slug": ..., "before": ...}-->
    for f in sorted(glob.glob(os.path.join(EXTRA, "inserts", "*.html"))):
        s = open(f, encoding="utf8").read()
        m = re.match(r"<!--insert (\{.*?\})-->\n", s, re.S)
        if not m:
            raise SystemExit(f"{f}: must start with <!--insert {{...}}-->")
        meta, body = json.loads(m.group(1)), s[m.end():].strip()
        tm = re.search(r'<template id="pg-%s">(.*?)</template>' % re.escape(meta["slug"]), h, re.S)
        if not tm:
            raise SystemExit(f"{f}: page {meta['slug']} not found")
        tpl = tm.group(1)
        if tpl.count(meta["before"]) != 1:
            raise SystemExit(f"{f}: anchor text found {tpl.count(meta['before'])} times in {meta['slug']}, expected once")
        tpl = tpl.replace(meta["before"], body + meta["before"])
        h = h[:tm.start(1)] + tpl + h[tm.end(1):]
        print(f"  inserted {os.path.basename(f)} into {meta['slug']}")

    # 2. cross-references
    titles = {p["slug"]: p["title"] for p in data["pages"]}
    count = 0

    def link(m):
        nonlocal count
        s = m.group(1)
        if s not in titles:
            raise SystemExit(f"cross-reference to a page that does not exist: @{s}")
        count += 1
        return f'<a class="xref" href="#{s}">{html.escape(titles[s])}</a>'

    def fix_templates(doc):
        return re.sub(r'(<template id="pg-[^"]+">)(.*?)(</template>)',
                      lambda m: m.group(1) + REF.sub(link, m.group(2)) + m.group(3), doc, flags=re.S)

    h = fix_templates(h)
    for x in data["quiz"]:
        x["q"], x["a"] = REF.sub(link, x["q"]), REF.sub(link, x["a"])
    for x in data["ladder"]:
        x["q"] = REF.sub(lambda m: titles.get(m.group(1), m.group(0)), x["q"])
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    dm = re.search(r'(<script type="application/json" id="hb-data">)(.*?)(</script>)', h, re.S)
    h = h[:dm.start(2)] + blob + h[dm.end(2):]

    # 3 and 4. scripts and hooks
    for find, rep in HOOKS:
        n = h.count(find)
        if n != 1:
            raise SystemExit(f"hook text found {n} times, expected once: {find[:60]}")
        h = h.replace(find, rep)
    start = "\nHB.start();\n"
    if h.count(start) != 1:
        raise SystemExit("could not find the single HB.start() call")
    labs = open(os.path.join(EXTRA, "labs.js"), encoding="utf8").read()
    study = open(os.path.join(EXTRA, "study.js"), encoding="utf8").read()
    css = open(os.path.join(EXTRA, "study.css"), encoding="utf8").read()
    for name, s in (("labs.js", labs), ("study.js", study)):
        if "</script" in s:
            raise SystemExit(f"extra/{name} must not contain </script")
    h = h.replace(start, f"\n/* ---- extra/labs.js ---- */\n{labs}\n/* ---- extra/study.js ---- */\n{study}\nHB.start();\n")
    h = h.replace("</head>", f"<style>\n{css}</style>\n{MARK}\n</head>", 1)

    left = [m for m in REF.findall(re.sub(r"<script.*?</script>", "", h, flags=re.S))]
    if left:
        raise SystemExit(f"cross-references left unlinked: {sorted(set(left))}")

    for code, title, nq, nl in added:
        print(f"  added {code} · {title}  ({nq} self-tests, {nl} rungs)")
    print(f"enhance: {len(data['pages'])} pages, {count} cross-references linked, "
          f"{len(data['quiz'])} self-tests, {len(data['ladder'])} interview questions")
    if not check:
        open(path, "w", encoding="utf8").write(h)


if __name__ == "__main__":
    main()
