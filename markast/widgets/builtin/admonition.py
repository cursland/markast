"""
Admonition widgets.

Six flavours (tip, note, info, warning, caution, danger) share an identical
contract — only their ``name`` and default labelling differs. They are
implemented as one parameterised :class:`Admonition` base plus thin
subclasses, so adding a new flavour is a one-line subclass.

All admonitions share this contract:

* Markdown::

      :::tip title="Pro tip" icon="lightbulb"
      Body content with **markdown** support.
      :::

* AST node::

      {
          "type":   "widget",
          "widget": "tip",
          "props":  {"title": "Pro tip", "icon": "lightbulb"},
          "slots":  {"default": [...]}
      }

* HTML::

      <aside class="admonition admonition-tip">
        <header>Pro tip</header>
        <div class="admonition-body">...</div>
      </aside>
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List

from ..base import BaseWidget, WidgetParam


class Admonition(BaseWidget):
    """Shared parent for all admonition flavours.

    Subclasses set :attr:`name` and (optionally) :attr:`default_icon` /
    :attr:`default_title`. Everything else is inherited.
    """

    #: Default icon used by HTML rendering when ``icon`` prop is absent.
    default_icon: str = ""
    #: Default title used by HTML rendering when ``title`` prop is absent.
    default_title: str = ""

    params = {
        "title": WidgetParam(str, default=None, description="Optional title shown in the header."),
        "icon":  WidgetParam(str, default=None, description="Icon name (consumer-defined)."),
    }

    def to_html(
        self,
        node: Dict[str, Any],
        render_children: Callable[[List[Dict[str, Any]]], str],
    ) -> str:
        props = node.get("props", {}) or {}
        title = props.get("title") or self.default_title
        body = render_children(node.get("slots", {}).get("default", []))
        cls = f"admonition admonition-{self.name}"
        header = f"<header>{title}</header>" if title else ""
        return f'<aside class="{cls}">{header}<div class="admonition-body">{body}</div></aside>'


class TipWidget(Admonition):
    """A friendly tip callout. Use to surface a useful but non-essential fact."""
    name = "tip"
    default_icon = "lightbulb"
    default_title = "Tip"


class NoteWidget(Admonition):
    """A neutral note callout. Use for asides that don't fit the surrounding flow."""
    name = "note"
    default_icon = "note"
    default_title = "Note"


class InfoWidget(Admonition):
    """An info callout. Slightly more emphatic than ``note``."""
    name = "info"
    default_icon = "info"
    default_title = "Info"


class WarningWidget(Admonition):
    """A warning callout. Use to flag something the reader should be careful about."""
    name = "warning"
    default_icon = "warning"
    default_title = "Warning"


class CautionWidget(Admonition):
    """A caution callout. Stronger than ``warning`` — use sparingly."""
    name = "caution"
    default_icon = "caution"
    default_title = "Caution"


class DangerWidget(Admonition):
    """A danger callout. Reserved for irrecoverable / destructive operations."""
    name = "danger"
    default_icon = "danger"
    default_title = "Danger"
