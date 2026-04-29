"""
:class:`HTMLRenderer` — AST → HTML text.

This is intentionally conservative HTML. The library avoids opinionated
classes or framework-specific markup so the output is usable as-is *and* easy
to override in subclasses.

Widget output is delegated to each widget's
:meth:`BaseWidget.to_html` method, which means custom widgets get HTML
support automatically as soon as they implement that one method (the
:class:`BaseWidget` default does the right thing for most cases).
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from ..ast import types as T
from ..widgets.registry import WidgetRegistry, default_registry


class HTMLRenderer:
    """AST → HTML. Subclass to override individual ``_block_*`` methods."""

    def __init__(
        self,
        registry: Optional[WidgetRegistry] = None,
        *,
        wrap_root: bool = False,
    ) -> None:
        self.registry = registry or default_registry
        self.wrap_root = wrap_root

    # ── Public API ───────────────────────────────────────────────────────────
    def render(self, ast: Dict[str, Any]) -> str:
        if ast.get("type") != T.DOCUMENT:
            return self._block(ast)
        body = "".join(self._block(c) for c in ast.get("children", []))
        return f'<article class="markast">{body}</article>' if self.wrap_root else body

    # ── Dispatch ─────────────────────────────────────────────────────────────
    def _block(self, node: Dict[str, Any]) -> str:
        method = getattr(self, f"_block_{node.get('type')}", None)
        return method(node) if method else ""

    def _inline(self, children: List[Dict[str, Any]]) -> str:
        return "".join(self._inline_node(c) for c in children)

    def _inline_node(self, node: Dict[str, Any]) -> str:
        method = getattr(self, f"_inline_{node.get('type')}", None)
        return method(node) if method else ""

    def _children_html(self, children: List[Dict[str, Any]]) -> str:
        """Helper handed to widget .to_html() callbacks."""
        return "".join(self._block(c) for c in children)

    # ── Block renderers ──────────────────────────────────────────────────────
    def _block_heading(self, node: Dict[str, Any]) -> str:
        lvl = max(1, min(6, node.get("level", 1)))
        idattr = f' id="{escape_attr(node["id"])}"' if node.get("id") else ""
        return f'<h{lvl}{idattr}>{self._inline(node.get("children", []))}</h{lvl}>'

    def _block_paragraph(self, node: Dict[str, Any]) -> str:
        return f'<p>{self._inline(node.get("children", []))}</p>'

    def _block_blockquote(self, node: Dict[str, Any]) -> str:
        return f'<blockquote>{self._children_html(node.get("children", []))}</blockquote>'

    def _block_code_block(self, node: Dict[str, Any]) -> str:
        lang = node.get("language", "") or ""
        cls = f' class="lang-{escape_attr(lang)}"' if lang else ""
        body = escape_text(node.get("value", ""))
        filename = node.get("filename")
        pre = f'<pre><code{cls}>{body}</code></pre>'
        if filename:
            return (f'<figure class="code-block">'
                    f'<figcaption>{escape_text(filename)}</figcaption>{pre}</figure>')
        return pre

    def _block_image(self, node: Dict[str, Any]) -> str:
        title = node.get("title")
        title_attr = f' title="{escape_attr(title)}"' if title else ""
        return (f'<figure class="image"><img src="{escape_attr(node.get("src", ""))}" '
                f'alt="{escape_attr(node.get("alt", ""))}"{title_attr}></figure>')

    def _block_video(self, node: Dict[str, Any]) -> str:
        cls = self.registry.get("video")
        if cls is None:
            return ""
        return cls().to_html(
            {"type": T.WIDGET, "widget": "video",
             "props": {k: v for k, v in node.items() if k != "type"},
             "slots": {"default": []}},
            self._children_html,
        )

    def _block_list(self, node: Dict[str, Any]) -> str:
        tag = "ol" if node.get("ordered") else "ul"
        start_attr = ""
        if node.get("ordered") and node.get("start", 1) != 1:
            start_attr = f' start="{node["start"]}"'
        items = "".join(self._block_list_item(li) for li in node.get("children", []))
        return f'<{tag}{start_attr}>{items}</{tag}>'

    def _block_list_item(self, node: Dict[str, Any]) -> str:
        body_parts: List[str] = []
        for child in node.get("children", []):
            if child.get("type") in T.INLINE_TYPES:
                body_parts.append(self._inline_node(child))
            else:
                body_parts.append(self._block(child))
        body = "".join(body_parts)
        checked = node.get("checked")
        if checked is not None:
            mark = ' checked' if checked else ''
            return (f'<li class="task-list-item">'
                    f'<input type="checkbox" disabled{mark}> {body}</li>')
        return f"<li>{body}</li>"

    def _block_table(self, node: Dict[str, Any]) -> str:
        head = node.get("head", {}) or {}
        body = node.get("body", {}) or {}
        head_html = "".join(self._row_html(r) for r in head.get("rows", []))
        body_html = "".join(self._row_html(r) for r in body.get("rows", []))
        out = ['<table>']
        if head_html:
            out.append(f'<thead>{head_html}</thead>')
        if body_html:
            out.append(f'<tbody>{body_html}</tbody>')
        out.append('</table>')
        return "".join(out)

    def _row_html(self, row: Dict[str, Any]) -> str:
        cells = "".join(self._cell_html(c) for c in row.get("cells", []))
        return f'<tr>{cells}</tr>'

    def _cell_html(self, cell: Dict[str, Any]) -> str:
        tag = "th" if cell.get("is_header") else "td"
        align = cell.get("align")
        align_attr = f' style="text-align:{align}"' if align else ""
        return f'<{tag}{align_attr}>{self._inline(cell.get("children", []))}</{tag}>'

    def _block_divider(self, _: Dict[str, Any]) -> str:
        return "<hr>"

    def _block_html_block(self, node: Dict[str, Any]) -> str:
        return node.get("value", "")

    def _block_widget(self, node: Dict[str, Any]) -> str:
        cls = self.registry.get(node.get("widget", ""))
        if cls is None:
            return self._block_widget_generic(node)
        return cls().to_html(node, self._children_html)

    def _block_widget_generic(self, node: Dict[str, Any]) -> str:
        slots = node.get("slots") or {}
        body = self._children_html(slots.get("default", []))
        name = escape_attr(node.get("widget", "unknown"))
        return f'<div class="widget widget-{name}">{body}</div>'

    def _block_footnote_def(self, node: Dict[str, Any]) -> str:
        return (f'<aside class="footnote" id="fn-{escape_attr(node.get("label", ""))}">'
                f'{self._children_html(node.get("children", []))}</aside>')

    # ── Inline renderers ─────────────────────────────────────────────────────
    def _inline_text(self, node):           return escape_text(node.get("value", ""))
    def _inline_bold(self, node):           return f"<strong>{self._inline(node.get('children', []))}</strong>"
    def _inline_italic(self, node):         return f"<em>{self._inline(node.get('children', []))}</em>"
    def _inline_bold_italic(self, node):    return f"<strong><em>{self._inline(node.get('children', []))}</em></strong>"
    def _inline_code_inline(self, node):    return f"<code>{escape_text(node.get('value', ''))}</code>"
    def _inline_strikethrough(self, node):  return f"<del>{self._inline(node.get('children', []))}</del>"
    def _inline_underline(self, node):      return f"<u>{self._inline(node.get('children', []))}</u>"
    def _inline_softbreak(self, _):         return "\n"
    def _inline_hardbreak(self, _):         return "<br>"

    def _inline_link(self, node):
        href = escape_attr(node.get("href", ""))
        title = node.get("title")
        title_attr = f' title="{escape_attr(title)}"' if title else ""
        body = self._inline(node.get("children", []))
        return f'<a href="{href}"{title_attr}>{body}</a>'

    def _inline_inline_image(self, node):
        title = node.get("title")
        title_attr = f' title="{escape_attr(title)}"' if title else ""
        return (f'<img src="{escape_attr(node.get("src", ""))}" '
                f'alt="{escape_attr(node.get("alt", ""))}"{title_attr}>')

    def _inline_footnote_ref(self, node):
        label = escape_attr(node.get("label", ""))
        return f'<sup class="footnote-ref"><a href="#fn-{label}">{node.get("label", "")}</a></sup>'


# ─── Escape helpers ──────────────────────────────────────────────────────────
def escape_text(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))


def escape_attr(s: Any) -> str:
    return (str(s).replace("&", "&amp;")
                  .replace('"', "&quot;")
                  .replace("<", "&lt;")
                  .replace(">", "&gt;"))
