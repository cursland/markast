"""
Node-type constants and structural :class:`TypedDict` definitions.

Why TypedDicts and not dataclasses?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AST is consumed by:

1. The library itself (Python — wants typing).
2. Clients that import the library (Python — also want typing).
3. Clients that consume serialized JSON (any front-end — wants plain JSON).

A :class:`TypedDict` gives static type checkers full information *and*
serialises trivially to JSON without a custom encoder. Because every node is
already a plain ``dict``, there is zero overhead crossing the library boundary
— a client can produce or modify nodes with literal dict syntax if it wants
to, and the type checker still catches mistakes.
"""
from __future__ import annotations
from typing import List, Optional, Set, Dict, Any

try:
    # ``NotRequired`` was added in Python 3.11. We fall back to a no-op alias
    # on 3.9/3.10 so type-checkers on modern Python still see optional fields,
    # while runtime behavior is unaffected.
    from typing import NotRequired, TypedDict
except ImportError:  # pragma: no cover - py<3.11
    from typing import TypedDict
    from typing_extensions import NotRequired  # type: ignore


# ─── Node-type constants ─────────────────────────────────────────────────────
class NodeType:
    """String constants for every node ``type`` discriminator.

    Usage::

        if node["type"] == NodeType.HEADING:
            ...
    """

    # Document & generic
    DOCUMENT = "document"

    # Block
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    BLOCKQUOTE = "blockquote"
    CODE_BLOCK = "code_block"
    IMAGE = "image"
    VIDEO = "video"
    LIST = "list"
    LIST_ITEM = "list_item"
    TABLE = "table"
    TABLE_HEAD = "table_head"
    TABLE_BODY = "table_body"
    TABLE_ROW = "table_row"
    TABLE_CELL = "table_cell"
    DIVIDER = "divider"
    WIDGET = "widget"
    HTML_BLOCK = "html_block"
    FOOTNOTE_DEF = "footnote_def"

    # Inline
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    BOLD_ITALIC = "bold_italic"
    CODE_INLINE = "code_inline"
    LINK = "link"
    STRIKETHROUGH = "strikethrough"
    UNDERLINE = "underline"
    INLINE_IMAGE = "inline_image"
    SOFTBREAK = "softbreak"
    HARDBREAK = "hardbreak"
    FOOTNOTE_REF = "footnote_ref"


# ─── Allowed-children sets ───────────────────────────────────────────────────

#: Inline nodes that the *parser* will produce.
INLINE_TYPES: Set[str] = {
    NodeType.TEXT, NodeType.BOLD, NodeType.ITALIC, NodeType.BOLD_ITALIC,
    NodeType.CODE_INLINE, NodeType.LINK, NodeType.STRIKETHROUGH,
    NodeType.UNDERLINE, NodeType.INLINE_IMAGE, NodeType.SOFTBREAK,
    NodeType.HARDBREAK, NodeType.FOOTNOTE_REF,
}

#: Block-level nodes that the *parser* will produce.
BLOCK_TYPES: Set[str] = {
    NodeType.HEADING, NodeType.PARAGRAPH, NodeType.BLOCKQUOTE,
    NodeType.CODE_BLOCK, NodeType.IMAGE, NodeType.VIDEO, NodeType.LIST,
    NodeType.LIST_ITEM, NodeType.TABLE, NodeType.TABLE_HEAD,
    NodeType.TABLE_BODY, NodeType.TABLE_ROW, NodeType.TABLE_CELL,
    NodeType.DIVIDER, NodeType.WIDGET, NodeType.HTML_BLOCK,
    NodeType.FOOTNOTE_DEF,
}

#: Inline nodes that may appear inside a heading. Block-level and image
#: content is forbidden — see rule W001.
HEADING_ALLOWED_INLINE: Set[str] = {
    NodeType.TEXT, NodeType.BOLD, NodeType.ITALIC, NodeType.BOLD_ITALIC,
    NodeType.CODE_INLINE, NodeType.LINK, NodeType.STRIKETHROUGH,
    NodeType.UNDERLINE,
}

#: Inline nodes valid inside a table cell. Same constraints as headings.
TABLE_CELL_ALLOWED_INLINE: Set[str] = {
    NodeType.TEXT, NodeType.BOLD, NodeType.ITALIC, NodeType.BOLD_ITALIC,
    NodeType.CODE_INLINE, NodeType.LINK, NodeType.STRIKETHROUGH,
    NodeType.UNDERLINE,
}


# ─── TypedDict shapes (for type checkers; runtime is plain dict) ─────────────
# We keep these intentionally permissive: ``children`` is ``List[dict]`` rather
# than a recursive union. Recursive TypedDicts blow up most type checkers and
# the cost of the strictness is rarely worth it for an AST.

class WarningDict(TypedDict):
    code: str
    message: str
    context: str
    severity: NotRequired[str]


class DocumentNode(TypedDict):
    type: str  # "document"
    version: str
    warnings: List[WarningDict]
    children: List[Dict[str, Any]]
    meta: NotRequired[Dict[str, Any]]


class HeadingNode(TypedDict):
    type: str
    level: int
    children: List[Dict[str, Any]]
    id: NotRequired[str]


class WidgetNode(TypedDict):
    type: str  # "widget"
    widget: str
    props: Dict[str, Any]
    slots: Dict[str, List[Dict[str, Any]]]


class CodeBlockNode(TypedDict):
    type: str  # "code_block"
    language: str
    value: str
    filename: NotRequired[Optional[str]]
    highlight_lines: NotRequired[List[int]]


class TextNode(TypedDict):
    type: str  # "text"
    value: str


# ─── Re-exported aliases ─────────────────────────────────────────────────────
# Some callers prefer module-level constants (no class lookup); we expose the
# most-used ones for ergonomics.
DOCUMENT      = NodeType.DOCUMENT
HEADING       = NodeType.HEADING
PARAGRAPH     = NodeType.PARAGRAPH
BLOCKQUOTE    = NodeType.BLOCKQUOTE
CODE_BLOCK    = NodeType.CODE_BLOCK
IMAGE         = NodeType.IMAGE
VIDEO         = NodeType.VIDEO
LIST          = NodeType.LIST
LIST_ITEM     = NodeType.LIST_ITEM
TABLE         = NodeType.TABLE
TABLE_HEAD    = NodeType.TABLE_HEAD
TABLE_BODY    = NodeType.TABLE_BODY
TABLE_ROW     = NodeType.TABLE_ROW
TABLE_CELL    = NodeType.TABLE_CELL
DIVIDER       = NodeType.DIVIDER
WIDGET        = NodeType.WIDGET
HTML_BLOCK    = NodeType.HTML_BLOCK
FOOTNOTE_DEF  = NodeType.FOOTNOTE_DEF
TEXT          = NodeType.TEXT
BOLD          = NodeType.BOLD
ITALIC        = NodeType.ITALIC
BOLD_ITALIC   = NodeType.BOLD_ITALIC
CODE_INLINE   = NodeType.CODE_INLINE
LINK          = NodeType.LINK
STRIKETHROUGH = NodeType.STRIKETHROUGH
UNDERLINE     = NodeType.UNDERLINE
INLINE_IMAGE  = NodeType.INLINE_IMAGE
SOFTBREAK     = NodeType.SOFTBREAK
HARDBREAK     = NodeType.HARDBREAK
FOOTNOTE_REF  = NodeType.FOOTNOTE_REF
