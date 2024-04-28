---
html_meta:
  "description": "How to use Module Federation in Mockup and add-on bundles."
  "property=og:description": "How to use Module Federation in Mockup and add-on bundles."
  "property=og:title": "Module Federation in Mockup"
  "keywords": "Plone, Classic UI, classic-ui, Mockup, mockup, Module Federation, Webpack, JavaScript"
---

(classic-ui-module-federation-in-mockup-label)=

# Module Federation in Mockup

Module Federation allows sharing of dependencies between bundles.
Each bundle includes the whole set of dependencies.
However, if multiple bundles have the same dependencies they are loaded only once.

For example, if bundle A and B both depend on jQuery and bundle A has already loaded it, bundle B can just reuse the already loaded jQuery file.
But if only bundle B is loaded, it uses its own bundled version of the jQuery library.

There is a host bundle, as in the fictional example above, our bundle A.
In Plone the host bundle is the main mockup bundle.
Add-ons can add bundles called "remotes" which are initialized for module federation by the host bundle.

```{seealso}
Webpack's documentation on [Module Federation](https://webpack.js.org/concepts/module-federation/).
```


## Using module federation

The following instructions are for you if you created an add-on with a Mockup pattern and you want to include the respective JavaScript code in your theme code.
Starting with the webpack configuration that you get when creating a Barceloneta theme package via [plonecli][1], add the following:

Create a new entry point `index.js` which only imports the normal entry point.

```js
import("./patterns");
```

Next add the module federation plugin in `webpack.config.js`.
There is a configuration factory `mf_config` which you can use for that.
Add the following line near the top of the file:

```js
const mf_config = require("@patternslib/dev/webpack/webpack.mf");
```

Import all the dependencies you want to share.
Potentially these are the ones from Patternslib, Mockup and your own dependencies.
You can just add the Patternslib and Mockup dependencies, even if you are not using them.

```js
const package_json = require("./package.json");
const package_json_mockup = require("@plone/mockup/package.json");
const package_json_patternslib = require("@patternslib/patternslib/package.json");
```

Then find the following line:

```js
    config = patternslib_config(env, argv, config, ["@plone/mockup"]);
```

Below this line add the following:

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

Replace the name `myaddon` with your addon bundle's name (any unique name will do...),
replace the filename `myaddon-remote.min.js` with the file name you want to use for your remote bundle,
and replace `myaddon.min` with the corresponding key in `config.entry` that points to your `index.js`.

For a full but simple example, see the Patterns generator [pat-PATTERN-TEMPLATE][2] or any other Pattern addon in the patternslib GitHub organisation.
For a complex example with Mockup integration see [plone.app.mosaic][3] and [Mockup][4] itself.

[1]: https://pypi.org/project/plonecli/
[2]: https://github.com/Patternslib/pat-PATTERN_TEMPLATE/blob/master/webpack.config.js
[3]: https://github.com/plone/plone.app.mosaic/blob/master/webpack.config.js
[4]: https://github.com/plone/mockup/blob/master/webpack.config.js

## Special case: global modules `jQuery` and `Bootstrap`

In order to preserve compatibility with older add-ons and JavaScript implementations,
the modules `jQuery` and `Bootstrap` are stored in the  global `window` namespace.
So constructs like the following are still working:

```js
    (function($) {
        // JS code which uses $
    })(jQuery);
```

