"""
Content blocks for every documentation page, in both languages.

Each entry is registered via ``page(slug, title_en, title_es, html_en, html_es)``
where the HTML strings are inserted into the shared layout. Keep them as
plain HTML — the build script does NOT process Markdown.
"""
from __future__ import annotations


# ─── Helper: wrap a hero block (used on the landing page) ───────────────────
def hero(title_html, sub_html, primary_label, primary_href, ghost_label, ghost_href):
    return f'''
<section class="hero">
    <h1 class="hero-title">{title_html}</h1>
    <p class="hero-sub">{sub_html}</p>
    <div class="hero-cta">
        <a class="btn btn-primary" href="{primary_href}">{primary_label}</a>
        <a class="btn btn-ghost" href="{ghost_href}">{ghost_label}</a>
    </div>
</section>
'''


def register(page):
    # ════════════════════════════════════════════════════════════════════════
    # 1. OVERVIEW (landing)
    # ════════════════════════════════════════════════════════════════════════
    page("index.html",
        "Overview", "Vista general",
        hero(
            'Markdown to a <span class="grad">typed AST</span><br>your front-end can render.',
            '<strong>markast</strong> parses Markdown into a typed, structured tree. '
            'Everything happens in the library — parsing, validation, traversal, rendering. '
            'Ship the JSON to any client and switch on <code>type</code>.',
            "Get started", "./getting-started.html",
            "View on GitHub", "https://github.com/cursland/markast",
        ) + '''
<h2>What you get</h2>

<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-card-icon">🌳</div>
        <h3>Typed AST</h3>
        <p>Every node has a <code>type</code> discriminator and known fields. Walk it, query it, mutate it — without writing a single regex.</p>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">🧱</div>
        <h3>Pluggable widgets</h3>
        <p>Author <code>:::widget</code> components in Markdown that survive into the AST as structured nodes with typed props and named slots.</p>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">🛡️</div>
        <h3>Never crashes</h3>
        <p>Bad input produces a diagnostic, not an exception. <code>parse</code> always returns a valid AST so your CMS keeps shipping.</p>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">🔀</div>
        <h3>Three output formats</h3>
        <p>Roundtrip back to Markdown, render to HTML server-side, or ship as JSON. Three single-method calls.</p>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">⚙️</div>
        <h3>Transform pipeline</h3>
        <p>Slugify headings, build a TOC, autolink URLs, normalise text spans — chain them, write your own.</p>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">🌐</div>
        <h3>Front-end agnostic</h3>
        <p>Native mobile, React/Vue/Svelte, terminal, plain HTML — anything that can <code>switch</code> on a string.</p>
    </div>
</div>

<h2>30-second tour</h2>

<pre><code class="language-bash">pip install markast</code></pre>

<pre><code class="language-python">from markast import parse

doc = parse("""
# Welcome

A paragraph with **bold** text and a [link](https://example.com).

:::tip title="Pro tip"
Markdown still works inside widgets.
:::
""")

doc.to_json()       # str — ship to any client
doc.to_markdown()   # str — roundtrip
doc.to_html()       # str — server-side render</code></pre>

<h2>Why a tree, not HTML?</h2>

<p>HTML is a one-way street. Once your content is rendered, the structure is gone — clients can't selectively style headings differently per platform, can't replace a <code>:::video</code> with a native player, can't extract a TOC without re-parsing. A typed AST keeps the meaning intact:</p>

<ul>
    <li>Mobile apps render headings with their own typography rules.</li>
    <li>The web renders <code>:::video</code> as a custom player; the terminal renders it as a link.</li>
    <li>Search indexes the same structured nodes that drive the UI.</li>
    <li>The same content powers a docs site, a CMS preview, and a CLI — without re-authoring.</li>
</ul>
''',
        hero(
            'Markdown a un <span class="grad">AST tipado</span><br>que cualquier front-end puede renderizar.',
            '<strong>markast</strong> convierte Markdown en un árbol estructurado y tipado. '
            'Todo ocurre dentro de la librería — parseo, validación, recorrido, render. '
            'Envías el JSON a cualquier cliente y haces <code>switch</code> sobre <code>type</code>.',
            "Empezar", "./getting-started.html",
            "Ver en GitHub", "https://github.com/cursland/markast",
        ) + '''
<h2>Qué obtienes</h2>

<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-card-icon">🌳</div>
        <h3>AST tipado</h3>
        <p>Cada nodo tiene un <code>type</code> discriminador y campos conocidos. Lo recorres, consultas y mutas sin escribir una sola regex.</p>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">🧱</div>
        <h3>Widgets enchufables</h3>
        <p>Escribe <code>:::widget</code> en Markdown y llegan al AST como nodos estructurados con props tipados y slots con nombre.</p>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">🛡️</div>
        <h3>Nunca crashea</h3>
        <p>El contenido inválido produce un diagnóstico, no una excepción. <code>parse</code> siempre devuelve un AST válido.</p>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">🔀</div>
        <h3>Tres formatos de salida</h3>
        <p>Roundtrip a Markdown, HTML para server-side, o JSON. Tres métodos de un solo paso.</p>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">⚙️</div>
        <h3>Pipeline de transformaciones</h3>
        <p>Slugs en headings, generar TOC, autolinks, normalizar texto. Encadenables; o escribe los tuyos.</p>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">🌐</div>
        <h3>Agnóstico al front-end</h3>
        <p>Móvil nativo, React/Vue/Svelte, terminal, HTML plano. Cualquier cosa que pueda hacer <code>switch</code> sobre un string.</p>
    </div>
</div>

<h2>Tour de 30 segundos</h2>

<pre><code class="language-bash">pip install markast</code></pre>

<pre><code class="language-python">from markast import parse

doc = parse("""
# Bienvenido

Un párrafo con **negrita** y un [enlace](https://example.com).

:::tip title="Consejo"
Markdown sigue funcionando dentro de los widgets.
:::
""")

doc.to_json()       # str — envíalo a cualquier cliente
doc.to_markdown()   # str — roundtrip
doc.to_html()       # str — render server-side</code></pre>

<h2>¿Por qué un árbol y no HTML?</h2>

<p>El HTML es de un solo sentido. Una vez que el contenido está renderizado, la estructura se pierde: los clientes no pueden estilar headings diferente según plataforma, no pueden reemplazar un <code>:::video</code> con un reproductor nativo, no pueden extraer un TOC sin volver a parsear. Un AST tipado preserva el significado:</p>

<ul>
    <li>Las apps móviles aplican sus propias reglas de tipografía a los headings.</li>
    <li>La web renderiza <code>:::video</code> con un player propio; la terminal lo muestra como un enlace.</li>
    <li>El buscador indexa los mismos nodos estructurados que pinta la UI.</li>
    <li>El mismo contenido alimenta el sitio de docs, el preview del CMS, y un CLI — sin reescribir.</li>
</ul>
''')

    # ════════════════════════════════════════════════════════════════════════
    # 2. GETTING STARTED
    # ════════════════════════════════════════════════════════════════════════
    page("getting-started.html",
        "Getting started", "Primeros pasos",
        # === EN ===
        '''
<h1>Getting started</h1>
<p class="lede">The shortest possible path from "I just installed markast" to "I'm shipping content to my client app." Everything here uses defaults; later chapters cover configuration.</p>

<h2>Install</h2>

<pre><code class="language-bash">pip install markast</code></pre>

<p>Optional extras:</p>

<ul>
    <li><code>pip install markast[test]</code> — pulls in <code>pytest</code> for running the test suite.</li>
    <li><code>pip install linkify-it-py</code> — required if you want bare-URL detection (the <code>autolinks</code> feature). Without it, that one feature is silently disabled — everything else still works.</li>
</ul>

<h2>Parse some Markdown</h2>

<pre><code class="language-python">from markast import parse

doc = parse("# Hello\\n\\nA paragraph with **bold** and a [link](https://example.com).")

print(doc.to_json(indent=2))</code></pre>

<p>Output (abbreviated):</p>

<pre><code class="language-json">{
  "type": "document",
  "version": "1.0",
  "warnings": [],
  "children": [
    { "type": "heading", "level": 1, "children": [
        { "type": "text", "value": "Hello" }
    ] },
    { "type": "paragraph", "children": [
        { "type": "text", "value": "A paragraph with " },
        { "type": "bold", "children": [
            { "type": "text", "value": "bold" }
        ] },
        { "type": "text", "value": " and a " },
        { "type": "link", "href": "https://example.com", "title": null,
          "children": [ { "type": "text", "value": "link" } ] },
        { "type": "text", "value": "." }
      ] }
  ]
}</code></pre>

<p>That's the entire API for the simplest case.</p>

<h2>Render</h2>

<p><code>parse()</code> returns a <code>Document</code>. The four operations you'll use most often:</p>

<pre><code class="language-python">doc.to_json(indent=2)   # str — the structured tree, for transport
doc.to_markdown()       # str — canonical Markdown, for editing UIs
doc.to_html()           # str — HTML, for server-side rendering
doc.to_dict()           # dict — the raw underlying tree</code></pre>

<h2>Inspect warnings</h2>

<p>The parser never raises on bad content. If something is invalid for client rendering (an image inside a heading, an unknown widget, …), it emits a <em>diagnostic</em>:</p>

<pre><code class="language-python">doc = parse("# ![alt](logo.png)")
for w in doc.warnings:
    print(w["code"], w["message"])
# W001  Image inside h1 heading — alt text used as content.</code></pre>

<div class="callout callout-tip">
    <div class="callout-icon">!</div>
    <div class="callout-body">
        <strong>Diagnostics never block parsing.</strong> Whatever is reported, you still get a valid AST you can ship. The full diagnostic catalogue lives in the <a href="./extending.html">Extending</a> chapter.
    </div>
</div>

<h2>Use a registered widget</h2>

<p>markast comes with several widgets pre-registered. The most common are admonitions:</p>

<pre><code class="language-python">from markast import parse

md = """
:::tip title="Pro tip"
You can nest **markdown** here.
:::
"""

doc = parse(md)
print(doc.to_html())
# &lt;aside class="admonition admonition-tip"&gt;&lt;header&gt;Pro tip&lt;/header&gt;
#   &lt;div class="admonition-body"&gt;&lt;p&gt;You can nest &lt;strong&gt;markdown&lt;/strong&gt; here.&lt;/p&gt;&lt;/div&gt;
# &lt;/aside&gt;</code></pre>

<p>Other built-ins: <code>note</code>, <code>info</code>, <code>warning</code>, <code>caution</code>, <code>danger</code>, <code>card</code>, <code>video</code>, <code>code-group</code>, <code>code-collapse</code>, <code>tabs</code>, <code>steps</code>, <code>badge</code>. Read on in the <a href="./widgets.html">Widgets</a> chapter for the full catalogue and how to write your own.</p>

<h2>Where to go next</h2>

<ul>
    <li><a href="./ast-reference.html">AST reference</a> — every node type and its fields.</li>
    <li><a href="./widgets.html">Widgets</a> — built-ins and custom widgets.</li>
    <li><a href="./client-integration.html">Client integration</a> — patterns for any front-end stack.</li>
</ul>
''',
        # === ES ===
        '''
<h1>Primeros pasos</h1>
<p class="lede">El camino más corto desde "acabo de instalar markast" hasta "estoy enviando contenido a mi cliente". Todo aquí usa los valores por defecto; los capítulos siguientes cubren la configuración.</p>

<h2>Instalación</h2>

<pre><code class="language-bash">pip install markast</code></pre>

<p>Extras opcionales:</p>

<ul>
    <li><code>pip install markast[test]</code> — añade <code>pytest</code> para correr la suite de tests.</li>
    <li><code>pip install linkify-it-py</code> — necesario si quieres detección automática de URLs (feature <code>autolinks</code>). Sin él, esa única feature se desactiva silenciosamente — el resto sigue funcionando.</li>
</ul>

<h2>Parsea Markdown</h2>

<pre><code class="language-python">from markast import parse

doc = parse("# Hola\\n\\nUn párrafo con **negrita** y un [enlace](https://example.com).")

print(doc.to_json(indent=2))</code></pre>

<p>Salida (abreviada):</p>

<pre><code class="language-json">{
  "type": "document",
  "version": "1.0",
  "warnings": [],
  "children": [
    { "type": "heading", "level": 1, "children": [
        { "type": "text", "value": "Hola" }
    ] },
    { "type": "paragraph", "children": [
        { "type": "text", "value": "Un párrafo con " },
        { "type": "bold", "children": [
            { "type": "text", "value": "negrita" }
        ] },
        { "type": "text", "value": " y un " },
        { "type": "link", "href": "https://example.com", "title": null,
          "children": [ { "type": "text", "value": "enlace" } ] },
        { "type": "text", "value": "." }
      ] }
  ]
}</code></pre>

<p>Esa es toda la API para el caso más simple.</p>

<h2>Render</h2>

<p><code>parse()</code> devuelve un <code>Document</code>. Las cuatro operaciones que usarás más:</p>

<pre><code class="language-python">doc.to_json(indent=2)   # str — el árbol estructurado, para transporte
doc.to_markdown()       # str — Markdown canónico, para UIs de edición
doc.to_html()           # str — HTML, para render server-side
doc.to_dict()           # dict — el árbol crudo subyacente</code></pre>

<h2>Inspeccionar warnings</h2>

<p>El parser nunca lanza excepciones por contenido inválido. Si algo no es válido para renderizar en el cliente (imagen dentro de heading, widget desconocido, …), emite un <em>diagnóstico</em>:</p>

<pre><code class="language-python">doc = parse("# ![alt](logo.png)")
for w in doc.warnings:
    print(w["code"], w["message"])
# W001  Image inside h1 heading — alt text used as content.</code></pre>

<div class="callout callout-tip">
    <div class="callout-icon">!</div>
    <div class="callout-body">
        <strong>Los diagnósticos nunca bloquean el parseo.</strong> Pase lo que pase, recibes un AST válido que puedes enviar. El catálogo completo está en el capítulo <a href="./extending.html">Extender la librería</a>.
    </div>
</div>

<h2>Usa un widget registrado</h2>

<p>markast trae varios widgets pre-registrados. Los más comunes son los admonitions:</p>

<pre><code class="language-python">from markast import parse

md = """
:::tip title="Consejo"
Puedes anidar **markdown** aquí.
:::
"""

doc = parse(md)
print(doc.to_html())
# &lt;aside class="admonition admonition-tip"&gt;&lt;header&gt;Consejo&lt;/header&gt;
#   &lt;div class="admonition-body"&gt;&lt;p&gt;Puedes anidar &lt;strong&gt;markdown&lt;/strong&gt; aquí.&lt;/p&gt;&lt;/div&gt;
# &lt;/aside&gt;</code></pre>

<p>Otros builtins: <code>note</code>, <code>info</code>, <code>warning</code>, <code>caution</code>, <code>danger</code>, <code>card</code>, <code>video</code>, <code>code-group</code>, <code>code-collapse</code>, <code>tabs</code>, <code>steps</code>, <code>badge</code>. Sigue en el capítulo <a href="./widgets.html">Widgets</a> para el catálogo completo y cómo escribir los tuyos.</p>

<h2>A dónde ir después</h2>

<ul>
    <li><a href="./ast-reference.html">Referencia del AST</a> — cada tipo de nodo y sus campos.</li>
    <li><a href="./widgets.html">Widgets</a> — builtins y widgets propios.</li>
    <li><a href="./client-integration.html">Integración con clientes</a> — patrones para cualquier stack de front-end.</li>
</ul>
''')

    # ════════════════════════════════════════════════════════════════════════
    # 3. AST REFERENCE
    # ════════════════════════════════════════════════════════════════════════
    page("ast-reference.html",
        "AST reference", "Referencia del AST",
        # === EN ===
        '''
<h1>AST reference</h1>
<p class="lede">Specification for every node type the parser can produce. Use this chapter when you write a client renderer.</p>

<h2>Document (root)</h2>

<pre><code class="language-json">{
  "type":     "document",
  "version":  "1.0",
  "warnings": [ {"code": "W001", "message": "...", "context": "..."} ],
  "children": [ /* block nodes */ ],
  "meta":     {}
}</code></pre>

<table>
    <thead><tr><th>Field</th><th>Type</th><th>Notes</th></tr></thead>
    <tbody>
    <tr><td><code>version</code></td><td>string</td><td>Bumped on breaking shape changes. Currently <code>"1.0"</code>.</td></tr>
    <tr><td><code>warnings</code></td><td>array</td><td>List of diagnostic dicts. Always present (may be empty).</td></tr>
    <tr><td><code>children</code></td><td>array</td><td>Block nodes. Always present (may be empty).</td></tr>
    <tr><td><code>meta</code></td><td>object</td><td>Open-ended bag for transforms (TOC, slug map, …). May be absent.</td></tr>
    </tbody>
</table>

<h2>Block nodes</h2>

<h3>heading</h3>
<pre><code class="language-json">{ "type": "heading", "level": 2, "children": [ /* inline */ ], "id": "section-id" }</code></pre>
<ul>
    <li><code>level</code> ∈ 1–6.</li>
    <li><code>id</code> is added by the <code>slugify</code> transform; absent otherwise.</li>
    <li>Inline children are restricted (rule W001). Images become alt text.</li>
</ul>

<h3>paragraph</h3>
<pre><code class="language-json">{ "type": "paragraph", "children": [ /* inline */ ] }</code></pre>

<h3>blockquote</h3>
<pre><code class="language-json">{ "type": "blockquote", "children": [ /* block */ ] }</code></pre>

<h3>code_block</h3>
<pre><code class="language-json">{
  "type":            "code_block",
  "language":        "python",
  "value":           "print('hi')",
  "filename":        "main.py",
  "highlight_lines": [1, 3, 4, 5]
}</code></pre>
<p><code>filename</code> and <code>highlight_lines</code> are omitted when absent.</p>

<h3>image (block-level)</h3>
<pre><code class="language-json">{ "type": "image", "src": "https://...", "alt": "description", "title": null }</code></pre>
<p>Produced when a Markdown source line contains exactly one image and nothing else. Mixed lines yield <code>inline_image</code> instead.</p>

<h3>list</h3>
<pre><code class="language-json">{
  "type":     "list",
  "ordered":  false,
  "start":    1,
  "children": [ /* list_item */ ]
}</code></pre>
<p><code>start</code> is only present on ordered lists.</p>

<h3>list_item</h3>
<pre><code class="language-json">{
  "type":     "list_item",
  "checked":  true,
  "children": [ /* block or inline */ ]
}</code></pre>
<p><code>checked</code> is <code>true</code>/<code>false</code> for GFM tasklist items, absent for plain items.</p>

<h3>table, table_row, table_cell</h3>
<pre><code class="language-json">{
  "type": "table",
  "head": { "type": "table_head", "rows": [ /* row */ ] },
  "body": { "type": "table_body", "rows": [ /* row */ ] }
}</code></pre>
<pre><code class="language-json">{
  "type":      "table_cell",
  "is_header": true,
  "align":     "center",
  "children":  [ /* inline */ ]
}</code></pre>
<p><code>align</code> ∈ <code>"left"</code> | <code>"center"</code> | <code>"right"</code> | <code>null</code>. Block content inside cells is forbidden (rule W002).</p>

<h3>divider</h3>
<pre><code class="language-json">{ "type": "divider" }</code></pre>

<h3>widget</h3>
<pre><code class="language-json">{
  "type":   "widget",
  "widget": "tip",
  "props":  { "title": "Pro tip" },
  "slots":  {
    "default": [ /* block nodes */ ],
    "footer":  [ /* block nodes */ ]
  }
}</code></pre>
<p><code>slots</code> always contains a <code>"default"</code> key (possibly an empty array). See the <a href="./widgets.html">Widgets</a> chapter.</p>

<h3>html_block</h3>
<pre><code class="language-json">{ "type": "html_block", "value": "&lt;div&gt;raw html&lt;/div&gt;" }</code></pre>
<p>The parser does not interpret HTML — it passes blocks through verbatim and emits a W007 informational diagnostic.</p>

<h3>footnote_def</h3>
<pre><code class="language-json">{ "type": "footnote_def", "label": "1", "children": [ /* block */ ] }</code></pre>

<h2>Inline nodes</h2>

<table>
    <thead><tr><th>Type</th><th>Fields</th></tr></thead>
    <tbody>
        <tr><td><code>text</code></td><td><code>value</code> (string)</td></tr>
        <tr><td><code>bold</code></td><td><code>children</code></td></tr>
        <tr><td><code>italic</code></td><td><code>children</code></td></tr>
        <tr><td><code>bold_italic</code></td><td><code>children</code></td></tr>
        <tr><td><code>code_inline</code></td><td><code>value</code></td></tr>
        <tr><td><code>strikethrough</code></td><td><code>children</code></td></tr>
        <tr><td><code>underline</code></td><td><code>children</code></td></tr>
        <tr><td><code>link</code></td><td><code>href</code>, <code>title</code> (or <code>null</code>), <code>children</code></td></tr>
        <tr><td><code>inline_image</code></td><td><code>src</code>, <code>alt</code>, <code>title</code></td></tr>
        <tr><td><code>softbreak</code></td><td>—</td></tr>
        <tr><td><code>hardbreak</code></td><td>—</td></tr>
        <tr><td><code>footnote_ref</code></td><td><code>label</code></td></tr>
    </tbody>
</table>

<h2>JSON Schema export</h2>

<p>The <code>markast.json_schema()</code> function returns a JSON-Schema describing all of the above. Drop the output into a JSON-Schema validator on your client to enforce shape compatibility, or feed it into a code generator for typed models.</p>

<pre><code class="language-python">import json
from markast import json_schema

with open("ast.schema.json", "w") as f:
    json.dump(json_schema(), f, indent=2)</code></pre>
''',
        # === ES ===
        '''
<h1>Referencia del AST</h1>
<p class="lede">Especificación de cada tipo de nodo que el parser puede producir. Usa este capítulo cuando escribas un renderer cliente.</p>

<h2>Document (raíz)</h2>

<pre><code class="language-json">{
  "type":     "document",
  "version":  "1.0",
  "warnings": [ {"code": "W001", "message": "...", "context": "..."} ],
  "children": [ /* nodos block */ ],
  "meta":     {}
}</code></pre>

<table>
    <thead><tr><th>Campo</th><th>Tipo</th><th>Notas</th></tr></thead>
    <tbody>
    <tr><td><code>version</code></td><td>string</td><td>Sube cuando hay cambios incompatibles. Actualmente <code>"1.0"</code>.</td></tr>
    <tr><td><code>warnings</code></td><td>array</td><td>Lista de diagnósticos. Siempre presente (puede estar vacía).</td></tr>
    <tr><td><code>children</code></td><td>array</td><td>Nodos block. Siempre presente (puede estar vacía).</td></tr>
    <tr><td><code>meta</code></td><td>object</td><td>Bolsa abierta para que las transformaciones agreguen datos (TOC, slugs, …). Puede estar ausente.</td></tr>
    </tbody>
</table>

<h2>Nodos block</h2>

<h3>heading</h3>
<pre><code class="language-json">{ "type": "heading", "level": 2, "children": [ /* inline */ ], "id": "section-id" }</code></pre>
<ul>
    <li><code>level</code> ∈ 1–6.</li>
    <li><code>id</code> lo añade la transformación <code>slugify</code>; ausente en otro caso.</li>
    <li>Los hijos inline están restringidos (regla W001). Las imágenes se convierten en su alt text.</li>
</ul>

<h3>paragraph</h3>
<pre><code class="language-json">{ "type": "paragraph", "children": [ /* inline */ ] }</code></pre>

<h3>blockquote</h3>
<pre><code class="language-json">{ "type": "blockquote", "children": [ /* block */ ] }</code></pre>

<h3>code_block</h3>
<pre><code class="language-json">{
  "type":            "code_block",
  "language":        "python",
  "value":           "print('hi')",
  "filename":        "main.py",
  "highlight_lines": [1, 3, 4, 5]
}</code></pre>
<p><code>filename</code> y <code>highlight_lines</code> se omiten cuando no aplican.</p>

<h3>image (block)</h3>
<pre><code class="language-json">{ "type": "image", "src": "https://...", "alt": "descripción", "title": null }</code></pre>
<p>Se produce cuando una línea de Markdown contiene exactamente una imagen y nada más. Las líneas mixtas producen <code>inline_image</code>.</p>

<h3>list</h3>
<pre><code class="language-json">{
  "type":     "list",
  "ordered":  false,
  "start":    1,
  "children": [ /* list_item */ ]
}</code></pre>
<p><code>start</code> solo está presente en listas ordenadas.</p>

<h3>list_item</h3>
<pre><code class="language-json">{
  "type":     "list_item",
  "checked":  true,
  "children": [ /* block o inline */ ]
}</code></pre>
<p><code>checked</code> es <code>true</code>/<code>false</code> para items de tasklist GFM, ausente en items normales.</p>

<h3>table, table_row, table_cell</h3>
<pre><code class="language-json">{
  "type": "table",
  "head": { "type": "table_head", "rows": [ /* row */ ] },
  "body": { "type": "table_body", "rows": [ /* row */ ] }
}</code></pre>
<pre><code class="language-json">{
  "type":      "table_cell",
  "is_header": true,
  "align":     "center",
  "children":  [ /* inline */ ]
}</code></pre>
<p><code>align</code> ∈ <code>"left"</code> | <code>"center"</code> | <code>"right"</code> | <code>null</code>. Contenido block dentro de celdas está prohibido (regla W002).</p>

<h3>divider</h3>
<pre><code class="language-json">{ "type": "divider" }</code></pre>

<h3>widget</h3>
<pre><code class="language-json">{
  "type":   "widget",
  "widget": "tip",
  "props":  { "title": "Consejo" },
  "slots":  {
    "default": [ /* nodos block */ ],
    "footer":  [ /* nodos block */ ]
  }
}</code></pre>
<p><code>slots</code> siempre contiene la clave <code>"default"</code> (posiblemente un array vacío). Ver el capítulo <a href="./widgets.html">Widgets</a>.</p>

<h3>html_block</h3>
<pre><code class="language-json">{ "type": "html_block", "value": "&lt;div&gt;raw html&lt;/div&gt;" }</code></pre>
<p>El parser no interpreta HTML — pasa los bloques tal cual y emite un diagnóstico informativo W007.</p>

<h3>footnote_def</h3>
<pre><code class="language-json">{ "type": "footnote_def", "label": "1", "children": [ /* block */ ] }</code></pre>

<h2>Nodos inline</h2>

<table>
    <thead><tr><th>Tipo</th><th>Campos</th></tr></thead>
    <tbody>
        <tr><td><code>text</code></td><td><code>value</code> (string)</td></tr>
        <tr><td><code>bold</code></td><td><code>children</code></td></tr>
        <tr><td><code>italic</code></td><td><code>children</code></td></tr>
        <tr><td><code>bold_italic</code></td><td><code>children</code></td></tr>
        <tr><td><code>code_inline</code></td><td><code>value</code></td></tr>
        <tr><td><code>strikethrough</code></td><td><code>children</code></td></tr>
        <tr><td><code>underline</code></td><td><code>children</code></td></tr>
        <tr><td><code>link</code></td><td><code>href</code>, <code>title</code> (o <code>null</code>), <code>children</code></td></tr>
        <tr><td><code>inline_image</code></td><td><code>src</code>, <code>alt</code>, <code>title</code></td></tr>
        <tr><td><code>softbreak</code></td><td>—</td></tr>
        <tr><td><code>hardbreak</code></td><td>—</td></tr>
        <tr><td><code>footnote_ref</code></td><td><code>label</code></td></tr>
    </tbody>
</table>

<h2>Exportar JSON Schema</h2>

<p>La función <code>markast.json_schema()</code> devuelve un JSON-Schema que describe todo lo anterior. Pásalo a un validador en tu cliente para hacer cumplir la compatibilidad de formas, o aliméntaselo a un generador de código para crear modelos tipados.</p>

<pre><code class="language-python">import json
from markast import json_schema

with open("ast.schema.json", "w") as f:
    json.dump(json_schema(), f, indent=2)</code></pre>
''')

    # ════════════════════════════════════════════════════════════════════════
    # 4. WIDGETS
    # ════════════════════════════════════════════════════════════════════════
    page("widgets.html",
        "Widgets", "Widgets",
        # === EN ===
        '''
<h1>Widgets</h1>
<p class="lede">Widgets are how markast carries rich, structured components through Markdown into the AST.</p>

<h2>Syntax</h2>

<pre><code class="language-markdown">:::widget-name key="value" key2=value
Body content with full **markdown** support.

# slot-name
Content of an additional slot.
:::</code></pre>

<p>…lands in the AST as:</p>

<pre><code class="language-json">{
  "type":   "widget",
  "widget": "widget-name",
  "props":  { "key": "value", "key2": "value" },
  "slots":  {
    "default":   [ /* body */ ],
    "slot-name": [ /* slot */ ]
  }
}</code></pre>

<h2>Built-in widgets</h2>

<table>
    <thead><tr><th>Widget</th><th>Purpose</th><th>Notable props</th></tr></thead>
    <tbody>
    <tr><td><code>tip</code></td><td>Friendly callout</td><td><code>title</code>, <code>icon</code></td></tr>
    <tr><td><code>note</code></td><td>Neutral aside</td><td><code>title</code>, <code>icon</code></td></tr>
    <tr><td><code>info</code></td><td>Information callout</td><td><code>title</code>, <code>icon</code></td></tr>
    <tr><td><code>warning</code></td><td>Caution callout</td><td><code>title</code>, <code>icon</code></td></tr>
    <tr><td><code>caution</code></td><td>Stronger warning</td><td><code>title</code>, <code>icon</code></td></tr>
    <tr><td><code>danger</code></td><td>Destructive-action warning</td><td><code>title</code>, <code>icon</code></td></tr>
    <tr><td><code>card</code></td><td>Container with header/body/footer</td><td><code>title</code>, <code>color</code>, <code>elevated</code></td></tr>
    <tr><td><code>video</code></td><td>Video embed</td><td><code>src</code>*, <code>poster</code>, <code>controls</code>, …</td></tr>
    <tr><td><code>code-group</code></td><td>Tabbed code blocks</td><td><code>default_tab</code></td></tr>
    <tr><td><code>code-collapse</code></td><td>Collapsible block</td><td><code>summary</code>, <code>open</code></td></tr>
    <tr><td><code>tabs</code></td><td>Generic tabbed content</td><td><code>default</code>, <code>vertical</code></td></tr>
    <tr><td><code>steps</code></td><td>Numbered step list</td><td><code>start</code></td></tr>
    <tr><td><code>badge</code></td><td>Inline label/pill</td><td><code>label</code>*, <code>color</code></td></tr>
    </tbody>
</table>

<h2>Writing a custom widget</h2>

<pre><code class="language-python">from markast import BaseWidget, Parser, WidgetParam


class CalloutWidget(BaseWidget):
    """A simple coloured callout."""

    name = "callout"
    params = {
        "level": WidgetParam(str, default="info",
                             choices=["info", "warn", "error"],
                             description="Callout severity"),
        "title": WidgetParam(str, default=None),
    }


parser = Parser(widgets=[CalloutWidget])
doc = parser.parse(""":::callout level=warn title="Heads up"
Something **important**.
:::""")

print(doc.to_html())</code></pre>

<p>That's the entire contract. The base class handles parsing the header into typed props, filling defaults, validating choices and emitting W004 diagnostics, required-prop checks (W005), Markdown roundtrip, and a default HTML render. You only override what you need.</p>

<h2>Slots</h2>

<p>A widget body can be split into named slots using bare <code># slot-name</code> H1 headings at the root of the body:</p>

<pre><code class="language-markdown">:::card title="Profile"
Some default body content.

# header
*Custom* header content.

# footer
A footer.
:::</code></pre>

<p>For a widget to acknowledge the extra slot names, declare them on the class:</p>

<pre><code class="language-python">class CardWidget(BaseWidget):
    name = "card"
    slots = ["header", "footer"]
    params = { "title": WidgetParam(str, default=None) }</code></pre>

<p>If you want to accept any slot names (e.g. for <code>tabs</code> or <code>steps</code>), leave <code>slots = []</code>.</p>

<h2>Param types</h2>

<table>
    <thead><tr><th><code>type_</code></th><th>Markdown value</th><th>Result</th></tr></thead>
    <tbody>
    <tr><td><code>str</code></td><td><code>key=hi</code></td><td><code>"hi"</code></td></tr>
    <tr><td><code>str</code></td><td><code>key="multi word"</code></td><td><code>"multi word"</code></td></tr>
    <tr><td><code>int</code></td><td><code>count=3</code></td><td><code>3</code></td></tr>
    <tr><td><code>float</code></td><td><code>ratio=1.5</code></td><td><code>1.5</code></td></tr>
    <tr><td><code>bool</code></td><td><code>autoplay=true</code></td><td><code>True</code> (also <code>1</code>, <code>yes</code>, <code>on</code>)</td></tr>
    <tr><td><code>list</code></td><td><code>tags=a,b,c</code></td><td><code>["a", "b", "c"]</code></td></tr>
    <tr><td><code>list</code></td><td><code>tags=[1,2,3]</code></td><td><code>[1, 2, 3]</code> (JSON form)</td></tr>
    <tr><td><code>dict</code></td><td><code>meta={"a":1}</code></td><td><code>{"a": 1}</code> (JSON only)</td></tr>
    <tr><td><code>Enum</code></td><td><code>level=high</code></td><td>matching <code>Enum</code> member</td></tr>
    </tbody>
</table>

<p>Custom validators:</p>

<pre><code class="language-python">WidgetParam(int, default=10,
            validator=lambda x: None if 1 &lt;= x &lt;= 100 else "must be 1..100")</code></pre>

<h2>Custom rendering</h2>

<pre><code class="language-python">class BadgeWidget(BaseWidget):
    name = "badge"
    params = {
        "label": WidgetParam(str, required=True),
        "color": WidgetParam(str, default="gray"),
    }

    def to_html(self, node, render_children):
        p = node["props"]
        return f'&lt;span class="badge badge-{p["color"]}"&gt;{p["label"]}&lt;/span&gt;'</code></pre>

<p><code>render_children</code> is a callable handed to your widget. Pass any list of child nodes and you get back the rendered string in the renderer's target format. Use it to render slot contents recursively:</p>

<pre><code class="language-python">def to_html(self, node, render_children):
    body = render_children(node["slots"]["default"])
    return f'&lt;aside class="callout"&gt;{body}&lt;/aside&gt;'</code></pre>

<h2>Registration patterns</h2>

<pre><code class="language-python"># 1. Per-parser (recommended) — keeps state local.
from markast import Parser
parser = Parser(widgets=[MyWidget])

# 2. Globally on the default registry — then the top-level parse() works.
from markast.widgets import default_registry
default_registry.register(MyWidget)

from markast import parse
parse(":::my-widget\\n...\\n:::")</code></pre>

<div class="callout callout-info">
    <div class="callout-icon">i</div>
    <div class="callout-body">Pattern 1 is preferred for libraries and servers — different parsers can hold different widget sets without cross-contamination.</div>
</div>

<h2>Schema introspection</h2>

<pre><code class="language-python">CalloutWidget.schema()
# {
#   "name": "callout",
#   "params": {
#     "level": {"type": "str", "required": False, "default": "info",
#               "description": "Callout severity",
#               "choices": ["info", "warn", "error"]},
#     "title": {"type": "str", "required": False}
#   },
#   "slots": ["default"],
#   "doc": "A simple coloured callout."
# }</code></pre>
''',
        # === ES ===
        '''
<h1>Widgets</h1>
<p class="lede">Los widgets son la manera en que markast lleva componentes ricos y estructurados a través de Markdown hasta el AST.</p>

<h2>Sintaxis</h2>

<pre><code class="language-markdown">:::widget-name key="value" key2=value
Contenido del cuerpo con soporte completo de **markdown**.

# slot-name
Contenido de un slot adicional.
:::</code></pre>

<p>…llega al AST como:</p>

<pre><code class="language-json">{
  "type":   "widget",
  "widget": "widget-name",
  "props":  { "key": "value", "key2": "value" },
  "slots":  {
    "default":   [ /* cuerpo */ ],
    "slot-name": [ /* slot */ ]
  }
}</code></pre>

<h2>Widgets builtin</h2>

<table>
    <thead><tr><th>Widget</th><th>Propósito</th><th>Props notables</th></tr></thead>
    <tbody>
    <tr><td><code>tip</code></td><td>Callout amistoso</td><td><code>title</code>, <code>icon</code></td></tr>
    <tr><td><code>note</code></td><td>Aclaración neutral</td><td><code>title</code>, <code>icon</code></td></tr>
    <tr><td><code>info</code></td><td>Callout informativo</td><td><code>title</code>, <code>icon</code></td></tr>
    <tr><td><code>warning</code></td><td>Callout de aviso</td><td><code>title</code>, <code>icon</code></td></tr>
    <tr><td><code>caution</code></td><td>Aviso más fuerte</td><td><code>title</code>, <code>icon</code></td></tr>
    <tr><td><code>danger</code></td><td>Aviso de acción destructiva</td><td><code>title</code>, <code>icon</code></td></tr>
    <tr><td><code>card</code></td><td>Contenedor con header/body/footer</td><td><code>title</code>, <code>color</code>, <code>elevated</code></td></tr>
    <tr><td><code>video</code></td><td>Embed de video</td><td><code>src</code>*, <code>poster</code>, <code>controls</code>, …</td></tr>
    <tr><td><code>code-group</code></td><td>Bloques de código en pestañas</td><td><code>default_tab</code></td></tr>
    <tr><td><code>code-collapse</code></td><td>Bloque colapsable</td><td><code>summary</code>, <code>open</code></td></tr>
    <tr><td><code>tabs</code></td><td>Pestañas genéricas</td><td><code>default</code>, <code>vertical</code></td></tr>
    <tr><td><code>steps</code></td><td>Lista de pasos numerados</td><td><code>start</code></td></tr>
    <tr><td><code>badge</code></td><td>Etiqueta inline</td><td><code>label</code>*, <code>color</code></td></tr>
    </tbody>
</table>

<h2>Escribir un widget propio</h2>

<pre><code class="language-python">from markast import BaseWidget, Parser, WidgetParam


class CalloutWidget(BaseWidget):
    """Un callout coloreado simple."""

    name = "callout"
    params = {
        "level": WidgetParam(str, default="info",
                             choices=["info", "warn", "error"],
                             description="Severidad del callout"),
        "title": WidgetParam(str, default=None),
    }


parser = Parser(widgets=[CalloutWidget])
doc = parser.parse(""":::callout level=warn title="Atención"
Algo **importante**.
:::""")

print(doc.to_html())</code></pre>

<p>Ese es el contrato completo. La clase base se encarga de parsear el header en props tipados, rellenar defaults, validar choices y emitir diagnósticos W004, validar props requeridos (W005), hacer roundtrip a Markdown, y un render HTML por defecto. Solo sobrescribes lo que necesitas.</p>

<h2>Slots</h2>

<p>El cuerpo de un widget se puede dividir en slots con nombre usando headings <code># slot-name</code> de nivel 1 a la raíz del cuerpo:</p>

<pre><code class="language-markdown">:::card title="Perfil"
Contenido del slot por defecto.

# header
Contenido *personalizado* del header.

# footer
Un footer.
:::</code></pre>

<p>Para que el widget reconozca los nombres extra de slot, decláralos en la clase:</p>

<pre><code class="language-python">class CardWidget(BaseWidget):
    name = "card"
    slots = ["header", "footer"]
    params = { "title": WidgetParam(str, default=None) }</code></pre>

<p>Si quieres aceptar cualquier nombre de slot (como <code>tabs</code> o <code>steps</code>), deja <code>slots = []</code>.</p>

<h2>Tipos de Param</h2>

<table>
    <thead><tr><th><code>type_</code></th><th>Valor en Markdown</th><th>Resultado</th></tr></thead>
    <tbody>
    <tr><td><code>str</code></td><td><code>key=hola</code></td><td><code>"hola"</code></td></tr>
    <tr><td><code>str</code></td><td><code>key="varias palabras"</code></td><td><code>"varias palabras"</code></td></tr>
    <tr><td><code>int</code></td><td><code>count=3</code></td><td><code>3</code></td></tr>
    <tr><td><code>float</code></td><td><code>ratio=1.5</code></td><td><code>1.5</code></td></tr>
    <tr><td><code>bool</code></td><td><code>autoplay=true</code></td><td><code>True</code> (también <code>1</code>, <code>yes</code>, <code>on</code>)</td></tr>
    <tr><td><code>list</code></td><td><code>tags=a,b,c</code></td><td><code>["a", "b", "c"]</code></td></tr>
    <tr><td><code>list</code></td><td><code>tags=[1,2,3]</code></td><td><code>[1, 2, 3]</code> (forma JSON)</td></tr>
    <tr><td><code>dict</code></td><td><code>meta={"a":1}</code></td><td><code>{"a": 1}</code> (solo JSON)</td></tr>
    <tr><td><code>Enum</code></td><td><code>level=high</code></td><td>el miembro de <code>Enum</code> correspondiente</td></tr>
    </tbody>
</table>

<p>Validadores propios:</p>

<pre><code class="language-python">WidgetParam(int, default=10,
            validator=lambda x: None if 1 &lt;= x &lt;= 100 else "debe estar en 1..100")</code></pre>

<h2>Render personalizado</h2>

<pre><code class="language-python">class BadgeWidget(BaseWidget):
    name = "badge"
    params = {
        "label": WidgetParam(str, required=True),
        "color": WidgetParam(str, default="gray"),
    }

    def to_html(self, node, render_children):
        p = node["props"]
        return f'&lt;span class="badge badge-{p["color"]}"&gt;{p["label"]}&lt;/span&gt;'</code></pre>

<p><code>render_children</code> es un callable que tu widget recibe. Pásale cualquier lista de nodos hijos y te devuelve el string renderizado en el formato del renderer. Úsalo para renderizar slots recursivamente:</p>

<pre><code class="language-python">def to_html(self, node, render_children):
    body = render_children(node["slots"]["default"])
    return f'&lt;aside class="callout"&gt;{body}&lt;/aside&gt;'</code></pre>

<h2>Patrones de registro</h2>

<pre><code class="language-python"># 1. Por parser (recomendado) — mantiene el estado local.
from markast import Parser
parser = Parser(widgets=[MyWidget])

# 2. Globalmente en el registry por defecto — el parse() top-level lo verá.
from markast.widgets import default_registry
default_registry.register(MyWidget)

from markast import parse
parse(":::my-widget\\n...\\n:::")</code></pre>

<div class="callout callout-info">
    <div class="callout-icon">i</div>
    <div class="callout-body">El patrón 1 es preferible para librerías y servidores — distintos parsers pueden tener distintos widgets sin contaminarse entre sí.</div>
</div>

<h2>Introspección de schema</h2>

<pre><code class="language-python">CalloutWidget.schema()
# {
#   "name": "callout",
#   "params": {
#     "level": {"type": "str", "required": False, "default": "info",
#               "description": "Severidad del callout",
#               "choices": ["info", "warn", "error"]},
#     "title": {"type": "str", "required": False}
#   },
#   "slots": ["default"],
#   "doc": "Un callout coloreado simple."
# }</code></pre>
''')

    # ════════════════════════════════════════════════════════════════════════
    # 5. TRANSFORMS
    # ════════════════════════════════════════════════════════════════════════
    page("transforms.html",
        "Transforms", "Transformaciones",
        # === EN ===
        '''
<h1>Transforms</h1>
<p class="lede">AST-to-AST mutations applied after parsing and before serialisation. They bake in cross-cutting behaviour without polluting the parser or renderer.</p>

<h2>Built-in transforms</h2>

<table>
    <thead><tr><th>Identifier</th><th>Class</th><th>What it does</th></tr></thead>
    <tbody>
    <tr><td><code>normalize</code></td><td><code>NormalizeText</code></td><td>Merge adjacent text nodes, drop empty ones.</td></tr>
    <tr><td><code>slugify</code></td><td><code>SlugifyHeadings</code></td><td>Add a stable <code>id</code> to every heading.</td></tr>
    <tr><td><code>toc</code></td><td><code>BuildTOC</code></td><td>Build a nested table-of-contents in <code>doc.meta["toc"]</code>. Requires <code>slugify</code>.</td></tr>
    <tr><td><code>linkify</code></td><td><code>Linkify</code></td><td>Convert bare URLs in text to <code>link</code> nodes.</td></tr>
    <tr><td><code>smarttypography</code></td><td><code>SmartTypography</code></td><td>Replace dashes/quotes/ellipses with typographic equivalents.</td></tr>
    </tbody>
</table>

<p>Apply them by name when constructing a parser:</p>

<pre><code class="language-python">from markast import Parser

parser = Parser(transforms=["normalize", "slugify", "toc"])
doc = parser.parse("# Top\\n\\n## Sub\\n\\n# Top2")

print(doc.meta["toc"])
# [
#   {"level": 1, "text": "Top",  "id": "top",  "children": [
#       {"level": 2, "text": "Sub", "id": "sub", "children": []}
#   ]},
#   {"level": 1, "text": "Top2", "id": "top2", "children": []}
# ]</code></pre>

<h2>Order matters</h2>

<p>Transforms run in the order you list them. <code>toc</code> reads ids set by <code>slugify</code>, so <code>slugify</code> must come first.</p>

<h2>Writing a custom transform</h2>

<pre><code class="language-python">from markast.transforms import Transform
from markast.ast import replace
from markast import NodeType


class StripDividers(Transform):
    """Remove every horizontal rule from the document."""

    name = "strip-dividers"

    def apply(self, doc, config):
        return replace(doc, lambda n: None if n.get("type") == NodeType.DIVIDER else n)</code></pre>

<p>Register it:</p>

<pre><code class="language-python">parser = Parser(transforms=[StripDividers])</code></pre>

<div class="callout callout-tip">
    <div class="callout-icon">!</div>
    <div class="callout-body">Three things to remember: (1) receive and return a document, (2) use <code>markast.ast.replace</code> for rewrites — it handles every container shape correctly, (3) use <code>doc["meta"]</code> to expose computed data rather than rewriting the tree to fit it.</div>
</div>

<h2>Transforms vs. rules</h2>

<table>
    <thead><tr><th></th><th>Transform</th><th>Rule (<code>markast.rules</code>)</th></tr></thead>
    <tbody>
    <tr><td><strong>When</strong></td><td>After parsing, before rendering</td><td>During parsing</td></tr>
    <tr><td><strong>What</strong></td><td>Mutates / annotates the AST</td><td>Observes and reports diagnostics</td></tr>
    <tr><td><strong>Side effect</strong></td><td>Changes the output</td><td>Adds entries to <code>doc.warnings</code></td></tr>
    <tr><td><strong>Use for</strong></td><td>Slugs, TOCs, autolinks, normalisation</td><td>Cross-cutting validation, lints</td></tr>
    </tbody>
</table>

<p>Pick a rule when you want to <em>flag</em> something. Pick a transform when you want to <em>change</em> something.</p>
''',
        # === ES ===
        '''
<h1>Transformaciones</h1>
<p class="lede">Mutaciones AST → AST que se aplican después del parseo y antes de la serialización. Hornean comportamiento transversal sin contaminar el parser ni el renderer.</p>

<h2>Transformaciones builtin</h2>

<table>
    <thead><tr><th>Identificador</th><th>Clase</th><th>Qué hace</th></tr></thead>
    <tbody>
    <tr><td><code>normalize</code></td><td><code>NormalizeText</code></td><td>Une nodos text adyacentes, descarta los vacíos.</td></tr>
    <tr><td><code>slugify</code></td><td><code>SlugifyHeadings</code></td><td>Añade un <code>id</code> estable a cada heading.</td></tr>
    <tr><td><code>toc</code></td><td><code>BuildTOC</code></td><td>Construye un table-of-contents anidado en <code>doc.meta["toc"]</code>. Requiere <code>slugify</code>.</td></tr>
    <tr><td><code>linkify</code></td><td><code>Linkify</code></td><td>Convierte URLs sueltas en texto a nodos <code>link</code>.</td></tr>
    <tr><td><code>smarttypography</code></td><td><code>SmartTypography</code></td><td>Reemplaza guiones/comillas/puntos suspensivos por equivalentes tipográficos.</td></tr>
    </tbody>
</table>

<p>Aplícalas por nombre al construir el parser:</p>

<pre><code class="language-python">from markast import Parser

parser = Parser(transforms=["normalize", "slugify", "toc"])
doc = parser.parse("# Top\\n\\n## Sub\\n\\n# Top2")

print(doc.meta["toc"])
# [
#   {"level": 1, "text": "Top",  "id": "top",  "children": [
#       {"level": 2, "text": "Sub", "id": "sub", "children": []}
#   ]},
#   {"level": 1, "text": "Top2", "id": "top2", "children": []}
# ]</code></pre>

<h2>El orden importa</h2>

<p>Las transformaciones corren en el orden que las listas. <code>toc</code> lee los ids que escribe <code>slugify</code>, así que <code>slugify</code> debe ir primero.</p>

<h2>Escribir una transformación propia</h2>

<pre><code class="language-python">from markast.transforms import Transform
from markast.ast import replace
from markast import NodeType


class StripDividers(Transform):
    """Quita cada regla horizontal del documento."""

    name = "strip-dividers"

    def apply(self, doc, config):
        return replace(doc, lambda n: None if n.get("type") == NodeType.DIVIDER else n)</code></pre>

<p>Regístrala:</p>

<pre><code class="language-python">parser = Parser(transforms=[StripDividers])</code></pre>

<div class="callout callout-tip">
    <div class="callout-icon">!</div>
    <div class="callout-body">Tres cosas a recordar: (1) recibe y devuelve un documento, (2) usa <code>markast.ast.replace</code> para reescrituras — maneja correctamente cada forma de contenedor, (3) usa <code>doc["meta"]</code> para exponer datos calculados en lugar de reescribir el árbol para acomodarlos.</div>
</div>

<h2>Transformaciones vs. reglas</h2>

<table>
    <thead><tr><th></th><th>Transformación</th><th>Regla (<code>markast.rules</code>)</th></tr></thead>
    <tbody>
    <tr><td><strong>Cuándo</strong></td><td>Después del parseo, antes del render</td><td>Durante el parseo</td></tr>
    <tr><td><strong>Qué</strong></td><td>Muta / anota el AST</td><td>Observa y reporta diagnósticos</td></tr>
    <tr><td><strong>Side effect</strong></td><td>Cambia el output</td><td>Añade entradas a <code>doc.warnings</code></td></tr>
    <tr><td><strong>Cuándo usar</strong></td><td>Slugs, TOCs, autolinks, normalización</td><td>Validación transversal, lints</td></tr>
    </tbody>
</table>

<p>Usa una regla cuando quieres <em>señalar</em> algo. Usa una transformación cuando quieres <em>cambiar</em> algo.</p>
''')

    # ════════════════════════════════════════════════════════════════════════
    # 6. RENDERERS
    # ════════════════════════════════════════════════════════════════════════
    page("renderers.html",
        "Renderers", "Renderers",
        # === EN ===
        '''
<h1>Renderers</h1>
<p class="lede">Two renderers ship in the box: <code>MarkdownRenderer</code> and <code>HTMLRenderer</code>. Both are subclassable Python classes — override individual node handlers to customise output.</p>

<h2>MarkdownRenderer</h2>

<p>Round-trips an AST back into Markdown. Useful for:</p>

<ul>
    <li>Rendering AST stored in a database back into a textarea / code editor.</li>
    <li>Re-emitting normalised Markdown after running transforms.</li>
    <li>Debugging — <code>print(doc.to_markdown())</code> is more readable than the JSON.</li>
</ul>

<pre><code class="language-python">from markast import MarkdownRenderer, parse

doc = parse("# Hi\\n\\nA paragraph.")
print(MarkdownRenderer().render(doc.root))</code></pre>

<p>For convenience, <code>Document.to_markdown()</code> does the same thing.</p>

<h3>Roundtrip stability</h3>

<p><code>parse(text).to_markdown()</code> reproduces the source for every Markdown construct markast supports, with these normalisations:</p>

<ul>
    <li>Excess blank lines collapse to a single blank line.</li>
    <li>Setext headings (<code>====</code> underline) become ATX (<code># title</code>).</li>
    <li>Loose-list marker positions normalise to flush-left.</li>
    <li>List indentation normalises to 2 spaces per level.</li>
</ul>

<p>The roundtrip is stable: <code>parse(parse(text).to_markdown()).to_markdown()</code> equals <code>parse(text).to_markdown()</code> for every supported construct.</p>

<h2>HTMLRenderer</h2>

<p>Conservative, opinion-free HTML. No CSS classes are emitted by default beyond the structural ones widgets explicitly add.</p>

<pre><code class="language-python">from markast import HTMLRenderer, parse

doc = parse("# Hi\\n\\n:::tip\\nA tip\\n:::")
print(HTMLRenderer().render(doc.root))</code></pre>

<p>Set <code>wrap_root=True</code> to wrap the output in an <code>&lt;article class="markast"&gt;</code>:</p>

<pre><code class="language-python">HTMLRenderer(wrap_root=True).render(doc.root)
# &lt;article class="markast"&gt;...&lt;/article&gt;</code></pre>

<h3>Special characters</h3>

<p>Plain <code>text</code> nodes are escaped: <code>&lt;</code>, <code>&gt;</code>, <code>&amp;</code> become <code>&amp;lt;</code>, <code>&amp;gt;</code>, <code>&amp;amp;</code>. Code blocks are escaped the same way. HTML attributes are escaped including <code>"</code>.</p>

<p><code>html_block</code> nodes (raw HTML appearing in source Markdown) are emitted verbatim — the parser already validated nothing about their content. Treat this as opt-in: if your source allows raw HTML, you trust the authors.</p>

<h2>Subclassing</h2>

<p>Both renderers dispatch by method name: <code>_block_&lt;type&gt;</code> for block nodes, <code>_inline_&lt;type&gt;</code> for inline nodes. Override only what you care about:</p>

<pre><code class="language-python">from markast import MarkdownRenderer


class FlushDividers(MarkdownRenderer):
    """Use a stronger divider syntax."""

    def _block_divider(self, node):
        return "* * *"


print(FlushDividers().render(doc.root))</code></pre>

<p><code>HTMLRenderer</code> follows the same convention. Override e.g. <code>_block_heading</code> to emit anchored headings:</p>

<pre><code class="language-python">class AnchoredHTMLRenderer(HTMLRenderer):
    def _block_heading(self, node):
        lvl = max(1, min(6, node.get("level", 1)))
        slug = node.get("id", "")
        anchor = f'&lt;a href="#{slug}"&gt;#&lt;/a&gt;' if slug else ""
        body = self._inline(node.get("children", []))
        return f'&lt;h{lvl} id="{slug}"&gt;{body}{anchor}&lt;/h{lvl}&gt;'</code></pre>

<p>Pair this with the <code>slugify</code> transform so every heading carries an <code>id</code>.</p>

<h2>Custom renderers</h2>

<p>If you want a third format (terminal? a different document model?), the easiest path is to extend the same dispatch pattern:</p>

<pre><code class="language-python">class AnsiRenderer:
    def render(self, doc):
        return "".join(self._block(c) for c in doc.get("children", []))

    def _block(self, node):
        method = getattr(self, f"_block_{node.get('type')}", None)
        return method(node) if method else ""

    def _block_heading(self, node):
        text = "".join(c.get("value", "") for c in node["children"])
        return f"\\033[1m{'#' * node['level']} {text}\\033[0m\\n\\n"

    def _block_paragraph(self, node):
        text = "".join(c.get("value", "") for c in node["children"])
        return text + "\\n\\n"</code></pre>

<p>Aim for the same <code>_block_&lt;type&gt;</code> / <code>_inline_&lt;type&gt;</code> convention so your users can extend your renderer the same way they extend the built-in ones.</p>
''',
        # === ES ===
        '''
<h1>Renderers</h1>
<p class="lede">Dos renderers vienen en la caja: <code>MarkdownRenderer</code> y <code>HTMLRenderer</code>. Ambas son clases Python subclasificables — sobrescribe handlers individuales para personalizar la salida.</p>

<h2>MarkdownRenderer</h2>

<p>Hace roundtrip de un AST de regreso a Markdown. Útil para:</p>

<ul>
    <li>Renderizar AST guardado en BD de regreso a un textarea / editor.</li>
    <li>Re-emitir Markdown normalizado después de correr transformaciones.</li>
    <li>Debugging — <code>print(doc.to_markdown())</code> es más legible que el JSON.</li>
</ul>

<pre><code class="language-python">from markast import MarkdownRenderer, parse

doc = parse("# Hola\\n\\nUn párrafo.")
print(MarkdownRenderer().render(doc.root))</code></pre>

<p>Por conveniencia, <code>Document.to_markdown()</code> hace lo mismo.</p>

<h3>Estabilidad del roundtrip</h3>

<p><code>parse(text).to_markdown()</code> reproduce la fuente para cada construcción Markdown que markast soporta, con estas normalizaciones:</p>

<ul>
    <li>Líneas en blanco en exceso colapsan a una sola.</li>
    <li>Headings setext (subrayado <code>====</code>) se vuelven ATX (<code># título</code>).</li>
    <li>Marcadores de listas sueltas se normalizan a la izquierda.</li>
    <li>Indentación de listas se normaliza a 2 espacios por nivel.</li>
</ul>

<p>El roundtrip es estable: <code>parse(parse(text).to_markdown()).to_markdown()</code> equivale a <code>parse(text).to_markdown()</code> para cada construcción soportada.</p>

<h2>HTMLRenderer</h2>

<p>HTML conservador, sin opiniones. No emite clases CSS por defecto más allá de las estructurales que los widgets añaden explícitamente.</p>

<pre><code class="language-python">from markast import HTMLRenderer, parse

doc = parse("# Hola\\n\\n:::tip\\nUn tip\\n:::")
print(HTMLRenderer().render(doc.root))</code></pre>

<p>Pasa <code>wrap_root=True</code> para envolver la salida en <code>&lt;article class="markast"&gt;</code>:</p>

<pre><code class="language-python">HTMLRenderer(wrap_root=True).render(doc.root)
# &lt;article class="markast"&gt;...&lt;/article&gt;</code></pre>

<h3>Caracteres especiales</h3>

<p>Los nodos <code>text</code> se escapan: <code>&lt;</code>, <code>&gt;</code>, <code>&amp;</code> se vuelven <code>&amp;lt;</code>, <code>&amp;gt;</code>, <code>&amp;amp;</code>. Los bloques de código se escapan igual. Los atributos HTML se escapan incluyendo <code>"</code>.</p>

<p>Los nodos <code>html_block</code> (HTML crudo en la fuente Markdown) se emiten verbatim — el parser ya no validó nada de su contenido. Trátalo como opt-in: si tu fuente permite HTML crudo, confías en los autores.</p>

<h2>Subclasificar</h2>

<p>Ambos renderers despachan por nombre de método: <code>_block_&lt;type&gt;</code> para nodos block, <code>_inline_&lt;type&gt;</code> para inline. Sobrescribe solo lo que te importa:</p>

<pre><code class="language-python">from markast import MarkdownRenderer


class FlushDividers(MarkdownRenderer):
    """Usa una sintaxis de divider más fuerte."""

    def _block_divider(self, node):
        return "* * *"


print(FlushDividers().render(doc.root))</code></pre>

<p><code>HTMLRenderer</code> sigue la misma convención. Sobrescribe por ejemplo <code>_block_heading</code> para emitir headings con ancla:</p>

<pre><code class="language-python">class AnchoredHTMLRenderer(HTMLRenderer):
    def _block_heading(self, node):
        lvl = max(1, min(6, node.get("level", 1)))
        slug = node.get("id", "")
        anchor = f'&lt;a href="#{slug}"&gt;#&lt;/a&gt;' if slug else ""
        body = self._inline(node.get("children", []))
        return f'&lt;h{lvl} id="{slug}"&gt;{body}{anchor}&lt;/h{lvl}&gt;'</code></pre>

<p>Combínalo con la transformación <code>slugify</code> para que cada heading lleve un <code>id</code>.</p>

<h2>Renderers personalizados</h2>

<p>Si quieres un tercer formato (terminal? otro modelo de documento?), la ruta más fácil es extender el mismo patrón de despacho:</p>

<pre><code class="language-python">class AnsiRenderer:
    def render(self, doc):
        return "".join(self._block(c) for c in doc.get("children", []))

    def _block(self, node):
        method = getattr(self, f"_block_{node.get('type')}", None)
        return method(node) if method else ""

    def _block_heading(self, node):
        text = "".join(c.get("value", "") for c in node["children"])
        return f"\\033[1m{'#' * node['level']} {text}\\033[0m\\n\\n"

    def _block_paragraph(self, node):
        text = "".join(c.get("value", "") for c in node["children"])
        return text + "\\n\\n"</code></pre>

<p>Mantén la convención <code>_block_&lt;type&gt;</code> / <code>_inline_&lt;type&gt;</code> para que tus usuarios puedan extender tu renderer igual que extienden los builtin.</p>
''')

    # ════════════════════════════════════════════════════════════════════════
    # 7. WALKER & UTILITIES
    # ════════════════════════════════════════════════════════════════════════
    page("walker.html",
        "Walker & utilities", "Walker y utilidades",
        # === EN ===
        '''
<h1>Walker &amp; utilities</h1>
<p class="lede">The <code>markast.ast</code> package exposes traversal primitives so you can inspect or rewrite the tree without writing recursion against every container shape.</p>

<h2>walk(node) — generator</h2>

<pre><code class="language-python">from markast import parse, walk

doc = parse("# Hi\\n\\nA **bold** word.")
for node in walk(doc.root):
    print(node["type"])
# document
# heading
# text
# paragraph
# text
# bold
# text</code></pre>

<p>The walker visits nodes in <strong>document order</strong> (depth-first, pre-order). It follows every container key (<code>children</code>, <code>slots</code>, <code>head</code>, <code>body</code>, <code>rows</code>, <code>cells</code>), so widgets and tables aren't skipped.</p>

<p><code>walk(node, include_root=False)</code> skips the starting node and only yields descendants.</p>

<h2>find(node, type_) and find_all(node, type_)</h2>

<pre><code class="language-python">from markast import find, find_all, parse

doc = parse("# A\\n\\n## B\\n\\n## C")
print(find(doc.root, "heading")["children"][0]["value"])      # A
print([h["children"][0]["value"] for h in find_all(doc.root, "heading")])
# ["A", "B", "C"]</code></pre>

<p>Both accept a string type or a list of types:</p>

<pre><code class="language-python">find_all(doc.root, ["link", "inline_image"])</code></pre>

<h2>Visitor — class-based dispatch</h2>

<pre><code class="language-python">from markast import Visitor, parse


class HeadingCollector(Visitor):
    def __init__(self):
        self.headings = []

    def visit_heading(self, node):
        self.headings.append(node)


v = HeadingCollector()
v.run(parse("# A\\n\\n## B"))
print(len(v.headings))  # 2</code></pre>

<p>Override <code>visit_&lt;node_type&gt;</code> for any node type you want to react to. Methods may return a value, which <code>run()</code> collects into a list.</p>

<h2>replace(node, fn) — functional rewrite</h2>

<p><code>replace</code> walks the tree and applies <code>fn</code> to every node, substituting each with whatever <code>fn</code> returns. Returning <code>None</code> <em>removes</em> the node:</p>

<pre><code class="language-python">from markast import NodeType, parse, replace

doc = parse("# Title\\n\\n---\\n\\nBody.")
trimmed = replace(doc.root, lambda n: None if n.get("type") == NodeType.DIVIDER else n)</code></pre>

<p>Returning a brand-new node is fine — the walker continues into the <em>replacement's</em> children, not the original's. This makes one-pass rewrites trivial:</p>

<pre><code class="language-python">def lowercase_text(node):
    if node.get("type") == "text":
        return {"type": "text", "value": node["value"].lower()}
    return node


lowered = replace(doc.root, lowercase_text)</code></pre>

<p>Pass <code>in_place=True</code> to mutate the existing dict tree if you need to keep object identity. Otherwise, the default behaviour is to return a fresh tree.</p>

<h2>extract_text(node)</h2>

<p>Shortcut for "give me the plain-text projection of this subtree":</p>

<pre><code class="language-python">from markast import extract_text, parse

doc = parse("# Hello **world**")
print(extract_text(doc.children[0]))
# "Hello world"</code></pre>

<p>It walks <code>children</code>, <code>slots</code>, and table rows/cells, so widgets and tables contribute too.</p>

<h2>count_nodes(node)</h2>

<pre><code class="language-python">from markast import count_nodes, parse

doc = parse("# A\\n\\n## B\\n\\n- x\\n- y")
print(count_nodes(doc.root))
# {'document': 1, 'heading': 2, 'text': 4, 'list': 1, 'list_item': 2, ...}</code></pre>

<h2>Cheat-sheet</h2>

<table>
    <thead><tr><th>Goal</th><th>Use</th></tr></thead>
    <tbody>
    <tr><td>Iterate every node, do something</td><td><code>walk</code></td></tr>
    <tr><td>Find the first / all of a kind</td><td><code>find</code> / <code>find_all</code></td></tr>
    <tr><td>Extract data into a list</td><td><code>Visitor</code></td></tr>
    <tr><td>Mutate a copy of the tree</td><td><code>replace</code></td></tr>
    <tr><td>Mutate in place</td><td><code>replace(..., in_place=True)</code></td></tr>
    <tr><td>Get plain text</td><td><code>extract_text</code></td></tr>
    <tr><td>Tally node types</td><td><code>count_nodes</code></td></tr>
    </tbody>
</table>

<p>Mental model: <em>the AST is just dicts.</em> The walker is the only non-trivial part of using it; everything else is dictionary manipulation.</p>
''',
        # === ES ===
        '''
<h1>Walker y utilidades</h1>
<p class="lede">El paquete <code>markast.ast</code> expone primitivas de recorrido para que inspecciones o reescribas el árbol sin escribir recursión contra cada forma de contenedor.</p>

<h2>walk(node) — generador</h2>

<pre><code class="language-python">from markast import parse, walk

doc = parse("# Hola\\n\\nUna palabra **negrita**.")
for node in walk(doc.root):
    print(node["type"])
# document
# heading
# text
# paragraph
# text
# bold
# text</code></pre>

<p>El walker visita los nodos en <strong>orden de documento</strong> (depth-first, pre-order). Sigue cada clave contenedora (<code>children</code>, <code>slots</code>, <code>head</code>, <code>body</code>, <code>rows</code>, <code>cells</code>), así que widgets y tablas no se saltan.</p>

<p><code>walk(node, include_root=False)</code> salta el nodo inicial y solo emite descendientes.</p>

<h2>find(node, type_) y find_all(node, type_)</h2>

<pre><code class="language-python">from markast import find, find_all, parse

doc = parse("# A\\n\\n## B\\n\\n## C")
print(find(doc.root, "heading")["children"][0]["value"])      # A
print([h["children"][0]["value"] for h in find_all(doc.root, "heading")])
# ["A", "B", "C"]</code></pre>

<p>Ambas aceptan un tipo string o una lista:</p>

<pre><code class="language-python">find_all(doc.root, ["link", "inline_image"])</code></pre>

<h2>Visitor — despacho por clase</h2>

<pre><code class="language-python">from markast import Visitor, parse


class HeadingCollector(Visitor):
    def __init__(self):
        self.headings = []

    def visit_heading(self, node):
        self.headings.append(node)


v = HeadingCollector()
v.run(parse("# A\\n\\n## B"))
print(len(v.headings))  # 2</code></pre>

<p>Sobrescribe <code>visit_&lt;node_type&gt;</code> para cualquier tipo de nodo al que quieras reaccionar. Los métodos pueden devolver un valor, que <code>run()</code> colecta en una lista.</p>

<h2>replace(node, fn) — reescritura funcional</h2>

<p><code>replace</code> recorre el árbol y aplica <code>fn</code> a cada nodo, sustituyendo cada uno por lo que <code>fn</code> retorne. Devolver <code>None</code> <em>elimina</em> el nodo:</p>

<pre><code class="language-python">from markast import NodeType, parse, replace

doc = parse("# Título\\n\\n---\\n\\nCuerpo.")
trimmed = replace(doc.root, lambda n: None if n.get("type") == NodeType.DIVIDER else n)</code></pre>

<p>Devolver un nodo nuevo está bien — el walker continúa por los hijos del <em>reemplazo</em>, no del original. Esto hace que reescrituras de una pasada sean triviales:</p>

<pre><code class="language-python">def lowercase_text(node):
    if node.get("type") == "text":
        return {"type": "text", "value": node["value"].lower()}
    return node


lowered = replace(doc.root, lowercase_text)</code></pre>

<p>Pasa <code>in_place=True</code> para mutar el árbol existente si necesitas preservar identidad de objetos. Por defecto devuelve un árbol nuevo.</p>

<h2>extract_text(node)</h2>

<p>Atajo para "dame la proyección de texto plano de este subárbol":</p>

<pre><code class="language-python">from markast import extract_text, parse

doc = parse("# Hola **mundo**")
print(extract_text(doc.children[0]))
# "Hola mundo"</code></pre>

<p>Recorre <code>children</code>, <code>slots</code>, y rows/cells de tablas, así que widgets y tablas también aportan texto.</p>

<h2>count_nodes(node)</h2>

<pre><code class="language-python">from markast import count_nodes, parse

doc = parse("# A\\n\\n## B\\n\\n- x\\n- y")
print(count_nodes(doc.root))
# {'document': 1, 'heading': 2, 'text': 4, 'list': 1, 'list_item': 2, ...}</code></pre>

<h2>Cheat-sheet</h2>

<table>
    <thead><tr><th>Objetivo</th><th>Usa</th></tr></thead>
    <tbody>
    <tr><td>Iterar cada nodo, hacer algo</td><td><code>walk</code></td></tr>
    <tr><td>Encontrar el primero / todos de un tipo</td><td><code>find</code> / <code>find_all</code></td></tr>
    <tr><td>Extraer datos en una lista</td><td><code>Visitor</code></td></tr>
    <tr><td>Mutar una copia del árbol</td><td><code>replace</code></td></tr>
    <tr><td>Mutar en sitio</td><td><code>replace(..., in_place=True)</code></td></tr>
    <tr><td>Obtener texto plano</td><td><code>extract_text</code></td></tr>
    <tr><td>Contar tipos de nodos</td><td><code>count_nodes</code></td></tr>
    </tbody>
</table>

<p>Modelo mental: <em>el AST es solo dicts.</em> El walker es la única parte no trivial; todo lo demás es manipulación de diccionarios.</p>
''')

    # ════════════════════════════════════════════════════════════════════════
    # 8. CLIENT INTEGRATION
    # ════════════════════════════════════════════════════════════════════════
    page("client-integration.html",
        "Client integration", "Integración con clientes",
        # === EN ===
        '''
<h1>Client integration</h1>
<p class="lede">The standard pattern for shipping markast output to a client — regardless of which technology that client uses. The ideas are the same whether you render with React, Vue, Svelte, native mobile widgets, terminal UIs, or anything else that can <code>switch</code> on a string.</p>

<h2>The pipeline</h2>

<pre><code class="language-text">┌──────────────┐    parse()     ┌──────────┐   to_json()   ┌───────────┐    HTTP    ┌──────────────┐
│  Markdown    │ ─────────────► │   AST    │ ────────────► │   JSON    │ ─────────► │   Client     │
│  source      │                │  (dict)  │               │  (string) │            │  renderer    │
└──────────────┘                └──────────┘               └───────────┘            └──────────────┘</code></pre>

<p>Every step happens server-side. The client receives a typed JSON tree and walks it. The client never parses Markdown.</p>

<h2>A FastAPI handler</h2>

<pre><code class="language-python">from fastapi import FastAPI
from markast import Parser

app = FastAPI()
parser = Parser(transforms=["normalize", "slugify", "toc"])


@app.get("/content/{slug}")
def get_content(slug: str):
    markdown = load_from_db(slug)
    doc = parser.parse(markdown)

    return {
        "ast":      doc.to_dict(),
        "warnings": doc.warnings,
        "toc":      doc.meta.get("toc", []),
    }</code></pre>

<p>One parser instance reused across requests. <code>Parser.parse()</code> is thread-safe for read operations.</p>

<h2>Client-side: switch on type</h2>

<p>Pseudocode that ports cleanly to any front-end:</p>

<pre><code class="language-text">function render(node):
    switch node.type:
        case "document":   render_each(node.children)
        case "heading":    return text_with_size(node.level, render_inline(node.children))
        case "paragraph":  return text(render_inline(node.children))
        case "list":       return list_view(node.ordered, render_each(node.children))
        case "list_item":  return list_item(render_each(node.children), checked=node.checked)
        case "image":      return image(node.src, node.alt)
        case "code_block": return code(node.language, node.value, filename=node.filename)
        case "table":      return table(render_table(node.head, node.body))
        case "blockquote": return quote(render_each(node.children))
        case "divider":    return divider()
        case "widget":     return render_widget(node)
        ...

function render_inline(nodes):
    parts = []
    for n in nodes:
        switch n.type:
            case "text":           parts.add(plain(n.value))
            case "bold":           parts.add(bold(render_inline(n.children)))
            case "italic":         parts.add(italic(render_inline(n.children)))
            case "code_inline":    parts.add(code_span(n.value))
            case "link":           parts.add(link(n.href, render_inline(n.children)))
            case "strikethrough":  parts.add(strike(render_inline(n.children)))
            case "softbreak":      parts.add(line_break())
            case "hardbreak":      parts.add(line_break())
            ...
    return parts</code></pre>

<p>Concrete code in your front-end framework will look almost identical.</p>

<h2>Widgets on the client</h2>

<p>A <code>widget</code> node lets your content carry custom components. Branch by widget name:</p>

<pre><code class="language-text">function render_widget(node):
    switch node.widget:
        case "tip":         return Callout(level="tip",  title=node.props.title, body=render_each(node.slots.default))
        case "warning":     return Callout(level="warn", title=node.props.title, body=render_each(node.slots.default))
        case "video":       return Video(src=node.props.src, poster=node.props.poster, controls=node.props.controls)
        case "card":        return Card(title=node.props.title, header=render_each(node.slots.header or []), body=render_each(node.slots.default), footer=render_each(node.slots.footer or []))
        case "code-group":  return Tabs(node.slots.default.map(b =&gt; (b.filename, render(b))))
        default:
            // Unknown widget — fail open: render the default slot if any, or skip.
            return render_each(node.slots.default or [])</code></pre>

<h2>Generating client schemas</h2>

<p>If your client language has a strong type system, generate type definitions from <code>json_schema()</code>:</p>

<pre><code class="language-python">import json
from markast import json_schema

with open("ast.schema.json", "w") as f:
    json.dump(json_schema(), f, indent=2)</code></pre>

<p>Feed that schema into:</p>

<ul>
    <li><code>quicktype</code> — Dart, TypeScript, Go, Swift, C#, Kotlin, Rust, …</li>
    <li><code>datamodel-code-generator</code> — Pydantic / TypedDict</li>
    <li><code>json-schema-to-typescript</code> — TS interfaces</li>
</ul>

<h2>Warnings: where to surface them</h2>

<p><code>doc.warnings</code> is the pragma channel between author and content review. Recommended:</p>

<ul>
    <li>In production responses, drop warnings — clients ignore them anyway.</li>
    <li>In staging / dev responses, surface them so authors see what's wrong.</li>
    <li>In a CMS authoring UI, render warnings inline next to the offending source.</li>
</ul>

<pre><code class="language-python">warnings = doc.warnings if request.app.debug else []
return {"ast": doc.to_dict(), "warnings": warnings}</code></pre>

<h2>What the AST guarantees</h2>

<table>
    <thead><tr><th>Invariant</th><th>Why it matters</th></tr></thead>
    <tbody>
    <tr><td>Every node has a <code>type</code> string</td><td>Lets the client switch on it</td></tr>
    <tr><td><code>heading.children</code> never contain images or block-level nodes</td><td>Headings render inline-only</td></tr>
    <tr><td><code>table_cell.children</code> never contain block-level nodes</td><td>Cells render inline-only</td></tr>
    <tr><td><code>widget.props</code> is a dict; <code>widget.slots</code> always has a <code>"default"</code> key</td><td>Always safe to destructure</td></tr>
    <tr><td><code>document.warnings</code> is always an array (may be empty)</td><td>Never <code>null</code></td></tr>
    <tr><td><code>document.version</code> is a string</td><td>Use for forward-compat checks</td></tr>
    </tbody>
</table>

<h2>Caching tip</h2>

<p>If your content rarely changes, parsing on every request is wasteful. Cache the JSON output keyed on the source's hash:</p>

<pre><code class="language-python">import hashlib
from functools import lru_cache

@lru_cache(maxsize=1024)
def parse_cached(text_hash, text):
    return parser.parse(text).to_dict()


@app.get("/content/{slug}")
def get_content(slug):
    md = load_from_db(slug)
    h = hashlib.sha256(md.encode("utf-8")).hexdigest()
    return parse_cached(h, md)</code></pre>
''',
        # === ES ===
        '''
<h1>Integración con clientes</h1>
<p class="lede">El patrón estándar para enviar la salida de markast a un cliente — sin importar la tecnología. Las ideas son las mismas si renderizas con React, Vue, Svelte, widgets nativos móviles, UIs de terminal, o cualquier cosa que pueda hacer <code>switch</code> sobre un string.</p>

<h2>El pipeline</h2>

<pre><code class="language-text">┌──────────────┐    parse()     ┌──────────┐   to_json()   ┌───────────┐    HTTP    ┌──────────────┐
│  Fuente      │ ─────────────► │   AST    │ ────────────► │   JSON    │ ─────────► │   Renderer   │
│  Markdown    │                │  (dict)  │               │  (string) │            │   cliente    │
└──────────────┘                └──────────┘               └───────────┘            └──────────────┘</code></pre>

<p>Cada paso ocurre server-side. El cliente recibe un árbol JSON tipado y lo recorre. El cliente nunca parsea Markdown.</p>

<h2>Un handler en FastAPI</h2>

<pre><code class="language-python">from fastapi import FastAPI
from markast import Parser

app = FastAPI()
parser = Parser(transforms=["normalize", "slugify", "toc"])


@app.get("/content/{slug}")
def get_content(slug: str):
    markdown = load_from_db(slug)
    doc = parser.parse(markdown)

    return {
        "ast":      doc.to_dict(),
        "warnings": doc.warnings,
        "toc":      doc.meta.get("toc", []),
    }</code></pre>

<p>Una instancia de Parser reutilizada entre requests. <code>Parser.parse()</code> es thread-safe para operaciones de lectura.</p>

<h2>Cliente: switch sobre type</h2>

<p>Pseudocódigo que se traduce limpiamente a cualquier front-end:</p>

<pre><code class="language-text">function render(node):
    switch node.type:
        case "document":   render_each(node.children)
        case "heading":    return text_with_size(node.level, render_inline(node.children))
        case "paragraph":  return text(render_inline(node.children))
        case "list":       return list_view(node.ordered, render_each(node.children))
        case "list_item":  return list_item(render_each(node.children), checked=node.checked)
        case "image":      return image(node.src, node.alt)
        case "code_block": return code(node.language, node.value, filename=node.filename)
        case "table":      return table(render_table(node.head, node.body))
        case "blockquote": return quote(render_each(node.children))
        case "divider":    return divider()
        case "widget":     return render_widget(node)
        ...

function render_inline(nodes):
    parts = []
    for n in nodes:
        switch n.type:
            case "text":           parts.add(plain(n.value))
            case "bold":           parts.add(bold(render_inline(n.children)))
            case "italic":         parts.add(italic(render_inline(n.children)))
            case "code_inline":    parts.add(code_span(n.value))
            case "link":           parts.add(link(n.href, render_inline(n.children)))
            case "strikethrough":  parts.add(strike(render_inline(n.children)))
            case "softbreak":      parts.add(line_break())
            case "hardbreak":      parts.add(line_break())
            ...
    return parts</code></pre>

<p>El código concreto en tu framework se verá casi idéntico.</p>

<h2>Widgets en el cliente</h2>

<p>Un nodo <code>widget</code> deja que tu contenido lleve componentes propios. Bifurca por nombre de widget:</p>

<pre><code class="language-text">function render_widget(node):
    switch node.widget:
        case "tip":         return Callout(level="tip",  title=node.props.title, body=render_each(node.slots.default))
        case "warning":     return Callout(level="warn", title=node.props.title, body=render_each(node.slots.default))
        case "video":       return Video(src=node.props.src, poster=node.props.poster, controls=node.props.controls)
        case "card":        return Card(title=node.props.title, header=render_each(node.slots.header or []), body=render_each(node.slots.default), footer=render_each(node.slots.footer or []))
        case "code-group":  return Tabs(node.slots.default.map(b =&gt; (b.filename, render(b))))
        default:
            // Widget desconocido — falla suave: renderiza el slot default si lo hay, o ignóralo.
            return render_each(node.slots.default or [])</code></pre>

<h2>Generar schemas para clientes</h2>

<p>Si tu lenguaje cliente tiene un sistema de tipos fuerte, genera definiciones desde <code>json_schema()</code>:</p>

<pre><code class="language-python">import json
from markast import json_schema

with open("ast.schema.json", "w") as f:
    json.dump(json_schema(), f, indent=2)</code></pre>

<p>Pasa ese schema a:</p>

<ul>
    <li><code>quicktype</code> — Dart, TypeScript, Go, Swift, C#, Kotlin, Rust, …</li>
    <li><code>datamodel-code-generator</code> — Pydantic / TypedDict</li>
    <li><code>json-schema-to-typescript</code> — interfaces TS</li>
</ul>

<h2>Warnings: dónde mostrarlos</h2>

<p><code>doc.warnings</code> es el canal de avisos entre autor y revisión de contenido. Recomendado:</p>

<ul>
    <li>En respuestas de producción, descártalos — los clientes los ignoran.</li>
    <li>En staging / dev, expónlos para que los autores vean qué falla.</li>
    <li>En una UI de autoría/CMS, renderízalos junto al fragmento ofensor.</li>
</ul>

<pre><code class="language-python">warnings = doc.warnings if request.app.debug else []
return {"ast": doc.to_dict(), "warnings": warnings}</code></pre>

<h2>Lo que el AST garantiza</h2>

<table>
    <thead><tr><th>Invariante</th><th>Por qué importa</th></tr></thead>
    <tbody>
    <tr><td>Cada nodo tiene un <code>type</code> string</td><td>El cliente puede hacer switch</td></tr>
    <tr><td><code>heading.children</code> nunca contiene imágenes ni nodos block</td><td>Los headings se renderizan solo inline</td></tr>
    <tr><td><code>table_cell.children</code> nunca contiene nodos block</td><td>Las celdas se renderizan solo inline</td></tr>
    <tr><td><code>widget.props</code> es un dict; <code>widget.slots</code> siempre tiene la clave <code>"default"</code></td><td>Siempre seguro de destructurar</td></tr>
    <tr><td><code>document.warnings</code> es siempre un array (puede estar vacío)</td><td>Nunca <code>null</code></td></tr>
    <tr><td><code>document.version</code> es un string</td><td>Útil para chequeos de compatibilidad futura</td></tr>
    </tbody>
</table>

<h2>Tip de caché</h2>

<p>Si tu contenido cambia poco, parsear en cada request es desperdicio. Cachea el JSON usando como clave un hash de la fuente:</p>

<pre><code class="language-python">import hashlib
from functools import lru_cache

@lru_cache(maxsize=1024)
def parse_cached(text_hash, text):
    return parser.parse(text).to_dict()


@app.get("/content/{slug}")
def get_content(slug):
    md = load_from_db(slug)
    h = hashlib.sha256(md.encode("utf-8")).hexdigest()
    return parse_cached(h, md)</code></pre>
''')

    # ════════════════════════════════════════════════════════════════════════
    # 9. EXTENDING
    # ════════════════════════════════════════════════════════════════════════
    page("extending.html",
        "Extending", "Extender la librería",
        # === EN ===
        '''
<h1>Extending</h1>
<p class="lede">Beyond widgets, transforms, and renderer subclasses, the parser exposes deeper hooks for cases where those aren't enough.</p>

<h2>Custom rules</h2>

<p>A rule observes the tree being built and reports diagnostics. Subclass <code>markast.rules.Rule</code> and override the methods you care about:</p>

<pre><code class="language-python">from markast import Parser
from markast.rules import Diagnostic, Rule, Severity


class HeadingMustBeShort(Rule):
    """Flag headings whose plain text exceeds 60 characters."""

    name = "short-heading"

    def check_heading_children(self, children, level):
        text = "".join(c.get("value", "") for c in children
                       if c.get("type") == "text")
        if len(text) &gt; 60:
            return [Diagnostic(
                code="X100",
                message=f"Heading too long ({len(text)} chars).",
                context=text[:40] + "…",
                severity=Severity.WARNING,
            )]
        return None


parser = Parser(rules=[HeadingMustBeShort])</code></pre>

<h3>Diagnostic codes</h3>

<table>
    <thead><tr><th>Code</th><th>Trigger</th></tr></thead>
    <tbody>
    <tr><td>W001</td><td>Image inside a heading</td></tr>
    <tr><td>W002</td><td>Block element where inline is required</td></tr>
    <tr><td>W003</td><td>Unknown widget name</td></tr>
    <tr><td>W004</td><td>Invalid widget prop value (wrong type / not in choices)</td></tr>
    <tr><td>W005</td><td>Required widget prop missing</td></tr>
    <tr><td>W006</td><td>Image inside a table cell</td></tr>
    <tr><td>W007</td><td>Raw HTML block found (informational)</td></tr>
    <tr><td>W008</td><td>Footnote reference without a matching definition</td></tr>
    <tr><td>W009</td><td>Widget nesting deeper than the configured limit</td></tr>
    </tbody>
</table>

<p>To <em>replace</em> the built-in rules entirely (e.g. for a strict mode), pass an empty default and add yours. To <em>extend</em>, include <code>BuiltinRules</code>:</p>

<pre><code class="language-python">from markast.rules.builtin import BuiltinRules
parser = Parser(rules=[BuiltinRules(), HeadingMustBeShort()])</code></pre>

<h2>Tweaking the parser config</h2>

<pre><code class="language-python">from markast import Parser, ParserConfig

cfg = ParserConfig(
    features=("tables", "strikethrough", "footnotes"),  # no autolinks/tasklists
    diagnose_html_blocks=False,
    max_widget_depth=8,
)

parser = Parser(cfg)</code></pre>

<p>Use <code>cfg.evolve(...)</code> to derive a new config:</p>

<pre><code class="language-python">strict = cfg.evolve(max_widget_depth=4)</code></pre>

<h2>Replacing the tokenizer</h2>

<p>Rare, but possible. <code>Parser</code> lazily constructs a <code>Tokenizer</code>; if you need a different one (e.g. to inject extra <code>markdown-it-py</code> plugins), assign it before the first parse:</p>

<pre><code class="language-python">from markast import Parser
from markast.parser.tokenizer import Tokenizer
from mdit_py_plugins.deflist import deflist_plugin


class MyTokenizer(Tokenizer):
    def _build_markdown_it(self):
        md = super()._build_markdown_it()
        md.use(deflist_plugin)
        return md


parser = Parser()
parser._tokenizer = MyTokenizer(parser.config, parser.registry)</code></pre>

<h2>Pattern: per-tenant parser</h2>

<p>A multi-tenant service may need different widget sets per tenant. Build a parser cache keyed on tenant id:</p>

<pre><code class="language-python">from functools import lru_cache
from markast import Parser
from markast.widgets import default_registry, WidgetRegistry


@lru_cache(maxsize=64)
def parser_for(tenant_id: str) -&gt; Parser:
    registry = default_registry.clone()
    for cls in load_tenant_widgets(tenant_id):
        registry.register(cls)
    return Parser(registry=registry, transforms=["normalize", "slugify"])


def render(tenant_id, markdown):
    return parser_for(tenant_id).parse(markdown)</code></pre>

<p>Each parser is independent — registry mutations on one don't affect others.</p>

<h2>Pattern: strict authoring CI</h2>

<p>Combine custom rules with <code>doc.has_errors</code> to fail a CI build on bad content:</p>

<pre><code class="language-python">from markast import Parser
from markast.rules import Diagnostic, Rule, Severity


class NoRawHtml(Rule):
    name = "no-raw-html"

    def check_html_block(self, value):
        return [Diagnostic(
            code="C001",
            message="Raw HTML is not allowed in this corpus.",
            severity=Severity.ERROR,
        )]


parser = Parser(rules=[NoRawHtml()])

doc = parser.parse(open("article.md").read())
if doc.has_errors:
    for w in doc.warnings:
        print(f"::error::[{w['code']}] {w['message']}")
    raise SystemExit(1)</code></pre>

<h2>Where the source lives</h2>

<pre><code class="language-text">markast/
├── ast/         types, factories, walker, schema export
├── parser/      tokenizer + builder (block / inline / widget / props)
├── render/      markdown + html
├── widgets/     base / registry / built-ins
├── rules/       diagnostic system + built-in rules
├── transforms/  normalize / slugify / toc / linkify / typography
├── config.py
├── document.py
├── parser_api.py
└── cli.py</code></pre>

<p>Every file starts with a module docstring. If you're stuck, that's the fastest way in.</p>
''',
        # === ES ===
        '''
<h1>Extender la librería</h1>
<p class="lede">Más allá de widgets, transformaciones y subclases de renderer, el parser expone hooks más profundos para casos donde esos no alcanzan.</p>

<h2>Reglas propias</h2>

<p>Una regla observa el árbol que se está construyendo y reporta diagnósticos. Subclasifica <code>markast.rules.Rule</code> y sobrescribe los métodos que te interesen:</p>

<pre><code class="language-python">from markast import Parser
from markast.rules import Diagnostic, Rule, Severity


class HeadingMustBeShort(Rule):
    """Marca headings cuyo texto plano supera los 60 caracteres."""

    name = "short-heading"

    def check_heading_children(self, children, level):
        text = "".join(c.get("value", "") for c in children
                       if c.get("type") == "text")
        if len(text) &gt; 60:
            return [Diagnostic(
                code="X100",
                message=f"Heading demasiado largo ({len(text)} chars).",
                context=text[:40] + "…",
                severity=Severity.WARNING,
            )]
        return None


parser = Parser(rules=[HeadingMustBeShort])</code></pre>

<h3>Códigos de diagnóstico</h3>

<table>
    <thead><tr><th>Código</th><th>Disparador</th></tr></thead>
    <tbody>
    <tr><td>W001</td><td>Imagen dentro de un heading</td></tr>
    <tr><td>W002</td><td>Elemento block donde se requiere inline</td></tr>
    <tr><td>W003</td><td>Nombre de widget desconocido</td></tr>
    <tr><td>W004</td><td>Valor de prop inválido (tipo incorrecto / no está en choices)</td></tr>
    <tr><td>W005</td><td>Prop requerido faltante</td></tr>
    <tr><td>W006</td><td>Imagen dentro de una celda de tabla</td></tr>
    <tr><td>W007</td><td>HTML crudo encontrado (informativo)</td></tr>
    <tr><td>W008</td><td>Referencia a footnote sin definición</td></tr>
    <tr><td>W009</td><td>Anidación de widgets más profunda que el límite configurado</td></tr>
    </tbody>
</table>

<p>Para <em>reemplazar</em> las reglas builtin (por ejemplo en modo estricto), pasa solo las tuyas. Para <em>extender</em>, incluye <code>BuiltinRules</code>:</p>

<pre><code class="language-python">from markast.rules.builtin import BuiltinRules
parser = Parser(rules=[BuiltinRules(), HeadingMustBeShort()])</code></pre>

<h2>Ajustar la configuración del parser</h2>

<pre><code class="language-python">from markast import Parser, ParserConfig

cfg = ParserConfig(
    features=("tables", "strikethrough", "footnotes"),  # sin autolinks/tasklists
    diagnose_html_blocks=False,
    max_widget_depth=8,
)

parser = Parser(cfg)</code></pre>

<p>Usa <code>cfg.evolve(...)</code> para derivar nuevas configuraciones:</p>

<pre><code class="language-python">strict = cfg.evolve(max_widget_depth=4)</code></pre>

<h2>Reemplazar el tokenizer</h2>

<p>Raro, pero posible. <code>Parser</code> construye un <code>Tokenizer</code> de forma perezosa; si necesitas otro (por ejemplo para inyectar plugins extra de <code>markdown-it-py</code>), asígnalo antes del primer parse:</p>

<pre><code class="language-python">from markast import Parser
from markast.parser.tokenizer import Tokenizer
from mdit_py_plugins.deflist import deflist_plugin


class MyTokenizer(Tokenizer):
    def _build_markdown_it(self):
        md = super()._build_markdown_it()
        md.use(deflist_plugin)
        return md


parser = Parser()
parser._tokenizer = MyTokenizer(parser.config, parser.registry)</code></pre>

<h2>Patrón: parser por tenant</h2>

<p>Un servicio multi-tenant puede necesitar conjuntos distintos de widgets por tenant. Cachea parsers por id:</p>

<pre><code class="language-python">from functools import lru_cache
from markast import Parser
from markast.widgets import default_registry, WidgetRegistry


@lru_cache(maxsize=64)
def parser_for(tenant_id: str) -&gt; Parser:
    registry = default_registry.clone()
    for cls in load_tenant_widgets(tenant_id):
        registry.register(cls)
    return Parser(registry=registry, transforms=["normalize", "slugify"])


def render(tenant_id, markdown):
    return parser_for(tenant_id).parse(markdown)</code></pre>

<p>Cada parser es independiente — mutar el registry de uno no afecta a los demás.</p>

<h2>Patrón: CI estricto de autoría</h2>

<p>Combina reglas propias con <code>doc.has_errors</code> para fallar una build de CI por contenido inválido:</p>

<pre><code class="language-python">from markast import Parser
from markast.rules import Diagnostic, Rule, Severity


class NoRawHtml(Rule):
    name = "no-raw-html"

    def check_html_block(self, value):
        return [Diagnostic(
            code="C001",
            message="HTML crudo no permitido en este corpus.",
            severity=Severity.ERROR,
        )]


parser = Parser(rules=[NoRawHtml()])

doc = parser.parse(open("article.md").read())
if doc.has_errors:
    for w in doc.warnings:
        print(f"::error::[{w['code']}] {w['message']}")
    raise SystemExit(1)</code></pre>

<h2>Dónde está el código fuente</h2>

<pre><code class="language-text">markast/
├── ast/         tipos, factories, walker, exportar schema
├── parser/      tokenizer + builder (block / inline / widget / props)
├── render/      markdown + html
├── widgets/     base / registry / builtins
├── rules/       sistema de diagnósticos + reglas builtin
├── transforms/  normalize / slugify / toc / linkify / typography
├── config.py
├── document.py
├── parser_api.py
└── cli.py</code></pre>

<p>Cada archivo empieza con un docstring de módulo. Si te atascas, esa es la entrada más rápida.</p>
''')
