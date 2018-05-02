======
Events
======

.. admonition:: Description

        How to add event hooks to your Plone code to perform actions when
        something happens on a Plone site.


Introduction
============

This document briefly discusses event handling using the ``zope.event`` module.
The Zope Component Architecture's
`zope.event package <https://pypi.python.org/pypi/zope.event>`_ is
used to manage subscribeable events in Plone.

Some of the notable characteristics of the Plone event system are:

* it is simple;
* subscriber calling order is not modifiable |---| you cannot set the order
  in which event handlers are called;
* events cannot be cancelled |---| all handlers will always get the event;
* event handlers cannot have return values;
* exceptions raised in an event handler will interrupt the request
  processing.

Registering an event handler
============================

Plone events can be scoped:

* *globally* (no scope)
* per *content type*


Example: Register an event-handler on your contenttype's creation
-----------------------------------------------------------------


In your.product/your/product/configure.zcml insert::

    <subscriber
        for=".interfaces.IMyContentTypeClass
             zope.lifecycleevent.IObjectCreatedEvent"
        handler=".your_python_file.your_method"
        />


The first line defines to which interface you want to bind the execution of your code, which means here,
that the code will only be executed if the object is one of your contenttype's.
If you want this to be interface-agnostic, insert an asterix as a wildcard instead.

The second line defines the event on which this should happen, which is here 'IObjectCreatedEvent' -- for Archetypes you should use 'Products.Archetypes.interfaces.IObjectInitializedEvent' instead.
For more available possible events to be used as a trigger, see :doc:`event handler documentation </external/plone.app.dexterity/docs/advanced/event-handlers>`

The third line gives the path to the script that is supposed to be executed.

Create your.product/your/product/your_python_file.py and insert::

    def your_method(object, event):

        # do sth with your created contenttype

For Dexterity-contenttype's and additional ZOPE-Illumination see also:
 :doc:`event handler documentation </external/plone.app.dexterity/docs/advanced/event-handlers>`


Subscribing using ZCML
----------------------

Subscribing to a global event using :term:`ZCML`.

.. code-block:: xml

    <subscriber
        for="Products.PlonePAS.events.UserLoggedOutEvent"
        handler=".smartcard.clear_extra_cookies_on_logout"
        />

For this event, the Python code in ``smartcard.py`` would be::

        def clear_extra_cookies_on_logout(event):
            # What event contains depends on the
            # triggerer of the event and event class
            request = event.object.REQUEST
            ...

Custom event example subscribing to all ``IMyEvents`` when fired by
``IMyObject``::

    <subscriber
        for=".interfaces.IMyObject
             .interfaces.IMyEvent"
        handler=".content.MyObject.myEventHandler"
        />

Life cycle events example::

    <subscriber
        zcml:condition="installed zope.lifecycleevent"
        for=".interfaces.ISitsPatient
             zope.lifecycleevent.IObjectModifiedEvent"
        handler=".content.SitsPatient.objectModified"
        />


Subscribing using Python
-------------------------

The following subscription is valid through the process life cycle. In unit
tests, it is important to clear test event handlers between the test steps.

.. XXX: What does "through the process life cycle" mean?

Example::

    import zope.component

    def my_event_handler(context, event):
        """
        @param context: Zope object for which the event was fired. Usually this is a Plone content object.

        @param event: Subclass of event.
        """
        pass

    gsm = zope.component.getGlobalSiteManager()
    gsm.registerHandler(my_event_handler, (IMyObject,IMyEvent))


Firing an event
===============

Use ``zope.event.notify()`` to fire event objects to their subscribers.

Example of how to fire an event in unit tests::

    import zope.event
    from plone.postpublicationhook.event import AfterPublicationEvent

    event = AfterPublicationEvent(self.portal, self.portal.REQUEST)
    zope.event.notify(event)


Event types
===========

*Creation* events
------------------

``Products.Archetypes.interfaces.IObjectInitializedEvent``
    is fired for an Archetypes-based object when it's being initialised;
    i.e.  when it's being populated for the first time.

``Products.Archetypes.interfaces.IWebDAVObjectInitializedEvent``
    is fired for an Archetypes-based object when it's being initialised via
    WebDAV.

``zope.lifecycleevent.IObjectCreatedEvent``
    is fired for all Zopeish objects when they are being created (they don't
    necessarily need to be content objects) or being copied (IObjectCopiedEvent).

.. warning::

   Archetypes and Zope 3 events might not be compatible with each other.
   Please see links below.

Other resources:

* https://plone.org/documentation/manual/developer-manual/archetypes/other-useful-archetypes-features/how-to-use-events-to-hook-the-archetypes-creation-process

* http://n2.nabble.com/IObjectInitializedEvent-tp4784897p4784897.html


*Modified* events
------------------

Two different content event types are available and might work differently
depending on your scenario:

``Products.Archetypes.interfaces.IObjectEditedEvent``
    called for Archetypes-based objects that are not in the creation stage
    any more.

.. note::

    ``Products.Archetypes.interfaces.IObjectEditedEvent`` is fired after
    ``reindexObject()`` is called. If you manipulate your content object in a
    handler for this event, you need to manually reindex new values, or the
    changes will not be reflected in the ``portal_catalog``.

``zope.lifecycleevent.IObjectModifiedEvent``
    called for creation-stage events as well, unlike the previous event type.

``Products.Archetypes.interfaces.IWebDAVObjectEditedEvent``
    called for Archetypes-based objects when they are being edited via WebDAV.

``Products.Archetypes.interfaces.IEditBegunEvent``
    called for Archetypes-based objects when an edit operation is begun.

``Products.Archetypes.interfaces.IEditCancelledEvent``
    called for Archetypes-based objects when an edit operation is canceled.


*Delete* events
----------------

Delete events can be fired several times for the same object.
Some delete event transactions are rolled back.

* Read more about Delete events in `this discussion <http://plone.293351.n2.nabble.com/Event-on-object-deletion-td3670562.html>`_.

*Copy* events
--------------

``zope.lifecycleevent.IObjectCopiedEvent``
    is triggered when an object is copied (will also fire IObjectCreatedEvent event code).

*Workflow* events
-----------------

``Products.DCWorkflow.interfaces.IBeforeTransitionEvent``
    is triggered before a workflow transition is executed.

``Products.DCWorkflow.interfaces.IAfterTransitionEvent``
    is triggered after a workflow transition has been executed.

The DCWorkflow events are low-level events that can tell you a lot about the
previous and current states.

``Products.CMFCore.interfaces.IActionSucceededEvent``
    this is a higher level event that is more commonly used to react after a
    workflow action has completed.


*Zope startup* events
----------------------

``zope.processlifetime.IProcessStarting``
    is triggered after component registry has been loaded and Zope is
    starting up.

``zope.processlifetime.IDatabaseOpened``
    is triggered after the main ZODB database has been opened.


Asynchronous event handling
================================

* http://stackoverflow.com/questions/15875088/running-plone-subscriber-events-asynchronously

See also
========

* https://pypi.python.org/pypi/zope.event/3.4.1

* http://apidoc.zope.org/++apidoc++/ZCML/http_co__sl__sl_namespaces.zope.org_sl_zope/subscriber/index.html

* ``zope.component.registry``

.. |---| unicode:: U+02014 .. em dash
