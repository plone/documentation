# Configuration file for the Sphinx documentation builder.
# Plone Documentation build configuration file


# -- Path setup --------------------------------------------------------------

from datetime import datetime

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath("."))


# -- Project information -----------------------------------------------------

project = "Plone Documentation"
copyright = "Plone Foundation"
author = "Plone community"
trademark_name = "Plone"
now = datetime.now()
year = str(now.year)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = "6"
# The full version, including alpha/beta/rc tags.
release = "6"


# -- General configuration ----------------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Add any Sphinx extension module names here, as strings.
# They can be extensions coming with Sphinx (named "sphinx.ext.*")
# or your custom ones.
extensions = [
    "myst_parser",
    "notfound.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",  # plone.api
    "sphinx.ext.doctest",  # plone.api
    "sphinx.ext.graphviz",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",  # plone.api
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_examples",
    "sphinx_reredirects",
    "sphinx_sitemap",
    "sphinxcontrib.httpdomain",  # plone.restapi
    "sphinxcontrib.httpexample",  # plone.restapi
    "sphinxcontrib.mermaid",
    "sphinxcontrib.video",
    "sphinxcontrib.youtube",
    "sphinxext.opengraph",
]

# If true, the Docutils Smart Quotes transform, originally based on SmartyPants
# (limited to English) and currently applying to many languages, will be used
# to convert quotes and dashes to typographically correct entities.
# Note to maintainers: setting this to `True` will cause contractions and
# hyphenated words to be marked as misspelled by spellchecker.
smartquotes = False

# Options for the linkcheck builder
# Ignore localhost
linkcheck_ignore = [
    # Ignore local and example URLs
    r"http://0.0.0.0",
    r"http://127.0.0.1",
    r"http://localhost",
    r"http://yoursite",
    # Ignore static file downloads
    r"^/_static/",
    r"^/_images/",
    # Ignore pages that require authentication
    r"https://github.com/orgs/plone/teams/",  # requires auth
    r"https://github.com/plone/documentation/issues/new",  # requires auth
    r"https://github.com/plone/volto/issues/new/choose",  # requires auth
    r"https://opensource.org/",  # requires auth
    # Ignore github.com pages with anchors
    r"https://github.com/.*#.*",
    # Ignore github.com searches
    r"https://github.com/search",
    # Ignore GitHub 429 Client Error: Too Many Requests for url
    r"https://github.com/collective/plone.app.locales/commits/master/",
    # Ignore rate limiting by github.com
    r"https://github.com/plone/volto/issues",
    r"https://github.com/plone/volto/pull",
    # Ignore other specific anchors
    r"https://coveralls.io/repos/github/plone/plone.restapi/badge.svg\?branch=main",  # plone.restapi
    r"https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors#Identifying_the_issue",  # volto
    r"https://docs.cypress.io/guides/references/migration-guide#Migrating-to-Cypress-version-10-0",  # volto
    r"https://browsersl.ist/#",
    # Ignore unreliable sites
    r"https://web.archive.org/",
    r"http://z3c.pt",  # fluke where Sphinx interprets this as a URL
]
linkcheck_allowed_redirects = {
    # All HTTP redirections from the source URI to the canonical URI will be treated as "working".
    # Example
    # r"https://chrome\.google\.com/webstore/detail/.*": r"https://consent\.google\.com/.*",
}
linkcheck_anchors = True
linkcheck_timeout = 5
linkcheck_retries = 1
# See https://github.com/plone/documentation/issues/1815
linkcheck_report_timeouts_as_broken = False

# The suffix of source filenames.
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "spelling_wordlist.txt",
    "**/CHANGES.rst",
    "**/CONTRIBUTORS.rst",
    "**/LICENSE.rst",
    "**/README.rst",
    "**/eggs",
    "_inc/.*",
    "plone.restapi/.*",
    "plone.restapi/bin",
    "plone.restapi/develop-eggs",
    "plone.restapi/docs/source/glossary.md",  # There can be only one Glossary.
    "plone.restapi/eggs",
    "plone.restapi/ideas",
    "plone.restapi/include",
    "plone.restapi/lib",
    "plone.restapi/news",
    "plone.restapi/parts",
    "plone.restapi/performance",
    "plone.restapi/src",
    "plone.restapi/var",
    "volto/_inc/*",
]

