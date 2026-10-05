---
myst:
  html_meta:
    "description": "Write the testing.py testing layer that both zope.testrunner and pytest-plone build on."
    "property=og:description": "Write the testing.py testing layer that both zope.testrunner and pytest-plone build on."
    "property=og:title": "Write a testing layer"
    "keywords": "Plone, testing layer, testing.py, plone.app.testing, PloneSandboxLayer, PloneWithPackageLayer"
---

(write-a-testing-layer)=

# Write a testing layer

This guide shows you how to write the testing layer for a Plone add-on.

The layer is the setup work both test runners share.
Whether you test with {doc}`zope-testrunner` or {doc}`pytest`, the layer is what builds the Plone site your tests run against: it loads your ZCML and installs your GenericSetup profile.
You write it once, in a `testing.py` module in your package.

For what a layer *is* and why Plone works this way, see {doc}`/conceptual-guides/testing`.
This page is about writing one.

## Two ways to write it

`plone.app.testing` gives you two forms.

Use the **declarative form** for a simple add-on: one package, one profile.
Use the **class form** when setup needs more than that: extra ZCML, several profiles, dependencies loaded first, or setup code that runs against the portal.

Both produce the same thing—a *fixture* layer—and from that fixture you derive the integration and functional layers your tests name.

## The declarative form

For an add-on that loads its own ZCML and installs one profile, instantiate `PloneWithPackageLayer` directly.
No subclass needed.

```python
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import my.addon


MY_ADDON_FIXTURE = PloneWithPackageLayer(
    zcml_package=my.addon,
    zcml_filename="configure.zcml",
    gs_profile_id="my.addon:default",
    name="MyAddonFixture",
)

MY_ADDON_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MY_ADDON_FIXTURE,),
    name="MyAddonLayer:IntegrationTesting",
)

MY_ADDON_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MY_ADDON_FIXTURE, WSGI_SERVER_FIXTURE),
    name="MyAddonLayer:FunctionalTesting",
)
```

That is a complete `testing.py`.
The three names it exports—the fixture, the integration layer, and the functional layer—are what your tests and your `conftest.py` refer to.

## The class form

When the declarative form is not enough, subclass `PloneSandboxLayer` and override two methods.

```python
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import my.addon


class MyAddonLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=my.addon)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "my.addon:default")


MY_ADDON_FIXTURE = MyAddonLayer()

MY_ADDON_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MY_ADDON_FIXTURE,),
    name="MyAddonLayer:IntegrationTesting",
)

MY_ADDON_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MY_ADDON_FIXTURE, WSGI_SERVER_FIXTURE),
    name="MyAddonLayer:FunctionalTesting",
)
```

The two methods are the whole difference:

`setUpZope`
:   Runs while Zope starts, before any Plone site exists.
    Load your ZCML here.
    This is also where you load dependencies—call `self.loadZCML(package=...)` for each, or add their fixtures to the layer's bases.

`setUpPloneSite`
:   Runs against a freshly created Plone site.
    Install your profile here with `applyProfile`.
    You can install more than one, create shared content, or set roles—anything that should be part of the fixture every test starts from.

`PloneSandboxLayer` builds on `PLONE_FIXTURE` by default, which is why you get a working Plone site without asking for one.

## Derive the integration and functional layers

Both forms end the same way: from the one fixture, derive the layers your tests actually use.

`IntegrationTesting` wraps each test in a transaction that is rolled back afterwards.
`FunctionalTesting` lets tests commit, which a separate process can then see.

```python
MY_ADDON_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MY_ADDON_FIXTURE,),
    name="MyAddonLayer:IntegrationTesting",
)

MY_ADDON_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MY_ADDON_FIXTURE, WSGI_SERVER_FIXTURE),
    name="MyAddonLayer:FunctionalTesting",
)
```

```{important}
Add `WSGI_SERVER_FIXTURE` to the functional layer's bases only when your tests make **real HTTP requests** over a socket—REST API tests, for example, including those that use `pytest-plone`'s `request_factory`.
It starts a WSGI server so an HTTP client can reach the site.
Tests that use a Zope testbrowser do not need it.
```

## Use the layers in your tests

Your `testing.py` is now the single input to whichever runner you use.

- With `zope.testrunner`, a test class sets `layer = MY_ADDON_INTEGRATION_TESTING`. See {doc}`zope-testrunner`.
- With pytest, you pass the layers to `fixtures_factory` in your `conftest.py`. See {doc}`pytest`.

## Where to go next

The two forms shown here cover most add-ons.
For the full set of options—additional Zope products, custom base layers, loading several ZCML files—consult the package that owns the machinery.

```{seealso}
[plone.app.testing](https://github.com/plone/plone.app.testing/blob/master/README.rst): the complete reference for layers, fixtures, and helpers.
```
