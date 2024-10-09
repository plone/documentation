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
A Plone distribution is a Python package that defines specific features, themes, add-ons, and configurations that get activated when creating a Plone site.
Now it is available in core Plone as the recommended way for creating a Plone site.

When you install the [`Plone` 6.1 Python package](https://pypi.org/project/Plone/), you get several new packages and two distributions:

-   [`plone.distribution`](https://github.com/plone/plone.distribution) is the new main package that offers the basis for distributions.
-   [`plone.exportimport`](https://github.com/plone/plone.exportimport) imports and exports content, users, and other objects between Plone sites and when upgrading Plone.
    It is now the preferred method, and `plone.distribution` uses it.
-   [`plone.volto`](https://github.com/plone/plone.volto) is the distribution to create a Plone site with the default frontend Volto.
    This package was already present in Plone 6.0, but was upgraded to a distribution.
-   [`plone.classicui`](https://github.com/plone/plone.classicui) is a new package and is the distribution to create a Plone site with the Classic UI frontend.

When you start a new project with `Plone` 6.1, the launch screen prompts you to choose a frontend distribution when creating a new Plone site.

````{card}
```{image} /backend/upgrading/version-specific-migration/images/distribution-chooser.png
:alt: Launch screen for choosing a frontend distribution
:target: /_images/distribution-chooser.png
```
+++
_Launch screen for choosing a frontend distribution_
````

After you select a frontend distribution, you will fill out a brief form to configure your new Plone 6.1 site, similar to the process for Plone 6.0.

Distributions are optional.
If your project only uses the `Products.CMFPlone` Python package, you can still create a Plone site in the usual way.
Consider, however, the following differences from distributions.

-   The configuration form is simpler and shorter.
-   The created site has no content, and therefore no {guilabel}`News` or {guilabel}`Events` folders.
-   You must install then activate add-ons through the {guilabel}`Add-ons` control panel.

There are a few things you should consider when upgrading a project to, or making an add-on compatible with, Plone 6.1:

-   In general, you don't need no change anything.
    Your existing site will keep working.
    But adding a new site may change in the ways described earlier.
-   Do you want to use the `Products.CMFPlone` package (0 distributions), either `plone.volto` or `plone.classicui` (1 distribution), or `Plone` (2 distributions)?
-   When your site used the default Volto frontend, you will already have `plone.volto` as a dependency.
    This can stay the same.
-   When your site uses only the `Products.CMFPlone` package, the frontend is Classic UI.
    This can stay the same, but you may want to depend on `plone.classicui`.
    With that package you can still create a new site and have the same content as before.
-   When your site is using the `Plone` package, you will have the two new distributions available.
    This is fine.
    If you know you only need `plone.volto` or only need `plone.classicui`, you can switch to that.
    You can also limit the options for selecting a distribution by setting the environment variable `ALLOWED_DISTRIBUTIONS` with fewer options.
    Set `ALLOWED_DISTRIBUTIONS=default` for the default Volto frontend distribution (`plone.volto`).
    Set `ALLOWED_DISTRIBUTIONS=classic` for the Classic UI frontend distribution (`plone.classicui`).
-   If you switch from `Plone` to `plone.volto` or `plone.classicui`, you might want to install extra core add-ons, for example `plone.app.upgrade` or `plone.app.caching`.
-   If your add-on is only for Volto, you may want to add `plone.volto` as a dependency.
-   If your add-on is only for Classic UI, you may want to add `plone.classicui` as a dependency.
    Note though that `plone.classicui` is not available for Plone 6.0.

You can create your own distributions to suit your needs.

-   Create a distribution demonstrating your favorite setup for Plone.
    This would contain the add-ons that you usually add in each project, including example content.
    With this you can create a fully configured Plone site filled with content for a potential client.
    Or they can try it themselves if the distribution is available publicly.
-   Create a distribution for an internal or client project.
    This would create a site with all add-ons activated and configured for this project, including example content, and optionally users and groups.
    During the development phase of a new project, all developers would use this to create a fresh site locally so that everyone has the same configuration and content.
    Before the project goes live, you can use the distribution to create the initial setup.

```{note}
For Plone 7, the [Plone roadmap](https://plone.org/why-plone/roadmap) guides development toward a clearer separation between the Classic UI frontend and the core `Products.CMFPlone` backend.
This means in Plone 7 `Products.CMFPlone` will have less code and pull in fewer dependencies.
`plone.classicui` may have more code and pull in more dependencies.
This is the direction in which the backend is heading, and the introduction of the `plone.classicui` distribution package is an important step along this path.
```

For detailed information, see the source code of the new packages.

-   [`plone.distribution`](https://github.com/plone/plone.distribution/)
-   [`plone.exportimport`](https://github.com/plone/plone.exportimport/)
