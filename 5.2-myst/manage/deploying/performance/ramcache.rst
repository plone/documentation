=========
RAM Cache
=========

Introduction
============

The RAM cache is a Zope facility to create custom in-process caches.

Using memcached backend
=======================

By default, Zope uses an in-process memory cache. It is possible to replace
this with ``memcached``.

Advantages:

* All front-end clients share the cache.

* Cache survives over a client restart.

Memoizers
---------

Memoize's RAM cache can be replaced with a ``memcached`` backend with the
following snippet.

See the set-up for the https://plone.org/ site as an example:

* https://github.com/plone/Products.PloneOrg/blob/master/src/Products/PloneOrg/caching.py

RAM Cache
---------

The RAM cache is used e.g. as a rendered template cache backend.

You can add ``MemcachedManager`` to your Zope setup, and replace the
RamCache instance in the Management Interface with a new instance of ``MemcachedManager``
(keep the id the same).

* https://pypi.python.org/pypi/Products.MemcachedManager

Using custom RAM cache
======================

You want to use a custom cache if you think cache size or saturation will
pose problems.

The following advanced example shows how to enhance existing content type
text and description accessors by performing HTML transformations and
caching the result in a custom RAM cache.

Example::

    import logging

    import lxml.html

    from zope.app.cache import ram

    from Products.feedfeeder.content.item import FeedFeederItem
    from gomobile.xhtmlmp.transformers.xhtmlmp_safe import clean_xhtml_mp

    logger = logging.getLogger("GoMobile")

    logger.info("Running in feedfeeder monkey-patches")

    # Cache storing transformed XHTML
    xhtml_cache = ram.RAMCache()
    xhtml_cache.update(maxAge=86400, maxEntries=1000)

    # Dummy object to mark missing values from cache
    _marker = object()

    def cache(name):
        """ Special cache decorator which generates cache key based on context object and cache name """
        def decorator(fun):
            def replacement(context):
                key = str(context.UID()) + "." + name

                cached_value = xhtml_cache.query(key, default=_marker)
                if cached_value is _marker:
                    cached_value = fun(context)
                    xhtml_cache.set(cached_value, key)
                return cached_value
            return replacement
        return decorator


    def flush_cache(name, context):
        """ Clear entry in RAMCache

        global_key is function specific key, key is context specific key.

        """
        key = context.UID() + "." + name
        xhtml_cache.invalidate(key)


    #
    # Modify existing body text and description accessors so that
    # 1) HTML is cleaned
    # 2) The result cleaned HTML is cached in RAM
    #
    # We do not persistently want to store cleaned HTML,
    # since our cleaner might be b0rked and we want to
    # regenerate cleaned HTML when needed.
    #

    # Run in monkey patching
    FeedFeederItem._old_getText = FeedFeederItem.getText
    FeedFeederItem._old_setText = FeedFeederItem.setText
    FeedFeederItem._old_Description = FeedFeederItem.Description
    FeedFeederItem._old_setDescription = FeedFeederItem.setDescription

    @cache("text")
    def _getText(self):
        """ Body text accessor """
        text = FeedFeederItem._old_getText(self)

        if text:
            # can be None
            clean = clean_xhtml_mp(text)
            print "Cleaned text:" + clean
            return clean

        return text

    def _setText(self, value):
        FeedFeederItem._old_setText(self, value)
        flush_cache("text", self)

    @cache("description")
    def _Description(self):
        """ Description accessor """
        text = FeedFeederItem._old_Description(self)

        #print "Accessing description:" + str(text)

        # Remove any HTML formatting in the description
        if text:
            parsed = lxml.html.fromstring(text.decode("utf-8"))
            clean = lxml.html.tostring(parsed, encoding="utf-8", method="text").decode("utf-8")
            #print "Cleaned decsription:" + clean
            return clean

        return text

    def _setDescription(self, value):
        FeedFeederItem._old_setDescription(self, value)
        flush_cache("description", self)

    FeedFeederItem.getText = _getText
    FeedFeederItem.setText = _setText
    FeedFeederItem.Description = _Description
    FeedFeederItem.setDescription = _setDescription

ZCacheable
==========

``ZCacheable`` is an ancient Zope design pattern for caching.  It allows
persistent objects that are subclasses of ``OFS.Cacheable`` to have the
cache backend configured externally.

The cache type (cache id) in use is stored
:doc:`persistently </develop/plone/persistency/persistent>` per cache user object,
but the cache can be created at runtime (RAM cache) or externally
(``memcached``) depending on the situation.

.. note::

    Do not use ``ZCacheable`` in new code.

It takes optional backends which must be explicitly set::

    def enableCaching():
        pas=getPAS()
        if pas.ZCacheable_getManager() is None:
            pas.ZCacheable_setManagerId(manager_id="RAMCache")
        getLDAPPlugin().ZCacheable_setManagerId(manager_id="RAMCache")

The ``RAMCache`` above is per thread.
Clearing this cache for all ZEO clients is hard.

Some hints:

It is enabled per persistent object::

    >>> app.test2.acl_users.ZCacheable_isCachingEnabled()
    <Products.StandardCacheManagers.RAMCacheManager.RAMCache instance at 0x10a064cf8>

    >>> app.test2.acl_users.ZCacheable_enabled()
    1

Get known cache backends::

    >>> app.test2.acl_users.ZCacheable_getManagerIds()
    ({'id': 'caching_policy_manager', 'title': ''}, {'id': 'HTTPCache', 'title': ''}, {'id': 'RAMCache', 'title': ''}, {'id': 'ResourceRegistryCache', 'title': 'Cache for saved ResourceRegistry files'})

Disabling it (persistent change)::

    >>> app.test2.acl_users.ZCacheable_setManagerId(None)
    >>> app.test2.acl_users.ZCacheable_enabled()
    1
    >>> app.test2.acl_users.ZCacheable_getManagerIds()
    ({'id': 'caching_policy_manager', 'title': ''}, {'id': 'HTTPCache', 'title': ''}, {'id': 'RAMCache', 'title': ''}, {'id': 'ResourceRegistryCache', 'title': 'Cache for saved ResourceRegistry files'})
    >>> app.test2.acl_users.ZCacheable_isCachingEnabled()
    >>> app.test2.acl_users.ZCacheable_setEnabled(False)


More info:

* https://github.com/zopefoundation/Zope/blob/master/src/OFS/Cache.py

* https://github.com/plone/plone.app.ldap/blob/master/plone/app/ldap/ploneldap/util.py

Other resources
===============

* `plone.memoize source code <https://github.com/plone/plone.memoize/blob/master/plone/memoize/>`_.

* `zope.app.cache source code <https://pypi.python.org/pypi/zope.app.cache>`_
