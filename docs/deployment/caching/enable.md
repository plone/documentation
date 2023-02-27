---
myst:
  html_meta:
    "description": "How to enable cache support in Plone"
    "property=og:description": "How to enable cache support in Plone"
    "property=og:title": "How to enable cache support in Plone"
    "keywords": "Plone, deployment, automation, caching, cache"
---

(caching-installation-label)=

# Installation

Caching support is implemented by the package `plone.app.caching`.
It is already installed as a dependency of the [Plone](https://github.com/plone/plone) package.
It should be available on all Plone installations.

Even though cache support is available in Plone, it is **not enabled by default**.
It is highly recommended to configure caching for every new Plone site in production.


(import-a-caching-profile-label)=

## Import a caching profile

Importing a caching profile is currently only supported in the Classic UI.

We recommend that you import a caching profile to start.
You can always modify the profile later as needed.

As an administrator, navigate to {guilabel}`Site Setup`.
Under the {guilabel}`Advanced` heading or navigation item, select the <img alt="Caching" src="/_static/caching/icon-caching.svg" class="inline"> {guilabel}`Caching` control panel.

````{card}
```{image} /_static/caching/caching-disabled.png
:alt: Caching Control Panel with caching disabled
:target: /_static/caching/caching-disabled.png
```
+++
_Caching Control Panel with caching disabled_
````

From here click either the helpful link in the blue information box {guilabel}`importing a preconfigured set of caching rules` or the {guilabel}`Import settings` tab.
You will see the {guilabel}`Import caching profiles` control panel.

````{card}
```{image} /_static/caching/import-caching-profiles.png
:alt: Import caching profiles control panel
:target: /_static/caching/import-caching-profiles.png
```
+++
_Import caching profiles control panel_
````

Select options that are appropriate for your caching environment.

{guilabel}`With caching proxy`
:   Settings useful for setups with a caching proxy such as Varnish or a CDN

{guilabel}`Without caching proxy`
:   Settings useful for setups without a caching proxy such as Varnish or a CDN

{guilabel}`Take a snapshot of the site prior to importing new setting.`
:   This allows rollback to a previous state via the `portal_setup` tool.


(enable-caching-label)=

## Enable caching

Enabling of caching is currently only supported in the Classic UI.

As an administrator, navigate to {guilabel}`Site Setup`.
Under the {guilabel}`Advanced` heading or navigation item, select the <img alt="Caching" src="/_static/caching/icon-caching.svg" class="inline"> {guilabel}`Caching` control panel.

````{card}
```{image} /_static/caching/advanced-caching-navigation.png
:alt: Plone Classic UI Caching Control Panel in the navigation
:target: /_static/caching/advanced-caching-navigation.png
```
+++
_Caching Control Panel in the navigation_
````

````{card}
```{image} /_static/caching/advanced-caching-heading.png
:alt: Plone Classic UI Caching Control Panel under a heading
:target: /_static/caching/advanced-caching-heading.png
```
+++
_Caching Control Panel under a heading_
````

In the Caching control panel, the tab {guilabel}`Change settings` is selected by default.
Inside of it, the tab {guilabel}`Global settings` has the option to {guilabel}`Enable caching`.
This setting is disabled by default.

````{card}
```{image} /_static/caching/caching-disabled.png
:alt: Caching Control Panel with caching disabled
:target: /_static/caching/caching-disabled.png
```
+++
_Caching Control Panel with caching disabled_
````

To enable caching, click the checkbox, and click the {guilabel}`Save` button.

````{card}
```{image} /_static/caching/caching-enabled.png
:alt: Caching Control Panel with caching enabled
:target: /_static/caching/caching-enabled.png
```
+++
_Caching Control Panel with caching enabled_
````


## Troubleshooting

When the caching control panel is not there, there can be various reasons for this:

-   If your installation does not load the `Plone` package, but only `Products.CMFPlone`, then `plone.app.caching` is not included.
-   If the package *is* included, but you add a Plone Site using the advanced form and disable caching, then the control panel is not there.

If you want to install it in an existing Plone Site:

1.  Make sure the package is available in the Plone instance by adding `plone.app.caching` or `Plone` to your installation.
2.  From the Plone Site Setup, under the {guilabel}`Advanced` heading or navigation item, select the <img alt="Management Interface" src="/_static/caching/icon-management-interface.svg" class="inline"> {guilabel}`Management Interface` control panel.
3.  Click {guilabel}`portal_setup`, and then click the {guilabel}`Import` tab.
4.  Select the profile by title {guilabel}`HTTP caching support`, or by id {guilabel}`profile-plone.app.caching:default`.
5.  Select {guilabel}`Apply new profiles. Run upgrade steps for already applied profiles. Recommended.`.
6.  Click the {guilabel}`Import all steps` button.

````{card}
```{image} /_static/caching/caching-import-configuration.png
:alt: Site Configuration Full Import for HTTP caching support
:target: /_static/caching/caching-import-configuration.png
```
+++
_Site Configuration Full Import for HTTP caching support_
````
