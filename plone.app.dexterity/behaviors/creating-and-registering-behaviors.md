---
myst:
  html_meta:
    "description": "How to create a basic behavior that provides form fields for content types in Plone"
    "property=og:description": "How to create a basic behavior that provides form fields for content types in Plone"
    "property=og:title": "How to create a basic behavior that provides form fields for content types in Plone"
    "keywords": "Plone, behaviors, content types, create, register"
---

# Creating and registering behaviors

This chapter describes how to create a basic behavior that provides form fields.

The following example is based on the [`collective.gtags`](https://pypi.org/project/collective.gtags/) product.
It comes with a behavior that adds a `tags` field to the `Categorization` fieldset, storing the actual tags in the Dublin Core `Subject` field.

`collective.gtags` is a standard package, with a `configure.zcml`, a GenericSetup profile, and a number of modules.
We won't describe those here, though, since we are only interested in the behavior.

First, there are a few dependencies in {file}`setup.py`.

```python
install_requires=[
    # ...,
    "plone.behavior",
    "zope.schema",
    "zope.interface",
    "zope.component",
],
```

Next, we have {file}`behaviors.zcml`, which is included from {file}`configure.zcml`, and contains all the necessary configuration to set up the behaviors.

```xml
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="collective.gtags">

    <include package="plone.behavior" file="meta.zcml" />

    <plone:behavior
        title="GTags"
        description="Use the Dublin Core Subject (keywords) field for Google Code like tags."
        provides=".behaviors.ITags"
        factory=".behaviors.Tags"
        marker=".behaviors.ITagsMarker"
        />

</configure>
```

We first include the `plone.behavior meta.zcml` file, so that we get access to the `<plone:behavior />` ZCML directive.

The behavior itself is registered with the `<plone:behavior />` directive.
We set a `title` and a `description`, and then specify the `behavior interface` with the `provides` attribute.
This attribute is required, and is used to construct the unique name for the behavior.
In this case, the behavior name is `collective.gtags.behaviors.ITags`, the full dotted name to the behavior interface.
When the behavior is enabled for a type, it will be possible to adapt instances of that type to `ITags`.
That adaptation will invoke the factory specified by the `factory` attribute.

The following is the {file}`behaviors.py` module.

```python
"""Behaviors to assign tags (to ideas).

Includes a form field and a behavior adapter that stores the data in the
standard Subject field.
"""

from plone.dexterity.interfaces import DexterityContent
# if your package was made with mr.bob, add your MessageFactory as shown:
from collective.mypackage import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class ITags(model.Schema):
    """Add tags to content
    """

    directives.fieldset(
            "categorization",
            label=_("Categorization"),
            fields=("tags",),
        )

    tags = Tags(
            title=_("Tags"),
            description=_("Applicable tags"),
            required=False,
            allow_uncommon=True,
        )


@implementer(ITags)
@adapter(IDexterityContent)
class Tags(object):
    """Store tags in the Dublin Core metadata Subject field. This makes
    tags easy to search for.
    """

    def __init__(self, context):
        self.context = context

    # the properties below are not necessary the first time when you just want to see your added field(s)
    @property
    def tags(self):
        return set(self.context.Subject())
    @tags.setter
    def tags(self, value):
        if value is None:
            value = ()
        self.context.setSubject(tuple(value))
```

We first define the `ITags` interface, which is also the behavior interface.
Here we define a single attribute, `tags`, but we could also have added methods and additional fields if required.
Naturally, these need to be implemented by the behavior adapter.

Since we want this behavior to provide form fields, we derive the behavior interface from `model.Schema` and set form hints using `plone.supermodel.directives`.
We also mark the `ITags` interface with `IFormFieldProvider` to signal that it should be processed for form fields by the standard forms.
See the {doc}`Dexterity Developer Manual <../index>` for more information about setting form hints in schema interfaces.

If your behavior does not provide form fields, you can just derive from `zope.interface.Interface` and omit the `alsoProvides()` line.

Next, we write the class that implements the behavior adapter and acts as the adapter factory.
Notice how it implements the behavior interface (`ITags`), and adapts a broad interface `(IDexterityContent`).
The behavior cannot be enabled on types not supporting this interface.
In many cases, you will omit the `adapter()` line, provided your behavior is generic enough to work on any context.

The adapter is otherwise identical to any other adapter.
It implements the interface, here by storing values in the `Subject` field.
