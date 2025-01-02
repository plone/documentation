---
myst:
  html_meta:
    "description": "Standardize project configuration in Plone"
    "property=og:description": "Standardize project configuration in Plone"
    "property=og:title": "Standardize project configuration in Plone"
    "keywords": "Plone 6, standardize, project, configuration, development"
---

# Standardize project configuration

This part of the documentation describes how to standardize project configuration in Plone.

Plone consists of hundreds of projects.
To lessen the effort of configuring a new project in the Plone GitHub organization, and keeping these projects current with latest configuration practices, the Plone community agreed upon a trusted set of configuration items.
The Plone community manages these configuration items using the [`meta`](https://github.com/plone/meta) project.

You can follow these practices in your own projects, or suggest new or alternative configuration items through the `meta` repository, sharing them with the rest of the Plone community.


## `meta` basic usage

`meta` has a rich set of features.
This section describes the most common use cases.

Begin by cloning `meta` to any machine, then changing your current working directory into `meta`.

```shell
git clone https://github.com/plone/meta.git
cd meta
```

Now you can run its Python scripts to generate configuration files to manage your project or any project that already uses `meta`.
When you run the script {file}`.py`, it will 