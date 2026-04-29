# 8. Extending the parser

You've seen the high-level extension points already: widgets, transforms,
custom renderer subclasses. This chapter covers the deeper hooks for cases
where those aren't enough.

## Custom rules

A rule observes the tree being built and reports diagnostics. Subclass
`markast.rules.Rule` and override the methods you care about:

```python
from markast import Parser
from markast.rules import Diagnostic, Rule, Severity


class HeadingMustBeShort(Rule):
    """Flag headings whose plain text exceeds 60 characters."""

    name = "short-heading"

    def check_heading_children(self, children, level):
        text = "".join(c.get("value", "") for c in children
                       if c.get("type") == "text")
        if len(text) > 60:
            return [Diagnostic(
                code="X100",
                message=f"Heading too long ({len(text)} chars).",
                context=text[:40] + "…",
                severity=Severity.WARNING,
            )]
        return None


parser = Parser(rules=[HeadingMustBeShort])
```

Built-in rule codes (defined in `markast.rules.codes`):

| Code  | Trigger                                                      |
|-------|--------------------------------------------------------------|
| W001  | Image inside a heading                                       |
| W002  | Block element where inline is required                       |
| W003  | Unknown widget name                                          |
| W004  | Invalid widget prop value (wrong type / not in choices)      |
| W005  | Required widget prop missing                                 |
| W006  | Image inside a table cell                                    |
| W007  | Raw HTML block found (informational)                         |
| W008  | Footnote reference without a matching definition             |
| W009  | Widget nesting deeper than the configured limit              |

To **replace** the built-in rules entirely (e.g. for a strict mode), pass an
empty list and add yours:

```python
parser = Parser(rules=[HeadingMustBeShort])  # implicit: no built-ins
```

To **extend** the built-ins instead, include `BuiltinRules`:

```python
from markast.rules.builtin import BuiltinRules
parser = Parser(rules=[BuiltinRules(), HeadingMustBeShort()])
```

## Tweaking the parser config

`ParserConfig` is a frozen dataclass:

```python
from markast import Parser, ParserConfig

cfg = ParserConfig(
    features=("tables", "strikethrough", "footnotes"),  # no autolinks/tasklists
    diagnose_html_blocks=False,
    max_widget_depth=8,
)

parser = Parser(cfg)
```

Use `cfg.evolve(...)` to derive a new config from an existing one:

```python
strict = cfg.evolve(max_widget_depth=4)
```

## Replacing the tokenizer

Rare, but possible. `Parser` lazily constructs a `Tokenizer`; if you need a
different one (e.g. to inject extra `markdown-it-py` plugins), assign it
before the first parse:

```python
from markast import Parser
from markast.parser.tokenizer import Tokenizer
from mdit_py_plugins.deflist import deflist_plugin


class MyTokenizer(Tokenizer):
    def _build_markdown_it(self):
        md = super()._build_markdown_it()
        md.use(deflist_plugin)
        return md


parser = Parser()
parser._tokenizer = MyTokenizer(parser.config, parser.registry)
```

If you find yourself doing this, consider opening an issue — your use case
might be a sign that the feature should be a first-class config option.

## Generating a JSON Schema

```python
import json
from markast import json_schema

print(json.dumps(json_schema(), indent=2))
```

Drop the output into a JSON-Schema validator on the client to enforce
shape compatibility, or feed it into a code generator for typed models.

## Pattern: a per-tenant parser

A multi-tenant service may need different widget sets per tenant. Build a
parser cache keyed on tenant id:

```python
from functools import lru_cache
from markast import Parser
from markast.widgets import default_registry, WidgetRegistry


@lru_cache(maxsize=64)
def parser_for(tenant_id: str) -> Parser:
    registry = default_registry.clone()
    for cls in load_tenant_widgets(tenant_id):
        registry.register(cls)
    return Parser(registry=registry, transforms=["normalize", "slugify"])


def render(tenant_id: str, markdown: str):
    return parser_for(tenant_id).parse(markdown)
```

Each parser is independent — registry mutations on one don't affect others.

## Pattern: a strict authoring CI

Combine custom rules with `doc.has_errors` to fail a CI build on bad
content:

```python
from markast import Parser
from markast.rules import Diagnostic, Rule, Severity


class NoRawHtml(Rule):
    name = "no-raw-html"

    def check_html_block(self, value):
        return [Diagnostic(
            code="C001",
            message="Raw HTML is not allowed in this corpus.",
            severity=Severity.ERROR,
        )]


parser = Parser(rules=[NoRawHtml()])

doc = parser.parse(open("article.md").read())
if doc.has_errors:
    for w in doc.warnings:
        print(f"::error::[{w['code']}] {w['message']}")
    raise SystemExit(1)
```

## Where the source code lives

The library is small — under 2,000 lines of code. Reading it is the fastest
way to internalise the architecture:

```
markast/
├── ast/         types, factories, walker, schema export
├── parser/      tokenizer + builder (block / inline / widget / props)
├── render/      markdown + html
├── widgets/     base / registry / built-ins
├── rules/       diagnostic system + built-in rules
├── transforms/  normalize / slugify / toc / linkify / typography
├── config.py
├── document.py
├── parser_api.py
└── cli.py
```

Every file starts with a module docstring explaining what it does and why.
If you're stuck, start there.
