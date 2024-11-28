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
    "sphinx_reredirects",
]

# If true, the Docutils Smart Quotes transform, originally based on SmartyPants
# (limited to English) and currently applying to many languages, will be used
# to convert quotes and dashes to typographically correct entities.
# Note to maintainers: setting this to `True` will cause contractions and
# hyphenated words to be marked as misspelled by spellchecker.
smartquotes = False

# The suffix of source filenames.
source_suffix = {
    ".md": "markdown",
}

# The master toctree document.
master_doc = "index"


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
    "repository_branch": "6.0",
    "repository_url": "https://github.com/plone/documentation",
    "search_bar_text": "Search",
    "use_edit_page_button": False,  # This option does not support multiple repositories.
    "use_issues_button": True,
    "use_repository_button": True,
}

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "%(project)s v%(release)s" % {"project": project, "release": release}

# If false, no index is generated.
html_use_index = True

html_js_files = []

html_extra_path = [
    "robots.txt",
]
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = [
    "_static",  # Last path wins. See https://github.com/plone/documentation/pull/1442
]


# -- Options for MyST markdown conversion to HTML -----------------------------

# For more information see:
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    "linkify",  # Identify "bare" web URLs and add hyperlinks.
]

# -- Options for sphinx-notfound-page ----------------------------------

notfound_urls_prefix = ""
notfound_template = "404.html"


# -- sphinx-reredirects configuration ----------------------------------
# https://documatt.com/sphinx-reredirects/usage.html
redirects = {
    "**": "https://6.docs.plone.org/",
}
