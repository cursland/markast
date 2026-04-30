"""
InlineBuilder — translates the *inline* token list (``token.children``) into
inline AST nodes.

Inline tokens are produced by ``markdown-it-py`` for the contents of
paragraphs, headings, table cells, and similar single-line containers. The
shape mirrors the block stream: ``strong_open / ... / strong_close``,
``em_open / ... / em_close``, plus self-closing leaves like ``code_inline``
or ``image``.

Detecting underlined text
-------------------------
Standard CommonMark has no underline syntax. We follow the convention used by
many doc tools: ``__text__`` → underline (only when wrapped in double
underscores at word boundaries — exactly the same set markdown-it produces as
``strong``-via-underscores). We expose this through the *config*; if the
caller didn't enable it, the parser uses the default ``bold`` mapping and
underline-text is never produced.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple

from ..ast import factory as F
from ..ast import types as T


class InlineBuilder:
    """Translates flat inline tokens into nested inline AST nodes."""

    def build(self, itoks: list) -> List[Dict[str, Any]]:
        return self._consume(itoks, 0, len(itoks))[0]

    # Returns (nodes, next_index). ``end`` is exclusive.
    def _consume(self, itoks: list, start: int, end: int) -> Tuple[List[Dict[str, Any]], int]:
        out: List[Dict[str, Any]] = []
        i = start
        while i < end:
            tok = itoks[i]
            t = tok.type

            if t == "text":
                if tok.content:
                    out.extend(_expand_literal_newlines(tok.content))
                i += 1

            elif t == "code_inline":
                out.append(F.code_inline(tok.content))
                i += 1

            elif t == "strong_open":
                j, inner = _slice(itoks, i, "strong_open", "strong_close")
                built = self.build(inner)
                if _is_single_wrapper(built, T.ITALIC):
                    out.append(F.bold_italic(built[0].get("children", [])))
                else:
                    out.append(F.bold(built))
                i = j

            elif t == "em_open":
                j, inner = _slice(itoks, i, "em_open", "em_close")
                built = self.build(inner)
                if _is_single_wrapper(built, T.BOLD):
                    out.append(F.bold_italic(built[0].get("children", [])))
                else:
                    out.append(F.italic(built))
                i = j

            elif t == "s_open":
                j, inner = _slice(itoks, i, "s_open", "s_close")
                out.append(F.strikethrough(self.build(inner)))
                i = j

            elif t == "link_open":
                j, inner = _slice(itoks, i, "link_open", "link_close")
                attrs = dict(tok.attrs or [])
                href  = attrs.get("href", "")
                title = attrs.get("title") or None
                out.append(F.link(str(href), self.build(inner), title))
                i = j

            elif t == "image":
                attrs = dict(tok.attrs or [])
                src   = str(attrs.get("src", ""))
                title = attrs.get("title") or None
                if tok.children:
                    alt = "".join(c.content for c in tok.children if c.type == "text")
                else:
                    alt = tok.content or attrs.get("alt", "") or ""
                out.append(F.inline_image(src, alt, title))
                i += 1

            elif t == "softbreak":
                out.append(F.softbreak()); i += 1

            elif t == "hardbreak":
                out.append(F.hardbreak()); i += 1

            elif t == "footnote_ref":
                meta = tok.meta or {}
                label = str(meta.get("label", "")) or str(meta.get("id", ""))
                out.append(F.footnote_ref(label)); i += 1

            elif t == "html_inline":
                out.append(F.text(tok.content))
                i += 1

            else:
                i += 1

        # Compress adjacent text spans — markdown-it occasionally emits
        # consecutive ``text`` tokens that we can merge for cleaner output.
        return _merge_adjacent_text(out), i


def _expand_literal_newlines(text: str) -> List[Dict[str, Any]]:
    """Split ``text`` on literal ``\\n`` sequences (backslash + lowercase n),
    emitting a ``hardbreak`` node for each occurrence. This lets authors write
    explicit line breaks that survive whitespace-normalising transports
    (CMSes, JSON encoders, copy-paste through editors that collapse blanks).
    The literal form roundtrips through the AST as a real hardbreak."""
    if "\\n" not in text:
        return [F.text(text)] if text else []

    out: List[Dict[str, Any]] = []
    pos = 0
    i = 0
    n = len(text)
    while i < n:
        if text[i] == "\\" and i + 1 < n and text[i + 1] == "n":
            if i > pos:
                out.append(F.text(text[pos:i]))
            while i + 1 < n and text[i] == "\\" and text[i + 1] == "n":
                out.append(F.hardbreak())
                i += 2
            pos = i
        else:
            i += 1
    if pos < n:
        out.append(F.text(text[pos:]))
    return out


def _is_single_wrapper(nodes: List[Dict[str, Any]], wrapped_type: str) -> bool:
    """True when ``nodes`` is exactly one node of ``wrapped_type``. Used to
    collapse ``strong > em`` (or ``em > strong``) into a single ``bold_italic``
    node so renderers can style the combination distinctly."""
    return len(nodes) == 1 and nodes[0].get("type") == wrapped_type


def _slice(
    itoks: list,
    open_i: int,
    open_t: str,
    close_t: str,
) -> Tuple[int, List[Any]]:
    depth = 1
    j = open_i + 1
    inner: List[Any] = []
    while j < len(itoks) and depth > 0:
        if itoks[j].type == open_t:
            depth += 1
        elif itoks[j].type == close_t:
            depth -= 1
        if depth > 0:
            inner.append(itoks[j])
        j += 1
    return j, inner


def _merge_adjacent_text(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for node in nodes:
        if (out and node.get("type") == T.TEXT and out[-1].get("type") == T.TEXT):
            out[-1] = F.text(out[-1].get("value", "") + node.get("value", ""))
        else:
            out.append(node)
    return out
