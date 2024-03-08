---
myst:
  html_meta:
    "description": "Upgrading to Plone 6.0"
    "property=og:description": "Upgrading to Plone 6.0"
    "property=og:title": "Upgrading to Plone 6.0"
    "keywords": "Upgrading, Plone 6"
---

(backend-upgrade-plone-v60-label)=

# Upgrading Plone 5.2 to 6.0

Plone 6.0 has seen the following major changes.
Some may require changes in your setup.


(v60-removed-portal_quickinstaller-label)=

## Removed `portal_quickinstaller`

Plone no longer ships with the `portal_quickinstaller` tool (`CMFQuickInstallerTool`).
In existing sites, the standard upgrade will remove the tool.

This is the final step in a deprecation path that started in Plone 5.1.

Documentation of how to switch to `GenericSetup` and the new installer, can be seen in {doc}`upgrade-addons-to-51`.

```{seealso}
[PLIP 1775](https://github.com/plone/Products.CMFPlone/issues/1775)
```


(v60-dexterity-site-root-label)=

## Dexterity site root

For content types, in Plone 4 and 5 you had the option to use the old Archetypes or the new Dexterity framework.
The Plone site root object was neither: it was in its own class.
In Plone 6, the site root itself is a Dexterity object.

When you upgrade a site from Plone 5.2 to 6.0, at first you will see an empty site root.
Do not panic.
😱
Your content is only temporarily invisible.
Perform the standard migration via the `@@plone-upgrade` view, and your content will be visible again.

```{seealso}
[PLIP 2454](https://github.com/plone/Products.CMFPlone/issues/2454)
```


(v60-volto-label)=

## Volto

Plone 6 ships with a new React-based frontend, Volto.
When you use the `Plone` package in your project, you will get the `plone.volto` integration package.
This package prepares your Plone site's backend as a REST API.

```{note}
The classic integrated frontend which is called "Classic UI" is still available if you are not ready for the new separate frontend.
If you choose to use Classic UI, then do not use the `plone.volto` package.
```

To learn how to modify an existing Plone site to run with Volto, please read {doc}`migrate-to-volto`.

```{seealso}
[PLIP 2703](https://github.com/plone/Products.CMFPlone/issues/2703)
```


(v60-archetypes-label)=

## Archetypes

The deprecated Archetypes content types framework is no longer supported.
Add-ons that define a content type must use Dexterity instead.

```{seealso}
[PLIP 2775](https://github.com/plone/Products.CMFPlone/issues/2775)
```


(v60-deprecated-views-label)=

## Some deprecated views have been removed

In Plone 6 some legacy view aliases have been removed.
You can replace them with the new ones based on the following table:

| Legacy name         | New name     |
|---------------------|--------------|
| `all_content`         | `full_view`    |
| `atct_album_view`     | `album_view`   |
| `collection_view`     | `listing_view` |
| `folder_album_view`   | `album_view`   |
| `folder_full_view`    | `full_view`    |
| `folder_listing`      | `listing_view` |
| `folder_summary_view` | `summary_view` |
| `folder_tabular_view` | `tabular_view` |
| `standard_view`       | `listing_view` |
| `thumbnail_view`      | `album_view`   |

```{seealso}
[plone/plone.app.contenttypes issue #621](https://github.com/plone/plone.app.contenttypes/pull/621)
```

(v60-no-temp_folder-tempstorage)=

## No more `temp_folder` or `tempstorage`

The `temp_folder` object in the Zope root is no longer created by default.
If the object is there, but it is broken, the standard Plone upgrade procedure will remove it.

For now, you must explicitly disable the `temp_folder` if you use buildout:

```ini
[instance]
recipe = plone.recipe.zope2instance
zodb-temporary-storage = off
```

```{seealso}
[plone/Products.CMFPlone issue #2957](https://github.com/plone/Products.CMFPlone/issues/2957)
```


(v60-templates-bootstrap-5-label)=

## Changed templates to Twitter Bootstrap 5 markup

All templates in core Plone have been updated to use Twitter Bootstrap 5 markup.
Add-on authors are encouraged to do the same.
If you have customized a core template, you should check if your change is still needed, and update it to fit the new markup.
Any CSS and JavaScript that relies on a specific structure, or certain IDs or classes, should be checked as well.

```{seealso}
[PLIP 2967](https://github.com/plone/Products.CMFPlone/issues/2967)
```


(v60-zope-5-label)=

## Zope 5

Plone 6.0 means we move from Zope 4 to 5.
This drops support for Python 2.7, drops `ZServer`, and removes deprecated code.

