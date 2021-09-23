# Icons in Plone 6 Classic UI

- Bootstrap Icons
- SVG Inline Icons
- Iconresolver
  

# Bootstrap Icons

Bootstrap is the default CSS Framework in Plone 6. We decided to use it's icons as well. Check out all available Icons:

https://icons.getbootstrap.com/

Icons are shipped via plone.staticresources. Check out the [package.json](https://github.com/plone/plone.staticresources/blob/master/package.json) of the package to get the actual version of the icons in Plone.


# Registration

* Icons are registered in Plone's registry
* Override of icons via xml
* [Bootstrap Icons](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_bootstrap.xml)
* [Contenttypes](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_contenttype.xml)
* [Plone UI](https://github.com/plone/plone.staticresources/blob/master/src/plone/staticresources/profiles/default/registry/icons_plone.xml)


# Customization

* Add custom icons
* Override some of the icons
* TODO


# Icon Font

* TODO
* Setup profile to install icon font
* Usage as known from e.g. Font Awesome


# Iconresolver

## Get Icon URL

URL method of @@icons view returns the actual URL to the SVG icon. This can be used e.g. in an img tag.

```
<img src="" tal:attributes="src python:icons.url('alarm')" class="custom-class" alt="foo" />
```

## Get Icon Tag

Tag method is used with tal:replace and returns an entire inline SVG image. tag_class and tag_alt is used to pass in custom classes and an alt text.

```
<tal:icon tal:replace="structure python:icons.tag('archive', tag_class='custom-class', tag_alt='foobar')" />
```
