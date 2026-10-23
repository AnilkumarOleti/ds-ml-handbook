# DS/ML Learning Handbook

**Read it here: https://anilkumaroleti.github.io/ds-ml-handbook/**

83 concept pages on statistics, experimentation, causal inference, machine learning, SQL, product cases, data engineering, communication and leading an analytics team. Every page starts with a problem to attempt, hides every answer until you ask for it, and ends with a five-rung interview ladder. The handbook also has a mixed self-test across topics and an index of every interview question, filterable by role.

Nothing to install and nothing to download. The link opens in any browser, on a phone or a laptop.

## Studying with it

Everything below is kept in your browser only; nothing is sent anywhere.

- **Your status.** Mark each page *shaky* or *solid* at the top of the page. The home page shows progress by part and a dot beside every topic.
- **Saved answers.** Every answer box keeps what you type, so attempts, one-liners and open questions survive a reload.
- **Review** (`#review`). Spaced review of the 822 self-test questions. Questions you get right come back after 1, 3, 7, 14, 30, then 60 days; questions you miss come back tomorrow. New questions are drawn from pages you have opened.
- **Mock interview** (`#mock`). One ladder question at a time against a 3, 5 or 8-minute clock, filtered by role and rung. Open the follow-ups and the weak and strong answers, then grade yourself; weak grades mark the page shaky.
- **Plans** (`#plans`). Eight-week Lead, IC and MLE tracks, about five pages a week, with progress per week.
- **Notes** (`#notes`). Every open question and one-liner you have written, by topic, with a copy-all button.
- **Print with answers.** A button on every page prints it with all answers open and the interactive parts left out.

## Picture pages

Eleven topics also have a picture page: a five-picture story for a first look, then a hands-on toy. Each is linked from the top of its concept page.

| Topic | Picture page | The question it answers |
| :-- | :-- | :-- |
| A1 The central limit theorem | [The Bell Machine](https://anilkumaroleti.github.io/ds-ml-handbook/explainers/bell-machine.html) | Why do averages always pile into a bell? |
| A3 Sample size and power | [Size the Test](https://anilkumaroleti.github.io/ds-ml-handbook/explainers/size-the-test.html) | Did the new button win, or was it luck? |
| A4 Peeking and sequential testing | [Don't Peek](https://anilkumaroleti.github.io/ds-ml-handbook/explainers/dont-peek.html) | Why does checking early crown fake winners? |
| A5 Difference-in-differences | [The Ghost Line](https://anilkumaroleti.github.io/ds-ml-handbook/explainers/ghost-line.html) | How do you know what a launch really did? |
| B1 The bias-variance trade-off | [Stiff or Wiggly](https://anilkumaroleti.github.io/ds-ml-handbook/explainers/stiff-or-wiggly.html) | Why can a perfect fit predict badly? |
| B4 Precision, recall and the threshold | [Catch the Fraud](https://anilkumaroleti.github.io/ds-ml-handbook/explainers/catch-the-fraud.html) | How strict should a fraud alarm be? |
| B5 k-means and clustering | [Herd the Dots](https://anilkumaroleti.github.io/ds-ml-handbook/explainers/herd-the-dots.html) | How does a computer find groups nobody labelled? |
| B6 Neural networks and backpropagation | [Roll Downhill](https://anilkumaroleti.github.io/ds-ml-handbook/explainers/roll-downhill.html) | How does a model find its best settings? |
| B7 Encoders, decoders and sampling | [Turn Up the Heat](https://anilkumaroleti.github.io/ds-ml-handbook/explainers/turn-up-the-heat.html) | Why does a chatbot answer differently each time? |
| B7 Self-attention and the transformer | [Who Looks Where](https://anilkumaroleti.github.io/ds-ml-handbook/explainers/who-looks-where.html) | How does a model know what "its" refers to? |
| C3 Diagnosing a metric change | [The Sneaky Average](https://anilkumaroleti.github.io/ds-ml-handbook/explainers/sneaky-average.html) | How can the total fall when nothing got worse? |

## What is in this repository

- `index.html` is the whole handbook in one file.
- `explainers/` holds the eleven picture pages, one file each.
- `tools/make_site.py` rebuilds those files from the handbook's published pages. Run it with the folder of saved pages as its argument. Add `--reuse-explainers` when only the handbook has changed, and the picture pages already in `explainers/` are kept as they are. It gives each page a normal document head, points the handbook's picture-page links at `explainers/`, and adds a link from each picture page back to its concept page. It then runs `tools/enhance.py`.
- `extra/` is the part of the handbook that lives in this repository, added on top of every build by `tools/enhance.py`:
  - `extra/src/*.py`: six concept pages, written with `tools/pagekit.py` in the handbook's own markup. Run `python3 tools/pagekit.py` after editing one; it writes `extra/pages/`.
  - `extra/inserts/`: additions to existing pages (the A3 design lab).
  - `extra/labs.js`: the labs for those pages. `extra/check/*.py` compute every figure the pages and labs quote.
  - `extra/study.js` and `extra/study.css`: the study features above.
- `tools/enhance.py` adds the extra pages in section order (their self-tests and ladder questions join the mixed self-test, the question index, review and mock interview), turns every `@slug` cross-reference into a link, adds the labs and study features, and puts four small hooks into the handbook's script. It stops with an error if a hook no longer matches the builder's output, or if any `@slug` names a page that does not exist. Running it twice is safe.
- `tools/smoke_test.py` opens the built site in headless Chromium and checks every page, lab and study view. It needs `pip install playwright` and `playwright install chromium`.

### Pages added in this repository

| Page | Section |
| :-- | :-- |
| Likelihood, cross-entropy and KL divergence | B0 Mathematics for machine learning |
| Incrementality, attribution and marketing mix | C4 Product and marketing economics |
| ML system design, end to end | D3 ML systems in production |
| Communicating results to executives | E1 Communication |
| Building an analytics function | E2 Leading an analytics team |
| Fairness and responsible models | E3 Responsible practice |

The site is served from the `gh-pages` branch, which is kept identical to `main`. An update is pushed to both: `git push origin main main:gh-pages`.

The page sources and the handbook builder for the original 77 pages are kept outside this repository, so edits made directly to `index.html` are overwritten at the next update. Put changes in `extra/` instead, and they are reapplied on every build.
