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
Documentation on how to switch to GenericSetup and the new installer, can be seen in the old [Plone 5.1 upgrade guide](https://docs.plone.org/develop/addons/upgrade-to-51.html#installation-code).

See [PLIP 1775](https://github.com/plone/Products.CMFPlone/issues/1775).


(v60-dexterity-site-root-label)=

## Dexterity site root

For content types, in Plone 4 and 5 you had the option to use the old Archetypes or the new Dexterity framework.
The Plone Site root object was neither: it was in its own class.
In Plone 6, the site root itself is a Dexterity object.

When you upgrade a site from Plone 5.2 to 6.0, at first you will see an empty site root.
Do not panic.
Your contents are only temporarily invisible.
Perform the standard migration via the `@@plone-upgrade` view and your content will be visible again.

See [PLIP 2454](https://github.com/plone/Products.CMFPlone/issues/2454).


(v60-volto-label)=

## Volto

Plone 6 ships with a new NodeJS frontend: Volto.
When you use the `Plone` package in your project, you will get the `plone.volto` integration package.
This package prepares your Plone Site as a REST API.

```{note}
The classic integrated frontend which is called "Classic UI" is still available if you are not ready for the new separate frontend.
If you choose to use Classic UI, then do not use the `plone.volto` package.
```

To learn how to modify an existing Plone site to run with Volto, please read {doc}`migrate-to-volto`.


See [PLIP 2703](https://github.com/plone/Products.CMFPlone/issues/2703).


(v60-archetypes-label)=

## Archetypes

The deprecated Archetypes contenttypes framework is no longer supported.
Add-ons that define a contenttype must use Dexterity instead.

See [PLIP 2775](https://github.com/plone/Products.CMFPlone/issues/2775).


(v60-deprecated-views-label)=

## Some deprecated views have been removed

In Plone 6 some legacy view aliases have been removed.
You can replace them with the new ones based on the following table:

| Legacy name         | New name     |
|---------------------|--------------|
| all_content         | full_view    |
| atct_album_view     | album_view   |
| collection_view     | listing_view |
| folder_album_view   | album_view   |
| folder_full_view    | full_view    |
| folder_listing      | listing_view |
| folder_summary_view | summary_view |
| folder_tabular_view | tabular_view |
| standard_view       | listing_view |
| thumbnail_view      | album_view   |

See [plone/plone.app.contenttypes#621](https://github.com/plone/plone.app.contenttypes/pull/621).


(v60-no-temp_folder-tempstorage)=

## No more temp_folder / tempstorage

The `temp_folder` object in the Zope root is no longer created by default.
If the object is there, but it is broken, the standard Plone upgrade procedure will remove it.

For now you must explicitly disable the `temp_folder` if you use buildout:

```ini
[instance]
recipe = plone.recipe.zope2instance
zodb-temporary-storage = off
```

See [issue 2957](https://github.com/plone/Products.CMFPlone/issues/2957).


(v60-templates-bootstrap-5-label)=

## Changed Templates to Bootstrap 5 Markup

All templates in core Plone have been updated to use Bootstrap 5 markup.
Add-on authors are encouraged to do the same.
If you have customized a core template, you should check if your change is still needed, and update it to fit the new markup.
Any CSS and JavaScript that relies on a specific structure, or certain IDs or classes, should be checked as well.

See [PLIP 2967](https://github.com/plone/Products.CMFPlone/issues/2967).


(v60-zope-5-label)=

## Zope 5

Plone 6.0 means we move from Zope 4 to 5.
This drops support for Python 2.7, drops ZServer, and removes deprecated code.
See [Zope 5.0a1](https://zope.readthedocs.io/en/latest/changes.html#a1-2020-02-28).

Some imports may need to change.
Add-on authors should check on Plone 5.2 if their code runs without any deprecation warnings from Zope 4.
If no warnings are shown, the add-on should run fine on Zope 5.

See [PLIP 3058](https://github.com/plone/Products.CMFPlone/issues/3058).


(v60-barceloneta-lts-label)=

## Modernize Plone default theme (Barceloneta LTS)

The standard theme in Classic UI was updated to Bootstrap 5, CSS variables, and an icon library.
If you have a theme that builds on Barceloneta, you most likely need various changes.

It may be best to start with a fresh theme, and try to keep the changes minimal.
The training documentation lists {ref}`three possible theming strategies <training:theming-label>`:

- Create a theme based on Barceloneta
- Create a theme from scratch
- Create a theme based on Diazo

See [PLIP 3061](https://github.com/plone/Products.CMFPlone/issues/3061).


(v60-python-label)=

## Python

You may need to use a newer Python version.
Supported Python versions are 3.8, 3.9 and 3.10.
We recommend the most recent version.
See https://www.python.org/downloads/ for which Python version is still supported by the Python community.

See [PLIP 3229](https://github.com/plone/Products.CMFPlone/issues/3229).


(v60-plone.api.relation-label)=

## `plone.api.relation`

The `plone.api` package now has a `relation` module.
Add-on authors may want to use this to get, create, or delete relations.

See [PLIP 3137](https://github.com/plone/Products.CMFPlone/issues/3137).


(v60-mockup-resource-registry-label)=

## Mockup and resource registry redone

Mockup contains the source of most Classic Plone JavaScript.
The compiled version is in `plone.staticresources`.

Mockup is now based on [Patternslib 4](https://patternslib.com/).
It uses ES6 module imports instead of RequireJS.
Add-ons for Classic Plone that use JavaScript should be updated to use ES6 modules as well.

The resource registries and their control panel have been simplified.
Add-ons for Classic Plone only need to register bundles, not individual resources.

See [PLIP 3211](https://github.com/plone/Products.CMFPlone/issues/3211).


(v60-relations-control-panel-label)=

## Relations control panel

Plone 6 has a new control panel for relations, `@@inspect-relations`.
As Manager you may want to use this control panel to look for and fix possible problems.

See [PLIP 3232](https://github.com/plone/Products.CMFPlone/pull/3232).


(v60-deprecated-unicode-property-types-label)=

## Deprecated Unicode property types

Zope 5 has deprecated the Unicode property types `ustring`, `ulines`, `utext`, and `utokens`.
If you use these in your add-on, you should switch to their standard variants `string`, `lines`, `text`, and `tokens`.
These behave exactly the same on Python 3.
Plone has an upgrade step that goes through all objects in the site, replacing the deprecated properties with the default ones.
You should avoid adding them to your code.

See [issue 3305](https://github.com/plone/Products.CMFPlone/issues/3305).


(v60-autoinclude-label)=

## autoinclude

We have replaced `z3c.autoinclude` with `plone.autoinclude`.
Both are used by add-ons (Python packages) to signal with an entry point that Plone must load the ZCML of the add-on.
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

See [PLIP 3339](https://github.com/plone/Products.CMFPlone/issues/3339).
Also see the [`plone.autoinclude`](https://github.com/plone/plone.autoinclude) documentation.
