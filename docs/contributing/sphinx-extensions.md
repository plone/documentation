---
myst:
  html_meta:
    "description": "Sphinx extensions"
    "property=og:description": "Sphinx extensions"
    "property=og:title": "Sphinx extensions"
    "keywords": "Documentation, Plone, Sphinx, reStructuredText, extensions"
---

(contributing-sphinx-extensions)=

# Sphinx extensions

We use several Sphinx extensions to enhance the presentation of Plone documentation.

-   [`sphinx.ext.intersphinx`](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html) provides linking between separate projects that use Sphinx for documentation.
-   [`sphinx.ext.todo`](https://www.sphinx-doc.org/en/master/usage/extensions/todo.html) adds support for todo items.
-   [`sphinx_copybutton`](https://sphinx-copybutton.readthedocs.io/en/latest/index.html)  adds a little "copy" button to the right of code blocks.
-   [`sphinx-design`](https://sphinx-design.readthedocs.io/en/latest/) adds grids, cards, icons, badges, buttons, tabs, and dropdowns.
-   [`sphinx_sitemap`](https://pypi.org/project/sphinx-sitemap/) generates multiversion and multilanguage [sitemaps.org](https://www.sitemaps.org/protocol.html) compliant sitemaps.
-   [`sphinxcontrib.httpdomain`](https://sphinxcontrib-httpdomain.readthedocs.io/en/stable/) provides a Sphinx domain for describing HTTP APIs.
    It is used by Plone's {doc}`plone.restapi/docs/source/index`.
-   [`sphinxcontrib.httpexample`](https://sphinxcontrib-httpexample.readthedocs.io/en/latest/) enhances `sphinxcontrib-httpdomain` by generating RESTful HTTP API call examples for different tools from a single HTTP request example.
    Supported tools include [curl](https://curl.se/), [wget](https://www.gnu.org/software/wget/), [httpie](https://httpie.io/), and [python-requests](https://requests.readthedocs.io/en/latest/).
    It is used by Plone's {doc}`plone.restapi/docs/source/index`.
-   [`sphinxcontrib.video`](https://pypi.org/project/sphinxcontrib-video/) allows you to embed local videos as defined by the HTML5 standard.
-   [`sphinxext.opengraph`](https://pypi.org/project/sphinxext-opengraph/) generates [OpenGraph metadata](https://ogp.me/).
-   [`sphinx.ext.viewcode`](https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html) generates pages of source code modules and links between the source and the description.
    It is used by {doc}`/plone.api/index`.
-   [`sphinx.ext.autosummary`](https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html) generates function/method/attribute summary lists.
    It is used by {doc}`/plone.api/index`.
