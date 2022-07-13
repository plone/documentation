============================================
Manually Removing Local Persistent Utilities
============================================


.. admonition:: Description


    This document explains how you can manually remove local persistent utilities that were not properly removed from a product while uninstalling.


.. note::

  **Update**

  There is now a useful tool available, `wildcard.fixpersistentutilities <https://pypi.python.org/pypi/wildcard.fixpersistentutilities>`_ ,  to address these issues TTW (Through The Web). I would suggest trying it before you go through this article.


Purpose
-------

Occasionally you'll download and install a product in Plone that uses local persistent utilities.
This usually seems pretty innocent in itself; however, it sometimes happens that when you uninstall the product and remove its egg from the file system, the utility is still registered.
This will essentially break your instance unless you make the egg available again so the ZODB can reference the utilities during lookups.
This how-to will explain how to remove these utilities manually.

Symptoms
--------

You'll find zope throwing errors like this,

.. code-block:: console

  AttributeError: type object 'IQueue' has no attribute '__iro__'

or

.. code-block:: console

  AttributeError: type object 'ISalt' has no attribute '__iro__'


Prerequisites
-------------

You will need appropriate access to the zope server in order to run the site in debug mode.

Step by step
------------

First off, fire up the instance in debug mode

.. code-block:: console

  ./bin/instance debug

Get the site manager for your Plone instance. 'app' references the zope root.

.. code-block:: console

  sm = app.Plone.getSiteManager()



Then you'll want to import the guilty utility's interface, unregister it and delete it. It should look somethings like this,

.. code-block:: console

  from collective.product.interfaces import IUtility, INamedUtility

  # for unnamed utility
  util = sm.getUtility(IUtility)
  sm.unregisterUtility(IUtility)
  del util
  sm.utilities.unsubscribe((), IUtility)
  del sm.utilities.__dict__['_provided'][IUtility]
  del sm.utilities._subscribers[0][IUtility]

  #also for named utility
  util = sm.queryUtility(INamedUtility, name='utility-name')
  sm.unregisterUtility(util, INamedUtility, name='utility-name')
  del util
  del sm.utilities._subscribers[0][INamedUtility]

Now you need to commit your changes to the ZODB.

.. code-block:: console

  import transaction
  transaction.commit()
  app._p_jar.sync()


An Example
----------

I found myself in this situation with the Singing and Dancing product so I'll just go through the code here to fix both a normal utility and named utility found in it.

.. code-block:: console

  from collective.singing.interfaces import ISalt
  from collective.singing.async import IQueue
  import transaction

  portal = app.Plone
  sm = portal.getSiteManager()

  util_obj = sm.getUtility(ISalt)
  sm.unregisterUtility(provided=ISalt)
  del util_obj
  sm.utilities.unsubscribe((), ISalt)
  del sm.utilities.__dict__['_provided'][ISalt]
  del sm.utilities._subscribers[0][ISalt]

  util = sm.queryUtility(IQueue, name='collective.dancing.jobs')
  sm.unregisterUtility(util, IQueue, name='collective.dancing.jobs')
  del util
  del sm.utilities._subscribers[0][IQueue]
  Handling subscribers, adapters and utilities
  sm = app.myportal.getSiteManager()
  adapters = sm.utilities._adapters
  for x in adapters[0].keys():
      if x.__module__.find("collective.myproduct") != -1:
        print "deleting %s" % x
        del adapters[0][x]
  sm.utilities._adapters = adapters

  subscribers = sm.utilities._subscribers
  for x in subscribers[0].keys():
      if x.__module__.find("collective.myproduct") != -1:
        print "deleting %s" % x
        del subscribers[0][x]
  sm.utilities._subscribers = subscribers

  provided = sm.utilities._provided
  for x in provided.keys():
      if x.__module__.find("collective.myproduct") != -1:
        print "deleting %s" % x
        del provided[x]
  sm.utilities._provided = provided

  from transaction import commit
  commit()
  app._p_jar.sync()

Removing portal tools
---------------------

If you still have problems (re)installing products after you removed the broken local persistent components, you probably have to clean the Portal setup tool.You probably see something like this in the error log :

.. code-block:: console

    setup_tool = app.myportal.portal_setup
    toolset = setup_tool.getToolsetRegistry()
    if 'portal_myproduct' in toolset._required.keys():
        del toolset._required['portal_myproduct']
        setup_tool._toolset_registry = toolset

    from transaction import commit
    commit()
    app._p_jar.sync()



References
----------

I didn't by any means figure this all our on my own so please do not give me credit for it. Actually, most of this is shamelessly stolen. Thanks for the original fixers of the problem! Here are my references:

- http://blog.fourdigits.nl/removing-a-persistent-local-utility
- http://blog.fourdigits.nl/removing-a-persistent-local-utility-part-ii

