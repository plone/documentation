==================
Zope's many hooks
==================

.. admonition:: Description

    What hooks does Zope provide for application code?

Zope provides many different hooks that can be used to execute code at various
times during its lifecycle. The most important ones are outlined below.

.. contents :: :local:

Process lifecycle
=================

``zope.processlifetime`` defines three events:

``IDatabaseOpened``
  notified when the main ZODB has been opened, but before the root
  application object is set.
``IDatabaseOpenedWithRoot``
  notified later in the startup cycle, when the application root has been
  set and initalised.
``IProcessStarting``
  notified when the Zope startup process has completed, but before the Zope
  server runs (and so can listen to requests).

ZODB connection lifecycle
=========================

Functions that should be called just after traversal over the
``ZApplicationWrapper`` as it opens a ZODB connection for the request should
be added to the ``App.ZApplication.connection_open_hooks`` list. They are
called with a ZODB connection as their sole argument.

The ZODB transaction provides two methods to register hooks |---|
``addBeforeCommitHook()`` and ``addAfterCommitHook()``. These can be passed
functions and a (static) set of arguments and will be called just before, and
just after, a transaction is committed. The hook function must take at least one
argument, a boolean indicating whether the transaction succeeded.

Use ``transaction.get()`` to get hold of the transaction object. See
``transaction.interfaces.ITransaction`` for more details.

Request lifecycle
=================

Request-scoped items may be protected from garbage collection using
``request._hold()``. If applicable, the item held can implement ``__del__()``,
which will be called when the request is destroyed.

The event ``zope.publisher.events.EndRequestEvent`` is triggered at the end
of an event, just before any held items are cleared.

Publication
===========

The publisher notifies a number of events, which can be used to hook into
various stages of the publication process. These are all defined in the module
``ZPublisher.pubevents``.

When an exception is raised, a view registered for the exception type as
context (and a generic request) named ``index.html`` will be rendered as an
error message, if it exists.

Traversal
=========

If an object has a method ``__bobo_traverse__(self, request, name)``, this will
be used during traversal in lieu of attribute or item access. It is expected to
return the next item to traverse to given the path segment ``name``. A more
modern approach is to register an adapter to ``IPublishTraverse`` although this
only applies to publication (URL) traversal, not path traversal.

The method ``__before_publishing_traverse__(self, object, request)`` can be
implemented to be notified when traversal first finds an object. Implemented on
a class, the ``self`` and ``object`` parameters will be the same.

See also the ``SiteAccess`` package, which implements a through-the-web
manageable, generic multi-hook to let any callable be invoked before access
through an "AccessRule".

The event ``zope.traversing.interfaces.IBeforeTraverseEvent`` is notified when
traversing over something that is a local component site, e.g. the Plone site
root.

The ``__browser_default__`` method can be implemented to specify a "default
page" (akin to an ``index.html`` in a folder). A more modern way to do this is
to register an adapter to ``IBrowserPublisher``.

An adapter to ``ITraversable`` can be used to implement namespace traversal
(``.../++<namespace>++name/...``). See above for further details.

.. |---| unicode:: U+02014 .. em dash
