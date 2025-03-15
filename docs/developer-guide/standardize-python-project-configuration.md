---
myst:
  html_meta:
    "description": "Standardize project configuration in Plone with plone.meta"
    "property=og:description": "Standardize project configuration in Plone with plone.meta"
    "property=og:title": "Standardize project configuration in Plone with plone.meta"
    "keywords": "Plone 6, standardize, project, configuration, development, plone.meta"
---

# Standardize Python project configuration

This part of the documentation describes how to standardize Python project configuration in Plone.
It does not cover the following.

-   Volto or any other JavaScript-based project, which has its own ecosystem.
-   Monorepo projects with backend and frontend code bases, such as those created by [Cookieplone](https://github.com/plone/cookieplone).
    Repositories must have a single Python package at the top level.
-   Projects that support multiple versions of Plone in the same branch.

Plone consists of hundreds of projects.
To lessen the effort of configuring a new project in the Plone GitHub organization, and to keep these projects current with latest configuration practices, the Plone community agreed upon a trusted set of configuration items.
The Plone community manages these configuration items using the [`plone.meta`](https://github.com/plone/meta) project.

You can follow these practices in your own projects, or suggest new or alternative configuration items through the `plone.meta` repository, sharing them with the rest of the Plone community.

```{seealso}
See also [`plone/meta` documentation](https://github.com/plone/meta?tab=readme-ov-file#setup) for setup and usage.
```
