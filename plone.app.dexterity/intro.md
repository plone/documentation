---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Introduction

This manual will teach you how to build content types using the Dexterity system.

If you have decided that Dexterity is for you, and you are a programmer and comfortable
working on the filesystem, then this manual is a good place to start.

This manual will cover:

-   Some basic design techniques for solving problems with content types in Plone
-   Getting a Dexterity development environment set up
-   Creating a package to house your types
-   Building a custom type based on a schema
-   Creating custom views and forms for your type
-   Advanced customization, including workflow and security
-   Testing your types
-   A quick reference to common fields, widgets, and APIs


## Why was Dexterity created?

Dexterity was created to serve two audiences: Administrators/integrators and developers.

For administrators and integrators, Dexterity offers:

-   the ability to create new content types through-the-web
-   the ability to switch on/off various aspects (called "behaviors") on a per-type basis
-   improved collaboration between integrators (who may define a type's schema, say) and programmers (who may provide re-usable behaviors that the administrator can plug in).

For developers, Dexterity promises:

-   the ability to create content types more quickly and easily, and with less boilerplate and repetition, than what is possible with Archetypes or plain CMF types
-   content objects with a smaller runtime footprint, to improve performance
-   types that use the now-standard `zope.interface`/`zope.schema` style of schema, and more broadly support modern idioms that sit a little awkardly with Archetypes and its ilk

## How is Dexterity different from Archetypes?

Dexterity is an alternative to Archetypes, Plone's venerable content type framework.
Being more recent, Dexterity has been able to learn from some of the mistakes that were made Archetypes, and more importantly leverage some of the technologies that did not exist when Archetypes was first conceived.

Some of the main differences include:

-   Dexterity is able to leverage many technologies that come with newer versions of CMF and Zope 3.
    This means that the Dexterity framework contains significantly less code than Archetypes.
    Dexterity also has better automated test coverage.
-   Dexterity is more modular where Archetypes is more monolithic.
    This promises to make it easier to support things like SQL database-backed types, alternative workflow systems, instance-specific sub-types, and so on.
    It also means that many of the components developed for Dexterity, such as the through-the-web schema editor, the "behaviors" system, or the forms construction API (`plone.autoform`) are re-usable in other contexts, for example, to build standalone forms or even to augment existing Archetypes-based types.
-   Archetypes has its own schema implementation, which is incompatible with the interface-based approached found in `zope.interface` and `zope.schema`.
    The latter is used throughout the Zope stack to describe components and build forms.
    Various techniques exist to bridge the Archetypes schema to the Zope 3 schema notation, but none are particularly attractive.
-   Archetypes uses accessor and mutator methods to get/set values.
    These are generated and scribbled onto a class at startup.
    Dexterity uses attribute notation.
    Whereas in Archetypes you may write `context.getFirstName()`, in Dexterity you would write `context.first_name`.
-   Archetypes has its own implementation of fields and widgets.
    It is difficult to re-use these in standalone forms or templates, because they are tied to the idea of a content object.
    Dexterity uses the de-facto standard `z3c.form` library instead, which means that the widgets used for standalone forms are the same as those used for content type add and edit forms.
-   Archetypes does not support add forms.
    Dexterity does, via `z3c.form`.
    This means that Dexterity types do not need to use the `portal_factory` hack to avoid stale objects in content space, and are thus significantly faster and less error prone.
-   Archetypes requires a chunk of boilerplate in your product's `initialize()` method (and requires that your package is registered as a Zope 2 product) and elsewhere.
    It requires a particular sequence of initialization calls to register content classes, run the class generator to add accessors/mutators, and set up permissions.
    Dexterity does away with all that boilerplate, and tries to minimise repetition.
-   It is possible to extend the schemata of existing Archetypes types with the `archetypes.schemaextender` product, although this adds some performance overhead and relies on a somewhat awkward programming technique.
    Dexterity types were built to be extensible from the beginning, and it is possible to declaratively turn on or off aspects of a type (such as Dublin Core metadata, locking support, ratings, tagging, and so on) with re-usable "behaviors".
-   Dexterity is built from the ground up to support through-the-web type creation.
    There are products that achieve the same thing with Archetypes types, but they have to work around a number of limitations in the design of Archetypes that make them somewhat brittle or slow.
    Dexterity also allows types to be developed jointly through-the-web and on the filesystem.
    For example, a schema can be written in Python and then extended through the web.

As of version 5 of Plone, Dexterity is the preferred way of creating content types.
Additionally, Archetypes was removed from Plone core in 5.2.
Archetypes can still be added to Plone 5 to support Archetypes-based add-ons, but it will not function when running Plone using Python 3.
