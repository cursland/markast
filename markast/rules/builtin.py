"""
Built-in validation rules.

The :class:`BuiltinRules` class bundles the classic W001–W009 checks. It is
registered on every :class:`markast.Parser` by default and can be replaced or
augmented.

The implementation is split across multiple short methods rather than one big
``check`` so a downstream user can subclass and selectively replace any one
of them.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from ..ast import types as T
from ..ast.utils import extract_text
from .base import Diagnostic, Rule, Severity
from .codes import (
    W_IMAGE_IN_HEADING, W_BLOCK_IN_INLINE, W_UNKNOWN_WIDGET,
    W_IMAGE_IN_TABLE, W_HTML_BLOCK, W_DANGLING_FOOTNOTE,
)


class BuiltinRules(Rule):
    """The default rules bundle. Every parser starts with a fresh instance."""

    name = "builtin"

    # ── Headings ─────────────────────────────────────────────────────────────
    def check_heading_children(
        self,
        children: List[Dict[str, Any]],
        level: int,
    ) -> Optional[List[Diagnostic]]:
        diagnostics: List[Diagnostic] = []
        for child in children:
            t = child.get("type")
            if t == T.INLINE_IMAGE:
                diagnostics.append(Diagnostic(
                    code=W_IMAGE_IN_HEADING,
                    message=f"Image inside h{level} heading — alt text used as content.",
                    context=f"src={child.get('src', '')!r}, alt={child.get('alt', '')!r}",
                ))
            elif t not in T.HEADING_ALLOWED_INLINE:
                diagnostics.append(Diagnostic(
                    code=W_BLOCK_IN_INLINE,
                    message=f"Node type '{t}' is not valid inside a heading — converted to plain text.",
                    context=f"level={level}",
                ))
        return diagnostics or None

    # ── Table cells ──────────────────────────────────────────────────────────
    def check_table_cell_children(
        self,
        children: List[Dict[str, Any]],
        is_header: bool,
    ) -> Optional[List[Diagnostic]]:
        diagnostics: List[Diagnostic] = []
        for child in children:
            t = child.get("type")
            if t == T.INLINE_IMAGE:
                diagnostics.append(Diagnostic(
                    code=W_IMAGE_IN_TABLE,
                    message="Image inside table cell — alt text used as content.",
                    context=f"src={child.get('src', '')!r}",
                ))
            elif t not in T.TABLE_CELL_ALLOWED_INLINE:
                diagnostics.append(Diagnostic(
                    code=W_BLOCK_IN_INLINE,
                    message=f"Node type '{t}' is not valid inside a table cell — converted to plain text.",
                ))
        return diagnostics or None

    # ── Widgets ──────────────────────────────────────────────────────────────
    def check_widget(
        self,
        widget_name: str,
        props: Dict[str, Any],
        slots: Dict[str, List[Dict[str, Any]]],
        registered: bool,
    ) -> Optional[List[Diagnostic]]:
        if registered:
            return None
        return [Diagnostic(
            code=W_UNKNOWN_WIDGET,
            message=f"Widget '{widget_name}' is not registered — rendered as a generic widget node.",
            context=f"widget={widget_name}",
        )]

    # ── HTML blocks ──────────────────────────────────────────────────────────
    def check_html_block(self, value: str) -> Optional[List[Diagnostic]]:
        snippet = (value[:60].replace("\n", " ") + "...") if len(value) > 60 else value
        return [Diagnostic(
            code=W_HTML_BLOCK,
            message="Raw HTML block found — passed through as html_block node.",
            context=snippet.strip(),
            severity=Severity.INFO,
        )]

    # ── Footnotes ────────────────────────────────────────────────────────────
    def check_footnote_ref(
        self,
        label: str,
        defined_labels: set,
    ) -> Optional[List[Diagnostic]]:
        if label in defined_labels:
            return None
        return [Diagnostic(
            code=W_DANGLING_FOOTNOTE,
            message=f"Footnote reference [^{label}] has no matching definition.",
            context=f"label={label}",
        )]
