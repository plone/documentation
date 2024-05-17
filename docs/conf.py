# Configuration file for the Sphinx documentation builder.
# Plone Documentation build configuration file


# -- Path setup --------------------------------------------------------------

from datetime import datetime

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# Attempt to make plone.api importable to Sphinx
sys.path.insert(0, os.path.abspath(os.path.join("..", "..")))


# -- Project information -----------------------------------------------------

project = "Plone Documentation"
copyright = "Plone Foundation"
author = "Plone Community"
trademark_name = "Plone"
now = datetime.now()
year = str(now.year)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = "6.0"
# The full version, including alpha/beta/rc tags.
release = "6.0"

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
    "sphinxcontrib.video",
    "sphinxext.opengraph",
]

# If true, the Docutils Smart Quotes transform, originally based on SmartyPants
# (limited to English) and currently applying to many languages, will be used
# to convert quotes and dashes to typographically correct entities.
# Note to maintainers: setting this to `True` will cause contractions and
# hyphenated words to be marked as misspelled by spellchecker.
smartquotes = False

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = "sphinx.pygments_styles.PyramidStyle"
pygments_style = "sphinx"

# Options for the linkcheck builder
# Ignore localhost
linkcheck_ignore = [
    # Ignore local and example URLs
    r"http://0.0.0.0",
    r"http://127.0.0.1",
    r"http://localhost",
    r"http://yoursite",
    # Ignore file downloads
    r"^/_static/",
    # Ignore pages that require authentication
    r"https://github.com/orgs/plone/teams/",  # requires auth
    r"https://github.com/plone/documentation/issues/new/choose",  # requires auth
    r"https://github.com/plone/volto/issues/new/choose",  # requires auth
    # Ignore github.com pages with anchors
    r"https://github.com/.*#.*",
    # Ignore other specific anchors
    r"https://coveralls.io/repos/github/plone/plone.restapi/badge.svg\?branch=main",  # plone.restapi
    r"https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors#Identifying_the_issue",
    r"https://docs.cypress.io/guides/references/migration-guide#Migrating-to-Cypress-version-10-0",  # volto
    # Ignore unreliable sites
    r"https://chromewebstore.google.com/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi",  # TODO retest with latest Sphinx when upgrading theme. chromewebstore recently changed its URL and has "too many redirects".
    r"https://chromewebstore.google.com/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd",  # TODO retest with latest Sphinx when upgrading theme. chromewebstore recently changed its URL and has "too many redirects".
    r"https://stackoverflow.com",  # volto and documentation  # TODO retest with latest Sphinx.
    r"https://web.archive.org/",  # volto
    r"https://www.youtube.com/playlist",  # volto, TODO remove after installing sphinxcontrib.youtube
]
linkcheck_anchors = True
linkcheck_timeout = 5
linkcheck_retries = 1

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
    "plone.restapi/.*",
    "plone.restapi/bin",
    "plone.restapi/docs/source/glossary.md",  # There can be only one Glossary.
    "plone.restapi/ideas",
    "plone.restapi/include",
    "plone.restapi/lib",
    "plone.restapi/news",
    "plone.restapi/performance",
    "plone.restapi/src",
    "volto/contributing/branch-policy.md",
    "volto/contributing/install-docker.md",
    "volto/contributing/install-git.md",
    "volto/contributing/install-make.md",
    "volto/contributing/install-nodejs.md",
    "volto/contributing/install-operating-system.md",
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
html_theme_options = {
    "article_header_start": ["toggle-primary-sidebar"],
    "extra_footer": """<p>The text and illustrations in this website are licensed by the Plone Foundation under a Creative Commons Attribution 4.0 International license. Plone and the Plone® logo are registered trademarks of the Plone Foundation, registered in the United States and other countries. For guidelines on the permitted uses of the Plone trademarks, see <a href="https://plone.org/foundation/logo">https://plone.org/foundation/logo</a>. All other trademarks are owned by their respective owners.</p>
<p>Pull request previews by <a href="https://readthedocs.org/">Read the Docs</a></p>""",
    "footer_end": ["version.html"],
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
            "name": "Twitter",
            "url": "https://twitter.com/plone",
            "icon": "fa-brands fa-square-twitter",
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
    ],
    "logo": {
        "text": "Plone Sphinx Theme",
    },
    "navigation_with_keys": True,
    "path_to_docs": "docs",
    "repository_branch": "6.0",
    "repository_url": "https://github.com/plone/documentation",
    "search_bar_text": "Search",  # TODO: Confirm usage of search_bar_text in plone-sphinx-theme
    "switcher": {
        "json_url": "/_static/switcher.json",
        "version_match": version,
    },
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
}

