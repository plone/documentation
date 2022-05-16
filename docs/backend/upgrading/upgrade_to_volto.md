---
html_meta:
  "description": "Upgrade to Volto"
  "property=og:description": "Upgrade to Volto"
  "property=og:title": "Upgrade to Volto"
  "keywords": "Upgrading, Plone 6, Volto"
---

(backend-upgrade-to-volto-label)=

# Upgrading to Volto

To upgrade an existing site to run with Volto requires a couple of changes to your existing content.

The form `/@@migrate_to_volto` allows you to run all these steps directly.
After you upgraded your existing Database to Plone 6 there also is a message **You can prepare your site for Volto, the default frontend of Plone 6!** with a link to the form `localhost:8080/Plone/@@migrate_to_volto`.

```{warning}
Test all migrations thoroughly it before applying them on a production-environment!

A migrated site will still work in Plone Classic but behave different.
Editors can only work with the content effectively using Volto.
```

The required steps are:

1. **Install the packages {py:mod}`plone.volto` and {py:mod}`plone.restapi`.**

    {py:mod}`plone.restapi` is the RESTful hypermedia API for Plone that allows the Frontend Volto to communicate with the backend.
    {py:mod}`plone.volto` configures Plone to work with Volto, the new default frontend for Plone 6.

1. **Migrate Richtext-Fields to Volto blocks**

    Volto has a new editor different from TinyMCE that is used in Classic Plone.
    This step converts the html stored in RichText fields into text-blocks so you can edit it in Volto.
    Images, Links and most kinds of html-formating are preserved.


    For this you need to have `blocks-conversion-tool` running on an accessible url.
    The easiest way to have that running on your machine is to use docker:

    ```shell
    docker run -it -p 5000:5000 plone/blocks-conversion-tool:latest
    ```

    For more options read https://github.com/plone/blocks-conversion-tool.

1. **Pages, News Items and Events are made folderish**

    That means these types can contain other content like Images or other Pages.
    When you create a new site in Plone 6 this setting is also applied automatically.
    But existing content remains non-folderish undtil this step is run.

1. **Turn folders into folderish pages**

    In Volto adding Folders is disabled by default.
    Instead folderish pages are used to create folder-structures.
    This step turn all folders into folderish pages.
    If the folder showed a listing of the content a appropriate listing block will be added.
    If the folder showed a default page that will be handled in the next step.
    You can re-enable Folders by checking the box *Implicitly addable?* in ``/portal_types/Folder/manage_propertiesForm``.

1. **Default Pages of Folders are merged with the Folderish Pages that replace the Folder**

    Volto does not have a concept of default pages.
    Instead folderish pages can show text and/or a listing of all the content inside that page.
    This step takes the content of the default-page (e.g. text or the query of a collection) and adds that to the folderish page that replaced the folder.
    Metadata (subjects, author, rights...) and relations are moved to the folderish page.


1. **Collections are migrated to Pages with Listing Blocks**

    In Volto adding Collections is disabled by default.
    Instead folderish pages with listing blocks are used.
    This step turns all collections into folderish pages.
    The criteria of the collection are uses to configure a listing block in that page.


It is recommended to use the default settings but you can choose to skip some of the migration-steps in the form.