---
myst:
  html_meta:
    "description": "Static resources in Plone 6"
    "property=og:description": "Static resources in Plone 6"
    "property=og:title": "Static resources in Plone 6"
    "keywords": "Plone, static, resources, JavaScript, CSS"
---

(classic-ui-static-resources-label)=

# Static resources

We often want to ship a website with a static resource, such as an image, icon, CSS, or JavaScript file.
For CSS and JavaScript files, we can use the resource registry to register, then deliver, them to the client browser.

The resource registry provides a programmatic way, either in code or through the web, to extend and configure the dependencies between static resources.
It also automatically manages caching of static resources.
If you were to hard-code these resources in templates with `<link>` or `<script>` tags, you would not have these advantages.

```{seealso}
For some additional implementation information, see {ref}`classic-ui-theming-from-scratch-theme-label`.
```


(classic-ui-static-resources-registering-label)=

## Registering JavaScript and CSS

To register a static resource in Plone 6, we need to use the `plone.base.interfaces.resources.IBundleRegistry` interface.

The following example registers a JavaScript resource in `browser/profiles/default/registry` of your Plone 6 project.
The JavaScript files have to be in the `browser/static` folder of your Plone 6 project.

```xml
<registry>
  <records interface="plone.base.interfaces.resources.IBundleRegistry" prefix="plone.bundles/jscript">
    <value key="enabled">True</value>
    <value key="jscompilation">++plone++myproject.site/javascript.min.js</value>
    <value key="load_async">False</value>
    <value key="load_defer">False</value>
    <value key="depends">plone</value>
  </records>
</registry>
```

You can register a CSS resource in the same way.

```xml
    <registry>
    <records interface="plone.base.interfaces.resources.IBundleRegistry" prefix="plone.bundles/css">
      <value key="enabled">True</value>
      <value key="csscompilation">++plone++myproject.site/style.min.css</value>
      <value key="depends">plone</value>
    </records>
  </registry>
```

You can also register both a JavaScript file and a CSS file in the same bundle.

```xml
<registry>
  <records interface="plone.base.interfaces.resources.IBundleRegistry" prefix="plone.bundles/css">
    <value key="enabled">True</value>
    <value key="csscompilation">++plone++myproject.site/style.min.css</value>
    <value key="jscompilation">++plone++myproject.site/javascript.min.js</value>
    <value key="load_async">False</value>
    <value key="load_defer">False</value>
    <value key="depends">plone</value>
  </records>
</registry>
```


(classic-ui-static-resources-available-attributeslabel)=

## Available attributes

The following attributes are available for registering a static resource.

`enabled`
:   Boolean.
    Whether the bundle is enabled or not.
    If it is disabled, the bundle will not be loaded.

`jscompilation`
:   String.
    The path to the compiled JavaScript file.

`csscompilation`
:   String.
    The path to the compiled CSS file.

`depends`
:   String.
    A comma-separated list of bundles that this bundle depends on.
    For a single dependency, do not insert commas.

    When a bundle depends on another one, its `<script>` or `<link>` tag is rendered after the bundle it depends on.

    If the bundle's dependencies do not exist, then the bundle will not render.

    The `depends` attribute may be assigned the value of `all`, making this bundle render last, after all other bundles.
    The `all` value lets you load CSS files after the automatically added theme resources and override CSS declarations from your own custom CSS files.

    If you set multiple bundles to `all`, then these bundles will render in alphabetical order by its name.

    ```{note}
    You can also add custom CSS through-the-web via the {guilabel}`Theming` control panel, under {menuselection}`Site Setup --> Theming --> Advanced settings --> Custom Styles`.
    Setting `depends` to `all` does not affect custom CSS that you define in the {guilabel}`Theming` control panel, which _always_ renders as the last style resource.
    It only affects bundles, not control panel settings.
    ```

    ```{versionadded} Plone 6.0.14
    `depends` value of `all`.
    ```

`load_async`
:   Boolean.
    Whether the bundle should be loaded asynchronously or not.
    *Only JavaScript*

`load_defer`
:   Boolean.
    Whether the bundle should be loaded deferred or not.
    If you use `load_async`, this attribute has no effect.
    *Only JavaScript*
