# 2. AST reference

This chapter documents every node type the parser can produce. Use it as a
specification when you write a client renderer.

## Document (root)

```json
{
  "type":     "document",
  "version":  "1.0",
  "warnings": [ {"code": "W001", "message": "...", "context": "..."} ],
  "children": [ ...block nodes... ],
  "meta":     {}
}
```

| Field      | Type   | Notes |
|------------|--------|-------|
| `version`  | string | Bumped on breaking shape changes. Currently `"1.0"`. |
| `warnings` | array  | List of diagnostic dicts. Always present (may be empty). |
| `children` | array  | Block nodes. Always present (may be empty). |
| `meta`     | object | Open-ended bag for transforms (TOC, slug map, etc.). May be absent. |

## Block nodes

### `heading`

```json
{ "type": "heading", "level": 2, "children": [...inline...], "id": "section-id" }
```

* `level` ∈ 1–6.
* `id` is added by the `slugify` transform; absent otherwise.
* Inline children are restricted (rule W001). Images get reduced to alt text.

### `paragraph`

```json
{ "type": "paragraph", "children": [...inline...] }
```

### `blockquote`

```json
{ "type": "blockquote", "children": [...block nodes...] }
```

### `code_block`

```json
{
  "type":            "code_block",
  "language":        "python",
  "value":           "print('hi')",
  "filename":        "main.py",
  "highlight_lines": [1, 3, 4, 5]
}
```

`filename` and `highlight_lines` are omitted when absent.

### `image` (block-level)

```json
{ "type": "image", "src": "https://...", "alt": "description", "title": null }
```

Produced when a Markdown source line contains exactly one image and nothing
else. Mixed lines yield `inline_image` instead.

### `list`

```json
{
  "type":     "list",
  "ordered":  false,
  "start":    1,
  "children": [ ...list_item nodes... ]
}
```

`start` is only present on ordered lists.

### `list_item`

```json
{
  "type":     "list_item",
  "checked":  true,
  "children": [ ...block or inline nodes... ]
}
```

`checked` is `true`/`false` for GFM tasklist items, absent for plain items.
Tight items hold inline children directly; loose items hold block children
(typically a paragraph + nested lists).

### `table`

```json
{
  "type": "table",
  "head": { "type": "table_head", "rows": [ ...table_row... ] },
  "body": { "type": "table_body", "rows": [ ...table_row... ] }
}
```

### `table_row`

```json
{ "type": "table_row", "cells": [ ...table_cell... ] }
```

### `table_cell`

```json
{
  "type":      "table_cell",
  "is_header": true,
  "align":     "center",
  "children":  [ ...inline nodes... ]
}
```

`align` ∈ `"left"` | `"center"` | `"right"` | `null`. Block content inside
cells is forbidden (rule W002).

### `divider`

```json
{ "type": "divider" }
```

### `widget`

```json
{
  "type":   "widget",
  "widget": "tip",
  "props":  { "title": "Pro tip" },
  "slots":  {
    "default": [ ...block nodes... ],
    "footer":  [ ...block nodes... ]
  }
}
```

`slots` always contains a `"default"` key (possibly an empty array). See
[chapter 3](03_widgets.md).

### `html_block`

```json
{ "type": "html_block", "value": "<div>raw html</div>" }
```

The parser does not interpret HTML — it passes blocks through verbatim and
emits a W007 informational diagnostic.

### `footnote_def`

```json
{ "type": "footnote_def", "label": "1", "children": [...block nodes...] }
```

Produced when the `footnotes` feature is enabled (it is, by default).

## Inline nodes

| Type              | Fields |
|-------------------|--------|
| `text`            | `value` (string) |
| `bold`            | `children` |
| `italic`          | `children` |
| `bold_italic`     | `children` |
| `code_inline`     | `value` |
| `strikethrough`   | `children` |
| `underline`       | `children` |
| `link`            | `href`, `title` (or `null`), `children` |
| `inline_image`    | `src`, `alt`, `title` |
| `softbreak`       | — |
| `hardbreak`       | — |
| `footnote_ref`    | `label` |

## Where these guarantees come from

These shapes are produced by the factory functions in
[`markast.ast.factory`](../markast/ast/factory.py). When in doubt, that module
is the source of truth — and a client codegen target if you want to
generate Dart, TypeScript, Go, etc. data classes mechanically.

The `markast.json_schema()` function returns a JSON-Schema describing the
shapes above. Use it to validate AST payloads or to drive client-side type
generation.
