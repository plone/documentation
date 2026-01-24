---
myst:
  html_meta:
    "description": "Conceptual guide of the Zope Component Architecture in Plone"
    "property=og:description": "Conceptual guide of the Zope Component Architecture in Plone"
    "property=og:title": "Conceptual guide of the Zope Component Architecture in Plone"
    "keywords": "Plone, Plone 6, Zope Component Architecture, ZCA, interface, adapter, utility, event, subscriber, registry, lookup"
---

# Component architecture

The {term}`Zope Component Architecture` (ZCA) is a Python framework for supporting component-based design and programming, utilizing the design patterns interface, adapter, abstract factory, and publish-subscribe.

Plone logic is wired together by Zope Component Architecture.
It provides the "enterprise business logic" engine for Plone.


## Concepts

The following high-level concepts are the core of the ZCA.

Interface
:   Abstract definition of the intended public behavior of an object providing the interface.

Adapter
:   Specific implementation of an interface.
    An adapter provides an interface on its own, and adapts one or more objects with specific interfaces.

Utility
:   Specific implementation of an interface either as a singleton or factored-on lookup.

Events and subscribers
:   Events are emitted, and a subscriber may listen to those events.
    Events provide an interface, and subscribers are registered for specific interfaces.
    Events are only dispatched to subscribers matching the interface of the event.

Registries
:   Adapters, utilities, and subscribers are registered in registries.
    Here the wiring is done.
    Additional to the interface, a name might be provided for adapters and utilities (so-called named adapters or named utilities).
    Registration can be done in Python code or via {term}`ZCML`, an XML dialect.

Lookup
:   The lookup functions are providing the logic to dynamically factor an adapter or utility matching the object that was fed in.
    You can ask to get an adapter to an object and pass in a name and the lookup method introspects the interface provided by the object and searches the registry for matches.


## Design patterns

