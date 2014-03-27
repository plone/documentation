Writing a PloneTestCase unit/integration test
---------------------------------------------

.. admonition:: description

    Sometimes, we need access to a full-blown Plone instance in order to effectively write tests

PloneTestCase, which in turn uses ZopeTestCase, is used to set up a full
Zope environment, including a Plone instance, for testing. This type of
test is very convenient and often necessary because content types, tools
and other parts of Plone have hard dependencies on various underlying
Zope, CMF and Plone components. It is generally better to write simpler
tests, however, both because they provide better isolation (thus testing
the component more directly and under better controlled circumstances)
and because they execute faster.

PloneTestCase-tests are often referred to as “unit tests”, but in truth
they are *integration* tests, since they depend on a “live” Zope
instance and thus test the integration between your code and the
underlying framework. We can use the PloneTestCase setup to run
doctests, as we will see in the next section.

Here, however, we will demonstrate how to use unittest.TestCase classes,
where each test is a method on a class (with a name beginning with test)
This type of test is not as good for documentation, but can be very
useful for systematically executing many variations on the same test.
Some developers also find this type of test easier to debug, since it is
plain Python code which can be stepped through using the debugger.

In the example.tests package, we have tests/base.py. This does not
contain any tests, but performs the necessary configuration to set up
the test fixture:

::

    """Test setup for integration and functional tests.

    When we import PloneTestCase and then call setupPloneSite(), all of Plone's
    products are loaded, and a Plone site will be created. This happens at module
    level, which makes it faster to run each test, but slows down test runner
    startup.
    """

    from Products.Five import zcml
    from Products.Five import fiveconfigure

    from Testing import ZopeTestCase as ztc

    from Products.PloneTestCase import PloneTestCase as ptc
    from Products.PloneTestCase.layer import onsetup

    #
    # When ZopeTestCase configures Zope, it will *not* auto-load products in
    # Products/. Instead, we have to use a statement such as:
    #
    #   ztc.installProduct('SimpleAttachment')
    #
    # This does *not* apply to products in eggs and Python packages (i.e. not in
    # the Products.*) namespace. For that, see below.
    #
    # All of Plone's products are already set up by PloneTestCase.
    #

    @onsetup
    def setup_product():
        """Set up the package and its dependencies.

        The @onsetup decorator causes the execution of this body to be deferred
        until the setup of the Plone site testing layer. We could have created our
        own layer, but this is the easiest way for Plone integration tests.
        """

        # Load the ZCML configuration for the example.tests package.
        # This can of course use <include /> to include other packages.

        fiveconfigure.debug_mode = True
        import example.tests
        zcml.load_config('configure.zcml', example.tests)
        fiveconfigure.debug_mode = False

        # We need to tell the testing framework that these products
        # should be available. This can't happen until after we have loaded
        # the ZCML. Thus, we do it here. Note the use of installPackage() instead
        # of installProduct().
        #
        # This is *only* necessary for packages outside the Products.* namespace
        # which are also declared as Zope 2 products, using
        # <five:registerPackage /> in ZCML.

        # We may also need to load dependencies, e.g.:
        #
        #   ztc.installPackage('borg.localrole')
        #

        ztc.installPackage('example.tests')

    # The order here is important: We first call the (deferred) function which
    # installs the products we need for this product. Then, we let PloneTestCase
    # set up this product on installation.

    setup_product()
    ptc.setupPloneSite(products=['example.tests'])

    class ExampleTestCase(ptc.PloneTestCase):
        """We use this base class for all the tests in this package. If necessary,
        we can put common utility or setup code in here. This applies to unit
        test cases.
        """

    class ExampleFunctionalTestCase(ptc.FunctionalTestCase):
        """We use this class for functional integration tests that use doctest
        syntax. Again, we can put basic common utility or setup code in here.
        """

Notice how we can explicitly install third party products (and egg-based packages which use product semantics) and then tell PloneTestCase to quick-install these into the test fixture site. The test runner will not automatically load all products in the Products.* namespace, nor will it execute ZCML for packages outside Products.* automatically.

The test class which uses this environment is found in tests/test_integration_unit.py:

::

    """This is an integration "unit" test. It uses PloneTestCase, but does not
    use doctest syntax.

    You will find lots of examples of this type of test in CMFPlone/tests, for
    example.
    """

    import unittest
    from example.tests.tests.base import ExampleTestCase

    from Products.CMFCore.utils import getToolByName

    class TestSetup(ExampleTestCase):
        """The name of the class should be meaningful. This may be a class that
        tests the installation of a particular product.
        """

        def afterSetUp(self):
            """This method is called before each single test. It can be used to
            set up common state. Setup that is specific to a particular test
            should be done in that test method.
            """
            self.workflow = getToolByName(self.portal, 'portal_workflow')

        def beforeTearDown(self):
            """This method is called after each single test. It can be used for
            cleanup, if you need it. Note that the test framework will roll back
            the Zope transaction at the end of each test, so tests are generally
            independent of one another. However, if you are modifying external
            resources (say a database) or globals (such as registering a new
            adapter in the Component Architecture during a test), you may want to
            tear things down here.
            """

        def test_portal_title(self):

            # This is a simple test. The method needs to start with the name
            # 'test'.

            # Look at the Python unittest documentation to learn more about hte
            # kinds of assertion methods which are available.

            # PloneTestCase has some methods and attributes to help with Plone.
            # Look at the PloneTestCase documentation, but briefly:
            #
            #   - self.portal is the portal root
            #   - self.folder is the current user's folder
            #   - self.logout() "logs out" so that the user is Anonymous
            #   - self.setRoles(['Manager', 'Member']) adjusts the roles of the current user

            self.assertEqual("Plone site", self.portal.getProperty('title'))

        def test_able_to_add_document(self):
            new_id = self.folder.invokeFactory('Document', 'my-page')
            self.assertEqual('my-page', new_id)

        # Keep adding methods here, or break it into multiple classes or
        # multiple files as appropriate. Having tests in multiple files makes
        # it possible to run tests from just one package:
        #
        #   ./bin/instance test -s example.tests -t test_integration_unit


    def test_suite():
        """This sets up a test suite that actually runs the tests in the class
        above
        """
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestSetup))
        return suite

