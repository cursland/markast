"""Widget system tests — built-ins, registration, props, slots."""
from __future__ import annotations
import pytest

from markast import (
    BaseWidget, NodeType as N, Parser, WidgetParam, WidgetRegistry, parse,
)


def widget_node(doc):
    return next(c for c in doc.children if c["type"] == N.WIDGET)


# ── Built-in admonitions ─────────────────────────────────────────────────────
@pytest.mark.parametrize("flavour", ["tip", "note", "info", "warning", "caution", "danger"])
def test_admonition_basic(flavour):
    doc = parse(f":::{flavour}\nhello\n:::")
    w = widget_node(doc)
    assert w["widget"] == flavour


def test_admonition_with_title():
    doc = parse(':::tip title="Pro tip"\nbody\n:::')
    assert widget_node(doc)["props"]["title"] == "Pro tip"


def test_admonition_positional_title():
    """Bare leading text becomes ``title``."""
    doc = parse(":::warning Heads up everyone\nbody\n:::")
    assert "Heads up" in widget_node(doc)["props"]["title"]


# ── Card with named slots ────────────────────────────────────────────────────
def test_card_default_slot():
    doc = parse(':::card title="Hi"\nbody\n:::')
    w = widget_node(doc)
    assert w["props"]["title"] == "Hi"
    assert w["slots"]["default"]


def test_card_footer_slot():
    md = """:::card title="Hi"
body

# footer
footer text
:::"""
    w = widget_node(parse(md))
    assert w["slots"]["footer"]


# ── Video — typed props ──────────────────────────────────────────────────────
def test_video_required_src():
    w = widget_node(parse(':::video src="v.mp4"\n:::'))
    assert w["props"]["src"] == "v.mp4"


def test_video_bool_props():
    w = widget_node(parse(':::video src="v.mp4" autoplay=true controls=false\n:::'))
    assert w["props"]["autoplay"] is True
    assert w["props"]["controls"] is False


def test_video_missing_required_warns():
    doc = parse(':::video\n:::')
    assert doc.has_warnings("W005")


# ── code-group ───────────────────────────────────────────────────────────────
def test_code_group_filenames():
    md = """:::code-group
```bash [npm]
npm i
```

```bash [yarn]
yarn add
```
:::"""
    w = widget_node(parse(md))
    assert w["widget"] == "code-group"
    blocks = w["slots"]["default"]
    assert blocks[0]["filename"] == "npm"
    assert blocks[1]["filename"] == "yarn"


# ── Unknown widgets warn but don't crash ────────────────────────────────────
def test_unknown_widget_warns():
    doc = parse(":::not-a-real-widget\nhi\n:::")
    assert doc.has_warnings("W003")


# ── Custom widget registration via Parser ───────────────────────────────────
def test_custom_widget_via_parser():
    class TaskWidget(BaseWidget):
        name = "task"
        params = {
            "id": WidgetParam(str, required=True),
            "priority": WidgetParam(str, default="normal",
                                    choices=["low", "normal", "high"]),
        }

    parser = Parser(widgets=[TaskWidget])
    doc = parser.parse(':::task id="t1" priority=high\nbody\n:::')
    w = next(c for c in doc.children if c["type"] == N.WIDGET)
    assert w["widget"] == "task"
    assert w["props"]["id"] == "t1"
    assert w["props"]["priority"] == "high"


def test_custom_widget_invalid_choice_warns():
    class StatusWidget(BaseWidget):
        name = "status"
        params = {"level": WidgetParam(str, default="ok",
                                       choices=["ok", "warn", "error"])}

    parser = Parser(widgets=[StatusWidget])
    doc = parser.parse(":::status level=bogus\n:::")
    assert doc.has_warnings("W004")


# ── Registry isolation ───────────────────────────────────────────────────────
def test_per_parser_registry_isolation():
    """Registering on one Parser must not leak to another."""
    class FooWidget(BaseWidget):
        name = "foo"
        params = {}

    p1 = Parser(widgets=[FooWidget])
    p2 = Parser()  # fresh clone of default registry
    assert "foo" in p1.registry
    assert "foo" not in p2.registry


# ── Empty registry, nothing built-in is recognised ───────────────────────────
def test_empty_registry_warns_on_admonition():
    parser = Parser(registry=WidgetRegistry())
    doc = parser.parse(":::tip\nbody\n:::")
    assert doc.has_warnings("W003")
