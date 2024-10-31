---
myst:
  html_meta:
    "description": "How to add a Plone site to an existing Zope instance"
    "property=og:description": "How to add a Plone site to an existing Zope instance"
    "property=og:title": "Create a Plone site"
    "keywords": "Plone 6, create, add, factory, distributions"
---

% This should move into the Admin guide once https://github.com/plone/documentation/pull/1746 is merged.

(add-a-plone-site-label)=

# Add a Plone site

This section explains how to add a Plone site to an existing Zope instance.
It assumes that you have already {doc}`installed </install/index>` and started Plone.

Some installation methods create a Plone site for you already.
Follow these instructions if you used an installation method that did not do this,
or if you need a second Plone site in the same instance for some reason.

```{versionadded} Plone 6.1
The user interface for creating a new Plone site was changed in Plone 6.1.
You can access it the same way in Plone 6.0, but the appearance and options are different.
```

Open the Plone backend. Usually it is running at http://localhost:8080/

This launch screen prompts you to choose one of the available {term}`distributions <distribution>` to create a new site.

% add a link to choose-user-interface doc once https://github.com/plone/documentation/pull/1749 is merged

````{card}
```{image} /backend/upgrading/version-specific-migration/images/distribution-chooser.png
:alt: Launch screen for choosing a distribution
:target: /_images/distribution-chooser.png
```
+++
_Launch screen for choosing a distribution_
````

Hover over your choice and click the {guilabel}`Create` button.

Now complete the form with initial configuration for your site. You can configure:

:::{card}
Path Identifier
:   The ID of the site. This ends up as part of the URL unless hidden by an upstream web server.

Title
:   The name of the site in the HTML `title` element. This will be shown as part of the title of the browser tab on each page.

Site Description
:   A brief description that will be served in an HTML `meta` tag.

Site Logo
:   Upload an image as the main site logo.

Language
:   The main language of the site.

Timezone
:   The default timezone setting of the portal.
:::

Finally, press {guilabel}`Submit`.

Have fun with your new Plone site!

```{important}
If you are using the Volto frontend, keep in mind that the launch screen for adding a site is hosted by the Plone backend server.
After you create the site, you must switch to Volto.
Usually, it is running at http://localhost:3000.
```
