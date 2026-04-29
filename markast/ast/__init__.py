"""
markast.ast
─────────
The AST layer: node types, factories, traversal, schema export.

This subpackage contains *everything* about the shape of the AST and how to
work with it after it has been built. The :mod:`markast.parser` subpackage
*produces* AST trees; this subpackage *describes* and *operates on* them.

Public surface
~~~~~~~~~~~~~~

* :mod:`markast.ast.types`    — node-type constants, allowed-children sets,
                              and :class:`TypedDict` shapes
* :mod:`markast.ast.factory`  — small functions that produce well-formed nodes
* :mod:`markast.ast.walker`   — :func:`walk`, :func:`find`, :func:`find_all`,
                              and the :class:`Visitor` base class
* :mod:`markast.ast.utils`    — :func:`extract_text`, :func:`children_of`, etc.
* :mod:`markast.ast.schema`   — JSON-Schema exporter for use by clients
"""
from .types import (
    NodeType,
    BLOCK_TYPES,
    INLINE_TYPES,
    HEADING_ALLOWED_INLINE,
    TABLE_CELL_ALLOWED_INLINE,
)
from .factory import (
    document, heading, paragraph, blockquote, code_block, image, video,
    list_node, list_item, table, table_head, table_body, table_row, table_cell,
    divider, html_block, widget_node, footnote_ref, footnote_def,
    text, bold, italic, bold_italic, code_inline, link, strikethrough,
    inline_image, softbreak, hardbreak, underline,
)
from .walker import walk, find, find_all, Visitor, replace
from .utils import (
    extract_text, children_of, slots_of, has_warnings, count_nodes,
    is_block, is_inline,
)
from .schema import json_schema

__all__ = [
    # types
    "NodeType",
    "BLOCK_TYPES",
    "INLINE_TYPES",
    "HEADING_ALLOWED_INLINE",
    "TABLE_CELL_ALLOWED_INLINE",
    # factories — block
    "document", "heading", "paragraph", "blockquote", "code_block", "image",
    "video", "list_node", "list_item", "table", "table_head", "table_body",
    "table_row", "table_cell", "divider", "html_block", "widget_node",
    "footnote_ref", "footnote_def",
    # factories — inline
    "text", "bold", "italic", "bold_italic", "code_inline", "link",
    "strikethrough", "inline_image", "softbreak", "hardbreak", "underline",
    # walker
    "walk", "find", "find_all", "Visitor", "replace",
    # utilities
    "extract_text", "children_of", "slots_of", "has_warnings", "count_nodes",
    "is_block", "is_inline",
    # schema
    "json_schema",
]
