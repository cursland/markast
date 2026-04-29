"""Block-level parse correctness."""
from __future__ import annotations
import pytest

from markast import NodeType as N
from markast import parse


def first_child(doc, type_=None):
    children = doc.children
    if type_:
        return next((c for c in children if c["type"] == type_), None)
    return children[0] if children else None


# ── Document root ────────────────────────────────────────────────────────────
def test_document_root():
    doc = parse("Hello")
    assert doc.root["type"] == N.DOCUMENT
    assert doc.version == "1.0"
    assert isinstance(doc.warnings, list)
    assert isinstance(doc.children, list)


# ── Headings ─────────────────────────────────────────────────────────────────
def test_heading_h1():
    doc = parse("# Hello World")
    h = first_child(doc)
    assert h["type"] == N.HEADING
    assert h["level"] == 1
    assert h["children"][0] == {"type": N.TEXT, "value": "Hello World"}


def test_heading_setext_h2():
    h = first_child(parse("My Title\n--------"))
    assert h["type"] == N.HEADING and h["level"] == 2


@pytest.mark.parametrize("lvl", range(1, 7))
def test_heading_levels(lvl):
    h = first_child(parse(f"{'#' * lvl} Title"))
    assert h["level"] == lvl


def test_heading_image_warns_and_collapses_to_alt():
    doc = parse("# ![alt text](img.png)")
    assert doc.has_warnings("W001")
    h = first_child(doc)
    assert h["children"][0] == {"type": N.TEXT, "value": "alt text"}


# ── Paragraphs ───────────────────────────────────────────────────────────────
def test_paragraph_plain():
    p = first_child(parse("Hello world"))
    assert p["type"] == N.PARAGRAPH
    assert p["children"][0]["value"] == "Hello world"


def test_paragraph_bold():
    p = first_child(parse("**bold text**"))
    assert p["children"][0]["type"] == N.BOLD
    assert p["children"][0]["children"][0]["value"] == "bold text"


def test_paragraph_italic():
    p = first_child(parse("*italic*"))
    assert p["children"][0]["type"] == N.ITALIC


def test_paragraph_inline_code():
    p = first_child(parse("Use `print()` here"))
    assert any(c["type"] == N.CODE_INLINE for c in p["children"])


def test_paragraph_strikethrough():
    p = first_child(parse("~~deleted~~"))
    assert p["children"][0]["type"] == N.STRIKETHROUGH


def test_paragraph_link_with_title():
    p = first_child(parse('[Click](https://example.com "Tip")'))
    a = p["children"][0]
    assert a["type"] == N.LINK
    assert a["href"] == "https://example.com"
    assert a["title"] == "Tip"


# ── Standalone image ─────────────────────────────────────────────────────────
def test_standalone_image_hoisted():
    img = first_child(parse("![alt](https://img.png)"))
    assert img["type"] == N.IMAGE
    assert img["src"] == "https://img.png"


def test_inline_image_stays_inline():
    p = first_child(parse("See ![logo](logo.png) here"))
    assert p["type"] == N.PARAGRAPH
    assert any(c["type"] == N.INLINE_IMAGE for c in p["children"])


# ── Code blocks ──────────────────────────────────────────────────────────────
def test_code_block_language():
    cb = first_child(parse("```python\nprint('hi')\n```"))
    assert cb["type"] == N.CODE_BLOCK
    assert cb["language"] == "python"
    assert "print" in cb["value"]


def test_code_block_filename():
    cb = first_child(parse("```ts [app.ts]\nconst x = 1;\n```"))
    assert cb["filename"] == "app.ts"
    assert cb["language"] == "ts"


def test_code_block_highlight_lines():
    cb = first_child(parse("```py{1,3-5}\na\nb\nc\nd\ne\n```"))
    assert 1 in cb["highlight_lines"]
    assert 3 in cb["highlight_lines"]
    assert 5 in cb["highlight_lines"]


# ── Blockquote ───────────────────────────────────────────────────────────────
def test_blockquote():
    bq = first_child(parse("> A quote"))
    assert bq["type"] == N.BLOCKQUOTE
    assert bq["children"][0]["type"] == N.PARAGRAPH


# ── Lists ────────────────────────────────────────────────────────────────────
def test_unordered_list():
    lst = first_child(parse("- a\n- b\n- c"))
    assert lst["type"] == N.LIST
    assert lst["ordered"] is False
    assert len(lst["children"]) == 3


def test_ordered_list():
    lst = first_child(parse("1. a\n2. b\n3. c"))
    assert lst["ordered"] is True
    assert lst["start"] == 1


def test_nested_list():
    parent_item = first_child(parse("- p\n  - c1\n  - c2"))["children"][0]
    nested = next(c for c in parent_item["children"] if c["type"] == N.LIST)
    assert len(nested["children"]) == 2


def test_tasklist_checkboxes():
    lst = first_child(parse("- [x] done\n- [ ] todo"))
    assert lst["children"][0]["checked"] is True
    assert lst["children"][1]["checked"] is False


# ── Tables ───────────────────────────────────────────────────────────────────
def test_table():
    t = first_child(parse("| A | B |\n|---|---|\n| 1 | 2 |"))
    assert t["type"] == N.TABLE
    assert len(t["head"]["rows"]) == 1
    assert len(t["body"]["rows"]) == 1


def test_table_header_marked():
    t = first_child(parse("| Name | Age |\n|------|-----|\n| Ana  | 30  |"))
    cells = t["head"]["rows"][0]["cells"]
    assert all(c["is_header"] for c in cells)


def test_table_alignment():
    t = first_child(parse("| L | C | R |\n|:--|:--:|--:|\n| a | b | c |"))
    aligns = [c["align"] for c in t["head"]["rows"][0]["cells"]]
    assert aligns == ["left", "center", "right"]


# ── Divider ──────────────────────────────────────────────────────────────────
def test_divider():
    assert first_child(parse("---"))["type"] == N.DIVIDER


# ── Multiple blocks ──────────────────────────────────────────────────────────
def test_multiple_blocks():
    types = [c["type"] for c in parse("# T\n\nP\n\n- a").children]
    assert N.HEADING in types and N.PARAGRAPH in types and N.LIST in types
