---
myst:
  html_meta:
    "description": "How to upgrade to Plone 6.2"
    "property=og:description": "How to upgrade to Plone 6.2"
    "property=og:title": "How to upgrade to Plone 6.2"
    "keywords": "Upgrade, Plone 6"
---

(backend-upgrade-plone-v62-label)=

# Upgrade Plone 6.1 to 6.2

Plone 6.2 has seen the following major changes.
Some may require changes in your setup.


## Move to native namespaces

Plone 6.2 has migrated all core Python packages from `pkg_resources`-style namespaces to native namespaces.

The Plone Python backend consists of over 200 packages.
Most of these are namespace packages.
Examples are `plone.batching` and `plone.api`, which share the `plone` namespace.

There are three styles or techniques of namespaces.
For Plone only two are important: `pkg_resources` and native.
The third style is `pkgutil`, but Plone has never used it.

Native namespaces are also referred to as implicit namespaces.
The two terms mean the same.

```{seealso}
- [Python Packaging Guide on native namespaces](https://packaging.python.org/en/latest/guides/.packaging-namespace-packages/#native-namespace-packages)
- [PEP 420 - Implicit Namespace Packages](https://peps.python.org/pep-0420/)
```

Native namespaces exist since Python 3.3.
Because Plone started in the days of Python 2, it has always used `pkg_resources`.
`pkg_resources` is part of the `setuptools` package.
This part is deprecated.
It's scheduled to be removed around the end of 2025, in `setuptools` 81.
This means Plone needs to move to native namespaces.

In general, this move shouldn't cause problems for integrators.
To install Plone 6.2 you can keep using the same version of `pip` (or `uv`), or `zc.buildout` as you do for Plone 6.1.
This assumes that all packages within one namespace use the same namespace style or technique.

You may encounter problems when this assumption isn't true.
As an example, say your Plone project uses a package `collective.example`, and this still uses `pkg_resources`-style namespaces.
Plone itself depends on a package `collective.monkeypatcher` which is now using native namespaces.
This may cause problems at startup, especially `ModuleNotFoundError`.
In a normal install:

* `pip` works fine.
* `zc.buildout` 4 won't work.
* `zc.buildout` 5 works fine.

If for one or both of these packages you don't use a final release from https://pypi.org, but an editable install, it may not work.
You can solve this by installing an extra package with `pip`, `horse-with-no-namespace`.

```{note}
If you let `zc.buildout` install `horse-with-no-namespace`, it won't work.
It really must be installed by `pip` into the same virtual environment where you have installed `zc.buildout`.
```

The recommendation is to migrate all namespace packages to native namespaces.
This includes the `collective` namespace that a lot of Plone add-ons use.
This {doc}`guide </developer-guide/native-namespace>` describes the needed steps.

## Start separating Classic UI code from the core

In Plone 6, the Python backend includes the Classic UI frontend.
You can't get one without the other.
If you use the Volto frontend, this means that you get lots of code that you never use.

Plone 6.2 starts separating Classic UI code from the core of Plone.
This is ongoing work, described in {term}`PLIP` [3953](https://github.com/plone/Products.CMFPlone/issues/3953).
You won't yet get less code yet.
This PLIP is preparation for a more complete separation in Plone 7.

The focus currently is on moving page templates into the `plone.app.layout` package.
Templates from the following packages are now in a new location:

* `plone.locking`
* `plone.protect`

```{note}
If you use the `z3c.jbot` add-on to override a template that has been moved, your override will still work.
This is because we keep a mapping from the old to the new location.
For example, `plone.locking` registers that `plone.locking.browser.info.pt` has a new location, `plone.app.layout.viewlets.locking.pt`.
You should rename your override to the new location if you no longer need compatibility with Plone 6.1 or earlier.
```
