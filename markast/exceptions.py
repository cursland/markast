"""Exception hierarchy for markast.

The library never raises on bad *content* — invalid markdown produces a
diagnostic in ``document.warnings`` and the parse continues. Exceptions are
reserved for genuine programmer errors (misconfiguration, invalid widget
class, etc.).
"""
from __future__ import annotations


class MdastError(Exception):
    """Base class for all markast exceptions."""


class ConfigurationError(MdastError):
    """Raised when a Parser is constructed with invalid options."""


class WidgetRegistrationError(MdastError):
    """Raised when registering a widget that is malformed (missing name,
    duplicate registration, etc.)."""


class RenderError(MdastError):
    """Raised by a renderer when it receives a node it can't handle and
    has no fallback. Most renderers prefer to silently skip unknown nodes
    instead of raising; this is for strict modes."""
