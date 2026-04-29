"""Diagnostic rules — both built-in and custom."""
from __future__ import annotations

from markast import Parser, parse
from markast.rules import Diagnostic, Rule, Severity
from markast.rules.codes import (
    W_BLOCK_IN_INLINE, W_HTML_BLOCK, W_IMAGE_IN_HEADING, W_IMAGE_IN_TABLE,
    W_INVALID_PROP, W_MISSING_PROP, W_UNKNOWN_WIDGET,
)


def test_image_in_heading_warns():
    doc = parse("# ![alt](x.png)")
    assert doc.has_warnings(W_IMAGE_IN_HEADING)


def test_image_in_table_warns():
    md = "| A |\n|---|\n| ![z](x.png) |"
    doc = parse(md)
    assert doc.has_warnings(W_IMAGE_IN_TABLE)


def test_html_block_emits_info():
    doc = parse("<div>raw</div>")
    assert doc.has_warnings(W_HTML_BLOCK)
    diag = next(w for w in doc.warnings if w["code"] == W_HTML_BLOCK)
    # severity=info is dropped from on-the-wire dict, so absence == info.
    assert diag.get("severity", "info") == "info"


def test_unknown_widget_warns():
    doc = parse(":::nope\nhi\n:::")
    assert doc.has_warnings(W_UNKNOWN_WIDGET)


def test_missing_required_prop_warns():
    doc = parse(":::video\n:::")
    assert doc.has_warnings(W_MISSING_PROP)


def test_invalid_choice_warns():
    doc = parse(":::badge label=hi color=neon\n:::")
    assert doc.has_warnings(W_INVALID_PROP)


def test_disable_html_diagnostic():
    from markast import ParserConfig
    parser = Parser(config=ParserConfig(diagnose_html_blocks=False))
    doc = parser.parse("<div>raw</div>")
    assert not doc.has_warnings(W_HTML_BLOCK)


def test_custom_rule_runs_and_emits():
    class HeadingMustBeShort(Rule):
        name = "short-heading"

        def check_heading_children(self, children, level):
            text = "".join(c.get("value", "") for c in children
                           if c.get("type") == "text")
            if len(text) > 30:
                return [Diagnostic(
                    code="X100",
                    message="Heading too long.",
                    severity=Severity.WARNING,
                )]
            return None

    parser = Parser(rules=[HeadingMustBeShort])
    doc = parser.parse("# This heading exceeds the configured maximum length")
    assert any(w["code"] == "X100" for w in doc.warnings)
