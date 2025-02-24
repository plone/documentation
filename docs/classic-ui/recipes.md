---
myst:
  html_meta:
    "description": "Collection of useful recipes for working with the Classic UI in Plone 6."
    "property=og:description": "Learn how to customize and enhance the Classic UI experience in Plone 6."
    "property=og:title": "Classic UI Recipes in Plone"
    "keywords": "Plone, Classic UI, Customization, Recipes, Plone 6"
---

(classic-ui-recipes-label)=

# Recipes

This chapter provides several recipes for working with the Classic UI in Plone 6.

(classic-ui-recipes-add-custom-classes-to-body-label)=

## Add Custom Classes to the `body` Element

Body classes are generated in the `LayoutPolicy.bodyClass` method in the module `plone.app.layout.globals.layout`.
It allows you to create your own body classes using named adapters.

### **1. Creating a Custom Body Class Adapter**

First, create a Python class to define additional body classes:

```python
from plone.app.layout.globals.interfaces import IBodyClassAdapter
from zope.interface import implementer

@implementer(IBodyClassAdapter)
class CustomBodyClasses:
    """Additional body classes adapter."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_classes(self, template, view):
        return ["additional-class", "another-css-class"]
