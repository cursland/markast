"""
Small utility functions for working with AST nodes.

Every helper here is intentionally tiny and stateless — they exist only to
spare callers from duplicating the same boilerplate over and over.
"""
from __future__ import annotations
from typing import Any, Dict, List

from . import types as T
from .walker import walk


def extract_text(node: Dict[str, Any]) -> str:
    """Best-effort plain-text projection of a node and its descendants.

    Returns an empty string for nodes that hold no text content (e.g. dividers
    or video widgets).

    The recursion follows ``children``, ``rows``/``cells``, and the named
    slots of widgets, so widgets contribute their slot contents too.
    """
    if "value" in node and not node.get("children"):
        # Pure leaf with a value field (text, code_inline, html_block).
        return str(node.get("value", ""))

    parts: List[str] = []

    if "value" in node:
        parts.append(str(node.get("value", "")))

    for child in node.get("children", []) or []:
        if isinstance(child, dict):
            parts.append(extract_text(child))

    # Tables hold rows/cells under different keys
    for row_container in ("head", "body"):
        cont = node.get(row_container)
        if isinstance(cont, dict):
            for row in cont.get("rows", []) or []:
                for cell in row.get("cells", []) or []:
                    parts.append(extract_text(cell))
                    parts.append(" ")

    # Widget slots
    slots = node.get("slots")
    if isinstance(slots, dict):
        for slot_children in slots.values():
            for child in slot_children or []:
                if isinstance(child, dict):
                    parts.append(extract_text(child))

    return "".join(parts).strip()


def children_of(node: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return the canonical ``children`` list, or ``[]`` if none.

    Doesn't dig into widget slots. For that, use :func:`slots_of`.
    """
    children = node.get("children")
    return children if isinstance(children, list) else []


def slots_of(widget: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """Return the slots dict of a widget node (always at least ``default``)."""
    slots = widget.get("slots") if isinstance(widget, dict) else None
    if not isinstance(slots, dict):
        return {"default": []}
    return slots


def has_warnings(doc: Dict[str, Any], code: str = "") -> bool:
    """Did the document collect any warnings (optionally of a specific code)?"""
    warnings = doc.get("warnings", [])
    if not warnings:
        return False
    if not code:
        return True
    return any(w.get("code") == code for w in warnings)


def count_nodes(root: Dict[str, Any]) -> Dict[str, int]:
    """Tally how many of each node type appear under ``root``.

    Useful for tests and content-analytics scripts.
    """
    counts: Dict[str, int] = {}
    for n in walk(root):
        t = n.get("type") or "<unknown>"
        counts[t] = counts.get(t, 0) + 1
    return counts


def is_block(node: Dict[str, Any]) -> bool:
    return node.get("type") in T.BLOCK_TYPES


def is_inline(node: Dict[str, Any]) -> bool:
    return node.get("type") in T.INLINE_TYPES
