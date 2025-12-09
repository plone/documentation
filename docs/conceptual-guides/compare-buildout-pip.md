---
myst:
  html_meta:
    "description": "Compare Plone Classic UI's installation tools, Buildout and pip"
    "property=og:description": "Compare Plone Classic UI's installation tools, Buildout and pip"
    "property=og:title": "Compare Buildout and pip"
    "keywords": "Plone 6, Conceptual guides, Classic UI, Buildout, pip, install"
---

(compare-buildout-pip-label)=

# Compare Buildout and pip

This guide explains the differences between two tools, {term}`Buildout` and {term}`pip`, to install Plone and its Classic UI user interface, helping to inform your choice when developing your new project in Plone.

The choice of installation tool has implications for admins and developers.

````{grid} 1 1 1 2
:gutter: 1
:margin: 0
:padding: 0

```{grid-item-card} Buildout
-   You can create recipes to automate development and production installations.
-   Maintained and used primarily by the small Plone community.
-   May have problems resolving dependencies when a new pip or setuptools version is released.
-   Source checkouts managed through {term}`mr.developer`.
```

```{grid-item-card} pip
-   Installs or uninstalls packages only.
-   Maintained and used by the large Python community.
-   Changes in dependency resolution are well-documented.
-   Source checkouts managed through {term}`mxdev`.
```
````

```{seealso}
[Proposal: Use pip constraints as canonical version location #3670](https://github.com/plone/Products.CMFPlone/issues/3670)
```