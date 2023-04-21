---
myst:
  html_meta:
    "description": "How to write basic unit tests for content types in Plone"
    "property=og:description": "How to write basic unit tests for content types in Plone"
    "property=og:title": "How to write basic unit tests for content types in Plone"
    "keywords": "Plone, content types, unit tests"
---

# Unit tests

This chapter describes how to write basic unit tests for content types.

As all good developers know, automated tests are very important.
If you are not comfortable with automated testing and test-driven development, you should read the [Plone testing tutorial](https://5.docs.plone.org/external/plone.testing/docs/index.html).
In this section, we will assume you are familiar with Plone testing basics, and show some tests that are particularly relevant to our example types.

Firstly, we will add a few unit tests.
Recall that unit tests are simple tests for a particular function or method, and do not depend on an outside environment being set up.
As a rule of thumb, if something can be tested with a simple unit test, do so for the following reasons.

-   Unit tests are quick to write.
-   They are also quick to run.
-   Because they are more isolated, you are less likely to have tests that pass or fail due to incorrect assumptions or by luck.
-   You can usually test things more thoroughly and exhaustively with unit tests than with (slower) integration tests.

You'll typically supplement a larger number of unit tests with a smaller number of integration tests, to ensure that your application's correctly wired up and working.

That's the theory, at least.
When we write content types, we're often more interested in integration tests, because a type schema and FTI are more like configuration of the Plone and Dexterity frameworks than imperative programming.
We can't "unit test" the type's schema interface, but we can and should test that the correct schema is picked up and used when our type is installed.
We will often write unit tests (with mock objects, where required) for custom event handlers, default value calculation functions and other procedural code.

In that spirit, let's write some unit tests for the default value handler and the invariant in {file}`program.py`.
We'll add the directory `tests`, with an `__init__.py` and a file {file}`test_program.py` as shown.

```python
import unittest
import datetime

from example.conference.program import startDefaultValue
from example.conference.program import endDefaultValue
from example.conference.program import IProgram
from example.conference.program import StartBeforeEnd

class MockProgram(object):
    pass

class TestProgramUnit(unittest.TestCase):
    """Unit test for the Program type
    """

    def test_start_defaults(self):
        data = MockProgram()
        default_value = startDefaultValue(data)
        today = datetime.datetime.today()
        delta = default_value - today
        self.assertEqual(6, delta.days)

    def test_end_default(self):
        data = MockProgram()
        default_value = endDefaultValue(data)
        today = datetime.datetime.today()
        delta = default_value - today
        self.assertEqual(9, delta.days)

    def test_validate_invariants_ok(self):
        data = MockProgram()
        data.start = datetime.datetime(2009, 1, 1)
        data.end = datetime.datetime(2009, 1, 2)

        try:
            IProgram.validateInvariants(data)
        except:
            self.fail()

    def test_validate_invariants_fail(self):
        data = MockProgram()
        data.start = datetime.datetime(2009, 1, 2)
        data.end = datetime.datetime(2009, 1, 1)

        try:
            IProgram.validateInvariants(data)
            self.fail()
        except StartBeforeEnd:
            pass

    def test_validate_invariants_edge(self):
        data = MockProgram()
        data.start = datetime.datetime(2009, 1, 2)
        data.end = datetime.datetime(2009, 1, 2)

        try:
            IProgram.validateInvariants(data)
        except:
            self.fail()

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
```

This is a test using the Python standard library's `unittest` module.
There are a few things to note here:

-   We have created a dummy class to simulate a `Program` instance.
    It doesn't contain anything at all, but we set some attributes onto it for certain tests.
    This is a very simple way to do mocks.
    There are much more sophisticated mock testing approaches, but starting simple is good.
-   Each test is self contained.
    There is no test layer or test case setup or tear down.
-   We use the `defaultTestLoader` to load all test classes in the module automatically.
    The test runner will look for modules in the `tests` package with names starting with `test` that have a `test_suite()` method to get test suites.

To run the tests, use the following command.

```shell
./bin/test example.conference
```

Hopefully it should show five passing tests.

```{note}
This uses the testrunner configured via the `[test]` part in our `buildout.cfg`.
This provides better test reporting and a few more advanced options, such as output coloring.
We could also use the built-in test runner in the `instance` script, for example, with `./bin/instance test -s example.conference`.
```

To run just this test suite, use the following command.

```shell
./bin/test example.conference -t TestProgramUnit
```

This is useful when we have other test suites that we don't want to run when they are integration tests and require lengthy setup.

To get a report about test coverage, we can run the following command.

```shell
./bin/test example.conference --coverage
```

Test coverage reporting is important.
If you have a module with low test coverage, it means that your tests do not cover many of the code paths in those modules, and so are less useful for detecting bugs or guarding against future problems.
Aim for 100% coverage.
