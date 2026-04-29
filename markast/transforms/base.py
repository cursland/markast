"""
:class:`Transform` — base class for AST→AST transformations.

A transform mutates a document. Whether it does so in place or by replacing
nodes is up to the implementation. The contract:

1. :meth:`apply` receives the document root and the parser config.
2. It returns the (possibly new) document root.
3. It may add entries to ``document["meta"]`` for downstream code (e.g. TOC).
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

from ..config import ParserConfig


class Transform:
    """Base transform. Override :meth:`apply`."""

    #: Stable identifier — used when looking up the transform from a string.
    name: str = ""

    def apply(self, doc: Dict[str, Any], config: ParserConfig) -> Dict[str, Any]:
        return doc


class TransformPipeline:
    """An ordered chain of :class:`Transform` instances."""

    def __init__(self, transforms: Optional[List[Transform]] = None) -> None:
        self._transforms: List[Transform] = list(transforms or [])

    def append(self, transform: Transform) -> None:
        self._transforms.append(transform)

    def extend(self, transforms: List[Transform]) -> None:
        self._transforms.extend(transforms)

    def run(self, doc: Dict[str, Any], config: ParserConfig) -> Dict[str, Any]:
        result = doc
        for t in self._transforms:
            result = t.apply(result, config)
        return result

    def names(self) -> List[str]:
        return [t.name or t.__class__.__name__ for t in self._transforms]

    def __len__(self) -> int:
        return len(self._transforms)
