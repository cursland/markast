<div align="center">

<img src="https://raw.githubusercontent.com/cursland/markast/docs/assets/favicon.svg" width="72" alt="markast">

# markast

**Markdown → typed AST → JSON / Markdown / HTML**

Parse Markdown into a structured, typed tree your front-end can render — natively, server-side, or as JSON.

[![Version](https://img.shields.io/badge/version-1.0.0-6d52ff)](https://github.com/cursland/markast/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-6d52ff)](pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-6d52ff)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-cursland.github.io-6d52ff)](https://cursland.github.io/markast/)

[**Docs**](https://cursland.github.io/markast/) ·
[**Documentación (ES)**](https://cursland.github.io/markast/es/) ·
[**Examples**](examples/)

</div>

---

```python
from markast import parse

doc = parse("# Hello\n\nA paragraph with **bold** and a [link](https://example.com).")

doc.to_json()       # str — ship to any client renderer
doc.to_markdown()   # str — roundtrip
doc.to_html()       # str — server-side render
```

## Why a tree, not HTML?

HTML is a one-way street. Once your content is rendered, the structure is gone — clients can't restyle headings per platform, can't swap a `:::video` for a native player, can't extract a TOC without re-parsing.

**markast keeps the meaning intact.** Parse once, render anywhere:

- Native mobile renders headings with platform typography.
- The web renders `:::video` as a custom player; the terminal renders it as a link.
- Search indexes the same structured nodes that drive the UI.
- One source of content powers a docs site, a CMS preview, and a CLI.

## What you get

| Layer | What it gives you |
|---|---|
| 🌳 **AST** | Typed nodes (`TypedDict`), walker/visitor, JSON-Schema export, factory helpers |
| 🧱 **Widgets** | `:::widget` containers with typed params, named slots, validation — and a per-parser registry, no global state |
| 🛡️ **Rules** | Validation diagnostics that **never crash** — bad content is repaired and a warning is emitted |
| ⚙️ **Transforms** | AST → AST passes: normalize, slugify, TOC, autolink |
| 🔀 **Renderers** | Markdown (full roundtrip) and HTML (server-side) — both subclassable |
| 🧰 **Parser** | CommonMark + GFM (tables, strikethrough, tasklists, autolinks) + footnotes + custom containers |
| ⌨️ **CLI** | `markast parse file.md --format json` |

## Install

```bash
pip install markast
```

## 30-second tour

```python
from markast import Parser
from markast.widgets import BaseWidget, WidgetParam

class CalloutWidget(BaseWidget):
    name = "callout"
    params = {
        "level": WidgetParam(str, default="info", choices=["info", "warn", "error"]),
        "title": WidgetParam(str, default=None),
    }

parser = Parser(widgets=[CalloutWidget], transforms=["normalize", "slugify"])

doc = parser.parse("""
# Welcome

:::callout level=warn title="Heads up"
This is **important** content.
:::
""")

print(doc.to_json(indent=2))
print(doc.to_html())
```

`parser.parse(...)` always returns a valid `Document`. Invalid input is repaired and reported on `doc.warnings` — the parser never raises on user content.

## Documentation

Full docs live at **[cursland.github.io/markast](https://cursland.github.io/markast/)** (English / Español, light & dark).

| | |
|---|---|
| 🚀 [Getting started](https://cursland.github.io/markast/en/getting-started.html) | Install, parse, render |
| 🌳 [AST reference](https://cursland.github.io/markast/en/ast-reference.html) | Every node type and field |
| 🧱 [Widgets](https://cursland.github.io/markast/en/widgets.html) | Built-ins and authoring your own |
| ⚙️ [Transforms](https://cursland.github.io/markast/en/transforms.html) | Built-in passes and custom transforms |
| 🔀 [Renderers](https://cursland.github.io/markast/en/renderers.html) | Markdown, HTML, and subclassing |
| 🧭 [Walker & utilities](https://cursland.github.io/markast/en/walker.html) | Traverse and mutate the AST safely |
| 🌐 [Client integration](https://cursland.github.io/markast/en/client-integration.html) | Patterns for any front-end |
| 🧩 [Extending](https://cursland.github.io/markast/en/extending.html) | Custom rules, plugins, tokenizers |

## Examples

Runnable scripts in [`examples/`](examples):

- [`basic_parse.py`](examples/basic_parse.py) — simplest usage
- [`custom_widget.py`](examples/custom_widget.py) — register a widget
- [`transform_pipeline.py`](examples/transform_pipeline.py) — chain transforms
- [`render_html.py`](examples/render_html.py) — server-side HTML
- [`api_backend.py`](examples/api_backend.py) — FastAPI handler returning AST JSON

## Status

`1.0.0` — first stable release. Backwards-compatible changes follow semver.

## License

[MIT](LICENSE) © [cursland](https://cursland.com)