html_context = {  # TODO: verify html_context usage in plone-sphinx-theme
    "edit_page_url_template": "https://6.docs.plone.org/contributing/index.html?{{ file_name }}#making-contributions-on-github",
}

# Announce that we have an opensearch plugin
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_use_opensearch
html_use_opensearch = "https://6.docs.plone.org"  # TODO: Confirm usage of opensearch in theme

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "%(project)s v%(release)s" % {"project": project, "release": release}

# If false, no index is generated.
html_use_index = True

html_css_files = ["custom.css", ("print.css", {"media": "print"})]
# html_js_files = ["patch_scrollToActive.js", "search_shortcut.js"]  ## TODO: Remove patches
html_extra_path = [
    "robots.txt",
]
html_static_path = [
    "volto/_static",
    "_static",  # Last path wins. See https://github.com/plone/documentation/pull/1442
]


# -- Options for sphinx_sitemap to html -----------------------------

# Used by sphinx_sitemap to generate a sitemap
html_baseurl = "https://6.docs.plone.org/"
# https://sphinx-sitemap.readthedocs.io/en/latest/advanced-configuration.html#customizing-the-url-scheme
sitemap_url_scheme = "{link}"


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
    "python": ("https://docs.python.org/3/", None),
    "training": ("https://training.plone.org/", None),
    "training-2022": ("https://2022.training.plone.org/", None),
}


# -- GraphViz configuration ----------------------------------

graphviz_output_format = "svg"


# -- OpenGraph configuration ----------------------------------

ogp_site_url = "https://6.docs.plone.org/"
ogp_description_length = 200
ogp_image = "https://6.docs.plone.org/_static/Plone_logo_square.png"
ogp_site_name = "Plone Documentation"
ogp_type = "website"
ogp_custom_meta_tags = [
    '<meta property="og:locale" content="en_US" />',
]


# -- sphinx.ext.todo -----------------------
# See http://sphinx-doc.org/ext/todo.html#confval-todo_include_todos
todo_include_todos = True


# -- sphinx-notfound-page configuration ----------------------------------

notfound_urls_prefix = ""
notfound_template = "404.html"


# -- sphinx-reredirects configuration ----------------------------------
# https://documatt.com/sphinx-reredirects/usage.html
redirects = {
    "contributing/plone-api": "/plone.api/contribute/index.html",
    "contributing/plone-restapi": "/plone.restapi/docs/source/contributing/index.html",
    "contributing/volto": "/volto/contributing/index.html",
    "install/install-from-packages": "/install/create-project.html",
}


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
        "The Plone community",
        "manual",
    ),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = "_static/logo_2x.png"


# suggest edit link
# remark: {{ file_name }} is mandatory in "edit_page_url_template"
html_context = {
    "edit_page_url_template": "https://6.docs.plone.org/contributing/index.html?{{ file_name }}#making-contributions-on-github",
}

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
    "{PLONE_BACKEND_PATCH_VERSION}": "6.0.11",
    "{NVM_VERSION}": "0.39.5",
    "{SUPPORTED_PYTHON_VERSIONS}": "3.8, 3.9, 3.10, 3.11, or 3.12",
}


def setup(app):
    app.add_config_value("source_replacements", {}, True)
    app.connect("source-read", source_replace)
    app.add_config_value("context", "documentation", "env")
