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

{term}`Diazo` allows you to apply a theme contained in a static HTML web page to a dynamic website created using any server-side technology.
With Diazo, you can take an HTML wireframe created by a web designer, and turn it into a theme for your favourite CMS, redesign the user interface of a legacy web application without even having access to the original source code, or build a unified user experience across multiple disparate systems, all in a matter of hours, not weeks.

A Diazo theme consists of a static HTML page, referred to as the _theme_, and a rules file, conventionally called {file}`rules.xml`.

When using Diazo, you will work with syntax and concepts familiar from working with HTML and CSS.
And by allowing you to seamlessly integrate XSLT into your rules files, Diazo makes common cases simple, and complex requirements possible.


## Create an add-on package

To create a Diazo theme, you need to create an add-on package with [`plonecli`](https://github.com/plone/plonecli).

You can run `plonecli` using [pipx](https://pipx.pypa.io/stable/), without needing to install `plonecli`, as follows.

```shell
pipx run plonecli create addon diazo.theme
```

Answer all the questions.

Next, add a theme called `theme` to the add-on package using `plonecli`.

```shell
cd diazo.theme
pipx run plonecli add theme
```

Answer the question of the theme name.


### Theme structure

The previous step creates a {file}`theme` folder inside {file}`diazo.theme/src/diazo/theme`, with the following structure.

```console
.
├── index.html
├── manifest.cfg
├── package.json
├── README.rst
├── rules.xml
├── styles
│   ├── theme.min.css
│   └── theme.scss
└── tinymce-templates
    ├── bs-dark-hero.html
    ├── bs-hero-left.html
    └── bs-pricing.html
```

The purpose of each item is described as follows.

{file}`index.html`
:   This is the theme file.
    Plone populates it with its content, according to rules defined in {file}`rules.xml`.

{file}`manifest.cfg`
:   This file contains the theme configuration, such as the theme name, the path to the rules file and some other configurations.

{file}`package.json`
:   The theme folder is, by itself, a JavaScript package.
    If you want to develop your theme here, you can declare the dependencies of your theme in this file.
    For instance, you can add `bootstrap` or `tailwind` as dependencies, and manage those dependencies and the building of your final CSS from here.

{file}`README.rst`
:   The file that explains how this theme is built and developed.

{file}`rules.xml`
:   The file where you will write your rules to bring Plone content into the theme in the {file}`index.html` file.

{file}`styles` folder
:   Where you can save your theme's CSS files.

{file}`tinymce-templates`
:   Template files that can be loaded into the TinyMCE editor in Plone.
    It requires additional configuration in the add-on's profile's {file}`registry.xml` file.


## Integrate an external theme using Diazo

Begin with any theme from outside Plone.
It should be composed of the required HTML, CSS, and JavaScript files.

When you have all files of your theme, put them in the {file}`theme` folder, and organize the CSS and JavaScript folders as you received them from your designer.

You may want to remove the `plonecli` generated `styles` and `tinymce-templates` folders.


## Adjust the theme manifest

Open the {file}`manifest.cfg` file.
You will see the following lines.

```cfg
production-css = ++theme++my-shiny-theme/styles/theme.min.css
tinymce-content-css = ++theme++my-shiny-theme/styles/theme.min.css
```

Comment them out as shown.

```cfg
# production-css = ++theme++my-shiny-theme/styles/theme.min.css
# tinymce-content-css = ++theme++my-shiny-theme/styles/theme.min.css
```

This way, you signal that you don't want either Plone or Diazo to manage the CSS files at all.
But it means that you will need to handle them in your design HTML files.


## Theme development advice

This section describes common practices when developing a Diazo theme.


### Avoid cache issues

CSS and JavaScript files should be properly versioned or hashed to avoid any caching problems whenever the theme is updated.

If the CSS file is called {file}`global.css`, and your designer updates the CSS without changing the file name, you will surely face caching issues.
Browsers, varnish, or other proxy servers might cache your files, and not serve them to the end users until the cache expires or gets flushed.

To avoid this issue, CSS bundling techniques that use npm tooling—such as Gulp, Grunt, or Webpack—create hashed or versioned filenames for CSS and JavaScript files.
The following HTML snippets show examples of versioned files.

```html
  <link id="frontend-css" rel="stylesheet" href="./css/app.css?v=14" />
  <script id="frontend-javascript" src="./js/app.js?v=3"></script>
```


### HTML template structure

Your theme should be as simple as possible.
That will make your {file}`rules.xml` file also as simple as possible.

The {file}`rules.xml` file declares which parts of theme will be replaced by the HTML produced by Plone.

It is a good practice to have a `<div>` element called `content` in your theme, which will contain the maximum space of the content area of your site.
That way you can inject the HTML produced by Plone there using Plone's content section, too.

Add a stanza in your {file}`rules.xml` file.

```xml
<replace
        css:theme-children="#content"
        css:content-children="article#content"
        css:if-content="#content"/>
```


### Minimize rules

You can start with the provided {file}`rules.xml` file.

You can read about how to write your rules and their syntax in the [official Diazo documentation](https://docs.diazo.org/en/latest/basic.html).

You will need to write your own rules to bring the dynamic content from Plone into the theme.

Sometimes you will face difficult situations where you may find it hard to put items in the same place that Plone produces in very different places.

For instance, you may need to put together the main menu, the language change, and the search box.
Sometimes it is easier to override the corresponding template in Plone, build the new HTML structure there, and replace one thing in the {file}`rules.xml` file than trying to write complex Diazo rules or writing XSLT.

The size of the {file}`rules.xml` file and the number of rules it contains can negatively impact the performance of your site.
