#!/usr/bin/env python3
"""Write the extra concept pages in the handbook's own markup.

Each page is described in extra/src/<slug>.py as a call to page(...). This module wraps the
section bodies in the handbook's frame (header, table of contents, acts, rails with role chips,
self-test blocks, the interview ladder, section 11 and the sources footer) and writes
extra/pages/<slug>.html, which tools/enhance.py then adds to the built handbook.

    python3 tools/pagekit.py            # rebuild every page in extra/src
"""
import glob
import html
import json
import os
import runpy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECS = {"B0": "Mathematics for machine learning", "C4": "Product and marketing economics",
        "D3": "ML systems in production", "E1": "Communication", "E2": "Leading an analytics team",
        "E3": "Responsible practice", "A3": "A/B testing and experiment design"}
NAMES = {1: "Try it first", 2: "Two analogies", 3: "Concept", 4: "Mechanics, faded", 5: "Assumptions and failures",
         6: "Neighbours", 7: "Applications in pairs", 8: "In practice", 9: "Contested ground",
         10: "Interview ladder", 11: "Your one-liner"}
H3 = {4: "Mechanics, faded", 5: "Assumptions and failure modes", 6: "Neighbours", 9: "Nuances and contested ground"}
ACTS = [(1, "Why it exists", [1, 2, 3]), (2, "How it works", [4, 5]), (3, "Where it sits in the real world", [6, 7, 8]),
        (4, "Prove you know it", [9, 10, 11])]
RUNGS = {1: "Recall the idea", 2: "Why", 3: "What if", 4: "Design", 5: "Judgment"}
ROLE = {"lead": "Lead", "ic": "IC", "mle": "MLE"}

e = html.escape


def chips(roles):
    return "".join(f'<span class="chip">{ROLE[r]}</span>' for r in roles)


def reveal(body, closed="Show answer", opened="Hide answer"):
    return (f'<details class="reveal"><summary><span class="when-closed">{closed}</span>'
            f'<span class="when-open">{opened}</span></summary><div class="reveal-body">{body}</div></details>')


