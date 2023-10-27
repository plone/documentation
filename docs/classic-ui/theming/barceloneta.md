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

This chapter describes how to create a custom theme for Plone Classic UI based on Barceloneta.
Barceloneta is the default enabled theme for Plone Classic UI.


(classic-ui-theming-barceloneta-pre-requisites-label)=

## Pre-requisites

To create an add-on package with a Plone Classic UI theme, you need to install the following pre-requisites.

-   [Node.js (16/18)](https://nodejs.org/en)
-   [Python (>=3.8)](https://www.python.org/)
-   [plonecli](https://pypi.org/project/plonecli/)

Read more about how to install pre-requisites in {doc}`/install/install-from-packages`.


(classic-ui-theming-barceloneta-create-a-classic-ui-theme-add-on-package-label)=

## Create a Classic UI theme add-on package

To create a Classic UI theme add-on, begin with the following command.

```shell
plonecli create addon plonetheme.themebasedonbarceloneta
```

Then change the working directory into the package you just created, and add the basic theme structure with the following commands.

```shell
cd plonetheme.themebasedonbarceloneta
plonecli add theme_barceloneta
```

Give your theme a name, and optionally commit the changes.
After that, the theming structure is set up and ready for customization.
You can create a Plone Site and install your theme add-on in the controlpanel.


(classic-ui-theming-barceloneta-theme-structure-label)=

## Theme structure

All the theming relevant files are now located inside `src/plonetheme/themebasedonbarceloneta/theme/`:

```text
./src/plonetheme/themebasedonbarceloneta/theme/
├── barceloneta-apple-touch-icon-114x114-precomposed.png
├── barceloneta-apple-touch-icon-144x144-precomposed.png
├── barceloneta-apple-touch-icon-57x57-precomposed.png
├── barceloneta-apple-touch-icon-72x72-precomposed.png
├── barceloneta-apple-touch-icon-precomposed.png
├── barceloneta-apple-touch-icon.png
├── barceloneta-favicon.ico
├── index.html
├── manifest.cfg
├── package.json
├── preview.png
├── rules.xml
├── scss
│   ├── _custom.scss
│   ├── _maps.scss
│   ├── _variables.scss
│   └── theme.scss
├── styles
│   ├── theme.css
│   └── theme.min.css
└── tinymce-templates
    ├── README.rst
    ├── card-group.html
    └── list.html
```

`index.html`
:   Basic HTML structure for the site layout.

`manifest.cfg`
:   Basic theme configuration for the backend.

`package.json`
:   npm package configuration which defines all requirements for theming with barceloneta.

`rules.xml`
:   Diazo rules which translate the `index.html` and fills it with content from the backend.

`scss/_custom.scss`
:   Custom SCSS rules for your theme.

`scss/_maps.scss`
:   Override Bootstrap mapping variables here.

`scss/_variables.scss`
:   Override Bootstrap and/or Barceloneta variables here.

`scss/theme.scss`
:   Base theme file which follows "Option B" of customizing Bootstrap imports to enable custom variable and map injections.
    Note that the order of these imports is mandatory to ensure overriding the defaults.
    See https://getbootstrap.com/docs/5.3/customize/sass/#importing.

`styles/theme.css[.min]`
:   Compiled CSS styles.

`tinymce-templates/*.html`
:   HTML snippets for the TinyMCE `template` plugin.


(classic-ui-theming-barceloneta-compiling-theme-resources-label)=

## Compiling theme resources

To compile the SCSS code, you have to install the required dependencies with `npm`.
Then run the package script `build` inside the `theme/` folder:

```shell
npm install
npm run build
```

During theme development, you can run:

```shell
npm run watch
```

This compiles the SCSS resources on the fly when you change something inside the `scss/` folder.
You can preview your changes when you reload your browser.


(classic-ui-theming-barceloneta-customize-components-label)=

## Customize Bootstrap and Barceloneta components

The base `scss/theme.scss` file provides all imports of the dependent Bootstrap and Barceloneta resources to build the default Classic UI theme.
As a convenience `bobtemplates.plone` has created three files to customize variables, maps, and custom SCSS code.

```text
scss/_custom.scss
scss/_maps.scss
scss/_variables.scss
```


(classic-ui-theming-barceloneta-scss-and-root-variables-label)=

### SCSS and root variables

To set a custom font, you define the font variables in `scss/_variables.scss`:

```scss
$font-family-sans-serif: Tahoma, Calimati, Geneva, sans-serif;
$font-family-serif: Georgia, Norasi, serif;
```

This will override the default values from Barceloneta.


### SCSS and properties

The following example shows how to disable rounded corners for borders.

```scss
$enabled-rounded: false;
```

A complete list of all properties see {ref}`classic-ui-theming-barceloneta-default-variables-and-properties-label`.


(classic-ui-theming-barceloneta-maps-label)=

### Maps

Maps are key/value pairs to make CSS generation easier.
As an example, the following example shows the workflow colors map:

```scss
$state-colors: (
  "draft":                          $state-draft-color,
  "pending":                        $state-pending-color,
  "private":                        $state-private-color,
  "internal":                       $state-internal-color,
  "internally-published":           $state-internally-published-color,
) !default;
```

If you have a custom workflow state, you can add your state color to the default map in `scss/_maps.scss` as shown below.

```scss
$custom-state-colors: (
  "my-custom-state-id": "#ff0000"
);

// Merge the maps
$state-colors: map-merge($state-colors, $custom-colors);
```

(classic-ui-theming-barceloneta-custom-css-code-label)=

### Custom CSS code

Inside the file `theme/_custom.scss` you can write all your custom CSS/Sass code to adapt the theme to your needs.
Feel free to add more files inside the `scss/` folder to make your code more readable.
Don't forget to import your custom files in `scss/theme.scss`.


(classic-ui-theming-barceloneta-default-variables-and-properties-label)=

## Default variables and properties

The following variables and properties are defined in Bootstrap and customized by Barceloneta.

### Component variables

```scss
// Barceloneta settings

$primary:                                   $plone-link-color!default;
$light:                                     $plone-light-color!default;
$dark:                                      $plone-dark-color!default;

$spacer:                                    1rem!default; // not changed but needed to calc other definitions


// Grid columns
// Set the number of columns and specify the width of the gutters.

// $grid-columns:                           12 !default;
// $grid-gutter-width:                      1.5rem !default;
// $grid-row-columns:                        6 !default;

$grid-main-breakpoint:                      lg!default;
$nav-main-breakpoint:                       $grid-main-breakpoint!default;

$navbar-barceloneta-background:             $primary!default;

$navbar-padding-y:                          0 !default;
$navbar-padding-x:                          0 !default;
$navbar-nav-link-padding-y:                 $spacer * .75 !default;
$navbar-nav-link-padding-x:                 $spacer !default;

$navbar-light-color:                        rgba($black, .55) !default;
$navbar-light-active-color:                 rgba($black, .7) !default;
$navbar-light-active-background:            rgba($black, .2) !default;
$navbar-light-hover-color:                  rgba($black, .9) !default;
$navbar-light-hover-background:             rgba($black, .3) !default;

$navbar-dark-color:                         rgba($white, 1) !default;
$navbar-dark-active-color:                  rgba($white, 1) !default;
$navbar-dark-active-background:             rgba($white, .2) !default;
$navbar-dark-hover-color:                   rgba($white, 1) !default;
$navbar-dark-hover-background:              rgba($white, .3) !default;

$navbar-barceloneta-color:                  rgba($white, 1) !default;
$navbar-barceloneta-active-color:           rgba($white, 1) !default;
$navbar-barceloneta-active-background:      rgba($black, .2) !default;
$navbar-barceloneta-hover-color:            rgba($white, 1) !default;
$navbar-barceloneta-hover-background:       rgba($black, .3) !default;


$plone-portlet-navtree-maxlevel:            5!default;


// Typography
// While Plone Logo uses the DIN Font, we use Roboto, which was designed for Android and so mobile optimized
// A free DIN variant is available here (TTF only): https://www.1001fonts.com/alte-din-1451-mittelschrift-font.html
$font-family-sans-serif:                    "Roboto", "Helvetica Neue", Helvetica, Arial, sans-serif!default;
$font-family-condensed:                     "Roboto Condensed", "Arial Narrow", sans-serif!default; //just on toolbar
$font-family-serif:                         Georgia, "Times New Roman", Times, serif!default;
// $font-family-base:                       var(--bs-font-sans-serif) !default;
// $font-family-code:                       var(--bs-font-monospace) !default;

// Include Roboto as webfont
$enable-roboto-webfont:                     true !default;

// $font-size-base:                         1rem !default; // Assumes the browser default, typically `16px`
// $font-size-sm:                           $font-size-base * .875 !default;
// $font-size-lg:                           $font-size-base * 1.25 !default;

$font-weight-lighter:                       lighter !default;
$font-weight-light:                         300 !default;
$font-weight-normal:                        400 !default;
$font-weight-semibold:                      600 !default;
$font-weight-bold:                          700 !default;
$font-weight-bolder:                        bolder !default;

// $font-weight-base:                       $font-weight-normal !default;

// $line-height-base:                       1.5 !default;
// $line-height-sm:                         1.25 !default;
// $line-height-lg:                         2 !default;

// $h1-font-size:                           $font-size-base * 2.5 !default;
// $h2-font-size:                           $font-size-base * 2 !default;
// $h3-font-size:                           $font-size-base * 1.75 !default;
// $h4-font-size:                           $font-size-base * 1.5 !default;
// $h5-font-size:                           $font-size-base * 1.25 !default;
// $h6-font-size:                           $font-size-base !default;

// $headings-margin-bottom:                 $spacer * .5 !default;
// $headings-font-family:                   null !default;
// $headings-font-style:                    null !default;
$headings-font-weight:                      $font-weight-normal !default;
// $headings-line-height:                   1.2 !default;
// $headings-color:                         null !default;

// Breadcrumbs
$breadcrumb-margin-bottom:                  2rem !default;
$breadcrumb-bg:                             var(--bs-secondary-bg) !default;
$breadcrumb-padding-y:                      $spacer * 0.5 !default;
$breadcrumb-padding-x:                      $spacer * 1 !default;


// Footer
$footer-bg:                                 $gray-900 !default;
$footer-color:                              $gray-300 !default;
```

### Properties

```scss
$enable-caret:                true !default;
$enable-rounded:              true !default;
$enable-shadows:              false !default;
$enable-gradients:            false !default;
$enable-transitions:          true !default;
$enable-reduced-motion:       true !default;
$enable-smooth-scroll:        true !default;
$enable-grid-classes:         true !default;
$enable-container-classes:    true !default;
$enable-cssgrid:              false !default;
$enable-button-pointers:      true !default;
$enable-rfs:                  true !default;
$enable-validation-icons:     true !default;
$enable-negative-margins:     true !default;
$enable-deprecation-messages: true !default;
$enable-important-utilities:  false !default;
```
