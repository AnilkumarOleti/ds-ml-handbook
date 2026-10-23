#!/usr/bin/env python3
"""Open the built handbook in headless Chromium and check every page and study view.

    python3 tools/smoke_test.py [--shots DIR]

Fails if any page throws a script error, any lab fails to mount, any raw "@slug" text is left,
or a study feature does not behave (saved answers, status marks, review grading, mock interview).
"""
import json
import os
import re
import sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "file://" + os.path.join(ROOT, "index.html")
shots = sys.argv[sys.argv.index("--shots") + 1] if "--shots" in sys.argv else None


def main():
    errors, fails = [], []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 900})
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" and "Failed to load resource" not in m.text else None)
        pg.goto(URL)
        data = pg.evaluate("JSON.parse(document.getElementById('hb-data').textContent)")
        slugs = [x["slug"] for x in data["pages"]]
        for s in slugs:
            pg.evaluate(f"HB.route('{s}')")
            r = pg.evaluate("""() => {
              const v=document.getElementById('view');
              const labs=[...v.querySelectorAll('.lab[data-lab]')];
              return {h1:(v.querySelector('h1')||{}).textContent||'',
                labs:labs.length, bad:labs.filter(l=>l.textContent.includes('not available')||!l.querySelector('svg,.bars,.stats')).length,
                raw:(v.innerText.match(/@[a-z]\\d-[a-z0-9-]+/g)||[]), mark:!!v.querySelector('.mark')}}""")
            if r["bad"] or r["raw"] or not r["mark"] or not r["h1"]:
                fails.append((s, r))
        print(f"pages checked: {len(slugs)}")

        # saved answer boxes and status marks survive a reload
        pg.evaluate("HB.route('b0-likelihood-entropy')")
        pg.fill("#ta-b0-likelihood-entropy-1", "B wins on log loss")
        pg.fill("#ta-b0-likelihood-entropy-gap", "When is Brier better?")
        pg.wait_for_timeout(600)
        pg.click(".mark button[data-v=shaky]")
        pg.reload(); pg.evaluate("HB.route('b0-likelihood-entropy')")
        if pg.input_value("#ta-b0-likelihood-entropy-1") != "B wins on log loss":
            fails.append(("saved answer", "not restored"))
        if pg.get_attribute(".mark button[data-v=shaky]", "aria-pressed") != "true":
            fails.append(("status mark", "not restored"))

        # home shows progress and dots
        pg.evaluate("HB.route('')")
        if not pg.query_selector(".prog") or not pg.query_selector("#parts .dot.shaky"):
            fails.append(("home", "progress panel or status dot missing"))
        pg.fill("#find", "likelihood")
        if not pg.query_selector("#parts .row[href='#b0-likelihood-entropy']"):
            fails.append(("search", "new page not found by search"))
        if shots: pg.screenshot(path=os.path.join(shots, "home.png"))

        # review queue: grade a card
        pg.evaluate("HB.route('review')")
        if not pg.query_selector(".card"):
            fails.append(("review", "no cards"))
        else:
            pg.click(".card details summary"); pg.click(".card .grade button[data-g='1']")
            n = pg.evaluate("Object.keys(JSON.parse(localStorage.getItem('hb:rv')||'{}')).length")
            if n != 1: fails.append(("review", f"grade not stored ({n})"))
        if shots: pg.screenshot(path=os.path.join(shots, "review.png"))

        # mock interview
        pg.evaluate("HB.route('mock')")
        pg.click("#mkGo"); pg.wait_for_timeout(1100)
        clock = pg.text_content("#mkClock")
        pg.click("#mkShow")
        if not pg.query_selector("#mkRub .ws"): fails.append(("mock", "rubric not shown"))
        if shots: pg.screenshot(path=os.path.join(shots, "mock.png"), full_page=True)
        pg.click("#mkRub button[data-g='2']")
        if pg.evaluate("JSON.parse(localStorage.getItem('hb:mock')||'[]').length") != 1:
            fails.append(("mock", "grade not stored"))
        print("mock clock read", clock)

        # plans and notes
        pg.evaluate("HB.route('plans')")
        nweeks = pg.evaluate("document.querySelectorAll('.week').length")
        missing = pg.evaluate("""() => { const T=[...document.querySelectorAll('.plist a')].map(a=>a.getAttribute('href').slice(1));
            return T.filter(s=>!HB.by[s]) }""")
        if nweeks != 8 or missing: fails.append(("plans", nweeks, missing))
        for t in ("ic", "mle"):
            pg.click(f"[data-t={t}]")
            n = pg.evaluate("document.querySelectorAll('.plist li').length")
            print(f"plan {t}: {n} pages")
        pg.evaluate("HB.route('notes')")
        if "When is Brier better?" not in pg.inner_text("#view"): fails.append(("notes", "gap note missing"))

        # mixed self-test and question index include the new pages
        pg.evaluate("HB.route('questions')")
        if "B0" not in pg.inner_text("#view"): fails.append(("questions", "B0 missing"))

        # print opens every answer
        pg.evaluate("HB.route('a3-experiment-design')")
        pg.evaluate("window.dispatchEvent(new Event('beforeprint'))")
        closed = pg.evaluate("[...document.querySelectorAll('#view details')].filter(d=>!d.open).length")
        pg.evaluate("window.dispatchEvent(new Event('afterprint'))")
        if closed: fails.append(("print", f"{closed} answers still closed"))
        if shots:
            pg.screenshot(path=os.path.join(shots, "a3.png"))
            pg.emulate_media(media="print"); pg.pdf(path=os.path.join(shots, "print.pdf")); pg.emulate_media(media="screen")

        # phone width: no horizontal scroll on a new page
        m = b.new_page(viewport={"width": 375, "height": 800})
        m.on("pageerror", lambda e: errors.append(str(e)))
        m.goto(URL)
        for s in [x for x in slugs if x in sys.argv] or slugs[-8:] + ["b0-likelihood-entropy", "a3-experiment-design"]:
            m.evaluate(f"HB.route('{s}')")
            w = m.evaluate("document.documentElement.scrollWidth")
            if w > 380: fails.append(("phone width", s, w))
        if shots:
            m.evaluate("HB.route('b0-likelihood-entropy')"); m.screenshot(path=os.path.join(shots, "phone.png"))
        b.close()

    for e in errors: print("SCRIPT ERROR:", e)
    for f in fails: print("FAIL:", f)
    if errors or fails:
        sys.exit(1)
    print("smoke test passed")


if __name__ == "__main__":
    main()
