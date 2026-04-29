"""Walker / Visitor / replace tests."""
from __future__ import annotations

from markast import NodeType as N
from markast import Visitor, find, find_all, parse, replace, walk


def test_walk_visits_every_node_in_order():
    doc = parse("# Hi\n\nA **bold** paragraph.")
    types = [n["type"] for n in walk(doc.root)]
    # Must include document, heading, text, paragraph, bold, etc.
    for expected in (N.DOCUMENT, N.HEADING, N.TEXT, N.PARAGRAPH, N.BOLD):
        assert expected in types


def test_find_returns_first_match():
    doc = parse("# A\n\n## B\n\n## C")
    h = find(doc.root, N.HEADING)
    assert h["children"][0]["value"] == "A"


def test_find_all_returns_all_matches():
    doc = parse("# A\n\n## B\n\n## C")
    headings = find_all(doc.root, N.HEADING)
    assert len(headings) == 3
    assert [h["children"][0]["value"] for h in headings] == ["A", "B", "C"]


def test_visitor_collects_results():
    class HeadingTitleVisitor(Visitor):
        def visit_heading(self, node):
            return node["children"][0]["value"]

    doc = parse("# A\n\n## B")
    titles = HeadingTitleVisitor().run(doc.root)
    assert titles == ["A", "B"]


def test_replace_strips_dividers():
    doc = parse("# A\n\n---\n\n# B")
    new = replace(doc.root, lambda n: None if n.get("type") == N.DIVIDER else n)
    assert all(n.get("type") != N.DIVIDER for n in walk(new))


def test_replace_with_new_node_walks_replacement():
    doc = parse("# A")
    new = replace(
        doc.root,
        lambda n: {"type": N.HEADING, "level": 2, "children": n.get("children", [])}
        if n.get("type") == N.HEADING else n,
    )
    h = find(new, N.HEADING)
    assert h["level"] == 2
