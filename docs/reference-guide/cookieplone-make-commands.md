---
myst:
  html_meta:
    "description": "Cookieplone make commands"
    "property=og:description": "Cookieplone make commands"
    "property=og:title": "Cookieplone make commands"
    "keywords": "Cookieplone, make, commands"
---

# Cookieplone `make` commands

This reference guide describes the function and purpose of all the `make` commands found in a {term}`Cookieplone` project.
It's organized according to its components.
-   Frontend
-   Backend
-   Documentation
-   Environment
-   Quality assurance (QA)
-   Internationalization (i18n)
-   Testing
-   Container images
-   Local stack
-   Acceptance

## Frontend

When you issue a `make` command at the root of your project, you call the file {file}`Makefile` also at the root.
In turn, it invokes commands in the file {file}`frontend/Makefile`.
You can refer to these files for implementation details.
You can run the following make targets by using the command structure of `make <TARGET>`.

`frontend-install`
:   Invokes the target `make install` in `frontend/Makefile`.
    This installs the add-ons in the development environment.

`frontend-build`
:   Invokes the target `make build` in `frontend/Makefile`.
    This creates a production bundle for distribution of the project with the add-on.

`frontend-start`
:   Invokes the target `make start` in `frontend/Makefile`.
    This starts Volto, allowing reloading of the add-on during development.

`frontend-test`
:   Invokes the target `make test` in `frontend/Makefile`.
    This runs unit tests.


## Backend

When you issue a `make` command at the root of your project, you call the file {file}`Makefile` also at the root.
In turn, it invokes commands in the file {file}`backend/Makefile`.
You can refer to these files for implementation details.
You can run the following make targets by using the command structure of `make <TARGET>`.

`backend-install`
:   Invokes the target `make install` in `backend/Makefile`.
    This creates a `Python` virtual environment if one does not exist.
    It then installs Plone and its dependencies in that virtual environment.
    After installation, it runs `make backend-create-site` to initialize a new Plone site.

`backend-build`
:   Invokes the target `make install` in `backend/Makefile`.
    This creates a production bundle for distribution of the project with the add-on.

`backend-create-site`
:   Invokes the target `make create-site` in `backend/Makefile`.
    This first ensures the virtual env exists.
    Creates a new Plone site with default content.
  
`backend-update-example-content`
:   Invokes the target `make update-example-content` in `backend/Makefile`.
    This first ensures the virtual env exists.
    Checks if example-content exists. If yes, deletes all files inside to ensure a fresh export.
    Then exports the Plone content.

`backend-start`
:   Invokes the target `make start` in `backend/Makefile`.
    This starts a Plone instance on localhost:8080.

`backend-test`
:   Invokes the target `make test` in `backend/Makefile`.
    This runs unit tests.


## Environment

When you issue a `make` command at the root of your project, you call the file {file}`Makefile` also at the root.
In turn, it invokes commands in the files {file}`backend/Makefile` and {file}`frontend/Makefile`.
You can refer to these files for implementation details.
You can run the following make targets by using the command structure of `make <TARGET>`.

`install`
:   Invokes the target `make backend-install` and `make frontend-install` in `backend/Makefile` and `frontend/Makefile` respectively.
    This installs the add-ons in the development environment for both backend and frontend.

`clean`
:   Invokes the target `make clean` in both `backend/Makefile` and `frontend/Makefile`.
    This command cleans both backend (removing virtual environments, cached files, and instance data) and frontend (removing core files and node_modules) environments.


## Quality assurance (QA)

When you issue a `make` command at the root of your project, you call the file {file}`Makefile` also at the root.
In turn, it invokes commands in the files {file}`backend/Makefile` and {file}`frontend/Makefile`.
You can refer to these files for implementation details.
You can run the following make targets by using the command structure of `make <TARGET>`.

`format`
:   Invokes the target `make format` in both `backend/Makefile` and `frontend/Makefile`. 
    This formats the codebase according to Plone standards

`lint`
:   Invokes the target `make lint` in both `backend/Makefile` and `frontend/Makefile`. 
    Checks for problems (linting, formatting, style issues) but does not auto-fix them, it only reports errors.

`check`
:   Runs both `format` and `lint` in sequence.


## Internationalization (i18n)

When you issue a `make` command at the root of your project, you call the file {file}`Makefile` also at the root.
In turn, it invokes commands in the files {file}`backend/Makefile` and {file}`frontend/Makefile`.
You can refer to these files for implementation details.
You can run the following make targets by using the command structure of `make <TARGET>`.

`i18n`
:   Invokes the target `make i18n` in both `backend/Makefile` and `frontend/Makefile`. 
    It is used to update locales in your project.


## Testing

When you issue a `make` command at the root of your project, you call the file {file}`Makefile` also at the root.
In turn, it invokes commands in the files {file}`backend/Makefile` and {file}`frontend/Makefile`.
You can refer to these files for implementation details.
You can run the following make targets by using the command structure of `make <TARGET>`.

`test`
:   Invokes the target `make backend-test` and `make frontend-test` in `backend/Makefile` and `frontend/Makefile` respectively. 
    This runs unit tests in the project.


## Container images

When you issue a `make` command at the root of your project, you call the file {file}`Makefile` also at the root.
In turn, it invokes commands in the files {file}`backend/Makefile` and {file}`frontend/Makefile`.
You can refer to these files for implementation details.
You can run the following make targets by using the command structure of `make <TARGET>`.

`build-images`
:   Invokes the target `make build-image` in both `backend/Makefile` and `frontend/Makefile`. 
    This build Docker Images for both backend and frontend.