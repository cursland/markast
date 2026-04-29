"""
``SmartTypography`` — light-touch typographic substitutions.

* ``"`` → ``“ … ”`` based on word boundaries.
* ``'`` → ``‘ … ’``.
* ``--`` → ``–`` (en dash).
* ``---`` → ``—`` (em dash).
* ``...`` → ``…``.

Only operates on plain ``text`` nodes — code spans, links, and HTML pass
through untouched.
"""
from __future__ import annotations
import re
from typing import Any, Dict, List

from ..ast import factory as F
from ..ast import types as T
from ..config import ParserConfig
from .base import Transform


_RULES = [
    (re.compile(r"---"), "—"),
    (re.compile(r"--"), "–"),
    (re.compile(r"\.\.\."), "…"),
]


def _quotes(s: str) -> str:
    out: List[str] = []
    in_double = False
    in_single = False
    for i, ch in enumerate(s):
        prev = s[i - 1] if i > 0 else " "
        if ch == '"':
            if not in_double and (prev.isspace() or prev in "([{"):
                out.append("“"); in_double = True
            else:
                out.append("”"); in_double = False
        elif ch == "'":
            if not in_single and (prev.isspace() or prev in "([{"):
                out.append("‘"); in_single = True
            else:
                out.append("’"); in_single = False
        else:
            out.append(ch)
    return "".join(out)


class SmartTypography(Transform):
    name = "smarttypography"

    def apply(self, doc: Dict[str, Any], config: ParserConfig) -> Dict[str, Any]:
        _walk(doc)
        return doc


def _walk(node: Dict[str, Any]) -> None:
    if node.get("type") in (T.CODE_INLINE, T.CODE_BLOCK, T.HTML_BLOCK):
        return

    if node.get("type") == T.TEXT:
        v = node.get("value", "")
        for pat, repl in _RULES:
            v = pat.sub(repl, v)
        v = _quotes(v)
        node["value"] = v
        return

    for key in ("children",):
        children = node.get(key)
        if isinstance(children, list):
            for c in children:
                if isinstance(c, dict):
                    _walk(c)

    slots = node.get("slots")
    if isinstance(slots, dict):
        for v in slots.values():
            if isinstance(v, list):
                for c in v:
                    if isinstance(c, dict):
                        _walk(c)

    for k in ("head", "body"):
        sub = node.get(k)
        if isinstance(sub, dict):
            _walk(sub)
    for k in ("rows", "cells"):
        sub = node.get(k)
        if isinstance(sub, list):
            for c in sub:
                if isinstance(c, dict):
                    _walk(c)
