"""
markast.rules
───────────
Validation diagnostics produced during parsing.

A *rule* never raises — it inspects content and reports a :class:`Diagnostic`
to the parser, which collects them under ``document["warnings"]`` (the name
is historical; some are errors, some are info).

The built-in rules cover the common rendering pitfalls clients encounter when
they map nodes to native UI widgets or HTML:

============= =====================================================
 Code          Trigger
============= =====================================================
W001           Image inside a heading
W002           Block element where inline is required
W003           Unknown widget name
W004           Invalid widget prop value (wrong type / not in choices)
W005           Required widget prop missing
W006           Image inside a table cell
W007           Raw HTML block found (informational)
W008           Footnote reference without matching definition
W009           Nested widget too deep (depth > config limit)
============= =====================================================

Custom rules can be added by subclassing :class:`Rule` and passing the
class to :class:`markast.Parser` in its ``rules=[...]`` argument.
"""
from .base import Diagnostic, Rule, Severity
from .codes import (
    W_IMAGE_IN_HEADING, W_BLOCK_IN_INLINE, W_UNKNOWN_WIDGET, W_INVALID_PROP,
    W_MISSING_PROP, W_IMAGE_IN_TABLE, W_HTML_BLOCK, W_DANGLING_FOOTNOTE,
    W_NESTING_TOO_DEEP,
)

__all__ = [
    "Diagnostic", "Rule", "Severity",
    "W_IMAGE_IN_HEADING", "W_BLOCK_IN_INLINE", "W_UNKNOWN_WIDGET",
    "W_INVALID_PROP", "W_MISSING_PROP", "W_IMAGE_IN_TABLE", "W_HTML_BLOCK",
    "W_DANGLING_FOOTNOTE", "W_NESTING_TOO_DEEP",
]
