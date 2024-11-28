# Makefile for Sphinx documentation
.DEFAULT_GOAL   = help
SHELL           = bash

# You can set these variables from the command line.
SPHINXOPTS      ?=
PAPER           ?=

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
	@echo
	@echo "Cleaned docs build directory, Python virtual environment, and symlinks."

venv/bin/python:  ## Setup up Python virtual environment and install requirements
	python3 -m venv venv
	venv/bin/pip install -r requirements-initial.txt
	venv/bin/pip install -r requirements.txt
	@echo
	@echo "Installation of requirements completed."

.PHONY: deps
deps: venv/bin/python  ## Create Python virtual environment and install requirements.

.PHONY: html
html: deps  ## Build html
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

.PHONY: livehtml
livehtml: deps  ## Rebuild Sphinx documentation on changes, with live-reload in the browser
	cd "$(DOCS_DIR)" && ${SPHINXAUTOBUILD} \
		--ignore "*.swp" \
		--port 8050 \
		-b html . "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

.PHONY: rtd-pr-preview
rtd-pr-preview:  ## Build pull request preview on Read the Docs
	pip install -r requirements-initial.txt
	pip install -r requirements.txt
	cd $(DOCS_DIR) && sphinx-build -b html $(ALLSPHINXOPTS) ${READTHEDOCS_OUTPUT}/html/

.PHONY: all
all: clean html  ## Clean docs build, then run vale and linkcheck, and build html
