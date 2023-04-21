---
myst:
  html_meta:
    "description": "How to write your own behaviors for content types in Plone"
    "property=og:description": "How to write your own behaviors for content types in Plone"
    "property=og:title": "How to write your own behaviors for content types in Plone"
    "keywords": "Plone, behaviors, content types, introduction"
---

# Introduction

This manual should teach you everything you need to know to write your own behaviors, but not how to integrate them into another framework.

Behaviors are reusable bundles of functionality that can be enabled or disabled on a per-content type basis.
Examples might include:

-   A set of form fields (on standard add and edit forms)
-   Enabling particular event handler
-   Enabling one or more views, viewlets, or other UI components
-   Anything else which may be expressed in code via an adapter or marker interface.

You would typically not write a behavior as a one-off.
Behaviors are normally used when:

-   You want to share fields and functionality across multiple types easily.
    Behaviors allow you to write a schema and associated components—including adapters, event handlers, views, and viewlets—once and reuse them.
-   A more experienced developer makes functionality available for reuse by less experienced integrators.
    For example, a behavior can be packaged up and released as an add-on product.
    Integrators can then install that product, and use the behavior in their own types, either in code or through-the-web.

This manual is aimed at developers who want to write new behaviors.
This is a slightly more advanced topic than the writing of custom content types.
It assumes you are familiar with buildout, know how to create a custom package, understand interfaces, and have a basic understanding of Zope's component architecture.

Behaviors are not tied to Dexterity, but Dexterity provides behavior support for its types via the *behaviors* FTI property.
In fact, if you've used Dexterity before, you've probably used some behaviors.
Take a look at the {doc}`Dexterity Developer Manual <../index>` for more information about how to enable behaviors on a type, and for a list of standard behaviors.

To learn more about how behaviors are implemented in detail, see the [`plone.behavior`](https://pypi.org/project/plone.behavior/) package.
