---
myst:
  html_meta:
    "description": "Through-the-web (TTW) theme customization in Plone 6 Classic UI"
    "property=og:description": "Through-the-web (TTW) theme customization in Plone 6 Classic UI"
    "property=og:title": "Through-the-web (TTW) theme customization in Plone 6 Classic UI"
    "keywords": "Plone 6, Classic UI, Through-the-web, TTW, theme, customization"
---

(classic-ui-through-the-web-label)=

# Through-the-web (TTW) theme customization

```{todo}
This page is only an outline and needs a lot of work.
See https://github.com/plone/documentation/issues/1645
```

TTW customization is useful when you need to make small CSS changes.
Theme changes can be made via control panels or by updating Plone 6 Classic UI's `custom.css`.
Other theming methods should be used for larger customizations or entire website designs.


(classic-ui-through-the-web-control-panels-label)=

## Control panels

You can make the following changes through control panels.

* Logo
* Favicon
* Custom CSS in `custom.css`

With `custom.css`, you can make custom styles without compilation.
It is shipped as the last resource after all other CSS files.
It can be used to override default CSS, sometimes with the use of the CSS property `!important` or specific CSS selectors.


```{todo}
Provide usage.
Provide navigation through {menuselection}`Site Setup --> Theming` or {guilabel}`Button Name`.
Add screenshots.
```


(classic-ui-through-the-web-css-variables-label)=

## CSS variables

Plone uses Bootstrap's CSS variables.
They are used to tweak colors, fonts, spacing, and other CSS attributes.

```{todo}
Provide usage.
```


(classic-ui-through-the-web-theming-control-panel-label)=

## Theming control panel

The Theming control panel is limited to downloading and uploading themes.


(classic-ui-through-the-web-templates-label)=

### Templates


(classic-ui-through-the-web-restricted-python-label)=

### Restricted python


(classic-ui-through-the-web-content-types-label)=

### Content types

