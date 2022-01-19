---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

(classic-ui-through-the-web-label)=

# Through-the-web (TTW) Theme Customization in Plone 6 Classic UI

```{todo}
This page is only an outline and needs a lot of work.
```

TTW customization is useful when you need to make small CSS changes.
Theme changes can be made via control panels or by updating Plone 6 Classic UI's `custom.css`.
Other theming methods should be used for larger customizations or entire website designs.


(classic-ui-through-the-web-control-panels-label)=

## Control Panels

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

## CSS Variables

Plone uses Twitter Bootstrap's CSS variables.
They are used to tweak colors, fonts, spacing, and other CSS attributes.

```{todo}
Provide usage.
```



(classic-ui-through-the-web-theming-control-panel-label)=

## Theming Control Panel

The Theming control panel is limited to downloading and uploading themes.


(classic-ui-through-the-web-templates-label)=

### Templates


(classic-ui-through-the-web-restricted-python-label)=

### Restricted Python


(classic-ui-through-the-web-content-types-label)=

### Content Types

