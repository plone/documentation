---
html_meta:
  "description": "Upgrading to Volto"
  "property=og:description": "Upgrading to Volto"
  "property=og:title": "Upgrading to Volto"
  "keywords": "Upgrading, Plone 6, Volto"
---

(backend-upgrading-to-volto-label)=

```{todo}
Is this "upgrading" or "migrating"? It seems to be a migration more than an upgrade. Please clarify.

Technically it is a migration since the version of Plone does not get changed and it is no upgrade-step.
It could be called a upgrade though because Volto is the new default frontend.
Not 100% sure...
```


# Upgrading to Volto

Plone 6 comes with a new default frontend, called Volto.
Volto is written in React and uses `plone.restapi` to communicate with the backend.
When creating a new site in Plone 6 you have the option to choose between creating a Volto site and a Classic Plone site.
This is because there are some non-trivial differences between the configuration of a Classic Plone and a Volto site.

This document discusses these differences and tells admins and developers how to modify their existing Plone site to be compatible with Volto.
Pre-requisites: The site needs to be upgraded to Plone 6 before

Plone provides a form `/@@migrate_to_volto` that allows you to run all the required changes to your existing site to make it compatible with Volto.
You can access this form in the browser when you are logged-in as an administrator by opening `http://localhost:8080/Plone/@@migrate_to_volto` (where `localhost` is your server, `8080` the port that Plone is running on and `Plone` is the name of the Plone instance).

After upgrading an existing site to Plone 6 (see {doc}`v60`) there will also appear a message **You can prepare your site for Volto, the default frontend of Plone 6!** with a link to that form.



```{warning}
Test all migrations thoroughly before applying them on a production environment!

A site that is make compatible with Volto will be accessible with Plone Classic UI, but it will behave differently.
For example, editors can only effectively work with the content using Volto because html is no longer editable in the TinyMCE editor.
```

```{todo}
`{py:mod}` does not link to the Python modules (see https://deploy-preview-1254--6-dev-docs-plone-org.netlify.app/backend/upgrading/upgrade_to_volto.html).

We could either use inline literals as shown in the suggestion, or we could link to their Glossary entry (or create one), GitHub repo, PyPI project, or relevant chapter in the docs. Which do you think is best?

I like `{py:mod}` because it is semantic and renders like a inline-literal. We don't require link in these cases.
```

The required steps are:

1.  **Install the packages {py:mod}`plone.volto` and {py:mod}`plone.restapi`.**

    {py:mod}`plone.restapi` is the RESTful API for Plone that allows the frontend Volto to communicate with the backend.
    {py:mod}`plone.volto` configures Plone to work with Volto, the new default frontend for Plone 6.

1.  **Migrate RichText fields to Volto blocks**

    Volto has a new editor called Slate, whereas Classic UI uses TinyMCE.
    This step converts the HTML stored in RichText fields to text blocks, allowing you to edit them in Volto.
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
    You can re-enable Folders by checking the box *Implicitly addable?* in ``/portal_types/Folder/manage_propertiesForm``.

1.  **Default Pages of Folders are merged with the Folderish Pages that replace the Folder**

    Volto does not have a concept of default pages.
    Instead folderish pages can show text, a listing of all the content inside that page, or both.
    This step takes the content of the default page (such as text or the query of a collection), and adds that to the folderish page that replaces the folder.
    Metadata (subjects, author, rights, and so on) and relations are moved to the folderish page.


1.  **Collections are migrated to Pages with Listing Blocks**

    In Volto adding Collections is disabled by default.
    Instead folderish pages with listing blocks are used.
    This step turns all collections into folderish pages.
    The criteria of the collection are uses to configure a listing block in that page.

It is recommended to use the default settings, but you can choose to skip some of the migration steps in the form.

```{note}
If you are migrating a existing site to Plone 6 using [{py:mod}`collective.exportimport`](https://pypi.org/project/collective.exportimport) and want to use Volto in the new site
you do not need to use the form `@@migrate_to_volto`.

All the changes documented above can be done efficiently during export and import and are discussed [here](https://github.com/collective/collective.exportimport/issues/133).
```
