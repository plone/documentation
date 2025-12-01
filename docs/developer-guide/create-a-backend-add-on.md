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

## Generate the add-on project with `cookieplone`

To develop an add-on for backend and/or Classic-UI, run the following command to generate your add-on project using the `backend_addon` Cookieplone template.
See {doc}`plone:install/create-project-cookieplone` for details of the latter scenario.
The following output assumes the former scenario.

```shell
uvx cookieplone backend_addon
```

```console
> uvx cookieplone backend_addon
╭──────────────────────────────── cookieplone ─────────────────────────────────╮
│                                                                              │
│                                   *******                                    │
│                               ***************                                │
│                             ***             ***                              │
│                           ***    ***          ***                            │
│                          ***    *****          ***                           │
│                         ***      ***            ***                          │
│                         ***               ***   ***                          │
│                         ***              *****  ***                          │
│                         ***      ***      ***   ***                          │
│                          ***    *****          ***                           │
│                           ***    ***          ***                            │
│                             ***             ***                              │
│                               ***************                                │
│                                   *******                                    │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
You've downloaded /Users/<username>/.cookiecutters/cookieplone-templates before. Is
it okay to delete and re-download it? [y/n] (y):
╭──────────────────────────────── Plone Addon ─────────────────────────────────╮
│                                                                              │
│ Creating a new Plone Addon                                                   │
│                                                                              │
│ Sanity check results:                                                        │
│                                                                              │
│   - Cookieplone: ✓                                                           │
│   - uv: ✓                                                                    │
│   - git: ✓                                                                   │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
  [1/10] Addon Title (Addon):
  [2/10] A short description of your addon (A new addon for Plone):
  [3/10] Author (Plone Community):
  [4/10] Author E-mail (collective@plone.org):
  [5/10] GitHub Username or Organization (collective):
  [6/10] Should we use prerelease versions? (No):
  [7/10] Plone Version (6.1.3):
  [8/10] Python package name (collective.addon):
  [9/10] Support headless Plone?
    1 - Yes
    2 - No
    Choose from [1/2] (1):
  [10/10] Would you like to add a documentation scaffold to your project?
    1 - Yes
    2 - No
    Choose from [1/2] (1):
 -> Remove files used in classic UI setup
 -> Create namespace packages
 -> Format code
 -> Initialize Git repository
 -> Generate documentation scaffold
╭────────────────────────── New addon was generated ───────────────────────────╮
│                                                                              │
│ Addon                                                                        │
│                                                                              │
│ Now, enter the repository, start coding, and push to your organization.      │
│                                                                              │
│ Sorry for the convenience,                                                   │
│ The Plone Community.                                                         │
│                                                                              │
│ https://plone.org/                                                           │
╰──────────────────────────────────────────────────────────────────────────────╯
```

Cookieplone creates a folder with the name of the add-on, in this example, `collective.addon`.

You can now continue to add subtemplates to your addon {ref}`create-a-backend-add-on-add-subtemplate-label`


(create-a-backend-add-on-add-subtemplate-label)=

## Add `plonecli` subtemplate to an addon

The generated addon contains a {file}`bobtemplates.cfg` file which lets you add several subtemplates with `plonecli`.

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
