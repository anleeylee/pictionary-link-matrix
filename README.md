# Pictionary Link Matrix

> **Backlink content matrix generator for a Pictionary word site — builds anchor-text link-building material for GitHub Pages, Kaggle and external placements, and checks Markdown link hygiene. Every link is emitted as standard Markdown `[text](url)`, never a bare URL.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![CLI](https://img.shields.io/badge/CLI-ready-4B8BBE)](link_matrix.py)
[![No dependencies](https://img.shields.io/badge/deps-stdlib%20only-blueviolet)](requirements.txt)

---

## Links

- 🎲 **Try the live tool:** [Pictionary Word Generator — 7,000+ free drawing prompts](https://pictionarywordgenerators.com/)
- 📋 **Complete word list:** [List of Pictionary Words — 1,000+ prompts by difficulty](https://pictionarywordgenerators.com/list-of-pictionary-words)
- Read the Chinese version: [README.zh-CN.md](README.zh-CN.md)

---

## What it does

Building a link profile for a content site is repetitive: every placement
needs an anchor text, a target page and a platform block — and every anchor
must be a **standard Markdown link**, because bare URLs are ignored by many
publishers and look spammy to Google. This tool automates the whole assembly
line.

Three subcommands:

1. **`generate`** — for each Pictionary keyword, build a complete material
   pack: 4 anchor-text variants (branded / partial / exact / generic), a
   SERP-style description, a **GitHub README link block**, a **GitHub Pages
   footer block** and a **Kaggle dataset description block** — all with
   `[text](url)` links pointing at the keyword's money page.
2. **`matrix`** — build the cross-platform backlink matrix
   (platform × keyword × anchor × target × status), 4 platforms per keyword:
   `github-readme`, `github-pages`, `kaggle`, `external`.
3. **`verify`** — hygiene gate: scan any Markdown file for bare URLs on your
   domain (outside code blocks and outside `[text](url)`), report them and
   exit non-zero on failure. Run it in CI before publishing material.

Every keyword maps to its own money page automatically
(e.g. *pictionary words for christmas* → `/christmas-pictionary-words`,
*list of pictionary words* → `/list-of-pictionary-words`), so the anchors
always point at the most relevant page. Output is deterministic per `--seed`
for reproducible tests and review.

## Why it matters

The rest of the toolkit produces the site and the data:
[Pictionary Wordlist Generator](https://github.com/anleeylee/pictionary-wordlist-generator)
creates the word libraries, [Pictionary Page Generator](https://github.com/anleeylee/pictionary-page-generator)
builds the SEO pages, [Pictionary SEO Scanner](https://github.com/anleeylee/pictionary-seo-scanner)
keeps on-page SEO healthy, [Pictionary Keyword Tracker](https://github.com/anleeylee/pictionary-keyword-tracker)
decides what to build next and [Pictionary GSC Monitor](https://github.com/anleeylee/pictionary-gsc-monitor)
tracks what Google indexes. This tool closes the *off-page* gap: ready-to-paste
anchor-text material that grows the backlink profile across GitHub Pages,
Kaggle and external placements — with link hygiene enforced by design.

## Install

```bash
git clone https://github.com/anleeylee/pictionary-link-matrix.git
cd pictionary-link-matrix

# standard library only — no pip install needed
python link_matrix.py --help
```

## Usage

```bash
# 1. build material packs for keywords
python link_matrix.py generate \
  --keywords "pictionary words for christmas,easy pictionary words" \
  --out-dir out

# or from a file
python link_matrix.py generate \
  --keywords-file examples/keywords.json --out-dir out

# 2. build the cross-platform backlink matrix
python link_matrix.py matrix \
  --keywords-file examples/keywords.json --out-dir out

# 3. hygiene gate (CI-friendly, exits non-zero on bare URLs)
python link_matrix.py verify --file out/material.md
```

### Output

- `material.md` / `material.json` — per-keyword material packs: anchor
  variants, headline, description, GitHub README / GitHub Pages / Kaggle
  blocks
- `matrix.md` / `matrix.json` — the cross-platform backlink matrix
  (keywords × platforms, with anchor text, target URL and status)

## Tests

```bash
python -m unittest discover -s tests -v
```

Covers material shape and target-page mapping, anchor variant generation,
zero-bare-URL guarantee for every generated block, matrix sizing
(keywords × 4 platforms), bare-URL detection and code-block exemption in the
hygiene check, and full CLI runs. 11 tests, all offline.

## License

MIT — use it, extend it, keep the attribution. The anchor material you
generate is yours to publish anywhere.
