"""
Badge widget — a compact, inline-feeling pill with a label and optional color.

Although clients usually want this *inside* a paragraph, markast keeps it as a
block-level widget for simplicity. Clients that want inline rendering can
detect the widget and merge it back into surrounding text.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List

from ..base import BaseWidget, WidgetParam


class BadgeWidget(BaseWidget):
    """A small label/value pill."""

    name = "badge"
    params = {
        "label": WidgetParam(str, required=True, description="Badge text."),
        "color": WidgetParam(str, default="gray",
                             choices=["gray", "red", "green", "blue", "yellow", "purple"],
                             description="Accent color."),
    }

    def to_markdown(
        self,
        node: Dict[str, Any],
        render_children: Callable[[List[Dict[str, Any]]], str],
    ) -> str:
        p = node.get("props", {}) or {}
        return f':::badge label="{p.get("label", "")}" color={p.get("color", "gray")}\n:::'

    def to_html(
        self,
        node: Dict[str, Any],
        render_children: Callable[[List[Dict[str, Any]]], str],
    ) -> str:
        p = node.get("props", {}) or {}
        return f'<span class="badge badge-{p.get("color", "gray")}">{p.get("label", "")}</span>'
