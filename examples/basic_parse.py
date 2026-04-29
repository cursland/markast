"""
Smallest possible markast example: parse markdown, print every output format.

Run::

    python examples/basic_parse.py
"""
from markast import parse


SAMPLE = """# Welcome to markast

A paragraph with **bold**, *italic*, ~~strikethrough~~, and a
[link](https://example.com).

- a tasklist
- [x] item done
- [ ] item pending

```python
from markast import parse
print(parse("# Hi").to_html())
```

:::tip title="First steps"
Try the other examples in this folder next.
:::
"""


def main() -> None:
    doc = parse(SAMPLE)

    print("=== Top-level node types ===")
    for node in doc.children:
        print(f"  {node['type']}")

    print("\n=== Diagnostics ===")
    if doc.warnings:
        for w in doc.warnings:
            print(f"  [{w['code']}] {w['message']}")
    else:
        print("  (none)")

    print("\n=== Markdown roundtrip (first 240 chars) ===")
    print(doc.to_markdown()[:240])

    print("\n=== HTML (first 240 chars) ===")
    print(doc.to_html()[:240])

    print("\n=== JSON (first 200 chars) ===")
    print(doc.to_json()[:200])


if __name__ == "__main__":
    main()
