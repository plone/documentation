# Icons in Plone 6 Classic UI

- Bootstrap Icons
- SVG Inline Icons
- Iconresolver

## Bootstrap Icons

Bootstrap is the default CSS Framework in Plone 6.
We decided to use it's icons as well.
Check out all available Icons at [icons.getbootstrap.com](https://icons.getbootstrap.com/).

Icons are shipped via plone.staticresources.
Check out the [package.json](https://github.com/plone/plone.staticresources/blob/master/package.json) of the package to get the actual version of the icons in Plone.

## Registration

- Icons are registered in Plone's registry
- Registrered to override of icons via xml
- Option to customize UI and contenttype icons
- [Bootstrap Icons](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_bootstrap.xml)
- [Contenttypes](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_contenttype.xml)
- [Plone UI](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_plone.xml)

## Contextual Icons

We definde contextual icons. If you don't like e.g. the share icon - override it without touching the share icon used by the system.

- Icons like copy, cut, paste
- Identical function all over the site
- That's why we reuse those icons
- Specific icon name is based on the usage in the system

## Icon expression

- `icon_expression` field is used again to define icons (e.g. for actions, contenttypes)
- Use icon name for icon expressions

## Customization

- Add custom icons
- Override some of the icons
- TODO

## Icon Font

- Setup profile to install icon font
- Usage as known from e.g. Font Awesome
- TODO

## Iconresolver

### Get Icon URL

URL method of @@icons view returns the actual URL to the SVG icon. This can be used e.g. in an img tag.

```HTML
<img src="" tal:attributes="src python:icons.url('alarm')" class="custom-class" alt="foo" />
```

### Get Icon Tag

Tag method is used with `tal:replace` and returns an entire inline SVG image.
Inline icons can be styled via CSS.
`tag_class` and `tag_alt` is used to pass in custom classes and an alt text.

```HTML
<tal:icon tal:replace="structure python:icons.tag('archive', tag_class='custom-class', tag_alt='foobar')" />
```

### Resource Path

SVG Files are avaiblae as resource: `++plone++bootstrap-icons/lightning.svg`

### Fallback

- There is a Plone icon defined as fallback if icon name is not found
- There are fallback groups e.g. for [mimetype icons](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_mimetype.xml)
- JPEG icon is e.g. `mimetype-image/jpeg`
- You can register specific icons
- If there is no specific icon mimetype-image is used as fallback
