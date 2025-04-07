---
myst:
  html_meta:
    "description": "Cookieplone make commands"
    "property=og:description": "Cookieplone make commands"
    "property=og:title": "Cookieplone make commands"
    "keywords": "Cookieplone, make, commands"
---

# Cookieplone `make` commands

This guide explains all the `make` commands found in a cookieplone project.

## Frontend

The Makefile at the root of your project invokes commands in frontend/Makefile. Here are excerpts from frontend/Makefile to show details of the frontend make commands.

`frontend-install`

The command `make frontend-install`:

-   Invokes the target `make install` in `frontend/Makefile`.
    -   This installs the add-ons in the development environment.

`frontend-build`

The command `make frontend-build`:

-   Invokes the target `make build` in `frontend/Makefile`.
    -   This creates a production bundle for distribution of the project with the add-on.

`frontend-start`

The command `make frontend-start`:

-   Invokes the target `make start` in `frontend/Makefile`.
    -   This starts Volto, allowing reloading of the add-on during development.

`frontend-test`

The command `make frontend-test`:

-   Invokes the target `make test` in `frontend/Makefile`.
    -   This runs unit tests.


## Backend

The Makefile at the root of your project invokes commands in backend/Makefile. Here are excerpts from backend/Makefile to show details of the backend make commands.

`backend-install`

The command `make backend-install`:

-   Invokes the target `make install` in `backend/Makefile`.
    -   This creates a `Python` virtual environment if one does not exist.
    -   It then installs Plone and its dependencies in that virtual environment.
    -   After installation, it runs `make backend-create-site` to initialize a new Plone site.

`backend-build`

The command `make backend-build`:

-   Invokes the target `make install` in `backend/Makefile`.
    -   This creates a production bundle for distribution of the project with the add-on.

`backend-create-site`

The command `make backend-create-site`:

-   Invokes the target `make create-site` in `backend/Makefile`.
    -   This first ensures the virtual env exists.
    -   Creates a new Plone site with default content.
  
`backend-update-example-content`

The command `make backend-update-example-content`:

-   Invokes the target `make update-example-content` in `backend/Makefile`.
    -   This first ensures the virtual env exists.
    -   Checks if example-content exists. If yes, deletes all files inside to ensure a fresh export.
    -   Then exports the Plone content.

`backend-start`

The command `make backend-start`:

-   Invokes the target `make start` in `backend/Makefile`.
    -   This starts a Plone instance on localhost:8080.

`backend-test`

The command `make backend-test`:

-   Invokes the target `make test` in `backend/Makefile`.
    -   This runs unit tests.