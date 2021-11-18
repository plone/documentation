# Add custom classes to the `body` element

Body classes are generated in the ``LayoutPolicy.bodyClass` method in mdoule `plone.app.layout.globals.layout`.
Contained is a feature to plugin in own body-classes using named adapters.

Create a class like so:

```Python:
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

Then register the adapter in ZCML:

```XML
<adapteer
    factory=".custombodyclasses.CustomBodyClasses"
    for="* *"
    name="myproject-customclasses"
/>
```
