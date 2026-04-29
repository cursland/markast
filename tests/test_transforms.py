"""Transform pipeline tests."""
from __future__ import annotations

from markast import NodeType as N
from markast import Parser
from markast.ast.walker import walk
from markast.transforms import (
    BuildTOC, Linkify, NormalizeText, SlugifyHeadings, SmartTypography,
)


def test_normalize_merges_adjacent_text():
    parser = Parser(transforms=["normalize"])
    # Markdown-it occasionally splits text — we synthesise a multi-text para
    # by parsing inline-emphasis-then-text and ensuring there's no empty span.
    doc = parser.parse("hello **world** today")
    p = doc.children[0]
    text_values = [c.get("value") for c in p["children"] if c["type"] == N.TEXT]
    assert all(v != "" for v in text_values)


def test_slugify_assigns_ids():
    parser = Parser(transforms=["slugify"])
    doc = parser.parse("# Hello World!\n\n## Sub Section")
    headings = [c for c in doc.children if c["type"] == N.HEADING]
    assert headings[0]["id"] == "hello-world"
    assert headings[1]["id"] == "sub-section"


def test_slugify_dedupes_collisions():
    parser = Parser(transforms=["slugify"])
    doc = parser.parse("# Intro\n\n# Intro")
    ids = [c["id"] for c in doc.children if c["type"] == N.HEADING]
    assert ids == ["intro", "intro-2"]


def test_slugify_unicode():
    parser = Parser(transforms=["slugify"])
    doc = parser.parse("# Configuración rápida")
    assert doc.children[0]["id"] == "configuracion-rapida"


def test_toc_requires_slugify():
    parser = Parser(transforms=["slugify", "toc"])
    doc = parser.parse("# Top\n\n## Mid\n\n### Leaf\n\n# Top2")
    toc = doc.meta.get("toc")
    assert toc is not None
    assert toc[0]["text"] == "Top"
    assert toc[0]["children"][0]["text"] == "Mid"
    assert toc[0]["children"][0]["children"][0]["text"] == "Leaf"
    assert toc[1]["text"] == "Top2"


def test_linkify_detects_bare_urls():
    parser = Parser(transforms=["linkify"])
    doc = parser.parse("Visit https://example.com today.")
    p = doc.children[0]
    types = [c["type"] for c in p["children"]]
    assert N.LINK in types


def test_linkify_doesnt_touch_existing_links():
    parser = Parser(transforms=["linkify"])
    doc = parser.parse("[Already](https://example.com)")
    p = doc.children[0]
    # Should still be exactly one link — not a nested or duplicated one.
    links = [c for c in walk(p) if c.get("type") == N.LINK]
    assert len(links) == 1


def test_smarttypography_dashes():
    parser = Parser(transforms=["smarttypography"])
    doc = parser.parse("a -- b --- c")
    p = doc.children[0]
    text = "".join(c.get("value", "") for c in p["children"] if c["type"] == N.TEXT)
    assert "–" in text  # en dash
    assert "—" in text  # em dash


def test_smarttypography_skips_code():
    parser = Parser(transforms=["smarttypography"])
    doc = parser.parse("`a -- b`")
    p = doc.children[0]
    code = next(c for c in p["children"] if c["type"] == N.CODE_INLINE)
    assert "--" in code["value"]
