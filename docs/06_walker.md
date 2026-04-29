# 6. Walker & utilities

The `markast.ast` package exposes traversal primitives so you can inspect or
rewrite the tree without writing recursion against every container shape.

## `walk(node)` — generator

```python
from markast import parse, walk

doc = parse("# Hi\n\nA **bold** word.")
for node in walk(doc.root):
    print(node["type"])
# document
# heading
# text
# paragraph
# text
# bold
# text
```

The walker visits nodes in **document order** (depth-first, pre-order). It
follows every container key (`children`, `slots`, `head`, `body`, `rows`,
`cells`), so widgets and tables aren't skipped.

`walk(node, include_root=False)` skips the starting node and only yields
descendants.

## `find(node, type_)` and `find_all(node, type_)`

```python
from markast import find, find_all, parse

doc = parse("# A\n\n## B\n\n## C")
print(find(doc.root, "heading")["children"][0]["value"])      # A
print([h["children"][0]["value"] for h in find_all(doc.root, "heading")])
# ["A", "B", "C"]
```

Both accept a string type or a list of types:

```python
find_all(doc.root, ["link", "inline_image"])
```

## `Visitor` — class-based dispatch

```python
from markast import Visitor, parse


class HeadingCollector(Visitor):
    def __init__(self):
        self.headings = []

    def visit_heading(self, node):
        self.headings.append(node)


v = HeadingCollector()
v.run(parse("# A\n\n## B"))
print(len(v.headings))  # 2
```

Override `visit_<node_type>` for any node you want to react to. Methods may
return a value, which `run()` collects into a list — useful for extracting
data without writing an accumulator yourself.

## `replace(node, fn)` — functional rewrite

`replace` walks the tree and applies `fn` to every node, substituting each
with whatever `fn` returns. Returning `None` *removes* the node (when its
parent stores it in a list).

```python
from markast import NodeType, parse, replace

doc = parse("# Title\n\n---\n\nBody.")
trimmed = replace(doc.root, lambda n: None if n.get("type") == NodeType.DIVIDER else n)
```

Returning a brand-new node is fine — the walker continues into the
*replacement's* children, not the original's. This makes one-pass rewrites
trivial:

```python
def lowercase_text(node):
    if node.get("type") == "text":
        return {"type": "text", "value": node["value"].lower()}
    return node


lowered = replace(doc.root, lowercase_text)
```

Pass `in_place=True` to mutate the existing dict tree if you need to keep
object identity (e.g. external references into the AST). Otherwise, the
default behaviour is to return a fresh tree.

## `extract_text(node)`

Shortcut for "give me the plain-text projection of this subtree":

```python
from markast import extract_text, parse

doc = parse("# Hello **world**")
print(extract_text(doc.children[0]))
# "Hello world"
```

It walks `children`, `slots`, and table rows/cells, so widgets and tables
contribute their textual content too.

## `count_nodes(node)`

```python
from markast import count_nodes, parse

doc = parse("# A\n\n## B\n\n- x\n- y")
print(count_nodes(doc.root))
# {'document': 1, 'heading': 2, 'text': 4, 'list': 1, 'list_item': 2, ...}
```

Handy for tests and content analytics.

## When to use which?

| Goal                              | Use |
|-----------------------------------|-----|
| Iterate every node, do something  | `walk` |
| Find the first / all of a kind    | `find` / `find_all` |
| Extract data into a list          | `Visitor` |
| Mutate a copy of the tree         | `replace` |
| Mutate in place (advanced)        | `replace(..., in_place=True)` |
| Get plain text                    | `extract_text` |
| Tally node types                  | `count_nodes` |

A correct mental model: *the AST is just dicts*. The walker is the only
non-trivial part of using it; everything else is dictionary manipulation.
