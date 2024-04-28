---
myst:
  html_meta:
    "description": "How to use a mock objects framework to write mock based tests of content types in Plone"
    "property=og:description": "How to use a mock objects framework to write mock based tests of content types in Plone"
    "property=og:title": "How to use a mock objects framework to write mock based tests of content types in Plone"
    "keywords": "Plone, content types, tests, mock objects, framework"
---

# Mock testing

This chapter describes how to use a mock objects framework to write mock based tests.

Mock testing is a powerful approach to testing that lets you make assertions about how the code under test is interacting with other system modules.
It is often useful when the code you want to test is performing operations that cannot be easily asserted by looking at its return value.

In our example product, we have an event handler.

```python
def notifyUser(presenter, event):
    acl_users = getToolByName(presenter, "acl_users")
    mail_host = getToolByName(presenter, "MailHost")
    portal_url = getToolByName(presenter, "portal_url")

    portal = portal_url.getPortalObject()
    sender = portal.getProperty("email_from_address")

    if not sender:
        return

    subject = "Is this you?"
    message = "A presenter called %s was added here %s" % (presenter.title, presenter.absolute_url(),)

    matching_users = acl_users.searchUsers(fullname=presenter.title)
    for user_info in matching_users:
        email = user_info.get("email", None)
        if email is not None:
            mail_host.send(message, email, sender, subject)
```

If we want to test that this sends the right kind of email message, we'll need to somehow inspect what is passed to `send().`
The only way to do that is to replace the `MailHost` object that is acquired when `getToolByName(presenter, ‘MailHost')` is called, with something that performs that assertion for us.

If we wanted to write an integration test, we could use `PloneTestCase` to execute this event handler by firing the event manually, and temporarily replace the `MailHost` object in the root of the test case portal (`self.portal`) with a dummy that raised an exception if the wrong value was passed.

However, such integration tests can get pretty heavy handed, and sometimes it is difficult to ensure that it works in all cases.
In the approach outlined above, for example, we would miss cases where no mail was sent at all.

Enter mock objects.
A mock object is a "test double" that knows how and when it ought to be called.
The typical approach is as follows.

-   Create a mock object.
-   The mock object starts out in "record" mode.
-   Record the operations that you expect the code under test perform on the mock object.
    You can make assertions about the type and value of arguments, the sequence of calls, the number of times a method is called, or whether an attribute is retrieved or set.
-   You can also give your mock objects behavior, such as specifying return values or exceptions to be raised in certain cases.
-   Initialize the code under test or the environment it runs in so that it will use the mock object rather than the real object.
    Sometimes this involves temporarily "patching" the environment.
-   Put the mock framework into "replay" mode.
-   Run the code under test.
-   Apply any assertions as you normally would.
-   The mock framework will raise exceptions if the mock objects are called incorrectly, such as with the wrong arguments or too many times, or insufficiently, such as an expected method was not called.

