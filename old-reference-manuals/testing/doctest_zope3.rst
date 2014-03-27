Testing a Zope 3 component with a separate doctest file
-------------------------------------------------------

.. admonition:: description

    Sometimes, we may need to perform additional set-up for our tests to run properly.

In the previous example, we wrote a doctest in a docstring. As tests
become more complex or require more involved configuration, it is
usually better to separate the actual test into a text file. Sometimes,
this can be the README.txt file of a package. This is the approach
favoured by Zope 3 components.

In this example, we will register an adapter that is used in a doctest.
This doctest also serves to illustrate how this particular adapter
should be used.  This style of test is great when the emphasis is on the
documentation as well as the test. Note that we do not load the
package’s ZCML in its entirely. Instead, we register the required
components explicitly. This means that we retain control over what is
executed in the test. We use the zope.component.testing.tearDown method
to ensure that our test environment is properly cleaned up.

In the example.tests package, we have the following test setup in
tests/test\_zope3\_doctest.py:

::

    """This is the setup for a doctest that tests a Zope 3 component.

    There is really nothing too different from a "plain Python" test. We are not
    parsing ZCML, for example. However, we use some of the helpers from Zope 3
    to ensure that the Component Architecture is properly set up and torn down.
    """

    import unittest

    import zope.testing
    import zope.component

    def setUp(test):
        """This method is used to set up the test environment. We pass it to the
        DocFileSuite initialiser. We also pass a tear-down, but in this case,
        we use the tear-down from zope.component.testing, which takes care of
        cleaning up Component Architecture registrations.
        """

        # Register the adapter. See zope.component.interfaces for more

        from example.tests.context import UpperCaser
        zope.component.provideAdapter(UpperCaser)

    def test_suite():
        return unittest.TestSuite((

            # Here, we tell the test runner to execute the tests in the given
            # file. The setUp and tearDown methods employed make use of the Zope 3
            # Component Architecture, but really there is nothing Zope-specific
            # about this. If you want to test "plain-Python" this way, the setup
            # is the same.

            zope.testing.doctest.DocFileSuite('tests/zope3.txt',
                         package='example.tests',
                         setUp=setUp,
                         tearDown=zope.component.testing.tearDown),
            ))

Notice how we use a custom setUp() method to register the custom
adapter, and then reference zope.component.testing.tearDown for the
tear-down method.

This refers to the file zope3.txt, which looks like this:

::

    ==========================
    A Zope 3 component doctest
    ==========================

    This is the type of test found most commonly in Zope 3. We have a custom
    setup method (in test_zope3_doctest.py) which registers the components we
    need for the test. We can then use those here. ZCML is not processed directly,
    nor do we have a full Zope 2/Plone environment available. This makes the test
    more isolated (and faster!). Often, we may choose to use mock implementations
    of certain components in order to make the test properly isolated.

    Of course, we should still tell a story with this documentation.

    Let's say we had one of our really exciting context objects:

        >>> from example.tests.context import Context
        >>> context = Context()
        >>> context.title = u"Some puny title"

    Of course, that's nice, but what if we wanted to make a bit more of an impact?
    We can use our handy upper-caser adapter!

        >>> from example.tests.interfaces import IUpperCaser
        >>> shout = IUpperCaser(context)
        >>> shout.title
        u'SOME PUNY TITLE'

    Wow!

To run just this test, we may do:


::

    ./bin/instance test -s example.tests -t zope3.txt
    Running unit tests:
      Running:
    ..
      Ran 2 tests with 0 failures and 0 errors in 0.010 seconds.
