---
myst:
  html_meta:
    "description": "Write and run tests for a Plone backend package, with either zope.testrunner or pytest."
    "property=og:description": "Write and run tests for a Plone backend package, with either zope.testrunner or pytest."
    "property=og:title": "Test a backend package"
    "keywords": "Plone, testing, pytest, zope.testrunner, backend, add-on"
---

(testing-backend-packages)=

# Test a backend package

How to write and run tests for a Plone package written in Python.

If you want to understand *why* Plone tests look the way they do before you write any, read {doc}`/conceptual-guides/testing` first.
This page assumes you have.

```{note}
This covers backend packages.
For testing a Volto add-on, see [Test add-ons](/volto/development/add-ons/test-add-ons-19).
```

## Before you start

You need a testing layer.

A layer builds the Plone site your tests run against: it loads your ZCML and installs your GenericSetup profile.
You declare it in a `testing.py` module in your package, and a package generated from a Plone template already has one.

Both test runners consume the same layer.
Choosing a runner does not change how you write `testing.py`.

If your package has no `testing.py`, write one first.
See {doc}`write-a-testing-layer`.

## Choose a runner

| | zope.testrunner | pytest |
| --- | --- | --- |
| Tests are | `unittest.TestCase` classes | plain functions |
| Layers | native | via [pytest-plone](https://plone.github.io/pytest-plone/) |
| Used by | Plone core | most new add-ons, Cookieplone |

Choose `zope.testrunner` if you contribute to Plone core, or if your package already uses it.
A working test suite is not worth converting.

Choose pytest for new work.

Do not use both in one package.

## Guides

- {doc}`write-a-testing-layer`: the `testing.py` layer both runners share.
- {doc}`zope-testrunner`: write and run tests with `unittest` and `zope.testrunner`.
- {doc}`pytest`: write and run tests with pytest.
- {doc}`install-add-ons-in-tests`: apply profiles and install add-ons in a test.
- {doc}`drive-the-test-browser`: end-to-end tests with `zope.testbrowser`.

## Reference and background

- {doc}`testing-api-reference`: the layers, fixtures, helpers, and sandboxing, across `plone.app.testing` and `plone.testing`.
- {doc}`how-testing-layers-work`: the layer model beneath it all.

```{toctree}
:hidden:
:maxdepth: 1

write-a-testing-layer
zope-testrunner
pytest
install-add-ons-in-tests
drive-the-test-browser
testing-api-reference
how-testing-layers-work
```
