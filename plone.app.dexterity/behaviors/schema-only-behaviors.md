---
myst:
  html_meta:
    "description": "Schema-only behaviors using annotations or attributes for content types in Plone"
    "property=og:description": "Schema-only behaviors using annotations or attributes for content types in Plone"
    "property=og:title": "Schema-only behaviors using annotations or attributes for content types in Plone"
    "keywords": "Plone, schema-only, behaviors, annotations, attributes, content types"
---

# Schema-only behaviors using annotations or attributes

This chapter describes how to write behaviors that provide schema fields.

Oftentimes, we simply want a behavior to be a reusable collection of form fields.
Integrators can then compose their types by combining different schemata.
Writing the behavior schema is no different than writing any other schema interface.
But how and where do we store the values?
By default, `plone.behavior` provides two alternatives.


## Using annotations

Annotations, as provided by the [`zope.annotation`](https://pypi.org/project/zope.annotation/) package, are a standard means of storing of key/value pairs on objects.
In the default implementation (so-called `attribute annotation`), the values are stored in a BTree on the object called `__annotations__`.
The raw annotations API involves adapting the object to the `IAnnotations` interface, which behaves like a dictionary, and storing values under unique keys here.
`plone.behavior` comes with a special type of factory that lets you adapt an object to its behavior interface to get an adapter providing this interface, on which you can get and set values, which are eventually stored in annotations.

We've already seen an example of this factory.

```xml
<plone:behavior
    title="Reviewers"
    description="The ability to assign a list of official and/or unofficial reviewers to an item, granting those users special powers."
    provides=".reviewers.IReviewers"
    factory="plone.behavior.AnnotationStorage"
    marker=".reviewers.IReviewersMarkere"
    />
```

Here `plone.behavior.AnnotationStorage` is a behavior factory that can be used by any behavior with an interface that consists entirely of `zope.schema` fields.
It stores those items in object annotations, saving you the trouble of writing your own annotation storage adapter.
If you adapt an object for which the behavior is enabled to the behavior interface, you will be able to read and write values off the resultant adapter as usual.


## Storing attributes

This approach is convenient, but there is another approach that is even more convenient, and, contrary to what you may think, may be more efficient: store the attributes of the schema interface directly on the content object.

As an example, here's the standard `IRelatedItems` behavior from `plone.app.dexerity`.

```xml
<plone:behavior
    title="Related items"
    description="Adds the ability to assign related items"
    provides=".related.IRelatedItems"
    for="plone.dexterity.interfaces.IDexterityContent"
    />
```

The following is the `IRelatedItems` schema.

```python
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.directives import form
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice,
from z3c.relationfield.schema import RelationList
from zope.interface import provider


@provider(IFormFieldProvider)
class IRelatedItems(model.Schema):
    """Behavior interface to make a type support related items.
    """

    form.fieldset("categorization", label="Categorization",
                  fields=["relatedItems"])

    relatedItems = RelationList(
        title="Related Items",
        default=[],
        value_type=RelationChoice(title="Related",
                      source=ObjPathSourceBinder()),
        required=False,
        )
```

This is a standard schema using `plone.autoform.directives`.
However, notice the lack of a behavior factory.
This is a directly provided "marker" interface, except that it has attributes, and so it is not actually a marker interface.
The result is that the `relatedItems` attribute will be stored directly onto a content object when first set (usually in the add form).

This approach has a few advantages:

-   There is no need to write or use a separate factory, so it is a little easier to use.
-   The attribute is available on the content object directly, so you can write `context/relatedItems` in a TAL expression, for example.
    This does require that it has been set at least once, though.
    If the schema is used in the type's add form, that will normally suffice, but old instances of the same type may not have the attribute and could raise an `AttributeError.`
-   If the value is going to be used frequently, and especially if it is read when viewing the content object, storing it in an attribute is more efficient than storing it in an annotation.
    This is because the `__annotations__` BTree is a separate persistent object which has to be loaded into memory, and may push something else out of the ZODB cache.

The possible disadvantages are:

-   The attribute name may collide with another attribute on the object, either from its class, its base schema, or another behavior.
    Whether this is a problem in practice depends largely on whether the name is likely to be unique.
    In most cases, it will probably be sufficiently unique.
-   If the attribute stores a large value, it will increase memory usage, as it will be loaded into memory each time the object is fetched from the ZODB.
    However, you should use blob to store large values and BTrees to store many values anyway.
    Loading an object with a blob or BTree does not mean loading the entire data, so the memory overhead does not occur unless the whole blob or BTree is actually used.

```{note}
"The moral of this story? BTrees do not always make things more efficient!" ~ Laurence Rowe
```
