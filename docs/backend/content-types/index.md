---
myst:
  html_meta:
    "description": "How to develop Dexterity content types in Plone."
    "property=og:description": "How to develop Dexterity content types in Plone."
    "property=og:title": "Content types"
    "keywords": "Content types, Dexterity, Plone"
---

# Content Types

This part of the documentation describes how to develop content types in Plone.
Content types are implemented through the {term}`Dexterity` framework.


## What is a content type?

Each item in a Plone site is an instance of a particular content type.
We have different content types to reflect the different kinds of information about which we need to collect and display information.

`Folder`, `Page`, `News item`, `Event`, `File` (binary), and `Image` are examples of content types.

Lots of things in Plone can be configured to work differently based on the content type.
For example, each content type has:

-   a {doc}`schema </backend/schemas>` specifying the fields which can be edited for the content type
-   a list of {doc}`behaviors </backend/behaviors>` which supply additional functionality that can be attached to the content types for which the behavior is enabled
-   a {doc}`workflow </backend/workflows>` controlling transitions between publishing states and associated permissions
-   a version policy controlling whether to store a revision history

It is common in developing a website that you'll need customized versions of common content types, or perhaps even entirely new types.


## Designing with content types

Plone uses the ZODB, an object database, instead of a relational database as its default content store.
The ZODB is well suited to heterogeneous, loosely structured content such as web pages.

Types in Plone are either `containers` or `items` (this distinction is sometimes called folderish versus non-folderish).
A one-to-many type relationship is typically modeled as a container (the "one") containing many items (the "many"), although it is also possible to use references across the content hierarchy.

Each type has a {doc}`schema </backend/schemas>`, which is a set of {doc}`/backend/fields` with related properties, such as a title, default value, constraints, and other properties.
The schema is used to generate forms and describe instances of the type.
In addition to schema-driven forms, a type typically comes with one or more {doc}`/classic-ui/views` as well as {doc}`/classic-ui/viewlets` and is subject to security—for example, add permissions, or per-field read and write permissions—and workflow.


## Topics

This part of the documentation will cover the following topics.

-   Some basic design techniques for solving problems with content types in Plone
-   Setting up a Dexterity development environment
-   Creating a package to house your types
-   Building a custom type based on a schema
-   Creating custom views and forms for your type
-   Advanced customization, including workflow and security
-   Testing your types
-   A quick reference to common fields, widgets, and APIs

```{seealso}
See the chapter {doc}`training:mastering-plone/dexterity` from the Mastering Plone 6 Training for a step-by-step tutorial to create a custom content type.
```


```{toctree}
:maxdepth: 2
:caption: Table of contents
creating-content-types
fti
```

```{toctree}
:maxdepth: 2
```
% Uncomment each of the following and move into the `toctree` above when migrated from Plone 5 documentation
% prerequisite
% schema-driven-types
% model-driven-types
% custom-views
% advanced/index
% testing/index
% reference/index
