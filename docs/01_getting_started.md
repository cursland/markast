# 1. Getting started

This page is the shortest possible path from "I just installed markast" to "I'm
shipping content to my client app." Everything here uses defaults — later
chapters cover configuration.

## Install

```bash
pip install markast
```

Optional extras:

* `pip install markast[test]` — pulls in `pytest` for running the test suite.
* `pip install linkify-it-py` — required if you want bare-URL detection
  (`autolinks` feature). The library degrades silently when this is missing.

## Parse some Markdown

```python
from markast import parse

doc = parse("# Hello\n\nA paragraph with **bold** and a [link](https://example.com).")

print(doc.to_json(indent=2))
```

Output (abbreviated):

```json
{
  "type": "document",
  "version": "1.0",
  "warnings": [],
  "children": [
    { "type": "heading", "level": 1, "children": [
        { "type": "text", "value": "Hello" }
    ] },
    { "type": "paragraph", "children": [
        { "type": "text", "value": "A paragraph with " },
        { "type": "bold", "children": [
            { "type": "text", "value": "bold" }
        ] },
        { "type": "text", "value": " and a " },
        { "type": "link", "href": "https://example.com", "title": null,
          "children": [ { "type": "text", "value": "link" } ] },
        { "type": "text", "value": "." }
      ] }
  ]
}
```

That's the whole API for the simplest case.

## Render

`parse()` returns a `Document`. The four operations you'll use most often are:

```python
doc.to_json(indent=2)   # str — the structured tree, for transport
doc.to_markdown()       # str — canonical Markdown, for editing UIs
doc.to_html()           # str — HTML, for server-side rendering
doc.to_dict()           # dict — the raw underlying tree
```

## Inspect warnings

The parser never raises on bad content. If something is invalid for client
rendering (an image inside a heading, an unknown widget, …), it emits a
diagnostic instead:

```python
doc = parse("# ![alt](logo.png)")
for w in doc.warnings:
    print(w["code"], w["message"])
# W001  Image inside h1 heading — alt text used as content.
```

The full diagnostic catalogue lives in [chapter 8](08_extending.md#rules)
and in `markast.rules.codes`.

## Use a registered widget

`markast` comes with several widgets pre-registered. The most useful is the
admonition family:

```python
from markast import parse

md = """
:::tip title="Pro tip"
You can nest **markdown** here.
:::
"""

doc = parse(md)
print(doc.to_html())
# <aside class="admonition admonition-tip"><header>Pro tip</header>
#   <div class="admonition-body"><p>You can nest <strong>markdown</strong> here.</p></div>
# </aside>
```

Other built-ins: `note`, `info`, `warning`, `caution`, `danger`, `card`,
`video`, `code-group`, `code-collapse`, `tabs`, `steps`, `badge`. See
[chapter 3](03_widgets.md) for full details and how to write your own.

## Where to go next

* **[2 — AST reference](02_ast_reference.md)**: every node type, every field.
* **[3 — Widgets](03_widgets.md)**: the most distinctive feature; this is
  what lets your content carry rich, structured components.
* **[7 — Client integration](07_client_integration.md)**: patterns for
  consuming the AST from a front-end of any technology.
