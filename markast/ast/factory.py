"""
Factory functions that build well-formed AST nodes.

Every node in markast is a plain :class:`dict`. These helpers exist because:

* They give a single source of truth for the *exact* fields a node carries.
* They make construction explicit and self-documenting (``heading(2, [...])``
  reads obviously; the equivalent dict literal does not).
* They omit ``None`` / falsy fields where appropriate, keeping the JSON output
  compact for transport.

Use them from custom widgets, transforms, or any code that needs to produce a
node — *not* the parser itself, which calls them directly.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from . import types as T

# Internal version of the produced AST. Bump only on breaking shape changes.
AST_VERSION = "1.0"


# ─── Document / root ─────────────────────────────────────────────────────────
def document(
    children: List[Dict[str, Any]],
    warnings: Optional[List[Dict[str, Any]]] = None,
    *,
    meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build the root document node.

    ``meta`` is an open-ended dict for extra info (TOC, slug map, parser
    config, anything a transform wants to attach). Clients may ignore it.
    """
    node: Dict[str, Any] = {
        "type": T.DOCUMENT,
        "version": AST_VERSION,
        "warnings": warnings or [],
        "children": children,
    }
    if meta:
        node["meta"] = meta
    return node


# ─── Block nodes ─────────────────────────────────────────────────────────────
def heading(level: int, children: List[Dict[str, Any]], *, id: Optional[str] = None) -> Dict[str, Any]:
    """An ATX or setext heading. ``level`` is 1–6."""
    if not 1 <= level <= 6:
        raise ValueError(f"heading level must be 1..6, got {level}")
    node: Dict[str, Any] = {"type": T.HEADING, "level": level, "children": children}
    if id is not None:
        node["id"] = id
    return node


def paragraph(children: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"type": T.PARAGRAPH, "children": children}


def blockquote(children: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"type": T.BLOCKQUOTE, "children": children}


def code_block(
    language: str,
    value: str,
    *,
    filename: Optional[str] = None,
    highlight_lines: Optional[List[int]] = None,
) -> Dict[str, Any]:
    node: Dict[str, Any] = {
        "type": T.CODE_BLOCK,
        "language": language,
        "value": value,
    }
    if filename:
        node["filename"] = filename
    if highlight_lines:
        node["highlight_lines"] = list(highlight_lines)
    return node


def image(src: str, alt: str = "", title: Optional[str] = None) -> Dict[str, Any]:
    return {"type": T.IMAGE, "src": src, "alt": alt, "title": title}


def video(src: str, *, poster: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    """A block-level video node. Most callers go through the ``video`` widget;
    this factory exists for transforms that synthesise videos directly."""
    node: Dict[str, Any] = {"type": T.VIDEO, "src": src}
    if poster is not None:
        node["poster"] = poster
    node.update(extra)
    return node


def list_node(
    ordered: bool,
    children: List[Dict[str, Any]],
    start: Optional[int] = None,
) -> Dict[str, Any]:
    node: Dict[str, Any] = {
        "type": T.LIST,
        "ordered": ordered,
        "children": children,
    }
    if ordered:
        node["start"] = start if start is not None else 1
    return node


def list_item(
    children: List[Dict[str, Any]],
    *,
    checked: Optional[bool] = None,
) -> Dict[str, Any]:
    """``checked`` is ``True``/``False`` for GFM tasklist items, ``None`` for
    plain list items."""
    node: Dict[str, Any] = {"type": T.LIST_ITEM, "children": children}
    if checked is not None:
        node["checked"] = checked
    return node


def table(head: Dict[str, Any], body: Dict[str, Any]) -> Dict[str, Any]:
    return {"type": T.TABLE, "head": head, "body": body}


def table_head(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"type": T.TABLE_HEAD, "rows": rows}


def table_body(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"type": T.TABLE_BODY, "rows": rows}


def table_row(cells: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"type": T.TABLE_ROW, "cells": cells}


def table_cell(
    children: List[Dict[str, Any]],
    align: Optional[str] = None,
    is_header: bool = False,
) -> Dict[str, Any]:
    return {
        "type": T.TABLE_CELL,
        "is_header": is_header,
        "align": align,
        "children": children,
    }


def divider() -> Dict[str, Any]:
    return {"type": T.DIVIDER}


def widget_node(
    name: str,
    props: Dict[str, Any],
    slots: Dict[str, List[Dict[str, Any]]],
) -> Dict[str, Any]:
    """A custom-widget node. Slots is a mapping of slot-name → child list and
    must contain a ``"default"`` key (possibly empty)."""
    if "default" not in slots:
        slots = {"default": [], **slots}
    return {"type": T.WIDGET, "widget": name, "props": props, "slots": slots}


def html_block(value: str) -> Dict[str, Any]:
    return {"type": T.HTML_BLOCK, "value": value}


def footnote_def(label: str, children: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"type": T.FOOTNOTE_DEF, "label": label, "children": children}


# ─── Inline nodes ────────────────────────────────────────────────────────────
def text(value: str) -> Dict[str, Any]:
    return {"type": T.TEXT, "value": value}


def bold(children: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"type": T.BOLD, "children": children}


def italic(children: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"type": T.ITALIC, "children": children}


def bold_italic(children: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"type": T.BOLD_ITALIC, "children": children}


def code_inline(value: str, *, language: Optional[str] = None) -> Dict[str, Any]:
    node: Dict[str, Any] = {"type": T.CODE_INLINE, "value": value}
    if language:
        node["language"] = language
    return node


def link(
    href: str,
    children: List[Dict[str, Any]],
    title: Optional[str] = None,
) -> Dict[str, Any]:
    return {"type": T.LINK, "href": href, "title": title, "children": children}


def strikethrough(children: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"type": T.STRIKETHROUGH, "children": children}


def underline(children: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"type": T.UNDERLINE, "children": children}


def inline_image(src: str, alt: str = "", title: Optional[str] = None) -> Dict[str, Any]:
    return {"type": T.INLINE_IMAGE, "src": src, "alt": alt, "title": title}


def softbreak() -> Dict[str, Any]:
    return {"type": T.SOFTBREAK}


def hardbreak() -> Dict[str, Any]:
    return {"type": T.HARDBREAK}


def footnote_ref(label: str) -> Dict[str, Any]:
    return {"type": T.FOOTNOTE_REF, "label": label}
