"""
Code-group widget — tabs over a sequence of code blocks. Each block's
``filename`` is its tab label.

Markdown::

    :::code-group
    ```bash [npm]
    npm install pkg
    ```

    ```bash [yarn]
    yarn add pkg
    ```
    :::
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List

from ...ast import types as T
from ..base import BaseWidget, WidgetParam


class CodeGroupWidget(BaseWidget):
    """A tab strip over multiple code blocks. Tabs are derived from each
    block's ``filename``."""

    name = "code-group"
    params = {
        "default_tab": WidgetParam(str, default=None, description="Filename of tab to show first."),
    }

    def to_markdown(
        self,
        node: Dict[str, Any],
        render_children: Callable[[List[Dict[str, Any]]], str],
    ) -> str:
        props = node.get("props", {}) or {}
        header = ":::code-group"
        if props.get("default_tab"):
            header += f' default_tab="{props["default_tab"]}"'

        parts: List[str] = [header, ""]
        for block in node.get("slots", {}).get("default", []):
            if block.get("type") != T.CODE_BLOCK:
                continue
            info = block.get("language", "") or ""
            if block.get("filename"):
                info += f" [{block['filename']}]"
            if block.get("highlight_lines"):
                info += f"{{{_format_highlight(block['highlight_lines'])}}}"
            parts.append(f"```{info}")
            parts.append(block.get("value", ""))
            parts.append("```")
            parts.append("")
        parts.append(":::")
        return "\n".join(parts)

    def to_html(
        self,
        node: Dict[str, Any],
        render_children: Callable[[List[Dict[str, Any]]], str],
    ) -> str:
        blocks = [
            b for b in node.get("slots", {}).get("default", [])
            if b.get("type") == T.CODE_BLOCK
        ]
        if not blocks:
            return '<div class="code-group"></div>'
        tabs = "".join(
            f'<button class="code-group-tab" data-filename="{b.get("filename", "")}">'
            f'{b.get("filename") or b.get("language") or "code"}</button>'
            for b in blocks
        )
        panes = "".join(
            f'<pre data-filename="{b.get("filename", "")}">'
            f'<code class="lang-{b.get("language", "")}">{_escape(b.get("value", ""))}</code>'
            f'</pre>'
            for b in blocks
        )
        return f'<div class="code-group"><div class="code-group-tabs">{tabs}</div>{panes}</div>'


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


def _escape(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))
