Functional and system tests with zope.testbrowser
-------------------------------------------------

.. admonition:: description

    Whilst unit tests and doctests verify the correctness of individual methods
    and modules, functional tests test portions of the application as a whole,
    often from the point of view of the user, and typically aligned with use cases.
    System tests, in comparison, test the entire application as a black box.

No developer likes to click around the browser to check if that button
that was only supposed to show up in some cases really did show up.
Unfortunately, these are also the types of problems that most often
suffer from regressions, because templates are difficult (and slow) to
test.

Zope 3 has an elegant library called zope.testbrowser which lets you
write doctests that behave like a real web browser (almost… it cannot
yet handle JavaScript, which means that testing dynamic UIs that depend
on JavaScript is not possible, although `Selenium <http://seleniumhq.org/>`_ may be a viable
alternative here). You can open URLs, click links, fill in form fields
and test the HTTP headers, URLs and page contents that are returned from
Plone. In fact, you could test any website, not just Zope or Plone ones.

Functional tests are no replacement for unit tests. They test a slice of
functionality, typically as the user sees it. Thus, they may not
systematically include every aspect of the application. For example, a
functional test may check whether a “Delete” button is present, and even
that it works as expected, but should not be used to exhaustively test
whether the delete operation works in every possible edge case. Where
they excel, however, is in testing things like which options appear to
which users depending on roles and permissions, or simply to exercise
all the various templates used in a given product to make sure they
don’t break.

Here is an example from the example.tests package. The test setup is in
tests/test\_functional\_doctest.py:

