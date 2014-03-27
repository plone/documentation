=================
What's a Portlet?
=================

.. admonition:: Description

    This manual covers what a developer needs to know to create new portlet
    types or customise existing ones.

Portlets are UI elements that can be shown in addition to the main content
of a page. They usually appear in the left of right columns, but are
sometimes also used instead of or below the main content.  They are usually
boxes of different kinds, which content editors can add, configure, and
set policies for showing.

(Screenshot).

Differences with viewlets
=========================

A portlet is like a viewlet but with persistent configuration (i.e.
persistent in the ZODB) and runtime changeable assignments.

Use a viewlet for:

- General content which is always displayed; for example: breadcrumbs, the
  logo, or the footer. This is not limited to visible elements, but can also
  include CSS, javascript, etc.  (actually, that's how
  ``ResourceRegistries`` work).
- Displaying elements based on the interface provided by the current
  context.

Use a portlet when:

- You need to specify the configuration data for an item; e.g. the number of
  entries to show.
- You want to give the content editors a choice about when and where to
  display it.
- You want to display it only from inside a specific folder.
- You'd like to show it only to some groups or users; e.g. the *Review*
  portlet is only shown to users who belong to the *Reviewers* group.
