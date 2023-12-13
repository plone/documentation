---
myst:
  html_meta:
    "description": "Plone Classic UI theming from scratch"
    "property=og:description": "Plone Classic UI theming from scratch"
    "property=og:title": "Plone Classic UI theming from scratch"
    "keywords": "Plone, Classic UI, theming, scratch"
---

(classic-ui-theming-from-scratch-label)=

# Classic UI theming from scratch

```{todo}
This page is only an outline and needs a lot of work.
See https://github.com/plone/documentation/issues/1286
```

Theming based on a filesystem package without any dependency.

-   Theming for Plone 6 Classic UI
-   Theme stored in a filesystem package
-   Built from scratch
-   No dependencies to Barceloneta
-   No Diazo needed


## Theme package

-   Create a theme package as explained here.
-   Remove what you do not need
-   Overrides
-   Static files


## Static files

Register directory to keep static files

File: `src/plonetheme/munich/browser/configure.zcml`
Directory: `src/plonetheme/munich/browser/static`

```xml
<!-- Publish static files -->
<plone:static
    name="plonetheme.munich"
    type="plone"
    directory="static"
    />
```

## Theme

### Manifest

-   Manifest for your theme
-   Keep rules empty to disable Diazo

```ini
[theme]
title = Munich Theme
description = A modernized Plone 6 theme
preview = preview.png
rules =
prefix = /++theme++plonetheme.munich
doctype = <!DOCTYPE html>
```

### Bundle registration

```xml
<?xml version="1.0"?>
<registry
    xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    i18n:domain="plonetheme.munich">

  <records interface="Products.CMFPlone.interfaces.IBundleRegistry" prefix="plone.bundles/munich">
    <value key="jscompilation">++theme++munich/js/munich.min.js</value>
    <value key="csscompilation">++theme++munich/css/munich.min.css</value>
    <value key="enabled">True</value>
    <value key="compile">False</value>
    <value key="last_compilation">2020-12-06 12:00:00</value>
  </records>

</registry>
```

### Theme registration

Register your theme via theme.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<theme>
  <name>munich</name>
  <enabled>true</enabled>
</theme>
```

### Compile the bundle

-   Compile SASS to SCSS

Install all requirements and dependencies from package.json:

```shell
yarn install
```

Build the actual bundle:

```shell
yarn dist
```


### Theming

-   Make use of Bootstrap [variables](https://github.com/twbs/bootstrap/blob/main/scss/_variables.scss)
-   Tweak basic settings like rounded corners, shadows, and so on.
-   Set custom fonts
-   Define your own stuff
-   Import Boostrap (as basis)


#### Minimal backend styling

When creating a theme from scratch, it still makes sense (and saves time) to reuse the barceloneta theme for:

- Plone toolbar
- add/edit forms
- control panels

To be able to do so:

- create a new CSS file on your theme like this:

```scss
// plone variables (used in toolbar)
// Plone specific colors
//colors
$state-draft-color:                 #fab82a!default; // lime-yellow //draft is visible
$state-pending-color:               #e2e721!default; // orange
$state-private-color:               #c4183c!default; // red
$state-internal-color:              #fab82a!default; // is draft
$state-internally-published-color:  #883dfa!default; // is intranet
$plone-link-color:                  #007bb1!default; //plone blue made slightly darker for wcag 2.0
$spacer:                            1rem!default;

// Toolbar
$plone-toolbar-bg: rgba(0, 0, 0, 0.9);
$plone-toolbar-submenu-bg: rgba(20, 20, 20, 0.95);
$plone-toolbar-font-primary: "Roboto Condensed", sans-serif;
$plone-toolbar-font-secondary: "Roboto", sans-serif;
$plone-toolbar-separator-color: rgba(255, 255, 255, 0.17);
$plone-toolbar-link: $plone-link-color;
$plone-toolbar-text-color: rgba(255, 255, 255, 0.9);
$plone-toolbar-submenu-text-color: #fff;
$plone-toolbar-submenu-header-color: lighten(#000, 80%);

$plone-toolbar-locked-color: var(--bs-warning); // is intranet

$plone-toolbar-width: 220px;
$plone-toolbar-width-collapsed: calc($spacer * 2.25);
$plone-toolbar-top-height: calc($spacer * 2.5);

@import "bootstrap/scss/bootstrap";

@import "@plone/plonetheme-barceloneta-base/scss/toolbar";
@import "@plone/plonetheme-barceloneta-base/scss/controlpanels";
@import "@plone/plonetheme-barceloneta-base/scss/forms";
```

```{tip}
See all the [barceloneta SCSS files](https://github.com/plone/plonetheme.barceloneta/tree/master/scss)
that are available and import the ones that you want to use.
```

Add `@plone/plonetheme-barceloneta-base` as a dependency:

```shell
yarn add @plone/plonetheme-barceloneta-base
```

Add a script on `package.json` to compile the CSS:

```json
  "css-compile-main": "sass --load-path=node_modules --style expanded --source-map --embed-sources --no-error-css plone.scss:../static/plone.css"
```

```{tip}
Look at [plonetheme.barcelonta package.json](https://github.com/plone/plonetheme.barceloneta/blob/master/package.json)
for a few more scripts to prefix and minify your CSS to get a production ready bundle.
```
    
Run the compilation:

```shell
yarn run css-compile-main
```

Finally, register the [CSS as a bundle](#bundle-registration).

With this, you will save yourself quite some work on styling the toolbar, the add/edit forms and controlpanels,
while keeping the rest of your theming on your own.

#### Templates

-   Add `z3c.jbot` overrides
-   Copy templates to customize
-   Add custom views for your story


### Available themes

-   [`plonetheme.tokyo`](https://github.com/collective/plonetheme.tokyo/) (mobile first, one column)
-   [`plonetheme.munich`](https://github.com/collective/plonetheme.munich/) (minimalistic)
