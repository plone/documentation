---
myst:
  html_meta:
    "description": "Form configuration with schema hints using directives in Plone"
    "property=og:description": "Form configuration with schema hints using directives in Plone"
    "property=og:title": "Form configuration with schema hints using directives in Plone"
    "keywords": "Plone, form, configuration, schema, hints, directives"
---

# Form configuration with schema hints using directives

Dexterity uses the directives in [`plone.autoform`](https://pypi.org/project/plone.autoform/) and [`plone.supermodel`](https://pypi.org/project/plone.supermodel/) packages to configure its [`z3c.form`](https://z3cform.readthedocs.io/en/latest/)-based add and edit forms.
A directive annotates a schema with "form hints", which are used to configure the form when it gets generated from the schema.

The easiest way to apply form hints in Python code is to use the directives from [`plone.autoform`](https://pypi.org/project/plone.autoform/) and `plone.supermodel`.
For the directives to work, the schema must derive from `plone.supermodel.model.Schema`.

Directives can be placed anywhere in the class body (annotations are made directly on the class).
By convention they are kept next to the fields to which they apply.

For example, here is a schema that omits a field.

```python
from plone.autoform import directives
from plone.supermodel import model
from zope import schema


class ISampleSchema(model.Schema):

    title = schema.TextLine(title="Title")

    directives.omitted("additionalInfo")
    additionalInfo = schema.Bytes()
```

The form directives take parameters in the form of a list of field names, or a set of field name/value pairs as keyword arguments.
Each directive can be used zero or more times.

There are two kinds of directives.

-   Appearance related directives
-   Security related directives


## Appearance related directives

`plone.autoform.directives` provides the following.

| Name         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| - | -|
| widget       | Specify an alternate widget for a field. Pass the field name as a key and a widget as the value. The widget can either be a `z3c.form` widget instance or a string giving the dotted name to one.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| omitted      | Omit one or more fields from forms. Takes a sequence of field names as parameters.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| mode         | Set the widget mode for one or more fields. Pass the field name as a key and the string `"input"`, `"display"`, or `"hidden"` as the value.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| order_before | Specify that a given field should be rendered before another. Fields can only be ordered if they are in the same fieldset, otherwise order directive is ignored. Pass the field name as a key and name of the other field as a value. If the other field is in a supplementary schema such as from a behavior, then its name will be, for example `IOtherSchema.other_field_name`. If the other field is from the same schema, its name can be abbreviated by a leading dot, for example `.other_field_name`. If the other field is is used without a prefix, it is looked up from the main schema, for example `other_field_name`. Alternatively, pass the string `*` to put a field first in the form's fieldset. |
| order_after  | The inverse of `order_before()`, putting a field after another. It works almost similar to `order_before`, except  passing `*` will put the field at the end of the fieldsets form.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

`plone.supermodel.directives` provides the following.

| Name     | Description                                                                                                                                               |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| fieldset | Creates a new (or reuses an existing) fieldset (rendered in Plone as a tab on the edit form).                                                             |
| primary  | Designate a given field as the primary field in the schema. This is not used for form rendering, but is used for WebDAV marshaling of the content object. |

The code sample below illustrates each of these directives.

```python
from plone.autoform import directives
from plone.supermodel.directives import fieldset
from plone.supermodel.directives import primary
from plone.supermodel import model
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from zope import schema


class ISampleSchema(model.Schema):

    # A fieldset with id "extra" and label "Extra information" containing
    # the "footer" and "dummy" fields. The label can be omitted if the
    # fieldset has already been defined.

    fieldset("extra",
        label="Extra information",
        fields=["footer", "dummy"]
    )

    # Here a widget is specified as a dotted name.
    # The body field is also designated as the primary field for this schema

    directives.widget(body="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    primary("body")
    body = schema.Text(
        title="Body text",
        required=False,
        default="Body text goes here"
    )

    # The widget can also be specified as an object

    directives.widget(footer=WysiwygFieldWidget)
    footer = schema.Text(
        title="Footer text",
        required=False
    )

    # An omitted field.
    # Use directives.omitted("a", "b", "c") to omit several fields

    directives.omitted("dummy")
    dummy = schema.Text(
        title="Dummy"
    )

    # A field in "hidden" mode

    directives.mode(secret="hidden")
    secret = schema.TextLine(
        title="Secret",
        default="Secret stuff"
    )

    # This field is moved before the "description" field of the standard
    # IDublinCore behavior, if this is in use.

    directives.order_before(importantNote="IDublinCore.description")
    importantNote = schema.TextLine(
        title="Important note",
    )
```


## Security related directives

The security directives in the `plone.autoform.directives` module are shown below.
Note that these are also used to control reading and writing of fields on content instances.

| Name             | Description                                                                                                                                                                                                                             |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| read_permission  | Set the name (ZCML-style) of a permission required to read the field's value. Pass the field name as a key and the permission name as a string value. Among other things, this controls the field's appearance in display forms.        |
| write_permission | Set the name (ZCML-style) of a permission required to write the field's value. Pass the field name as a key and the permission name as a string value. Among other things, this controls the field's appearance in add and edit forms. |

The code sample below illustrates each of these directives.

```python
from plone.autoform import directives
from plone.supermodel import model
from zope import schema

class ISampleSchema(model.Schema):

    # This field requires the "cmf.ReviewPortalContent" permission
    # to be read and written

    directives.read_permission(reviewNotes="cmf.ReviewPortalContent")
    directives.write_permission(reviewNotes="cmf.ReviewPortalContent")
    reviewNotes = schema.Text(
        title="Review notes",
        required=False,
    )
```
