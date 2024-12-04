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
For CSS and JavaScript files we can use the resource registry to register them and have them delivered to the client browser.
The benefit of using the resource registry for CSS and JavaScript resources over putting them hard-coded into templates is that the resource registry provides an programmatic way, which is easy to extend and configure in code and also through the web, cares about dependencies between resources and handles caching automatically for us.

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

Registering a JavaScript file and a CSS file in the same bundle is also possible.

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

The following attributes are available for registering a static resource:

`enabled`
:   Whether the bundle is enabled or not.
    If it is disabled, the bundle will not be loaded.

`jscompilation`
:   The path to the compiled JavaScript file.

`csscompilation`
:   The path to the compiled CSS file.

`depends`
:   A comma separated list of bundles that this bundle depends on.
    For a single dependency, just put it's name in there.
    When a bundle depends on another one, the script or link tag is rendered after the bundle it depends on.
    The bundle you want to depend on must exist, otherwise the resource is not rendered.
    You can use the special value `all` to depend on all other resources and have the resource rendered after all other (new in Plone 6.0.14).
    This allows CSS files be loaded after the automatically added theme resources and overload CSS declarations from own CSS customization files.
    There is one exception though - the custom CSS files which can be edited trough the web in the theming control panel always come last.

`load_async`
:   Whether the bundle should be loaded asynchronously or not.
    *Only JavaScript*

`load_defer`
:   Whether the bundle should be loaded deferred or not (not effect if `load_async` is used).
    *Only JavaScript*


(classic-ui-static-resources-loading-order-label)=

## Loading order of resources

`depends` is used to define the loading order of resources by specifying the name of the depending bundle.
