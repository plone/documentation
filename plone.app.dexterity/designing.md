---
myst:
  html_meta:
    "description": "Designing with content types in Plone"
    "property=og:description": "Designing with content types in Plone"
    "property=og:title": "Designing with content types in Plone"
    "keywords": "Plone, designing, content types"
---

# Designing with content types

Before we dive into Dexterity, it is worth thinking about the way we design solutions with content types in Plone.
If you are familiar with Archetypes based development, Grok, or Zope 3, then much of this will probably be familiar.

Plone uses the ZODB, an object database, instead of a relational database as its default content store.
The ZODB is well suited to heterogeneous, loosely structured content such as web pages.

Types in Plone are either containers or items (this distinction is sometimes called folderish versus non-folderish).
A one-to-many type relationship is typically modeled as a container (the "one") containing many items (the "many"), although it is also possible to use references across the content hierarchy.

Each type has a schema, which is a set of fields with related properties, such as a title, default value, constraints, and so on.
The schema is used to generate forms and describe instances of the type.
In addition to schema-driven forms, a type typically comes with one or more views, and is subject to security—for example, add permissions, or per-field read/write permissions—and workflow.

When we attempt to solve a particular content management problem with Plone, we will often design new content types.
For the purpose of this tutorial, we'll build a simple set of types to help conference organizers.
We want to manage a program consisting of multiple sessions.
Each session should be listed against a track, and have a time slot, a title, a description, and a presenter.
We also want to manage biographies for presenters.

There are many ways to approach this, but here is one possible design:

-   A content type Presenter is used to represent presenter biographies.
    Fields include name, description, and professional experience.
-   A content type Program represents a given conference program.
    Besides some basic metadata, it will list the available tracks.
    This type is folderish.
-   A content type Session represents a session.
    Sessions can only be added inside Programs.
    A Session will contain some information about the session, and allow the user to choose the track and associate a presenter.

Each type will also have custom views, and we will show how to configure catalog indexers, security, and workflow for the types.
