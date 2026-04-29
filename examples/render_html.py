"""
Server-side render of a small document, with the AST written to stdout for
inspection alongside the HTML output.
"""
import json

from markast import Parser


SAMPLE = """# Release notes — v2.0

:::warning title="Breaking changes"
The legacy `/api/v1/*` endpoints have been removed. Update your clients.
:::

## What's new

- :::badge label="new" color=green
  :::
  GraphQL endpoint at `/api/v2/graphql`.
- :::badge label="changed" color=blue
  :::
  Token expiry now defaults to 1 hour (was 24).

## Migration

```python
# before
from sdk_v1 import Client
# after
from sdk_v2 import Client
```

| Endpoint           | Status   |
|--------------------|:--------:|
| `/api/v1/login`    | removed  |
| `/api/v2/login`    | added    |
"""


def main() -> None:
    parser = Parser(transforms=["normalize", "slugify"])
    doc = parser.parse(SAMPLE)

    print("<!doctype html><html><body>")
    print(doc.to_html())
    print("</body></html>")

    if doc.warnings:
        print("\n<!-- warnings -->")
        for w in doc.warnings:
            print(f"<!-- [{w['code']}] {w['message']} -->")


if __name__ == "__main__":
    main()
