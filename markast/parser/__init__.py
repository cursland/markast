"""
markast.parser
────────────
Markdown text → AST tree.

The pipeline is::

    text  ──tokenize──▶  markdown-it tokens  ──build──▶  AST dict

split into:

* :mod:`markast.parser.tokenizer` — caches a :class:`MarkdownIt` instance per
  parser config and ensures every widget name appears as a registered
  container.
* :mod:`markast.parser.builder`   — walks the token stream and emits AST nodes,
  applying each registered :class:`Rule` along the way.
* :mod:`markast.parser.props`     — parses ``key="value"`` widget headers.
* :mod:`markast.parser.inline`    — inline-token → inline-node converter.

The public class :class:`markast.Parser` (defined in :mod:`markast.parser_api` and
re-exported at the package root) ties everything together.
"""
from .tokenizer import Tokenizer
from .builder import ASTBuilder

__all__ = ["Tokenizer", "ASTBuilder"]
