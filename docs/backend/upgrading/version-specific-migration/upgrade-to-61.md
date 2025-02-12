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

We only support Python {{SUPPORTED_PYTHON_VERSIONS_PLONE61}}.


## TinyMCE upgraded in Classic UI

In Plone 6.0, the Classic UI frontend uses TinyMCE 5, a rich text editor for websites.
TinyMCE 5 reached its end of support on April 20, 2023.
For Plone 6.1, Classic UI upgraded TinyMCE from version 5 to 7.

If you upgrade a site using Classic UI from Plone 6.0 to 6.1, you do not need to take any action, unless you implemented custom plugins, or you use a plugin which got removed or moved to premium in TinyMCE versions 6 or 7.
To upgrade your plugin implementation to TinyMCE 7, see the [upgrade guides](https://www.tiny.cloud/docs/tinymce/6/migration-from-5x/#plugins).


### Enable the TinyMCE accordion plugin

1.  Install the add-on [`collective.outputfilters.tinymceaccordion`](https://pypi.org/project/collective.outputfilters.tinymceaccordion/) to use an output filter that transforms the TinyMCE markup to valid HTML markup for the Bootstrap 5 accordion.
    Install via either pip or buildout.

    -   Install using pip.

        ```shell
        pip install collective.outputfilters.tinymceaccordion   
        ```

    -   Configure your local buildout file.

        ```cfg
        [instance]
        eggs += collective.outputfilters.tinymceaccordion
        ```
        
        Then run the command to install.
    
        ```shell
        bin/buildout
        ```
    
1.  Start your Plone instance.

    ```shell
    bin/instance fg
    ```

1.  Complete installation of the add-on by navigating to {menuselection}`Site Setup --> General --> Add-ons`, then clicking {guilabel}`Install` for `collective.outputfilters.tinymceaccordion`.

1.  Go to the {menuselection}`Site Setup --> General --> TinyMCE` control panel to manage TinyMCE settings.

1.  Under the {menuselection}`Plugins and Toolbar` tab, if not already checked, check {guilabel}`accordion` to enable the accordion plugin.

1.  Under the same tab, edit the `insert` menu by editing its `items` key as shown.

    ```json
    {
      "insert": {
        "title": "Insert",
        "items": "link media | template hr | accordion"
      },
    }
    ```

1.  Click the {guilabel}`Save` button to save your settings.

1.  In the {menuselection}`Security --> HTML filtering` control panel, ensure that you have the following tags under {guilabel}`Valid tags`.

    -   `button`
    -   `details`
    -   `summary`

1.  Also in the {menuselection}`Security --> HTML filtering` control panel, add a new attribute to {guilabel}`Custom attributes`, if not already present.

    -   `open`


## `z3c.form` and `plone.app.z3cform`

[`plone.app.z3cform`](https://github.com/plone/plone.app.z3cform) is the form widget integration package for [`z3c.form`](https://github.com/zopefoundation/z3c.form) in Plone.
This adds [Bootstrap 5](https://getbootstrap.com/) styling and mockup pattern options to all widgets.

In Plone 6.1 all Classic UI widget classes were moved to the module `plone.app.z3cform.widgets`.
The previous paths are marked as deprecated and will be removed in Plone 7.

The `BaseWidget` for patterns is refactored to the new `z3c.form` extendable attributes introduced in version 5.1 and doesn't use LXML anymore.
See https://github.com/zopefoundation/z3c.form/pull/116.
If you have customizations in your base pattern widget class, see the new implementation at https://github.com/plone/plone.app.z3cform/blob/e9d1ebf478e663d2da259cb9435927f7ad1ddb92/plone/app/z3cform/widgets/base.py.

`RelatedItemsWidget` is marked as deprecated.
The implementation for selecting related items, internal links and images in TinyMCE, or internal paths for collection criteria is now done with the new `ContentBrowserWidget`.
This introduces a new pattern `pat-contentbrowser` from mockup.
See the next section for details.


## `mockup` new pattern `pat-contentbrowser`

A new content browsing pattern [`pat-contentbrowser`](https://plone.github.io/mockup/pat/contenbrowser/) for Classic UI is now available.

This is a [Miller column browser](https://en.wikipedia.org/wiki/Miller_columns) implementation which replaces [`pat-relateditems`](https://plone.github.io/mockup/pat/relateditems/) seamlessly.
All basic options from `pat-relateditems` are implemented and behave the same as before.

Additionally `pat-contentbrowser` comes with some new features.

-   Keyboard navigation.
-   Multi-selection of items with {kbd}`Shift/Ctrl/CMD + click` combination.
    This comes in handy for selecting multiple related items in one step.
-   Uploading items to the current path.


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
Now it is available in core Plone as the recommended way for {doc}`creating a new Plone site </admin-guide/add-site>`.

```{seealso}
For more information about distribution concepts, see {doc}`/conceptual-guides/distributions`.
```

Distributions are optional.
If your project only uses the `Products.CMFPlone` Python package, you can still create a Plone site in the old way.
Consider, however, that doing so you will have the following differences when compared to using distributions.

-   The configuration form is simpler and shorter.
-   The created site has no content, and therefore no {guilabel}`News` or {guilabel}`Events` folders.
-   You must activate add-ons through the {guilabel}`Add-ons` control panel.

There are a few things you should consider when upgrading a project to, or making an add-on compatible with, Plone 6.1.

-   In general, you don't need to change anything.
    Your existing site will keep working.
    But adding a new site may change in the ways described earlier.
-   Do you want to use the `Products.CMFPlone` package (no distributions), either `plone.volto` or `plone.classicui` (one distribution), or `Plone` (two distributions)?
-   If your site uses Volto for the frontend, you will already have `plone.volto` as a dependency.
    This can stay the same.
-   If your site depends on the `Products.CMFPlone` package without the `Plone` or `plone.volto` packages, then the frontend is Classic UI.
    This can stay the same, but you may want to depend on `plone.classicui`.
    With that package you can still create a new site and have the same content as before.
-   If your site uses the `Plone` package, you will have the two new distributions available.
    This is fine.
    If you know you only need `plone.volto` or only need `plone.classicui`, you can switch to only one or the other.
    You can also limit the options for selecting a distribution by setting the environment variable `ALLOWED_DISTRIBUTIONS` with fewer options.
    Set `ALLOWED_DISTRIBUTIONS=default` for the distribution targeting the Volto frontend (`plone.volto`).
    Set `ALLOWED_DISTRIBUTIONS=classic` for the distribution with the Classic UI frontend (`plone.classicui`).
-   If you switch from `Plone` to `plone.volto` or `plone.classicui`, you might want to install extra core add-ons, for example `plone.app.upgrade` or `plone.app.caching`.
-   If your add-on is only for Volto, you might want to add `plone.volto` as a dependency.
-   If your add-on is only for Classic UI, you might want to add `plone.classicui` as a dependency.
    Note though that `plone.classicui` is not available for Plone 6.0.
