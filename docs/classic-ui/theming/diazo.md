---
myst:
  html_meta:
    "description": "Plone Classic UI theming with Diazo"
    "property=og:description": "Plone Classic UI theming with Diazo"
    "property=og:title": "Plone Classic UI theming with Diazo"
    "keywords": "Plone, Classic UI, theming, Diazo"
---

(classic-ui-theming-diazo-label)=

# Classic UI theming with Diazo

```{todo}
This page is only an outline and needs a lot of work.
See https://github.com/plone/documentation/issues/1645
```

Diazo allows you to apply a theme contained in a static HTML web page to a dynamic website created using any server-side technology. With Diazo, you can take an HTML wireframe created by a web designer and turn it into a theme for your favourite CMS, redesign the user interface of a legacy web application without even having access to the original source code, or build a unified user experience across multiple disparate systems, all in a matter of hours, not weeks.

When using Diazo, you will work with syntax and concepts familiar from working with HTML and CSS. And by allowing you seamlessly integrate XSLT into your rule files, Diazo makes common cases simple and complex requirements possible.

## Create an addon package

To create a Diazo theme, you need to create an add.on package. To do so, you can do it using `plonecli`.

```
plonecli create addon diazo.theme
```

You need to answer to all the questions, you can accept the default ones.

Then you need to add a `theme` to the add-on package, you can do it like this using `plonecli`:

```
cd diazo.theme
plonecli add theme
```

you need to answer the question of the theme name and you are done!

## Theme structure

This process has created a `theme` folder inside diazo.theme/src/diazo/theme, with the following structure:

```
$ tree .
.
├── index.html
├── manifest.cfg
├── package.json
├── README.rst
├── rules.xml
├── styles
│   ├── theme.min.css
│   └── theme.scss
└── tinymce-templates
    ├── bs-dark-hero.html
    ├── bs-hero-left.html
    └── bs-pricing.html

3 directories, 10 files
```

## How to integrate an external theme using Diazo

First of all you need to have a theme built externally to Plone. It should be composed by the required HTML, CSS and JS files.

CSS and JS files should be properly versioned or hashed, in order to avoid any caching problems whenever the theme is updated.

If the CSS file is called `global.css` and your designer updates the CSS without changing the file name, you will surely face caching issues because browsers, varnish or other proxy servers *may* cache your files and may not serve them fresh to the end users.

To avoid so, it is common to use CSS bundling techniques using npm tooling like Gulp, Grunt or Webpack, and create hashed or versioned filenames for CSS and JS files like

```
  <link id="frontend-css" rel="stylesheet" href="./css/app.css?v=14" />

  <script id="frontend-javascript" src="./js/app.js?v=3"></script>

```

When you have all files of your theme, put them in the `theme` folder, and organize the CSS and JS folders like you have received from your designer.

You may want to remove the plonecli generated `styles` and `tinymce-templates` folders.

## Adjust the theme manifest

Open the `manifest.cfg` file. You will see the following lines there:

```
production-css = ++theme++my-shiny-theme/styles/theme.min.css
tinymce-content-css = ++theme++my-shiny-theme/styles/theme.min.css
```

Comment them, and leave them like this:

```
# production-css = ++theme++my-shiny-theme/styles/theme.min.css
# tinymce-content-css = ++theme++my-shiny-theme/styles/theme.min.css
```

This way we signal that we don't want either Plone or Diazo manage the CSS files at all.

But it means that we will need to handle them in our design HTML files.

## HTML Template structure

You want to have an as simple as possible theme because that means that your `rules.xml` file will also be simple.

The `rules.xml` file is the file that will say which parts of theme will be repaced by the HTML produced by Plone.

It is a good practice to have a div called `content` in your theme which will contain the maximum space of the content area of your site, because that way you can inject the HTML produced by Plone there using Plone's content section too.

So, you will be adding a stanza like this in your `rules.xml` file:


```
<replace css:theme-children="#content" css:content-children="article#content" css:if-content="#content"/>
```


