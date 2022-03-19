---
html_meta:
  "description": "Icon registration and resolving in Plone Classic UI"
  "property=og:description": "Icon registration and resolving in Plone Classic UI"
  "property=og:title": "Icon registration and resolving"
  "keywords": "Plone, Classic UI, classic-ui, icons, svg"
---

(classic-ui-icons-label)=

# Icons

This sections describes how to work with icons in Plone 6 Classic UI.
Examples include the following.

- Bootstrap icons
- SVG inline icons
- Iconresolver


(classic-ui-icons-bootstrap-label)=

## Bootstrap Icons

Twitter Bootstrap 5 is the default CSS framework in Plone 6.
Plone uses its icons.
Check out all the available Bootstrap icons at [icons.getbootstrap.com](https://icons.getbootstrap.com/).

Icons are shipped via `plone.staticresources`.
See the file [package.json](https://github.com/plone/plone.staticresources/blob/master/package.json) of the package to get the actual version of the icons in Plone.


(classic-ui-icons-registration-label)=

## Registration

Icons are registered in Plone's registry.
This provides an option to customize the content type and Plone UI icons by overriding icons via XML.
Plone ships with the following icon registrations by default.

- [Bootstrap](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_bootstrap.xml)
- [Content Type](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_contenttype.xml)
- [Mimetype](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_mimetype.xml)
- [Language Flags](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_language_flags.xml)
- [Country Flags](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_country_flags.xml)
- [Plone](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_plone.xml)
- [Toolbar](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_plone.xml)

The icons above are made available as Plone resources.
For example, the lightning icon's resource path is `++plone++bootstrap-icons/lightning.svg`.
One could register another icon set under a new name, for example `++plone++fontawesome-icons`, and override the registrations above to use them.


(classic-ui-icons-contextual-icons-label)=

## Contextual Icons

Plone defines contextual icons, which are used in specific places in a website.
For example we have an icon registered under the name `plone.icon.plone-copy` in https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_plone.xml which points to the bootstrap `clipboard-plus` icon `++plone++bootstrap-icons/clipboard-plus.svg`.
To use a different icon than the system default, you can override the registration for `plone.icon.plone-copy` with another icon path.


(classic-ui-icons-icon-expression-label)=

## Icon expression

```{todo}
How does this work? We need an example here!
```

- The field `icon_expression` is used again to define icons for actions, contenttypes, and other purposes.
- Use the icon name for icon expressions.


(classic-ui-icons-iconresolver-label)=

## Iconresolver

The iconresolver take's an icon name (without the `plone.icon.` prefix) like `plone-copy` or `align-center` and resolves it to an actual icon.

```
http://localhost:8080/Plone/@@iconresolver/plone-copy
```

```
http://localhost:8080/Plone/@@iconresolver/align-center
```

It can be used via URL or via Python as shown below.


(classic-ui-icons-iconresolver-get-icon-url-label)=

### Get icon URL via Python expression

The `url` method of the `@@iconresolver` view returns the actual URL to the SVG icon.
The icon resolver view is globally available in templates under the name `icons`.
This can be used in a template for an `img` tag:

```xml
<img class="custom-class"
    alt="foo"
    src="${python:icons.url('alarm')}" />
```


(classic-ui-icons-iconresolver-get-icon-tag-label)=

### Get an inline icon (tag) via Python expression

The tag method is used with `tal:replace`.
It returns an SVG image.
Inline icons can be styled via CSS.
`tag_class` and `tag_alt` are used to pass in custom classes and an `alt` text.

```xml
<tal:icon
  tal:replace="structure python:icons.tag('alarm')" />

<tal:icon
  tal:replace="structure python:icons.tag('archive', tag_class='custom-class', tag_alt='foobar')" />
```

### Get inline icon (tag) in a template via traverse

```xml
<tal:icon tal:replace="structure icons/alarm" />
```

### Get an inline icon (tag) in JavaScript

```js
const baseUrl = $("body").attr("data-portal-url");
let icon = null;
if(baseUrl){
    const url = baseUrl + "/@@iconresolver";
    if (url) {
        const resp = await fetch(`${url}/${name}`);
        icon = await resp.text();
    }
}
```

[Mockup](https://github.com/plone/mockup) provides an iconResolver function, defined in core/utils.js,  which does this the same way and has a fallback for demo and testing.




(classic-ui-icons-iconresolver-fallback-label)=

### Fallback

There is a Plone icon defined as `fallback` if the name of the icon cannot be found in the registry.

Fallbacks are grouped, such as [`mimetype icons`](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_mimetype.xml).

For example, the JPEG icon is in this group and is in the mimetype group and is named `mimetype-image/jpeg`.
You can also register specific image icons.
If there is no specific icon in that group, then `mimetype-image` is used as the fallback.
