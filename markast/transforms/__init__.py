"""
markast.transforms
────────────────
AST → AST mutations applied *after* parsing and *before* serialisation.

Transforms compose: a parser keeps an ordered list of them and runs them in
sequence. The pipeline operates on the document dict in place when possible
and produces a new tree when not.

Built-in transforms
-------------------

* :class:`NormalizeText` (``"normalize"``)
    Merge adjacent ``text`` nodes, drop empty ones. Cleans up the AST so
    consumers don't have to special-case the corner cases markdown-it
    occasionally emits.
* :class:`SlugifyHeadings` (``"slugify"``)
    Add a stable ``id`` to every heading derived from its plain-text content.
    Required by ``BuildTOC``.
* :class:`BuildTOC` (``"toc"``)
    Walk the document and build a nested table of contents from headings.
    The result is stored in ``document["meta"]["toc"]``.
* :class:`Linkify` (``"linkify"``)
    Detect bare URLs in text nodes and convert them into proper ``link``
    nodes. (CommonMark ``autolinks`` already covers the ``<https://…>`` form;
    this transform handles unwrapped URLs.)
* :class:`SmartTypography` (``"smarttypography"``)
    Replace straight quotes / dashes with their typographic counterparts.

Custom transforms
-----------------
Subclass :class:`Transform` and override :meth:`apply`::

    class StripDividers(Transform):
        name = "strip-dividers"
        def apply(self, doc, config):
            from markast.ast import replace
            return replace(doc, lambda n: None if n.get("type") == "divider" else n)
"""
from .base import Transform, TransformPipeline
from .normalize import NormalizeText
from .slugify import SlugifyHeadings
from .toc import BuildTOC
from .linkify import Linkify
from .typography import SmartTypography

#: Default registry of named transforms. The :class:`Parser` uses this to
#: resolve string identifiers like ``"normalize"`` from its ``transforms``
#: argument.
BUILTIN_TRANSFORMS = {
    "normalize":       NormalizeText,
    "slugify":         SlugifyHeadings,
    "toc":             BuildTOC,
    "linkify":         Linkify,
    "smarttypography": SmartTypography,
}

__all__ = [
    "Transform", "TransformPipeline",
    "NormalizeText", "SlugifyHeadings", "BuildTOC", "Linkify", "SmartTypography",
    "BUILTIN_TRANSFORMS",
]
