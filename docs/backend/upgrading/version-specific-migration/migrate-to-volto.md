---
myst:
  html_meta:
    "description": "Migrating from Plone Classic UI to Volto"
    "property=og:description": "Migrating from Plone Classic UI to Volto"
    "property=og:title": "Migrating from Plone Classic UI to Volto"
    "keywords": "Migrating, Upgrading, Plone 6, Volto, Classic UI"
---

(backend-migrate-to-volto-label)=

# Migrating from Plone Classic UI to Volto

Plone 6 comes with a new default frontend called {term}`Volto`.
Volto is written in React and uses {py:mod}`plone.restapi` to communicate with the backend.

When creating a new Plone 6 site, you may choose between frontends.

-   Volto - {guilabel}`Create a new Plone site`, the default option.
-   {term}`Classic UI` - {guilabel}`Create Classic Plone site`.
-   {guilabel}`Advanced`.

```{image} /_static/plone-classic-ui-landing-page.png
:class: figure
:alt: Plone Classic UI landing page
```

This choice is presented because there are some non-trivial differences between their configurations.
This document discusses these differences.
It also informs administrators and developers of how to migrate their existing Plone 6 site with Classic UI to instead become compatible with Volto for its frontend.

```{important}
As a pre-requisite, your Plone site must be {doc}`upgraded to Plone 6 <upgrade-to-60>` before migrating to Volto for the frontend.
```

Plone provides a form `/@@migrate_to_volto` that allows you to run all the required changes to your existing site to make it compatible with Volto.

You can access this form in the browser when you are logged in as an Administrator.
Open `http://localhost:8080/Plone/@@migrate_to_volto`, where `localhost` is your hostname, `8080` is the port on which Plone runs, and `Plone` is the name of the Plone instance.

Additionally, after upgrading an existing site to Plone 6 (see {doc}`upgrade-to-60`), a message will appear, **You can prepare your site for Volto, the default frontend of Plone 6!**, with a link to that form.

```{warning}
Test all migrations thoroughly before applying them on a production environment!

A site that is made compatible with Volto will be accessible with Plone Classic UI, but it will behave differently.
For example, Editors can only effectively work with the content using Volto because HTML is no longer editable in the TinyMCE editor used in Classic UI.
```


## Upgrade to Volto steps

The required steps are:

1.  **Install the packages {py:mod}`plone.volto` and {py:mod}`plone.restapi`.**

    {py:mod}`plone.restapi` is the RESTful API for Plone that allows the frontend Volto to communicate with the backend.
    {py:mod}`plone.volto` configures Plone to work with Volto, the new default frontend for Plone 6.

1.  **Migrate `RichText` fields to Volto blocks**

    Volto has a new editor called Slate, whereas Classic UI uses TinyMCE.
    This step converts the HTML stored in `RichText` fields to text blocks, allowing you to edit them in Volto.
    Images, links, and most kinds of HTML formatting are preserved.

    For this you need to have `blocks-conversion-tool` running on an accessible URL.
    The easiest way to have that running on your machine is to use Docker:

    ```shell
    docker run -it -p 5000:5000 plone/blocks-conversion-tool:latest
    ```

    For more options read https://github.com/plone/blocks-conversion-tool.

1.  **Pages, News Items, and Events are made folderish**

    That means these types can contain other content such as Images or other Pages.
    When you create a new site in Plone 6, this setting is also applied automatically.
    But existing content remains non-folderish until this step is run.

1.  **Turn folders into folderish pages**

    In Volto adding Folders is disabled by default.
    Instead folderish pages are used to create folder structures.
    This step turns all folders into folderish pages.
    If the folder shows a listing of the content, an appropriate listing block will be added.
    If the folder shows a default page, then it will be handled in the next step.
    You can re-enable Folders by checking the box {guilabel}`Implicitly addable?` in `/portal_types/Folder/manage_propertiesForm`.

1.  **Default Pages of Folders are merged with the Folderish Pages that replace the Folder**

    Volto does not have a concept of default pages.
    Instead, folderish pages can show text, a listing of all the content inside that page, or both.
    This step takes the content of the default page (such as text or the query of a collection), and adds that to the folderish page that replaces the folder.
    Metadata (subjects, author, rights, and so on) and relations are moved to the folderish page.

1.  **Collections are migrated to Pages with Listing Blocks**

    In Volto adding Collections is disabled by default.
    Instead, folderish pages with listing blocks are used.
    This step turns all collections into folderish pages.
    The criteria of the collection are used to configure a listing block in that page.

It is recommended to use the default settings, but you can choose to skip some migration steps in the form.

```{note}
If you are migrating an existing site to Plone 6 using [{py:mod}`collective.exportimport`](https://pypi.org/project/collective.exportimport) and want to use Volto in the new site, then you do not need to use the form `@@migrate_to_volto`.

All the changes documented above can be done efficiently during export and import.
[Read details](https://github.com/collective/collective.exportimport?tab=readme-ov-file#migrate-to-volto).
```
