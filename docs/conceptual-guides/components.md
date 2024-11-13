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

```{note}
If you need to use parameters, such as context or request, consider using views or adapters instead.
```

To learn about some important utilities in Plone, read the chapter {doc}`/backend/global-utils`.


```{todo}
The rest of this chapter is a work in progress and an outline of great things to come.
Pull requests are welcome!
```

### Adapters

- general
- views, viewlets
- forms
- overriding
  - adapters
  - utilities
  - views


### Lookup

- lookup adapter
  - using the Interface as abstract factory
  - using the API
  - IRO, names ...
- lookup an utility, names, singletons and factory based


### Events and Subscribers

- general zope events
- lifecycle events
- important events in plone
