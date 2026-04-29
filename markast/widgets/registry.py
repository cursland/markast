"""
:class:`WidgetRegistry` — a per-parser registry of widget classes.

Registries are **not** singletons. Each :class:`markast.Parser` owns one. A
separate :data:`default_registry` exists so the top-level :func:`markast.parse`
shortcut has somewhere to look up built-in widgets without forcing every
caller to construct a parser.

This design makes:

* Multi-tenant servers safe (different parsers can hold different widget sets).
* Tests trivially reproducible (no leftover state between cases).
* Widget overrides explicit (clone the default and tweak — or build a fresh
  registry from scratch).
"""
from __future__ import annotations
from typing import Dict, Iterator, List, Optional, Type

from ..exceptions import WidgetRegistrationError
from .base import BaseWidget


class WidgetRegistry:
    """Maps widget names → widget classes.

    Methods
    -------
    register(cls):       add a widget class (also usable as a decorator)
    unregister(name):    remove by name
    get(name):           lookup, returns None if missing
    names():             list registered names
    clone():             deep copy (new registry, same classes)
    """

    def __init__(self, widgets: Optional[List[Type[BaseWidget]]] = None) -> None:
        self._widgets: Dict[str, Type[BaseWidget]] = {}
        if widgets:
            for w in widgets:
                self.register(w)

    # ── Registration ─────────────────────────────────────────────────────────
    def register(self, widget_class: Type[BaseWidget]) -> Type[BaseWidget]:
        """Register a widget class. Usable as a decorator::

            @registry.register
            class FooWidget(BaseWidget):
                name = "foo"
        """
        if not isinstance(widget_class, type) or not issubclass(widget_class, BaseWidget):
            raise WidgetRegistrationError(
                f"register() expects a BaseWidget subclass, got {widget_class!r}",
            )
        if not widget_class.name:
            raise WidgetRegistrationError(
                f"Widget class {widget_class.__name__} must define a non-empty `name`.",
            )
        self._widgets[widget_class.name] = widget_class
        return widget_class

    def register_many(self, classes: List[Type[BaseWidget]]) -> None:
        for cls in classes:
            self.register(cls)

    def unregister(self, name: str) -> None:
        self._widgets.pop(name, None)

    # ── Lookup ───────────────────────────────────────────────────────────────
    def get(self, name: str) -> Optional[Type[BaseWidget]]:
        return self._widgets.get(name)

    def has(self, name: str) -> bool:
        return name in self._widgets

    __contains__ = has

    def names(self) -> List[str]:
        return list(self._widgets)

    def __iter__(self) -> Iterator[str]:
        return iter(self._widgets)

    # ── Cloning ──────────────────────────────────────────────────────────────
    def clone(self) -> "WidgetRegistry":
        """Return a new registry holding the same widget classes."""
        new = WidgetRegistry()
        new._widgets = dict(self._widgets)
        return new

    def __repr__(self) -> str:
        return f"WidgetRegistry({sorted(self._widgets)})"


# ─── Default shared registry ─────────────────────────────────────────────────
#: A registry pre-populated with built-in widgets (admonitions, card, video,
#: code-group, code-collapse, tabs, steps). Used by the top-level
#: :func:`markast.parse` helper so callers don't have to construct a Parser for
#: simple cases.
default_registry = WidgetRegistry()


def _populate_default_registry() -> None:
    """Import built-in widget modules so they self-register on import.

    Called once at package import time. Done lazily here to avoid circular
    imports between :mod:`markast.widgets.registry` and ``builtin/*``.
    """
    from .builtin import (   # noqa: F401  — import side effects register classes
        admonition, card, video, code_group, code_collapse, tabs, steps, badge,
    )

    classes = (
        admonition.TipWidget,
        admonition.NoteWidget,
        admonition.WarningWidget,
        admonition.InfoWidget,
        admonition.CautionWidget,
        admonition.DangerWidget,
        card.CardWidget,
        video.VideoWidget,
        code_group.CodeGroupWidget,
        code_collapse.CodeCollapseWidget,
        tabs.TabsWidget,
        steps.StepsWidget,
        badge.BadgeWidget,
    )
    for cls in classes:
        if cls.name and cls.name not in default_registry:
            default_registry.register(cls)
