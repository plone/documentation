Events
========

**Registering event handlers and sending events**

Zope provides an events system. Various components (e.g the standard add
and edit forms) *notify* any number of *event subscribers* (also known
as *event handlers*) of a particular event. The subscribers are then
executed.

Note that:

-  Event subscribers are executed in arbitrary order
-  Events are executed *synchronously*: The code which notifies of the
   event will block until all event handlers have returned


Each type of event is described by an interface. The implementation of
this interface will typically carry some information about the event,
which may be useful to event subscribers.

Some events are known as **object events**. These have an *object*
attribute, giving access to the (content) object that the event relates
to. Object events allow event handlers to be registered for a specific
type of object as well as a specific type of event.

Some of the most commonly used event types in Plone are shown below.
They are all object events (i.e. they derive from
*zope.component.interfaces.IObjectEvent)*.

-  *zope.lifecycleevent.interfaces.IObjectCreatedEvent*, fired by the
   standard add form just after an object has been created, but before
   it has been added on the container. Note that it is often easier to
   write a handler for *IObjectAddedEvent* (see below), because at this
   point the object has a proper acquisition context. This makes it
   possible to look up tools using *getToolByName()*, for example.
-  *zope.lifecycleevent.interfaces.IObjectModifiedEvent*, fired by the
   standard edit form when an object has been modified
-  *zope.lifecycleevent.interfaces.IObjectAddedEvent*, fired when an
   object has been added to its container. The container is available as
   the *newParent* attribute, and the name the new item holds in the
   container is available as *newName*.
-  *zope.lifecycleevent.interfaces.IObjectRemovedEvent*, fired when an
   object has been removed from its container. The container is
   available as the *oldParent* attribute, and the name the item held in
   the container is available as *oldName*.
-  *zope.lifecycleevent.interfaces.IObjectMovedEvent*, fired when an
   object is added to, removed from, renamed in, or moved between
   containers. This event is a super-type of *IObjectAddedEvent*
   and*IObjectRemovedEvent*, shown above, so an event handler registered
   for this interface will be invoked for the ‘added’ and ‘removed’
   cases as well. When an object is moved or renamed, all of
   *oldParent*, *newParent*, *oldName* and *newName* will be set.
-  *Products.CMFCore.interfaces.IActionSucceededEvent*, fired when a
   workflow event has completed. The *workflow* attribute holds the
   workflow instance involved, and the *action* attribute holds the
   action (transition) invoked.

Of course, you can create your own event types as well. However, for
standard CRUD type operations (create, read, update, delete), it is best
to use the standard event types with a custom object type rather than
creating an object-specific event type.

Registering an event subscriber
-------------------------------

Event subscribers can be registered using the *subscribe()* decorator.
This takes at least one argument: the type (interface) of event to
subscribe to. For object events, it can take two parameters: the type of
object, and the type of event. This allows us to limit an event handler
to a particular type of context object.

Here is an example, printing a message every time a CMF content object
is added to a folder:

::

    from five import grok

    from zope.lifecycleevent.interfaces import IObjectAddedEvent
    from Products.CMFCore.interfaces import IContentish

    @grok.subscribe(IContentish, IObjectAddedEvent)
    def printMessage(obj, event):
        print "Received event for", obj, "added to", event.newParent

Provided the module is grokked, this is all we have to do to register a
new event subscriber. Although this example is trivial, there is no
limit to what you can do within an event handler.

Notes:

-  The two arguments to the function correspond to the two arguments to
   the *subscribe()* decorator. For object events, the first is the
   object that the event relates to (which will be the same as
   *event.object* in most cases). The second is the event instance.
-  Obviously, we could use a more specific content type interface if we
   wanted to be more specific.
-  Unlike adapters, you cannot override an event subscriber by using a
   more specific interface. Each and every applicable event subscriber
   will be executed when an event is fired.

Creating a custom event type
----------------------------

Creating a new type of event is not much more difficult. Here is an
example that involves the sample message broadcasting service we saw in
the previous sections:

First, we define an object event type. This would typically be in an
*interfaces.py* module:

::

    from zope.component.interfaces import IObjectEvent
    from zope import schema

    class IMessageSentEvent(IObjectEvent)

        message = schema.Object(title=u"Message", schema=IMessage)
        messageCount = schema.Int(title=u"Number of messages so far")

The event implementation itself is simple too. The *object* attribute is
mandated by the *IObjectEvent* interface.

::

    from five import grok
    from zope.component.interfaces import ObjectEvent

    class MessageSentEvent(ObjectEvent):
        grok.implements(IMessageSentEvent)

        def __init__(self, object, message, messageCount):
            self.object = object
            self.message = message
            self.messageCount = messageCount

Here is another implementation of the messaging service, this time
broadcasting an event:

::

    from five import grok
    from zope.annotation.interfaces import IAnnotations
    from zope.event import notify

    class BloggingBroadcaster(grok.MultiAdapter):
        grok.provides(IMessageBroadcaster)
        grok.adapts(IContent, IBloggingService)

        COUNTER_KEY = 'example.messaging.counter'

        def __init__(self, context, service):
            self.context = context
            self.service = service

        def send(self):
            message = IMessage(self.context)
            text = message.format()

            annotations = IAnnotations(self.context, None)
            messageCount = -1
            if annotations is not None:
                messageCount = annotations.get(COUNTER_KEY, 0)
                messageCount += 1
                annotations[COUNTER_KEY] = messageCount
                print "This is message number", messageCount

            notify(MessageSentEvent(self.context, message, messageCount))

            print text

Notes:

-  We use the *notify()* function from the *zope.event* package to
   broadcast the event.
-  The call to *notify()* will not return until every event subscriber
   has been executed.

As before, we could now register an event subscriber for this event.
Since it is an object event, we can use the two-argument version of the
*subscribe* decorator as shown above. However, we could also have a more
general event handler that executes for any type of object. Here is one
that simply logs that a message has been sent:

::

    from five import grok
    import logging

    auditLog = logging.getLogger('auditlog')

    @grok.subscriber(IMessageSentEvent)
    def log(event):
        auditLog.info("Message number %s sent for %s" % (event.messageCount, event.object,))
