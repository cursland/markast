"""
Build script for the markast docs site.

Generates 9 pages × 2 languages from a single template + content blocks.
Run once to (re)build all en/*.html and es/*.html. The generated files are
checked into the docs branch — GitHub Pages serves them directly.

Not part of the published library. Lives here only to make doc edits easier.
"""
from __future__ import annotations
import re
import textwrap
from pathlib import Path
from dataclasses import dataclass


ROOT = Path(__file__).parent


# ─── Site structure ─────────────────────────────────────────────────────────

SECTIONS = {
    "en": [
        ("Documentation", [
            ("index.html",            "Overview"),
            ("getting-started.html",  "Getting started"),
            ("ast-reference.html",    "AST reference"),
        ]),
        ("Concepts", [
            ("widgets.html",          "Widgets"),
            ("transforms.html",       "Transforms"),
            ("renderers.html",        "Renderers"),
            ("walker.html",           "Walker & utilities"),
        ]),
        ("Integration", [
            ("client-integration.html", "Client integration"),
            ("extending.html",          "Extending"),
        ]),
    ],
    "es": [
        ("Documentación", [
            ("index.html",            "Vista general"),
            ("getting-started.html",  "Primeros pasos"),
            ("ast-reference.html",    "Referencia del AST"),
        ]),
        ("Conceptos", [
            ("widgets.html",          "Widgets"),
            ("transforms.html",       "Transformaciones"),
            ("renderers.html",        "Renderers"),
            ("walker.html",           "Walker y utilidades"),
        ]),
        ("Integración", [
            ("client-integration.html", "Integración con clientes"),
            ("extending.html",          "Extender la librería"),
        ]),
    ],
}

# Page order (used for prev/next nav)
PAGE_ORDER = [
    "index.html",
    "getting-started.html",
    "ast-reference.html",
    "widgets.html",
    "transforms.html",
    "renderers.html",
    "walker.html",
    "client-integration.html",
    "extending.html",
]


I18N = {
    "en": {
        "menu":      "Menu",
        "es":        "Spanish",
        "en":        "English",
        "toc":       "On this page",
        "github":    "GitHub",
        "previous":  "Previous",
        "next":      "Next",
        "theme":     "Toggle dark mode",
    },
    "es": {
        "menu":      "Menú",
        "es":        "Español",
        "en":        "Inglés",
        "toc":       "En esta página",
        "github":    "GitHub",
        "previous":  "Anterior",
        "next":      "Siguiente",
        "theme":     "Cambiar a modo oscuro",
    },
}


# ─── Content blocks (per page, per language) ───────────────────────────────
@dataclass
class Page:
    slug: str
    title: dict      # {"en": "...", "es": "..."}
    content: dict    # {"en": "<html>", "es": "<html>"}


PAGES: dict[str, Page] = {}


def page(slug, title_en, title_es, content_en, content_es):
    PAGES[slug] = Page(slug, {"en": title_en, "es": title_es},
                       {"en": content_en, "es": content_es})


# ─── HTML helpers ───────────────────────────────────────────────────────────
def render_layout(lang, page_slug, page_title, body_html):
    """Render a complete page (nav + sidebar + content)."""
    other_lang = "es" if lang == "en" else "en"
    t = I18N[lang]

    # Sidebar
    sidebar_html = []
    for section_title, items in SECTIONS[lang]:
        sidebar_html.append(f'<h4>{section_title}</h4>')
        for href, label in items:
            sidebar_html.append(f'<a href="./{href}">{label}</a>')
    sidebar = "\n".join(sidebar_html)

    # Prev / next
    idx = PAGE_ORDER.index(page_slug) if page_slug in PAGE_ORDER else 0
    prev_slug = PAGE_ORDER[idx - 1] if idx > 0 else None
    next_slug = PAGE_ORDER[idx + 1] if idx < len(PAGE_ORDER) - 1 else None
    prev_title = next((lab for s, items in SECTIONS[lang] for h, lab in items if h == prev_slug), "") if prev_slug else ""
    next_title = next((lab for s, items in SECTIONS[lang] for h, lab in items if h == next_slug), "") if next_slug else ""

    prev_a = f'<a href="./{prev_slug}" class="footer-prev">{prev_title}</a>' if prev_slug else "<span></span>"
    next_a = f'<a href="./{next_slug}" class="footer-next">{next_title}</a>' if next_slug else "<span></span>"

    return textwrap.dedent(f"""\
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{page_title} — markast</title>
        <link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
        <link rel="stylesheet" href="../assets/main.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism.min.css">
    </head>
    <body>

    <nav class="nav">
        <button class="nav-toggle" aria-label="{t['menu']}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>
        </button>
        <a class="nav-brand" href="./index.html">
            <img class="nav-brand-mark" src="../assets/favicon.svg" alt="" aria-hidden="true">
            markast <small>v1.0</small>
        </a>
        <span class="nav-spacer"></span>
        <div class="nav-actions">
            <a class="nav-btn" href="../{other_lang}/{page_slug}" data-lang="{other_lang}" title="{t[other_lang]}">{other_lang.upper()}</a>
            <a class="nav-btn" href="./{page_slug}" data-lang="{lang}" aria-pressed="true" title="{t[lang]}">{lang.upper()}</a>
            <button class="nav-btn" data-theme-toggle aria-label="{t['theme']}" aria-pressed="false">
                <span class="icon-sun" style="display:inline">☀</span>
                <span class="icon-moon" style="display:none">☾</span>
            </button>
            <a class="nav-btn" href="https://github.com/cursland/markast" title="{t['github']}">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5C5.7.5.5 5.7.5 12c0 5.1 3.3 9.4 7.8 10.9.6.1.8-.2.8-.6v-2c-3.2.7-3.9-1.5-3.9-1.5-.5-1.3-1.3-1.7-1.3-1.7-1.1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.7 1.3 3.4 1 .1-.8.4-1.3.7-1.6-2.6-.3-5.3-1.3-5.3-5.7 0-1.3.5-2.3 1.2-3.1-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.2 1.2.9-.3 1.9-.4 3-.4s2 .1 3 .4c2.2-1.5 3.2-1.2 3.2-1.2.6 1.6.2 2.9.1 3.2.7.8 1.2 1.8 1.2 3.1 0 4.4-2.7 5.4-5.3 5.7.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6 4.5-1.5 7.8-5.8 7.8-10.9C23.5 5.7 18.3.5 12 .5z"/></svg>
            </a>
        </div>
    </nav>
    <div class="sidebar-backdrop"></div>

    <div class="shell">
        <aside class="sidebar">
    {textwrap.indent(sidebar, '        ')}
        </aside>

        <main class="main">
            <article class="content">
    {body_html.strip()}
                <div class="page-footer">
                    {prev_a}
                    {next_a}
                </div>
            </article>
        </main>

        <aside class="toc">
            <h5>{t['toc']}</h5>
            <nav class="toc-list"></nav>
        </aside>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
    <script src="../assets/main.js"></script>

    </body>
    </html>
    """)


def build():
    for slug, p in PAGES.items():
        for lang in ("en", "es"):
            html = render_layout(lang, slug, p.title[lang], p.content[lang])
            (ROOT / lang / slug).write_text(html, encoding="utf-8")
            print(f"  wrote {lang}/{slug}")


# ─── Page content (imported from a sibling module so this file stays small) ──
if __name__ == "__main__":
    import _content   # populates PAGES via page(...) calls
    _content.register(page)
    build()
    print(f"\nGenerated {len(PAGES)} pages × 2 languages = {len(PAGES) * 2} files.")
