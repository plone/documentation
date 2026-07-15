---
myst:
  html_meta:
    "description": "Write and run tests for a Plone package with unittest and zope.testrunner."
    "property=og:description": "Write and run tests for a Plone package with unittest and zope.testrunner."
    "property=og:title": "Test with zope.testrunner"
    "keywords": "Plone, zope.testrunner, unittest, testing layers, coverage"
---

(test-with-zope-testrunner)=

# Test with `zope.testrunner`

This guide shows you how to write and run tests with `unittest` and `zope.testrunner`, the runner Plone core uses.

For pytest instead, see {doc}`pytest`.

## Install the runner

```shell
pip install zope.testrunner
```

## Write an integration test

A test is a `unittest.TestCase`.
It declares the layer it needs by assigning it to a `layer` attribute.

```python
from my.addon.testing import MY_ADDON_INTEGRATION_TESTING
from plone import api

import unittest


class TestDocument(unittest.TestCase):
    layer = MY_ADDON_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

    def test_portal_title(self):
        self.assertEqual(self.portal.title, "Plone site")

    def test_create_document(self):
        with api.env.adopt_roles(["Manager"]):
            api.content.create(
                container=self.portal,
                type="Document",
                id="doc1",
                title="A document",
            )
        self.assertIn("doc1", self.portal)
```

The `layer` attribute is the whole integration.
The runner reads it, sets that layer up once, and runs every test that declares it.

`self.layer["portal"]` is how you reach the Plone site.
The layer exposes the objects it built through this mapping.

Note what `test_create_document` does *not* need: no cleanup.
The integration layer aborts the transaction after each test, so `doc1` is gone before the next test runs.

## Write a functional test

Use the functional layer when a request has to arrive over the network, and the site must therefore commit.

```python
from my.addon.testing import MY_ADDON_FUNCTIONAL_TESTING

import unittest


class TestDocumentView(unittest.TestCase):
    layer = MY_ADDON_FUNCTIONAL_TESTING
```

Everything else is the same.
Only the layer changes.

## Run the tests

```shell
zope-testrunner --auto-path -s my.addon
```

`-s` takes the dotted name of the package to search.
`--auto-path` adds that package's directory to the test search path, which is what you want for a package installed in development mode.

Add `--auto-color` and `--auto-progress` for readable output:

```shell
zope-testrunner --auto-color --auto-progress --auto-path -s my.addon
```

```{note}
Under Buildout, the equivalent command was `bin/test`.
Buildout generated that script for you.
With a pip-installed Plone, you call `zope-testrunner` directly.
```

## Read the output

The runner groups tests by layer, and tells you so:

```console
Running my.addon.testing.MyAddon:Integration tests:
  Set up my.addon.testing.MyAddon:Integration in 4.521 seconds.
  Ran 12 tests with 0 failures, 0 errors and 0 skipped in 0.843 seconds.
Running my.addon.testing.MyAddon:Functional tests:
  Set up my.addon.testing.MyAddon:Functional in 0.128 seconds.
  Ran 3 tests with 0 failures, 0 errors and 0 skipped in 1.204 seconds.
```

This grouping is the runner's defining behavior.
Each layer is set up once, and every test that declared it runs against that one setup.

The `Set up ... in N seconds` line is the expensive part.
If you see it repeated many times, something is forcing the layer to be rebuilt.

## Narrow down what runs

While working on one thing, run one thing.

Filter by test name, a case-sensitive regular expression:

```shell
zope-testrunner --auto-path -s my.addon -t test_create_document
```

Filter by module, also a regular expression:

```shell
zope-testrunner --auto-path -s my.addon -m test_document
```

Run only unit tests, ignoring every layer:

```shell
zope-testrunner --auto-path -s my.addon -u
```

Run a single layer:

```shell
zope-testrunner --auto-path -s my.addon --layer Integration
```

List what would run, without running it:

```shell
zope-testrunner --auto-path -s my.addon --list-tests
```

`--list-tests` is the fastest way to check that a filter matches what you think it does.

## Run tests in parallel

```shell
zope-testrunner --auto-path -s my.addon -j 4
```

Each process sets up its own layers, so this trades memory for wall-clock time.
It pays off on large suites.

## Measure coverage

`zope.testrunner` runs as a module, so `coverage` can wrap it:

```shell
coverage run -m zope.testrunner --auto-path -s my.addon
coverage report
```

## Run tests at all levels

Some tests are registered at a higher level and are skipped by default, notably Robot Framework tests.

```shell
zope-testrunner --auto-path -s my.addon --all
```

Expect this to be considerably slower.
