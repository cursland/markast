"""
:class:`Parser` — the high-level entry point.

A :class:`Parser` bundles a :class:`ParserConfig`, a :class:`WidgetRegistry`,
the rule list, and the transform pipeline. Construct one per configuration
profile you need (most apps need exactly one — and the top-level
:func:`markast.parse` shortcut handles that case for you).

The class is intentionally small — most logic lives in the dedicated
sub-modules (:mod:`markast.parser`, :mod:`markast.transforms`, …) and this is
just the orchestrator.
"""
from __future__ import annotations
from typing import List, Optional, Sequence, Type, Union

from .config import DEFAULT_CONFIG, ParserConfig
from .document import Document
from .exceptions import ConfigurationError
from .parser.builder import ASTBuilder
from .parser.tokenizer import Tokenizer
from .rules.base import Rule
from .rules.builtin import BuiltinRules
from .transforms import BUILTIN_TRANSFORMS
from .transforms.base import Transform, TransformPipeline
from .widgets.base import BaseWidget
from .widgets.registry import WidgetRegistry, default_registry


# Type alias used in the constructor signature.
TransformLike = Union[str, Transform, Type[Transform]]
RuleLike      = Union[Rule, Type[Rule]]


class Parser:
    """High-level Markdown → :class:`Document` parser.

    Parameters
    ----------
    config : ParserConfig, optional
        Tokeniser/diagnostic settings. Defaults to :data:`DEFAULT_CONFIG`.
    widgets : sequence of BaseWidget subclasses, optional
        Custom widgets to register on top of the default registry. To start
        from a clean registry, pass an explicit ``registry=WidgetRegistry()``.
    registry : WidgetRegistry, optional
        Replace the registry entirely. When given, ``widgets`` is registered
        on top of *this* registry rather than the default one.
    rules : list, optional
        Validation rules. Each item may be a :class:`Rule` instance or a
        subclass (will be instantiated). Defaults to ``[BuiltinRules()]``.
    transforms : list, optional
        Transform pipeline. Each item may be a string identifier (looked up
        in :data:`markast.transforms.BUILTIN_TRANSFORMS`), a :class:`Transform`
        instance, or a :class:`Transform` subclass.

    Example
    -------
    >>> from markast import Parser
    >>> from markast.widgets import BaseWidget, WidgetParam
    >>> class TaskWidget(BaseWidget):
    ...     name = "task"
    ...     params = {"id": WidgetParam(str, required=True)}
    >>> parser = Parser(widgets=[TaskWidget], transforms=["normalize", "slugify"])
    >>> doc = parser.parse("# Hi\\n\\n:::task id=t1\\nDo this\\n:::")
    >>> doc.to_html()
    """

    def __init__(
        self,
        config: Optional[ParserConfig] = None,
        *,
        widgets: Optional[Sequence[Type[BaseWidget]]] = None,
        registry: Optional[WidgetRegistry] = None,
        rules: Optional[Sequence[RuleLike]] = None,
        transforms: Optional[Sequence[TransformLike]] = None,
    ) -> None:
        self.config = config or DEFAULT_CONFIG

        # Registry: explicit > default-clone (so we don't mutate the shared one)
        self.registry = registry if registry is not None else default_registry.clone()
        if widgets:
            for w in widgets:
                self.registry.register(w)

        # Rules
        self.rules: List[Rule] = []
        if rules is None:
            self.rules.append(BuiltinRules())
        else:
            for r in rules:
                if isinstance(r, Rule):
                    self.rules.append(r)
                elif isinstance(r, type) and issubclass(r, Rule):
                    self.rules.append(r())
                else:
                    raise ConfigurationError(f"Invalid rule entry: {r!r}")

        # Transforms
        self.pipeline = TransformPipeline()
        if transforms:
            for t in transforms:
                self.pipeline.append(self._resolve_transform(t))

        # Tokenizer (built lazily so config changes after __init__ still work
        # through evolve()).
        self._tokenizer: Optional[Tokenizer] = None

    # ── Helpers ──────────────────────────────────────────────────────────────
    @staticmethod
    def _resolve_transform(t: TransformLike) -> Transform:
        if isinstance(t, str):
            cls = BUILTIN_TRANSFORMS.get(t)
            if cls is None:
                raise ConfigurationError(
                    f"Unknown transform '{t}'. "
                    f"Known: {sorted(BUILTIN_TRANSFORMS)}",
                )
            return cls()
        if isinstance(t, Transform):
            return t
        if isinstance(t, type) and issubclass(t, Transform):
            return t()
        raise ConfigurationError(f"Invalid transform entry: {t!r}")

    def _get_tokenizer(self) -> Tokenizer:
        if self._tokenizer is None:
            self._tokenizer = Tokenizer(self.config, self.registry)
        return self._tokenizer

    # ── Public API ───────────────────────────────────────────────────────────
    def parse(self, text: str) -> Document:
        """Parse Markdown text and return a :class:`Document`."""
        tokens = self._get_tokenizer().tokenize(text)
        builder = ASTBuilder(self.config, self.registry, self.rules)
        ast = builder.build(tokens)
        ast = self.pipeline.run(ast, self.config)
        return Document(ast, registry=self.registry)

    # ── Mutation helpers (return new Parser instances) ───────────────────────
    def with_widgets(self, *widgets: Type[BaseWidget]) -> "Parser":
        """Return a new parser with extra widgets registered."""
        new_registry = self.registry.clone()
        for w in widgets:
            new_registry.register(w)
        return Parser(
            self.config,
            registry=new_registry,
            rules=self.rules,
            transforms=list(self.pipeline._transforms),
        )

    def with_transforms(self, *transforms: TransformLike) -> "Parser":
        """Return a new parser with extra transforms appended."""
        new_pipeline_items = list(self.pipeline._transforms) + [
            self._resolve_transform(t) for t in transforms
        ]
        return Parser(
            self.config,
            registry=self.registry,
            rules=self.rules,
            transforms=new_pipeline_items,
        )

    def __repr__(self) -> str:
        return (f"<Parser config={self.config!r} "
                f"widgets={self.registry.names()} "
                f"rules={[r.name or type(r).__name__ for r in self.rules]} "
                f"transforms={self.pipeline.names()}>")
