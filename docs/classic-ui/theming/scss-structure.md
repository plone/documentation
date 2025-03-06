---
myst:
  html_meta:
    "description": "SCSS structure for Classic UI themes for Plone"
    "property=og:description": "SCSS structure for Classic UI themes for Plone"
    "property=og:title": "SCSS structure for Classic UI themes for Plone"
    "keywords": "Plone, Classic UI, theming, add-on"
---

(classic-ui-theming-theme-structure-label)=

# Theme structure

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
