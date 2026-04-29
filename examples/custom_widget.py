"""
Register a custom widget and use it.

Demonstrates:

* Subclassing :class:`markast.BaseWidget`.
* Declaring typed parameters with :class:`markast.WidgetParam`.
* Slot-aware widgets (header / default / footer).
* Custom HTML rendering.
"""
from markast import BaseWidget, Parser, WidgetParam


class ProductCardWidget(BaseWidget):
    """A product card with price, rating, and CTA slot.

    Markdown::

        :::product price=29.99 rating=4.5 currency=USD
        Body description with **markdown**.

        # cta
        [Buy now](https://shop.example.com/p/42)
        :::
    """

    name = "product"
    slots = ["cta"]
    params = {
        "price":    WidgetParam(float, required=True),
        "rating":   WidgetParam(float, default=0.0),
        "currency": WidgetParam(str, default="USD",
                                choices=["USD", "EUR", "GBP", "JPY"]),
        "stock":    WidgetParam(int, default=None),
    }

    def to_html(self, node, render_children):
        p = node["props"]
        slots = node["slots"]
        body = render_children(slots.get("default", []))
        cta = render_children(slots.get("cta", []))
        return (
            f'<article class="product">'
            f'<div class="product-body">{body}</div>'
            f'<div class="product-meta">'
              f'<span class="price">{p["currency"]} {p["price"]:.2f}</span>'
              f'<span class="rating">rating: {p["rating"]}</span>'
            f'</div>'
            f'<div class="product-cta">{cta}</div>'
            f'</article>'
        )


SAMPLE = """# Featured product

:::product price=29.99 rating=4.5 currency=USD stock=12

Top-quality, **hand-stitched** leather wallet. Holds 8 cards plus cash.

# cta
[Buy now](https://shop.example.com/p/42)

:::
"""


def main() -> None:
    parser = Parser(widgets=[ProductCardWidget])
    doc = parser.parse(SAMPLE)

    print("=== AST widget node ===")
    widget_node = next(n for n in doc.children if n.get("type") == "widget")
    import json
    print(json.dumps(widget_node, indent=2)[:500])

    print("\n=== HTML ===")
    print(doc.to_html())

    print("\n=== Schema introspection ===")
    print(json.dumps(ProductCardWidget.schema(), indent=2))


if __name__ == "__main__":
    main()
