"""
Collapsible code block — wraps any block content in a ``<details>``.

Markdown::

    :::code-collapse summary="Show full config"
    ```toml [pyproject.toml]
    ...long file...
    ```
    :::
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List

from ..base import BaseWidget, WidgetParam


class CodeCollapseWidget(BaseWidget):
    """A collapsible region around code (or any) blocks."""

    name = "code-collapse"
    params = {
        "summary": WidgetParam(str,  default="Show code",
                               description="Label shown on the toggle button."),
        "open":    WidgetParam(bool, default=False,
                               description="Whether the region starts expanded."),
    }

    def to_markdown(
        self,
        node: Dict[str, Any],
        render_children: Callable[[List[Dict[str, Any]]], str],
    ) -> str:
        props = node.get("props", {}) or {}
        header = f':::code-collapse summary="{props.get("summary", "Show code")}"'
        if props.get("open"):
            header += " open"
        parts: List[str] = [header, ""]
        slot = node.get("slots", {}).get("default", [])
        if slot:
            parts.append(render_children(slot))
            parts.append("")
        parts.append(":::")
        return "\n".join(parts)

    def to_html(
        self,
        node: Dict[str, Any],
        render_children: Callable[[List[Dict[str, Any]]], str],
    ) -> str:
        props = node.get("props", {}) or {}
        body = render_children(node.get("slots", {}).get("default", []))
        open_attr = " open" if props.get("open") else ""
        summary = props.get("summary", "Show code")
        return f'<details{open_attr}><summary>{summary}</summary>{body}</details>'
