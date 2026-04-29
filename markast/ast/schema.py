"""
JSON-Schema export for the AST shape.

Why?
----
Clients written in other languages (Dart, TypeScript, Go) often want a single
source of truth that describes the JSON they will receive. Generating a JSON
Schema from the library guarantees the description never drifts from the
implementation.

The schema is intentionally permissive: ``children`` is ``array of node`` not
a strict union, because most generators choke on deep recursive unions and the
discriminator (``type``) is what clients actually switch on.

Use::

    from markast import json_schema
    import json
    print(json.dumps(json_schema(), indent=2))
"""
from __future__ import annotations
from typing import Any, Dict

from . import types as T


def json_schema() -> Dict[str, Any]:
    """Return a JSON-Schema dict describing the AST root and node shapes."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:cursland:markast:schema:document",
        "title": "markast Document",
        "type": "object",
        "required": ["type", "version", "warnings", "children"],
        "properties": {
            "type": {"const": T.DOCUMENT},
            "version": {"type": "string"},
            "warnings": {
                "type": "array",
                "items": {"$ref": "#/$defs/Warning"},
            },
            "children": {
                "type": "array",
                "items": {"$ref": "#/$defs/Node"},
            },
            "meta": {"type": "object"},
        },
        "$defs": {
            "Warning": {
                "type": "object",
                "required": ["code", "message", "context"],
                "properties": {
                    "code": {"type": "string"},
                    "message": {"type": "string"},
                    "context": {"type": "string"},
                    "severity": {"enum": ["error", "warning", "info"]},
                },
            },
            "Node": {
                "type": "object",
                "required": ["type"],
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": sorted(T.BLOCK_TYPES | T.INLINE_TYPES),
                    },
                },
                "additionalProperties": True,
            },
        },
    }
