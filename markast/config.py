"""
:class:`ParserConfig` — every option that influences how markast parses input.

The config is a frozen dataclass. Construct it explicitly when you need
non-default behaviour, or pass equivalent kwargs to :class:`markast.Parser`
which builds one for you.

Defaults are tuned for typical structured-content authoring:

* CommonMark + GFM tables / strikethrough / tasklists / autolinks.
* Footnotes enabled.
* Typographic substitutions (``"smartquotes"``) disabled — clients usually
  want exact author input.
* Widgets enabled with the default registry.
"""
from __future__ import annotations
from dataclasses import dataclass, field, replace
from typing import List, Optional, Sequence


@dataclass(frozen=True)
class ParserConfig:
    """Immutable configuration for a :class:`Parser`.

    Mutate via :meth:`evolve` (returns a new instance with overrides applied).
    """

    #: Markdown features to enable. The library translates these into
    #: ``markdown-it-py`` plugin activations:
    #:
    #:   * ``"tables"``        GFM tables
    #:   * ``"strikethrough"`` ``~~text~~``
    #:   * ``"tasklists"``     ``- [ ]`` / ``- [x]``
    #:   * ``"autolinks"``     bare URL detection (linkify)
    #:   * ``"footnotes"``     ``[^1]`` references and definitions
    #:   * ``"smartquotes"``   typographic quote conversion
    features: Sequence[str] = field(default_factory=lambda: (
        "tables", "strikethrough", "tasklists", "autolinks", "footnotes",
    ))

    #: When ``True``, emit a W007 diagnostic for any raw HTML block. Clients
    #: that *expect* HTML (e.g. embedding pre-rendered widgets) can disable
    #: the diagnostic without disabling the feature.
    diagnose_html_blocks: bool = True

    #: Maximum nesting depth for widget bodies. Beyond this, the W009
    #: diagnostic is emitted. ``0`` disables the check.
    max_widget_depth: int = 16

    #: When ``True`` (default), the renderer emits warnings to ``stderr`` for
    #: nodes it does not know how to render. Set to ``False`` for silent
    #: degradation (skip the node entirely).
    verbose_renderer: bool = False

    #: Default indent used by :meth:`Document.to_json`.
    json_indent: int = 2

    def evolve(self, **overrides) -> "ParserConfig":
        """Return a copy with the given fields replaced."""
        return replace(self, **overrides)


#: A frozen default config used when ``Parser()`` is constructed with no
#: arguments and by the top-level :func:`markast.parse` shortcut.
DEFAULT_CONFIG = ParserConfig()
