"""
markast.render
────────────
Serialise an AST back into text.

Two renderers ship in the box:

* :class:`MarkdownRenderer` — produces canonical Markdown. The roundtrip
  ``parse → MarkdownRenderer().render`` reproduces the source for every
  Markdown construct markast supports, modulo whitespace normalisation.
* :class:`HTMLRenderer` — produces server-side HTML. Uses each widget's
  :meth:`BaseWidget.to_html` for custom containers.

Both renderers are extensible: subclass and override the relevant
``render_<node_type>`` method.
"""
from .markdown import MarkdownRenderer
from .html import HTMLRenderer

__all__ = ["MarkdownRenderer", "HTMLRenderer"]
