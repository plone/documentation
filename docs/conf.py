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
author = "the Plone community"
trademark_name = "Plone"
now = datetime.now()
year = str(now.year)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = "6.0-dev"
# The full version, including alpha/beta/rc tags.
release = "6.0-dev"

# -- General configuration ----------------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Add any Sphinx extension module names here, as strings.
# They can be extensions coming with Sphinx (named "sphinx.ext.*")
# or your custom ones.
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx_copybutton",
    "sphinx_sitemap",
    "sphinxcontrib.httpdomain",  # plone.restapi
    "sphinxcontrib.httpexample",  # plone.restapi
    "sphinxcontrib.spelling",
    "sphinxext.opengraph",
    "sphinx.ext.viewcode",  # plone.api
    "sphinx.ext.autosummary",  # plone.api
    "sphinx.ext.graphviz",
]

graphviz_output_format = 'svg'

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
    r"http://localhost",
    r"http://0.0.0.0",
    r"http://127.0.0.1",
    r"https://www.linode.com",
    r"https://github.com/plone/documentation/issues/new/choose",  # requires auth
    # Ignore specific anchors
    r"https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors#Identifying_the_issue",
    r"https://github.com/browserslist/browserslist#queries",
    r"https://github.com/plone/cookiecutter-zope-instance#options",
    r"https://github.com/plone/plone.docker#for-basic-usage",
    r"https://github.com/plone/plone.rest#cors",
    r"https://github.com/plone/plone.volto/blob/6f5382c74f668935527e962490b81cb72bf3bc94/src/kitconcept/volto/upgrades.py#L6-L54",
    r"https://github.com/tc39/proposals/blob/HEAD/finished-proposals.md#finished-proposals",
    r"https://coveralls.io/repos/github/plone/plone.restapi/badge.svg\?branch=master",  # plone.restapi
    r"https://github.com/plone/plone.restapi/blob/dde57b88e0f1b5f5e9f04e6a21865bc0dde55b1c/src/plone/restapi/services/content/add.py#L35-L61",  # plone.restapi
]
linkcheck_anchors = True
linkcheck_timeout = 10
linkcheck_retries = 2

# This is our wordlist with known words, like Github or Plone ...
spelling_word_list_filename = "spelling_wordlist.txt"
spelling_ignore_pypi_package_names = True

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
    "plone.restapi/ideas",
    "plone.restapi/include",
    "plone.restapi/lib",
    "plone.restapi/news",
    "plone.restapi/performance",
    "plone.restapi/src",
]

html_extra_path = [
    "robots.txt",
]

html_static_path = [
    "_static",
    "volto/_static/*.png",
    "volto/_static/*.jpg",
]

# -- Options for myST markdown conversion to html -----------------------------

# For more information see:
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    "deflist",  # You will be able to utilise definition lists
    # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#definition-lists
    "linkify",  # Identify “bare” web URLs and add hyperlinks.
    "colon_fence",  # You can also use ::: delimiters to denote code fences,\
    #  instead of ```.
    "substitution",  # plone.restapi \
    # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#substitutions-with-jinja2
]

myst_substitutions = {
    "postman_basic_auth": "![](_static/img/postman_basic_auth.png)",
    "postman_headers": "![](_static/img/postman_headers.png)",
    "postman_request": "![](_static/img/postman_request.png)",
    "postman_response": "![](_static/img/postman_response.png)",
    "postman_retain_headers": "![](_static/img/postman_retain_headers.png)",
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
    "plone": ("https://6.dev-docs.plone.org/", None),  # for imported packages
    "python": ("https://docs.python.org/3/", None),
    "training": ("https://training.plone.org/5/", None),
}


# -- GraphViz configuration ----------------------------------

graphviz_output_format = "svg"


# -- OpenGraph configuration ----------------------------------

ogp_site_url = "https://6.dev-docs.plone.org/"
ogp_description_length = 200
ogp_image = "https://6.dev-docs.plone.org/_static/Plone_logo_square.png"
ogp_site_name = "Plone Documentation"
ogp_type = "website"
ogp_custom_meta_tags = [
    '<meta property="og:locale" content="en_US" />',
]


# -- sphinx_copybutton -----------------------
copybutton_prompt_text = r"^ {0,2}\d{1,3}"
copybutton_prompt_is_regexp = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.ico"

html_css_files = ["custom.css", ("print.css", {"media": "print"})]

# See http://sphinx-doc.org/ext/todo.html#confval-todo_include_todos
todo_include_todos = True

# Announce that we have an opensearch plugin
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_use_opensearch
html_use_opensearch = "https://docs.plone.org"

html_theme_options = {
    "google_analytics_id": "G-P8NCTB796E",
    "path_to_docs": "docs",
    "repository_url": "https://github.com/plone/documentation",
    "repository_branch": "main",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "extra_navbar": """
    <p class="ploneorglink">
        <a href="https://plone.org">
            <img src="/_static/logo.svg" alt="plone.org" /> plone.org</a>
    </p>""",
    "extra_footer": """<p>The text and illustrations in this website are licensed by the Plone Foundation under a Creative Commons Attribution 4.0 International license. Plone and the Plone® logo are registered trademarks of the Plone Foundation, registered in the United States and other countries. For guidelines on the permitted uses of the Plone trademarks, see <a href="https://plone.org/foundation/logo">https://plone.org/foundation/logo</a>. All other trademarks are owned by their respective owners.</p>
    <p><a href="https://www.netlify.com">
  <img src="https://www.netlify.com/img/global/badges/netlify-color-bg.svg" alt="Deploys by Netlify" />
</a></p>""",
}

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "%(project)s v%(release)s" % {"project": project, "release": release}

# If false, no index is generated.
html_use_index = True

# Used by sphinx_sitemap to generate a sitemap
html_baseurl = "https://6.dev-docs.plone.org"

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
    "edit_page_url_template": "https://6.dev-docs.plone.org/contributing/index.html?{{ file_name }}#making-contributions-on-github",
}