To better understand the Zope Component Architecture, it helps to review the basics of a few of the 23 classical [design patterns](https://en.wikipedia.org/wiki/Software_design_pattern).

The interface pattern (its former name, and is now called "protocol pattern") is used to define the behavior of the adapter.

>   [...] a protocol or interface type is a data type describing a set of method signatures, the implementations of which may be provided by multiple classes that are otherwise not necessarily related to each other.
>   A class which provides the methods listed in a protocol is said to adopt the protocol, or to implement the interface.
>   
>   ~ _[Wikipedia, Protocol (object-oriented programming)](https://en.wikipedia.org/wiki/Protocol_(object-oriented_programming))_

The [marker pattern](https://en.wikipedia.org/wiki/Marker_interface_pattern) is an empty interface to associate metadata with a class.

Adapters in the ZCA are an implementation of the adapter design pattern in Zope.

>   In software engineering, the adapter pattern is a software design pattern [...] that allows the interface of an existing class to be used as another interface.
>   It is often used to make existing classes work with others without modifying their source code.
>   
>   ~ _[Wikipedia, Adapter design pattern](https://en.wikipedia.org/wiki/Adapter_pattern)_

Both adapters and utilities are initialized by an abstract factory pattern using the registries.

>   The abstract factory pattern provides a way to encapsulate a group of individual factories that have a common theme without specifying their concrete classes.
>   In normal usage, the client software creates a concrete implementation of the abstract factory and then uses the generic interface of the factory to create the concrete objects that are part of the theme.
>   The client does not know (or care) which concrete objects it gets from each of these internal factories, since it uses only the generic interfaces of their products.
>   This pattern separates the details of implementation of a set of objects from their general usage and relies on object composition, as object creation is implemented in methods exposed in the factory interface.
>   
>   ~ _[Wikipedia, Abstract factory pattern](https://en.wikipedia.org/wiki/Abstract_factory_pattern)_

The event system uses the publish-subscribe pattern.

>   [...] publish–subscribe is a messaging pattern where senders of messages, called publishers, do not program the messages to be sent directly to specific receivers, called subscribers, but instead categorize published messages into classes without knowledge of which subscribers, if any, there may be.
>   Similarly, subscribers express interest in one or more classes and only receive messages that are of interest, without knowledge of which publishers, if any, there are.
> 
>   ~ [Wikipedia, Publish–subscribe pattern](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)


### Further reading

-   [`zope.component`](https://zopecomponent.readthedocs.io/en/latest/index.html) documentation
-   [A Comprehensive Guide to Zope Component Architecture](https://github.com/baijum/zcadoc) by @baijum


## Component architecture in Plone

Plone incorporates the component architecture in its design.


### Registries

The component registry is used to register adapters, utilities, and subscribers.
On lookup, it is used to find and initialize the matching adapter for the given objects, and name if given; to adapt; to find the right utility for an interface, and name if given; and to call the matching subscribers for an event.

We have two levels of registries.

Global component registry
:   The Global component registry is always and globally available as a singleton.
    Configuration is done in Plone using {term}`ZCML` files, which is a {term}`XML`-{term}`DSL`.
    Usually they are named {file}`configure.zcml`, but they may include differently named ZCML files.

Local component registry
:   Each Plone site has its own local component registry.
    If there are one, two, or more Plone sites created in one database, each has its own local component registry.
    The local registry is activated and registered on traversal time.
    If a lookup in the local registry fails, then it falls back to the lookup in the global registry.
    In theory, registries can be stacked upon each other in several layers, but in practice in Plone, we have two levels: local and global.
    Configuration is done in the profile {term}`GenericSetup` in a file {file}`componentregistry.xml`.
    Note its syntax is completely different from ZCML.


### Utilities

Utility classes provide site-wide utility objects or functions.
Compared to "plain Python functions", utilities provide the advantage of being plug-in points without the need for monkey-patching.

They are registered by marker interfaces, and optionally with a name, in which case they are called "named utilities".
Accordingly, utilities can be looked up by name or interface.

Site customization logic or add-on products can override utilities for enhanced or modified functionality.


#### Global and local utilities

Utilities can be either global or local.

global
:   Registered during Zope's start-up.
    Global utilities are registered in ZCML, and affect the Zope application server and all Plone site instances.

local
:   Registered at the Plone site or add-on installer time for a certain site.
    Local utilities are registered to persistent objects.
    The context of local utilities is stored in a thread-local variable which is set during traversal.
    Thus, when you ask for local utilities, they usually come from a persistent registry set up in the Plone site root object.


#### Register a utility

You can register utilities in two ways, either by providing a _factory_, or a callable, which creates the object as a result, or by _component_, a ready-to-use object.
Utility factories take no constructor parameters.

A utility factory can be provided by either a function or class.

function
:   The function is called and it returns the utility object.

class
:   The class `__call__()` method itself acts as a factory and returns a new class instance.

A utility component can be either a:

-   function that needs to provide a (marker) interface, or
-   a global instance of a class implementing a marker interface, or
in the case of a local registry, a so-called "local component" which persists as an object in the ZODB and itself needs to provide a marker interface.

Utilities may or may not have a name.

```{todo}
A global utility is constructed when Plone is started and ZCML is read. (needs Verification)
A local component is either a persistent object in the ZODB or constructed when (TODO: When? Traversal time? Lookup time?)
```


To learn about some important utilities in Plone, read the chapter {doc}`/backend/global-utils`.


### Adapters

Adapters are a core part of the {term}`Zope Component Architecture` (ZCA).
They allow you to extend or change the behavior of an object without modifying its class.
They map one interface to another, allowing objects to gain new behavior without changing their original class.
By moving functionality out of the class and into adapters, Plone achieves loose coupling and a highly modular design, where components depend on interfaces rather than concrete implementations.

There are two kinds of adapters:

Normal Adapters

Normal adapters adapt a single object and are used when behavior depends on just one context. They are commonly applied to content objects to add computed values, helper methods, or additional behavior without modifying the original class. Because they deal with only one parameter, they are simple, lightweight, and easy to understand.

Multi-Adapters

Multi-adapters adapt multiple objects at once, passed as a tuple of parameters. They are used when behavior depends on more than one context, such as the content object, the current request, or the active view. 


#### Views, Viewlets

In Plone, views and viewlets are implemented as adapters.

Views:

In Plone, views are implemented as multi-adapters that adapt both the context (the content object being viewed) and the request (the current HTTP request). Their main responsibility is to produce rendered output, such as HTML pages, JSON responses for APIs, or other representations of content. Views are registered using ZCML, which allows them to be cleanly integrated into the system and easily replaced or customized. Because views are adapters, they can be overridden by registering another view with the same name and interfaces, making it possible to change or extend behavior without modifying any core Plone code.

Viewlets:

Viewlets, on the other hand, are small, reusable user interface components that together make up a page layout, such as headers, footers, navigation elements, or portlets. A viewlet is a more complex multi-adapter that adapts the context, request, the current view, and a viewlet manager, which controls where and how the viewlet is rendered on the page. This design allows viewlets to be highly flexible and context-aware. Themes and add-ons commonly override viewlet adapters to customize the look, placement, or behavior of specific UI elements, again without changing Plone’s core templates or logic.


#### Forms

Adapters play a central role in schema-driven forms in Plone. Rather than embedding logic directly inside form or field classes, Plone uses adapters to control field behavior, select appropriate widgets, apply validators, and perform data conversion between user input and stored values. This design brings several important benefits: form logic becomes highly reusable, behavior can be customized per content type or context, and developers can alter or extend form behavior without subclassing forms directly. As a result, forms remain clean, flexible, and easy to maintain, even in large and complex Plone applications.


#### Overriding

Plone allows behavior to be overridden without modifying core code, mainly through adapters and ZCML load order. This keeps customizations clean and upgrade-safe.

##### Overriding Adapters

Adapters are overridden by registering a new adapter with the same required and provided interfaces. The last loaded adapter wins, making this approach common in add-ons and themes for changing business logic or content-specific behavior.

##### Overriding Utilities

Utilities are global, context-independent services. They are overridden by re-registering the same interface and are typically used for configuration and core services like mail or search.

##### Overriding Views

Views can be overridden by:

Views can be overridden by registering a new view with the same name and controlling ZCML order. This is widely used for custom templates, API changes, and theme customization—all without touching core code.


### Lookup

Lookup is the dynamic process of retrieving an adapter or utility from the component registry.
The registry matches the requested interface against registered factories or components.

#### Lookup an adapter

There are two main ways to look up adapters.

Using the interface as an abstract factory
:   The notation `IMyInterface(context)` is shorthand for `getAdapter(context, IMyInterface)`.
    It uses the interface as an abstract factory and returns the adapted object.

Using the API
:   Use `zope.component.getAdapter()` or `zope.component.getMultiAdapter()` when you want an error if no adapter is found.
    Use `queryAdapter()` or `queryMultiAdapter()` when you want `None` instead.


For multi-adapters, pass a tuple of objects in the order declared in the registration:


##### Interface Resolution Order (IRO) and names

Adapter lookups consider the interfaces provided by the context in interface resolution order (IRO).
More specific interfaces win over more general ones.

Named adapters allow multiple implementations for the same required/provided interfaces.
You can pass a `name` to `getAdapter()` or `queryAdapter()` to select a specific implementation.



#### Lookup a utility

Utilities are looked up by provided interface and optional name.

Use `getUtility()` when you want an error if the utility is not found.
Use `queryUtility()` when you want `None` instead.


To list utilities, use `getUtilitiesFor()` or `getAllUtilitiesRegisteredFor()`:


#### Global and local lookup

Lookups use the current site manager.
In a Plone site, the local component registry is active and falls back to the global registry when needed.
Outside a site context, lookups use the global registry.



### Events and Subscribers

Events are objects that represent something happening in the system.
Subscribers (event handlers) are callables that react to those events.
Plone uses `zope.event` and the Zope Component Architecture to register and dispatch subscribers.

#### General Zope events

Events are interface-driven.
Subscribers are registered for a combination of object interface and event interface.
When an event is notified, all matching subscribers are called.


#### Lifecycle events

The most common lifecycle events in Plone come from `zope.lifecycleevent`, such as:

`IObjectCreatedEvent`
:   Fired when a new object is created.
    Often used to set defaults, initialize metadata, or attach related content.

`IObjectModifiedEvent`
:   Fired when an object is modified.
    Use it to react to data changes (for example, reindexing or updating derived fields).

`IObjectMovedEvent`
:   Fired when an object is moved or renamed.
    Useful for updating references, breadcrumbs, or paths stored elsewhere.

`IObjectRemovedEvent`
:   Fired when an object is removed.
    Use it to clean up external resources or related objects.

`IObjectCopiedEvent`
:   Fired when an object is copied.
    You can use it to adjust IDs, titles, or external references on the new copy.

#### Important events in Plone

Plone adds a few events you may need to handle explicitly:

Workflow events
:   `Products.DCWorkflow.interfaces.IBeforeTransitionEvent` is fired before a workflow transition is executed.
    It is useful for validation, veto logic, or preparing state changes.
    `Products.DCWorkflow.interfaces.IAfterTransitionEvent` is fired after the transition completes,
    and is commonly used for side effects such as notifications or reindexing.
    `Products.CMFCore.interfaces.IActionSucceededEvent` is a higher-level event that signals a completed action,
    and is often easier to use for general workflow reactions.

Local roles change event
:   `LocalrolesModifiedEvent` is triggered when local roles are updated, for example in the sharing view.
    Use it to update cached permissions, invalidate security-related indexes, or refresh UI state.
    If your add-on depends on local roles or sharing changes, subscribe to this event.

Login and logout events
:   `Products.PlonePAS.events.UserLoggedInEvent` and
    `Products.PlonePAS.events.UserLoggedOutEvent` are fired on successful login and logout.
    They are useful for audit trails, login/logout hooks, cleanup tasks, or session initialization.

Modification date handling
:   Dexterity updates the modification date when objects are modified.
    If your subscriber changes data, be aware that it may update the modification timestamp and trigger more events.
