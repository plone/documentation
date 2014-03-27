==========================
Basic integration tests 
==========================

.. admonition:: Description

		No product is complete without tests. 

To build high-quality software, you *must* provide automatic tests -
often known as “unit” tests (though tests for Archetypes products tend
to be “integration” tests, strictly speaking).

The `tutorial on testing and test-driven development`_ is essential
reading if you want to write high-quality software (and you don’t know
the techniques it advocates already). Please refer to it for details.

The example.archetype product contains basic tests that prove that the
product is properly installed, that it registers its types, and that an
InstantMessage object can actually be instantiated. If it contained more
functionality, there would have been more tests, but even simple
integration tests like this can be surprisingly useful - if you
accidentally broke the content type with some change, you’d notice that
it failed to install or instantiate.

The tests are in the “tests” directory. The file “base.py” contains some
base classes that are used for tests, to ensure the site is properly set
up:

::

    import unittest

    from zope.testing import doctestunit
    from zope.component import testing
    from Testing import ZopeTestCase as ztc

    from Products.Five import zcml
    from Products.Five import fiveconfigure
    from Products.PloneTestCase import PloneTestCase as ptc
    from Products.PloneTestCase.layer import PloneSite
    from Products.PloneTestCase.layer import onsetup

    @onsetup
    def setup_product():
        """Set up the package and its dependencies.
        
        The @onsetup decorator causes the execution of this body to be deferred
        until the setup of the Plone site testing layer. We could have created our
        own layer, but this is the easiest way for Plone integration tests.
        """
        
        fiveconfigure.debug_mode = True
        import example.archetype
        zcml.load_config('configure.zcml', example.archetype)
        fiveconfigure.debug_mode = False
            
        ztc.installPackage('example.archetype')
        

    setup_product()
    ptc.setupPloneSite(products=['example.archetype'])


    class InstantMessageTestCase(ptc.PloneTestCase):
        """Base class for integration tests.

        This may provide specific set-up and tear-down operations, or provide
        convenience methods.
        """

The actual tests are in “test\_setup.py”:

::

    from base import InstantMessageTestCase
    from example.archetype.interfaces import IInstantMessage

    class TestProductInstall(InstantMessageTestCase):

        def afterSetUp(self):
            self.types = ('InstantMessage',)

        def testTypesInstalled(self):
            for t in self.types:
                self.assertIn(t, self.portal.portal_types.objectIds(),
                              '%s content type not installed' % t)

        def testPortalFactoryEnabled(self):
            for t in self.types:
                self.assertIn(t, self.portal.portal_factory.getFactoryTypes().keys(),
                              '%s content type not installed' % t)

    class TestInstantiation(InstantMessageTestCase):

        def afterSetUp(self):
            # Adding an InstantMessage anywhere - can only be done by a Manager or Portal Owner
            self.setRoles(['Manager'])
            self.portal.invokeFactory('InstantMessage', 'im1')

        def testCreateInstantMessage(self):
            self.assertIn('im1', self.portal.objectIds())

        def testInstantMessageInterface(self):
            im = self.portal.im1
            self.assertTrue(IInstantMessage.providedBy(im))

    def test_suite():
        from unittest import TestSuite, makeSuite
        suite = TestSuite()
        suite.addTest(makeSuite(TestProductInstall))
        suite.addTest(makeSuite(TestInstantiation))
        return suite

To run these tests within your buildout environment:

::

    ./bin/instance test -s example.archetype

You may see output like:

::

     Ran 4 tests with 0 failures and 0 errors in 0.119 seconds.

If there was an error with one or more of the tests, you’d be told here!

Please refer to the `testing tutorial`_ for more about writing tests -
and writing *good* tests - and how to run them.

.. _tutorial on testing and test-driven development: /documentation/tutorial/testing
.. _testing tutorial: /documentation/tutorial/testing

