---
myst:
  html_meta:
    "description": "Explanation of how to choose between Plone's two user interfaces, Volto and Classic UI"
    "property=og:description": "Explanation of how to choose between Plone's two user interfaces, Volto and Classic UI"
    "property=og:title": "Choose a user interface"
    "keywords": "Plone 6, Conceptual guides, UI, user interface, frontend, Volto, Classic UI, distribution"
---

# Choose a user interface

This guide explains the differences between Plone's two user interfaces, Volto and Classic UI, to help inform you to choose one when developing your new project in Plone, or whether to migrate from Classic UI to Volto.
There is no migration path available from Volto to Classic UI.

The choice of user interface has implications for editors, admins, and developers.

`````{grid} 1 1 1 2
:gutter: 1
:margin: 0
:padding: 0

````{grid-item-card} Volto
```{image} /_static/volto-ui.png
:alt: Plone home page in Volto
:target: /_static/volto-ui.png
```

Test it on https://volto.demo.plone.org (without add-ons) or https://demo.plone.org (with add-ons).

For editors and other end users:

-   The user interface is a fast, modern, single-page web application.
-   Editors can create sophisticated page layouts by arranging {term}`blocks` of different types.
-   There is not a comprehensive {doc}`/volto/user-manual/index` yet, and only a few pages exist.

For developers and integrators:

-   The frontend is a {term}`React`-based application written in JavaScript and TypeScript.
-   The backend is a Python process which provides a {term}`REST API` for the frontend.
-   Python skills are not required, but can be helpful for extending the backend.
-   Content is stored as structured JSON.
-   Customization of themes is well-documented and relatively easy for developers who have experience with React.

````

````{grid-item-card} Classic UI
```{image} /_static/classic-ui.png
:alt: Plone home page in Classic UI
:target: /_static/classic-ui.png
```

Test it on https://classic.demo.plone.org.

For editors and other end users:

-   The user interface is similar to Plone 5.
-   Editors create a page using a {term}`WYSIWYG` editor, {term}`TinyMCE`.
-   Additional widgets can be added to predefined locations, using {term}`portlets`.
    More sophisticated page layout requires the use of add-ons.
-   There is a comprehensive [User Manual for Plone 5](https://5.docs.plone.org/working-with-content/index.html), but it has not been updated for Plone 6.

For developers and integrators:

-   The frontend and backend run in a single Python process, so hosting is a bit simpler.
-   The frontend is implemented as server-side templates using the {term}`ZPT` language.
-   Interactive functionality is implemented in JavaScript using {term}`Mockup`.
-   The visual design is based on the {term}`Barceloneta` theme from Plone 5, but updated to use Bootstrap 5.
-   Content is stored as HTML.
-   Customization of themes is not well-documented.

````
`````
