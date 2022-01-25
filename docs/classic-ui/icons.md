---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

(classic-ui-icons-label)=

# Icons in Plone 6 Classic UI

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
This provides an option to customize the contenttype and Plone UI icons by overriding icons via XML.

- [Bootstrap icons](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_bootstrap.xml)
- [contenttypes](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_contenttype.xml)
- [Plone UI](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_plone.xml)


(classic-ui-icons-contextual-icons-label)=

## Contextual Icons

We can define contextual icons to be used in specific places in a website while preserving the default system icons to be used elsewhere throughout the site.
To use a different icon than the system default, you would override it without touching the system icon.
 
You should avoid replacing system icons because it may result in an inconsistent user interface.

The specific icon name is based on the usage in the system.
For example the copy icon is named `plone.icon.plone-copy`.


(classic-ui-icons-icon-expression-label)=

## Icon expression

- The field `icon_expression` is used again to define icons for actions, contenttypes, and other purposes.
- Use the icon name for icon expressions.


(classic-ui-icons-customization-label)=

## Customization

```{admonition} TODO
:class: warning

Add content for this section
```

- Add custom icons
- Override some of the icons


(classic-ui-icons-icon-font-label)=

## Icon font

```{admonition} TODO
:class: warning

Add content for this section
```

- Set up a profile to install the icon font.
- Use Font Awesome as an example.


(classic-ui-icons-iconresolver-label)=

## Iconresolver

```{admonition} TODO
:class: warning

What is `iconresolver`?
Add to Glossary.
```


(classic-ui-icons-iconresolver-get-icon-url-label)=

### Get Icon URL

URL method of `@@icons` view returns the actual URL to the SVG icon.
This can be used in an HTML `img` tag, for example.

```xml
<img src="" tal:attributes="src python:icons.url('alarm')" class="custom-class" alt="foo" />
```


(classic-ui-icons-iconresolver-get-icon-tag-label)=

### Get Icon Tag

The tag method is used with `tal:replace`.
It returns an SVG image.
Inline icons can be styled via CSS.
`tag_class` and `tag_alt` is used to pass in custom classes and an `alt` text.

```xml
<tal:icon tal:replace="structure python:icons.tag('archive', tag_class='custom-class', tag_alt='foobar')" />
```

(classic-ui-icons-iconresolver-resource-path-label)=

### Resource Path

SVG files are available from the resource path.
For example, the lightning icon's resource path is `++plone++bootstrap-icons/lightning.svg`.


(classic-ui-icons-iconresolver-fallback-label)=

### Fallback

There is a Plone icon defined as `fallback` if the name of the icon cannot be found in the registry.

Fallbacks are grouped, such as [`mimetype icons`](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_mimetype.xml).

For example, the JPEG icon is in this group and is in the mimetype group and is named `mimetype-image/jpeg`.
You can also register specific image icons.
If there is no specific icon in that group, then `mimetype-image` is used as the fallback.
