#!/bin/bash
# Dependencies: https://github.com/Gyumeijie/github-files-fetcher
# Script to 'fetch' docs folders from GitHub.

# Vars
ESC_SEQ="\x1b["
COL_RESET=$ESC_SEQ"39;49;00m"
COL_YELLOW=$ESC_SEQ"33;01m"
COL_RED=$ESC_SEQ"31;01m"
COL_GREEN=$ESC_SEQ"32;01m"

fetch_docs() {
    echo -en "$COL_YELLOW Fetching docs $COL_RESET\n"
    # Download plone-ansible (currently hardcoded for testing)
    fetcher --url="https://github.com/plone/ansible-playbook/tree/master/docs" --out="source/install/ansible"
}

fetch_docs
