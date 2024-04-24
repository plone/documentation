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
