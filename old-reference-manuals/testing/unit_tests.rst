Writing unit tests
------------------

.. admonition:: description

    Now that you understand the principle of tests and how to run them, it's
    time to write some. We will start with simple unit tests using doctest syntax.

We will start by showing how to create a simple unit test with doctest
syntax. There is nothing Zope- or Plone-specific about this test. This
type of test is ideal for methods and classes that perform some kind of
well-defined operation on primitives or simple objects. The doctest
syntax is well-suited for explaining the inputs and outputs. Since the
tests are relatively few and/or descriptive, keeping the tests,
documentation and code close together makes sense.

Tests are usually found in a tests/ sub-package. In the example.tests
package, we have created a file called tests/test\_simple\_doctest.py.
This sets up a test suite to run doctests in the doc strings in the
module example.tests.context. Let’s look at the test setup first:

::

    """This is the setup for a doctest where the actual test examples are held in
    docstrings in a module.

    Here, we are not using anything Zope-specific at all. We could of course
    use the Zope 3 Component Architecture in the setup if we wanted. For that,
    take a look at test_zope3_doctest.py.

    However, we *do* use the zope.testing package, which provides improved
    version of Python's standard DocTestSuite, DocFileSuite and so on. If you
    don't want this dependency, just use doctest.DocTestSuite.
    """

    import unittest
    import zope.testing

    import example.tests.context

    def setUp(test):
        """We can use this to set up anything that needs to be available for
        each test. It is run before each test, i.e. for each docstring that
        contains doctests.

        Look at the Python unittest and doctest module documentation to learn
        more about how to prepare state and pass it into various tests.
        """

    def tearDown(test):
        """This is the companion to setUp - it can be used to clean up the
        test environment after each test.
        """

    def test_suite():
        return unittest.TestSuite((

            # Here, we tell the test runner to execute the tests in the given
            # module. The setUp and tearDown methods can be used to perform
            # test-specific setup and tear-down.

            zope.testing.doctest.DocTestSuite(example.tests.context,
                         setUp=setUp,          # setUp and tearDown are optional!
                         tearDown=tearDown),
            ))

There are a lot of comments here, and we show how to use setUp() and
tearDown() methods for additional initialisation and clean-up, if
necessary. The test runner will call the test\_suite() method and expect
a TestSuite object back. If desired, we could have put multiple test
suites referring to multiple modules into the TestSuite that is being
returned.

Here is the actual code under test, in context.py:

::

    from zope.interface import implements
    from example.tests.interfaces import IContext

    class Context(object):
        """An object used for testing. We will register an adapter from this
        interface to IUpperCaser in the test setup.

        Here's how you use it. First, import the class.

            >>> from example.tests.context import Context

        Then in-stan-ti-ate it (with me so far?):

            >>> my_context = Context()

        Okay, here's the tricky bit ... now we need to set the title:

            >>> my_context.title = u"Some string!"

        Phew ... did that work?

            >>> my_context.title
            u'Some string!'

        Yeah!
        """

        implements(IContext)

        def __init__(self, title=u""):
            self.title = title

Here is how we may run the tests from a buildout:

::

    ./bin/instance test -s example.tests -t context
    Running unit tests:
      Running:
    ....
    Ran 4 tests with 0 failures and 0 errors in 0.071 seconds.