```{seealso}
[Zope 5.0a1](https://zope.readthedocs.io/en/latest/changes.html#a1-2020-02-28)
```

Some imports may need to change.
Add-on authors should check on Plone 5.2 if their code runs without any deprecation warnings from Zope 4.
If no warnings are shown, the add-on should run fine on Zope 5.

```{seealso}
[PLIP 3058](https://github.com/plone/Products.CMFPlone/issues/3058)
```


(v60-barceloneta-lts-label)=

## Modernize Plone Classic UI theme (Barceloneta)

The standard theme in Classic UI was updated to Bootstrap 5, CSS variables, and an icon library.
If you have a theme that builds on Barceloneta, you most likely need various changes.

It may be best to start with a fresh theme, and try to keep the changes minimal.
The training documentation lists {doc}`three possible theming strategies <theming_plone_5/index>`:

-   Create a theme based on Barceloneta.
-   Create a theme from scratch.
-   Create a theme based on Diazo.

```{seealso}
[PLIP 3061](https://github.com/plone/Products.CMFPlone/issues/3061)
```


(v60-python-label)=

## Python

You may need to use a newer Python version.
Supported Python versions are 3.8, 3.9, 3.10, and 3.11.
We recommend the most recent version.
See https://www.python.org/downloads/ for which Python version is still supported by the Python community.

```{seealso}
[PLIP 3229](https://github.com/plone/Products.CMFPlone/issues/3229)
```


(v60-plone.api.relation-label)=

## `plone.api.relation`

The `plone.api` package now has a `relation` module.
Add-on authors may want to use this to get, create, or delete relations.

```{seealso}
[PLIP 3137](https://github.com/plone/Products.CMFPlone/issues/3137)
```


(v60-mockup-resource-registry-label)=

## Mockup and resource registry redone

Mockup contains the source of most Classic UI Plone JavaScript.
The compiled version is in `plone.staticresources`.

