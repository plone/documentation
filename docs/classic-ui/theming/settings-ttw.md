---
myst:
  html_meta:
    "description": "Change Classic UI theme settings through-the-web (TTW) in Plone 6"
    "property=og:description": "Change Classic UI theme settings through-the-web (TTW) in Plone 6"
    "property=og:title": "Change Classic UI theme settings through-the-web (TTW) in Plone 6"
    "keywords": "Plone 6, Classic UI, Through-the-web, TTW, theme, customization"
---

(classic-ui-through-the-web-label)=

# Change theme settings TTW

This chapter describes how to change Classic UI theme settings through-the-web ({term}`TTW`) in Plone 6.

Small theme changes can be made via control panels.
Other theming methods should be used for larger customizations or entire website designs.


(classic-ui-through-the-web-control-panels-label)=

## Control panels

You can make the following changes through control panels.

-   Logo
-   Favicon
-   Custom Styles


### Logo

Navigate to {menuselection}`Admin --> Site Setup --> Site`, or visit the URL path `/@@site-controlpanel` in your web browser's address bar.

Under {guilabel}`Site Logo`, you can upload a custom logo for your site.


### Favicon

Navigate to {menuselection}`Admin --> Site Setup --> Site`, or visit the URL path `/@@site-controlpanel` in your web browser's address bar.

Under {guilabel}`Site Favicon`, you can upload a custom favicon for your site.

When you upload a new favicon, the previous field {guilabel}`MIME type of the site favicon` will update with the favicon's correct media type.


### Custom Styles

Navigate to {menuselection}`Admin --> Site Setup --> Theming --> Advanced settings --> Custom Styles`, or visit the URL path `/@@theming-controlpanel#autotoc-item-autotoc-2` in your web browser's address bar.

Enter any arbitrary styles, and save your changes.
The changes are stored in a `BrowserView` called `custom.css`.
It is shipped as the last resource after all other CSS files.
It can be used to override default CSS, sometimes with the use of the CSS property `!important` or specific CSS selectors.

However, you should use it only for small changes to CSS.
For larger changes, see {doc}`create-add-on`.


## Themes

Under {menuselection}`Admin --> Site Setup --> Theming --> Themes`, you are limited to downloading and uploading themes.
