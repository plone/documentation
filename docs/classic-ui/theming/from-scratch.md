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
See https://github.com/plone/documentation/issues/1645
```

Theming based on a filesystem package without any dependency.

-   Theming for Plone 6 Classic UI
-   Theme stored in a filesystem package
-   Built from scratch
-   No dependencies to Barceloneta
-   No Diazo needed


(classic-ui-theming-from-scratch-package-label)=

## Theme package

-   Create a theme package as explained here.
-   Remove what you do not need
-   Overrides
-   Static files


(classic-ui-theming-from-scratch-static-files-label)=

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


(classic-ui-theming-from-scratch-theme-label)=

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

(classic-ui-from-scratch-bundle-registration-label)=

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
-   Import Bootstrap (as basis)


#### Minimal backend styling

When you create a theme from scratch, it is convenient to reuse the Barceloneta theme for:

-   Plone toolbar
-   add and edit forms
-   control panels

To do so, follow this guide.

-   Create a new CSS file in your theme, such as the following.

    ```scss
    @import "@plone/plonetheme-barceloneta-base/scss/variables.colors.plone";
    @import "@plone/plonetheme-barceloneta-base/scss/variables.colors.dark.plone";
    @import "@plone/plonetheme-barceloneta-base/scss/root_variables";
    @import "bootstrap/scss/bootstrap";
    
    @import "@plone/plonetheme-barceloneta-base/scss/toolbar";
    @import "@plone/plonetheme-barceloneta-base/scss/controlpanels";
    @import "@plone/plonetheme-barceloneta-base/scss/forms";
    ```

    ```{tip}
    See all the available [Barceloneta SCSS files](https://github.com/plone/plonetheme.barceloneta/tree/master/scss), and import the ones that you want to use.
    ```

-   Add `@plone/plonetheme-barceloneta-base` as a dependency.

    ```shell
    yarn add @plone/plonetheme-barceloneta-base
    ```

-   Add a script in {file}`package.json` to compile the CSS.

    ```json
    "css-compile-main": "sass --load-path=node_modules --style expanded --source-map --embed-sources --no-error-css plone.scss:../static/plone.css"
    ```

    ```{tip}
    Look at [`plonetheme.barcelonta`'s {file}`package.json`](https://github.com/plone/plonetheme.barceloneta/blob/master/package.json) for a few more scripts that can prefix and minify your CSS and get a bundle for use in production.
    ```

-   Run the compilation.

    ```shell
    yarn run css-compile-main
    ```

-   Finally, {ref}`register the bundle <classic-ui-from-scratch-bundle-registration-label>`.

With this guide, you will save yourself quite some work on styling the toolbar, the add and edit forms, and control panels, while keeping the rest of your theming separate.


#### Templates

-   Add `z3c.jbot` overrides
-   Copy templates to customize
-   Add custom views for your story


### Available themes

-   [`plonetheme.tokyo`](https://github.com/collective/plonetheme.tokyo/) (mobile first, one column)
-   [`plonetheme.munich`](https://github.com/collective/plonetheme.munich/) (minimalistic)
