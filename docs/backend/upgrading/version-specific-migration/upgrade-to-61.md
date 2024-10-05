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
