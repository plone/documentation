---
myst:
  html_meta:
    "description": "Mockup together with Patternslib are used to build the UI toolkit for Classic UI, a frontend for Plone."
    "property=og:description": "Mockup together with Patternslib are used to build the UI toolkit for Classic UI, a frontend for Plone."
    "property=og:title": "Mockup and Patternslib"
    "keywords": "Mockup, Patternslib, Classic UI, plonecli, bobtemplates.plone, mr.bob, frontend, Plone"
---

(mockup-and-patternslib-label)=

# Mockup and Patternslib

{term}`Mockup` together with {term}`Patternslib` are used to build the UI toolkit for {term}`Classic UI`, a frontend for Plone.

View the [interactive documentation of Mockup](https://plone.github.io/mockup/).


## Get started

[`bobtemplates.plone`](https://github.com/plone/bobtemplates.plone) provides [`mr.bob`](https://github.com/collective/mr.bob) templates to generate packages for Plone projects.
[Plone CLI (`plonecli`)](https://github.com/plone/plonecli) provides a command line client for `bobtemplates.plone`.

Install {term}`plonecli` into your Python user packages to make it available to all your projects.

```shell
pip install plonecli --user
```

Create an add-on package with `plonecli`.

```shell
plonecli create addon project.addon
```

This will create a package `project.addon`, which you can install in your Plone site.

You can `cd` to the project, and add features to that package, such as content types, behaviors, control panels, or REST API endpoints.

```shell
cd project.addon
plonecli add content_type
plonecli add behavior
plonecli theme_barceloneta
```

Each of the features asks several questions to create the desired feature, customized to your preferences.

You can check the full list of available features using the `-l` parameter:

```shell
plonecli -l
```

## Create a custom pattern

To create a custom pattern in your addon use the `mockup_pattern` bobtemplate:

```shell
cd project.addon
plonecli add mockup_pattern
```

Now enter your pattern name without *pat-* prefix:

```shell
--> Pattern name (without “pat-” prefix) [my-pattern]: testpattern
```

This creates the necessary JS resources and webpack configuration for you:

```text
...
├── resources
|   ├── pat-testpattern
|   |   ├── documentation.md
|   |   ├── testpattern.js
|   |   ├── testpattern.scss
|   |   ├── testpattern.test.js
│   ├── bundle.js
│   ├── index.html
│   ├── index.js
├── package.json
├── webpack.config.js
...
```

All your pattern JS code goes into `resources/pat-testpattern/testpattern.js`.
SCSS files can be imported too since webpack provides the `sass-loader` module.

Next step is to install the npm packages (yarn recommended):

```shell
yarn install
```

When you have finished your JS code you have to build the bundle with:

```shell
yarn build
```

This creates the webpack chunks and the JS bundle files in your addon package:

```text
...
├── src
|   ├── project
|   |   ├── addon
|   |   |   ├── browser
|   |   |   |   ├── static
|   |   |   |   |   ├── bundles
|   |   |   |   |   |   ├── chunks
|   |   |   |   |   |   ├── addon-remote.min.js
|   |   |   |   |   |   ├── addon-remote.min.js.map
|   |   |   |   |   |   ├── addon.min.js
|   |   |   |   |   |   ├── addon.min.js.map
```

Note that `plonecli` also creates a XML file in `src/project/addon/profiles/default/registry/bundles.xml`
which registers the `addon-remote.min.js` in the resources registry.

```{important}
You have to re-import your profile with an upgrade step if you have installed
your addon in Plone before adding the pattern.
```

You can test your pattern now with the browser view `@@addon-pattern-demo` (see /src/project/addon/browser/pattern-demo.pt)
or implement it in your own templates by adding the CSS class `pat-testpattern` to a tag.


## References

-   [`bobtemplates.plone` documentation](https://bobtemplatesplone.readthedocs.io/en/latest/)
-   [`mr.bob` documentation](https://mrbob.readthedocs.io/en/latest/)
-   [Plone CLI documentation](https://plonecli.readthedocs.io/en/latest/)
-   [`bobtemplates.plone` repository](https://github.com/plone/bobtemplates.plone)
-   [`mr.bob` repository](https://github.com/collective/mr.bob)
-   [Plone CLI (`plonecli`) repository](https://github.com/plone/plonecli)
-   {ref}`v60-mockup-resource-registry-label` in Plone 6.0
-   [Mockup repository on GitHub](https://github.com/plone/mockup)
-   [Patternslib](https://patternslib.com/)
