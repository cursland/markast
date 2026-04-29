"""
markast
─────
Markdown → typed AST → JSON / Markdown / HTML, with a pluggable widget system.

Quick start
~~~~~~~~~~~
::

    from markast import parse

    doc = parse("# Hello\\n\\nA paragraph with **bold**.")
    doc.to_json()       # str
    doc.to_markdown()   # str  (roundtrip)
    doc.to_html()       # str

For configuration beyond the defaults, construct an explicit parser::

    from markast import Parser
    from markast.widgets import BaseWidget, WidgetParam

    class FooWidget(BaseWidget):
        name = "foo"
        params = {"label": WidgetParam(str, required=True)}

    parser = Parser(widgets=[FooWidget], transforms=["normalize", "slugify"])
    doc = parser.parse(text)

Module map
~~~~~~~~~~
* :mod:`markast.ast`         — node types, factories, walker, schema export
* :mod:`markast.parser`      — tokenizer + builder (low-level)
* :mod:`markast.render`      — Markdown / HTML renderers
* :mod:`markast.widgets`     — :class:`BaseWidget`, :class:`WidgetParam`,
                             :class:`WidgetRegistry`, built-in widgets
* :mod:`markast.transforms`  — AST → AST mutators
* :mod:`markast.rules`       — diagnostic rules
* :mod:`markast.config`      — :class:`ParserConfig`
"""
from .__version__ import __version__

from .ast import (
    NodeType,
    walk, find, find_all, replace, Visitor,
    extract_text, count_nodes, json_schema,
)
from .config import ParserConfig, DEFAULT_CONFIG
from .document import Document
from .exceptions import (
    MdastError, ConfigurationError, WidgetRegistrationError, RenderError,
)
from .parser_api import Parser
from .render import MarkdownRenderer, HTMLRenderer
from .rules import Diagnostic, Rule, Severity
from .widgets import BaseWidget, WidgetParam, WidgetRegistry, default_registry

# Populate the default registry with the built-in widgets so the bare
# ``parse()`` shortcut recognises them out of the box.
from .widgets.registry import _populate_default_registry as _populate
_populate()
del _populate


# ─── Top-level convenience helpers ───────────────────────────────────────────
_default_parser: Parser | None = None


def _get_default_parser() -> Parser:
    """Return a process-wide default :class:`Parser` (lazy-initialised).

    The default parser uses :data:`DEFAULT_CONFIG` and
    :data:`default_registry`, with no transforms and the built-in rules.
    """
    global _default_parser
    if _default_parser is None:
        _default_parser = Parser(registry=default_registry)
    return _default_parser


def parse(text: str) -> Document:
    """Parse Markdown text using the default parser.

    Equivalent to::

        Parser().parse(text)

    but reuses a shared parser instance so the underlying tokeniser is
    initialised once. Use :class:`Parser` directly when you need custom
    config, widgets, or transforms.
    """
    return _get_default_parser().parse(text)


def render_markdown(doc: Document | dict) -> str:
    """Render a Document (or raw AST dict) back to Markdown."""
    if isinstance(doc, Document):
        return doc.to_markdown()
    return MarkdownRenderer().render(doc)


def render_html(doc: Document | dict) -> str:
    """Render a Document (or raw AST dict) to HTML."""
    if isinstance(doc, Document):
        return doc.to_html()
    return HTMLRenderer().render(doc)


def from_json(json_str: str) -> Document:
    """Reconstruct a :class:`Document` from a JSON string previously produced
    by :meth:`Document.to_json`."""
    return Document.from_json(json_str)


__all__ = [
    "__version__",
    # high-level API
    "parse", "render_markdown", "render_html", "from_json",
    "Parser", "Document", "ParserConfig", "DEFAULT_CONFIG",
    # AST primitives
    "NodeType", "walk", "find", "find_all", "replace", "Visitor",
    "extract_text", "count_nodes", "json_schema",
    # widgets
    "BaseWidget", "WidgetParam", "WidgetRegistry", "default_registry",
    # rules
    "Diagnostic", "Rule", "Severity",
    # renderers
    "MarkdownRenderer", "HTMLRenderer",
    # exceptions
    "MdastError", "ConfigurationError", "WidgetRegistrationError", "RenderError",
]
