# Makefile for Sphinx documentation
.DEFAULT_GOAL   = help
SHELL           = bash

# You can set these variables from the command line.
SPHINXOPTS      ?=
PAPER           ?=
VALEOPTS        ?=

# Internal variables.
SPHINXBUILD     = "$(realpath venv/bin/sphinx-build)"
SPHINXAUTOBUILD = "$(realpath venv/bin/sphinx-autobuild)"
DOCS_DIR        = ./docs/
BUILDDIR        = ../_build
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
VALEFILES       := $(shell find -L $(DOCS_DIR) -type d \( -path $(DOCS_DIR)/plone.restapi/lib/* -o  -path $(DOCS_DIR)"/plone.restapi/performance/*" \) -prune -false -o -type f -name "*.md" -print)

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help:  # This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean:  ## Clean docs build directory
	cd $(DOCS_DIR) && rm -rf $(BUILDDIR)/

.PHONY: distclean
distclean: clean ## Clean docs build directory, Python virtual environment, and symlinks
	rm -rf venv
	rm docs/plone.api
	rm docs/plone.restapi
	rm docs/volto
	@echo "Cleaned docs build directory, Python virtual environment, and symlinks."
	@echo

venv/bin/python:  ## Setup up Python virtual environment and install requirements
	python3 -m venv venv
	venv/bin/pip install -r requirements-initial.txt
	venv/bin/pip install -r requirements.txt
	@echo "Installation of requirements completed."
	@echo

docs/plone.api:  ## Setup plone.api docs
	git submodule init
	git submodule update
	ln -s ../submodules/plone.api/docs ./docs/plone.api
	@echo "Documentation of plone.api initialized."
	@echo

venv/plone.api-install: docs/plone.api
	touch venv/plone.api-install
	venv/bin/pip install plone.api -c submodules/plone.api/constraints.txt
	venv/bin/pip install --no-deps -e submodules/plone.api/"[test]"
	@echo "plone.api installed."
	@echo

docs/plone.restapi:  ## Setup plone.restapi docs
	git submodule init
	git submodule update
	ln -s ../submodules/plone.restapi ./docs/plone.restapi
	@echo "Documentation of plone.restapi initialized."
	@echo

docs/volto:  ## Setup Volto docs
	git submodule init
	git submodule update
	ln -s ../submodules/volto/docs/source ./docs/volto
	@echo "Documentation of volto initialized."
	@echo

.PHONY: deps
deps: venv/bin/python docs/volto docs/plone.restapi venv/plone.api-install  ## Create Python virtual environment, install requirements, initialize or update the volto, plone.restapi, and plone.api submodules, create symlinks to the source files, and finally install plone.api.

.PHONY: html
html: deps  ## Build html
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."
	@echo

.PHONY: manual
manual: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b html -t manual . $(BUILDDIR)/manual
	@echo "Build finished. The manual pages are in $(BUILDDIR)/manual."
	@echo

.PHONY: dirhtml
dirhtml: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."
	@echo

.PHONY: singlehtml
singlehtml: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."
	@echo

.PHONY: pickle
pickle: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) $(BUILDDIR)/pickle
	@echo "Build finished; now you can process the pickle files."
	@echo

.PHONY: json
json: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
	@echo "Build finished; now you can process the JSON files."
	@echo

.PHONY: htmlhelp
htmlhelp: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in $(BUILDDIR)/htmlhelp."
	@echo

.PHONY: epub
epub: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b epub $(ALLSPHINXOPTS) $(BUILDDIR)/epub
	@echo "Build finished. The epub file is in $(BUILDDIR)/epub."
	@echo

.PHONY: latex
latex: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
	@echo "Run \`make' in that directory to run these through (pdf)latex" \
	      "(use \`make latexpdf' here to do that automatically)."
	@echo

.PHONY: latexpdf
latexpdf: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."
	@echo

.PHONY: text
text: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
	@echo "Build finished. The text files are in $(BUILDDIR)/text."
	@echo

.PHONY: man
man: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man
	@echo "Build finished. The manual pages are in $(BUILDDIR)/man."
	@echo

.PHONY: texinfo
texinfo: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo "Build finished. The Texinfo files are in $(BUILDDIR)/texinfo."
	@echo "Run \`make' in that directory to run these through makeinfo" \
	      "(use \`make info' here to do that automatically)."
	@echo

.PHONY: info
info: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo "Running Texinfo files through makeinfo..."
	make -C $(BUILDDIR)/texinfo info
	@echo "makeinfo finished; the Info files are in $(BUILDDIR)/texinfo."
	@echo

.PHONY: changes
changes: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo "The overview file is in $(BUILDDIR)/changes."
	@echo

.PHONY: linkcheck
linkcheck: deps  ## Run linkcheck
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo "Link check complete; look for any errors in the above output " \
		"or in $(BUILDDIR)/linkcheck/ ."
	@echo

.PHONY: linkcheckbroken
linkcheckbroken: deps  ## Run linkcheck and show only broken links
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck | GREP_COLORS='0;31' grep -wi "broken\|redirect" --color=always | GREP_COLORS='0;31' grep -vi "https://github.com/plone/volto/issues/" --color=always && if test $$? = 0; then exit 1; fi || test $$? = 1
	@echo "Link check complete; look for any errors in the above output " \
		"or in $(BUILDDIR)/linkcheck/ ."
	@echo

.PHONY: vale
vale: deps  ## Run Vale style, grammar, and spell checks
	venv/bin/vale sync
	venv/bin/vale --no-wrap $(VALEOPTS) $(VALEFILES)
	@echo "Vale is finished; look for any errors in the above output."
	@echo

.PHONY: html_meta
html_meta: deps  ## Add meta data headers to all Markdown pages
	python ./docs/addMetaData.py

.PHONY: doctest
doctest: deps
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."
	@echo

.PHONY: test
test: clean linkcheckbroken  ## Clean docs build, then run linkcheckbroken

.PHONY: deploy
deploy: clean html

.PHONY: livehtml
livehtml: deps  ## Rebuild Sphinx documentation on changes, with live-reload in the browser
	cd "$(DOCS_DIR)" && ${SPHINXAUTOBUILD} \
		--ignore "*.swp" \
		--port 8050 \
		--watch volto \
		--watch plone.api \
		--watch plone.restapi \
		-b html . "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

.PHONY: rtd-pr-preview
rtd-pr-preview:  ## Build pull request preview on Read the Docs
	pip install -r requirements-initial.txt
	pip install -r requirements.txt
	git submodule init
	git submodule update
	pip install plone.api -c submodules/plone.api/constraints.txt
	pip install --no-deps -e submodules/plone.api[test]
	ln -s ../submodules/volto/docs/source ./docs/volto
	ln -s ../submodules/plone.restapi ./docs/plone.restapi
	ln -s ../submodules/plone.api/docs ./docs/plone.api
	cd $(DOCS_DIR) && sphinx-build -b html $(ALLSPHINXOPTS) ${READTHEDOCS_OUTPUT}/html/

.PHONY: storybook
storybook:
	cd submodules/volto && pnpm i && pnpm build:registry && pnpm --filter @plone/volto build-storybook -o ../../../../_build/html/storybook

.PHONY: all
all: clean vale linkcheck html  ## Clean docs build, then run vale and linkcheck, and build html
