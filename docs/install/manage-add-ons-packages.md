---
myst:
  html_meta:
    "description": "Manage add-ons, packages, and processes"
    "property=og:description": "Manage add-ons, packages, and processes"
    "property=og:title": "Manage add-ons, packages, and processes"
    "keywords": "Plone 6, manage, backend, add-ons, packages, processes, cookiecutter, Zope"
---


(manage-add-ons-packages-and-processes-label)=

# Manage add-ons and packages

This chapter assumes you have previously followed {doc}`create-project`.
In this section, we discuss details of the installation process so that you can customize your Plone installation.


(manage-installation-details-with-cookiecutter-label)=

## Installation details with Cookiecutter

{term}`Cookiecutter` creates projects from project templates.
The cookiecutter [`cookiecutter-plone-starter`](https://github.com/collective/cookiecutter-plone-starter/) creates a Plone project that you can install using {term}`Make`.
It generates files for installing and configuring both the frontend and backend.
For the backend, it uses [`cookiecutter-zope-instance`](https://github.com/plone/cookiecutter-zope-instance) to generate configuration files for a Zope WSGI instance.


(manage-configuration-with-cookiecutter-zope-instance-label)=

## Configuration with `cookiecutter-zope-instance`

You can configure your instance's options, including the following.

-   persistent storage: blobs, direct filestorage, relational database, ZEO, and so on
-   ports
-   threads
-   cache
-   debugging and profiling for development

```{seealso}
For a complete list of features, usage, and options, read [`cookiecutter-zope-instance`'s `README.rst`](https://github.com/plone/cookiecutter-zope-instance#readme).
```
