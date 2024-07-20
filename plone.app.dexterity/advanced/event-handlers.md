---
myst:
  html_meta:
    "description": "How to add custom event handlers for your content types"
    "property=og:description": "How to add custom event handlers for your content types"
    "property=og:title": "How to add custom event handlers for your content types"
    "keywords": "Plone, content types, event handlers"
---

# Event handlers

This chapter describes how to add custom event handlers for your type.

Zope (and so Plone) has a powerful event notification and subscriber subsystem.
Events notifications are already fired at several places.

With custom subscribers to these events, more dynamic functionality can be added.
It is possible to react when something happens to objects of a specific type.

Zope's event model is *synchronous*.
When an event is broadcast (via the `notify()` function from the [`zope.event`](https://pypi.org/project/zope.event/) package), all registered event handlers will be called.
This happens, for example, from the `save` action of an add form, or on move or delete of content objects.
There is no guarantee in which order the event handlers will be called.

Each event is described by an interface, and will typically carry some information about the event.
Some events are known as *object events*, and provide `zope.component.interfaces.IObjectEvent`.
These have an `object` attribute giving access to the content object that the event relates to.
Object events allow event handlers to be registered for a specific type of object as well as a specific type of event.

Some of the most commonly used event types in Plone are shown below.
They are all object events.

`zope.lifecycleevent.interfaces.IObjectCreatedEvent`
:   Fired by the standard add form just after an object has been created, but before it has been added on the container.
    Note that it is often easier to write a handler for `IObjectAddedEvent` (see below), because at this point the object has a proper acquisition context.

`zope.lifecycleevent.interfaces.IObjectAddedEvent`
:   Fired when an object has been added to its container.
    The container is available as the `newParent` attribute.
    The name the new item holds in the container is available as `newName`.

`OFS.interfaces.IObjectWillBeAddedEvent`
:   Fired before an object is added to its container.
    It is also fired on move of an object (copy/paste).

`zope.lifecycleevent.interfaces.IObjectModifiedEvent`
:   Fired by the standard edit form when an object has been modified.

`zope.lifecycleevent.interfaces.IObjectRemovedEvent`
:   Fired when an object has been removed from its container.
    The container is available as the `oldParent` attribute.
    The name the item held in the container is available as `oldName`.

`OFS.interfaces.IObjectWillBeRemovedEvent`
:   Fired before an object is removed.
    Until here, no deletion has happend.
    It is also fired on move of an object (copy/paste).

`zope.lifecycleevent.interfaces.IObjectMovedEvent`
:   Fired when an object is added to, removed from, renamed in, or moved between containers.
    This event is a super-type of `IObjectAddedEvent` and `IObjectRemovedEvent`, shown above.
    An event handler registered for this interface will be invoked for the "added" and "removed" cases as well.
    When an object is moved or renamed, all of `oldParent`, `newParent`, `oldName`, and `newName` will be set.

`Products.CMFCore.interfaces.IActionSucceededEvent`
:   Fired when a workflow event has completed.
    The `workflow` attribute holds the workflow instance involved, and the `action` attribute holds the action (transition) invoked.

Event handlers can be registered using ZCML with the `<subscriber />` directive.

As an example, let's add an event handler to the `Presenter` type.
It tries to find users with matching names matching the presenter ID, and sends these users an email.

First, we require an additional import at the top of {file}`presenter.py`.

```python
from plone import api
```

Then we'll add the following event subscriber after the schema definition.

```python
def notifyUser(presenter, event):
    acl_users = api.portal.get_tool("acl_users")
    sender = api.portal.get_registry_record("plone.email_from_name")

    if not sender:
        return

    subject = "Is this you?"
    message = "A presenter called {0} was added here {1}".format(
        presenter.title,
        presenter.absolute_url()
    )

    matching_users = acl_users.searchUsers(fullname=presenter.title)
    for user_info in matching_users:
        email = user_info.get("email", None)
        if email is not None:
            api.portal.send_email(
                recipient=email,
                sender=sender,
                subject=subject
                body=message,
            )
```

And register it in ZCML.

-   The first argument to `for` is an interface describing the object type.
-   The second argument is the event type.
-   The arguments to the function reflects these two, so the first argument is the `IPresenter` instance, and the second is an `IObjectAddedEvent` instance.

```xml
<subscriber
  for=".presenter.IPresenter
       zope.lifecycleevent.interfaces.IObjectAddedEvent"
  handler=".presenter.notifyUser"
/>
```

There are many ways to improve this rather simplistic event handler, but it illustrates how events can be used.
