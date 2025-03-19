---
myst:
  html_meta:
    "description": "How to add custom event handlers for your type in Plone"
    "property=og:description": "How to add custom event handlers for your type in Plone"
    "property=og:title": "Subscribers (event handlers)"
    "keywords": "Plone, subscribers, event handlers"
---

(backend-subscribers-label)=

# Subscribers (event handlers)

A _subscriber_ is a callable object that takes one argument, an object that we call the _event_.

_Events_ are objects that represent something happening in a system.
They are used to extend processing by providing processing plug points.

A _notification_ alerts subscribers that an event has occurred.

The {term}`Zope Component Architecture`'s [`zope.event`](https://zopeevent.readthedocs.io/en/latest/) package is used to manage subscribable events in Plone.

The Plone event system has some notable characteristics:

-   It's simple.
-   The calling order of subscribers is random.
    You can't set the order in which event handlers are called.
-   Events can't be cancelled.
    All handlers will always get the event.
-   Event handlers can't have return values.
-   Exceptions raised in an event handler will interrupt the request processing.


## Register an event handler

Plone events can be scoped:

-   globally (no scope)
-   per content type
-   per behavior or marker interface


### Register an event handler on content type creation

The following example demonstrates how to register an event handler when a content type is created.

In your {file}`.product/your/product/configure.zcml` insert the following code.

{lineno-start=1}
```xml
<subscriber
    for=".interfaces.IMyContentTypeClass
         zope.lifecycleevent.IObjectCreatedEvent"
    handler=".your_python_file.your_method"
    />
```

The second line defines to which interface you want to bind the execution of your code. 
Here, the event handler code will only be executed if the object is a content type providing the interface `.interfaces.IMyContentTypeClass`.
If you want this to be interface agnostic, insert an asterix `*` as a wildcard instead.

The third line defines the event on which this should happen, which is `IObjectCreatedEvent`. 
For more available possible events to use as a trigger, see {ref}`subscribers-event-handlers`. 

The fourth line gives the path to the callable function to be executed.

Create your {file}`.product/your/product/your_python_file.py` and insert the following code.

```python
def your_subscriber(object, event):
    # do something with your created content type
```


### Subscribe to an event using ZCML

Subscribe to a global event using {term}`ZCML` by inserting the following code in your {file}`.product/your/product/configure.zcml`.

```xml
<subscriber
    for="Products.PlonePAS.events.UserLoggedOutEvent"
    handler=".smartcard.clear_extra_cookies_on_logout"
    />
```

For this event, the Python code in {file}`smartcard.py` would be the following.

```python
def clear_extra_cookies_on_logout(event):
    # What event contains depends on the
    # triggerer of the event and event class
    request = event.object.REQUEST
```

The following example for a custom event subscribes content types to all `IMyEvents` when fired by `IMyObject`.

```xml
<subscriber
    for=".interfaces.IMyObject
         .interfaces.IMyEvent"
    handler=".content.MyObject.myEventHandler"
    />
```

The following example shows how to subscribe a content type to the life cycle event.

```xml
<subscriber
    zcml:condition="installed zope.lifecycleevent"
    for=".interfaces.ISitsPatient
         zope.lifecycleevent.IObjectModifiedEvent"
    handler=".content.SitsPatient.objectModified"
    />
```


## Fire an event

Use `zope.event.notify()` to fire event objects to their subscribers.

The following code shows how to fire an event in unit tests.

```python
import zope.event
from plone.postpublicationhook.event import AfterPublicationEvent

event = AfterPublicationEvent(self.portal, self.portal.REQUEST)
zope.event.notify(event)
```


(subscribers-event-types-label)=

## Event types

Plone has the following types of events.


### Creation events

`zope.lifecycleevent.IObjectCreatedEvent` is fired for all Zope-ish objects when they are created, or copied via `IObjectCopiedEvent`.
They don't have to be content objects.

### Modified events

`zope.lifecycleevent.IObjectModifiedEvent` is called for creation stage events as well, unlike the previous event type.

### Delete events

Delete events can be fired several times for the same object.
Some delete event transactions are rolled back.

### Copy events

`zope.lifecycleevent.IObjectCopiedEvent` is triggered when an object is copied.
It will also fire `IObjectCreatedEvent` event code.

### Workflow events

`Products.DCWorkflow.interfaces.IBeforeTransitionEvent` is triggered before a workflow transition is executed.

`Products.DCWorkflow.interfaces.IAfterTransitionEvent` is triggered after a workflow transition has been executed.

The DCWorkflow events are low-level events that can tell you a lot about the previous and current states.

`Products.CMFCore.interfaces.IActionSucceededEvent` is a higher level event that is more commonly used to react after a workflow action has completed.

### Zope startup events

`zope.processlifetime.IProcessStarting` is triggered after the component registry has been loaded and Zope is starting up.

`zope.processlifetime.IDatabaseOpened` is triggered after the main ZODB database has been opened.
