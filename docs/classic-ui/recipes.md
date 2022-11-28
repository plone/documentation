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
