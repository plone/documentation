Integration doctests using PloneTestCase
----------------------------------------

.. admonition:: description

    The PloneTestCase integration test setup can also be used in doctests

The choice of test case classes over doctest is purely one of syntactic
preference. We can use the test setup from the previous section (in
base.py) in a doctest as well. This type of test is more useful for
documenting the integration of your code with Zope/Plone in a narrative
fashion.

There is no change to tests/base.py for this type of setup. However, we
must be careful to use a test class that derives from
FunctionalTestCase, since this performs the initialisation necessary for
doctests. The test setup is found in
tests/test\_integration\_doctest.py:

::

    """This is an integration doctest test. It uses PloneTestCase and doctest
    syntax.
    """

    import unittest
    import doctest

    from zope.testing import doctestunit
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

            # The actual test is in integration.txt

            ztc.ZopeDocFileSuite(
                'tests/integration.txt', package='example.tests',
                test_class=base.ExampleFunctionalTestCase,
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
                            doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            # We could add more doctest files here as well, by copying the file
            # block above.

            ])

Here, we set ExampleFunctionalTestCase from base.py as the test\_class,
which means that self in the doctest will be the same as self in the
test class we saw in the previous section. In particular, we can access
variables such as self.portal and self.folder. We also set some common
doctest option flags - reporting only the first failure (to avoid overly
long error output when an example early on in the doctest fails),
normalising whitespace (so that we can use newlines freely) and allowing
the ellipsis operator everywhere (as opposed to having to turn it on
each time we want to use it). Look at the doctest module documentation
for more information.

The test itself, in tests/integration.txt, is written much like the
other doctests we have seen:

::

    ======================
    An integration doctest
    ======================

    This test is an integration test that uses PloneTestCase. Here, 'self' is
    the test class, so we can use 'self.folder', 'self.portal' and so on. The
    setup is done in teststest_integration_doctest.py

    Being a doctest, we can tell a story here.

    For example, let's say a user had a dying wish: to add a news item. We'll do
    that using the standard Plone API.

        >>> self.folder.invokeFactory('News Item', 'news-item')
        'news-item'

    That's great, but really, he wanted to add it to the portal root:

        >>> self.portal.invokeFactory('News Item', 'news-item')
        Traceback (most recent call last):
        ...
        Unauthorized: Cannot create News Item

    Whoops! Too bad!

    At least we got to demonstrate the ellipsis operator, which
    matches arbitrary text. We enabled this in test_integration_doctest.py. It
    is also possible to enable (or disable) this flag on a single statement.
    See the Python doctest documentation for more information.

To run this test on its own, we would do:

::

      ./bin/instance test -s example.tests -t integration.txt
        Running:
      ..
        Ran 2 tests with 0 failures and 0 errors in 0.384 seconds.

Again, we have cut out some of the output from PloneTestCase.
