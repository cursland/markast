"""
Tabs widget — each named slot is a tab. Slot dividers act as tab labels.

Markdown::

    :::tabs default="overview"

    # overview
    The **overview** tab content.

    # details
    Deeper details with code:

    ```python
    print("hi")
    ```

    # faq
    Frequently asked questions.

    :::
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List

from ..base import BaseWidget, WidgetParam


class TabsWidget(BaseWidget):
    """A tab strip whose tabs are the named slots of the widget body.

    Note that :attr:`slots` is left empty: the parser doesn't restrict slot
    names, so any ``# slot-name`` divider becomes a tab. The default slot
    (content before the first divider) is treated as a fallback / preamble.
    """

    name = "tabs"
    slots: List[str] = []  # any slot name is accepted
    allow_unknown_props = True
    params = {
        "default":  WidgetParam(str,  default=None,
                                description="Slot name of the tab to open first."),
        "vertical": WidgetParam(bool, default=False,
                                description="Render tabs vertically (clients may ignore)."),
    }

    def to_markdown(
        self,
        node: Dict[str, Any],
        render_children: Callable[[List[Dict[str, Any]]], str],
    ) -> str:
        props = node.get("props", {}) or {}
        slots_data = node.get("slots", {}) or {}

        header = ":::tabs"
        if props.get("default"):
            header += f' default="{props["default"]}"'
        if props.get("vertical"):
            header += " vertical"

        parts: List[str] = [header, ""]

        # Default slot first (preamble), then named slots.
        if slots_data.get("default"):
            parts.append(render_children(slots_data["default"]))
            parts.append("")

        for slot_name, slot_children in slots_data.items():
            if slot_name == "default" or not slot_children:
                continue
            parts.append(f"# {slot_name}")
            parts.append("")
            parts.append(render_children(slot_children))
            parts.append("")

        parts.append(":::")
        return "\n".join(parts)

    def to_html(
        self,
        node: Dict[str, Any],
        render_children: Callable[[List[Dict[str, Any]]], str],
    ) -> str:
        slots_data = node.get("slots", {}) or {}
        named = [(k, v) for k, v in slots_data.items() if k != "default" and v]
        if not named:
            return f'<div class="tabs">{render_children(slots_data.get("default", []))}</div>'
        labels = "".join(
            f'<button class="tab" data-tab="{name}">{name}</button>' for name, _ in named
        )
        panes = "".join(
            f'<section class="tab-pane" data-tab="{name}">{render_children(children)}</section>'
            for name, children in named
        )
        return f'<div class="tabs"><div class="tab-strip">{labels}</div>{panes}</div>'
