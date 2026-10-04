# DS/ML Learning Handbook

**Read it here: https://anilkumaroleti.github.io/ds-ml-handbook/**

59 concept pages on statistics, experimentation, causal inference, machine learning, SQL, product cases and data engineering. Every page starts with a problem to attempt, hides every answer until you ask for it, and ends with a five-rung interview ladder. The handbook also has a mixed self-test across topics and an index of every interview question, filterable by role.

Nothing to install and nothing to download. The link opens in any browser, on a phone or a laptop.

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
- `tools/make_site.py` rebuilds those files from the handbook's published pages. Run it with the folder of saved pages as its one argument. It gives each page a normal document head, points the handbook's picture-page links at `explainers/`, and adds a link from each picture page back to its concept page.

The site is served from the `gh-pages` branch, which is kept identical to `main`. An update is pushed to both: `git push origin main main:gh-pages`.

The page sources and the handbook builder are kept outside this repository. This repository holds the built pages only, so edits made directly to `index.html` are overwritten at the next update.
