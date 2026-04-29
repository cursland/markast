"""
ASTBuilder — turns a flat ``markdown-it-py`` token stream into the AST tree.

The token stream is a sequence of open/inline/close triplets (with some
self-closing tokens like ``hr``, ``fence``, ``image``). The builder walks the
stream sequentially: when it sees an opener, it finds the matching closer by
counting depth and recurses into the slice between them.

Inline tokens live in ``token.children`` already — they don't appear at the
top level. We hand those off to :class:`InlineBuilder` for translation to
inline AST nodes.

Diagnostics
-----------
For each inspectable position the builder calls every registered
:class:`Rule` and appends any returned :class:`Diagnostic` instances to the
document's ``warnings`` list. Diagnostics never alter the parse — they are
purely informational. *Mutation* (e.g. converting an image inside a heading
to plain text) is performed unconditionally in the builder; the rule's job is
only to *observe and report*.
"""
from __future__ import annotations
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from ..ast import factory as F
from ..ast import types as T
from ..ast.utils import extract_text
from ..config import ParserConfig
from ..rules.base import Diagnostic, Rule
from ..rules.codes import W_NESTING_TOO_DEEP, W_DANGLING_FOOTNOTE
from ..widgets.registry import WidgetRegistry
from .inline import InlineBuilder
from .props import parse_fence_info, parse_props


_SLOT_ID_RE = re.compile(r"^[a-z][a-z0-9_-]*$")