suppress_warnings = [
    # "toc.excluded",  # Suppress `WARNING: document isn't included in any toctree`
    "toc.not_readable",  # Suppress `WARNING: toctree contains reference to nonexisting document 'news*'`
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "plone_sphinx_theme"
html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.ico"
# The default value includes icon-links, so override it with that one omitted, and add it to html_theme_options[footer_content_items].
html_sidebars = {
    "**": [
        "navbar-logo",
        "search-button-field",
        "sbt-sidebar-nav",
    ]
}

html_theme_options = {
    "article_header_start": ["toggle-primary-sidebar"],
    "footer_content_items": [
        "author",
        "copyright",
        "last-updated",
        "extra-footer",
        "icon-links",
    ],
    "extra_footer": """<p>The text and illustrations in this website are licensed by the Plone Foundation under a Creative Commons Attribution 4.0 International license. Plone and the Plone® logo are registered trademarks of the Plone Foundation, registered in the United States and other countries. For guidelines on the permitted uses of the Plone trademarks, see <a href="https://plone.org/foundation/logo">https://plone.org/foundation/logo</a>. All other trademarks are owned by their respective owners.</p>
    <p>Pull request previews by <a href="https://readthedocs.org/">Read the Docs</a>.</p>""",
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/plone/documentation",
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
            "attributes": {
                "target": "_blank",
                "rel": "noopener me",
                "class": "nav-link custom-fancy-css"
            }
        },
        {
            "name": "Mastodon",
            "url": "https://plone.social/@plone",
            "icon": "fa-brands fa-mastodon",
            "type": "fontawesome",
            "attributes": {
                "target": "_blank",
                "rel": "noopener me",
                "class": "nav-link custom-fancy-css"
            }
        },
        {
            "name": "YouTube",
            "url": "https://www.youtube.com/@PloneCMS",
            "icon": "fa-brands fa-youtube",
            "type": "fontawesome",
            "attributes": {
                "target": "_blank",
                "rel": "noopener me",
                "class": "nav-link custom-fancy-css"
            }
        },
        {
            "name": "X (formerly Twitter)",
            "url": "https://x.com/plone",
            "icon": "fa-brands fa-square-x-twitter",
            "type": "fontawesome",
            "attributes": {
                "target": "_blank",
                "rel": "noopener me",
                "class": "nav-link custom-fancy-css"
            }
        },
    ],
    "logo": {
        "text": "Plone Documentation v" + version,
    },
    "navigation_with_keys": True,
    "path_to_docs": "docs",
    "primary_sidebar_end": [
        "version-switcher",
    ],
    "repository_branch": "6.0",
    "repository_url": "https://github.com/plone/documentation",
    "search_bar_text": "Search",
    "show_toc_level": 2,
    "switcher": {
        "json_url": "https://6.docs.plone.org/_static/switcher.json",
        "version_match": version,
    },
    "use_edit_page_button": False,  # This option does not support multiple repositories.
    "use_issues_button": True,
    "use_repository_button": True,
}
# suggest edit link
# remark: {{ file_name }} is mandatory in "edit_page_url_template"
# used by `use_edit_page_button`, but it does not support multiple repositories
# html_context = {
#     "edit_page_url_template": "https://6.docs.plone.org/contributing/documentation/index.html?{{ file_name }}#making-contributions-on-github",
# }

# Announce that we have an opensearch plugin
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_use_opensearch
html_use_opensearch = "https://6.docs.plone.org"

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "%(project)s v%(release)s" % {"project": project, "release": release}

# If false, no index is generated.
html_use_index = True

html_css_files = [("print.css", {"media": "print"})]
html_js_files = []

html_extra_path = [
    "robots.txt",
]
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = [
    "volto/_static",
    "_static",  # Last path wins. See https://github.com/plone/documentation/pull/1442
]


# -- Options for autodoc ----------------------------------------------------

# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration
# Automatically extract typehints when specified and place them in
# descriptions of the relevant function/method.
# autodoc_typehints = "description"

# Don't show class signature with the class' name.
autodoc_class_signature = "separated"

# -- Options for MyST markdown conversion to HTML -----------------------------

# For more information see:
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    "deflist",  # Support definition lists.
    # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#definition-lists
    "linkify",  # Identify "bare" web URLs and add hyperlinks.
    "colon_fence",  # You can also use ::: delimiters to denote code fences,\
    #  instead of ```.
    "substitution",  # plone.restapi \
    # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#substitutions-with-jinja2
    "html_image",  # For inline images. See https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#html-images
]

