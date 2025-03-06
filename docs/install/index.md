---
myst:
  html_meta:
    "description": "Get started with Plone 6"
    "property=og:description": "Get started with Plone 6"
    "property=og:title": "Get started"
    "keywords": "Plone 6, install"
---

(get-started-label)=

# Get started

This part of the documentation helps you find the best way to get started with Plone, depending on what you want to do.

```{contents} I'd like to...
:local: true
```


(get-started-try-plone-label)=

## Try a Plone demo

Choose a version to demo.

https://volto.demo.plone.org/
:   Plone 6 with Volto frontend

https://demo.plone.org/
:   Plone 6 with Volto frontend and some add-ons, including Volto Light Theme, with content that demonstrates all the content types of Plone and blocks in Volto

[https://classic.demo.plone.org/](https://classic.demo.plone.org/login?came_from=/en)
:   Plone 6 with Classic UI frontend


(get-started-install-label)=

## Install Plone

First, choose a Plone user interface, or frontend.
You can read {doc}`/conceptual-guides/choose-user-interface` to help inform your choice between Volto and Classic UI.

If you choose Classic UI, then you can read {doc}`/conceptual-guides/compare-buildout-pip` to help inform your choice between Buildout and pip for an installation method.

Then choose one of the following installation methods.
If you are following a [Plone training](https://training.plone.org/), it should specify which option to choose.

{doc}`create-project-cookieplone`
:   This is the recommended way to install Plone for a new project with the Volto frontend.
    Cookieplone requires Python version {{SUPPORTED_PYTHON_VERSIONS_PLONE61}}.

{doc}`/admin-guide/install-buildout`
:   This is one way to install Plone with the Classic UI frontend.
    Using Buildout will be the most familiar way for admins who have experience with Plone 3, 4, or 5.

{doc}`/admin-guide/install-pip`
:   This is one way to install Plone with the Classic UI frontend.
    It provides a basic installation without many additional tools to help with development.

{doc}`Install Plone as a contributor </contributing/index>`
:   This option is for developers who want to contribute to Plone and its packages.


(get-started-learn-more-label)=

## Learn more about Plone

The {doc}`/conceptual-guides/index` explain concepts to help you understand Plone.

The community has created a set of [Plone trainings](https://training.plone.org/) which are hosted separately from the documentation.
Plone trainings take place at every annual Plone Conference.


(get-started-contribute-label)=

## Contribute to Plone

See the {doc}`Contributor Guide </contributing/index>` to learn how to participate in the Plone community and contribute to our open source software. 
