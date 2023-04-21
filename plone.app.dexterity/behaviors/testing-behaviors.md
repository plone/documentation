---
myst:
  html_meta:
    "description": "How to write unit tests for behaviors for content types in Plone"
    "property=og:description": "How to write unit tests for behaviors for content types in Plone"
    "property=og:title": "How to write unit tests for behaviors for content types in Plone"
    "keywords": "Plone, content types, testing, behaviors"
---

# Testing behaviors

This chapter describes how to write unit tests for behaviors for content types in Plone.

Behaviors, like any other code, should be tested.
If you write a behavior with just a marker interface or schema interface, it is probably not necessary to test the interface.
However, any actual code, such as a behavior adapter factory, ought to be tested.

Writing a behavior integration test is not very difficult if you are happy to depend on Dexterity in your test.
You can create a dummy type by instantiating a Dexterity FTI in `portal_types`.
Then enable your behavior by adding its interface name to the `behaviors` property.

In many cases, however, it is better not to depend on Dexterity at all.
It is not too difficult to mimic what Dexterity does to enable behaviors on its types.
The following example is taken from `collective.gtags` and tests the `ITags` behavior we saw on the first page of this manual.


## Behaviors

This package provides a behavior called `collective.gtags.behaviors.ITags`.
This adds a `Tags` field called `tags` to the `Categorization` fieldset, with a behavior adapter that stores the chosen tags in the `Subject` metadata field.


### Test setup

Before we can run these tests, we need to load the `collective.gtags` configuration.
This will configure the behavior.

```pycon
>>> configuration = """\
... <configure
...      xmlns="http://namespaces.zope.org/zope"
...      i18n_domain="collective.gtags">
...
...     <include package="Products.Five" file="meta.zcml" />
...     <include package="collective.gtags" file="behaviors.zcml" />
...
... </configure>
... """

>>> from StringIO import StringIO
>>> from zope.configuration import xmlconfig
>>> xmlconfig.xmlconfig(StringIO(configuration))
```

This behavior can be enabled for any `IDublinCore`.
For the purposes of testing, we will use the `CMFDefault` `Document` type and a custom `IBehaviorAssignable` adapter to mark the behavior as enabled.

```pycon
>>> from Products.CMFDefault.Document import Document

>>> from plone.behavior.interfaces import IBehaviorAssignable
>>> from collective.gtags.behaviors import ITags
>>> from zope.component import adapter
>>> from zope.interface import implementer
>>> @adapter(Document)
... @implementer(IBehaviorAssignable)
... class TestingAssignable(object):
...
...     enabled = [ITags]
...
...     def __init__(self, context):
...         self.context = context
...
...     def supports(self, behavior_interface):
...         return behavior_interface in self.enabled
...
...     def enumerate_behaviors(self):
...         for e in self.enabled:
...             yield queryUtility(IBehavior, name=e.__identifier__)

>>> from zope.component import provideAdapter
>>> provideAdapter(TestingAssignable)
```


### Behavior installation

We can now test that the behavior is installed when the ZCML for this package is loaded.

```pycon
>>> from zope.component import getUtility
>>> from plone.behavior.interfaces import IBehavior
>>> tags_behavior = getUtility(IBehavior, name="collective.gtags.behaviors.ITags")
>>> tags_behavior.interface
<InterfaceClass collective.gtags.behaviors.ITags>
```

We also expect this behavior to be a form field provider.
Let's verify that.

```pycon
>>> from plone.autoform.interfaces import IFormFieldProvider
>>> IFormFieldProvider.providedBy(tags_behavior.interface)
True
```


Using the behavior
------------------

Let's create a content object that has this behavior enabled and check that
it works.

```pycon
>>> doc = Document("doc")
>>> tags_adapter = ITags(doc, None)
>>> tags_adapter is not None
True
```

We'll check that the `tags` set is built from the `Subject()` field:

```pycon
>>> doc.setSubject(["One", "Two"])
>>> doc.Subject()
("One", "Two")

>>> tags_adapter.tags == set(["One", "Two"])
True

>>> tags_adapter.tags = set(["Two", "Three"])
>>> doc.Subject() == ("Two", "Three")
True
```

This test tries to prove that the behavior is correctly installed and works as intended on a suitable content class.
It is not a true unit test, however.
For a true unit test, we would test the `Tags` adapter directly on a dummy context, but that is not terribly interesting, since all it does is convert sets to tuples.

First, we configure the package.
To keep the test small, we limit ourselves to the {file}`behaviors.zcml` file, which in this case will suffice.
We still need to include a minimal set of ZCML from `Five`.

Next, we implement an `IBehaviorAssignable` adapter.
This is a low-level component used by `plone.behavior` to determine if a behavior is enabled on a particular object.
Dexterity provides an implementation that checks the type's FTI.
Our test version is much simpler: it hardcodes the supported behaviors.

