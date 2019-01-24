# Makefile for lazy people, like me
# The shell we use
SHELL := /bin/bash

# Get version form VERSION
#VERSION := $(shell cat VERSION)
DOCKER := $(bash docker)

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

# Add the following 'help' target to your Makefile
# # And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

.PHONY: html
html: ## Builds HTML of the docs
	@echo "$(YELLOW)==> Building HTML  ....$(RESET)"
	#@cp VERSION source
	docker run --rm -v "${PWD}/source":/build/docs:rw testthedocs/ttd-sphinx html
	#@rm source/VERSION

.PHONY: build
build:
	docker build --no-cache=true --build-arg container_version=$(VERSION) -t $(NAME):$(VERSION) --rm -f dockerfiles/Dockerfile .

.PHONY: push
push: ## Pushes images
	docker push $(NAME):$(VERSION)
	docker push $(NAME):latest

.PHONY: tag_latest
tag_latest: ## Tag image with version and latest tag
	docker tag $(NAME):$(VERSION) $(NAME):latest

.PHONY: last_built_date
last_built_date: ## Show last build date
	docker inspect -f '{{ .Created }}' $(NAME):$(VERSION)

PHONY: check_release_version
check_release_version:
	@if docker images $(NAME) | awk '{ print $$2 }' | grep -q -F $(VERSION); then echo "$(RED)$(NAME) version $(VERSION) is already build !$(RESET)"; false; fi

.PHONY: release
release: check_release_version build tag_latest push ## Combine steps to make release

.PHONY: check-sphinx
check-sphinx: ## Run Sphinx in nitpicky mode
	@echo "$(YELLOW)==> Checking Sphinx build files ...$(RESET)"
	@rm -rf source/_build
	@docker run --rm -v "${PWD}/source":/build/docs:rw testthedocs/ttd-sphinx debug-strict

.PHONY: check-links
check-links: ## Run linkcheck, ignoring "localhost"
	@echo "$(YELLOW)==> Running Linkcheck ...$(RESET)"
	@rm -rf source/_build
	@docker run -it -v "${PWD}/source":/srv/test testthedocs/ttd-linkcheck

.PHONY: check-toctree
check-toctree: ## Checks for for multiple "numbered" entries in toctrees
	@echo "$(YELLOW)==> Checking toctree entries ...$(RESET)"
	@docker run -it -v "${PWD}/source":/build/docs testthedocs/ttd-toctree

.PHONY: check-spaces
check-spaces: ## Checks for trailing spaces on line ends
	@echo "$(YELLOW)==> Checking for trailing spaces on line ends ...$(RESET)"
	@rm -rf source/_build
	@docker run -it -v "${PWD}/source":/build/docs testthedocs/ttd-ts

.PHONY: check-rst
check-rst: ## Runs docs8, rst checks
	@echo "$(YELLOW)==> Running doc8 checks against rst files ...$(RESET)"
	@rm -rf source/_build
	docker run -it -v "${PWD}/source":/srv/data testthedocs/ttd-doc8

.PHONY: check-style
check-style: ## Runs vale style-checks (Plone wording style-guide) against the docs
	@echo "$(YELLOW)==>Running wording style checks ...$(RESET)"
	@docker run --rm -it -v "${PWD}/styles":/styles --rm -v "${PWD}/source":/docs -w /docs testthedocs/plone-vale:latest

.PHONY: check-text
check-text: ## Runs textlint against the docs
	@echo "$(YELLOW)==>Running textlint checks ...$(RESET)"
	@docker run -it -v "${PWD}/source":/srv testthedocs/ttd-textlint *

.PHONY: check-html
check-html: ## Runs validation checks against HTML
	# Use ttd-linkcheck here
	#@echo "$(YELLOW)==>Running HTML tests ...$(RESET)"
	#@rm -rf source/_build
	#@docker run --rm -v "${PWD}/source":/build/docs:rw testthedocs/ttd-sphinx html
	#@docker run -it -v "${PWD}/source":/build/docs testthedocs/ttd-htmltest


.PHONY: checks
checks: check-rst check-toctree check-links check-sphinx ## Runs collection of checks against the docs
