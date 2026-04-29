"""
:class:`MarkdownRenderer` — AST → Markdown text.

Designed so that ``MarkdownRenderer().render(parse(text))`` yields a string
equivalent to ``text``, modulo:

* Excess blank lines collapsed to a single blank line.
* Setext headings normalised to ATX.
* Loose list marker positions normalised.
* List indent normalised to 2 spaces.

Subclassing
-----------
Each block / inline node has its own ``_block_*`` / ``_inline_*`` method.
Override only what you need::

    class MyMarkdownRenderer(MarkdownRenderer):
        def _block_divider(self, node):
            return "***"   # use asterisks instead of dashes
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional

from ..ast import types as T
from ..widgets.registry import WidgetRegistry, default_registry


class MarkdownRenderer:
    """Stateful renderer. One instance per render call (state is just the
    registry, which is fine to reuse if you want).
    """

    def __init__(self, registry: Optional[WidgetRegistry] = None) -> None:
        self.registry = registry or default_registry

    # ── Public API ───────────────────────────────────────────────────────────
    def render(self, ast: Dict[str, Any]) -> str:
        if ast.get("type") != T.DOCUMENT:
            # Allow rendering subtrees too — useful for previews and tests.
            return self._render_block(ast) or ""
        return self._render_block_children(ast.get("children", []))

    # ── Block dispatch ───────────────────────────────────────────────────────
    def _render_block_children(self, children: List[Dict[str, Any]]) -> str:
        parts: List[str] = []
        for child in children:
            rendered = self._render_block(child)
            if rendered is not None and rendered != "":
                parts.append(rendered)
        return "\n\n".join(parts)

    def _render_block(self, node: Dict[str, Any]) -> Optional[str]:
        method = getattr(self, f"_block_{node.get('type')}", None)
        if method is None:
            return None
        return method(node)

    # ── Block renderers ──────────────────────────────────────────────────────
    def _block_heading(self, node: Dict[str, Any]) -> str:
        level = max(1, min(6, node.get("level", 1)))
        return f"{'#' * level} {self._inline(node.get('children', []))}"

    def _block_paragraph(self, node: Dict[str, Any]) -> str:
        return self._inline(node.get("children", []))

    def _block_blockquote(self, node: Dict[str, Any]) -> str:
        inner = self._render_block_children(node.get("children", []))
        return "\n".join(f"> {line}" if line else ">" for line in inner.split("\n"))

    def _block_code_block(self, node: Dict[str, Any]) -> str:
        info = node.get("language", "") or ""
        if node.get("filename"):
            info += f" [{node['filename']}]"
        if node.get("highlight_lines"):
            info += f"{{{_format_highlight(node['highlight_lines'])}}}"
        return f"```{info}\n{node.get('value', '')}\n```"

    def _block_image(self, node: Dict[str, Any]) -> str:
        return _image_md(node.get("src", ""), node.get("alt", ""), node.get("title"))

    def _block_video(self, node: Dict[str, Any]) -> str:
        # Synthetic block-video nodes (rare). Use the video widget's syntax.
        cls = self.registry.get("video")
        if cls is None:
            return ""
        return cls().to_markdown(
            {"type": T.WIDGET, "widget": "video",
             "props": {k: v for k, v in node.items() if k != "type"},
             "slots": {"default": []}},
            self._render_block_children,
        )

    def _block_list(self, node: Dict[str, Any]) -> str:
        ordered = node.get("ordered", False)
        start = node.get("start", 1) or 1
        lines: List[str] = []
        for idx, item in enumerate(node.get("children", [])):
            prefix = f"{start + idx}." if ordered else "-"
            checked = item.get("checked")
            if checked is True:
                prefix += " [x]"
            elif checked is False:
                prefix += " [ ]"
            content = self._list_item_content(item.get("children", []))
            content_lines = content.split("\n")
            lines.append(f"{prefix} {content_lines[0]}")
            for line in content_lines[1:]:
                lines.append(f"  {line}")
        return "\n".join(lines)

    def _list_item_content(self, children: List[Dict[str, Any]]) -> str:
        parts: List[str] = []
        for child in children:
            t = child.get("type")
            if t in T.INLINE_TYPES:
                parts.append(self._inline_node(child))
            elif t == T.PARAGRAPH:
                parts.append(self._inline(child.get("children", [])))
            elif t == T.LIST:
                parts.append("\n" + self._block_list(child))
            else:
                rendered = self._render_block(child)
                if rendered:
                    parts.append("\n\n" + rendered)
        return "".join(parts)

    def _block_table(self, node: Dict[str, Any]) -> str:
        head = node.get("head", {}) or {}
        body = node.get("body", {}) or {}
        lines: List[str] = []

        head_rows = head.get("rows", []) or []
        if head_rows:
            cells = head_rows[0].get("cells", [])
            lines.append("| " + " | ".join(self._inline(c.get("children", [])) for c in cells) + " |")
            lines.append("| " + " | ".join(_align_sep(c.get("align")) for c in cells) + " |")

        for row in body.get("rows", []) or []:
            cells = row.get("cells", [])
            lines.append("| " + " | ".join(self._inline(c.get("children", [])) for c in cells) + " |")

        return "\n".join(lines)

    def _block_divider(self, node: Dict[str, Any]) -> str:
        return "---"

    def _block_html_block(self, node: Dict[str, Any]) -> str:
        return node.get("value", "").rstrip("\n")

    def _block_widget(self, node: Dict[str, Any]) -> str:
        widget_name = node.get("widget", "")
        cls = self.registry.get(widget_name)
        if cls is not None:
            return cls().to_markdown(node, self._render_block_children)
        return self._block_widget_generic(node)

    def _block_widget_generic(self, node: Dict[str, Any]) -> str:
        widget_name = node.get("widget", "unknown")
        props = node.get("props", {}) or {}
        prop_str = " ".join(
            f'{k}="{v}"' if (isinstance(v, str) and " " in v) else f"{k}={v}"
            for k, v in props.items()
        )
        header = f":::{widget_name}"
        if prop_str:
            header += f" {prop_str}"
        parts: List[str] = [header, ""]
        for slot_name, slot_children in (node.get("slots") or {}).items():
            if slot_name != "default":
                parts += [f"# {slot_name}", ""]
            rendered = self._render_block_children(slot_children or [])
            if rendered:
                parts += [rendered, ""]
        parts.append(":::")
        return "\n".join(parts)

    def _block_footnote_def(self, node: Dict[str, Any]) -> str:
        body = self._render_block_children(node.get("children", []))
        # Indent continuation lines to keep them part of the definition.
        body_lines = body.split("\n")
        if not body_lines:
            return f"[^{node.get('label', '')}]:"
        first, rest = body_lines[0], body_lines[1:]
        out = [f"[^{node.get('label', '')}]: {first}"]
        out.extend(f"    {line}" if line else "" for line in rest)
        return "\n".join(out)

    # ── Inline ───────────────────────────────────────────────────────────────
    def _inline(self, children: List[Dict[str, Any]]) -> str:
        return "".join(self._inline_node(c) for c in children)

    def _inline_node(self, node: Dict[str, Any]) -> str:
        method = getattr(self, f"_inline_{node.get('type')}", None)
        if method is None:
            return ""
        return method(node)

    def _inline_text(self, node):           return node.get("value", "")
    def _inline_bold(self, node):           return f"**{self._inline(node.get('children', []))}**"
    def _inline_italic(self, node):         return f"*{self._inline(node.get('children', []))}*"
    def _inline_bold_italic(self, node):    return f"***{self._inline(node.get('children', []))}***"
    def _inline_code_inline(self, node):    return f"`{node.get('value', '')}`"
    def _inline_strikethrough(self, node):  return f"~~{self._inline(node.get('children', []))}~~"
    def _inline_underline(self, node):      return f"__{self._inline(node.get('children', []))}__"
    def _inline_softbreak(self, _):         return "\n"
    def _inline_hardbreak(self, _):         return "  \n"

    def _inline_link(self, node):
        href = node.get("href", "")
        title = node.get("title")
        text = self._inline(node.get("children", []))
        if title:
            return f'[{text}]({href} "{title}")'
        return f"[{text}]({href})"

    def _inline_inline_image(self, node):
        return _image_md(node.get("src", ""), node.get("alt", ""), node.get("title"))

    def _inline_image(self, node):  # alias for blocks rendered inline
        return _image_md(node.get("src", ""), node.get("alt", ""), node.get("title"))

    def _inline_footnote_ref(self, node):
        return f"[^{node.get('label', '')}]"


# ─── Helpers ─────────────────────────────────────────────────────────────────
def _image_md(src: str, alt: str, title: Optional[str]) -> str:
    if title:
        return f'![{alt}]({src} "{title}")'
    return f"![{alt}]({src})"


def _align_sep(align: Optional[str]) -> str:
    return {"left": ":---", "center": ":---:", "right": "---:"}.get(align or "", "---")


def _format_highlight(lines: List[int]) -> str:
    if not lines:
        return ""
    srt = sorted(set(lines))
    out: List[str] = []
    s = e = srt[0]
    for x in srt[1:]:
        if x == e + 1:
            e = x
        else:
            out.append(f"{s}-{e}" if s != e else str(s))
            s = e = x
    out.append(f"{s}-{e}" if s != e else str(s))
    return ",".join(out)
