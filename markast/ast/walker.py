"""
Tree walker / visitor.

These primitives let callers traverse and mutate the AST without writing
recursion against every container shape (``children``, ``slots``, ``rows``,
``cells``, ``head``, ``body``, …).

Two complementary APIs are provided:

* :func:`walk` — a generator. Yields every node in document order.
* :class:`Visitor` — declarative subclass dispatch. Override
  ``visit_<node_type>`` methods to react to specific kinds.

In addition, :func:`find` / :func:`find_all` are convenience wrappers, and
:func:`replace` rewrites a tree by applying a callable to every node.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, Iterator, List, Optional, Union


# ─── Container shape registry ────────────────────────────────────────────────
# Different node kinds hold their children in different keys. We enumerate the
# attributes that can hold child nodes (or *lists* of child nodes) so the
# walker stays generic.

_LIST_CHILD_KEYS = ("children", "rows", "cells")
_DICT_CHILD_KEYS = ("slots",)        # value is dict[str, list[node]]
_NODE_CHILD_KEYS = ("head", "body")  # value is itself a node


def _iter_immediate_children(node: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
    """Yield every immediate child node held under any container key.

    Order is stable: list keys → dict-of-lists keys → single-node keys.
    """
    for key in _LIST_CHILD_KEYS:
        children = node.get(key)
        if isinstance(children, list):
            for c in children:
                if isinstance(c, dict):
                    yield c

    for key in _DICT_CHILD_KEYS:
        slots = node.get(key)
        if isinstance(slots, dict):
            for slot_children in slots.values():
                if isinstance(slot_children, list):
                    for c in slot_children:
                        if isinstance(c, dict):
                            yield c

    for key in _NODE_CHILD_KEYS:
        child = node.get(key)
        if isinstance(child, dict):
            yield child


# ─── walk() — generator API ──────────────────────────────────────────────────
def walk(node: Dict[str, Any], *, include_root: bool = True) -> Iterator[Dict[str, Any]]:
    """Yield every node in document order (depth-first, pre-order).

    Args:
        node: Any AST node (typically the document root).
        include_root: If ``True`` (default), the starting node is yielded
            first. If ``False``, only descendants are yielded.

    Example::

        from markast import parse, walk

        doc = parse("# Hi\\n\\nA paragraph with **bold**.")
        for n in walk(doc):
            print(n["type"])
    """
    if include_root:
        yield node
    for child in _iter_immediate_children(node):
        yield from walk(child, include_root=True)


# ─── find() / find_all() — convenience helpers ───────────────────────────────
def find(
    node: Dict[str, Any],
    type_: Union[str, List[str]],
) -> Optional[Dict[str, Any]]:
    """Return the first descendant node matching ``type_`` (string or list).
    Returns ``None`` if nothing matches."""
    types = {type_} if isinstance(type_, str) else set(type_)
    for n in walk(node, include_root=False):
        if n.get("type") in types:
            return n
    return None


def find_all(
    node: Dict[str, Any],
    type_: Union[str, List[str]],
) -> List[Dict[str, Any]]:
    """Return every descendant node matching ``type_`` (string or list)."""
    types = {type_} if isinstance(type_, str) else set(type_)
    return [n for n in walk(node, include_root=False) if n.get("type") in types]


# ─── replace() — functional rewrite ──────────────────────────────────────────
def replace(
    node: Dict[str, Any],
    fn: Callable[[Dict[str, Any]], Optional[Dict[str, Any]]],
    *,
    in_place: bool = False,
) -> Dict[str, Any]:
    """Walk the tree and apply ``fn`` to every node, replacing each node with
    whatever ``fn`` returns.

    Args:
        node: The root to traverse.
        fn:   Callable receiving a node, returning a node (or ``None`` to drop
              it from its parent's list).
        in_place: If ``True``, mutate the existing dict instead of producing a
              fresh tree. Useful when you need to keep object identity.

    Notes:
        * Returning a new dict is fine — the walker will continue into the
          *replacement's* children, not the original's. This makes one-pass
          rewrites trivial.
        * Returning ``None`` removes the node from its parent if the parent
          stores it inside a list (children/rows/cells/slots-values). Single-
          node attributes (``head``, ``body``) cannot be removed; ``None``
          there is treated as "leave as-is".

    Returns:
        The (possibly new) root node. If the root itself is replaced, the new
        root is returned.
    """
    new_root = fn(node) if not in_place else fn(node) or node
    if new_root is None:
        # Replacing the root with None makes no sense — keep original.
        new_root = node
    return _rewrite(new_root, fn, in_place=in_place)


def _rewrite(
    node: Dict[str, Any],
    fn: Callable[[Dict[str, Any]], Optional[Dict[str, Any]]],
    *,
    in_place: bool,
) -> Dict[str, Any]:
    target = node if in_place else dict(node)

    for key in _LIST_CHILD_KEYS:
        if isinstance(target.get(key), list):
            target[key] = _rewrite_list(target[key], fn, in_place=in_place)

    for key in _DICT_CHILD_KEYS:
        slots = target.get(key)
        if isinstance(slots, dict):
            new_slots = slots if in_place else {}
            for slot_name, slot_children in slots.items():
                if isinstance(slot_children, list):
                    new_slots[slot_name] = _rewrite_list(slot_children, fn, in_place=in_place)
                else:
                    new_slots[slot_name] = slot_children
            target[key] = new_slots

    for key in _NODE_CHILD_KEYS:
        child = target.get(key)
        if isinstance(child, dict):
            replaced = fn(child)
            if replaced is None:
                replaced = child
            target[key] = _rewrite(replaced, fn, in_place=in_place)

    return target


def _rewrite_list(
    children: List[Dict[str, Any]],
    fn: Callable[[Dict[str, Any]], Optional[Dict[str, Any]]],
    *,
    in_place: bool,
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for child in children:
        if not isinstance(child, dict):
            out.append(child)
            continue
        replaced = fn(child)
        if replaced is None:
            continue  # drop
        out.append(_rewrite(replaced, fn, in_place=in_place))
    return out


# ─── Visitor — class-based dispatch ──────────────────────────────────────────
class Visitor:
    """Subclass and override ``visit_<node_type>`` methods to react to nodes.

    The base :meth:`visit` dispatches based on ``node["type"]``. If no
    specific method exists, :meth:`generic_visit` is called instead. Both
    return a value, which :meth:`run` collects into a list (this is useful
    when extracting data; ignore it when only side effects matter).

    Example::

        class HeadingCollector(Visitor):
            def __init__(self):
                self.headings = []

            def visit_heading(self, node):
                self.headings.append(node)

        v = HeadingCollector()
        v.run(doc)
        print(len(v.headings))
    """

    def visit(self, node: Dict[str, Any]) -> Any:
        method = getattr(self, f"visit_{node.get('type')}", None)
        if method is None:
            return self.generic_visit(node)
        return method(node)

    def generic_visit(self, node: Dict[str, Any]) -> Any:
        """Default handler. Override to act on every unmatched node type.
        Returning :data:`None` is fine; the walker simply continues."""
        return None

    def run(self, root: Dict[str, Any]) -> List[Any]:
        """Visit every node in document order and collect non-None results."""
        out: List[Any] = []
        for n in walk(root):
            result = self.visit(n)
            if result is not None:
                out.append(result)
        return out
