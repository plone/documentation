---
myst:
  html_meta:
    "description": "How to write integration tests with plone.app.testing for content types in Plone"
    "property=og:description": "How to write integration tests with plone.app.testing for content types in Plone"
    "property=og:title": "How to write integration tests with plone.app.testing for content types in Plone"
    "keywords": "Plone, content types, integration tests"
---

# Integration tests

This chapter describes how to write integration tests with [`plone.app.testing`](https://pypi.org/project/plone.app.testing/).

We'll now add some integration tests for our type.
These should ensure that the package installs cleanly, and that our custom types are addable in the right places and have the right schemata, at the very least.

To help manage test setup, we'll make use of the Zope test runner's concept of *layers*.
Layers allow common test setup (such as configuring a Plone site and installing a product) to take place once and be reused by multiple test cases.
Those test cases can still modify the environment, but their changes will be torn down and the environment reset to the layer's initial state between each test, facilitating test isolation.

As the name implies, layers are, uh..., layered.
One layer can extend another.
If two test cases in the same test run use two different layers with a common ancestral layer, the ancestral layer is only set up and torn down once.

`plone.app.testing` provides tools for writing integration and functional tests for code that runs on top of Plone, so we'll use it.

In {file}`setup.py`, we will add the `extras_require` option as shown.

```python
extras_require = {
    "test": ["plone.app.testing"]
},
```

```{note}
Don't forget to re-run buildout after making changes to {file}`setup.py`.
```

`plone.app.testing` includes a set of layers that set up fixtures containing a Plone site, intended for writing integration and functional tests.

We need to create a custom fixture.
The usual pattern is to create a new layer class that has `PLONE_FIXTURE` as its default base, instantiating that as a separate "fixture" layer.
This layer is not to be used in tests directly, since it won't have test and transaction lifecycle management, but represents a shared fixture, potentially for both functional and integration testing.
It is also the point of extension for other layers that follow the same pattern.

Once this fixture has been defined, "end-user" layers can be defined using the `IntegrationTesting` and `FunctionalTesting` classes.
We'll add this in a {file}`testing.py` file.

```python
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import example.conference
        self.loadZCML(package=example.conference)

    def setUpPloneSite(self, portal):
        # Install the example.conference product
        self.applyProfile(portal, "example.conference:default")


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="example.conference:Integration",
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name="example.conference:Functional",
    )
```

This extends a base layer that sets up Plone, and adds some custom layer setup for our package, in this case installing the `example.conference` extension profile.
We could also perform additional setup here, such as creating some initial content or setting the default roles for the test run.
See the [`plone.app.testing`](https://pypi.org/project/plone.app.testing/#introduction) documentation for more details.

To use the layer, we can create a new test case based on `unittest.TestCase` that uses our layer.
We'll add one to `test_program.py` first.
In the code snippet below, the unit test we created previously has been removed to conserve space.

```python
import unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from example.conference.program import IProgram
from example.conference.testing import INTEGRATION_TESTING

class TestProgramIntegration(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Folder", "test-folder")
        setRoles(self.portal, TEST_USER_ID, ["Member"])
        self.folder = self.portal["test-folder"]

    def test_adding(self):
        self.folder.invokeFactory("example.conference.program", "program1")
        p1 = self.folder["program1"]
        self.assertTrue(IProgram.providedBy(p1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name="example.conference.program")
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name="example.conference.program")
        schema = fti.lookupSchema()
        self.assertEqual(IProgram, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name="example.conference.program")
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IProgram.providedBy(new_object))

    def test_view(self):
        self.folder.invokeFactory("example.conference.program", "program1")
        p1 = self.folder["program1"]
        view = p1.restrictedTraverse("@@view")
        sessions = view.sessions()
        self.assertEqual(0, len(sessions))

    def test_start_end_dates_indexed(self):
        self.folder.invokeFactory("example.conference.program", "program1")
        p1 = self.folder["program1"]
        p1.start = datetime.datetime(2009, 1, 1, 14, 01)
        p1.end = datetime.datetime(2009, 1, 2, 15, 02)
        p1.reindexObject()

        result = self.portal.portal_catalog(path="/".join(p1.getPhysicalPath()))

        self.assertEqual(1, len(result))
        self.assertEqual(result[0].start, DateTime("2009-01-01T14:01:00"))
        self.assertEqual(result[0].end, DateTime("2009-01-02T15:02:00"))

    def test_tracks_indexed(self):
        self.folder.invokeFactory("example.conference.program", "program1")
        p1 = self.folder["program1"]
        p1.tracks = ["Track 1", "Track 2"]
        p1.reindexObject()

        result = self.portal.portal_catalog(Subject="Track 2")

        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), p1.absolute_url())

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
```

This illustrates a basic set of tests that make sense for most content types.
There are many more things we could test.
For example, we could test the add permissions more thoroughly, and we ought to test the `sessions()` method on the view with some actual content, but even this small set of integration tests tells us that our product has installed, that the content type is addable, that it has the right factory, and that instances of the type provide the right schema interface.

There are some important things to note about this test case.

-   We extend `unittest.TestCase`, which means we have access to a full Plone integration test environment.
    See the [testing tutorial](https://5.docs.plone.org/external/plone.testing/docs/index.html) for more details.
-   We set the `layer` attribute to our custom layer.
    This means that all tests in our test case will have the `example.conference:default` profile installed.
-   We need to create a test user's member folder as `self.folder` because `plone.app.testing` takes a minimalist approach and no content is available by default.
-   We test that the content is addable as a normal member in their member folder, since that is the default security context for the test.
    Use `self.setRoles([‘Manager'])` to get the `Manager` role and `self.portal` to access the portal root.
    We also test that the FTI is installed and can be located, and that both the FTI and instances of the type know about the correct type schema.
-   We also test that the view can be looked up and has the correct methods.
    We've not included a fully functional test using `zope.testbrowser` or any other front-end testing here.
    If you require those, take a look at the testing tutorial.
-   We also test that our custom indexers are working, by creating an appropriate object and searching for it.
    Note that we need to reindex the object after we've modified it so that the catalog is up to date.
-   The `defaultTestLoader` will find this test and load it, just as it found the `TestProgramUnit` test case.

To run our tests, we can still do.

```shell
./bin/test example.conference
```

You should now notice layers being set up and torn down.
Again, use the `-t` option to run a particular test case (or test method) only.

The other tests are similar.
We have {file}`tests/test_session.py` to test the `Session` type.

```python
import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from example.conference.session import ISession
from example.conference.session import possible_tracks
from example.conference.testing import INTEGRATION_TESTING

class TestSessionIntegration(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Folder", "test-folder")
        setRoles(self.portal, TEST_USER_ID, ["Member"])
        self.folder = self.portal["test-folder"]

    def test_adding(self):

        # We can't add this directly
        self.assertRaises(ValueError, self.folder.invokeFactory, "example.conference.session", "session1")

        self.folder.invokeFactory("example.conference.program", "program1")
        p1 = self.folder["program1"]

        p1.invokeFactory("example.conference.session", "session1")
        s1 = p1["session1"]
        self.assertTrue(ISession.providedBy(s1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name="example.conference.session")
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name="example.conference.session")
        schema = fti.lookupSchema()
        self.assertEqual(ISession, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name="example.conference.session")
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ISession.providedBy(new_object))

    def test_tracks_vocabulary(self):
        self.folder.invokeFactory("example.conference.program", "program1")
        p1 = self.folder["program1"]
        p1.tracks = ["T1", "T2", "T3"]

        p1.invokeFactory("example.conference.session", "session1")
        s1 = p1["session1"]

        vocab = possible_tracks(s1)

        self.assertEqual(["T1", "T2", "T3"], [t.value for t in vocab])
        self.assertEqual(["T1", "T2", "T3"], [t.token for t in vocab])

    def test_catalog_index_metadata(self):
        self.assertTrue("track" in self.portal.portal_catalog.indexes())
        self.assertTrue("track" in self.portal.portal_catalog.schema())

    def test_workflow_installed(self):
        self.folder.invokeFactory("example.conference.program", "program1")
        p1 = self.folder["program1"]

        p1.invokeFactory("example.conference.session", "session1")
        s1 = p1["session1"]

        chain = self.portal.portal_workflow.getChainFor(s1)
        self.assertEqual(("example.conference.session_workflow",), chain)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
```

Notice here how we test that the `Session` type cannot be added directly to a folder, and that it can be added inside a program.
We also add a test for the `possible_tracks()` vocabulary method, as well as tests for the installation of the `track` index and metadata column and the custom workflow.

```python
import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from example.conference.presenter import IPresenter
from example.conference.testing import INTEGRATION_TESTING

class TestPresenterIntegration(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Folder", "test-folder")
        setRoles(self.portal, TEST_USER_ID, ["Member"])
        self.folder = self.portal["test-folder"]

    def test_adding(self):
        self.folder.invokeFactory("example.conference.presenter", "presenter1")
        p1 = self.folder["presenter1"]
        self.assertTrue(IPresenter.providedBy(p1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name="example.conference.presenter")
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name="example.conference.presenter")
        schema = fti.lookupSchema()
        self.assertEqual(IPresenter, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name="example.conference.presenter")
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IPresenter.providedBy(new_object))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
```
