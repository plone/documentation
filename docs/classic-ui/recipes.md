---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(classic-ui-recipes-label)=

# Recipes

This chapter provides several recipes to working with the Classic UI in Plone 6.


(classic-ui-recipes-add-custom-classes-to-body-label)=

## Add custom classes to the `body` element

Body classes are generated in the `LayoutPolicy.bodyClass` method in the module `plone.app.layout.globals.layout`.
It allows you to create your own body-classes using named adapters.

First create a class as follows.

```python
from plone.app.layout.globals.interfaces import IBodyClassAdapter

@implementer(IBodyClassAdapter)
class CustomBodyClasses(object):
    """Additional body classes adapter."""
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_classes(self, template, view):
        return ["additional-class", "another-css-class"]
```

Then register the adapter in ZCML.

```xml
<adapter
    factory=".custombodyclasses.CustomBodyClasses"
    for="* *"
    name="myproject-customclasses"
/>
```

(classic-ui-recipes-customize-pattern-options)=

## Customize `pattern_options`

This example shows how to customize the {menuselection}`Favorites` menu in the contentbrowser pattern:

First create a multiadapter:

```{code-block} python
:linenos:

    from plone import api
    from z3c.form.interface import IValue
    from zope.interface import implementer


    @implementer(IValue)
    class ContentbrowserPatternOptions:

        def __init__(self, context, request, form, field, widget):
            self.context = context
            self.request = request
            self.form = form
            self.field = field
            self.widget = widget

        def get(self):
            portal_path = "/".join(api.portal.get().getPhysicalPath())
            return {
                "favorites": [
                    {"title": "my favorite folder", "path": f"{portal_path}/path/to/my/favorite/folder"},
                    {"title": "Portal", "path": portal_path},
                ],
            }
```

And register it with zcml:

```xml
<adapter factory=".ContentbrowserPatternOptions"
         for="*
              *
              *
              *
              plone.app.z3cform.interfaces.IContentBrowserWidget"
         name="pattern_options">
```
