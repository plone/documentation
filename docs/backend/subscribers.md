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

The Zope Component Architecture’s zope.event package is used to manage subscribeable events in Plone.

Some of the notable characteristics of the Plone event system are:

- It is simple;
- Subscriber calling order is random — you cannot set the order in which event handlers are called;
- Events cannot be cancelled — all handlers will always get the event;
- Event handlers cannot have return values;
- Exceptions raised in an event handler will interrupt the request processing.

## Registering an event handler

Plone events can be scoped:

- Globally (no scope)
- Per content type
- per behavior/ marker interface

### Example: Register an event-handler on your content type’s creation

In your `.product/your/product/configure.zcml` insert:
```xml
<subscriber
    for=".interfaces.IMyContentTypeClass
         zope.lifecycleevent.IObjectCreatedEvent"
    handler=".your_python_file.your_method"
    />
```
The second line defines to which interface you want to bind the execution of your code. 
Here, the event handler code will only be executed if the object is a content-type providing the interface `.interfaces.IMyContentTypeClass`. 
If you want this to be interface-agnostic, insert an asterix `*` as a wildcard instead.

The third line defines the event on which this should happen, which is here ‘IObjectCreatedEvent’. 
For more available possible events to be used as a trigger, see {ref}`event-handlers` 

The fourth line gives the path to the callable (function) that is supposed to be executed.

Create your `.product/your/product/your_python_file.py` and insert:
```python
def your_subscriber(object, event):
    ...
    # do sth with your created contenttype
```

### Subscribing using ZCML

Subscribing to a global event using {term}`ZCML`.
```xml
<subscriber
    for="Products.PlonePAS.events.UserLoggedOutEvent"
    handler=".smartcard.clear_extra_cookies_on_logout"
    />
```
For this event, the Python code in `smartcard.py` would be:
```python
def clear_extra_cookies_on_logout(event):
    # What event contains depends on the
    # triggerer of the event and event class
    request = event.object.REQUEST
    ...
```
Custom event example subscribing to all `IMyEvents` when fired by `IMyObject`:
```xml
<subscriber
    for=".interfaces.IMyObject
         .interfaces.IMyEvent"
    handler=".content.MyObject.myEventHandler"
    />
```
Life cycle events example:
```xml
<subscriber
    zcml:condition="installed zope.lifecycleevent"
    for=".interfaces.ISitsPatient
         zope.lifecycleevent.IObjectModifiedEvent"
    handler=".content.SitsPatient.objectModified"
    />
```

### Subscribing using Python

The following subscription is valid through the process life cycle. In unit tests, it is important to clear test event handlers between the test steps.

Example:
```python
import zope.component

def my_event_handler(context, event):
    """
    @param context: Zope object for which the event was fired. Usually this is a Plone content object.

    @param event: Subclass of event.
    """
    pass

gsm = zope.component.getGlobalSiteManager()
gsm.registerHandler(my_event_handler, (IMyObject,IMyEvent))
```

## Firing an event

Use `zope.event.notify()` to fire event objects to their subscribers.

Example of how to fire an event in unit tests:
```python
import zope.event
from plone.postpublicationhook.event import AfterPublicationEvent

event = AfterPublicationEvent(self.portal, self.portal.REQUEST)
zope.event.notify(event)
```

## Event types

### Creation events

`zope.lifecycleevent.IObjectCreatedEvent` is fired for all Zopeish objects when they are being created (they don’t necessarily need to be content objects) or being copied (IObjectCopiedEvent).

### Modified events

`zope.lifecycleevent.IObjectModifiedEvent`
called for creation-stage events as well, unlike the previous event type.

### Delete events

Delete events can be fired several times for the same object. Some delete event transactions are rolled back.

### Copy events

`zope.lifecycleevent.IObjectCopiedEvent` is triggered when an object is copied (will also fire IObjectCreatedEvent event code).

### Workflow events

`Products.DCWorkflow.interfaces.IBeforeTransitionEvent` is triggered before a workflow transition is executed.

`Products.DCWorkflow.interfaces.IAfterTransitionEvent` is triggered after a workflow transition has been executed.

The DCWorkflow events are low-level events that can tell you a lot about the previous and current states.

