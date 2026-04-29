"""
``SlugifyHeadings`` — give every heading a stable, kebab-case ``id``.

The slug is derived from the heading's plain-text content. Duplicate slugs
within a single document are disambiguated with a numeric suffix
(``-2``, ``-3``…).

Why is this useful?
-------------------
Many clients want anchor links inside long documents. Instead of forcing
every consumer to derive ids the same way, we compute them once during the
parse pipeline and write them into the AST.
"""
from __future__ import annotations
import re
import unicodedata
from typing import Any, Dict, Set

from ..ast import types as T
from ..ast.utils import extract_text
from ..ast.walker import walk
from ..config import ParserConfig
from .base import Transform


_SLUG_DROP_RE = re.compile(r"[^\w\s-]", flags=re.UNICODE)
_SLUG_SPACES_RE = re.compile(r"[\s_]+")


class SlugifyHeadings(Transform):
    name = "slugify"

    def apply(self, doc: Dict[str, Any], config: ParserConfig) -> Dict[str, Any]:
        seen: Set[str] = set()
        for node in walk(doc):
            if node.get("type") != T.HEADING:
                continue
            base = self.slugify(extract_text(node))
            slug = base or "section"
            i = 2
            while slug in seen:
                slug = f"{base}-{i}"
                i += 1
            seen.add(slug)
            node["id"] = slug
        return doc

    @staticmethod
    def slugify(text: str) -> str:
        """Convert arbitrary text into a kebab-case slug.

        Steps:
        1. Lowercase.
        2. NFKD-normalise and drop combining marks (so accents disappear).
        3. Drop punctuation other than spaces/underscores/hyphens.
        4. Collapse runs of whitespace/underscores to a single hyphen.
        5. Strip leading/trailing hyphens.
        """
        s = text.strip().lower()
        s = unicodedata.normalize("NFKD", s)
        s = "".join(c for c in s if not unicodedata.combining(c))
        s = _SLUG_DROP_RE.sub("", s)
        s = _SLUG_SPACES_RE.sub("-", s).strip("-")
        return s
