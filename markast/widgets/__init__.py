"""
markast.widgets
─────────────
The widget system. A *widget* is a Python class that knows how to:

1. Validate its props (typed parameters parsed from the ``:::widget`` header).
2. Reconstruct itself as Markdown when the renderer roundtrips an AST.
3. *Optionally* render to HTML if the HTML renderer is used.

Widgets are registered on a :class:`WidgetRegistry`. Every :class:`Parser`
owns its own registry — there is no global mutable state — but a default
registry (:data:`default_registry`) is exposed for convenience and is what the
top-level :func:`markast.parse` shortcut uses.

Public surface
~~~~~~~~~~~~~~

* :class:`BaseWidget` — base class to subclass
* :class:`WidgetParam` — declarative parameter descriptor
* :class:`WidgetRegistry` — non-singleton registry
* :data:`default_registry` — shared default registry used by the top-level
  ``parse()`` helper
"""
from .base import BaseWidget, WidgetParam
from .registry import WidgetRegistry, default_registry

__all__ = [
    "BaseWidget",
    "WidgetParam",
    "WidgetRegistry",
    "default_registry",
]
