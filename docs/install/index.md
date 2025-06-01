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
Read {doc}`/conceptual-guides/choose-user-interface` to help inform your choice between Volto and Classic UI.

Then choose one of the following installation methods.

```{note}
If you are following a [Plone training](https://training.plone.org/), it should specify which option to choose.
```

{doc}`create-project-cookieplone`
:   This is the recommended way to install Plone with either Volto or Classic UI for a frontend.

{doc}`/admin-guide/install-buildout`
:   This is another way to install Plone with the Classic UI frontend, but not Volto.
    Using Buildout will be the most familiar way for admins who have experience with Plone 3, 4, or 5.

{doc}`/admin-guide/install-pip`
:   This is another way to install Plone with the Classic UI frontend, but not Volto.
    It provides a basic installation without many additional tools to help with development.

{doc}`Install Plone as a contributor </contributing/index>`
:   This option is for developers who want to contribute to Plone and its packages.

```{seealso}
If you don't want to use Cookieplone as the recommended way to install Plone with Classic UI for a frontend, read {doc}`/conceptual-guides/compare-buildout-pip` to help inform your choice between Buildout and pip for an installation method.
```
