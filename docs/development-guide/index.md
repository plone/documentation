---
myst:
  html_meta:
    "description": "Development guide for Plone 6"
    "property=og:description": "Development guide for Plone 6"
    "property=og:title": "Development guide for Plone 6"
    "keywords": "Plone, development, guide, tests, Volto, frontend, REST API, plone.api, backend"
---

(development-guide-label)=

# Development guide

This part of Plone 6 documentation provides guidance for the development of Plone.

Development of Plone uses both the Python and JavaScript ecosystems.

-   Volto, the default frontend for Plone 6, is based on the React JavaScript framework.
-   Classic UI, the legacy frontend in Plone 6 and earlier versions, is based on the Twitter Bootstrap 5 framework and other JavaScript tools.
-   The backend consists of dozens of Python packages.
    Plone REST API and `plone.api` are two of the more prominent Python packages in the Plone backend.

Each frontend and backend package may have its own specific development methods.
This development guide points you, as a developer, to the appropriate resource.


## Tests

Tests ensure that your project functions as expected, and that changes to the code base during development don't break anything.



### Volto

```{note}
Frontend testing for Plone 6 is in the process of being written using Cookieplone and pytest.
Until it is complete, you can refer to the following guides and use tests in Volto core and add-ons for examples.
```

-   {doc}`Volto acceptance tests </volto/contributing/acceptance-tests>`
-   {doc}`Volto unit tests </volto/contributing/testing>`
-   {ref}`testing-the-add-on-label`


### Backend

```{note}
Backend testing for Plone 6 is in the process of being written using Cookieplone and pytest.
Until it is complete, Plone 5 documentation is the authoritative source for writing tests for the Plone backend.
```

-   {doc}`Backend tests <plone5:develop/testing/index>` (Plone 5)
