# 3. Widgets

Widgets are how markast carries rich, structured components through Markdown
and into the AST. A widget is announced in source like this:

````markdown
:::widget-name key="value" key2=value
Body content with full **markdown** support.

# slot-name
Content of an additional slot.
:::
````

…and it lands in the AST as:

```json
{
  "type":   "widget",
  "widget": "widget-name",
  "props":  { "key": "value", "key2": "value" },
  "slots":  {
    "default":   [ ...body... ],
    "slot-name": [ ...slot... ]
  }
}
```

## Built-in widgets

| Widget          | Purpose                                | Notable props                          |
|-----------------|----------------------------------------|----------------------------------------|
| `tip`           | Friendly callout                       | `title`, `icon`                        |
| `note`          | Neutral aside                          | `title`, `icon`                        |
| `info`          | Information callout                    | `title`, `icon`                        |
| `warning`       | Caution callout                        | `title`, `icon`                        |
| `caution`       | Stronger warning                       | `title`, `icon`                        |
| `danger`        | Destructive-action warning             | `title`, `icon`                        |
| `card`          | Container with header / body / footer  | `title`, `color`, `elevated`           |
| `video`         | Video embed                            | `src` (required), `poster`, `controls`, `autoplay`, `loop`, `muted`, `caption`, `width`, `height` |
| `code-group`    | Tabbed code blocks                     | `default_tab`                          |
| `code-collapse` | Collapsible block container            | `summary`, `open`                      |
| `tabs`          | Generic tabbed content                 | `default`, `vertical`                  |
| `steps`         | Numbered step list (each step = slot)  | `start`                                |
| `badge`         | Inline label/pill                      | `label` (required), `color`            |

Each is a thin subclass of `BaseWidget`; their source files in
`markast/widgets/builtin/` double as templates for your own widgets.

## Writing a custom widget

A minimal widget needs three things:

1. A unique `name`.
2. A `params` dict (can be empty).
3. Registration with a `Parser` (or with `default_registry` for global use).

```python
from markast import BaseWidget, Parser, WidgetParam


class CalloutWidget(BaseWidget):
    """A simple coloured callout."""

    name = "callout"
    params = {
        "level": WidgetParam(str, default="info",
                             choices=["info", "warn", "error"],
                             description="Callout severity"),
        "title": WidgetParam(str, default=None),
    }


parser = Parser(widgets=[CalloutWidget])
doc = parser.parse(""":::callout level=warn title="Heads up"
Something **important**.
:::""")

print(doc.to_html())
```

That's the whole contract. The base class handles:

* Parsing the header into typed props,
* Filling in defaults,
* Validating choices and emitting W004 diagnostics,
* Required-prop checks (W005),
* Rendering back to Markdown (`to_markdown` default),
* Rendering to HTML (`to_html` default).

You only override what you need.

## Slots

A widget body can be split into named slots using bare `# slot-name` H1
headings at the *root* level of the body:

````markdown
:::card title="Profile"
Some default body content.

# header
*Custom* header content.

# footer
A footer.
:::
````

For a widget to acknowledge the extra slot names, declare them on the class:

```python
class CardWidget(BaseWidget):
    name = "card"
    slots = ["header", "footer"]
    params = { "title": WidgetParam(str, default=None) }
```

If you want to accept *any* slot names (e.g. for `tabs` or `steps`), leave
`slots = []` — the parser still groups everything correctly; only the
Markdown roundtrip needs to know whether to enumerate explicit slots.

## Param types

`WidgetParam` accepts the following Python types and parses raw Markdown
header values accordingly:

| `type_`     | Markdown value     | Result |
|-------------|--------------------|--------|
| `str`       | `key=hi`           | `"hi"` |
| `str`       | `key="multi word"` | `"multi word"` |
| `int`       | `count=3`          | `3` |
| `float`     | `ratio=1.5`        | `1.5` |
| `bool`      | `autoplay=true`    | `True` (also accepts `1`, `yes`, `on`) |
| `list`      | `tags=a,b,c`       | `["a", "b", "c"]` |
| `list`      | `tags=[1,2,3]`     | `[1, 2, 3]` (JSON form) |
| `dict`      | `meta={"a":1}`     | `{"a": 1}` (JSON only) |
| `Enum`      | `level=high`       | the matching `Enum` member |

You can also supply a `validator=callable(value) -> Optional[str]` that
returns an error message for invalid values:

```python
WidgetParam(int, default=10,
            validator=lambda x: None if 1 <= x <= 100 else "must be 1..100")
```

## Custom rendering

The default `to_markdown` and `to_html` produce sensible output for most
widgets. Override either to take full control:

```python
class BadgeWidget(BaseWidget):
    name = "badge"
    params = {
        "label": WidgetParam(str, required=True),
        "color": WidgetParam(str, default="gray"),
    }

    def to_html(self, node, render_children):
        p = node["props"]
        return f'<span class="badge badge-{p["color"]}">{p["label"]}</span>'
```

`render_children` is a callable handed to your widget. Pass any list of
child nodes and you get back the rendered string in the renderer's target
format. Use it to render slot contents recursively:

```python
def to_html(self, node, render_children):
    body = render_children(node["slots"]["default"])
    return f'<aside class="callout">{body}</aside>'
```

## Registering widgets

Two patterns:

```python
# 1. Per-parser (recommended) — keeps state local.
from markast import Parser
parser = Parser(widgets=[MyWidget])

# 2. Globally on the default registry — then the top-level parse() works.
from markast.widgets import default_registry
default_registry.register(MyWidget)

from markast import parse
parse(":::my-widget\n...\n:::")
```

The second pattern is convenient for small scripts but means the widget is
visible everywhere in the process. Prefer pattern 1 for libraries and
servers.

## Schema introspection

`MyWidget.schema()` returns a dict you can use to drive auto-generated docs
or IDE hover tips:

```python
>>> CalloutWidget.schema()
{
  "name": "callout",
  "params": {
    "level": {"type": "str", "required": False, "default": "info",
              "description": "Callout severity",
              "choices": ["info", "warn", "error"]},
    "title": {"type": "str", "required": False}
  },
  "slots": ["default"],
  "doc": "A simple coloured callout."
}
```

Pair this with `markast.json_schema()` to produce a complete API description
for client codegen.
