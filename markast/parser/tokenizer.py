"""
Tokenizer — wraps :mod:`markdown-it-py`.

Each :class:`Tokenizer` caches a :class:`MarkdownIt` instance configured for
its parser's feature set, so a long-running server doesn't rebuild the
underlying parser on every request. New widget names that appear in source
text are registered as containers on the fly so unknown widgets still produce
proper container tokens (and a W003 diagnostic) instead of being silently
swallowed.
"""
from __future__ import annotations
import re
from typing import Set
from markdown_it import MarkdownIt
from mdit_py_plugins.container import container_plugin

from ..config import ParserConfig
from ..widgets.registry import WidgetRegistry


_WIDGET_NAME_RE = re.compile(r"^:{3,}\s*([\w][\w-]*)", re.MULTILINE)


def _scan_widget_names(text: str) -> Set[str]:
    """Find every ``:::name`` pattern at the start of a line."""
    return set(_WIDGET_NAME_RE.findall(text))


class Tokenizer:
    """Holds a configured :class:`MarkdownIt` instance and the set of widget
    container names it has already registered.

    Each :class:`Parser` owns one. Tokenizers are cheap to create but not
    free, so a parser that handles many documents reuses the same one.
    """

    def __init__(self, config: ParserConfig, registry: WidgetRegistry) -> None:
        self._config = config
        self._registry = registry
        self._md = self._build_markdown_it()
        self._registered: Set[str] = set()
        self._register_known_widgets()

    # ── Construction ─────────────────────────────────────────────────────────
    def _build_markdown_it(self) -> MarkdownIt:
        md = MarkdownIt("commonmark", {"typographer": "smartquotes" in self._config.features})

        feat = set(self._config.features)
        if "tables" in feat:
            md.enable("table")
        if "strikethrough" in feat:
            try:
                md.enable("strikethrough")
            except Exception:
                pass
        if "autolinks" in feat:
            # markdown-it's "linkify" rule needs the optional ``linkify-it-py``
            # runtime. We try to import it before enabling the rule so that a
            # missing optional dep degrades silently instead of crashing every
            # parse call.
            try:
                import linkify_it  # noqa: F401
                md.enable("linkify")
                md.options["linkify"] = True
            except ImportError:
                pass
        if "tasklists" in feat:
            try:
                from mdit_py_plugins.tasklists import tasklists_plugin
                md.use(tasklists_plugin)
            except ImportError:
                pass
        if "footnotes" in feat:
            try:
                from mdit_py_plugins.footnote import footnote_plugin
                md.use(footnote_plugin)
            except ImportError:
                pass

        return md

    # ── Widget container registration ────────────────────────────────────────
    def _register_known_widgets(self) -> None:
        for name in self._registry.names():
            if name not in self._registered:
                self._md.use(container_plugin, name=name)
                self._registered.add(name)

    def _register_unknown(self, text: str) -> None:
        """Register any widget names we see in the source even if they are
        not in the registry — that way the builder receives proper container
        tokens and can emit W003 instead of silently dropping content."""
        for name in _scan_widget_names(text):
            if name not in self._registered:
                self._md.use(container_plugin, name=name)
                self._registered.add(name)

    # ── Public API ───────────────────────────────────────────────────────────
    def tokenize(self, text: str) -> list:
        """Tokenize markdown text. Returns a flat token list."""
        # Re-sync if the registry was mutated after construction.
        self._register_known_widgets()
        self._register_unknown(text)
        return self._md.parse(text)

    @property
    def md(self) -> MarkdownIt:
        return self._md
