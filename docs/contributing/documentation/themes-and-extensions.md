---
myst:
  html_meta:
    "description": "Themes and extensions"
    "property=og:description": "Themes and extensions"
    "property=og:title": "Themes and extensions"
    "keywords": "Documentation, Plone, Sphinx, reStructuredText, MyST, Markdown, themes, sphinx-book-theme, pydata_sphinx_theme, extensions"
---

(contributing-themes-and-extensions)=

# Themes and extensions

The Plone Documentation team learned the hard way that maintaining the design and features of documentation is a lot of work.
To make all documentation maintainable, we use actively developed themes and extensions to build the documentation.


## Themes

When customizing the theme, we use [Sphinx Book Theme](https://sphinx-book-theme.readthedocs.io/en/stable/), which in turn depends on [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html).
See their documentation for features, tips, and tricks that you might want to include in your documentation.

We minimize the customizations of these themes as much as possible.


## Extensions

We use several MyST and Sphinx extensions to enhance the presentation of Plone documentation.


### MyST

-   [`attrs_block`](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#block-attributes) supports parsing of block attributes before certain block syntaxes.
-   [`attrs_inline`](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#inline-attributes) supports parsing of inline attributes before certain inline syntaxes.
-   [`colon_fence`](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#code-fences-using-colons) supports the use of three colons `:::` as delimiters to denote code fences, instead of three backticks `` ``` ``.
-   [`deflist`](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#definition-lists) supports definition lists.
-   [`html_image`](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#html-images) supports the use of HTML `<img>` tags.
-   [`linkify`](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#linkify) identifies "bare" web URLs and adds hyperlinks.
-   [`strikethrough`](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#syntax-strikethrough) supports the use of strikethrough markup.
-   [`substitution`](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#substitutions-with-jinja2) supports the use of substitutions with Jinja2.


### Sphinx

-   [`myst_parser`](https://myst-parser.readthedocs.io/en/latest/) parses MyST, a rich and extensible flavour of Markdown for authoring documentation.
-   [`sphinx-design`](https://sphinx-design.readthedocs.io/en/latest/), with a configuration name of `sphinx_design`, adds grids, cards, icons, badges, buttons, tabs, and dropdowns.
-   [`sphinx-examples`](https://ebp-sphinx-examples.readthedocs.io/en/latest/) adds "example snippets" that allow you to show off source Markdown and the result of rendering it in Sphinx.
-   [`sphinx-notfound-page`](https://sphinx-notfound-page.readthedocs.io/en/latest/index.html), with a configuration name of `notfound.extension`, creates a custom 404 page and helps generate proper static resource links to render the page.
-   [`sphinx-tippy`](https://sphinx-tippy.readthedocs.io/en/latest/), with a configuration name of `sphinx_tippy`, provides hover tips in your documentation.
-   [`sphinx.ext.autodoc`](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) pulls in documentation from Python docstrings to generate reStructuredText which in turn gets parsed by Sphinx and rendered to the output format.
    It's used by {doc}`/plone.api/index`.
-   [`sphinx.ext.autosummary`](https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html) generates function/method/attribute summary lists.
    It's used by {doc}`/plone.api/index`.
-   [`sphinx.ext.graphviz`](https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html) allows you to embed [Graphviz](https://graphviz.org/download/) graphs in your documents.
-   [`sphinx.ext.ifconfig`](https://www.sphinx-doc.org/en/master/usage/extensions/ifconfig.html) includes content based on configuration.
-   [`sphinx.ext.intersphinx`](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html) provides linking between separate projects that use Sphinx for documentation.
-   [`sphinx.ext.todo`](https://www.sphinx-doc.org/en/master/usage/extensions/todo.html) adds support for todo items.
-   [`sphinx.ext.viewcode`](https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html) generates pages of source code modules and links between the source and the description.
    It's used by {doc}`/plone.api/index`.
-   [`sphinx_copybutton`](https://sphinx-copybutton.readthedocs.io/en/latest/index.html)  adds a little "copy" button to the right of code blocks.
-   [`sphinx_reredirects`](https://documatt.com/sphinx-reredirects/) handles redirects for moved pages.
-   [`sphinx_sitemap`](https://pypi.org/project/sphinx-sitemap/) generates multiversion and multilanguage [sitemaps.org](https://www.sitemaps.org/protocol.html) compliant sitemaps.
-   [`sphinxcontrib.httpdomain`](https://sphinxcontrib-httpdomain.readthedocs.io/en/stable/) provides a Sphinx domain for describing HTTP APIs.
    It's used by Plone's {doc}`/plone.restapi/docs/source/index`.
-   [`sphinxcontrib.httpexample`](https://sphinxcontrib-httpexample.readthedocs.io/en/latest/) enhances `sphinxcontrib-httpdomain` by generating RESTful HTTP API call examples for different tools from a single HTTP request example.
    Supported tools include [`curl`](https://curl.se/), [`wget`](https://www.gnu.org/software/wget/), [`httpie`](https://httpie.io/), and [`python-requests`](https://requests.readthedocs.io/en/latest/).
    It's used by Plone's {doc}`/plone.restapi/docs/source/index`.
-   [`sphinxcontrib.mermaid`](https://pypi.org/project/sphinxcontrib-mermaid/) allows you to embed [Mermaid](https://mermaid.js.org/) graphs in your documents, including general flowcharts, sequence diagrams, and Gantt charts.
-   [`sphinxcontrib.video`](https://pypi.org/project/sphinxcontrib-video/) allows you to embed local videos as defined by the HTML5 standard.
-   [`sphinxcontrib.youtube`](https://pypi.org/project/sphinxcontrib-video/) allows you to embed remotely hosted videos from [YouTube](https://www.youtube.com/), [Vimeo](https://vimeo.com/), or [PeerTube](https://joinpeertube.org/).
-   [`sphinxext.opengraph`](https://pypi.org/project/sphinxext-opengraph/) generates [OpenGraph metadata](https://ogp.me/).