def table(head, rows, narrow=False):
    th = "".join(f"<th>{c}</th>" for c in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl{" narrow" if narrow else ""}"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def tests(items):
    """items: list of (question, answer_html) or (question, answer_html, True) for a "Why?" question."""
    if not items:
        return ""
    out = '<div class="check"><p class="label">Self-test</p>'
    for it in items:
        q, a = it[0], it[1]
        why = '<span class="why">Why?</span>' if len(it) > 2 and it[2] else ""
        out += f'<div class="q"><p>{why}{q}</p>{reveal(a)}</div>'
    return out + "</div>"


def ladder(slug, rungs):
    out = "<p>Answer each one out loud before opening it. The follow-ups are where interviews are decided.</p>"
    for i, r in enumerate(rungs, 1):
        own = chips(r["roles"]) if r.get("roles") else ""
        model = f'<div class="model"><p class="label">Model answer</p>{r["model"]}</div>' if r.get("model") else ""
        fu = "".join(f"<li>{x}</li>" for x in r["follow"])
        body = (f'<ul class="chain">{fu}</ul>{model}<div class="ws"><div><p class="label">Weak</p>{r["weak"]}</div>'
                f'<div><p class="label">Strong</p>{r["strong"]}</div></div>')
        out += (f'<div class="rung"><div class="rung-head"><span class="label">Rung {i} · {RUNGS[i]}</span>{own}</div>'
                f'<p class="ask">{r["ask"]}</p>{reveal(body, "Follow-ups, weak and strong answers", "Hide")}</div>')
    return out


def page(slug, code, title, lede, keywords, roles, sections, rungs, oneliner, contains, know, unlocks,
         sources=(), sec_roles=None, picture=None):
    """sections: {n: html} for 1..9; tests go inside those strings via tests([...])."""
    sec_roles = sec_roles or {}
    toc = '<nav class="toc" aria-label="On this page">'
    for _, name, ns in ACTS:
        toc += f'<div><p class="label">{name}</p><ol>' + "".join(
            f'<li><a href="#s{n}" data-jump="s{n}"><span>{n}</span>{NAMES[n]}</a></li>' for n in ns) + "</ol></div>"
    toc += "</nav>"
    pic = (f'<p class="explainer">Picture version for a first look: <a href="{picture[1]}">{picture[0]}</a></p>' if picture else "")
    out = (f'<header class="top"><p class="label">{code} · {SECS[code]}</p><h1>{e(title)}</h1>'
           f'<p class="lede">{lede}</p>{pic}{toc}</header>')

    def sec(n, inner):
        r = sec_roles.get(n, roles)
        return (f'<section class="sec" id="s{n}"><div class="rail"><span class="n">{n}</span><div class="chips">{chips(r)}</div></div>'
                f'<div class="body">{inner}</div></section>')

    for a, name, ns in ACTS:
        out += f'<div class="act"><span class="label">Act {a}</span><h2>{name}</h2></div>'
        for n in ns:
            if n <= 9:
                head = f"<h3>{H3.get(n, NAMES[n])}</h3>"
                if n == 1:
                    head += "<p>Spend two or three minutes on this before reading anything else.</p>"
                out += sec(n, head + sections[n])
            elif n == 10:
                out += sec(10, "<h3>Interview ladder</h3>" + ladder(slug, rungs))
            else:
                k = lambda s: f'<li><a href="#{s[0]}">{e(s[1])}</a></li>' if isinstance(s, tuple) else f"<li>{s}</li>"
                body = ("<h3>Your one-liner</h3><p>Without scrolling up, write the whole topic in one sentence.</p>"
                        f'<textarea id="ta-{slug}-one" placeholder="One sentence, from memory." aria-label="Your one-sentence summary"></textarea>'
                        + reveal(f"<p>{oneliner}</p>", "Compare with mine", "Hide")
                        + '<div class="q"><p>Now explain it out loud in 60 seconds to someone outside analytics. Then check your explanation against the list.</p>'
                        + reveal("<ul>" + "".join(f"<li>{c}</li>" for c in contains) + "</ul>", "What it should contain", "Hide") + "</div>"
                        + f'<div class="q"><p>One question about this topic you cannot answer yet.</p><textarea id="ta-{slug}-gap" placeholder="Bring this one to the next session." aria-label="A question you cannot answer yet"></textarea></div>'
                        + '<div class="links"><div><p class="label">Know these first</p><ul>' + "".join(k(s) for s in know)
                        + '</ul></div><div><p class="label">This unlocks</p><ul>' + "".join(k(s) for s in unlocks) + "</ul></div></div>")
                out += sec(11, body)
    foot = '<footer class="refs" id="refs"><p>Figures on this page were computed in code before publishing.</p>'
    if sources:
        foot += "<p>Sources:</p><ol>" + "".join(
            f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in sources) + "</ol>"
    out += foot + "</footer>"
    meta = {"slug": slug, "code": code, "title": title, "lede": html.unescape(lede), "keywords": keywords}
    path = os.path.join(ROOT, "extra", "pages", slug + ".html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf8").write(f"<!--meta {json.dumps(meta, ensure_ascii=False)}-->\n{out}\n")
    print("wrote", os.path.relpath(path, ROOT))


def ref(n):
    return f'<sup><a href="#refs" data-jump="refs">{n}</a></sup>'


def attempt(slug, n, placeholder="Your attempt. It stays on this page only."):
    return f'<textarea id="ta-{slug}-{n}" placeholder="{placeholder}" aria-label="{placeholder}"></textarea>'


if __name__ == "__main__":
    for f in sorted(glob.glob(os.path.join(ROOT, "extra", "src", "*.py"))):
        runpy.run_path(f)
