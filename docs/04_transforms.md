# 4. Transforms

Transforms are AST-to-AST mutations that run after parsing and before
serialisation. They're how you bake in cross-cutting behaviour — slug ids,
TOCs, link auto-detection — without polluting the parser or the renderer.

## Built-in transforms

| Identifier        | Class              | What it does |
|-------------------|--------------------|--------------|
| `normalize`       | `NormalizeText`    | Merge adjacent `text` nodes, drop empty ones. |
| `slugify`         | `SlugifyHeadings`  | Add a stable `id` to every heading. |
| `toc`             | `BuildTOC`         | Build a nested table-of-contents in `doc.meta["toc"]`. Requires `slugify`. |
| `linkify`         | `Linkify`          | Convert bare URLs in text to `link` nodes. |
| `smarttypography` | `SmartTypography`  | Replace dashes / quotes / ellipses with typographic equivalents. |

Apply them by name when constructing a parser:

```python
from markast import Parser

parser = Parser(transforms=["normalize", "slugify", "toc"])
doc = parser.parse("# Top\n\n## Sub\n\n# Top2")

print(doc.meta["toc"])
# [
#   {"level": 1, "text": "Top",  "id": "top",  "children": [
#       {"level": 2, "text": "Sub", "id": "sub", "children": []}
#   ]},
#   {"level": 1, "text": "Top2", "id": "top2", "children": []}
# ]
```

## Order matters

Transforms run in the order you list them. `toc` reads ids that `slugify`
sets, so `slugify` must come first. `normalize` is cheap and idempotent —
it's safe to put it first or last.

## Writing a custom transform

Subclass `Transform` and implement `apply`:

```python
from markast.transforms import Transform
from markast.ast import replace
from markast import NodeType


class StripDividers(Transform):
    """Remove every horizontal rule from the document."""

    name = "strip-dividers"

    def apply(self, doc, config):
        return replace(doc, lambda n: None if n.get("type") == NodeType.DIVIDER else n)
```

Plug it in:

```python
parser = Parser(transforms=[StripDividers])
```

Three things to keep in mind:

1. **Receive and return a document.** If you mutate in place, return the
   same dict; if you build a new tree, return that.
2. **Use `markast.ast.walker.replace` for rewrites.** It correctly handles
   every container shape in the AST — `children`, `slots`, `head`/`body`,
   `rows`/`cells`. Hand-rolling recursion gets corner cases wrong.
3. **Use `doc["meta"]` to expose data.** A transform that *computes*
   something (like a TOC) should attach the result to `doc["meta"]` rather
   than rewriting the tree to fit the new data.

## Transforms vs. rules

|              | Transform                                | Rule (`markast.rules`)                    |
|--------------|------------------------------------------|-----------------------------------------|
| When         | After parsing, before rendering          | During parsing                          |
| What         | Mutates / annotates the AST              | Observes and reports diagnostics        |
| Side effect  | Changes the output                       | Adds entries to `doc.warnings`          |
| Use for      | Slugs, TOCs, autolinks, normalisation    | Cross-cutting validation, lints         |

Pick a rule when you want to *flag* something. Pick a transform when you
want to *change* something.
