"""
Video embed widget.

Roundtrips to ``:::video`` markdown and produces a ``<video>`` element in HTML
output.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List

from ..base import BaseWidget, WidgetParam


class VideoWidget(BaseWidget):
    """A video embed.

    Required prop: ``src``. Common props: ``poster``, ``controls`` (default
    ``True``), ``autoplay``, ``loop``, ``width``, ``height``, ``caption``.
    """

    name = "video"
    params = {
        "src":      WidgetParam(str,  required=True,  description="Video URL."),
        "poster":   WidgetParam(str,  default=None,   description="Poster image URL."),
        "controls": WidgetParam(bool, default=True,   description="Show playback controls."),
        "autoplay": WidgetParam(bool, default=False,  description="Autoplay on load."),
        "loop":     WidgetParam(bool, default=False,  description="Loop playback."),
        "muted":    WidgetParam(bool, default=False,  description="Start muted."),
        "width":    WidgetParam(str,  default=None,   description="CSS width (e.g. 100%, 640px)."),
        "height":   WidgetParam(str,  default=None,   description="CSS height."),
        "caption":  WidgetParam(str,  default=None,   description="Caption text shown below."),
    }

    def to_markdown(
        self,
        node: Dict[str, Any],
        render_children: Callable[[List[Dict[str, Any]]], str],
    ) -> str:
        props = node.get("props", {}) or {}
        tokens: List[str] = [f'src="{props.get("src", "")}"']

        for key in ("poster", "width", "height", "caption"):
            v = props.get(key)
            if v:
                tokens.append(f'{key}="{v}"')

        for key in ("controls", "autoplay", "loop", "muted"):
            v = props.get(key)
            if v is True:
                tokens.append(key)
            elif v is False and key in props:
                tokens.append(f"{key}=false")

        return f":::video {' '.join(tokens)}\n:::"

    def to_html(
        self,
        node: Dict[str, Any],
        render_children: Callable[[List[Dict[str, Any]]], str],
    ) -> str:
        p = node.get("props", {}) or {}
        attrs: List[str] = [f'src="{p.get("src", "")}"']
        for key in ("poster", "width", "height"):
            v = p.get(key)
            if v:
                attrs.append(f'{key}="{v}"')
        for flag in ("controls", "autoplay", "loop", "muted"):
            if p.get(flag):
                attrs.append(flag)
        video_tag = f"<video {' '.join(attrs)}></video>"
        if p.get("caption"):
            return f'<figure>{video_tag}<figcaption>{p["caption"]}</figcaption></figure>'
        return video_tag
