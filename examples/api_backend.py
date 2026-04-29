"""
Minimal FastAPI service that returns parsed AST as JSON.

Run::

    pip install fastapi uvicorn
    uvicorn examples.api_backend:app --reload

Then::

    curl localhost:8000/content/hello
    curl localhost:8000/content/hello?format=html
"""
from typing import Any, Dict

try:
    from fastapi import FastAPI, Query
except ImportError as exc:  # pragma: no cover
    raise SystemExit("This example needs FastAPI. Install it with `pip install fastapi uvicorn`.") from exc

from markast import Parser

# In a real app this would be your DB. Inline here for runnability.
CONTENT: Dict[str, str] = {
    "hello": """# Hello

A demo article with a **callout**:

:::tip
Press `?` for keyboard shortcuts.
:::
""",
    "release": """# v2.0

See the [release notes](https://example.com/v2).

:::warning
Breaking change in `/api/v1/login`.
:::
""",
}

parser = Parser(transforms=["normalize", "slugify", "toc"])
app = FastAPI()


@app.get("/content/{slug}")
def get_content(slug: str, format: str = Query("json", regex="^(json|html|markdown)$")) -> Any:
    if slug not in CONTENT:
        return {"error": "not found"}, 404

    doc = parser.parse(CONTENT[slug])

    if format == "html":
        return {"html": doc.to_html()}
    if format == "markdown":
        return {"markdown": doc.to_markdown()}

    return {
        "ast":      doc.to_dict(),
        "warnings": doc.warnings,
        "toc":      doc.meta.get("toc", []),
    }


@app.get("/widgets")
def list_widgets() -> Any:
    """Return the registered widgets and their schemas."""
    return {
        name: parser.registry.get(name).schema()
        for name in sorted(parser.registry.names())
    }
