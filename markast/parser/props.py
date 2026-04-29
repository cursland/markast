"""
Parse a widget's header line into a raw props dict.

Examples
--------

* ``:::tip title="Pro tip" icon=lightbulb``
  → ``{"title": "Pro tip", "icon": "lightbulb"}``

* ``:::warning Deprecated since v3.0``
  → ``{"title": "Deprecated since v3.0"}`` (positional → ``title``)

* ``:::card title="Hi" elevated=true color='blue'``
  → ``{"title": "Hi", "elevated": "true", "color": "blue"}``

The output is always ``Dict[str, str]`` — type coercion happens later in
:meth:`BaseWidget.validate_props`. Keeping the layers separate means the
parser doesn't need to know anything about the widget schema.
"""
from __future__ import annotations
import re
from typing import Dict


_PROP_RE = re.compile(
    r'(?P<key>[\w][\w-]*)='
    r'(?:'
        r'"(?P<dq>[^"]*)"'
        r"|'(?P<sq>[^']*)'"
        r"|(?P<bare>[^\s\"']+)"
    r')'
)


def parse_props(info: str, widget_name: str) -> Dict[str, str]:
    """Parse the trailing portion of a widget header into a props dict.

    Recognises three quoting styles:

    * ``key="quoted with spaces"``
    * ``key='single-quoted'``
    * ``key=bare-token``

    Anything before the first ``key=`` (and after the widget name) is captured
    as the implicit ``title`` prop, *unless* an explicit ``title=`` is given.
    """
    s = info.strip()
    if s.startswith(widget_name):
        s = s[len(widget_name):].strip()

    props: Dict[str, str] = {}
    for m in _PROP_RE.finditer(s):
        key = m.group("key")
        val = m.group("dq")
        if val is None:
            val = m.group("sq")
        if val is None:
            val = m.group("bare") or ""
        props[key] = val

    first = _PROP_RE.search(s)
    leading = s[: first.start()].strip() if first else s.strip()
    if leading and "title" not in props:
        props["title"] = leading

    return props


def parse_fence_info(info: str) -> Dict[str, object]:
    """Parse a fenced-code-block info string into language / filename /
    highlight_lines components.

    Recognised forms:

    * ``ts``                                 → language only
    * ``ts [nuxt.config.ts]``                → language + filename
    * ``ts [nuxt.config.ts]{4-5,7}``         → language + filename + highlights
    * ``{1,3-5}``                            → highlights only
    """
    out: Dict[str, object] = {"language": "", "filename": None, "highlight_lines": []}
    s = info.strip()
    if not s:
        return out

    m = re.match(
        r"^(?P<lang>[^\s\[{]*)"
        r"(?:\s*\[(?P<file>[^\]]*)\])?"
        r"(?:\s*\{(?P<lines>[^}]*)\})?",
        s,
    )
    if not m:
        return out

    out["language"] = m.group("lang") or ""
    out["filename"] = m.group("file") or None
    out["highlight_lines"] = parse_highlight_lines(m.group("lines") or "")
    return out


def parse_highlight_lines(s: str) -> list:
    """Parse ``"1,3-5,7"`` into ``[1, 3, 4, 5, 7]``. Robust against junk."""
    result = []
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, _, b = part.partition("-")
            try:
                result.extend(range(int(a), int(b) + 1))
            except ValueError:
                continue
        else:
            try:
                result.append(int(part))
            except ValueError:
                continue
    return result
