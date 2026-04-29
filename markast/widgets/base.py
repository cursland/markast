"""
:class:`WidgetParam` (parameter descriptor) and :class:`BaseWidget` (the class
every widget subclasses).

Why explicit param descriptors?
-------------------------------
With :class:`WidgetParam` the parser knows how to:

* cast strings into the right Python type (``int``, ``bool``, ``Enum``, …);
* fill in default values when a prop is omitted;
* warn (without crashing) when a value is out of ``choices`` or required;
* emit an introspectable schema for IDE tooling and clients.

That keeps each widget class small — most need only a name, a ``params``
dict, and (optionally) a custom ``to_html``. Type coercion, default values,
choice validation, required-prop checks, and roundtrip rendering are all
handled by :class:`BaseWidget` itself.
"""
from __future__ import annotations
import enum
import json
from abc import ABC
from typing import (
    Any, Callable, ClassVar, Dict, List, Optional, Tuple, Type, Union,
)

from ..rules.base import Diagnostic
from ..rules.codes import W_INVALID_PROP, W_MISSING_PROP


# ─── WidgetParam ─────────────────────────────────────────────────────────────
class WidgetParam:
    """A typed parameter descriptor for widget props.

    Parameters
    ----------
    type_ : type
        Python type the prop will be coerced to. One of:
        ``str``, ``int``, ``float``, ``bool``, ``list``, ``dict``, or any
        :class:`enum.Enum` subclass.
    default :
        Default Python value when the prop is omitted in markdown. Use
        :data:`None` to mean "no default" (still recorded as ``None`` in the
        produced AST so clients can distinguish "absent" from "present").
    required : bool
        If ``True``, a missing prop raises a :data:`W005` diagnostic.
    choices : list, optional
        Restrict the prop to a discrete set of values. Anything else raises
        :data:`W004`.
    description : str
        Free-form description used in ``BaseWidget.schema()`` and IDE tools.
    validator : Callable[[value], Optional[str]], optional
        Custom validator. Receives the casted value and returns ``None`` on
        success or an error message string. Errors raise :data:`W004`.

    Examples
    --------
    >>> WidgetParam(int, default=1, description="Repeat count")
    >>> WidgetParam(str, default="info", choices=["info", "warn", "error"])
    >>> WidgetParam(MyEnum, default=MyEnum.A)
    >>> WidgetParam(list, default=[])
    >>> WidgetParam(dict, default={})
    """

    def __init__(
        self,
        type_: Type[Any] = str,
        *,
        default: Any = None,
        required: bool = False,
        description: str = "",
        choices: Optional[List[Any]] = None,
        validator: Optional[Callable[[Any], Optional[str]]] = None,
    ) -> None:
        self.type_ = type_
        self.default = default
        self.required = required
        self.description = description
        self.choices = choices
        self.validator = validator

    # ── Type coercion ────────────────────────────────────────────────────────
    def cast(self, raw: str) -> Any:
        """Coerce a raw string (as it appears in markdown) into the param's
        Python type. Raises :class:`ValueError` on malformed input."""
        if self.type_ is bool:
            return _parse_bool(raw)
        if self.type_ is int:
            return int(raw)
        if self.type_ is float:
            return float(raw)
        if self.type_ is list:
            # Comma-separated, with JSON fallback for `[a,b,c]`-style values.
            stripped = raw.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                return json.loads(stripped)
            return [v.strip() for v in raw.split(",") if v.strip()]
        if self.type_ is dict:
            return json.loads(raw)
        if isinstance(self.type_, type) and issubclass(self.type_, enum.Enum):
            try:
                return self.type_(raw)
            except ValueError:
                # Allow lookup by member *name* too (case-insensitive).
                for member in self.type_:
                    if member.name.lower() == raw.lower():
                        return member
                raise
        # Default: keep as string.
        return raw

    # ── Schema dict ──────────────────────────────────────────────────────────
    def to_schema(self) -> Dict[str, Any]:
        """Describe this param in a tooling-friendly dict."""
        schema: Dict[str, Any] = {
            "type": _type_name(self.type_),
            "required": self.required,
        }
        if self.default is not None:
            schema["default"] = _serialize(self.default)
        if self.description:
            schema["description"] = self.description
        if self.choices:
            schema["choices"] = [_serialize(c) for c in self.choices]
        return schema


