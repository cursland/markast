"""
Built-in widgets bundled with markast.

The :data:`markast.widgets.default_registry` is populated with these on package
import so that :func:`markast.parse` recognises them out of the box.

Widgets included
----------------

* **Admonitions** (consolidated): ``tip``, ``note``, ``warning``, ``info``,
  ``caution``, ``danger`` — all share the same logic via a parameterised base.
* ``card`` — generic card with ``header``/``footer`` slots.
* ``video`` — video embed with poster, controls, autoplay, loop.
* ``code-group`` — tabbed group of code blocks.
* ``code-collapse`` — collapsible block of code.
* ``tabs`` — tabbed content (each tab is a slot).
* ``steps`` — numbered step list (each step is a slot).
* ``badge`` — inline badge with label and color.

Each module here can serve as a worked example for writing your own widget;
they are short on purpose and avoid clever metaprogramming.
"""
from . import admonition, card, video, code_group, code_collapse, tabs, steps, badge

__all__ = [
    "admonition", "card", "video", "code_group", "code_collapse",
    "tabs", "steps", "badge",
]