::

    """This is a a functional doctest test. It uses PloneTestCase and doctest
    syntax. In the test itself, we use zope.testbrowser to test end-to-end
    functionality, including the UI.

    One important thing to note: zope.testbrowser is not JavaScript aware! For
    that, you need a real browser. Look at zope.testbrowser.real and Selenium
    if you require "real" browser testing.
    """

    import unittest
    import doctest


    from Testing import ZopeTestCase as ztc

    from example.tests.tests import base

    def test_suite():
        """This sets up a test suite that actually runs the tests in the class
        above
        """
        return unittest.TestSuite([

            # Here, we create a test suite passing the name of a file relative
            # to the package home, the name of the package, and the test base
            # class to use. Here, the base class is a full PloneTestCase, which
            # means that we get a full Plone site set up.

            # The actual test is in functional.txt

            ztc.ZopeDocFileSuite(
                'tests/functional.txt', package='example.tests',
                test_class=base.ExampleFunctionalTestCase,
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
                            doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            # We could add more doctest files here as well, by copying the file
            # block above.

            ])

This code is actually identical to the test setup for the integration
doctest in the previous section. The differences are found in the actual
test itself, which uses Products.Five.testbrowser.Browser, a Zope 2
compatibility wrapper around zope.testbrowser.Browser:

::

    ====================
    A functional doctest
    ====================

    This is a full-blown functional test. The emphasis here is on testing what
    the user may input and see, and the system is largely tested as a black box.
    We use PloneTestCase to set up this test as well, so we have a full Plone site
    to play with. We *can* inspect the state of the portal, e.g. using
    self.portal and self.folder, but it is often frowned upon since you are not
    treating the system as a black box. Also, if you, for example, log in or set
    roles using calls like self.setRoles(), these are not reflected in the test
    browser, which runs as a separate session.

    Being a doctest, we can tell a story here.

    First, we must perform some setup. We use the testbrowser that is shipped
    with Five, as this provides proper Zope 2 integration. Most of the
    documentation, though, is in the underlying zope.testbrower package.

        >>> from Products.Five.testbrowser import Browser
        >>> browser = Browser()
        >>> portal_url = self.portal.absolute_url()

    The following is useful when writing and debugging testbrowser tests. It lets
    us see all error messages in the error_log.

        >>> self.portal.error_log._ignored_exceptions = ()

    With that in place, we can go to the portal front page and log in. We will
    do this using the default user from PloneTestCase:

        >>> from Products.PloneTestCase.setup import portal_owner, default_password

        >>> browser.open(portal_url)

    We have the login portlet, so let's use that.

        >>> browser.getControl(name='__ac_name').value = portal_owner
        >>> browser.getControl(name='__ac_password').value = default_password
        >>> browser.getControl(name='submit').click()

    Here, we set the value of the fields on the login form and then simulate a
    submit click.

    We then test that we are still on the portal front page:

        >>> browser.url == portal_url
        True

    And we ensure that we get the friendly logged-in message:

        >>> "You are now logged in" in browser.contents
        True

    To learn more, look at the zope.testbrowser documentation and interfaces.
    There are also a few examples of testbrowser tests in Plone itself.

All the action happens with the browser object. This simulates a web browser (though
as stated above, one that does not support JavaScript), and has a pleasant API for
finding form controls and links and clicking on them. The variables browser.url and
browser.contents represent what would've been in the URL bar and the rendered view
of the page, respectively, and can be examined like any other variable.

zope.testbrowser has pretty comprehensive documentation in its README.txt file - which
is, of course, a runnable doctest. In brief, the most important methods of the
IBrowser interface (and thus the Browser class) are:

open(url)
    Open a given URL.
reload()
    Reload the current page, much as the Refresh button in your browser would do.
goBack(count=1)
    Simulate pressing the Back button count times.
getLink(text=None, url=None, id=None)
    Get an ILink (which you can then call click() on), either by the text inside the <a> tags, by the URL in the href attribute, or the id of the link.
getControl(label=None, name=None, index=None)
    Get an IControl, representing a form control, by label (either the value of a submit button or the contents of an associated <label> tag) or form name. The index argument is used to disambiguate if there is more than one control (e.g. index=0 gets the first one). Again, you can call click() on the control object to simulate clicking on it.

The IBrowser interface also provides some properties that can be used to examine
the state of the current page. The most important ones are:

url
    The full URL to the current page.
contents
    The full contents of the current page, as a string (usually containing HTML tags)
headers
    A dict of HTTP headers

Please refer to the `interfaces`_ and the `README file`_ for details on
the other methods and attributes, the interfaces for various types of
links and controls, and further examples.

.. _interfaces: http://svn.zope.org/zope.testbrowser/trunk/src/zope/testbrowser/interfaces.py?view=auto
.. _README file: http://svn.zope.org/zope.testbrowser/trunk/src/zope/testbrowser/README.txt?view=auto


Debugging functional tests
~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you will get errors from Zope resulting from some command executed using
the testbrowser. In this case, it can sometimes be difficult to know what the
underlying cause is. Two debugging aids exist to make this a bit easier.

First of all, make sure you see all errors in full by setting:

::

    >>> browser.handleErrors = False

If handleErrors is True (the default) you will get errors like HTTPError: HTTP
Error 404: Not Found or HTTPError: HTTP Error 500: Internal Server Error. Those
are probably not very useful to you. Setting handleErrors to False will show the
full exceptions Zope (or possibly the HTML rendering of the error page, depending
on the type of error).

Secondly, if you are using PloneTestCase, you can use Plone's error log. At the top of the example, we do:

::

    >>> self.portal.error_log._ignored_exceptions = ()

This means that errors such as NotFound and Unauthorized will be shown in the
error log. It may also be useful to enable Verbose Security in zope.conf (see the
comments in that file for details). Now, when a line appears that is throwing an
error you can't debug, you can do:

::

    >>> try:
    ...     browser.getControl('Save').click()
    ... except:
    ...     print self.portal.error_log.getLogEntries()[0]['tb_text']
    ...     import pdb; pdb.set_trace()
    >>> # continue as normal

This will print the most recent entry in the error log, and set a PDB break point.

Using a real browser to render the results of your tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you would like to see the output of browser.contents in a browser to
easily debug what's happening in your functional tests. To do so, place a PDB
break point in your tests as described above (import pdb; pdb.set_trace())
and type the following when you get to the PDB prompt while running the tests:

::
    >>> from Testing.ZopeTestCase.utils import startZServer
    >>> startZServer()

This will print a tuple like

::
    ('127.0.0.1', 55143)

containing an IP address and port where you can access the same test site that
the testbrowser is working with, in a real browser.

Functional tests vs. system tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A system test is one which treats the entire system as a black box, interacting
with it as a user would. A functional test is more focused on a single "vertical"
of functionality, typically linked to a particular use case.

For a functional test, it may be acceptable to examine the internal state of the
portal (using self.portal and the PloneTestCase.FunctionalTestCase class to build
a test suite) to provide assertions. A system test, by contrast, makes no such
assumptions. Ideally, you should be able to point a zope.testbrowser test at a
remote site running a fresh installation of your system, and have the tests pass.

Beyond that, the tools used to write a system test are the same. It is only the
approach to testing that changes. Whether you need one, or the other, or both,
will depend on the level of rigour you need in your tests, and how your system is
constructed. In general, though, true system tests are more rare than functional
(integration) tests and unit tests.