Mockup is now based on [Patternslib 4](https://patternslib.com/).
It uses ES6 module imports instead of RequireJS.
Add-ons for Classic UI Plone that use JavaScript should be updated to use ES6 modules as well.

The resource registries and their control panel have been simplified.
Add-ons for Classic UI Plone only need to register bundles, not individual resources.

```{seealso}
[PLIP 3211](https://github.com/plone/Products.CMFPlone/issues/3211)
```


(v60-relations-control-panel-label)=

## Relations control panel

Plone 6 has a new control panel for relations, `@@inspect-relations`.
As a Manager, you may want to use this control panel to look for and fix possible problems.

```{seealso}
[PLIP 3232](https://github.com/plone/Products.CMFPlone/pull/3232)
```


(v60-deprecated-unicode-property-types-label)=

## Deprecated Unicode property types

Zope 5 has deprecated the Unicode property types `ustring`, `ulines`, `utext`, and `utokens`.
If you use these in your add-on, you should switch to their standard variants `string`, `lines`, `text`, and `tokens`.
These behave exactly the same on Python 3.
Plone has an upgrade step that goes through all objects in the site, replacing the deprecated properties with the default ones.
You should avoid adding them to your code.

```{seealso}
[plone/Products.CMFPlone issue #3305](https://github.com/plone/Products.CMFPlone/issues/3305)
```


(v60-autoinclude-label)=

## `autoinclude`

We have replaced `z3c.autoinclude` with `plone.autoinclude`.
Both are used by add-ons (Python packages) to signal, with an entry point, that Plone must load the ZCML of the add-on.
In most cases, the existing entry point can stay the same.
For example in `setup.py`:

```python
entry_points="""
[z3c.autoinclude.plugin]
target = plone
"""
```

When your package name differs from your module name, you need to specify a differently named entry point.
When your module is named `example.alternative`, create this entry point:

```python
entry_points="""
[plone.autoinclude.plugin]
target = plone
module = example.alternative
"""
```

The `includeDependencies` directive is no longer supported.
It was already recommended not to use this directive, as it is too implicit.
In the ZCML files of your add-on, search for `includeDependencies`.
Replace all of its instances by explicitly loading any ZCML from other packages used by the add-on.
Here is a sample change from [`dexterity.membrane`](https://github.com/collective/dexterity.membrane/pull/60):

```diff
-  <includeDependencies package="." />
+  <include package="Products.membrane" />
```

The same change is needed for the no longer supported `includeDependenciesOverrides` directive, which may be used in `overrides.zcml`.

```{seealso}
-   [PLIP 3339](https://github.com/plone/Products.CMFPlone/issues/3339)
-   [`plone.autoinclude`](https://github.com/plone/plone.autoinclude) documentation
```


(v60-dexteritytextindexer-label)=

## `collective.dexteritytextindexer` merged

You can mark fields of a content type as searchable.
You can then find an object in the search form by using any text from these fields.
For this to work, you need to enable the `plone.textindexer` behavior on the content type.
For more information, see {ref}`backend-indexing-textindexer-label`.

In earlier Plone versions, this feature was available in the `collective.dexteritytextindexer` package.
This was merged into Plone 6.0 core, with most code ending up in `plone.app.dexterity`.

If you have an add-on or custom code that uses the old package, then this must be upgraded.
These are the needed changes:

- Remove `collective.dexteritytextindexer` from the `install_requires` in `setup.py`.
- Update the Python code of your content type code, like this:

```diff
-from collective import dexteritytextindexer
+from plone.app.dexterity import textindexer
 from plone.app.textfield import RichText
 from plone.supermodel import model
...
 class IExampleType(model.Schema):
-    dexteritytextindexer.searchable("text")
+    textindexer.searchable("text")
     text = RichText(...)
```

- In the GenericSetup xml of your content type, use the new behavior:

```diff
 <property name="behaviors" purge="false">
-  <element value="collective.dexteritytextindexer" />
-  <element value="collective.dexteritytextindexer.behavior.IDexterityTextIndexer" />
+  <element value="plone.textindexer" />
 </property>
```

- Search for any leftovers of `collective.dexteritytextindexer` in your code and replace it.

The in-place upgrade to Plone will replace the two versions of the old behavior with the new one in all content types.

```{seealso}
[plone/Products.CMFPlone issue #2780](https://github.com/plone/Products.CMFPlone/issues/2780)
```


(v60-plone-base-label)=

## `plone.base` package

Within the Plone code base there are circular dependencies.
Package A uses package B and package B uses package A.
Specifically, `Products.CMFPlone` is the main package of Plone where everything comes together.
`Products.CMFPlone` depends on a lot of Plone packages.
But these packages often import code from `Products.CMFPlone`.
This is done in such a way that it works, but it creates an unclear situation and makes it hard to debug errors when they occur in this implicit dependency chain.

The solution in Plone 6.0 was to create a package called `plone.base`.
Some often used code from `Products.CMFPlone` and other packages was moved here.
Backwards compatibility imports were kept in place, so this should not cause any breakage in add-ons.
You *will* get warnings in your logs, unless you have silenced them.
For example when your code has `from Products.CMFPlone.utils import base_hasattr` you will see:

```console
DeprecationWarning: base_hasattr is deprecated.
Import from plone.base.utils instead (will be removed in Plone 7)
```

If the add-on only needs to support Plone 6, you can change the code like this:

```diff
- from Products.CMFPlone.utils import base_hasattr
+ from plone.base.utils import base_hasattr
```

If the add-on needs to support both Plone 5 and 6, this works and avoids the warning:

```python
try:
    from plone.base.utils import base_hasattr
except ImportError:
    # BBB for Plone 5
    from Products.CMFPlone.utils import base_hasattr
```

```{seealso}
[plone/Products.CMFPlone issue #3395](https://github.com/plone/Products.CMFPlone/issues/3395)
```


(v60-modern-image-scales-label)=

## Support for modern image scales

In Plone 5.2 the following image scales were available, with scale name, width, and height:

```text
large 768:768
preview 400:400
mini 200:200
humb 128:128
tile 64:64
icon 32:32
listing 16:16
```

Plone 6.0 changes them:

```text
huge 1600:65536
great 1200:65536
larger 1000:65536
large 800:65536
teaser 600:65536
preview 400:65536
mini 200:65536
thumb 128:128
tile 64:64
icon 32:32
listing 16:16
```

- The biggest scale now has a width of 1600 instead of 768.
- The `large` scale was made slightly bigger: from 768 to 800.
- All scales above `mini` have a height of 65536.
  This does not mean you get an extremely high image.
  It means only the width is taken into account when resizing the image.
  This is a better fit for most modern themes.

```{note}
The standard Plone upgrade only adds the completely new scales: `huge`, `great`, `larger`, and `teaser`.
It leaves the other scales untouched.
This is to avoid strange differences between old and new images.
For example, old images would otherwise have a large scale with width 768, where for new images this would be width 800.
```

```{seealso}
[plone/Products.CMFPlone issue #3279](https://github.com/plone/Products.CMFPlone/issues/3279)
```


(v60-pre-scaling-label)=

## Image pre-scaling

In Plone 6, we have made a split between generating a URL for an image scale and actually scaling the image.
Why would you want this?

As an add-on author, you create a template and you want to show an uploaded image with the preview scale.
The code would be like this:

```xml
<img tal:define="images context/@@images"
     tal:replace="structure python:images.tag('image', scale='preview')" />
```

In Plone 5 this creates a scale of the image, using the Pillow imaging library.
In Plone 6, the scaled image is not yet created at this point.
The scaled image is only created when the browser actually requests the image.

This is good, because for various reasons, the browser may never actually ask for this scaled image.
For example, the browser may be on a mobile phone with the images turned off to prevent using costly band width.
Also, when the tag contains source sets for HiDPI or picture variants, the browser may see five possible images and only choose to download one of them.

In Plone 6, when generating a tag for, as in this case, the `preview` scale, a unique URL is generated, and information for this scale is pre-registered.
Only when the browser requests the scaled image at this URL, does Plone generate the scale.
This avoids generating image scales that never get used.

This performance improvement makes two other image improvements possible.
These follow in the sections directly below.

Add-on authors do not *have* to change anything.
But it is a good idea to check how you are using images, otherwise you miss out on this improvement.
If you call the `tag` method like above, you are good.
If you use the `scale` method and then use its `tag` method, then you should change:

```diff
  <img tal:define="images context/@@images"
-      tal:replace="structure python:images.scale('image', scale='preview').tag()" />
+      tal:replace="structure python:images.tag('image', scale='preview')" />
```

Alternatively, you can explicitly use the new `pre` argument, but this will fail on Plone 5:

```xml
<img tal:define="images context/@@images"
     tal:replace="structure python:images.scale('image', scale='preview', pre=True).tag()" />
```

```{note}
There now is an image test page that shows several scales of an image, in various modes.
In your browser, go to an image, and add `/@@images-test` to the end of the URL.
```

```{seealso}
- [plone/plone.scale PR 57](https://github.com/plone/plone.scale/pull/57)
- [plone/plone.namedfile PR 113](https://github.com/plone/plone.namedfile/pull/113)
```


(v60-responsive-image-support-label)=

## Responsive image support

Responsive image support was added with picture tags.
For more information, see {ref}`classic-ui-images-responsive-image-support`.

In an add-on nothing needs to be changed.
But if you want to use the responsive image support, you should use the `picture` method:

```diff
  <img tal:define="images context/@@images"
-      tal:replace="structure python:images.tag('image', scale='preview')" />
+      tal:replace="structure python:images.picture('image', picture_variant='small')" />
```



(v60-image-scale-catalog-label)=

## Store image scale info in catalog metadata

When you add or edit an image, Plone 6 pre-registers all scales and stores information about them in the portal catalog.
The catalog brain of an image then has all the needed information about each scale, especially the unique URL, width, and height.
This is used on lists of images to be able to show a scale in a tag without waking up the image objects from the database.
In other words, this speeds up pages that contain lots of images.

Add-on authors do not have to change anything, as this happens automatically.
If you have a very special use case, you can influence this with some new adapters.

````{note}
When upgrading your Plone Site to Plone 6.0, the in-place migration finds all images in your site.
It then adds the scale information to the catalog.
This may take a long time.
You can disable this with an environment variable:

```shell
export UPDATE_CATALOG_FOR_IMAGE_SCALES=0
```

In that case, you are advised to add the `image_scales` column manually to the catalog later.
````

```{seealso}
[plone/plone.app.upgrade PR 292](https://github.com/plone/plone.app.upgrade/pull/292)
```


(v60-tinymce-label)=

## New version of TinyMCE

Plone 6 ships with a new version of TinyMCE.
While Plone 5.2 ships with TinyMCE 4.7, Plone 6.0 ships with TinyMCE 5.10.
The TinyMCE integration `pat-tinymce` has also changed, but the configuration options have been almost kept the same and are likely to be compatible with your existing installation.
The configuration changes are:

-   Added configuration options `text.enableImageZoom`, `defaultSrcset`, `imageCaptioningEnabled`, and `tiny.language`.
-   Removed configuration option `imageScales`.
-   Option values changed for `imageClasses`.


### TinyMCE templates

In Plone 6, the TinyMCE template plugin is built-in and can be enabled via a checkbox.
Whereas in Plone 5, you had to enable the template plugin as an external plugin via the `custom_plugins` configuration option.
The template registration is the same as before, but in Plone 6 your templates need to have a `description`.
Otherwise TinyMCE will throw a JavaScript error, and the templates won't be usable at all.

The following example {file}`registry.xml` may be used for configuring TinyMCE with some templates.

```xml
  <records interface="Products.CMFPlone.interfaces.controlpanel.ITinyMCESchema"
           prefix="plone">
    <value key="plugins" purge="False">
      <element>template</element>
    </value>
    <value key="custom_plugins" purge="True">
      <!-- Remove the old TinyMCE template plugin -->
    </value>
    <value key="templates">
        [
            {
                "title": "Template 1",
                "description": "This is an example template",
                "url": "++plone++my.site/template1.html"
            },
            {
                "title": "Template 2",
                "description": "This is another example template",
                "url": "++plone++my.site/template2.html"
            }
        ]
    </value>
  </records>
```

Please make sure you write valid JSON for the `template` option.

```{seealso}
See also the [TinyMCE 4 to 5 upgrade guide](https://www.tiny.cloud/docs/migration-from-4x/).
```

## Viewlets

Plone 6.0 renames various viewlets or moves them to a different viewlet manager.
This is because some viewlet names contained the name of a viewlet manager.
This didn't always match the name of their actual viewlet manager, especially after moving them.
Plone 6.0 removes such references from the viewlet names to avoid confusion.

-   Plone 6.0 removes the `plone.header` viewlet from `plone.portaltop` manager, making it empty.
-   Plone 6.0 renames the `plone.abovecontenttitle.documentactions` viewlet to `plone.documentactions`, and moves it from manager `plone.belowcontentbody` to `plone.belowcontent`.
-   Plone 6.0 renames the `plone.abovecontenttitle.socialtags` viewlet to `plone.socialtags`.
    It remains in manager `plone.abovecontenttitle`.
-   Plone 6.0 renames the `plone.belowcontentbody.relateditems` viewlet to `plone.relateditems`.
    It remains in manager `plone.belowcontentbody`.
-   Plone 6.0 removes the `plone.manage_portlets_fallback` viewlet from the `plone.belowcontent` manager.
-   Plone 6.0 renames the `plone.belowcontenttitle.documentbyline` viewlet to `plone.documentbyline`.
    It remains in manager `plone.belowcontenttitle`.
-   Plone 6.0 renames the `plone.belowcontenttitle.keywords` viewlet to `plone.keywords`, and moves it from manager `plone.belowcontent` to `plone.belowcontentbody`.
-   Plone 6.0 adds the `plone.rights` viewlet in manager `plone.belowcontentbody`.

The names in the following table have had the namespace `plone.` removed from them for display purposes only.
In your code, you should use the object's `plone.` namespace as a prefix.
This table shows the same information, but in tabular form.

```{table} Viewlet changes from 5.2 to 6.0

| 5.2 viewlet name | 5.2 viewlet manager | 6.0 viewlet name | 6.0 viewlet manager |
| ---------------- | ------------------- | ---------------- | ------------------- |
| `header` | `portaltop` | | `portaltop` |
| `abovecontenttitle.documentactions` | `belowcontentbody` | `documentactions` | `belowcontent` |
| `abovecontenttitle.socialtags` | `abovecontenttitle` | `socialtags` | `abovecontenttitle` |
| `belowcontentbody.relateditems` | `belowcontentbody` | `relateditems` | `belowcontentbody` |
| `manage_portlets_fallback` | `belowcontent` | | `belowcontent` |
| `belowcontenttitle.documentbyline` | `belowcontenttitle` | `documentbyline` | `belowcontenttitle` |
| `belowcontenttitle.keywords` | `belowcontent` | `keywords` | `belowcontentbody` |
| | `belowcontentbody` | `rights` | `belowcontentbody` |
```

Plone 6.0 makes changes to two viewlet managers:

-   Plone 6.0 removes the `plone.documentactions` (`IDocumentActions`) viewlet manager.
    In Plone 5.2 it was already empty.
-   Plone 6.0 adds the `plone.belowcontentdescription` (`IBelowContentDescription`) viewlet manager.
    By default this has no viewlets.

One final change is that Plone 6.0 moves the `plone.footer` viewlet from `plone.app.layout/viewlets` to `plone.app.portlets`.
The viewlet remains in manager `plone.portalfooter`.
It renders the portlets from the `plone.footerportlets` portlet manager.

## Boolean fields

Since `zope.schema==6.1.0` all `zope.schema.Bool` fields need to have a `required=False` attribute,
otherwise, you will not be able to save the form without marking the checkbox, which effectively turns that field to be always `True`.
