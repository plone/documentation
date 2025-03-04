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

In Plone 6, the event system provides a robust mechanism for developers to execute custom actions in response to various occurrences within the system. This capability is facilitated through the use of event subscribers, also known as event handlers, which listen for specific events and perform predefined operations when those events are triggered.

## Overview of the Event System

Plone's event system is built upon the Zope Component Architecture's `zope.event` package, enabling a publish-subscribe pattern where events are broadcasted, and subscribers (event handlers) respond accordingly. Key characteristics of this system include:

- **Simplicity**: The event system is straightforward to implement and use.
- **Non-deterministic Handler Execution Order**: The order in which event handlers are invoked is not specified and cannot be controlled.
- **Non-cancelable Events**: Once an event is emitted, all associated handlers will receive it; events cannot be canceled.
- **No Return Values**: Event handlers do not return values.
- **Exception Handling**: Exceptions raised within an event handler can interrupt the request processing.

Events are typically defined by interfaces and may carry pertinent information about the event. Object events, which pertain to specific content objects, implement the `zope.component.interfaces.IObjectEvent` interface and include an `object` attribute referencing the related content object. This structure allows event handlers to be registered for specific object types and event types.

## Commonly Used Event Types

Several standard event types are frequently utilized in Plone:

- **`zope.lifecycleevent.interfaces.IObjectCreatedEvent`**: Triggered just after an object is created but before it is added to its container.
- **`zope.lifecycleevent.interfaces.IObjectAddedEvent`**: Occurs when an object has been added to its container.
- **`zope.lifecycleevent.interfaces.IObjectModifiedEvent`**: Fired when an object is modified.
- **`zope.lifecycleevent.interfaces.IObjectRemovedEvent`**: Triggered when an object is removed from its container.

These events are part of the `zope.lifecycleevent` package and are integral to Plone's event-handling infrastructure.

## Registering Event Handlers

Event handlers can be registered in two primary ways: using ZCML (Zope Configuration Markup Language) or Python decorators.

### Using ZCML

To register an event handler via ZCML, add a `<subscriber>` directive to your package's `configure.zcml` file:


```xml
<subscriber
    for=".interfaces.IMyContentTypeClass zope.lifecycleevent.IObjectCreatedEvent"
    handler=".your_module.your_function"
/>
```


In this configuration:

- The `for` attribute specifies the interface of the content type and the event interface.
- The `handler` attribute points to the function that will handle the event.

This setup ensures that `your_function` is called whenever an object implementing `IMyContentTypeClass` is created.

### Using Python Decorators

Alternatively, you can register an event handler using the `subscribe` decorator from the `zope.component` module:


```python
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from .interfaces import IMyContentTypeClass

@adapter(IMyContentTypeClass, IObjectCreatedEvent)
def your_function(obj, event):
    # Your code here
```


In this example, `your_function` will be invoked whenever an object implementing `IMyContentTypeClass` is created.

## Firing Events

To emit an event, use the `notify` function from the `zope.event` module:


```python
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

notify(ObjectModifiedEvent(your_object))
```


This call broadcasts an `ObjectModifiedEvent`, and all subscribers to this event will be notified.

## Considerations for Event Handlers

When implementing event handlers, keep the following considerations in mind:

- **Performance**: Since event handlers are executed synchronously, long-running operations can delay the request processing.
- **Error Handling**: Exceptions in event handlers can disrupt the normal flow of the application. Ensure proper error handling within your handlers.
- **Asynchronous Processing**: For tasks that require significant processing time, consider using asynchronous processing mechanisms to avoid blocking the main application flow.

By effectively leveraging event subscribers, developers can create responsive and dynamic behaviors in Plone 6, enhancing the functionality and user experience of their applications. 
