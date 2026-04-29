"""Inline-level parse correctness — corners that block-level tests don't cover."""
from __future__ import annotations

from markast import NodeType as N
from markast import parse


def test_text_concatenation_when_normalize_off():
    p = parse("plain text").children[0]
    assert p["type"] == N.PARAGRAPH
    text_nodes = [c for c in p["children"] if c["type"] == N.TEXT]
    assert text_nodes and text_nodes[0]["value"] == "plain text"


def test_mixed_inline_formatting():
    p = parse("a **b** c *d* e").children[0]
    types = [c["type"] for c in p["children"]]
    assert N.BOLD in types
    assert N.ITALIC in types
    assert N.TEXT in types


def test_inline_code_in_paragraph():
    p = parse("`code` and text").children[0]
    assert p["children"][0]["type"] == N.CODE_INLINE
    assert p["children"][0]["value"] == "code"


def test_softbreak_between_lines():
    p = parse("line one\nline two").children[0]
    types = [c["type"] for c in p["children"]]
    assert N.SOFTBREAK in types


def test_hardbreak_two_spaces():
    p = parse("line one  \nline two").children[0]
    types = [c["type"] for c in p["children"]]
    assert N.HARDBREAK in types


def test_link_without_title():
    p = parse("[label](https://example.com)").children[0]
    a = p["children"][0]
    assert a["title"] is None
    assert a["href"] == "https://example.com"


def test_inline_image_alt_and_src():
    p = parse("see ![cap](url)").children[0]
    img = next(c for c in p["children"] if c["type"] == N.INLINE_IMAGE)
    assert img["alt"] == "cap"
    assert img["src"] == "url"
