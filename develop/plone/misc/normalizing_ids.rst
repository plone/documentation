===============
Normalizing ids
===============

.. admonition:: Description

	How to convert arbitrary text input to URL/CSS/file/programming safe ids.


Introduction
============

Normalizers turns arbitrary string (with unicode letters) to machine friendly ASCII ids.
Plone provides different id normalizers.

E.g::

    åland -> aland

Plone has conversion utilities for

* For URIs and URLs (plone.i18n.normalizer.interfaces.IURLNormalizer)

* For filenames

* For HTML ids and CSS

Normalization depends on the locale. E.g. in English "æ" will be normalized as "ae" but in Finnish it will
be normalized "å" -> "a".

See `plone.i18n.normalizers package <https://github.com/plone/plone.i18n/blob/master/plone/i18n/normalizer/__init__.py>`_.

Examples
========

Simple example for CSS id::

    from zope.component import getUtility
    from plone.i18n.normalizer.interfaces import IIDNormalizer

    normalizer = getUtility(IIDNormalizer)
    id = "portlet-static-%s" % normalizer.normalize(header)

Hard-coded id localizer which directly uses class instance and does not allow override by utility configuration.
You can use normalizers this way also when getUtility() is not available (e.g. start up code)::

    from plone.i18n.normalizer import idnormalizer

    id = idnormalizer.normalize(u"ÅÄÖrjy")

Language specific example for URL::

    from zope.component import queryUtility
    from plone.i18n.normalizer.interfaces import IURLNormalizer

	# Get URL normalizer for language english
    util = queryUtility(IURLNormalizer, name="en")

To see available language specific localizers, see the source code of plone.i18n.normalizers package.

More examples:

* `Static text portlets normalizes portlet title for CSS class <https://github.com/plone/plone.portlet.static/blob/master/plone/portlet/static/static.py>`_.

Creating ids programmatically
-----------------------------

If you are creating content programmatically using invokeFactory() or by
calling the class constructor you need to provide the id yourself.

Below is an example how to generate id from a title. *container* is the
folderish object that will contain our new object.::

    import time
    import transaction
    from zope.container.interfaces import INameChooser

    # For the NameChooser to work, it needs our object to already exist.
    # We create our object with a temporary but unique id. Seconds since
    # epoch will do.
    oid = container.invokeFactory(portal_type, id=time.time())

    # It's necessary to save the object creation before we can rename it
    transaction.savepoint(optimistic=True)
    new_obj = container._getOb(oid)

    # Now we create and set a new user-friendly id from the object title
    title = "My Little Pony"
    oid = INameChooser(container).chooseName(title, new_obj)
    new_obj.setId(oid)
    new_obj.reindexObject()

Other
-----

`Enforcing normalization for old migrated context <https://plone.org/documentation/how-to/how-to-force-all-your-old-content-into-the-new-normalized-id-format>`_.

