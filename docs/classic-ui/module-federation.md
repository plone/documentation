---
html_meta:
  "description": "How to use Module Federation in Mockup and add-on bundles."
  "property=og:description": "How to use Module Federation in Mockup and add-on bundles."
  "property=og:title": "Module Federation in Mockup"
  "keywords": "Plone, Classic UI, classic-ui, Mockup, mockup, Module Federation, Webpack, JavaScript"
---

(classic-ui-module-federation-in-mockup-label)=

# Module Federation in Mockup


```{seealso}
Webpack's documentation on [Module Federation](https://webpack.js.org/concepts/module-federation/).
```

Module Federation allows sharing of dependencies between bundles.
Each bundle includes the whole set of dependencies.
However, if multiple bundles have the same dependencies they are loaded only once.

For example, if bundle A and B both depend on jQuery and bundle A has already loaded it, bundle B can just reuse the already loaded jQuery file.
But if only bundle B is loaded, it uses its own bundled version of the jQuery library.

There is a host bundle - in the fictional example above our bundle "A".
In Plone the host bundle is the main mockup bundle.
Addons can add bundles called "remotes" which are initialized for module federation by the host bundle.

## Using module federation
This instruction is for you if you created an add-on with a Mockup pattern and you want to include the respective JavaScript code in your theme code.
Starting with the webpack configuration that you get when creating a barceloneta theme package via [plonecli][1], add the following:

- Create a new entry point `index.js` which only imports the normal entry point.

```js
import("./patterns");
```

- Add the module federation plugin in webpack.config.js. There is a configuration factory `mf_config` which you can use for that. Add the following line near the top of the file:

```js
const mf_config = require("@patternslib/dev/webpack/webpack.mf");
```

Then find the following line:

```js
    config = patternslib_config(env, argv, config, ["mockup"]);
```

Below this line add the following:

```js
    config.plugins.push(
        mf_config({
            filename: "myaddon-remote.min.js",
            package_json: package_json,
            remote_entry: config.entry["myaddon.min"],
        })
    );
```

Replace `myaddon-remote.min.js` with the file name you want to use for your remote bundle. Replace `myaddon.min` with the corresponding key in `config.entry` that points to your `index.js`.

[1]: https://pypi.org/project/plonecli/

## Special case: global modules `jQuery` and `Bootstrap`

In order to preserve compatibility with older addons and JavaScript implementations,
the modules `jQuery` and `Bootstrap` are stored in the  global `window` namespace.
So constructs like the following are still working:

```js
    (function($) {
        // JS code which uses $
    })(jQuery);
```
