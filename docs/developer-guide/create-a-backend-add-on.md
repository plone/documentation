---
myst:
  html_meta:
    "description": "How to create a backend add-on"
    "property=og:description": "How to create a backend add-on"
    "property=og:title": "Create a backend add-on"
    "keywords": "Plone 6, backend, add-on"
---

(create-a-backend-add-on-label)=

# Create a backend add-on

This section explains how a developer can create an {term}`add-on` for the Plone backend.

## System requirements

Follow the section {ref}`create-project-cookieplone-system-requirements` to set up your system.

## Generate the add-on project with `plonecli`

Choose your desired local development base folder and run the following command to create an addon project with `plonecli`

```shell
uvx plonecli create addon <addon namespace package>
```

```console
> uvx plonecli create addon collective.addon
RUN: bobtemplates.plone:addon -O collective.addon

Welcome to mr.bob interactive mode. Before we generate directory structure,
some questions need to be answered.

Answer with a question mark to display help.
Values in square brackets at the end of the questions show the default value if
there is no answer.


--> Package description [An add-on for Plone]:

--> Plone version [6.0.0]:

--> Python version for virtualenv [python3]:

--> Do you want me to activate VS Code support? (y/n) [y]:



isort-apply: successful:
isort-apply: install_deps> python -I -m pip install isort -c constraints.txt
isort-apply: commands[0]> isort /Users/<username>/Development/collective.addon/src
/Users/<username>/Development/collective.addon/setup.py
Fixing /Users/<username>/Development/collective.addon/src/collective/addon/testing.py
Fixing /Users/<username>/Development/collective.addon/src/collective/addon/tests/test_setup.py
  isort-apply: OK (2.57=setup[1.94]+cmd[0.63] seconds)
  congratulations :) (2.59 seconds)


Identified `/` as project root containing a file system root.
Sources to be formatted: "Users/<username>/Development/collective.addon/src",
  "Users/<username>/Development/collective.addon/setup.py"
src/collective/__init__.py wasn't modified on disk since last run.
src/collective/addon/browser/__init__.py wasn't modified on disk since last run.
src/collective/addon/locales/__init__.py wasn't modified on disk since last run.
src/collective/addon/tests/__init__.py wasn't modified on disk since last run.
src/collective/addon/interfaces.py already well formatted, good job.
reformatted src/collective/addon/__init__.py
reformatted src/collective/addon/setuphandlers.py
reformatted src/collective/addon/testing.py
reformatted setup.py
reformatted src/collective/addon/locales/update.py
reformatted src/collective/addon/tests/test_setup.py

All done! ✨ 🍰 ✨
6 files reformatted, 5 files left unchanged.

black-enforce: successful:
black-enforce: install_deps> python -I -m pip install black -c constraints.txt
black-enforce: commands[0]> black -v src setup.py
  black-enforce: OK (2.60=setup[2.12]+cmd[0.48] seconds)
  congratulations :) (2.61 seconds)


git init is disabled!
Generated file structure at /Users/<username>/Development/collective.addon/collective.addon
```

Plonecli creates a folder with the name of the add-on, in this example, `collective.addon`.

You can now continue to add subtemplates to your addon.


(create-a-backend-add-on-add-subtemplate-label)=

## Add `plonecli` subtemplate to an addon

The generated addon contains a {file}`bobtemplate.cfg` file which lets you add several subtemplates with `plonecli`.

Run the following command to list the available subtemplates.

```shell
uvx plonecli -l
```

```shell
> uvx plonecli -l
Available mr.bob templates:
 - addon
  - behavior
  - content_type
  - controlpanel
  - form
  - indexer
  - mockup_pattern
  - portlet
  - restapi_service
  - site_initialization
  - subscriber
  - svelte_app
  - theme
  - theme_barceloneta
  - theme_basic
  - upgrade_step
  - view
  - viewlet
  - vocabulary
 - buildout
 ```

 All templates below `addon` can be added to your newly created addon with:

 ```shell
 make add <subtemplate>
 ```

Currently documented subtemplates:

- behavior: {ref}`backend-behaviors-label`
- content_type: {ref}`creating-content-types-label`
- controlpanel: {ref}`control-panels-label`
- form: {reg}`forms-label`
- mockup_pattern: {ref}`mockup-and-patternslib-label`
- theme_barceloneta: {ref}`create-a-theme-add-on-label`


The addon also contains a {term}`GenericSetup` default install/uninstall profile.

See {ref}`genericsetup-label` for more information.
