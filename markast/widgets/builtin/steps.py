"""
Steps widget — numbered procedural sequences.

Markdown::

    :::steps

    # step-1
    Install the dependency.

    ```bash
    pip install markast
    ```

    # step-2
    Import and call ``parse``.

    ```python
    from markast import parse
    doc = parse("# Hi")
    ```

    :::

Slots are rendered in the order they appear in the source. Their names are
opaque labels — clients can show them as-is or hide them and rely solely on
order.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List

from ..base import BaseWidget, WidgetParam


class StepsWidget(BaseWidget):
    """A numbered list of steps, where each step is a named slot."""

    name = "steps"
    slots: List[str] = []
    allow_unknown_props = True
    params = {
        "start": WidgetParam(int, default=1, description="Number to start counting from."),
    }

    def to_markdown(
        self,
        node: Dict[str, Any],
        render_children: Callable[[List[Dict[str, Any]]], str],
    ) -> str:
        props = node.get("props", {}) or {}
        slots_data = node.get("slots", {}) or {}

        header = ":::steps"
        if props.get("start") and props["start"] != 1:
            header += f' start={props["start"]}'

        parts: List[str] = [header, ""]
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
        start = (node.get("props") or {}).get("start", 1)
        items: List[str] = []
        for i, (slot_name, slot_children) in enumerate(
            (k, v) for k, v in slots_data.items() if k != "default" and v
        ):
            n = start + i
            items.append(
                f'<li class="step" data-step="{slot_name}">'
                f'<span class="step-number">{n}</span>'
                f'<div class="step-body">{render_children(slot_children)}</div>'
                f'</li>'
            )
        return f'<ol class="steps">{"".join(items)}</ol>'
