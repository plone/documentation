---
myst:
  html_meta:
    "description": "Mockup together with Patternslib are used to build the UI toolkit for Classic UI, a frontend for Plone."
    "property=og:description": "Mockup together with Patternslib are used to build the UI toolkit for Classic UI, a frontend for Plone."
    "property=og:title": "Mockup and Patternslib"
    "keywords": "Mockup, Patternslib, Classic UI, plonecli, bobtemplates.plone, mr.bob, frontend, Plone"
---

(mockup-and-patternslib-label)=

# Mockup and Patternslib

{term}`Mockup` together with {term}`Patternslib` are used to build the UI toolkit for {term}`Classic UI`, a frontend for Plone.

View the [interactive documentation of Mockup](https://plone.github.io/mockup/).


## Get started

[bobtemplates.plone](https://github.com/plone/bobtemplates.plone) provides [mr.bob](https://mrbob.readthedocs.io/en/latest/) templates to generate packages for Plone projects.
[plonecli](https://github.com/plone/plonecli) provides a command line client for bobtemplates.plone.

Install plonecli into your Python user packages to make it available to all your projects.

```shell
pip install plonecli --user
```

Create a theme package add-on with {term}`plonecli`.

```shell
plonecli add mockup_pattern
```


## References

-   {ref}`v60-mockup-resource-registry-label` in Plone 6.0
-   [Mockup repository on GitHub](https://github.com/plone/mockup)
-   [Patternslib](https://patternslib.com/)
