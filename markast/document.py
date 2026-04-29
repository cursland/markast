"""
:class:`Document` — a thin wrapper around the AST root dict that exposes the
common operations as methods.

Why a wrapper instead of bare dicts?
------------------------------------
The AST is *still* a plain dict — :class:`Document` is just a façade. The
underlying data structure is reachable via :attr:`Document.root`, every
method delegates to existing functions, and serialised output is identical.

The wrapper exists so the most common workflows are one-liners::

    doc = parser.parse(text)
    doc.to_json(indent=2)
    doc.to_html()
    doc.find("heading")
    doc.warnings              # list[dict]
    doc.has_errors            # bool

Without it, every caller would write the same boilerplate. With it, you can
still `dict(doc)` your way back to the underlying structure whenever you need
to interoperate.
"""
from __future__ import annotations
import json
from typing import Any, Dict, Iterator, List, Optional, Union

from .ast import find, find_all, walk
from .ast.utils import count_nodes, has_warnings
from .render import HTMLRenderer, MarkdownRenderer
from .widgets.registry import WidgetRegistry, default_registry


class Document:
    """A façade over the AST root dict.

    Construct via :meth:`markast.Parser.parse` or the top-level
    :func:`markast.parse`; you rarely call this constructor directly. If you
    do, ``root`` must be a dict with ``type=="document"``.
    """

    def __init__(
        self,
        root: Dict[str, Any],
        *,
        registry: Optional[WidgetRegistry] = None,
    ) -> None:
        if not isinstance(root, dict) or root.get("type") != "document":
            raise ValueError("Document requires a dict with type='document'")
        self._root = root
        self._registry = registry or default_registry

    # ── Pass-through accessors ───────────────────────────────────────────────
    @property
    def root(self) -> Dict[str, Any]:
        """The underlying AST dict."""
        return self._root

    @property
    def children(self) -> List[Dict[str, Any]]:
        return self._root.get("children", [])

    @property
    def warnings(self) -> List[Dict[str, Any]]:
        return self._root.get("warnings", [])

    @property
    def meta(self) -> Dict[str, Any]:
        return self._root.setdefault("meta", {})

    @property
    def version(self) -> str:
        return self._root.get("version", "")

    @property
    def has_errors(self) -> bool:
        """``True`` if any diagnostic has severity ``error``."""
        return any(w.get("severity") == "error" for w in self.warnings)

    # ── Serialisation ────────────────────────────────────────────────────────
    def to_dict(self) -> Dict[str, Any]:
        """Return the underlying dict (live reference, not a copy)."""
        return self._root

    def to_json(self, *, indent: Optional[int] = 2, **kwargs: Any) -> str:
        """Serialise to JSON.

        Extra ``kwargs`` are forwarded to :func:`json.dumps`. ``ensure_ascii``
        defaults to ``False`` so unicode is preserved on the wire.
        """
        kwargs.setdefault("ensure_ascii", False)
        return json.dumps(self._root, indent=indent, **kwargs)

    def to_markdown(self, *, renderer: Optional[MarkdownRenderer] = None) -> str:
        """Render back to Markdown."""
        return (renderer or MarkdownRenderer(self._registry)).render(self._root)

    def to_html(self, *, renderer: Optional[HTMLRenderer] = None) -> str:
        """Render to HTML."""
        return (renderer or HTMLRenderer(self._registry)).render(self._root)

    # ── Traversal helpers ────────────────────────────────────────────────────
    def walk(self) -> Iterator[Dict[str, Any]]:
        """Yield every node in document order (depth-first, pre-order)."""
        return walk(self._root)

    def find(self, type_: Union[str, List[str]]) -> Optional[Dict[str, Any]]:
        return find(self._root, type_)

    def find_all(self, type_: Union[str, List[str]]) -> List[Dict[str, Any]]:
        return find_all(self._root, type_)

    def count(self) -> Dict[str, int]:
        """Tally how many nodes of each type appear in the document."""
        return count_nodes(self._root)

    def has_warnings(self, code: str = "") -> bool:
        return has_warnings(self._root, code)

    # ── Misc ─────────────────────────────────────────────────────────────────
    @classmethod
    def from_json(
        cls,
        json_str: str,
        *,
        registry: Optional[WidgetRegistry] = None,
    ) -> "Document":
        """Parse a JSON string back into a Document. Useful when receiving
        the AST over a network or from a file."""
        return cls(json.loads(json_str), registry=registry)

    def __repr__(self) -> str:
        return (f"<Document version={self.version!r} "
                f"children={len(self.children)} warnings={len(self.warnings)}>")
