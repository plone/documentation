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

To create a custom {term}`pattern` in your add-on, use the `mockup_pattern` {term}`bobtemplate`.

```shell
cd project.addon
plonecli add mockup_pattern
```

Next, enter your pattern name without the `pat-` prefix
In the following example, its name is `testpattern`.

```shell
--> Pattern name (without “pat-” prefix) [my-pattern]: testpattern
```

This creates the necessary JavaScript resources and webpack configuration for you, as shown in the following file system tree diagram.

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

All your pattern JavaScript code goes into {file}`resources/pat-testpattern/testpattern.js`.
SCSS files can be imported, too, since webpack provides the `sass-loader` module.

Next, install the npm packages using {term}`yarn`.

```shell
yarn install
```

When you finish writing your JavaScript code, you have to build the bundle with the following command.

```shell
yarn build
```

This creates the webpack chunks, the JavaScript bundle files, and a demo browser view in your add-on package.

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
|   |   |   |   ├── pattern-demo.pt
```

There is also an XML file in {file}`src/project/addon/profiles/default/registry/bundles.xml` which registers the {file}`addon-remote.min.js` in the resources registry.

```{important}
You must re-import your profile with an upgrade step if you installed your add-on in Plone before adding the pattern.
Uninstall, then re-install, the add-on in the control panel.
Alternatively you can write a GenericSetup upgrade step.
```

You can access the demo browser view in your browser with `http://localhost:8080/Plone/@@addon-pattern-demo`.
Alternatively you can implement it in your own templates by adding the CSS class `pat-testpattern` to an HTML tag, such as an `img` tag.

```html
<img class="pat-testpattern">
```


## References

-   [`bobtemplates.plone` documentation](https://bobtemplatesplone.readthedocs.io/)
-   [`mr.bob` documentation](https://mrbob.readthedocs.io/en/latest/)
-   [Plone CLI documentation](https://plonecli.readthedocs.io/en/latest/)
-   [`bobtemplates.plone` repository](https://github.com/plone/bobtemplates.plone)
-   [`mr.bob` repository](https://github.com/collective/mr.bob)
-   [Plone CLI (`plonecli`) repository](https://github.com/plone/plonecli)
-   {ref}`v60-mockup-resource-registry-label` in Plone 6.0
-   [Mockup repository on GitHub](https://github.com/plone/mockup)
-   [Patternslib](https://patternslib.com/)
