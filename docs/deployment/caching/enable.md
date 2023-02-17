---
myst:
  html_meta:
    "description": "Caching Plone: Enable cache support"
    "property=og:description": "Enabling caching support for Plone"
    "property=og:title": "Caching Plone: Enabling support"
    "keywords": "Plone, deployment, automation, caching"
---

(caching-installation-label)=

# Installation

Caching support is implemented by the package `plone.app.caching`, which is already shipped as a dependency of the *Plone* package, and it should be available on all Plone installations.

Even though Caching support is available in Plone, it is **not enabled by default**, although it is highly recommended to configure caching for every new Plone site in production.

## Enable Caching

Under the Advanced header, look for the `Caching` control panel -- currently only supported on the Classic UI -- and select it.

```{image} /_static/caching/ControlPanel-01.png
:alt: Plone Control Panel (Classic UI)
```

In the Caching control panel, the tab `Change settings` is selected and inside of it the tab `Global settings` have the option to **Enable caching** (disable by default)

```{image} /_static/caching/ControlPanel-02.png
:alt: Caching Control Panel with caching disabled
```

To enable caching, just click the checkbox:

```{image} /_static/caching/ControlPanel-03.png
:alt: Caching Control Panel with caching enabled
```

## Troubleshooting

When the Caching control panel is not there, there can be various reasons for this:

- If your installation does not load the `Plone` package, but only `Products.CMFPlone`, then `plone.app.caching` is not included.
- If the package *is* included, but you add a Plone Site using the advanced form and disable caching, then the control panel is not there.

If you want to install it in an existing Plone Site:

1. Make sure the package is available in the Plone instance, by adding `plone.app.caching` or `Plone` to your installation.
2. From the Plone Site Setup go to the ZMI (Zope Management Interface).
3. Go to ``portal_setup``, and then to the Import tab.
4. Select the HTTP caching support profile, perhaps easiest by id: `profile-plone.app.caching:default`.
5. Click 'Import all steps'.
