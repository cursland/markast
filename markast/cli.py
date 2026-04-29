"""
``markast`` command-line interface.

Usage::

    markast parse INPUT [-f json|markdown|html] [-o OUTPUT] [--indent N]
    markast schema             # print the AST JSON-Schema
    markast widgets            # list registered widgets

Examples::

    markast parse README.md
    markast parse README.md -f html -o out.html
    cat note.md | markast parse -        # read from stdin
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from typing import IO, List, Optional

from . import (
    HTMLRenderer, MarkdownRenderer, Parser, default_registry, json_schema,
)


def _read_input(source: str) -> str:
    if source == "-":
        return sys.stdin.read()
    return Path(source).read_text(encoding="utf-8")


def _write_output(target: Optional[str], content: str) -> None:
    if not target or target == "-":
        sys.stdout.write(content)
        if not content.endswith("\n"):
            sys.stdout.write("\n")
        return
    Path(target).write_text(content, encoding="utf-8")


def cmd_parse(args: argparse.Namespace) -> int:
    text = _read_input(args.input)
    parser = Parser(transforms=args.transforms or None)
    doc = parser.parse(text)

    if args.format == "json":
        out = doc.to_json(indent=args.indent)
    elif args.format == "markdown":
        out = doc.to_markdown()
    elif args.format == "html":
        out = doc.to_html()
    else:  # pragma: no cover - argparse guards this
        out = ""

    _write_output(args.output, out)
    if args.warnings_to_stderr and doc.warnings:
        for w in doc.warnings:
            print(f"[{w.get('code', '?')}] {w.get('message', '')}", file=sys.stderr)
    return 0


def cmd_schema(args: argparse.Namespace) -> int:
    print(json.dumps(json_schema(), indent=2))
    return 0


def cmd_widgets(args: argparse.Namespace) -> int:
    for name in sorted(default_registry.names()):
        cls = default_registry.get(name)
        doc = (cls.__doc__ or "").strip().split("\n", 1)[0] if cls else ""
        print(f"{name:20s} {doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="markast",
        description="Parse Markdown into a structured AST and render it.",
    )
    sub = p.add_subparsers(dest="command", required=True)

    parse_p = sub.add_parser("parse", help="Parse markdown and emit an AST or rendered text.")
    parse_p.add_argument("input", help="Path to a markdown file, or '-' for stdin.")
    parse_p.add_argument("-o", "--output", help="Output path (default: stdout).")
    parse_p.add_argument(
        "-f", "--format",
        choices=("json", "markdown", "html"),
        default="json",
        help="Output format.",
    )
    parse_p.add_argument("--indent", type=int, default=2, help="JSON indent (default 2).")
    parse_p.add_argument(
        "-t", "--transform",
        dest="transforms",
        action="append",
        help="Transform to apply (can be repeated). Built-ins: normalize, "
             "slugify, toc, linkify, smarttypography.",
    )
    parse_p.add_argument(
        "--warnings-to-stderr",
        action="store_true",
        help="Print parse diagnostics to stderr.",
    )
    parse_p.set_defaults(func=cmd_parse)

    schema_p = sub.add_parser("schema", help="Print the AST JSON-Schema.")
    schema_p.set_defaults(func=cmd_schema)

    widgets_p = sub.add_parser("widgets", help="List built-in widgets.")
    widgets_p.set_defaults(func=cmd_widgets)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