`Products.CMFCore.interfaces.IActionSucceededEvent` this is a higher level event that is more commonly used to react after a workflow action has completed.

### Zope startup events

`zope.processlifetime.IProcessStarting` is triggered after component registry has been loaded and Zope is starting up.

`zope.processlifetime.IDatabaseOpened` is triggered after the main ZODB database has been opened.

(event-handlers)=

## Event Handlers

*Adding custom event handlers for your type*

Zope (and so Plone) has a powerful event notification and subscriber subsystem. Events notifications are already fired at several places.

With custom subscribers to these events more dynamic functionality can be added. It is possible to react when something happens to objects of a specific type.

Zope’s event model is synchronous. When an event is broadcast (via the `notify()` function from the zope.event package) all registered event handlers will be called. This happens for example from the `save` action of an add form, on move or delete of content-objects. There is no guarantee of which order the event handlers will be called in, however.

Each event is described by an interface, and will typically carry some information about the event. Some events are known as object events, and provide `zope.component.interfaces.IObjectEvent`. These have an `object` attribute giving access to the (content) object that the event relates to. Object events allow event handlers to be registered for a specific type of object as well as a specific type of event.

Some of the most commonly used event types in Plone are shown below. They are all object events.

`zope.lifecycleevent.interfaces.IObjectCreatedEvent` fired by the standard add form just after an object has been created, but before it has been added on the container. Note that it is often easier to write a handler for IObjectAddedEvent (see below), because at this point the object has a proper acquisition context.

`zope.lifecycleevent.interfaces.IObjectAddedEvent` fired when an object has been added to its container. The container is available as the newParent attribute. The name the new item holds in the container is available as newName.

`OFS.interfaces.IObjectWillBeAddedEvent` fired before an object is added to its container. It is also fired on move of an object (copy/paste).

`zope.lifecycleevent.interfaces.IObjectModifiedEvent` fired by the standard edit form when an object has been modified.

`zope.lifecycleevent.interfaces.IObjectRemovedEvent` fired when an object has been removed from its container. The container is available as the oldParent attribute. The name the item held in the container is available as oldName.

`OFS.interfaces.IObjectWillBeRemovedEvent` fired before an object is removed. Until here no deletion has happend. It is also fired on move of an object (copy/paste).

`zope.lifecycleevent.interfaces.IObjectMovedEvent` fired when an object is added to, removed from, renamed in, or moved between containers. This event is a super-type of IObjectAddedEvent and IObjectRemovedEvent, shown above. An event handler registered for this interface will be invoked for the ‘added’ and ‘removed’ cases as well. When an object is moved or renamed, all of oldParent, newParent, oldName and newName will be set.

`Products.CMFCore.interfaces.IActionSucceededEvent` fired when a workflow event has completed. The `workflow` attribute holds the workflow instance involved, and the `action` attribute holds the action (transition) invoked.

Event handlers can be registered using ZCML with the `<subscriber />` directive.

As an example, let’s add an event handler to the `Presenter` type. It tries to find users with matching names matching the presenter id, and send these users an email.

First, we require an additional import at the top of `presenter.py`:
```python
from plone import api
```

Then, we’ll add the following event subscriber after the schema definition:
```python
def notifyUser(presenter, event):
    acl_users = api.portal.get_tool('acl_users')
    sender = api.portal.get_registry_record('plone.email_from_name')

    if not sender:
        return

    subject = 'Is this you?'
    message = 'A presenter called {0} was added here {1}'.format(
        presenter.title,
        presenter.absolute_url()
    )

    matching_users = acl_users.searchUsers(fullname=presenter.title)
    for user_info in matching_users:
        email = user_info.get('email', None)
        if email is not None:
            api.portal.send_email(
                recipient=email,
                sender=sender,
                subject=subject
                body=message,
            )
```

And register it in ZCML:

- First argument to `for` is an interface describing the object type.
- Second argument is the event type.
- The arguments to the function reflects these two, so the first argument is the `IPresenter` instance and the second is an `IObjectAddedEvent` instance.

```xml
<subscriber
  for=".presenter.IPresenter
       zope.lifecycleevent.interfaces.IObjectAddedEvent"
  handler=".presenter.notifyUser"
/>
```
There are many ways to improve this rather simplistic event handler, but it illustrates how events can be used.