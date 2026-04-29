"""
Diagnostic and Rule primitives.

A :class:`Diagnostic` is the data record collected on the document. It carries
a code, a message, the offending context, and a severity.

A :class:`Rule` is a unit of validation logic. It exposes hooks the builder
calls at well-defined points; the default implementations do nothing so
subclasses can override only what they care about.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


# ─── Severity ────────────────────────────────────────────────────────────────
class Severity:
    """String constants for the ``severity`` field of a diagnostic."""
    ERROR   = "error"
    WARNING = "warning"
    INFO    = "info"


# ─── Diagnostic record ───────────────────────────────────────────────────────
@dataclass
class Diagnostic:
    """A single diagnostic entry to be attached to ``document["warnings"]``.

    Stored as a dataclass so callers can inspect ``diagnostic.code`` etc.;
    serialised to a plain dict via :meth:`to_dict` for JSON output.
    """
    code: str
    message: str
    context: str = ""
    severity: str = Severity.WARNING

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # Keep the on-the-wire format minimal — clients only care about
        # severity if it isn't "warning".
        if d["severity"] == Severity.WARNING:
            d.pop("severity")
        return d


# ─── Rule base ───────────────────────────────────────────────────────────────
class Rule:
    """Base class for validation rules.

    The builder calls each registered rule's hooks at well-defined points and
    appends any returned :class:`Diagnostic` instances to the document.

    Subclasses typically override one of:

    * :meth:`check_heading_children`
    * :meth:`check_table_cell_children`
    * :meth:`check_widget`
    * :meth:`check_html_block`
    * :meth:`check_footnote_ref`

    Returning ``None`` (or an empty list) signals "nothing to report".
    """

    #: A short, unique identifier — used for selective enable/disable.
    name: str = ""

    def check_heading_children(
        self,
        children: List[Dict[str, Any]],
        level: int,
    ) -> Optional[List[Diagnostic]]:
        return None

    def check_table_cell_children(
        self,
        children: List[Dict[str, Any]],
        is_header: bool,
    ) -> Optional[List[Diagnostic]]:
        return None

    def check_widget(
        self,
        widget_name: str,
        props: Dict[str, Any],
        slots: Dict[str, List[Dict[str, Any]]],
        registered: bool,
    ) -> Optional[List[Diagnostic]]:
        return None

    def check_html_block(
        self,
        value: str,
    ) -> Optional[List[Diagnostic]]:
        return None

    def check_footnote_ref(
        self,
        label: str,
        defined_labels: set,
    ) -> Optional[List[Diagnostic]]:
        return None
