"""Markdown roundtrip tests."""
from __future__ import annotations

from markast import parse


def rt(md: str) -> str:
    return parse(md).to_markdown()


# ── Headings & paragraphs ────────────────────────────────────────────────────
def test_rt_heading_h1():
    assert rt("# Hello") == "# Hello"


def test_rt_heading_h3():
    assert rt("### Section") == "### Section"


def test_rt_plain():
    assert rt("Hello world") == "Hello world"


# ── Inline ──────────────────────────────────────────────────────────────────
def test_rt_bold():
    assert "**bold**" in rt("**bold** text")


def test_rt_italic():
    assert "*italic*" in rt("*italic* text")


def test_rt_strike():
    assert "~~del~~" in rt("~~del~~")


def test_rt_inline_code():
    assert "`code`" in rt("Use `code` here")


def test_rt_link():
    assert "[Click](https://example.com)" in rt("[Click](https://example.com)")


def test_rt_image():
    assert "![alt](img.png)" in rt("![alt](img.png)")


# ── Code blocks ──────────────────────────────────────────────────────────────
def test_rt_code_block():
    out = rt("```python\nprint('hi')\n```")
    assert "```python" in out
    assert "print" in out


def test_rt_code_block_filename():
    assert "[app.ts]" in rt("```ts [app.ts]\nconst x = 1;\n```")


def test_rt_code_block_highlight_lines():
    assert "{1,3-5}" in rt("```py{1,3-5}\na\nb\nc\nd\ne\n```")


# ── Blockquote / divider ─────────────────────────────────────────────────────
def test_rt_blockquote():
    out = rt("> A quote")
    assert out.startswith(">")
    assert "A quote" in out


def test_rt_divider():
    assert "---" in rt("---")


# ── Lists ────────────────────────────────────────────────────────────────────
def test_rt_unordered():
    out = rt("- a\n- b")
    assert "- a" in out and "- b" in out


def test_rt_ordered():
    out = rt("1. a\n2. b")
    assert "1." in out and "2." in out


def test_rt_tasklist():
    out = rt("- [x] done\n- [ ] todo")
    assert "[x] done" in out
    assert "[ ] todo" in out


# ── Tables ───────────────────────────────────────────────────────────────────
def test_rt_table():
    out = rt("| A | B |\n|---|---|\n| 1 | 2 |")
    assert "| A | B |" in out
    assert "| 1 | 2 |" in out


# ── Widgets ──────────────────────────────────────────────────────────────────
def test_rt_tip_widget():
    out = rt(':::tip title="My Tip"\n\nContent\n\n:::')
    assert ":::tip" in out
    assert 'title="My Tip"' in out
    assert "Content" in out


def test_rt_card_with_footer_slot():
    md = """:::card title="Card"

body

# footer

footer text

:::"""
    out = rt(md)
    assert ":::card" in out
    assert "footer" in out


def test_rt_video_widget():
    out = rt(':::video src="v.mp4" controls\n:::')
    assert ":::video" in out
    assert 'src="v.mp4"' in out


# ── from_json round trip ─────────────────────────────────────────────────────
def test_json_roundtrip():
    from markast import from_json
    md = "# Hi\n\nPara with **bold**."
    doc = parse(md)
    js = doc.to_json()
    back = from_json(js)
    assert back.to_markdown().startswith("# Hi")
