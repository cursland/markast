"""
``Linkify`` — turn bare URLs in plain-text spans into ``link`` nodes.

This is opt-in because some content authors prefer literal URLs in code-like
contexts. Enable it explicitly via the parser's ``transforms=["linkify"]``
argument.
"""
from __future__ import annotations
import re
from typing import Any, Dict, List

from ..ast import factory as F
from ..ast import types as T
from ..config import ParserConfig
from .base import Transform


# Conservative URL pattern: scheme://host plus optional path/query/fragment.
_URL_RE = re.compile(
    r"\b(?P<url>https?://[^\s<>'\"\)]+)",
    flags=re.IGNORECASE,
)


class Linkify(Transform):
    name = "linkify"

    def apply(self, doc: Dict[str, Any], config: ParserConfig) -> Dict[str, Any]:
        _walk(doc)
        return doc


def _walk(node: Dict[str, Any]) -> None:
    if node.get("type") == T.LINK:
        return  # already inside a link — leave it alone

    children = node.get("children")
    if isinstance(children, list):
        node["children"] = _linkify_inline(children)
        for c in node["children"]:
            if isinstance(c, dict):
                _walk(c)

    slots = node.get("slots")
    if isinstance(slots, dict):
        for k, v in slots.items():
            if isinstance(v, list):
                slots[k] = _linkify_inline(v)
                for c in slots[k]:
                    if isinstance(c, dict):
                        _walk(c)

    for key in ("head", "body"):
        sub = node.get(key)
        if isinstance(sub, dict):
            _walk(sub)
    for key in ("rows", "cells"):
        sub = node.get(key)
        if isinstance(sub, list):
            for c in sub:
                if isinstance(c, dict):
                    _walk(c)


def _linkify_inline(children: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Walk an inline list and split text nodes that contain URLs."""
    out: List[Dict[str, Any]] = []
    for c in children:
        if not isinstance(c, dict):
            out.append(c)
            continue
        if c.get("type") != T.TEXT:
            out.append(c)
            continue

        text = c.get("value", "")
        if not text:
            out.append(c)
            continue

        last = 0
        any_match = False
        for m in _URL_RE.finditer(text):
            any_match = True
            if m.start() > last:
                out.append(F.text(text[last:m.start()]))
            url = m.group("url")
            out.append(F.link(url, [F.text(url)]))
            last = m.end()
        if any_match:
            if last < len(text):
                out.append(F.text(text[last:]))
        else:
            out.append(c)
    return out
