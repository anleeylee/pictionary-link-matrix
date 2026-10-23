# -*- coding: utf-8 -*-
"""pictionary-link-matrix — backlink content matrix for a Pictionary word site.

Generates anchor-text link-building material around Pictionary keywords and
coordinates it across GitHub Pages, Kaggle and external placements. Every
generated link uses standard Markdown syntax [text](url) — never bare URLs —
so the material is safe to publish and safe for Google to pick up as a
natural backlink profile.

Standard library only.

Subcommands:
    generate    Build link-building material for a list of keywords: anchor
                variants, SERP-style description, GitHub README link block,
                GitHub Pages footer block and Kaggle dataset description.
    matrix      Build a cross-platform backlink matrix
                (platform x keyword x anchor x target URL x status).
    verify      Check a Markdown file for bare URLs and confirm all
                pictionarywordgenerators.com links use [text](url).

Examples:
    python link_matrix.py generate --keywords "pictionary words for christmas,easy pictionary words" --out-dir out
    python link_matrix.py generate --keywords-file examples/keywords.json --out-dir out
    python link_matrix.py matrix --keywords-file examples/keywords.json --out-dir out
    python link_matrix.py verify --file out/material.md
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys

SITE = "https://pictionarywordgenerators.com/"
HOMEPAGE = "https://pictionarywordgenerators.com/"
LIST_PAGE = "https://pictionarywordgenerators.com/list-of-pictionary-words"

# Keyword -> target inner page (the money page the anchor points at).
KEYWORD_PAGES = {
    "pictionary words for christmas": "https://pictionarywordgenerators.com/christmas-pictionary-words",
    "easy pictionary words": "https://pictionarywordgenerators.com/easy-pictionary-words",
    "hard pictionary words": "https://pictionarywordgenerators.com/hard-pictionary-words",
    "printable pictionary words": "https://pictionarywordgenerators.com/printable-pictionary-words",
    "how to play pictionary": "https://pictionarywordgenerators.com/how-to-play-pictionary",
    "list of pictionary words": LIST_PAGE,
    "virtual pictionary": "https://pictionarywordgenerators.com/virtual-pictionary",
}

# Anchor-text template library (by style). {k} is replaced with the keyword,
# {site} with the site name.
ANCHOR_TEMPLATES = {
    "branded": ["Pictionary Word Generator", "{site}", "Pictionary Word Generator — free drawing prompts"],
    "partial": ["free {k}", "{k} generator", "printable {k}", "online {k}"],
    "exact": ["{k}", "best {k}"],
    "generic": ["free drawing prompts", "party game word lists", "7000+ drawing prompt ideas"],
}

PLATFORMS = ["github-readme", "github-pages", "kaggle", "external"]


def _slug(keyword: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", keyword.lower()).strip("-")


def _lookup_target(keyword: str) -> str:
    return KEYWORD_PAGES.get(keyword.lower(), HOMEPAGE)


# --------------------------------------------------------------------------- #
# Material generation
# --------------------------------------------------------------------------- #
def generate_material(keyword: str, rng: random.Random) -> dict:
    """Build the full link-building material pack for one keyword."""
    target = _lookup_target(keyword)
    variants = []
    seen = set()
    for style, templates in ANCHOR_TEMPLATES.items():
        tmpl = rng.choice(templates)
        text = tmpl.format(k=keyword, site="Pictionary Word Generator")
        if text in seen:
            text = templates[0].format(k=keyword, site="Pictionary Word Generator")
        seen.add(text)
        variants.append({
            "style": style,
            "text": text,
            "link": f"[{text}]({target})",
        })
    headline = rng.choice([
        f"Free {keyword} — 100+ prompts to keep the party going",
        f"{keyword.title()} for every crowd: printable, silly and easy",
        f"The best {keyword} list — print it, shuffle it, draw it",
    ])
    description = (f"Looking for {keyword}? The generator serves thousands of "
                   "ready-to-draw prompts with difficulty filters, printable "
                   "lists and a live shuffle mode — no sign-up needed.")
    material = {
        "keyword": keyword,
        "slug": _slug(keyword),
        "target_url": target,
        "headline": headline,
        "description": description,
        "anchor_variants": variants,
        "github_readme_block": _github_readme_block(keyword, variants, rng),
        "github_pages_block": _github_pages_block(keyword, variants, rng),
        "kaggle_block": _kaggle_block(keyword, variants, rng),
    }
    return material


def _github_readme_block(keyword: str, variants: list[dict],
                         rng: random.Random) -> str:
    a = rng.choice(variants)
    b = rng.choice(variants)
    lines = [
        f"## {keyword.title()} — free drawing prompts",
        "",
        f"Need {keyword} for your next game night? The "
        f"[Pictionary Word Generator]({HOMEPAGE}) serves thousands of "
        f"prompts with difficulty filters, printable lists and a live "
        f"shuffle mode. Grab the {b['text']} list straight from "
        f"{a['link']} — no account, no sign-up.",
    ]
    return "\n".join(lines)


def _github_pages_block(keyword: str, variants: list[dict],
                        rng: random.Random) -> str:
    a = rng.choice(variants)
    return (f"Looking for more? Explore [free drawing prompts]"
            f"({HOMEPAGE}) or jump straight to the {keyword} collection: "
            f"{a['link']}.")


def _kaggle_block(keyword: str, variants: list[dict],
                  rng: random.Random) -> str:
    a = rng.choice(variants)
    lines = [
        f"**{keyword.title()}** — a ready-to-use prompt list for Pictionary "
        f"parties, classrooms and content creators.",
        "",
        f"- Format: JSON + CSV, ~100 prompts, difficulty-tagged",
        f"- Source tool: [Pictionary Word Generator]({HOMEPAGE})",
        f"- Live list: {a['link']}",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Matrix
# --------------------------------------------------------------------------- #
def build_matrix(keywords: list[str], rng: random.Random) -> dict:
    """Build the cross-platform backlink matrix."""
    rows = []
    for keyword in keywords:
        target = _lookup_target(keyword)
        material = generate_material(keyword, rng)
        for platform in PLATFORMS:
            anchor = rng.choice(material["anchor_variants"])
            rows.append({
                "platform": platform,
                "keyword": keyword,
                "anchor_text": anchor["text"],
                "anchor_style": anchor["style"],
                "target_url": target,
                "markdown_link": anchor["link"],
                "status": "pending",
                "notes": _platform_note(platform, keyword),
            })
    return {"keywords": keywords, "rows": rows,
            "generated": True, "tool": "pictionary-link-matrix"}


def _platform_note(platform: str, keyword: str) -> str:
    notes = {
        "github-readme": "README top link block of the sibling script repo",
        "github-pages": "Footer / resources block on a GitHub Pages page",
        "kaggle": "Dataset description block on Kaggle",
        "external": "Blog, forum or guest post placement",
    }
    return notes[platform]


def matrix_markdown(matrix: dict) -> str:
    lines = ["# Backlink Content Matrix", "",
             "| Platform | Keyword | Anchor text | Target URL | Status |",
             "|---|---|---|---|---|"]
    for row in matrix["rows"]:
        lines.append(f"| {row['platform']} | {row['keyword']} | "
                     f"{row['anchor_text']} | "
                     f"[{row['keyword']}]({row['target_url']}) | "
                     f"{row['status']} |")
    lines.append("")
    lines.append("Generated by [pictionary-link-matrix]"
                 "(https://github.com/anleeylee/pictionary-link-matrix) — "
                 "free prompts from [Pictionary Word Generator]"
                 "(https://pictionarywordgenerators.com/).")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Link hygiene check
# --------------------------------------------------------------------------- #
def check_markdown_links(text: str, domain: str = "pictionarywordgenerators.com") -> dict:
    """Find bare URLs on the domain outside code blocks and outside [text](url)."""
    no_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    pattern = re.compile(r"https?://" + re.escape(domain) + r"[^\s\)\]]*")
    bare = []
    links = []
    for m in pattern.finditer(no_code):
        prefix = no_code[: m.start()]
        if prefix.endswith("]("):
            links.append(m.group())
        else:
            bare.append(m.group())
    return {"bare_urls": bare, "markdown_links": links,
            "ok": len(bare) == 0}


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _load_keywords(args) -> list[str]:
    if args.keywords_file:
        with open(args.keywords_file, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        return payload if isinstance(payload, list) else payload.get("keywords", [])
    return [k.strip() for k in args.keywords.split(",") if k.strip()]


def _write(directory: str, name: str, content: str) -> str:
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return path


def cmd_generate(args: argparse.Namespace) -> int:
    keywords = _load_keywords(args)
    if not keywords:
        print("no keywords given", file=sys.stderr)
        return 1
    rng = random.Random(args.seed)
    packs = [generate_material(k, rng) for k in keywords]
    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "material.json"), "w",
              encoding="utf-8") as fh:
        json.dump(packs, fh, ensure_ascii=False, indent=2)
    md_parts = ["# Link-Building Material Pack", ""]
    for pack in packs:
        md_parts += [f"## {pack['keyword'].title()}",
                     "",
                     f"- **Target:** [{pack['keyword']}]({pack['target_url']})",
                     f"- **Headline:** {pack['headline']}",
                     f"- **Description:** {pack['description']}",
                     "",
                     "### Anchor variants", ""]
        for v in pack["anchor_variants"]:
            md_parts.append(f"- `{v['style']}`: {v['link']}")
        md_parts += ["",
                     "### GitHub README block", "",
                     pack["github_readme_block"], "",
                     "### GitHub Pages block", "",
                     pack["github_pages_block"], "",
                     "### Kaggle block", "",
                     pack["kaggle_block"], "",
                     "---", ""]
    path = _write(args.out_dir, "material.md", "\n".join(md_parts))
    print(f"Generated {len(packs)} material packs -> {args.out_dir}/ "
          f"(material.md + material.json), seed={args.seed}")
    return 0


def cmd_matrix(args: argparse.Namespace) -> int:
    keywords = _load_keywords(args)
    if not keywords:
        print("no keywords given", file=sys.stderr)
        return 1
    rng = random.Random(args.seed)
    matrix = build_matrix(keywords, rng)
    with open(os.path.join(args.out_dir, "matrix.json"), "w",
              encoding="utf-8") as fh:
        json.dump(matrix, fh, ensure_ascii=False, indent=2)
    path = _write(args.out_dir, "matrix.md", matrix_markdown(matrix))
    print(f"Matrix: {len(matrix['rows'])} placements "
          f"({len(keywords)} keywords x {len(PLATFORMS)} platforms) -> "
          f"{path}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    with open(args.file, "r", encoding="utf-8") as fh:
        text = fh.read()
    result = check_markdown_links(text, args.domain)
    print(f"bare URLs: {result['bare_urls'] if result['bare_urls'] else 'NONE'}")
    print(f"markdown links: {len(result['markdown_links'])}")
    print("hygiene:", "OK" if result["ok"] else "FAIL")
    return 0 if result["ok"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="link_matrix.py",
        description="Backlink content matrix generator for a Pictionary word "
                    "site — anchor-text link-building material for GitHub "
                    "Pages, Kaggle and external placements.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("generate", help="build link-building material packs")
    p.add_argument("--keywords", default="", help="comma-separated keywords")
    p.add_argument("--keywords-file", help="JSON file with [..] or "
                                           '{"keywords": [...]}')
    p.add_argument("--out-dir", required=True)
    p.add_argument("--seed", type=int, default=42)
    p.set_defaults(func=cmd_generate)

    p = sub.add_parser("matrix", help="build cross-platform backlink matrix")
    p.add_argument("--keywords", default="")
    p.add_argument("--keywords-file")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--seed", type=int, default=42)
    p.set_defaults(func=cmd_matrix)

    p = sub.add_parser("verify", help="check Markdown link hygiene")
    p.add_argument("--file", required=True)
    p.add_argument("--domain", default="pictionarywordgenerators.com")
    p.set_defaults(func=cmd_verify)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
