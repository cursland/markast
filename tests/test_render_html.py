"""HTML-renderer correctness."""
from __future__ import annotations

from markast import HTMLRenderer, parse


def html(md: str) -> str:
    return parse(md).to_html()


def test_heading_html():
    assert "<h1>Hello</h1>" in html("# Hello")


def test_paragraph_html():
    assert "<p>" in html("hi") and "</p>" in html("hi")


def test_bold_html():
    assert "<strong>bold</strong>" in html("**bold**")


def test_italic_html():
    assert "<em>italic</em>" in html("*italic*")


def test_link_html():
    out = html("[Go](https://example.com)")
    assert '<a href="https://example.com">Go</a>' in out


def test_image_html():
    out = html("![cap](url)")
    assert 'src="url"' in out and 'alt="cap"' in out


def test_code_block_html_escaped():
    out = html("```html\n<b>hi</b>\n```")
    assert "&lt;b&gt;hi&lt;/b&gt;" in out
    assert 'class="lang-html"' in out


def test_code_block_with_filename_uses_figure():
    out = html("```ts [app.ts]\nconst x = 1;\n```")
    assert "<figure" in out and "<figcaption>app.ts</figcaption>" in out


def test_table_html():
    out = html("| A | B |\n|:--|--:|\n| 1 | 2 |")
    assert "<table>" in out
    assert "<th" in out
    assert "text-align:left" in out
    assert "text-align:right" in out


def test_admonition_html_uses_aside():
    out = html(":::tip title=\"Hi\"\nbody\n:::")
    assert '<aside class="admonition admonition-tip">' in out
    assert "<header>Hi</header>" in out


def test_unknown_widget_html_fallback():
    out = html(":::xyz-unknown\nhi\n:::")
    assert 'class="widget widget-xyz-unknown"' in out


def test_wrap_root_option():
    doc = parse("# Hi")
    out = HTMLRenderer(wrap_root=True).render(doc.root)
    assert out.startswith('<article class="markast">')
    assert out.endswith("</article>")


def test_html_special_chars_escaped_in_text():
    out = html("Use < and & here")
    assert "&lt;" in out
    assert "&amp;" in out
