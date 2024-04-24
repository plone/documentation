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


## TinyMCE upgraded

Plone 6.0 uses TinyMCE, a rich text editor for websites.
TinyMCE 5 reached its end of support on April 20, 2023.
For Plone 6.1, TinyMCE has been upgraded from version 5 to 7.

```{seealso}
-   [How to upgrade TinyMCE 5 to TinyMCE 6](https://www.tiny.cloud/blog/upgrade-to-tinymce-6/)
-   [Upgrading TinyMCE](https://www.tiny.cloud/docs/tinymce/latest/upgrading/)
```

### Enable the TinyMCE accordion plugin

Go to the controlpanel to manage TinyMCE settings

Enable the Plugin in the controlpanel

Add a menu entry `accordion` for TinyMCE in the controlpanel 

```{code-block} json
{
  "insert": {
    "title": "Insert",
    "items": "link media | template hr | accordion"
  },
}
```

Check your settings in the HTML filter controlpanel

add two new tags to `valid tags`

- `summary`
- `details`

add a new attribute to `custom_attributes`

- `open`

for a transform to valid bootstrap5 accordion markup use an outputfilter

```{seealso}
-   [Addon collective.outputfilters.tinymceaccordion](https://github.com/collective/collective.outputfilters.tinymceaccordion)
```