================
Sitemap protocol
================


Introduction
-------------

Sitemap is used to submit the site content to search engines.

* http://www.google.com/webmasters/

Plone sitemap
--------------

Plone supports basic sitemap out of the box.

* https://github.com/plone/plone.app.layout/blob/master/plone/app/layout/sitemap/sitemap.py

Customized sitemap
-------------------

Example

* https://plonegomobile.googlecode.com/svn/trunk/gomobile/gomobile.mobile/gomobile/mobile/browser/sitemap.py

Enabling sitemap programmatically
----------------------------------

For unit tests::

        # Sitemap must be enabled from the settings to access the view
        self.portal.portal_properties.site_properties.enable_sitemap = True