With this in place, we first check that the `IBehavior` utility has been correctly registered.
This is essentially a test to show that we've used the `<plone:behavior />` directive as intended.
We also verify that our schema interface is an `IFormFieldsProvider`.
For a non-form behavior, we'd omit this.

Finally, we test the behavior.
We've chosen to use CMFDefault's `Document` type for our test, as the behavior adapter requires an object providing `IDublinCore`.
Ideally, we'd write our own class and implement `IDublinCore` directly.
However, in many cases, the types from `CMFDefault` are going to provide convenient test fodder.

If our behavior was more complex, we'd add more intricate tests.
By the last section of the doctest, we have enough context to test the adapter factory.

To run the test, we need a test suite.
Here is our {file}`tests.py`.

```python
from zope.app.testing import setup
import doctest
import unittest

def setUp(test):
    pass

def tearDown(test):
    setup.placefulTearDown()

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            "behaviors.rst",
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
        ))
```

This runs the {file}`behaviors.rst` doctest from the same directory as the {file}`tests.py` file.
To run the test, we can use the usual test runner.

```shell
./bin/instance test -s collective.gtags
```


## Testing a Dexterity type with a behavior

Not all behaviors are enabled by default.
Let's say you want to test your Dexterity type when a behavior is enabled or disabled.
To do this, you will need to setup the behavior in your test.
There is an example of this kind of test in the `collective.cover` product.
There is a behavior that adds the capability for the cover page to refresh itself.
The test checks if the behavior is not yet enabled, enables the behavior, check its effect, and then disables it again.

```python
# -*- coding: utf-8 -*-
from collective.cover.behaviors.interfaces import IRefresh
from collective.cover.interfaces import ICoverLayer
from collective.cover.testing import INTEGRATION_TESTING
from plone import api
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.schema import SchemaInvalidatedEvent
from zope.component import queryUtility
from zope.event import notify
from zope.interface import alsoProvides

import unittest


class RefreshBehaviorTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def _enable_refresh_behavior(self):
        fti = queryUtility(IDexterityFTI, name="collective.cover.content")
        behaviors = list(fti.behaviors)
        behaviors.append(IRefresh.__identifier__)
        fti.behaviors = tuple(behaviors)
        # invalidate schema cache
        notify(SchemaInvalidatedEvent("collective.cover.content"))

    def _disable_refresh_behavior(self):
        fti = queryUtility(IDexterityFTI, name="collective.cover.content")
        behaviors = list(fti.behaviors)
        behaviors.remove(IRefresh.__identifier__)
        fti.behaviors = tuple(behaviors)
        # invalidate schema cache
        notify(SchemaInvalidatedEvent("collective.cover.content"))

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        alsoProvides(self.request, ICoverLayer)
        with api.env.adopt_roles(["Manager"]):
            self.cover = api.content.create(
                self.portal, "collective.cover.content", "c1")

    def test_refresh_registration(self):
        registration = queryUtility(IBehavior, name=IRefresh.__identifier__)
        self.assertIsNotNone(registration)

    def test_refresh_behavior(self):
        view = api.content.get_view(u"view", self.cover, self.request)
        self.assertNotIn("<meta http-equiv="refresh" content="300" />", view())
        self._enable_refresh_behavior()
        self.cover.enable_refresh = True
        self.assertIn("<meta http-equiv="refresh" content="300" />", view())
        self.cover.ttl = 5
        self.assertIn("<meta http-equiv="refresh" content="5" />", view())
        self._disable_refresh_behavior()
        self.assertNotIn("<meta http-equiv="refresh" content="5" />", view())
```

The methods `_enable_refresh_behavior` and `_disable_refresh_behavior` use the `IDexterityFTI` to get the Factory Type Information for the Dexterity type (`collective.cover.content` in this case).
Then the FTI of `collective.cover.content` is used by both methods to get a list of enabled behaviors.
To enable it, add the desired behavior to the FTI behaviors: `behaviors.append(IRefresh.__identifier__)`.
To disable it, remove the behavior from the FTI behaviors: `behaviors.remove(IRefresh.__identifier__)`.
Assign the resulting behaviors list to the behaviors attribute of the FTI as a tuple: `fti.behaviors = tuple(behaviors)`.
Finally, to have the changes take effect, invalidate the schema cache: `notify(SchemaInvalidatedEvent('collective.cover.content'))`.


## A note about marker interfaces

Marker interface support depends on code that is implemented in Dexterity and is non-trivial to reproduce in a test.
If you need a marker interface in a test, set it manually with `zope.interface.alsoProvides`, or write an integration test with Dexterity content.
