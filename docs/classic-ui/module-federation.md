---
myst:
  html_meta:
    "description": "How to use Module Federation in Mockup and add-on bundles."
    "property=og:description": "How to use Module Federation in Mockup and add-on bundles."
    "property=og:title": "Module Federation in Mockup"
    "keywords": "Plone, Classic UI, classic-ui, Mockup, Module Federation, webpack, JavaScript"
---

(classic-ui-module-federation-in-mockup-label)=

# Module Federation in Mockup

Module Federation allows sharing of dependencies between bundles.
Each bundle includes the whole set of dependencies.
However, if multiple bundles have the same dependencies, then they are loaded only once.

For example, if bundle A and B both depend on jQuery and bundle A has already loaded it, then bundle B can just reuse the already loaded jQuery file.
But if only bundle B is loaded, it uses its own bundled version of the jQuery library.

There is a host bundle, as in the fictional example above, our bundle A.
In Plone the host bundle is the main Mockup bundle.
Add-ons can add bundles called "remotes" which are initialized for Module Federation by the host bundle.

```{seealso}
Webpack's documentation on [Module Federation](https://webpack.js.org/concepts/module-federation/).
```


## Use Module Federation

If you created an add-on with a Mockup pattern, and you want to include the respective JavaScript code in your theme code, then the following instructions are for you.

Starting with the webpack configuration that you get when creating a Barceloneta theme package via [`plonecli`](https://pypi.org/project/plonecli/), add the following.

Create a new entry point {file}`index.js` which only imports the normal entry point.

```js
import("./patterns");
```

Next add the Module Federation plugin in {file}`webpack.config.js`.
There is a configuration factory `mf_config` which you can use for that.
Add the following line near the top of the file.

```js
const mf_config = require("@patternslib/dev/webpack/webpack.mf");
```

Import all the dependencies you want to share.
Potentially these are the ones from [Patternslib](https://github.com/Patternslib/Patterns/blob/master/package.json), Mockup, and your own dependencies.
You can add the Patternslib and Mockup dependencies, even if you are not using them.

```js
const package_json = require("./package.json");
const package_json_mockup = require("@plone/mockup/package.json");
const package_json_patternslib = require("@patternslib/patternslib/package.json");
```

Then find the following line.

```js
config = patternslib_config(env, argv, config, ["@plone/mockup"]);
```

Below this line add the following.

```js
config.plugins.push(
    mf_config({
        name: "myaddon",
        filename: "myaddon-remote.min.js",
        remote_entry: config.entry["myaddon.min"],
        dependencies: {
            ...package_json_patternslib.dependencies,
            ...package_json_mockup.dependencies,
            ...package_json.dependencies,
        },
    })
);
```

Replace the name `myaddon` with your add-on bundle's unique name.
Replace the file name {file}`myaddon-remote.min.js` with the file name you want to use for your remote bundle.
Finally replace `myaddon.min` with the corresponding key in `config.entry` that points to your {file}`index.js`.

For a full and basic example, see the Patterns generator [pat-PATTERN-TEMPLATE](https://github.com/Patternslib/pat-PATTERN_TEMPLATE/blob/master/webpack.config.js) or any other Pattern add-on in the [patternslib GitHub organization](https://github.com/patternslib/).
For a complex example with Mockup integration see [`plone.app.mosaic`](https://github.com/plone/plone.app.mosaic/blob/master/webpack.config.js) and [Mockup](https://github.com/plone/mockup/blob/master/webpack.config.js) itself.


## Special case: global modules `jQuery` and `Bootstrap`

To preserve compatibility with older add-ons and JavaScript implementations, the modules `jQuery` and `Bootstrap` are stored in the  global `window` namespace.
Constructs like the following still work:

```js
(function($) {
    // JS code which uses $
})(jQuery);
```
