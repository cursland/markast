"""
``NormalizeText`` — merge adjacent ``text`` nodes and drop empties.

A typical inline run produced by ``markdown-it-py`` can look like::

    [text "Hello "]
    [strong  [text "world"] ]
    [text "."]
    [text ""]
    [text " Done."]

The two trailing text nodes can be merged into one. The empty one can be
dropped. This transform does that recursively.
"""
from __future__ import annotations
from typing import Any, Dict, List

from ..ast import factory as F
from ..ast import types as T
from ..config import ParserConfig
from .base import Transform


class NormalizeText(Transform):
    name = "normalize"

    def apply(self, doc: Dict[str, Any], config: ParserConfig) -> Dict[str, Any]:
        _walk(doc)
        return doc


def _walk(node: Dict[str, Any]) -> None:
    children = node.get("children")
    if isinstance(children, list):
        node["children"] = _normalize_children(children)
        for child in node["children"]:
            if isinstance(child, dict):
                _walk(child)

    slots = node.get("slots")
    if isinstance(slots, dict):
        for key, slot_children in list(slots.items()):
            if isinstance(slot_children, list):
                slots[key] = _normalize_children(slot_children)
                for child in slots[key]:
                    if isinstance(child, dict):
                        _walk(child)

    for k in ("head", "body"):
        sub = node.get(k)
        if isinstance(sub, dict):
            _walk(sub)

    rows = node.get("rows")
    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict):
                _walk(row)

    cells = node.get("cells")
    if isinstance(cells, list):
        for cell in cells:
            if isinstance(cell, dict):
                _walk(cell)


def _normalize_children(children: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for c in children:
        if not isinstance(c, dict):
            out.append(c)
            continue
        if c.get("type") == T.TEXT:
            value = c.get("value", "")
            if value == "":
                continue
            if out and out[-1].get("type") == T.TEXT:
                out[-1] = F.text(out[-1].get("value", "") + value)
                continue
        out.append(c)
    return out
