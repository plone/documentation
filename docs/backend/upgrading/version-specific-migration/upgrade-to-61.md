---
myst:
  html_meta:
    "description": "How to upgrade to Plone 6.1"
    "property=og:description": "How to upgrade to Plone 6.1"
    "property=og:title": "How to upgrade to Plone 6.1"
    "keywords": "Upgrade, Plone 6"
---

(backend-upgrade-plone-v61-label)=

# Upgrade Plone 6.0 to 6.1

Plone 6.1 has seen the following major changes.
Some may require changes in your setup.


## Drop Python 3.8 and 3.9

We only support Python 3.10, 3.11, and 3.12.


## TinyMCE upgraded in Classic UI

In Plone 6.0, the Classic UI frontend uses TinyMCE 5, a rich text editor for websites.
TinyMCE 5 reached its end of support on April 20, 2023.
For Plone 6.1, Classic UI upgraded TinyMCE from version 5 to 7.

If you upgrade a site using Classic UI from Plone 6.0 to 6.1, you do not need to take any action, unless you implemented custom plugins, or you use a plugin which got removed or moved to premium in TinyMCE versions 6 or 7.
To upgrade your plugin implementation to TinyMCE 7, see the [upgrade guides](https://www.tiny.cloud/docs/tinymce/6/migration-from-5x/#plugins).


### Enable the TinyMCE accordion plugin

1.  Go to the {guilabel}`Site Setup > General > TinyMCE` control panel to manage TinyMCE settings.
1.  Under the {guilabel}`Plugins and Toolbar` tab, check {guilabel}`accordion` to enable the accordion plugin.
1.  Under the same tab, add a menu entry `accordion` for TinyMCE in the control panel by editing the `items` key as shown.

    ```json
    {
      "insert": {
        "title": "Insert",
        "items": "link media | template hr | accordion"
      },
    }
    ```

1.  Click the {guilabel}`Save` button to save your settings.
1.  In the {guilabel}`Security > HTML filtering` control panel, add two new tags to {guilabel}`Valid tags`.

    -   `summary`
    -   `details`

1.  Also in the {guilabel}`Security > HTML filtering` control panel, add a new attribute to {guilabel}`Custom attributes`.

    -   `open`

1.  For a transform to valid markup of the Bootstrap 5 accordion, use an output filter.

    ```{seealso}
    -   [Addon collective.outputfilters.tinymceaccordion](https://github.com/collective/collective.outputfilters.tinymceaccordion)
    ```


## `z3c.form` and `plone.app.z3cform`

````{todo}
This is a placeholder.

-   Update deprecated imports
-   New widget templates

```{seealso}
https://github.com/plone/plone.app.z3cform/pull/181
```
````


## `plone.app.multilingual` is a core add-on

`plone.app.multilingual` is the package that adds multilingual support to Plone, allowing the storage and display of content in multiple languages.
In Plone 6.0 and earlier, this was a dependency of `Products.CMFPlone`, making it available for installation in all Plone sites.
In Plone 6.1 it is now a dependency of the `Plone` package.

If your project or your add-on needs this package, and you only depend on `Products.CMFPlone` until now, you should add `plone.app.multilingual` as a dependency.
Then your project or add-on will keep working in both Plone 6.0 and 6.1.

The goal of turning more of the current core packages into core add-ons is to make the core smaller, and in some cases solve circular dependencies.


(backend-upgrade-plone-v61-discussion-label)=


## Discussion is a core add-on

Discussion is a feature that allows your site visitors to comment on web pages for any content object.
The code behind this is in the `plone.app.discussion` package.
In Plone 6.0 and earlier, this was a dependency of `Products.CMFPlone`, making it available for installation in all Plone sites.
In Plone 6.1 it's a dependency of the `Plone` package.

Discussion is disabled by default in Plone 6.1 and later.
To enable discussion, you need to perform the following tasks.

1.  In your Python {file}`requirements.txt` or {file}`pyproject.toml` file, add the core add-on `plone.app.discussion` to your dependencies.
1.  Run pip to install `plone.app.discussion`.
1.  Restart the Plone backend to load `plone.app.discussion`.
1.  Enable the {guilabel}`Discussion Support` add-on in the {guilabel}`Add-ons` control panel under {menuselection}`Site Setup --> General`.
1.  If you use Plone Classic UI, you can then use the {guilabel}`Discussion` control panel to further configure this feature, for example, to enable comment moderation.
1.  🍻

If you have an existing Plone 5.2 or 6.0 site and you migrate to 6.1, then migration code handles the change as follows.

-   If the `plone.app.discussion` Python package is in your setup, the migration does nothing.
    Existing discussion configuration and comments remain unchanged.
-   If the `plone.app.discussion` Python package is _not_ in your setup, and the site has no existing comments (discussions), then the migration code removes the Discussion configuration from your site.
    Apparently you were _not_ using comments in your site, so the configuration is no longer needed.
-   If the `plone.app.discussion` Python package is _not_ in your setup, but the site has existing comments (discussions), then the migration code stops with an error.
    Apparently you _were_ using comments in your site.
    Add the `plone.app.discussion` package to your dependencies, and run the migration again.


## Distributions

Plone 6.1 introduces the concept of a Plone {term}`distribution`.
The idea for distributions has been around for a long time.
Now it is available in core Plone as the recommended way for creating a Plone site.
A Plone distribution defines its Python package dependencies and add-ons that are always activated when creating a new site.
It defines content items, plus possibly extras like users.

When you install the `Plone` 6.1 Python package you get several new packages and two distributions:

* `plone.distribution` is the main new package that offers the basis for distributions.
* `plone.exportimport` is the way for importing and exporting content, users, etc.
  `plone.distribution` uses this.
* `plone.volto` is the default distribution.
   This package was already there in Plone 6.0, but has gotten an upgrade to a distribution.
   This would be the distribution that you use for creating a Plone site for use with the default Volto frontend.
* `plone.classicui` is a new package and contains the Classic UI distribution.
   This would be the distribution that you use for creating a Plone site with the server side Classic UI frontend.

When you start a new project with `Plone` 6.1 the Zope root looks like this when there are no Plone sites yet:

```{image} images/zope-root-distributions.png
```

On the left you can create a Plone site with the default distribution (`plone.volto`) and on the right with the Classic UI distribution.
Clicking will show more or less the same form with questions as you would get before in Plone 6.0.

If you don't want to use distributions, you don't have to.
If your project only uses the `Products.CMFPlone` Python package, you can still create a Plone site in the usual way.
The form is simpler and shorted though.
The created site has no content, so no News or Events folders.
You can't select extra add-ons to install.
You can still activate extra add-ons in the Add-ons control panel.

There are a few things you should consider when upgrading a project to 6.1 or making an add-on compatible:

* In general, you don't need no change anything.
  Your existing site will keep working.
  But adding a new site may change in the ways described earlier.
* Do you want to use the `Products.CMFPlone` package (0 distributions), `plone.volto/classicui` (1 distribution) or `Plone` (2 distributions)?
* When your site used the default Volto frontend, you will already have `plone.volto` as dependency.
  This can stay the same.
* When your site is only using the `Products.CMFPlone` package, this is a Classic UI site.
  This can stay the same, but you may want to depend on `plone.classicui`.
  With that package you can still create a new site and have the same content as before.
* When your site is using the `Plone` package, you will have the two new distributions available.
  This is fine.
  If you know you only need `plone.volto` or only need `plone.classicui`, you can switch to that.
  You can also limit the options for selecting a distribution by setting the environment variable `ALLOWED_DISTRIBUTIONS` with fewer options.
  Set `ALLOWED_DISTRIBUTIONS=default` for the default distribution (`plone.volto`).
  Set `ALLOWED_DISTRIBUTIONS=classic` for the classic distribution (`plone.classicui`).
* If you switch from `Plone` to `plone.volto` or `plone.classicui` you may want to install extra core add-ons, for example `plone.app.upgrade` or `plone.app.caching`.
* If your add-on is only for Volto, you may want to add `plone.volto` as dependency.
* If your add-on is only for Classic UI, you may want to add `plone.classicui` as dependency.
  Note though that `plone.classicui` is not available for Plone 6.0.

You can create your own distributions.
Some use cases for this:

* Create a distribution demonstrating your favorite setup for Plone.
  This would contain the add-ons that you usually add in each project, including example content.
  With this you can create a fully configured Plone site filled with content for a potential client.
  Or they can try it themselves if the distribution is available publicly.
* Create a distribution for an internal or client project.
  This would create a site with all add-ons activated and configured for this project, including example content and maybe users.
  During the development phase of a new project all developers would use this to create a fresh site locally so that everyone has the same setup and contents.
  Before the project goes live, you can use the distribution to create the initial setup.

Note: in Plone 7 the aim is to create a clearer separation between Classic UI and the core `Products.CMFPlone` backend.
This means in Plone 7 `Products.CMFPlone` will have less code and pull in less dependencies.
`plone.classicui` may have more code and pull in more dependencies.
This is the direction the backend is heading in, and the introduction of the `plone.classicui` distribution package is an important step for this.

For detailed information, see the source code of the new packages:

* [`plone.distribution`](https://github.com/plone/plone.distribution/)
* [`plone.exportimport`](https://github.com/plone/plone.exportimport/)
