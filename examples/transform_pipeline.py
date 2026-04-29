"""
Apply a transform pipeline to add slug ids and a TOC.
"""
import json

from markast import Parser


SAMPLE = """# Quick start

A short intro.

## Installation

```bash
pip install markast
```

## Configuration

Default settings work well.

### Custom widgets

Register on a Parser instance.

### Custom transforms

See chapter 4.

## Troubleshooting

If something breaks, file a ticket.
"""


def main() -> None:
    parser = Parser(transforms=["normalize", "slugify", "toc"])
    doc = parser.parse(SAMPLE)

    print("=== Slugged headings ===")
    for n in doc.children:
        if n.get("type") == "heading":
            print(f"  h{n['level']}  {n.get('id', '<no id>'):<25}  "
                  f"{n['children'][0]['value']}")

    print("\n=== TOC tree ===")
    print(json.dumps(doc.meta.get("toc", []), indent=2))


if __name__ == "__main__":
    main()