There are several Python mock object frameworks.
Dexterity itself uses a powerful one called [`mocker`](https://labix.org/mocker), via the [`plone.mocktestcase`](https://pypi.org/project/plone.mocktestcase/) integration package.
You are encouraged to read the documentation for those two packages to better understand how mock testing works, and what options are available.

```{note}
Take a look at the tests in `plone.dexterity` if you're looking for more examples of mock tests using `plone.mocktestcase`.
```

To use the mock testing framework, we first need to depend on `plone.mocktestcase`.
As usual, we add it to {file}`setup.py` and re-run buildout.

```python
install_requires=[
    # ...
    "plone.mocktestcase",
],
```

As an example test case, consider the following class in {file}`test_presenter.py`.

```python
import unittest

# ...

from plone.mocktestcase import MockTestCase
from zope.app.container.contained import ObjectAddedEvent
from example.conference.presenter import notifyUser

class TestPresenterUnit(MockTestCase):

    def test_notify_user(self):

        # dummy presenter
        presenter = self.create_dummy(
                __parent__=None,
                __name__=None,
                title="Jim",
                absolute_url = lambda: "http://example.org/presenter",
            )

        # dummy event
        event = ObjectAddedEvent(presenter)

        # search result for acl_users
        user_info = [{"email": "jim@example.org", "id": "jim"}]

        # email data
        message = "A presenter called Jim was added here http://example.org/presenter"
        email = "jim@example.org"
        sender = "test@example.org"
        subject = "Is this you?"

        # mock tools/portal

        portal_mock = self.mocker.mock()
        self.expect(portal_mock.getProperty("email_from_address")).result("test@example.org")

        portal_url_mock = self.mocker.mock()
        self.mock_tool(portal_url_mock, "portal_url")
        self.expect(portal_url_mock.getPortalObject()).result(portal_mock)

        acl_users_mock = self.mocker.mock()
        self.mock_tool(acl_users_mock, "acl_users")
        self.expect(acl_users_mock.searchUsers(fullname="Jim")).result(user_info)

        mail_host_mock = self.mocker.mock()
        self.mock_tool(mail_host_mock, "MailHost")
        self.expect(mail_host_mock.send(message, email, sender, subject))


        # put mock framework into replay mode
        self.replay()

        # call the method under test
        notifyUser(presenter, event)

        # we could make additional assertions here, e.g. if the function
        # returned something. The mock framework will verify the assertions
        # about expected call sequences.

# ...

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
```

Note that the other tests in this module have been removed for the sake of brevity.

If you are not familiar with mock testing, it may take a bit of time to get your head around what's going on here.
Let's run though the test.

-   First, we create a dummy presenter object.
    This is *not* a mock object, it's just a class with the required minimum set of attributes, created using the `create_dummy()` helper method from the `MockTestCase` base class.
    We use this type of dummy because we are not interested in making any assertions on the `presenter` object: it is used as an "input" only.
-   Next, we create a dummy event.
    Here we have opted to use a standard implementation from `zope.app.container`.
-   We then define a few variables that we will use in the various assertions and mock return values: the user data that will form our dummy user search results, and the email data passed to the mail host.
-   Next, we create mocks for each of the tools that our code needs to look up.
    For each, we use the `expect()` method from `MockTestCase` to make some assertions.
    For example, we expect that `getPortalObject()` will be called (once) on the `portal_url` tool, and it should return another mock object, the `portal_mock`.
    On this, we expect that `getProperty()` is called with an argument equal to `"email_from_address"`.
    The mock will then return `"test@example.org"`.
    Take a look at the `mocker` and `plone.mocktestcase` documentation to see the various other types of assertions you can make.
-   The most important mock assertion is the line `self.expect(mail_host_mock.send(message, email, sender, subject))`.
    This asserts that the `send()` method gets called with the required message, recipient address, sender address, and subject, exactly once.
-   We then put the mock into replay mode, using `self.replay()`.
    Up until this point, any calls on our mock objects have been to record expectations and specify behaviour.
    From now on, any call will count towards verifying those expectations.
-   Finally, we call the code under test with our dummy presenter and event.
-   In this case, we don't have any "normal" assertions, although the usual unit test assertion methods are all available if you need them, for example, to test the return value of the method under test.
    The assertions in this case are all coming from the mock objects.
    The `tearDown()` method of the `MockTestCase` class will in fact check that all the various methods were called exactly as expected.

To run these tests, use the normal test runner.

```shell
./bin/test example.conference -t TestPresenterMock
```

Note that mock tests are typically as fast as unit tests, so there is typically no need for something like roadrunner.


## Mock testing caveats

Mock testing is a somewhat controversial topic.
On the one hand, it allows you to write tests for things that are often difficult to test, and a mock framework can—once you are familiar with it—make child's play out of the often laborious task of creating reliable test doubles.
On the other hand, mock based tests are inevitably tied to the implementation of the code under test, and sometimes this coupling can be too tight for the test to be meaningful.
Using mock objects normally also means that you need a very good understanding of the external APIs you are mocking.
Otherwise, your mock may not be a good representation of how these systems would behave in the real world.
Much has been written on this, including [_Mocks Aren't Stubs_ by Martin Fowler](https://www.martinfowler.com/articles/mocksArentStubs.html).

As always, it pays to be pragmatic.
If you find that you can't write a mock based test without reading every line of code in the method under test and reverse engineering it for the mocks, then an integration test may be more appropriate.
In fact, it is prudent to have at least some integration tests in any case, since you can never be 100% sure your mocks are valid representations of the real objects they are mocking.

On the other hand, if the code you are testing is using well-defined APIs in a relatively predictable manner, mock objects can be a valuable way to test the "side effects" of your code, and a helpful tool to simulate things like exceptions and input values that may be difficult to produce otherwise.

Remember also that mock objects are not necessarily an "all or nothing" proposition.
You can use simple dummy objects or "real" instances in most cases, and augment them with a few mock objects for those difficult-to-replicate test cases.
