======================
 Clean uninstall
======================

.. admonition:: Description

        How to test that your Plone add-on uninstalls cleanly

.. contents:: :local:

Introduction
-------------

Clean uninstall means that removing your add-on does not leave Plone site to broken state.
Sometimes damage might not be noticed immediately, causing great frustration for the users.

Clean uninstall procedure is

* Use ``Add on installer`` to uninstall any add-ons. This MUST remove
  all add-on Python objects from the site ZODB database

* Remove eggs from the buildout, rerun buildout

If there are any Python objects, which classes come from the removed
egg, around the site cannot be exported or imported anymore. Also,
Plone upgrade might fail.

Clean uninstall test procedure
------------------------------

Manual procedure

* Create a Plone site from buildout, with your add-on egg present

* Install your add-on

* Play around with add-on to make sure it stores all its data (settings, local utilities,
  annotations, etc.)

* Uninstall add-on

* Export Plone site through ZMI as zexp

* Create another Plone site from vanilla buildout (no any add-ons installed)

* Import .zexp

* If .zexp does not contain any objects from your add-on egg, which is missing in vanilla
  Plone installation, your add-on installs cleanly

Example unit test
------------------

This code shows how to test that certain :doc`annotations </components/annotations>`
are correctly cleaned.

Example::

        """

            Check that the site is clean after uninstall.

        """

        __license__ = "GPL 2"
        __copyright__ = "2009-2011 mFabrik Research Oy"

        import unittest

        from zope.component import getUtility, queryUtility, queryMultiAdapter

        from Products.CMFCore.utils import getToolByName

        from gomobile.mobile.tests.base import BaseTestCase
        from gomobile.mobile.behaviors import IMobileBehavior, mobile_behavior_factory,  MobileBehaviorStorage

        from zope.annotation.interfaces import IAnnotations

        class TestUninstall(BaseTestCase):
            """ Test UA sniffing functions """


            def make_some_evil_site_content(self):
                """
                Add annotations etc. around the site
                """

                self.loginAsPortalOwner()
                self.portal.invokeFactory("Document", "doc")
                doc = self.portal.doc

                behavior = IMobileBehavior(doc)
                behavior.mobileFolderListing = False
                behavior.save()

                annotations = IAnnotations(doc)

            def uninstall(self, name="gomobile.mobile"):
                qi = self.portal.portal_quickinstaller

                try:
                    qi.uninstallProducts([name])
                except:
                    pass
                qi.installProduct(name)

            def test_annotations(self):
                """ Check that uninstaller cleans up annotations from the docs
                """
                self.make_some_evil_site_content()
                self.uninstall()

                annotations = IAnnotations(self.portal.doc)
                self.assertFalse("mobile" in annotations)



        def test_suite():
            suite = unittest.TestSuite()
            suite.addTest(unittest.makeSuite(TestUninstall))
            return suite


