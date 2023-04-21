---
myst:
  html_meta:
    "description": "The fundamental concepts behind behaviors for content types in Plone"
    "property=og:description": "The fundamental concepts behind behaviors for content types in Plone"
    "property=og:title": "The fundamental concepts behind behaviors for content types in Plone"
    "keywords": "Plone, content types, behavior, basics"
---

# Behavior basics

This chapter describes the fundamental concepts behind behaviors.

Before we dive into the practical examples, we need to explain a few of the concepts that underpin behaviors.

At the most basic level, a behavior is like a "conditional" adapter.
For a Dexterity content type, the default condition is, "is this behavior listed in the `behaviors` property in the FTI?"
But the condition itself is an adapter; in rare cases this can be overruled.
When a behavior is enabled for a particular object, it will be possible to adapt that object to the behavior's interface.
If the behavior is disabled, adaptation will fail.

A behavior consists at the very least of an interface and some metadata, namely a title and a description.
In most cases, there is also a *factory*, akin to an adapter factory, which will be invoked to get an appropriate adapter when requested.
This is usually just a class that looks like any other adapter factory, although it will tend to be applicable to `Interface`, `IContentish`, or a similarly broad context.

Behaviors may specify a *marker interface*, which will be directly provided by instances for which the behavior is enabled.
This is useful if you want to conditionally enable event handlers or view components, which are registered for this marker interface.
Some behaviors have no factory.
In this case, the behavior interface and the marker interface must be one and the same.
If a factory is given, a marker interface different from the behavior interface must be declared.

Behaviors are registered globally, using the `<plone.behavior />` ZCML directive.
This results in, among other things, a named utility providing `plone.behavior.interfaces.IBehavior` being registered.
This utility contains various information about the behavior, such as its name, title, interface, and (optional) marker interface.
The utility name is the full dotted name to the behavior interface.
