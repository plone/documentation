============
Status check
============

Introduction
============

It is good practice to regularly check if your web site is still up.
This may be done by a command line tool like ``httpok`` or some online service.
For this you don't want to query a possibly expensive page.
And you don't want to query anything that may be stored in an intermediate caching server.
There are a few options.


ok browser view
===============

Call ``http://plonesite-url/@@ok``.
Or if a tool is confused by the ``@`` signs, call ``http://plonesite-url/ok``.
You can also call this on the Zope site root.
This returns the text ``OK`` and sets headers to avoid caching.

This was introduced in the ``Products.CMFPlone`` package in Plone 4.3.12, 5.0.7, and 5.1b1.


ZopeTime
========

Call ``http://plonesite-url/ZopeTime``.
You can also call this on the Zope site root.
This will return the current time on the server.

This may be served by a caching server in front of Plone, so it does not guarantee that Plone is still live.

If you use the ``experimental.publishtraverse`` package, this will either give you a ``NotFound`` error, or log a warning each time it is called, due to lacking permissions.
And this may happen in core Plone in the future too.
