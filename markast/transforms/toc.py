"""
``BuildTOC`` — produce a nested table-of-contents structure from headings.

The result is attached to ``document["meta"]["toc"]`` as a tree of dicts::

    [
        {"level": 1, "text": "Top", "id": "top", "children": [
            {"level": 2, "text": "Sub", "id": "sub", "children": []}
        ]}
    ]

Requires :class:`SlugifyHeadings` to have run first (otherwise headings have
no ``id``).
"""
from __future__ import annotations
from typing import Any, Dict, List

from ..ast import types as T
from ..ast.utils import extract_text
from ..ast.walker import walk
from ..config import ParserConfig
from .base import Transform


class BuildTOC(Transform):
    name = "toc"

    def apply(self, doc: Dict[str, Any], config: ParserConfig) -> Dict[str, Any]:
        flat: List[Dict[str, Any]] = []
        for n in walk(doc):
            if n.get("type") == T.HEADING:
                flat.append({
                    "level":    n.get("level", 1),
                    "text":     extract_text(n),
                    "id":       n.get("id"),
                    "children": [],
                })

        meta = doc.setdefault("meta", {})
        meta["toc"] = self._nest(flat)
        return doc

    @staticmethod
    def _nest(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert a flat list of heading dicts into a nested tree."""
        root: List[Dict[str, Any]] = []
        # Stack of (level, container_list) pairs.
        stack: List[tuple] = [(0, root)]

        for entry in items:
            level = entry["level"]
            while stack and stack[-1][0] >= level:
                stack.pop()
            if not stack:
                stack.append((0, root))
            stack[-1][1].append(entry)
            stack.append((level, entry["children"]))
        return root
