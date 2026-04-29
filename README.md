# markast

> Markdown → typed AST → JSON / Markdown / HTML.
> Everything happens **inside the library**: parsing, validation, traversal, transformation, rendering. Clients only import, register their custom widgets, and consume the output.

```python
from markast import parse

doc = parse("# Hello\n\nA paragraph with **bold** and a [link](https://example.com).")

doc.to_json()         # str  — ship to any client renderer
doc.to_markdown()     # str  — roundtrip
doc.to_html()         # str  — server-side render
```

## Why markast?

This package solves one specific problem: **author content in Markdown, ship it to clients as a structured tree**, and let those clients render the tree however they want — native mobile widgets, React/Vue/Svelte components, plain HTML, terminal renderers, anything that can `switch` on a `type` discriminator.

It builds on `markdown-it-py` for tokenization and adds:

| Layer        | What it gives you |
|--------------|-------------------|
| **AST**      | Typed nodes (`TypedDict`), walker/visitor, JSON-Schema export, factory helpers |
| **Parser**   | CommonMark + GFM (tables, strikethrough, tasklists, autolinks) + footnotes + custom containers (`:::widget`) |
| **Widgets**  | Pluggable widget classes with typed params, named slots, validation. Per-parser registry — no global state |
| **Rules**    | Validation diagnostics that **never crash** — invalid content is repaired and a diagnostic is reported |
| **Transforms** | AST → AST mutations: normalize text spans, slugify headings, build TOC, autolink URLs |
| **Renderers**| Markdown (full roundtrip) and HTML (server-side) — both extensible |
| **CLI**      | `markast parse file.md --format json` |

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

## Installation

```bash
pip install markast
```

Or from a local checkout:

```bash
pip install -e .
```

## Documentation

The docs are organised from basic to advanced:

1. **[Getting started](docs/01_getting_started.md)** — install, parse, render
2. **[AST reference](docs/02_ast_reference.md)** — every node type, every field
3. **[Widgets](docs/03_widgets.md)** — built-in widgets and how to write your own
4. **[Transforms](docs/04_transforms.md)** — slugify, TOC, normalize, custom transforms
5. **[Renderers](docs/05_renderers.md)** — Markdown, HTML, and writing your own
6. **[Walker & utilities](docs/06_walker.md)** — traverse and mutate the AST safely
7. **[Client integration](docs/07_client_integration.md)** — patterns for consuming the AST from any front-end
8. **[Extending the parser](docs/08_extending.md)** — custom rules, plugins, tokenizers

## Examples

The [`examples/`](examples) folder has runnable scripts:

- `basic_parse.py` — simplest usage
- `custom_widget.py` — register a widget
- `transform_pipeline.py` — chain transforms
- `render_html.py` — server-side HTML
- `api_backend.py` — FastAPI handler that returns AST JSON

## Status

`1.0.0` — first stable release. Backwards-compatible changes follow semver.

## License

MIT.
