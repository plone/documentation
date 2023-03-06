---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# References

**How to work with references between content objects**

References are a way to maintain links between content that remain valid
even if one or both of the linked items are moved or renamed.

Under the hood, Dexterity’s reference system uses [five.intid], a Zope
2 integration layer for [zope.intid], to give each content item a unique
integer id. These are the basis for relationships maintained with the
[zc.relationship] package, which in turn is accessed via an API
provided by [z3c.relationfield], integrated into Zope 2 with
[plone.app.relationfield]. For most purposes, you need only to worry
about the `z3c.relationfield` API, which provides methods for finding
source and target objects for references and searching the relationship
catalog.

References are most commonly used in form fields with a selection or
content browser widget. Dexterity comes with a standard widget in
[plone.formwidget.contenttree] configured for the `RelationList` and
`RelationChoice` fields from `z3c.relationfield`.

To illustrate the use of references, we will allow the user to create a
link between a `Session` and its `Presenter`. Since Dexterity already
ships with and installs `plone.formwidget.contenttree` and
`z3c.relationfield`, we do not need to add any further setup code, and
we can use the field directly in `session.py`:

```
...

from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
...

from example.conference.presenter import IPresenter

class ISession(form.Schema):
    """A conference session. Sessions are managed inside Programs.
    """
    ...

    presenter = RelationChoice(
        title=_(u"Presenter"),
        source=ObjPathSourceBinder(object_provides=IPresenter.__identifier__),
        required=False,
    )
```

:::{Note}
Remeber that [plone.app.relationfield] needs to be installed to use any
RelationChoice or RelationList field.
:::

To allow multiple items to be selected, we could have used a
`RelationList` like:

```
relatedItems = RelationList(
    title=u"Related Items",
    default=[],
    value_type=RelationChoice(title=_(u"Related"),
                              source=ObjPathSourceBinder()),
    required=False,
)
```

The `ObjPathSourceBinder` class is an `IContextSourceBinder` that returns
a vocabulary with content objects as values, object titles as term
titles and object paths as tokens.

You can pass keyword arguments to the constructor for
`ObjPathSourceBinder()` to restrict the selectable objects. Here, we
demand that the object must provide the `IPresenter` interface. The
syntax is the same as that used in a catalog search, except that only
simple values and lists are allowed (e.g. you can’t use a dict to
specify a range or values for a field index).

If you want to restrict the folders and other content shown in the
content browser, you can pass a dictionary with catalog search
parameters (and here, any valid catalog query will do) as the first
non-keyword argument (`navigation_tree_query`) to the
`ObjPathSourceBinder()` constructor.

You can also create the fields in an XML schema, however you have to provide a
pre-baked source instance. If you are happy with not restricting folders shown,
you can use some that `plone.formwidget.contenttree` makes for you. For example:

```
<field name="links" type="plone.app.relationfield.RelationList">
    <title>Related Items</title>
    <value_type type="plone.app.relationfield.Relation">
        <title>Related</title>
        <source>plone.formwidget.contenttree.obj_path_src_binder</source>
    </value_type>
</field>
```

:::{note}
The pre-baked source binders were added in plone.formwidget.contenttree
1.0.7, which ships with Plone 4.3.2+.
:::

If you want to use a different widget, you can use the same source (or a
custom source that has content objects as values) with something like
the autocomplete widget. The following line added to the interface will
make the presenter selection similar to the `organizer` selection widget
we showed in the previous section:

```python
from plone.autoform import directives
directives.widget('presenter', AutocompleteFieldWidget)
```

Once the user has created some relationships, the value stored in the
relation field is a `RelationValue` object. This provides various
attributes, including:

- `from_object`, the object from which the relationship is made;
- `to_object`, the object to which the relationship is made;
- `from_id` and `to_id`, the integer ids of the source and target;
- `from_path` and `to_path`, the path of the source and target.

The `isBroken()` method can be used to determine if the relationship is
broken. This normally happens if the target object is deleted.

To display the relationship on our form, we can either use a display
widget on a *display view*, or use this API to find the object and
display it. We’ll do the latter in `templates/sessionview.pt`:

```html
<div tal:condition="context/presenter">
    <label i18n:translate="presenter">Presenter:</label>
    <span tal:content="context/presenter/to_object/Title | nothing" />
</div>
```

## Back references

To retrieve back-reference (all objects pointing to particular object using specified attribute) you can't simply use `from_object` or `from_path`, because source object is stored in the relation without acquisition wrappers.
You should use `from_id` and `helper` method, which search the object in the `IntId` catalog:

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

Please note, this method does not check effective and expiration date or content language.

Original issue: [http://code.google.com/p/dexterity/issues/detail?id=234](http://code.google.com/p/dexterity/issues/detail?id=234)

[five.intid]: http://pypi.python.org/pypi/five.intid
[plone.app.relationfield]: http://pypi.python.org/pypi/plone.app.relationfield
[plone.formwidget.contenttree]: http://pypi.python.org/pypi/plone.formwidget.contenttree
[z3c.relationfield]: http://pypi.python.org/pypi/z3c.relationfield
[zc.relationship]: http://pypi.python.org/pypi/zc.relationship
[zope.intid]: http://pypi.python.org/pypi/zope.intid
