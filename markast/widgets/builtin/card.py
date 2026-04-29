"""
Card widget — a container with optional ``header`` and ``footer`` slots.

Markdown::

    :::card title="My Card" elevated=true
    Body content.

    # header
    Custom header.

    # footer
    Custom footer.
    :::
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List

from ..base import BaseWidget, WidgetParam


class CardWidget(BaseWidget):
    """A flexible card with header / default / footer slots."""

    name = "card"
    slots = ["header", "footer"]
    params = {
        "title":    WidgetParam(str,  default=None, description="Card title shown in the header."),
        "color":    WidgetParam(str,  default=None, description="Accent color hint for clients."),
        "elevated": WidgetParam(bool, default=False, description="Show a subtle shadow."),
    }

    def to_html(
        self,
        node: Dict[str, Any],
        render_children: Callable[[List[Dict[str, Any]]], str],
    ) -> str:
        props = node.get("props", {}) or {}
        slots = node.get("slots", {}) or {}

        title = props.get("title")
        cls = "card"
        if props.get("elevated"):
            cls += " card-elevated"
        if props.get("color"):
            cls += f" card-color-{props['color']}"

        header_slot = slots.get("header")
        body_slot   = slots.get("default", [])
        footer_slot = slots.get("footer")

        out: List[str] = [f'<article class="{cls}">']
        if header_slot:
            out.append(f'<header>{render_children(header_slot)}</header>')
        elif title:
            out.append(f'<header><h3>{title}</h3></header>')
        if body_slot:
            out.append(f'<div class="card-body">{render_children(body_slot)}</div>')
        if footer_slot:
            out.append(f'<footer>{render_children(footer_slot)}</footer>')
        out.append("</article>")
        return "".join(out)
