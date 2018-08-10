=================
 Unit testing
=================


Introduction
============

Unit tests are automated tests created by the developer to ensure that the
add-on product is intact in the current product configuration. Unit tests
are regression tests and are designed to catch broken functionality over the
code evolution.

Running unit tests
===================

Since Plone 4, it is recommended to use ``zc.testrunner``  to run the test
suites.  You need to add it to your ``buildout.cfg``, so that the ``test``
command will be generated.

.. code-block:: cfg

    parts =
       ...
       test

    [test]
    recipe = zc.recipe.testrunner
    defaults = ['--auto-color', '--auto-progress']
    eggs =
        ${instance:eggs}


Running tests for one package:

.. code-block:: console

    bin/test -s package.subpackage

Running tests for one test case:

.. code-block:: console

    bin/test -s package.subpackage -t TestCaseClassName

Running tests for two test cases:

.. code-block:: console

    bin/test -s package.subpackage -t TestClass1|TestClass2

To drop into the pdb debugger after each test failure:

.. code-block:: console

    bin/test -s package.subpackage -D

To exclude tests:

.. code-block:: console

    bin/test -s package.subpackage -t !test_name

To list tests that will be run:

.. code-block:: console

    bin/test -s package.subpackage --list-tests

The following will run tests for *all* Plone add-ons: useful to check
whether you have a set of component that function well together:

.. code-block:: console

    bin/test

.. warning::

    The test runner does not give an error if you supply invalid package and
    test case name.  Instead it just simply doesn't execute tests.

More information:

* https://plone.org/documentation/manual/upgrade-guide/version/upgrading-plone-3-x-to-4.0/updating-add-on-products-for-plone-4.0/no-longer-bin-instance-test-use-zc.recipe.testrunner

AttributeError: 'module' object has no attribute 'test_suite'
-------------------------------------------------------------

If you get the above error message there are two potential reasons:

* You have both a ``tests.py`` file and a ``tests`` folder.

* Old version: Zope version X unit test framework was updated not to need
  an explicit ``test_suite`` declaration in the ``test`` module any more.
  Instead, all subclasses of ``TestCase`` are automatically picked.
  However, this change is backwards incompatible.

Test coverage
=============

Zope test running can show how much of your code is covered by automatic
tests:

* https://pypi.python.org/pypi/plone.testing#coverage-reporting

Running tests against Python egg
===================================

You might need to add additional setup.py options to get your tests work

* http://rpatterson.net/blog/running-tests-in-egg-buildouts

Creating unit tests
====================

For any new test suites, you should be using `plone.app.testing`, your next step should be to
`read the documentation </external/plone.app.testing/docs/source>`.

You may come across `Products.PloneTestCase <https://pypi.python.org/pypi/Products.PloneTestCase>` in older code.
Also interesting is `ZopeTestCase <http://www.zope.org/Members/shh/ZopeTestCaseWiki/ApiReference>`.

Miscellaneous hints
===================

Setting log level in unit tests
-------------------------------

Many components use the ``DEBUG`` output level, while the default output
level for unit testing is ``INFO``.  Import messages may go unnoticed during
the unit test development.

Add this to your unit test code::

    def enableDebugLog(self):
        """ Enable context.plone_log() output from Python scripts """
        import sys, logging
        from Products.CMFPlone.log import logger
        logger.root.setLevel(logging.DEBUG)
        logger.root.addHandler(logging.StreamHandler(sys.stdout))

Test outgoing email messages
----------------------------

The ``MailHost`` code has changed in Plone 4. For more detail about the
changes please read the relevant section in the `Plone Upgrade Guide`_.
According to that guide we can reuse some of the test code in
``Products.CMFPlone.tests``.

.. _`Plone Upgrade Guide`: https://plone.org/documentation/manual/upgrade-guide/version/upgrading-plone-3-x-to-4.0/updating-add-on-products-for-plone-4.0/mailhost.securesend-is-now-deprecated-use-send-instead

Here's some example of a ``unittest.TestCase`` based on the excellent ``plone.app.testing``
framework. Adapt it to your own needs.

