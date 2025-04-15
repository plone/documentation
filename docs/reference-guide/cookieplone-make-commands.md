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
:   Invokes the target `install` in `frontend/Makefile`.
    Uses `pnpm dlx` to run [mrs-developer](https://github.com/collective/mrs-developer) to retrieve dependencies in the file {file}`frontend/mrs.developer.json`.
    It then installs the dependencies.
    Finally, it builds the dependency packages `@plone/registry` and `@plone/components` from source.

`frontend-build`
:   Invokes the target `build` in `frontend/Makefile`.
    This creates a production bundle for distribution of the project with the add-on.

`frontend-start`
:   Invokes the target `start` in `frontend/Makefile`.
    This starts Volto, allowing reloading of the add-on during development.

`frontend-test`
:   Invokes the target `test` in `frontend/Makefile`.
    This runs unit tests.


## Backend

When you issue a `make` command at the root of your project, you call the file {file}`Makefile` also at the root.
In turn, it invokes commands in the file {file}`backend/Makefile`.
You can refer to these files for implementation details.
You can run the following make targets by using the command structure of `make <TARGET>`.

`backend-install`
:   Invokes the target `install` in `backend/Makefile`.
    This creates a `Python` virtual environment if one does not exist.
    It then installs Plone and its dependencies in that virtual environment.
    After installation, it runs `make backend-create-site` to initialize a new Plone site with default content.

`backend-build`
:   Invokes the target `install` in `backend/Makefile`.
    This creates a `Python` virtual environment if one does not exist.
    It then installs Plone and its dependencies in that virtual environment.
    This is useful when you need to reload changes from your backend add-on, and don't need to recreate a full Plone site.

`backend-create-site`
:   Invokes the target `create-site` in `backend/Makefile`.
    This first ensures the virtual environment exists.
    Creates a new Plone site with default content.
  
`backend-update-example-content`
:   Invokes the target `update-example-content` in `backend/Makefile`.
    This first ensures the virtual environment exists.
    Next, it removes all content from the destination directory, if any content exists.
    Finally, it exports the Plone site content.

`backend-start`
:   Invokes the target `start` in `backend/Makefile`.
    This starts a Plone instance on `localhost:8080`.

`backend-test`
:   Invokes the target `test` in `backend/Makefile`.
    This runs unit tests.


## Environment

When you issue a `make` command at the root of your project, you call the file {file}`Makefile` also at the root.
In turn, it invokes commands in the files {file}`backend/Makefile` and {file}`frontend/Makefile`.
You can refer to these files for implementation details.
You can run the following make targets by using the command structure of `make <TARGET>`.

`install`
:   Invokes the target `backend-install` and `make frontend-install` in `backend/Makefile` and `frontend/Makefile` respectively.
    This installs the add-ons in the development environment for both backend and frontend.

`clean`
:   Invokes the target `clean` in both `backend/Makefile` and `frontend/Makefile`.
    This command cleans both backend (removing virtual environments, cached files, and instance data) and frontend (removing core files and node_modules) environments.


## Quality assurance (QA)

When you issue a `make` command at the root of your project, you call the file {file}`Makefile` also at the root.
In turn, it invokes commands in the files {file}`backend/Makefile` and {file}`frontend/Makefile`.
You can refer to these files for implementation details.
You can run the following make targets by using the command structure of `make <TARGET>`.

`format`
:   Invokes the target `format` in both `backend/Makefile` and `frontend/Makefile`. 
    This formats the code base according to Plone standards.

`lint`
:   Invokes the target `lint` in both `backend/Makefile` and `frontend/Makefile`. 
    Checks for problems—such as linting, formatting, and style issues—but does not auto-fix them.
    It only reports errors.

`check`
:   Runs both `format` and `lint` in sequence.


## Internationalization (i18n)

When you issue a `make` command at the root of your project, you call the file {file}`Makefile` also at the root.
In turn, it invokes commands in the files {file}`backend/Makefile` and {file}`frontend/Makefile`.
You can refer to these files for implementation details.
You can run the following make targets by using the command structure of `make <TARGET>`.

`i18n`
:   Invokes the target `i18n` in both `backend/Makefile` and `frontend/Makefile`. 
    It updates translations in your project.


## Testing

When you issue a `make` command at the root of your project, you call the file {file}`Makefile` also at the root.
In turn, it invokes commands in the files {file}`backend/Makefile` and {file}`frontend/Makefile`.
You can refer to these files for implementation details.
You can run the following make targets by using the command structure of `make <TARGET>`.

`test`
:   Invokes the target `backend-test` and `make frontend-test` in `backend/Makefile` and `frontend/Makefile` respectively. 
    This runs unit tests in the project.


## Container images

When you issue a `make` command at the root of your project, you call the file {file}`Makefile` also at the root.
In turn, it invokes commands in the files {file}`backend/Makefile` and {file}`frontend/Makefile`.
You can refer to these files for implementation details.
You can run the following make targets by using the command structure of `make <TARGET>`.

`build-images`
:   Invokes the target `build-image` in both `backend/Makefile` and `frontend/Makefile`. 
    This builds Docker images for both backend and frontend.