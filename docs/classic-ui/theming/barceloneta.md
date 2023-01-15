---
myst:
  html_meta:
    "description": "Plone Classic UI theming based on Barceloneta"
    "property=og:description": "Plone Classic UI theming based on Barceloneta"
    "property=og:title": "Plone Classic UI theming based on Barceloneta"
    "keywords": "Plone, Classic UI, theming, Barceloneta"
---

(classic-ui-theming-barceloneta-label)=

# Classic UI theming based on Barceloneta

```{todo}
This page is only an outline and needs a lot of work.
See https://github.com/plone/documentation/issues/1286
```

-   Use of SCSS
-   Colors, fonts, and sizes via variables is changeable
-   Properties for shadows, rounded corners, gradients.
-   `plonetheme.barceloneta` npm package for includes
-   `bobtemplates.plone` template
-   Theming is based on Twitter Bootstrap 5
-   We use Bootstrap markup in templates
-   We use Bootstrap components wherever possible
-   Most of the look and feel can be changed via Bootstrap's variables
-   Hint: order is important in SCSS


(classic-ui-theming-barceloneta-theme-package-label)=

## Theme package

-   Generated theme package can be uploaded as a .zip file.


(classic-ui-theming-barceloneta-theme-structure-label)=

## Theme structure

### `base.scss`

-   Basics required for backend

### `barceloneta.scss`

-   Barceloneta theme basics


## npm package

-   npm package with files required for Plone
-   dependencies required by theme to compile


## Bootstrap components

-   Default components are extended with some custom components, such as a select or dropdown menu.
-   We use Boostrap variables in these cases.


## Add-ons and templates

Make life easy with...

-   use Bootstrap markup
-   use Bootstrap components
-   use Bootstrap variables
