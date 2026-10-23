# -*- coding: utf-8 -*-
"""Tests for pictionary-link-matrix. Run:

    python -m unittest discover -s tests -v
"""
import json
import re
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from link_matrix import (  # noqa: E402
    KEYWORD_PAGES,
    LIST_PAGE,
    PLATFORMS,
    build_matrix,
    check_markdown_links,
    generate_material,
    main,
    matrix_markdown,
)

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
DOMAIN = "pictionarywordgenerators.com"


def all_md_links(text):
    return re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", text)


class GenerateTests(unittest.TestCase):
    def test_material_shape(self):
        mat = generate_material("easy pictionary words", __import__("random").Random(1))
        self.assertEqual(mat["target_url"],
                         "https://pictionarywordgenerators.com/easy-pictionary-words")
        self.assertEqual(len(mat["anchor_variants"]), 4)
        for v in mat["anchor_variants"]:
            self.assertIn("style", v)
            self.assertRegex(v["link"], r"^\[.+\]\(https?://.+\)$")

    def test_target_mapping_has_list_page(self):
        self.assertEqual(KEYWORD_PAGES["list of pictionary words"], LIST_PAGE)

    def test_generated_material_has_no_bare_urls(self):
        mat = generate_material("pictionary words for christmas",
                                __import__("random").Random(7))
        blocks = [
            mat["github_readme_block"],
            mat["github_pages_block"],
            mat["kaggle_block"],
        ]
        for block in blocks:
            result = check_markdown_links(block, DOMAIN)
            self.assertEqual(result["bare_urls"], [])
            self.assertGreater(len(result["markdown_links"]), 0)


class MatrixTests(unittest.TestCase):
    def test_matrix_size(self):
        keywords = ["easy pictionary words", "hard pictionary words"]
        matrix = build_matrix(keywords, __import__("random").Random(2))
        self.assertEqual(len(matrix["rows"]), 2 * len(PLATFORMS))
        for row in matrix["rows"]:
            self.assertIn(row["platform"], PLATFORMS)
            self.assertRegex(row["markdown_link"],
                             r"^\[.+\]\(https?://.+\)$")

    def test_matrix_markdown_hygiene(self):
        matrix = build_matrix(["easy pictionary words"],
                              __import__("random").Random(3))
        md = matrix_markdown(matrix)
        result = check_markdown_links(md, DOMAIN)
        self.assertEqual(result["bare_urls"], [])


class VerifyTests(unittest.TestCase):
    def test_detects_bare_url(self):
        text = "See https://pictionarywordgenerators.com/easy-pictionary-words now"
        result = check_markdown_links(text, DOMAIN)
        self.assertEqual(len(result["bare_urls"]), 1)
        self.assertFalse(result["ok"])

    def test_accepts_markdown_link(self):
        text = "See [easy pictionary words](https://pictionarywordgenerators.com/easy-pictionary-words)"
        result = check_markdown_links(text, DOMAIN)
        self.assertEqual(result["bare_urls"], [])
        self.assertTrue(result["ok"])

    def test_ignores_code_blocks(self):
        text = "```\nhttps://pictionarywordgenerators.com/hard-pictionary-words\n```\nOk."
        result = check_markdown_links(text, DOMAIN)
        self.assertEqual(result["bare_urls"], [])


class CliTests(unittest.TestCase):
    def test_generate_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            code = main(["generate", "--keywords",
                         "easy pictionary words,hard pictionary words",
                         "--out-dir", tmp, "--seed", "5"])
            self.assertEqual(code, 0)
            md = (Path(tmp) / "material.md").read_text(encoding="utf-8")
            self.assertIn("easy pictionary words", md)
            result = check_markdown_links(md, DOMAIN)
            self.assertEqual(result["bare_urls"], [])

    def test_matrix_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            code = main(["matrix", "--keywords-file",
                         str(EXAMPLES / "keywords.json"),
                         "--out-dir", tmp, "--seed", "9"])
            self.assertEqual(code, 0)
            mj = json.loads((Path(tmp) / "matrix.json").read_text(
                encoding="utf-8"))
            self.assertEqual(len(mj["rows"]), 7 * len(PLATFORMS))

    def test_verify_detects_bad_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.md"
            bad.write_text("https://pictionarywordgenerators.com/x",
                           encoding="utf-8")
            self.assertEqual(main(["verify", "--file", str(bad)]), 1)


if __name__ == "__main__":
    unittest.main()
