# 5. Renderers

Two renderers ship in the box: `MarkdownRenderer` and `HTMLRenderer`. Both
are ordinary Python classes you can subclass to override individual node
handlers.

## MarkdownRenderer

Round-trips an AST back into Markdown. Useful for:

* Rendering AST stored in a database back into a textarea / code editor.
* Re-emitting normalised Markdown after running transforms.
* Debugging — `print(doc.to_markdown())` is more readable than the JSON.

```python
from markast import MarkdownRenderer, parse

doc = parse("# Hi\n\nA paragraph.")
print(MarkdownRenderer().render(doc.root))
```

For convenience, `Document.to_markdown()` does the same thing.

### Roundtrip stability

`parse(text).to_markdown()` reproduces the source for every Markdown
construct markast supports, with these normalisations:

* Excess blank lines collapse to a single blank line.
* Setext headings (`====` underline) become ATX (`# title`).
* Loose-list marker positions normalise to a flush-left bullet/number.
* List indentation normalises to 2 spaces per level.

The roundtrip is stable: `parse(parse(text).to_markdown()).to_markdown()`
equals `parse(text).to_markdown()` for every supported construct.

## HTMLRenderer

Produces clean, opinion-free HTML. No CSS classes are emitted by default
beyond the structural ones widgets explicitly add.

```python
from markast import HTMLRenderer, parse

doc = parse("# Hi\n\n:::tip\nA tip\n:::")
print(HTMLRenderer().render(doc.root))
```

Set `wrap_root=True` to wrap the output in an `<article>` element with a
`markast` class:

```python
HTMLRenderer(wrap_root=True).render(doc.root)
# <article class="markast">...</article>
```

### Special characters

Plain `text` nodes are escaped: `<`, `>`, `&` become `&lt;`, `&gt;`,
`&amp;`. Code blocks are escaped the same way. HTML attributes are escaped
including `"` for safe quoting.

`html_block` nodes (raw HTML appearing in source Markdown) are emitted
verbatim — the parser already validated nothing about their content. Treat
this as an opt-in: if your source allows raw HTML, you trust the authors.

## Subclassing

Both renderers dispatch by method name: `_block_<type>` for block nodes,
`_inline_<type>` for inline nodes. Override only what you care about:

```python
from markast import MarkdownRenderer


class FlushDividers(MarkdownRenderer):
    """Use a stronger divider syntax."""

    def _block_divider(self, node):
        return "* * *"


print(FlushDividers().render(doc.root))
```

`HTMLRenderer` follows the same convention. Override e.g. `_block_heading`
to emit anchored headings:

```python
class AnchoredHTMLRenderer(HTMLRenderer):
    def _block_heading(self, node):
        lvl = max(1, min(6, node.get("level", 1)))
        slug = node.get("id", "")
        anchor = f'<a href="#{slug}">#</a>' if slug else ""
        body = self._inline(node.get("children", []))
        return f'<h{lvl} id="{slug}">{body}{anchor}</h{lvl}>'
```

For consistent results, pair this with the `slugify` transform so every
heading carries an `id`.

## Custom renderers

If you want a third format (terminal output? a different document model?),
the easiest path is to extend the same dispatch pattern:

```python
class AnsiRenderer:
    def render(self, doc):
        return "".join(self._block(c) for c in doc.get("children", []))

    def _block(self, node):
        method = getattr(self, f"_block_{node.get('type')}", None)
        return method(node) if method else ""

    def _block_heading(self, node):
        text = "".join(c.get("value", "") for c in node["children"])
        return f"\033[1m{'#' * node['level']} {text}\033[0m\n\n"

    def _block_paragraph(self, node):
        text = "".join(c.get("value", "") for c in node["children"])
        return text + "\n\n"
```

Aim for the same `_block_<type>` / `_inline_<type>` convention so users can
extend your renderer the same way they extend the built-in ones.
