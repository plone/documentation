=================
Zope Debug Prompt
=================

.. admonition:: Description

    Interacting with Plone from the Zope debug prompt.


Introduction
============

The Zope debug prompt is a way of starting a Zope client from the command line, and allows you to directly interact with Plone.

Some things that you can do through the debug prompt:

- Examine objects to see their properties/methods
- Update objects in bulk, as opposed to one at a time through the user interface.
- Produce reports or export data from objects

This is similar to the Python debug prompt (entering ``python`` at the command line) and the same whitespace restrictions apply.

Cautions
========

**With great power comes great responsibility.**

Interacting with Plone from the Zope debug prompt is a very powerful tool, and lets you quickly make changes that  might take hours or days to implement manually.

It is also a great way to severely damage your site, in a way that might take hours or days to fix.

Precautions for developing code that makes updates via the debug prompt:

- Log the changes that you're going to make using the ``print`` statement
- Only commit the transaction (``transaction.commit()``) after the code has run successfully.
- Attempt to develop the code in an idempotent (able to be run multiple times with no ill effects) manner.

Starting the debug prompt interactively
=======================================

This assumes that you are running Plone in a ZEO configuration on a \*NIX server, and your Zope clients run as the ``plone_daemon`` user.

After logging into your server, start the debug prompt with

.. code-block:: console

    sudo -u plone_daemon /path/to/zope/bin/client1 debug

The output will look something like::

    Starting debugger (the name "app" is bound to the top-level Zope object)
    2015-06-26 12:33:51 WARNING SecurityInfo Conflicting security declarations for "manage_pasteObjects"
    2015-06-26 12:33:51 WARNING SecurityInfo Class "CopyContainer" had conflicting security declarations
    2015-06-26 12:33:52 WARNING Init Class Products.Five.metaclass.RedirectsView has a security declaration for nonexistent method 'errors'

    >>>

There may be some additional warnings, based on the products installed.

From here, the ``app`` variable is equivalent to the root of your Zope instance.

A simple example::

    from AccessControl.SecurityManagement import newSecurityManager
    from Testing.makerequest import makerequest
    from zope.component.hooks import setSite
    from plone import api
    import transaction

    app = makerequest(app) # Enables functionality that expects a REQUEST

    app._p_jar.sync() # Syncs the debug prompt with any transactions

    site=app['Plone'] # Use your site id

    setSite(site) # Sets the current site as the active site

    # Simulate logging in as the Zope 'admin' user
    with api.env.adopt_user(username="admin"):
        # Grab the portal_catalog tool
        portal_catalog = api.portal.get_tool(name='portal_catalog')

        # Query the catalog for all results. Returns 'brains'
        results = portal_catalog.searchResults()

        # Print the number of objects in the catalog
        print u"My site has %d objects." % len(results)

Code Snippets
=============

`Sample code snippets <https://github.com/collective/code-snippets>`_ for use in the debug prompt.
