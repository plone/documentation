---
myst:
  html_meta:
    "description": "How Plone testing layers work: the plone.testing layer model, resources, bases, sandboxing, and isolation."
    "property=og:description": "How Plone testing layers work: the plone.testing layer model, resources, bases, sandboxing, and isolation."
    "property=og:title": "How testing layers work"
    "keywords": "Plone, testing, plone.testing, layers, DemoStorage, component registry, isolation"
---

(how-testing-layers-work)=

# How testing layers work

This page explains the machinery beneath the testing layers—the [plone.testing](https://github.com/plone/plone.testing) model that [plone.app.testing](https://github.com/plone/plone.app.testing) builds on.

You do not need this to write ordinary tests.
Read it when you write a non-trivial base layer, or when you need to understand why a layer behaves the way it does.

For *why* Plone tests with layers at all, and the trade-off between integration and functional testing, read {ref}`about-testing-in-plone` first.
For the classes and helpers named here, see {doc}`testing-api-reference`.

## A layer is an object with a lifecycle

A layer is an object with four lifecycle methods:

- `setUp` and `tearDown` run **once**, around the whole group of tests that share the layer.
  This is where the expensive work goes—start Zope, create the Plone site, load ZCML, install a profile.
- `testSetUp` and `testTearDown` run **around every test**. This is where the cheap per-test isolation goes.

Splitting the expensive from the cheap is the entire point: the costly setup happens once and is shared, while each test still starts from a clean state.

## Layers share state through resources

A layer is also a mapping.
Set-up code stores things in it by key, and tests read them back:

```python
def setUp(self):
    self["app"] = ...   # the Zope root
```

```python
def test_something(self):
    app = self.layer["app"]
```

Resources are **stacked**.
When a layer sets a key that one of its bases already set, the layer's value shadows the base's for the duration of that layer, and the base's value reappears when the layer tears down.
This is how a functional layer can, for example, replace the database with a sandboxed copy without disturbing the layer it builds on.

## Layers compose through bases

A layer declares its bases—the layers it builds on.
When you write a reusable layer class, you set them as the `defaultBases` class attribute.
When you instantiate a layer directly to combine existing ones, you pass them as the `bases` argument instead; that is the exception, not the rule.
Either way, the test runner sets up each base once, in order, before the layer itself, and reuses an already-set-up base rather than building it again.

The result is a tree of layers, each built once.
A typical add-on's stack looks like this:

```text
Zope startup            (plone.testing.zope.STARTUP)
  └─ PloneFixture       (a Plone site: PLONE_FIXTURE)
       └─ your fixture  (your PloneSandboxLayer subclass: loads ZCML, installs your profile)
            ├─ IntegrationTesting   (per-test transaction)
            └─ FunctionalTesting    (per-test DemoStorage)
```

`PLONE_FIXTURE` sits in the middle: it is the shared Plone site every add-on layer builds on.
You never use it in a test directly—you build your own fixture on it, then derive integration and functional layers from that.

Notice that both `IntegrationTesting` and `FunctionalTesting` are built on the *same* fixture, by passing it as their `bases`.
This is the point of separating the fixture from the lifecycle: the expensive site is built once, and the two layers add only the cheap per-test behavior on top.
The same trick lets a package reuse a base layer with a different lifecycle, or add a second fixture beside it, without paying for the expensive setup twice.

## How isolation works

Isolation happens in the cheap per-test half, and the two layer kinds do it differently.

An **integration** layer begins a transaction in `testSetUp` and **aborts** it in `testTearDown`.
Nothing a test writes is committed, so the next test sees the pristine site.
This is fast, and it is what most tests use.

A **functional** layer instead stacks a temporary `DemoStorage` on the database in `testSetUp` and discards it in `testTearDown`.
The test may **commit** for real, and a separate process—a browser, an HTTP client—can see the result, because the data really is in the (sandboxed) database.
When the test ends, the whole stacked storage is thrown away.
This is more expensive, which is why you reach for it only when a request has to travel over the network.

(zca-sandbox)=

## The component-registry sandbox

Plone relies heavily on the Zope Component Architecture—a global registry of components, populated by loading ZCML.
If a test layer loaded ZCML into the one global registry and never undid it, registrations would leak from one layer into the next, and tests would interfere with each other in ways that depend on run order.

To prevent this, a sandboxing layer **pushes a new component registry** on set-up and **pops it** on tear-down, so every registration it makes lives only as long as the layer.
`PloneSandboxLayer` does this for you—that is what the "sandbox" in its name means.
The primitives are {ref}`pushGlobalRegistry and popGlobalRegistry <testing-api-reference>`; you rarely call them directly.

## Server fixtures for real HTTP

An in-process functional test can drive Plone through a test browser without a socket.
When a test needs a **real** HTTP server—a live URL that an external client hits—add `WSGI_SERVER_FIXTURE` (from `plone.testing.zope`) to the functional layer's bases.
It starts a WSGI server for the duration of the layer and exposes its address, so requests genuinely travel over the network.

```{seealso}
The full model, including the ZODB and component-architecture helpers, lives in [plone.testing](https://github.com/plone/plone.testing/blob/master/src/plone/testing/README.rst).
```
