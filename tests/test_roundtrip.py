"""End-to-end roundtrip stability — parse, serialise, reload, re-render."""
from __future__ import annotations

from markast import from_json, parse


SAMPLE = """# Title

A paragraph with **bold**, *italic*, and a [link](https://example.com).

- item one
- item two

```python
print("hi")
```

> A quote.

| col1 | col2 |
|------|------|
| a    | b    |

:::tip title="Pro tip"
A useful **tip**.
:::
"""


def test_parse_then_render_is_stable():
    doc1 = parse(SAMPLE)
    md1 = doc1.to_markdown()
    doc2 = parse(md1)
    md2 = doc2.to_markdown()
    assert md1 == md2  # idempotent after the first render


def test_json_serialization_preserves_structure():
    doc1 = parse(SAMPLE)
    js = doc1.to_json()
    doc2 = from_json(js)
    assert doc1.count() == doc2.count()
    assert doc1.to_markdown() == doc2.to_markdown()


def test_html_render_does_not_crash_on_full_sample():
    out = parse(SAMPLE).to_html()
    # Sanity checks — full string match is fragile, so check landmarks.
    assert "<h1>" in out
    assert "<table>" in out
    assert '<aside class="admonition admonition-tip">' in out


def test_jsonschema_describes_document():
    from markast import json_schema
    s = json_schema()
    assert s["title"] == "markast Document"
    props = s["properties"]
    assert "type" in props and "version" in props and "warnings" in props
