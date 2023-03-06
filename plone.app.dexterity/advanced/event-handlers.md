---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Event handlers

**Adding custom event handlers for your type**

Zope (and so Plone) has a powerful event notification and subscriber subsystem.
Events notifications are already fired at several places.

With custom subscribers to these events more dynamic functionality can be added.
It is possible to react when something happens to objects of a specific type.

Zope’s event model is *synchronous*.
When an event is broadcast (via the `notify()` function from the [zope.event] package) all registered event handlers will be called.
This happens for example from the `save` action of an add form, on move or delete of content-objects.
There is no guarantee of which order the event handlers will be called in, however.

Each event is described by an interface, and will typically carry some information about the event.
Some events are known as *object events*, and provide `zope.component.interfaces.IObjectEvent`.
These have an `object` attribute giving access to the (content) object that the event relates to.
Object events allow event handlers to be registered for a specific type of object as well as a specific type of event.

Some of the most commonly used event types in Plone are shown below.
They are all object events.

`zope.lifecycleevent.interfaces.IObjectCreatedEvent`

: fired by the standard add form just after an object has been created, but before it has been added on the container.
  Note that it is often easier to write a handler for `IObjectAddedEvent` (see below), because at this point the object has a proper acquisition context.

`zope.lifecycleevent.interfaces.IObjectAddedEvent`

: fired when an object has been added to its container.
  The container is available as the `newParent` attribute.
  The name the new item holds in the container is available as `newName`.

`OFS.interfaces.IObjectWillBeAddedEvent`

: fired before an object is added to its container.
  It is also fired on move of an object (copy/paste).

`zope.lifecycleevent.interfaces.IObjectModifiedEvent`

: fired by the standard edit form when an object has been modified.

`zope.lifecycleevent.interfaces.IObjectRemovedEvent`

: fired when an object has been removed from its container.
  The container is available as the `oldParent` attribute.
  The name the item held in the container is available as `oldName`.

`OFS.interfaces.IObjectWillBeRemovedEvent`

: fired before an object is removed. Until here no deletion has happend.
  It is also fired on move of an object (copy/paste).

`zope.lifecycleevent.interfaces.IObjectMovedEvent`

: fired when an object is added to, removed from, renamed in, or moved between containers.
  This event is a super-type of `IObjectAddedEvent` and `IObjectRemovedEvent`, shown above.
  An event handler registered for this interface will be invoked for the ‘added’ and ‘removed’ cases as well.
  When an object is moved or renamed, all of `oldParent`, `newParent`, `oldName` and `newName` will be set.

`Products.CMFCore.interfaces.IActionSucceededEvent`

: fired when a workflow event has completed.
  The `workflow` attribute holds the workflow instance involved, and the `action` attribute holds the action (transition) invoked.

Event handlers can be registered using ZCML with the `<subscriber />` directive.

As an example, let’s add an event handler to the `Presenter` type.
It tries to find users with matching names matching the presenter id, and send these users an email.

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

[zope.event]: http://pypi.python.org/pypi/zope.event
