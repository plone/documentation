---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Introduction

**About this manual**

This manual should teach you everything you need to know to write your own behaviors, but not how to integrate them into another framework.

*Behaviors* are re-usable bundles of functionality that can be enabled or disabled on a per-content type basis.
Examples might include:

- A set of form fields (on standard add and edit forms),
- Enabling particular event handler,
- Enabling one or more views, viewlets or other UI components,
- Anything else which may be expressed in code via an adapter and/or marker interface.

You would typically not write a behavior as a one-off.
Behaviors are normally used when:

- You want to share fields and functionality across multiple types easily.
  Behaviors allow you to write a schema and associated components (e.g. adapters, event handlers, views, viwelets) once and re-use them easily.
- A more experienced developer is making functionality available for re-use by less experienced integrators.
  For example, a behavior can be packaged up and release as an add-on product.
  Integrators can then install that product and use the behavior in their own types, either in code or through-the-web.

This manual is aimed at developers who want to write new behaviors.
This is a slightly more advanced topic than the writing of custom content types.
It assumes you are familiar with buildout, know how to create a custom package, understand interfaces and have a basic understanding of Zope’s component architecture.

Behaviors are not tied to Dexterity, but Dexterity provides behavior support for its types via the *behaviors* FTI property.
In fact, if you’ve used Dexterity before, you’ve probably used some behaviors.
Take a look at the [Dexterity Developer Manual] for more information about how to enable behaviors on a type and for a list of standard behaviors.

To learn more about how behaviors in detail are implemented, see the [plone.behavior] package.

[dexterity developer manual]: ../index.html
[plone.behavior]: http://pypi.python.org/pypi/plone.behavior
