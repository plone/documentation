==========================
Upgrading Caching Products
==========================

Plone 3's primary caching add-on product, CacheFu (aka CacheSetup) is not compatible with Plone 4. It has been replaced by plone.app.caching, a more modern and powerful caching subsystem.

Many production Plone sites use the add-on CacheFu (aka CacheSetup) to boost site performance. This is a widely recognized "best practice." **However, CacheFu is not compatible with Plone 4.**

Do not despair: the Plone community has created a new, simpler and more powerful replacement for CacheFu called `plone.app.caching <https://pypi.python.org/pypi/plone.app.caching>`_, which is Plone 4 compatible.

If your Plone 3 site currently includes CacheFu/CacheSetup, you should:
* Uninstall CacheFu from your Plone 3 site **before upgrading it to Plone 4**. (If, after migration, your site triggers "AttributeError: getHTTPCachingHeaders" on file system resources, try reconfiguring CacheFu to not use a proxy and turn it off **before** uninstalling it.)
* After upgrading to Plone 3, install plone.app.caching and configure it appropriately.  If you have highly customized rules for CacheFu, you may need to recreate these for plone.app.caching.

**Do not attempt to upgrade a Plone 3 site to Plone 4 without uninstalling CacheFu first.** Your migrated site will fail to start up, and you won't be able to effectively remove CacheFu at this point.

However, if you should already find yourself in this situation before reading this document, `there does exist a Plone-4 compatible branch of CacheFu. <http://svn.plone.org/svn/collective/Products.CacheSetup/branches/matthewwilkes-plone4compat/>`_ This branch is unmaintained and not recommended for production use under Plone 4, but it works well enough to allow you to boot your instance and remove CacheFu.