class ASTBuilder:
    """Stateful builder. One instance per parse call (don't reuse).

    Parameters
    ----------
    config : ParserConfig
    registry : WidgetRegistry
    rules : list[Rule]
        Rules to consult during the build. Each rule's hooks are called at
        the appropriate points; their diagnostics are merged into the
        document warnings.
    """

    def __init__(
        self,
        config: ParserConfig,
        registry: WidgetRegistry,
        rules: List[Rule],
    ) -> None:
        self._config = config
        self._registry = registry
        self._rules = rules
        self._inline = InlineBuilder()
        self._diagnostics: List[Diagnostic] = []
        self._footnote_defs: Set[str] = set()
        self._footnote_refs: List[Tuple[str, str]] = []  # (label, context)
        self._widget_depth = 0

    # ── Public ───────────────────────────────────────────────────────────────
    def build(self, tokens: list) -> Dict[str, Any]:
        # First pass: harvest footnote definitions so dangling-ref diagnostics
        # are correct regardless of source order.
        self._collect_footnote_defs(tokens)

        children = self._blocks(tokens, 0, len(tokens))

        # Post-pass: emit dangling footnote diagnostics.
        for label, ctx in self._footnote_refs:
            for rule in self._rules:
                diags = rule.check_footnote_ref(label, self._footnote_defs) or []
                self._diagnostics.extend(diags)

        return F.document(
            children,
            [d.to_dict() for d in self._diagnostics],
        )

    # ── Helpers ──────────────────────────────────────────────────────────────
    def _emit(self, diagnostics: Optional[List[Diagnostic]]) -> None:
        if diagnostics:
            self._diagnostics.extend(diagnostics)

    def _emit_one(self, diagnostic: Diagnostic) -> None:
        self._diagnostics.append(diagnostic)

    def _collect_footnote_defs(self, tokens: list) -> None:
        for tok in tokens:
            if tok.type == "footnote_open":
                meta = tok.meta or {}
                label = str(meta.get("label", "")) or str(meta.get("id", ""))
                if label:
                    self._footnote_defs.add(label)

    # ── Block dispatch ───────────────────────────────────────────────────────
    def _blocks(self, toks: list, start: int, end: int) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        i = start
        while i < end:
            tok = toks[i]
            t = tok.type

            if t == "heading_open":
                out.append(self._heading(toks, i)); i += 3

            elif t == "paragraph_open":
                out.append(self._paragraph(toks, i)); i += 3

            elif t == "fence":
                out.append(self._fence(tok)); i += 1

            elif t == "code_block":
                out.append(F.code_block("", tok.content.rstrip("\n"))); i += 1

            elif t == "blockquote_open":
                j = _close(toks, i, "blockquote_open", "blockquote_close", end)
                out.append(F.blockquote(self._blocks(toks, i + 1, j - 1)))
                i = j

            elif t in ("bullet_list_open", "ordered_list_open"):
                ordered = t == "ordered_list_open"
                close_t = t.replace("_open", "_close")
                j = _close(toks, i, t, close_t, end)
                start_n = 1
                if ordered:
                    attrs = dict(tok.attrs or [])
                    try:
                        start_n = int(attrs.get("start", 1))
                    except (TypeError, ValueError):
                        start_n = 1
                items = self._list_items(toks, i + 1, j - 1)
                out.append(F.list_node(ordered, items, start_n))
                i = j

            elif t == "table_open":
                j = _close(toks, i, "table_open", "table_close", end)
                out.append(self._table(toks, i + 1, j - 1))
                i = j

            elif t == "hr":
                out.append(F.divider()); i += 1

            elif t == "html_block":
                if self._config.diagnose_html_blocks:
                    for rule in self._rules:
                        self._emit(rule.check_html_block(tok.content))
                out.append(F.html_block(tok.content))
                i += 1

            elif t == "footnote_block_open":
                j = _close(toks, i, "footnote_block_open", "footnote_block_close", end)
                out.extend(self._footnote_block(toks, i + 1, j - 1))
                i = j

            elif t.startswith("container_") and t.endswith("_open"):
                widget_name = t[len("container_"):-len("_open")]
                close_t = f"container_{widget_name}_close"
                j = _close(toks, i, t, close_t, end)
                out.append(self._widget(widget_name, tok.info or "", toks, i + 1, j - 1))
                i = j

            else:
                i += 1
        return out

    # ── Specific block builders ──────────────────────────────────────────────
    def _heading(self, toks: list, i: int) -> Dict[str, Any]:
        tok = toks[i]
        level = int(tok.tag[1])
        inline_tok = toks[i + 1]
        spans = self._inline.build(inline_tok.children or [])

        # Apply rules — they observe; we mutate.
        for rule in self._rules:
            self._emit(rule.check_heading_children(spans, level))

        cleaned = self._sanitize_heading_children(spans)
        return F.heading(level, cleaned)

    def _sanitize_heading_children(self, spans: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cleaned: List[Dict[str, Any]] = []
        for span in spans:
            t = span.get("type")
            if t == T.INLINE_IMAGE:
                alt = span.get("alt") or ""
                if alt:
                    cleaned.append(F.text(alt))
            elif t in T.HEADING_ALLOWED_INLINE:
                cleaned.append(span)
            else:
                txt = extract_text(span)
                if txt:
                    cleaned.append(F.text(txt))
        return cleaned

    def _paragraph(self, toks: list, i: int) -> Dict[str, Any]:
        inline_tok = toks[i + 1]
        spans = self._inline.build(inline_tok.children or [])

        # Hoist a lone image to a block image.
        non_break = [s for s in spans if s["type"] not in (T.SOFTBREAK, T.HARDBREAK)]
        if len(non_break) == 1 and non_break[0]["type"] == T.INLINE_IMAGE:
            img = non_break[0]
            return F.image(img.get("src", ""), img.get("alt", ""), img.get("title"))

        # Track footnote refs for the dangling-ref check.
        for span in spans:
            if span.get("type") == T.FOOTNOTE_REF:
                self._footnote_refs.append((span.get("label", ""), "paragraph"))

        return F.paragraph(spans)

    def _fence(self, tok) -> Dict[str, Any]:
        info = parse_fence_info(tok.info or "")
        return F.code_block(
            language=str(info["language"] or ""),
            value=tok.content.rstrip("\n"),
            filename=info["filename"],  # type: ignore[arg-type]
            highlight_lines=info["highlight_lines"] or None,  # type: ignore[arg-type]
        )

    def _list_items(self, toks: list, start: int, end: int) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        i = start
        while i < end:
            if toks[i].type == "list_item_open":
                tok = toks[i]
                j = _close(toks, i, "list_item_open", "list_item_close", end)

                attrs = dict(tok.attrs or [])
                is_tasklist = (
                    "class" in attrs and "task-list-item" in str(attrs["class"])
                )

                content = self._list_item_content(toks, i + 1, j - 1)
                checked: Optional[bool] = None
                if is_tasklist:
                    checked, content = _strip_tasklist_marker(content)

                out.append(F.list_item(content, checked=checked))
                i = j
            else:
                i += 1
        return out

    @staticmethod
    def _detect_tasklist_marker(text: str):  # legacy alias retained for tests
        return _strip_tasklist_marker_text(text)

    def _list_item_content(self, toks: list, start: int, end: int) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        i = start
        while i < end:
            t = toks[i].type
            if t == "paragraph_open":
                inline_tok = toks[i + 1]
                spans = self._inline.build(inline_tok.children or [])
                if toks[i].hidden:  # tight list — flatten to inline
                    out.extend(spans)
                else:
                    out.append(F.paragraph(spans))
                i += 3
            elif t in ("bullet_list_open", "ordered_list_open"):
                ordered = t == "ordered_list_open"
                close_t = t.replace("_open", "_close")
                j = _close(toks, i, t, close_t, end)
                items = self._list_items(toks, i + 1, j - 1)
                out.append(F.list_node(ordered, items))
                i = j
            elif t == "fence":
                out.append(self._fence(toks[i])); i += 1
            elif t == "blockquote_open":
                j = _close(toks, i, "blockquote_open", "blockquote_close", end)
                out.append(F.blockquote(self._blocks(toks, i + 1, j - 1)))
                i = j
            else:
                i += 1
        return out

    def _table(self, toks: list, start: int, end: int) -> Dict[str, Any]:
        head_rows: List[Dict[str, Any]] = []
        body_rows: List[Dict[str, Any]] = []
        in_head = False
        in_body = False
        cells: List[Dict[str, Any]] = []

        i = start
        while i < end:
            t = toks[i].type
            if t == "thead_open":
                in_head = True; i += 1
            elif t == "thead_close":
                in_head = False; i += 1
            elif t == "tbody_open":
                in_body = True; i += 1
            elif t == "tbody_close":
                in_body = False; i += 1
            elif t == "tr_open":
                cells = []; i += 1
            elif t == "tr_close":
                row = F.table_row(cells)
                (head_rows if in_head else body_rows).append(row)
                i += 1
            elif t in ("th_open", "td_open"):
                is_header = t == "th_open"
                attrs = dict(toks[i].attrs or [])
                style = attrs.get("style", "")
                align = (
                    str(style).replace("text-align:", "").strip() or None
                )
                inline_tok = toks[i + 1]
                spans = self._inline.build(inline_tok.children or [])

                for rule in self._rules:
                    self._emit(rule.check_table_cell_children(spans, is_header))

                cleaned = self._sanitize_cell_children(spans)
                cells.append(F.table_cell(cleaned, align, is_header))
                i += 3
            else:
                i += 1

        return F.table(F.table_head(head_rows), F.table_body(body_rows))

    def _sanitize_cell_children(self, spans: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cleaned: List[Dict[str, Any]] = []
        for span in spans:
            t = span.get("type")
            if t == T.INLINE_IMAGE:
                alt = span.get("alt") or ""
                if alt:
                    cleaned.append(F.text(alt))
            elif t in T.TABLE_CELL_ALLOWED_INLINE:
                cleaned.append(span)
            else:
                txt = extract_text(span)
                if txt:
                    cleaned.append(F.text(txt))
        return cleaned

    # ── Widget container ─────────────────────────────────────────────────────
    def _widget(
        self,
        widget_name: str,
        info: str,
        toks: list,
        start: int,
        end: int,
    ) -> Dict[str, Any]:
        # Depth check.
        self._widget_depth += 1
        try:
            if (self._config.max_widget_depth and
                    self._widget_depth > self._config.max_widget_depth):
                self._emit_one(Diagnostic(
                    code=W_NESTING_TOO_DEEP,
                    message=(f"Widget '{widget_name}' nested deeper than "
                             f"max_widget_depth={self._config.max_widget_depth}."),
                    context=f"widget={widget_name}",
                ))

            raw_props = parse_props(info, widget_name)
            widget_cls = self._registry.get(widget_name)

            if widget_cls is None:
                validated = raw_props
                widget_diagnostics: List[Diagnostic] = []
            else:
                instance = widget_cls()
                validated, widget_diagnostics = instance.validate_props(raw_props)
                widget_diagnostics.extend(instance.validate(validated, {}))

            self._diagnostics.extend(widget_diagnostics)

            slots = self._split_slots(toks, start, end)

            # Notify rules.
            for rule in self._rules:
                self._emit(rule.check_widget(widget_name, validated, slots, widget_cls is not None))

            return F.widget_node(widget_name, validated, slots)
        finally:
            self._widget_depth -= 1

    def _split_slots(
        self,
        toks: list,
        start: int,
        end: int,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Split widget body tokens into named slots using bare h1 dividers."""
        if start >= end:
            return {"default": []}

        expected_level = toks[start].level

        slots: Dict[str, List[Dict[str, Any]]] = {"default": []}
        current_slot = "default"
        current_toks: List = []

        i = start
        while i < end:
            tok = toks[i]
            if (
                tok.type == "heading_open"
                and tok.tag == "h1"
                and tok.level == expected_level
                and i + 1 < end
            ):
                next_tok = toks[i + 1]
                if next_tok.type == "inline":
                    slot_text = next_tok.content.strip()
                    if _SLOT_ID_RE.match(slot_text):
                        slots[current_slot] = self._blocks(current_toks, 0, len(current_toks))
                        current_slot = slot_text
                        current_toks = []
                        i += 3
                        continue
            current_toks.append(tok)
            i += 1

        slots[current_slot] = self._blocks(current_toks, 0, len(current_toks))
        return slots

    # ── Footnote definitions block ───────────────────────────────────────────
    def _footnote_block(self, toks: list, start: int, end: int) -> List[Dict[str, Any]]:
        """Convert footnote definitions to AST footnote_def nodes."""
        out: List[Dict[str, Any]] = []
        i = start
        while i < end:
            tok = toks[i]
            if tok.type == "footnote_open":
                meta = tok.meta or {}
                label = str(meta.get("label", "")) or str(meta.get("id", ""))
                j = _close(toks, i, "footnote_open", "footnote_close", end)
                children = self._blocks(toks, i + 1, j - 1)
                if label:
                    self._footnote_defs.add(label)
                out.append(F.footnote_def(label, children))
                i = j
            else:
                i += 1
        return out


# ─── Module-level helpers ────────────────────────────────────────────────────
def _strip_tasklist_marker(content: List[Dict[str, Any]]):
    """Find and remove a tasklists-plugin checkbox marker from a list item.

    The plugin inserts an ``html_inline`` token whose content is an
    ``<input ...>`` tag containing ``checked="checked"`` for ticked boxes.
    Because markast turns ``html_inline`` into a plain text node during the
    inline build, the marker shows up here as a ``text`` node carrying that
    HTML literal. We detect it, strip it, and return the checked state.
    """
    if not content:
        return None, content

    # The marker can live either directly in inline children (tight list) or
    # inside the first paragraph's children (loose list).
    target = content
    paragraph: Optional[Dict[str, Any]] = None
    if content[0].get("type") == "paragraph":
        paragraph = content[0]
        target = paragraph.get("children", [])

    if not target or target[0].get("type") != "text":
        return None, content
    text = target[0].get("value", "")
    checked = _strip_tasklist_marker_text(text)
    if checked is None:
        return None, content

    cleaned_text = _strip_tasklist_html(text)
    if cleaned_text:
        target[0] = F.text(cleaned_text)
    else:
        target.pop(0)

    if paragraph is not None:
        paragraph["children"] = target
    else:
        content = target
    return checked, content


def _strip_tasklist_marker_text(text: str) -> Optional[bool]:
    """Return ``True``/``False`` if ``text`` starts with a tasklists checkbox
    marker, or ``None`` if no marker is present."""
    if "task-list-item-checkbox" not in text:
        return None
    end = text.find(">")
    if end == -1:
        return None
    head = text[: end + 1]
    return "checked=" in head


def _strip_tasklist_html(text: str) -> str:
    """Remove the leading ``<input class="task-list-item-checkbox" ...>`` from
    ``text`` and any single leading whitespace that immediately follows."""
    marker_end = text.find(">")
    if marker_end == -1:
        return text
    rest = text[marker_end + 1:]
    if rest.startswith(" "):
        rest = rest[1:]
    return rest


def _close(toks: list, open_i: int, open_t: str, close_t: str, end: int) -> int:
    """Return index *after* the matching close token."""
    depth = 1
    j = open_i + 1
    while j < end and depth > 0:
        if toks[j].type == open_t:
            depth += 1
        elif toks[j].type == close_t:
            depth -= 1
        j += 1
    return j