Here, we have a test suite with one test class - we could have added more classes if
necessary. The afterSetUp() and beforeTearDown() methods - if present - are called
immediately before and after each test. After a test is run, the transaction is rolled
back, causing tests to run in isolation. You only really need explicit teardown if
your tests make permantent changes that are not covered by the ZODB transaction machinery.

You are free to add whatever helper methods you wish to your unit test class, but any
method with a name starting with test will be executed as a test. Tests are usually
written to be as concise (not to be confused with "obfuscated") as possible.

Notice the calls to methods like self.assertEqual() or self.assertTrue(). These are
the assertion methods that do the actual testing. If any of these fail, that test is
counted as a failure and you'll get an ugly F in your test output.

To run the test, we would do:

::

    ./bin/instance test -s example.tests -t test_integration_unit
      Running:
    ..
      Ran 2 tests with 0 failures and 0 errors in 0.178 seconds.

There is actually more output than this, as PloneTestCase installs a number of products and processes ZCML.

Rules of thumb
~~~~~~~~~~~~~~

There are some basic rules of thumb for writing unit tests with
PloneTestCase you should be aware of:

* Write test first, don't put it off, and don't be lazy (did we say this enough already?)
* Write one test (i.e. one method) for each thing you want to test
* Keep related tests together (i.e. in the same test case class)
* Be pragmatic. If you want to test every combination of inputs and outputs you will
  probably go blue in the face, and the additional tests are unlikely to be of much value.
  Similarly, if a method is complicated, don't just test the basic case. This comes with
  experience, but in general, you should test common cases, edge cases and preferably cases
  in which the method or component is expected to fail (i.e. test that it fails as
  expected - you still shouldn't get any F's in your test output!).
* Keep tests simple. Don't try to be clever, don't over-generalise. When a test fails,
  you need to easily determine whether it is because the test itself is wrong, or the
  thing it is testing has a bug.

Assertion and utility methods in the unit testing framework
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are quite a few assertion methods, most of which do basically the same thing - check
if something is True or False. Having a variety of names allows you to make your tests read
the way you want. The list of assertion methods can be found in the Python documentation
for unittest.TestCase. The most common ones are:

assertTrue(expr)
    Ensure expr is true
assertEqual(expr1, expr2)
    Ensure expr1 is equal to expr2
assertRaises(exception, callable, …)
    Make sure exception is raised by the callable. Note that callable
    here should be the name of a method or callable object, not an
    actual call, so you write e.g. self.assertRaises(AttributeError,
    myObject.myMethod, someParameter). Note lack of () after myMethod.
    If you included it, you’d get the exception raised in your test
    method, which is probably not what you want. Instead, the statement
    above will cause the unit testing framework to call
    myMethod(someParameter) (you can pass along any parameters you want
    after the calalble) and check for an AttributeError.
fail()
    Simply fail. This is useful if a test has not yet been completed, or
    in an if statement inside a test where you know the test has
    failed.

In addition to the unit testing framework assertion methods, ZopeTestCase and PloneTestCase include some helper methods and variables to help you interact with Zope. It's instructive to read the source code for these two products, but briefly, the key variables you can use in unit tests are:

self.portal
     The Plone portal the test is executing in

self.folder
     The member folder of the member you are executing as

And the key methods are:

self.logout()
    Log out, i.e. become anonymous
self.login()
    Log in again. Pass a username to log in as a different user.
self.setRoles(roles)
    Pass in a list of roles you want to have. For example, self.setRoles(('Manager',)) lets you be manager for a while. How nice.
self.setPermissions(permissions)
    Similarly, grant a number of permissions to the current user in self.folder.
self.setGroups(groups)
    Set which groups the test user is in.

Tips & Tricks
~~~~~~~~~~~~~

Good unit testing comes with experience. It's always useful to read the unit tests of code with which you are fairly familiar, to see how other people unit test. We'll cover a few hints here to get you thinking about how you approach your own tests:

*  Don’t be timid! Python, being a dynamic scripting language, lets you
   do all kinds of crazy things. You can rip a function right out from
   the Plone core and replace it with your own implementation in
   afterSetUp() or a test if that serves your testing purposes.
*  Similarly, replacing things like the MailHost with dummy
   implementations may be the only way to test certain features. Look at
   CMFPlone/tests/dummy.py for some examples of dummy objects.
*  Use tests to try things out. They are a safe environment. If you need
   to try something a bit out of the ordinary, writing them in a test is
   often the easiest way of seeing how something works.
*  During debugging, you can insert print statements in tests to get
   traces in your terminal when you execute the tests. Don’t check in
   code with printing tests, though. :)
*  Similarly, the python debugger is very valuable inside tests. Putting
   import pdb; pdb.set\_trace() inside your test methods lets you step
   through testing code and step into the code it calls. If you’re not
   familiar with the python debugger, your life is incomplete.