# ─── BaseWidget ──────────────────────────────────────────────────────────────
class BaseWidget(ABC):
    """Subclass to define a widget.

    Class attributes you typically set:

    name : str
        Identifier used in markdown — the ``foo`` in ``:::foo``.
    params : Dict[str, WidgetParam]
        Declarative schema for the widget's props.
    slots : List[str]
        Extra named slots beyond ``"default"``. Slot dividers in markdown are
        bare ``# slot-name`` h1 headings at the root level of the widget body.
    allow_unknown_props : bool
        If ``False`` (default), unknown props produce a W004 diagnostic. Set
        to ``True`` for forward-compatibility.

    Methods you may override:

    to_markdown(node, render_children) -> str
        Roundtrip back to markdown. The default reproduces the canonical
        ``:::name key="value"`` syntax, which is enough for most widgets.
    to_html(node, render_children) -> str
        Optional HTML rendering. The default produces a ``<div>`` carrying
        the widget name as a class.
    validate(props, slots) -> List[Diagnostic]
        Custom semantic validation beyond per-param type checks. Default is
        a no-op.

    Example
    -------
    >>> class BadgeWidget(BaseWidget):
    ...     name = "badge"
    ...     params = {
    ...         "label": WidgetParam(str, required=True),
    ...         "color": WidgetParam(str, default="gray",
    ...                              choices=["gray", "red", "green", "blue"]),
    ...     }
    """

    #: Widget identifier — used in :::name. *Must* be set on subclasses.
    name: ClassVar[str] = ""

    #: Parameter schema. {prop_name: WidgetParam(...)}
    params: ClassVar[Dict[str, WidgetParam]] = {}

    #: Extra slot names beyond "default".
    slots: ClassVar[List[str]] = []

    #: When False, unknown prop names emit W004; when True they pass through.
    allow_unknown_props: ClassVar[bool] = False

    # ── Prop validation (called by the builder) ──────────────────────────────
    def validate_props(
        self,
        raw_props: Dict[str, str],
    ) -> Tuple[Dict[str, Any], List[Diagnostic]]:
        """Cast raw string props into typed values and report problems.

        Returns ``(validated_props_dict, diagnostics_list)``.
        """
        validated: Dict[str, Any] = {}
        diagnostics: List[Diagnostic] = []

        # 1. Apply defaults.
        for pname, param in self.params.items():
            if param.default is not None:
                validated[pname] = param.default

        # 2. Validate provided values.
        for key, raw_val in raw_props.items():
            param = self.params.get(key)
            if param is None:
                if not self.allow_unknown_props:
                    diagnostics.append(Diagnostic(
                        code=W_INVALID_PROP,
                        message=f"Unknown prop '{key}' on widget '{self.name}'.",
                        context=f"widget={self.name}",
                    ))
                validated[key] = raw_val
                continue

            try:
                value = param.cast(raw_val) if isinstance(raw_val, str) else raw_val
            except (ValueError, TypeError, json.JSONDecodeError) as exc:
                diagnostics.append(Diagnostic(
                    code=W_INVALID_PROP,
                    message=(f"Prop '{key}' on widget '{self.name}' could not be parsed "
                             f"as {_type_name(param.type_)} ({exc}); raw value kept."),
                    context=f"widget={self.name}, raw={raw_val!r}",
                ))
                validated[key] = raw_val
                continue

            if param.choices and value not in param.choices:
                diagnostics.append(Diagnostic(
                    code=W_INVALID_PROP,
                    message=(f"Prop '{key}'={value!r} is not in allowed choices "
                             f"{param.choices} for widget '{self.name}'."),
                    context=f"widget={self.name}",
                ))

            if param.validator is not None:
                err = param.validator(value)
                if err:
                    diagnostics.append(Diagnostic(
                        code=W_INVALID_PROP,
                        message=f"Prop '{key}' failed validation: {err}",
                        context=f"widget={self.name}",
                    ))

            validated[key] = value

        # 3. Required-prop check.
        for pname, param in self.params.items():
            if param.required and pname not in raw_props:
                diagnostics.append(Diagnostic(
                    code=W_MISSING_PROP,
                    message=f"Required prop '{pname}' missing on widget '{self.name}'.",
                    context=f"widget={self.name}",
                ))

        return validated, diagnostics

    # ── Roundtrip rendering ──────────────────────────────────────────────────
    def to_markdown(
        self,
        node: Dict[str, Any],
        render_children: Callable[[List[Dict[str, Any]]], str],
    ) -> str:
        """Render the widget back to markdown.

        The default implementation produces::

            :::name k1="v1" k2=v2

            <default slot rendered>

            # slot-name
            <slot rendered>

            :::

        which is round-trip-stable for most widgets. Override only when the
        canonical syntax differs (e.g. ``:::code-group`` whose default slot is
        a sequence of fenced code blocks).
        """
        props = node.get("props", {}) or {}
        slots_data = node.get("slots", {}) or {}

        prop_str = _format_props(props)
        header = f":::{self.name}{(' ' + prop_str) if prop_str else ''}"
        parts: List[str] = [header, ""]

        default_slot = slots_data.get("default", [])
        if default_slot:
            parts.append(render_children(default_slot))
            parts.append("")

        for slot_name in self.slots:
            slot_children = slots_data.get(slot_name)
            if slot_children:
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
        """Render the widget to HTML.

        Default implementation: a ``<div class="widget widget-{name}">``
        wrapping the rendered default slot. Suitable for widgets whose visual
        meaning is carried by CSS rather than custom markup.
        """
        slots_data = node.get("slots", {}) or {}
        body = render_children(slots_data.get("default", []))
        attrs = f' class="widget widget-{self.name}"'
        return f"<div{attrs}>{body}</div>"

    # ── Custom validation hook ───────────────────────────────────────────────
    def validate(
        self,
        props: Dict[str, Any],
        slots: Dict[str, List[Dict[str, Any]]],
    ) -> List[Diagnostic]:
        """Override for cross-prop semantic checks. Default is no-op."""
        return []

    # ── Schema export (introspection) ────────────────────────────────────────
    @classmethod
    def schema(cls) -> Dict[str, Any]:
        """Describe this widget as a dict suitable for documentation tools."""
        return {
            "name": cls.name,
            "params": {k: p.to_schema() for k, p in cls.params.items()},
            "slots": ["default", *cls.slots],
            "doc": (cls.__doc__ or "").strip(),
        }


# ─── Helpers ─────────────────────────────────────────────────────────────────
def _parse_bool(raw: str) -> bool:
    s = raw.strip().lower()
    if s in ("true", "1", "yes", "on"):
        return True
    if s in ("false", "0", "no", "off"):
        return False
    raise ValueError(f"cannot parse {raw!r} as bool")


def _type_name(t: Type[Any]) -> str:
    if isinstance(t, type) and issubclass(t, enum.Enum):
        return f"enum:{t.__name__}"
    return getattr(t, "__name__", str(t))


def _serialize(v: Any) -> Any:
    if isinstance(v, enum.Enum):
        return v.value
    return v


def _format_props(props: Dict[str, Any]) -> str:
    """Format a typed props dict back into ``key="val"`` markdown syntax."""
    tokens: List[str] = []
    for key, val in props.items():
        if val is None:
            continue
        if val is True:
            tokens.append(key)
            continue
        if val is False:
            tokens.append(f"{key}=false")
            continue
        if isinstance(val, enum.Enum):
            val = val.value
        s = str(val)
        if any(c.isspace() for c in s) or any(c in s for c in '"\'='):
            tokens.append(f'{key}="{s}"')
        else:
            tokens.append(f"{key}={s}")
    return " ".join(tokens)
