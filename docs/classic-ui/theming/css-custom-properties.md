---
myst:
  html_meta:
    "description": "Create a Classic UI theme add-on for Plone"
    "property=og:description": "Create a Classic UI theme add-on for Plone"
    "property=og:title": "Create a Classic UI theme add-on for Plone"
    "keywords": "Plone, Classic UI, theming, add-on"
---

(classic-ui-theming-CSS-custom-properties-label)=

# CSS custom properties

This chapter describes the [CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascading_variables/Using_CSS_custom_properties) used in Bootstrap and customized by Classic UI themes.
Custom properties (sometimes referred to as CSS variables or cascading variables) are entities defined by CSS authors that represent specific values to be reused throughout a document.


## Component variables

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

## Properties

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