.. code-block:: python

    #Pythonic libraries
    import unittest2 as unittest
    from email import message_from_string

    #Plone
    from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
    from plone.app.testing import login, logout
    from plone.app.testing import setRoles
    from plone.testing.z2 import Browser

    from Acquisition import aq_base
    from zope.component import getSiteManager
    from Products.CMFPlone.tests.utils import MockMailHost
    from Products.MailHost.interfaces import IMailHost
    import transaction

    #hkl namespace
    from holokinesislibros.purchaseorder.testing import\
        HKL_PURCHASEORDER_FUNCTIONAL_TESTING


    class TestOrder(unittest.TestCase):

        layer = HKL_PURCHASEORDER_FUNCTIONAL_TESTING

        def setUp(self):
            self.app = self.layer['app']
            self.portal = self.layer['portal']
            self.portal._original_MailHost = self.portal.MailHost
            self.portal.MailHost = mailhost = MockMailHost('MailHost')
            sm = getSiteManager(context=self.portal)
            sm.unregisterUtility(provided=IMailHost)
            sm.registerUtility(mailhost, provided=IMailHost)

            self.portal.email_from_address = 'noreply@holokinesislibros.com'
            transaction.commit()

        def tearDown(self):
            self.portal.MailHost = self.portal._original_MailHost
            sm = getSiteManager(context=self.portal)
            sm.unregisterUtility(provided=IMailHost)
            sm.registerUtility(aq_base(self.portal._original_MailHost),
                               provided=IMailHost)

        def test_mockmailhost_setting(self):
            #open contact form
            browser = Browser(self.app)
            browser.open('http://nohost/plone/contact-info')
            # Now fill in the form:

            form = browser.getForm(name='feedback_form')
            form.getControl(name='sender_fullname').value = 'T\xc3\xa4st user'
            form.getControl(name='sender_from_address').value = 'test@plone.test'
            form.getControl(name='subject').value = 'Saluton amiko to\xc3\xb1o'
            form.getControl(name='message').value = 'Message with funny chars: \xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\xb1.'

            # And submit it:
            form.submit()
            self.assertEqual(browser.url, 'http://nohost/plone/contact-info')
            self.assertIn('Mail sent', browser.contents)

            # As part of our test setup, we replaced the original MailHost with our
            # own version.  Our version doesn't mail messages, it just collects them
            # in a list called ``messages``:
            mailhost = self.portal.MailHost
            self.assertEqual(len(mailhost.messages), 1)
            msg = message_from_string(mailhost.messages[0])

            self.assertEqual(msg['MIME-Version'], '1.0')
            self.assertEqual(msg['Content-Type'], 'text/plain; charset="utf-8"')
            self.assertEqual(msg['Content-Transfer-Encoding'], 'quoted-printable')
            self.assertEqual(msg['Subject'], '=?utf-8?q?Saluton_amiko_to=C3=B1o?=')
            self.assertEqual(msg['From'], 'noreply@holokinesislibros.com')
            self.assertEqual(msg['To'], 'noreply@holokinesislibros.com')
            msg_body = msg.get_payload()
            self.assertIn(u'Message with funny chars: =C3=A1=C3=A9=C3=AD=C3=B3=C3=BA=C3=B1',
                          msg_body)


Unit testing and the Zope component architecture
------------------------------------------------

If you are dealing with the Zope component architecture at a low level in
your unit tests, there are some things to remember, because the global site
manager doesn't behave properly in unit tests.

See discussion: http://plone.293351.n2.nabble.com/PTC-global-components-bug-tp3413057p3413057.html

Below are examples how to run special ZCML snippets for your unit tests.

.. code-block:: python

    import unittest
    from base import PaymentProcessorTestCase
    from Products.Five import zcml
    from zope.configuration.exceptions import ConfigurationError
    from getpaid.paymentprocessors.registry import paymentProcessorRegistry

    configure_zcml = '''
    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:five="http://namespaces.zope.org/five"
        xmlns:paymentprocessors="http://namespaces.plonegetpaid.com/paymentprocessors"
        i18n_domain="foo">


        <paymentprocessors:registerProcessor
           name="dummy"
           processor="getpaid.paymentprocessors.tests.dummies.DummyProcessor"
           selection_view="getpaid.paymentprocessors.tests.dummies.DummyButton"
           thank_you_view="getpaid.paymentprocessors.tests.dummies.DummyThankYou"
           />

    </configure>'''


    bad_processor_zcml = '''
    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:five="http://namespaces.zope.org/five"
        xmlns:paymentprocessors="http://namespaces.plonegetpaid.com/paymentprocessors"
        i18n_domain="foo">


        <paymentprocessors:registerProcessor
           name="dummy"
           selection_view="getpaid.paymentprocessors.tests.dummies.DummyButton"
           thank_you_view="getpaid.paymentprocessors.tests.dummies.DummyThankYou"
           />


    </configure>'''




    class TestZCML(PaymentProcessorTestCase):
        """ Test ZCML directives """


        def test_register(self):
            """ Check that ZCML entry gets added to our processor registry """
            zcml.load_string(configure_zcml)


            # See that our processor got registered
            self.assertEqual(len(papaymentProcessorRegistryistry.items()), 1)


        def test_bad_processor(self):
            """ Check that ZCML entry which has bad processor declaration is caught """


            try:
                zcml.load_string(bad_processor_zcml)
                raise AssertionError("Should not be never reached")
            except ConfigurationError, e:
                pass
