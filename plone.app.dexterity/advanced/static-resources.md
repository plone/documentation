---
myst:
  html_meta:
    "description": "How to add images, stylesheets, JavaScripts, and other static assets with Plone content types"
    "property=og:description": "How to add images, stylesheets, JavaScripts, and other static assets with Plone content types"
    "property=og:title": "How to add images, stylesheets, JavaScripts, and other static assets with Plone content types"
    "keywords": "Plone, content types, static, resources"
---

# Static resources

This chapter describes how to add images, stylesheets, JavaScripts, and other static assets.

Earlier in this manual, we have seen how to create views, and how to use file and image fields.
These are all dynamic, however, and often we just want to ship with a static image, icon, CSS or JavaScript file.
For this, we need to register static resources.


## Registering a static resource directory

The easiest way to manage static resources is to create a `static` resource directory in your Dexterity project using the ZCML `resourceDirectory` directive.

Registration of the resource directory is done using the `<browser:resourceDirectory />` ZCML directive.
This requires two attributes.
`name` is the name that appears after the `++resource++` namespace
`directory` is a relative path to the directory containing resources.

It's conventional to use `static` for the directory name, and the dotted name of your package for the resource name.
You would use this ZCML to register it.

```xml
<browser:resourceDirectory
  name="example.conference"
  directory="static" />
```

Then, if a "static" resource directory in the `example.conference` package contains a file called {file}`conference.css`, it will be accessible on a URL, such as `https://<server>/site/++resource++example.conference/conference.css`.
The resource name is the same as the package name wherein the `resources` directory appears.


## Importing CSS and JavaScript files in templates

One common use of static resources is to add a static CSS or JavaScript file to a specific template.
We can do this by filling the `style_slot` or `javascript_slot` in Plone's `main_template` in our own view template and using an appropriate resource link.

For example, we could add the following near the top of {file}`presenter_templates/view.pt`.

```xml
<head>
    <metal:block fill-slot="style_slot">
        <link rel="stylesheet" type="text/css"
            tal:define="navroot context/@@plone_portal_state/navigation_root_url"
            tal:attributes="href string:${navroot}/++resource++example.conference/conference.css"
            />
    </metal:block>
</head>
```

```{note}
Always create the resource URL relative to the navigation root as shown here, so that the URL is the same for all content objects using this view.
This allows for efficient resource caching.
```


## Registering resources with Plone's resource registries

Sometimes it is more appropriate to register a stylesheet with Plone's `portal_css` registry (or a JavaScript file with `portal_javascripts`), rather than add the registration on a per-template basis.
This ensures that the resource is available site-wide.

```{note}
It may seem wasteful to include a resource that is not be used on all pages in the global registry.
Remember, however, that `portal_css` and `portal_javascripts` will merge and compress resources, and set caching headers such that browsers and caching proxies can cache resources well.
It is often more effective to have one slightly larger file that caches well, than to have a variable number of files that may need to be loaded at different times.
```

To add a static resource file, you can use the GenericSetup {file}`cssregistry.xml` or {file}`jsregistry.xml` import steps in the `profiles/default` directory. For example, an import step to add the {file}`conference.css` file site-wide may involve a {file}`cssregistry.xml` file such as the following.

```xml
<?xml version="1.0"?>
<object name="portal_css">
 <stylesheet id="++resource++example.conference/conference.css"
    title="" cacheable="True" compression="safe" cookable="True"
    enabled="1" expression="" media="screen" rel="stylesheet" rendering="import"
    />
</object>
```

Similarly, a JavaScript resource could be imported with a {file}`jsregistry.xml` file such as the following.

```xml
<?xml version="1.0"?>
<object name="portal_javascripts">
 <javascript cacheable="True" compression="none" cookable="True"
    enabled="False" expression=""
    id="++resource++example.conference/conference.js" inline="False"/>
</object>
```


## Image resources

Images can be added to resource directories just like any other type of resource.
To use the image in a view, you can construct an `<img />` tag as follows.

```xml
<img style="float: left; margin-right: 2px; margin-top: 2px"
     tal:define="navroot context/@@plone_portal_state/navigation_root_url"
     tal:attributes="src string:${navroot}/++resource++example.conference/program.gif"
     />
```


## Content type icons

Finally, to use an image resource as the icon for a content type, simply list it in the FTI under the `content_icon` property.
For example, in {file}`profiles/default/types/example.conference.presenter.xml`, we can use the following line, presuming we have a {file}`presenter.gif` in the `example.conference` resource directory.

```xml
<property name="content_icon">++resource++example.conference/presenter.gif</property>
```
