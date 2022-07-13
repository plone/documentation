================
Testing Cookbook
================

These are test snippets useful for common use cases.


General snippets
================

Test portal title::

    def test_portal_title(self):
        self.assertEqual("Plone site", self.portal.getProperty('title'))


Test if view is protected::

    def test_view_is_protected(self):
        from AccessControl import Unauthorized
        self.logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@view-name')


Test if object exists in folder::

    def test_object_in_folder(self):
        self.assertNotIn('object_id', self.portal.objectIds())


JavaScript registered::

    def test_js_available(self):
        jsreg = getattr(self.portal, 'portal_javascripts')
        script_ids = jsreg.getResourceIds()
        self.assertIn('my-js-file.js', script_ids)


CSS registered::

    def test_css_available(self):
        cssreg = getattr(self.portal, 'portal_css')
        stylesheets_ids = cssreg.getResourceIds()
        self.assertIn('MyCSS.css', stylesheets_ids)


Test that a certain skin layer is present in portal_skins::

    def test_skin_layer_installed(self):
        self.assertIn('my-skin-layer', self.skins.objectIds())
        self.assertIn('attachment_widgets', self.skins.objectIds())


Testing a clean uninstall
=========================

.. admonition:: Description

        How to test that your Plone add-on uninstalls cleanly


Introduction
------------

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

* Export Plone site through the Management Interface as zexp

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
        from Products.CMFPlone.utils import get_installer

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
                qi = get_installer(self.portal)

                try:
                    qi.uninstall_product(name)
                except:
                    pass
                qi.install_product(name)

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
