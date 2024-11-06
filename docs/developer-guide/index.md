---
myst:
  html_meta:
    "description": "Plone development guide"
    "property=og:description": "Plone development guide"
    "property=og:title": "Development guide"
    "keywords": "Plone 6, development guide, developer, development"
---

# Development guide

```{note}
This part of the documentation is under revision, consolidating documentation for development from its various locations into in one section.
Until then, you can use the [search feature](https://6.docs.plone.org/search.html?q=development).
You can also help with this effort, even if it is to report that something is missing, by [creating an issue](https://github.com/plone/documentation/issues/new?assignees=&labels=&projects=&template=new-issue-form.yml).
```

This part of the documentation provides information for how to develop in Plone.
This development guide points you, as a developer, to the appropriate resource.


## Tests

Tests ensure that your project functions as expected, and that changes to the code base during development don't break anything.


### Volto

-   {doc}`Volto acceptance tests </volto/contributing/acceptance-tests>`
-   {doc}`Volto unit tests </volto/contributing/testing>`
-   {ref}`testing-the-add-on-label`


### Classic UI

```{note}
Classic UI testing for Plone 6 is in the process of being written.
```


### Backend

```{note}
Backend testing for Plone 6 is in the process of being written.
Until it is complete, Plone 5 documentation is the authoritative source for writing tests for the Plone backend.
```

-   {doc}`Backend tests <plone5:develop/testing/index>` (Plone 5)


## Create an add-on

-   {doc}`create-a-backend-add-on`
-   {doc}`/volto/development/add-ons/create-an-add-on-18`


## Create a Plone distribution

{doc}`create-a-distribution`


## Create content types

-   {doc}`/backend/content-types/creating-content-types`
-   {doc}`plone5:develop/plone/content/index` (Plone 5)


## Register views

{doc}`plone5:develop/plone/views/index` (Plone 5)


## Register API services

{doc}`backend/configuration-registry`


## {term}`ZCA`
% TODO: This is a mixture of conceptual and how-to guides. Move its parts where they belong and rewrite.
{doc}`plone5:develop/addons/components/index` (Plone 5)


## {term}`ZCML`
% TODO: This is a mixture of conceptual and how-to guides. Move its parts where they belong and rewrite.
{doc}`plone5:develop/addons/components/zcml` (Plone 5)


```{toctree}
:maxdepth: 2
:hidden:

create-a-backend-add-on
create-a-distribution
```