myst_substitutions = {
    "postman_basic_auth": "![](../_static/img/postman_basic_auth.png)",
    "postman_headers": "![](../_static/img/postman_headers.png)",
    "postman_request": "![](../_static/img/postman_request.png)",
    "postman_response": "![](../_static/img/postman_response.png)",
    "postman_retain_headers": "![](../_static/img/postman_retain_headers.png)",
    "fawrench": '<span class="fa fa-wrench" style="font-size: 1.6em;"></span>',
    "SUPPORTED_PYTHON_VERSIONS_PLONE60": "3.9, 3.10, 3.11, 3.12, or 3.13",
    "SUPPORTED_PYTHON_VERSIONS_PLONE61": "3.10, 3.11, 3.12, or 3.13",
}


# -- Intersphinx configuration ----------------------------------

# This extension can generate automatic links to the documentation of objects
# in other projects. Usage is simple: whenever Sphinx encounters a
# cross-reference that has no matching target in the current documentation set,
# it looks for targets in the documentation sets configured in
# intersphinx_mapping. A reference like :py:class:`zipfile.ZipFile` can then
# linkto the Python documentation for the ZipFile class, without you having to
# specify where it is located exactly.
#
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
#
# Note that Plone Documentation imports documentation from several remote repositories.
# These projects need to build their docs as part of their CI/CD and testing.
# We use Intersphinx to resolve targets when either the individual project's or
# the entire Plone Documentation is built.
intersphinx_mapping = {
    "plone": ("https://6.docs.plone.org/", None),  # for imported packages
    "plone5": ("https://5.docs.plone.org/", None),
    "python": ("https://docs.python.org/3/", None),
    "training": ("https://training.plone.org/", None),
    "training-2022": ("https://2022.training.plone.org/", None),
    "training-2023": ("https://2023.training.plone.org/", None),
}


# -- GraphViz configuration ----------------------------------

graphviz_output_format = "svg"


# -- Mermaid configuration ----------------------------------
mermaid_version = "11.2.0"


# -- OpenGraph configuration ----------------------------------

ogp_site_url = "https://6.docs.plone.org/"
ogp_description_length = 200
ogp_image = "https://6.docs.plone.org/_static/Plone_logo_square.png"
ogp_site_name = "Plone Documentation"
ogp_type = "website"
ogp_custom_meta_tags = [
    '<meta property="og:locale" content="en_US" />',
]


# -- Options for sphinx.ext.todo -----------------------

# See http://sphinx-doc.org/ext/todo.html#confval-todo_include_todos
todo_include_todos = True


# -- Options for sphinx-notfound-page ----------------------------------

notfound_urls_prefix = ""
notfound_template = "404.html"


# -- sphinx-reredirects configuration ----------------------------------
# https://documatt.com/sphinx-reredirects/usage.html
redirects = {
    "contributing/plone-api": "/plone.api/contribute.html",
    "contributing/plone-restapi": "/plone.restapi/docs/source/contributing/index.html",
    "contributing/volto": "/volto/contributing/index.html",
    "install/install-from-packages": "/install/create-project.html",
    "manage/frontend": "/volto/addons/index.html",
}


# -- Options for sphinx_sitemap to HTML -----------------------------

# Used by sphinx_sitemap to generate a sitemap
html_baseurl = "https://6.docs.plone.org/"
# https://sphinx-sitemap.readthedocs.io/en/latest/advanced-configuration.html#customizing-the-url-scheme
sitemap_url_scheme = "{link}"
sitemap_filename = "sitemap-custom.xml"


# -- Options for HTML help output -------------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "PloneDocumentation"


# -- Options for LaTeX output -------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual])
latex_documents = [
    (
        "index",
        "PloneDocumentation.tex",
        "Plone Documentation",
        "Plone community",
        "manual",
    ),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = "_static/logo_2x.png"

# --  Configuration for source_replacements extension -----------------------

# An extension that allows replacements for code blocks that
# are not supported in `rst_epilog` or other substitutions.
# https://stackoverflow.com/a/56328457/2214933
def source_replace(app, docname, source):
    result = source[0]
    for key in app.config.source_replacements:
        result = result.replace(key, app.config.source_replacements[key])
    source[0] = result


# Dict of replacements.
source_replacements = {
    "{PLONE_BACKEND_MINOR_VERSION}": "6.0",
}

# Finally, configure app attributes.
def setup(app):
    app.add_config_value("source_replacements", {}, True)
    app.connect("source-read", source_replace)
    app.add_config_value("context", "documentation", "env")
