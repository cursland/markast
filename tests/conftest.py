"""Shared fixtures.

Adds the repo root to ``sys.path`` so the test suite runs without the package
being installed. Real installs use the ``pip install -e .`` development mode
and don't need this — but it keeps the README's "clone and run pytest"
workflow honest.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


import pytest
from markast import Parser, default_registry


@pytest.fixture
def parser():
    """A fresh :class:`Parser` with the default config and built-in widgets."""
    return Parser()


@pytest.fixture
def empty_parser():
    """A parser with an empty registry (no built-in widgets)."""
    from markast.widgets import WidgetRegistry
    return Parser(registry=WidgetRegistry())
