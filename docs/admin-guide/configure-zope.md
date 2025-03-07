---
myst:
  html_meta:
    "description": "Configure Zope options"
    "property=og:description": "Configure Zope options"
    "property=og:title": "Configure Zope"
    "keywords": "Plone 6, Zope, instance, app server, config, Cookieplone, Buildout, pip, cookiecutter-zope-instance, plone.recipe.zope2instance"
---

(configure-zope-label)=

# Configure Zope

Plone runs in an application server called {term}`Zope`.

You can configure your Zope instance's options, including the following.

-   persistent storage: blobs, direct file storage, relational database, ZEO, and other storage mechanisms
-   ports
-   threads
-   cache
-   logging
-   debugging and profiling for development


## Cookieplone

If you installed Plone using Cookieplone or pip, then Zope is configured using {term}`cookiecutter-zope-instance`.
For a complete list of features, usage, and options, read [`cookiecutter-zope-instance`'s README](https://github.com/plone/cookiecutter-zope-instance#readme).


## Buildout

If you installed Plone using Buildout, then Zope is configured using `plone.recipe.zope2instance`.
For a complete list of features, usage, and options, read [`plone.recipe.zope2instance`'s README](https://pypi.org/project/plone.recipe.zope2instance/).
