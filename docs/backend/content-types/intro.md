---
myst:
  html_meta:
    "description": "A content type is an object that can store information and is editable by users."
    "property=og:description": "A content type is an object that can store information and is editable by users."
    "property=og:title": "Content Types"
    "keywords": "Content Types, FTI, Dexterity"
---

(backend-content-types-label)=

# Content types introduction

This part of the documentation describes how to develop content types in Plone.
Content types are implemented through the {term}`Dexterity` framework.


## What is a content type?

Each item in a Plone site is an instance of a particular content type.
We have different content types to reflect the different kinds of information about which we need to collect and display information.

Folder, Page, News item, Event, File (binary), and Image are examples of content types.

Lots of things in Plone can be configured to work differently based on the content type. For example, each content type has:
- a {ref}`schema <backend-schemas-label>` specifying the fields which can be edited for the content type
- a list of {ref}`behaviors <backend-behaviors-label>` which supply additional functionality that can be attached to the content types for which the behavior is enabled
- a {ref}`workflow <backend-workflows-label>` controlling transitions between publishing states and associated permissions
- a version policy controlling whether to store a revision history

It is common in developing a web site that you'll need customized versions of common content types, or perhaps even entirely new types.


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
See the chapter {ref}`training:dexterity1-label` from the Mastering Plone 6 Training for a step-by-step tutorial to create a custom content type.
```

## Designing with content types

Plone uses the ZODB, an object database, instead of a relational database as its default content store.
The ZODB is well suited to heterogeneous, loosely structured content such as web pages.

Types in Plone are either `containers` or `items` (this distinction is sometimes called folderish versus non-folderish).
A one-to-many type relationship is typically modeled as a container (the "one") containing many items (the "many"), although it is also possible to use references across the content hierarchy.

Each type has a {ref}`schema <backend-schemas-label>`, which is a set of {ref}`backend-fields-label` with related properties, such as a title, default value, constraints, and so on.
The schema is used to generate forms and describe instances of the type.
In addition to schema-driven forms, a type typically comes with one or more {ref}`classic-ui-views-label` as well as {ref}`classic-ui-viewlets-label` and is subject to security—for example, add permissions, or per-field read/write permissions—and workflow.



```{toctree}
:maxdepth: 2
```
% Uncomment each of the following and move into the toctree above when migrated from Plone 5 documentation
% designing
% prerequisite
% schema-driven-types
% model-driven-types
% custom-views
% advanced/index
% testing/index
% reference/index

