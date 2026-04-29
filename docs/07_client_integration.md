# 7. Client integration

This chapter covers the standard pattern for shipping markast output to a
client — regardless of which technology that client uses. The ideas are the
same whether you're rendering with React, Vue, Svelte, native iOS / Android
widgets, terminal UIs, or any other system that can `switch` on a string.

## The pipeline

```
┌──────────────┐    parse()     ┌──────────┐   to_json()   ┌───────────┐    HTTP    ┌──────────────┐
│  Markdown    │ ─────────────► │   AST    │ ────────────► │   JSON    │ ─────────► │   Client     │
│  source      │                │  (dict)  │               │  (string) │            │  renderer    │
└──────────────┘                └──────────┘               └───────────┘            └──────────────┘
```

Every step happens **server-side**. The client receives a typed JSON tree
and walks it. The client never parses Markdown.

## A FastAPI handler

```python
# server.py
from fastapi import FastAPI
from markast import Parser

app = FastAPI()
parser = Parser(transforms=["normalize", "slugify", "toc"])


@app.get("/content/{slug}")
def get_content(slug: str):
    markdown = load_from_db(slug)         # your DB code
    doc = parser.parse(markdown)

    return {
        "ast":      doc.to_dict(),
        "warnings": doc.warnings,
        "toc":      doc.meta.get("toc", []),
    }
```

Three calls, one parser instance reused across requests. The
`Parser.parse()` method is thread-safe for read operations (the tokenizer
is rebuilt only when its registry changes).

## Client-side: switch on `type`

The client receives the JSON tree and writes one function per node type.
Pseudocode that ports cleanly to any front-end:

```text
function render(node):
    switch node.type:
        case "document":   render_each(node.children)
        case "heading":    return text_with_size(node.level, render_inline(node.children))
        case "paragraph":  return text(render_inline(node.children))
        case "list":       return list_view(node.ordered, render_each(node.children))
        case "list_item":  return list_item(render_each(node.children), checked=node.checked)
        case "image":      return image(node.src, node.alt)
        case "code_block": return code(node.language, node.value, filename=node.filename)
        case "table":      return table(render_table(node.head, node.body))
        case "blockquote": return quote(render_each(node.children))
        case "divider":    return divider()
        case "widget":     return render_widget(node)
        ...

function render_inline(nodes):
    parts = []
    for n in nodes:
        switch n.type:
            case "text":           parts.add(plain(n.value))
            case "bold":           parts.add(bold(render_inline(n.children)))
            case "italic":         parts.add(italic(render_inline(n.children)))
            case "code_inline":    parts.add(code_span(n.value))
            case "link":           parts.add(link(n.href, render_inline(n.children)))
            case "strikethrough":  parts.add(strike(render_inline(n.children)))
            case "softbreak":      parts.add(line_break())
            case "hardbreak":      parts.add(line_break())
            ...
    return parts
```

Concrete code in your front-end framework will look almost identical.

## Widgets on the client

A `widget` node lets your content carry custom components. Branch by
`widget` name and your own client renderer:

```text
function render_widget(node):
    switch node.widget:
        case "tip":         return Callout(level="tip",  title=node.props.title, body=render_each(node.slots.default))
        case "warning":     return Callout(level="warn", title=node.props.title, body=render_each(node.slots.default))
        case "video":       return Video(src=node.props.src, poster=node.props.poster, controls=node.props.controls)
        case "card":        return Card(title=node.props.title, header=render_each(node.slots.header or []), body=render_each(node.slots.default), footer=render_each(node.slots.footer or []))
        case "code-group":  return Tabs(node.slots.default.map(b => (b.filename, render(b))))
        default:
            // Unknown widget — fail open: render the default slot if any, or skip.
            return render_each(node.slots.default or [])
```

## Generating a client schema

If your client language has a strong type system, generate the type
definitions from `json_schema()`:

```python
import json
from markast import json_schema

with open("ast.schema.json", "w") as f:
    json.dump(json_schema(), f, indent=2)
```

Feed that schema into:

* `quicktype` — Dart, TypeScript, Go, Swift, C#, Kotlin, Rust, …
* `datamodel-code-generator` — Pydantic / TypedDict
* `json-schema-to-typescript` — TS interfaces

…and you get a typed model on the client side automatically.

## Warnings: where to surface them

`doc.warnings` is the pragma channel between author and content review.
Recommended pattern:

* In **production** responses, drop warnings (clients ignore them anyway).
* In **staging / dev** responses, surface them so authors see what's wrong.
* In a CMS authoring UI, render warnings inline next to the offending source.

```python
warnings = doc.warnings if request.app.debug else []
return {"ast": doc.to_dict(), "warnings": warnings}
```

## What the AST guarantees

These invariants are stable and clients can rely on them:

| Invariant                                                              | Why it matters |
|------------------------------------------------------------------------|----------------|
| Every node has a `type` string                                         | Lets the client switch on it |
| `heading.children` never contain images or block-level nodes           | Headings render inline-only |
| `table_cell.children` never contain block-level nodes                  | Cells render inline-only |
| `widget.props` is a dict; `widget.slots` is a dict with `"default"` key| Always safe to destructure |
| `document.warnings` is always an array (may be empty)                  | Never `null` |
| `document.version` is a string                                         | Use for forward-compat checks |

## A FastAPI cache hint

If your content rarely changes, parsing on every request is wasteful. Cache
the JSON output keyed on the source's hash:

```python
import hashlib
from functools import lru_cache

@lru_cache(maxsize=1024)
def parse_cached(text_hash: str, text: str):
    return parser.parse(text).to_dict()


@app.get("/content/{slug}")
def get_content(slug: str):
    md = load_from_db(slug)
    h = hashlib.sha256(md.encode("utf-8")).hexdigest()
    return parse_cached(h, md)
```

Or push it further upstream — `Cache-Control` headers + a CDN do the same
job and need no app code.
