---
myst:
  html_meta:
    "description": "Plone content type references between content objects"
    "property=og:description": "Plone content type references between content objects"
    "property=og:title": "Plone content type references between content objects"
    "keywords": "Plone, content types, references, content objects"
---

# References

This chapter describes how to work with references between content objects.

References are a way to maintain links between content that remain valid, even if one or both of the linked items are moved or renamed.

Under the hood, Dexterity's reference system uses [`five.intid`](https://pypi.org/project/five.intid/), a Zope 2 integration layer for [`zope.intid`](https://pypi.org/project/zope.intid/), to give each content item a unique integer ID.
These are the bases for relationships maintained with the [`zc.relationship`](https://pypi.org/project/zc.relationship/) package, which in turn is accessed via an API provided by [`z3c.relationfield`](https://pypi.org/project/z3c.relationfield/), integrated into Zope 2 with [`plone.app.relationfield`](https://pypi.org/project/plone.app.relationfield/).
For most purposes, you need only to worry about the `z3c.relationfield` API, which provides methods for finding source and target objects for references and searching the relationship catalog.

References are most commonly used in form fields with a selection or content browser widget.
Dexterity comes with a standard widget in [`plone.formwidget.contenttree`](https://pypi.org/project/plone.formwidget.contenttree/) configured for the `RelationList` and `RelationChoice` fields from `z3c.relationfield`.

To illustrate the use of references, we will allow the user to create a link between a `Session` and its `Presenter`.
Since Dexterity already ships with and installs `plone.formwidget.contenttree` and `z3c.relationfield`, we do not need to add any further setup code, and we can use the field directly in {file}`session.py`:

```python
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from example.conference.presenter import IPresenter

class ISession(form.Schema):
    """A conference session. Sessions are managed inside Programs.
    """

    presenter = RelationChoice(
        title=_("Presenter"),
        source=ObjPathSourceBinder(object_provides=IPresenter.__identifier__),
        required=False,
    )
```

```{note}
Remeber that `plone.app.relationfield` needs to be installed to use any `RelationChoice` or `RelationList` field.
```

To allow multiple items to be selected, we could have used a `RelationList` as shown:

```python
relatedItems = RelationList(
    title="Related Items",
    default=[],
    value_type=RelationChoice(title=_("Related"),
                              source=ObjPathSourceBinder()),
    required=False,
)
```

The `ObjPathSourceBinder` class is an `IContextSourceBinder` that returns a vocabulary with content objects as values, object titles as term titles, and object paths as tokens.

You can pass keyword arguments to the constructor for `ObjPathSourceBinder()` to restrict the selectable objects.
Here we demand that the object must provide the `IPresenter` interface.
The syntax is the same as that used in a catalog search, except that only simple values and lists are allowed (in other words, you can't use a dict to specify a range or values for a field index).

If you want to restrict the folders and other content shown in the content browser, you can pass a dictionary with catalog search parameters (and here, any valid catalog query will do) as the first non-keyword argument (`navigation_tree_query`) to the `ObjPathSourceBinder()` constructor.

You can also create the fields in an XML schema.
However you have to provide a pre-baked source instance.
If you are happy with not restricting folders shown, you can use those which `plone.formwidget.contenttree` makes for you.
For example:

```xml
<field name="links" type="plone.app.relationfield.RelationList">
    <title>Related Items</title>
    <value_type type="plone.app.relationfield.Relation">
        <title>Related</title>
        <source>plone.formwidget.contenttree.obj_path_src_binder</source>
    </value_type>
</field>
```

```{versionadded} 4.3.2
The pre-baked source binders were added in `plone.formwidget.contenttree` 1.0.7, which ships with Plone 4.3.2+.
```

If you want to use a different widget, you can use the same source (or a custom source that has content objects as values) with something such as the autocomplete widget.
The following line added to the interface will make the presenter selection similar to the `organizer` selection widget that we showed in the previous section.

```python
from plone.autoform import directives
directives.widget('presenter', AutocompleteFieldWidget)
```

Once the user has created some relationships, the value stored in the relation field is a `RelationValue` object.
This provides various attributes, including:

`from_object`
: The object from which the relationship is made.

`to_object`
: The object to which the relationship is made.

`from_id` and `to_id`
: The integer IDs of the source and target.

`from_path` and `to_path`
: The path of the source and target.

The `isBroken()` method can be used to determine if the relationship is broken.
This normally happens if the target object is deleted.

To display the relationship on our form, we can either use a display widget on a *display view*, or use this API to find the object and display it.
We'll do the latter in {file}`templates/sessionview.pt`.

```xml
<div tal:condition="context/presenter">
    <label i18n:translate="presenter">Presenter:</label>
    <span tal:content="context/presenter/to_object/Title | nothing" />
</div>
```


## Back references

To retrieve back references (all objects pointing to a particular object using the specified attribute) you can't simply use `from_object` or `from_path`, because the source object is stored in the relation without acquisition wrappers.
You should use the `from_id` method, which searches the object in the `IntId` catalog:

```python
from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog

def back_references(source_object, attribute_name):
    """
    Return back references from source object on specified attribute_name
    """
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    result = []
    for rel in catalog.findRelations(
                dict(to_id=intids.getId(aq_inner(source_object)),
                from_attribute=attribute_name)
    ):
        obj = intids.queryObject(rel.from_id)
        if obj is not None and checkPermission('zope2.View', obj):
            result.append(obj)
    return result
```

This method does not check effective and expiration dates or content language.
