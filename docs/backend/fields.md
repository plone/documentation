---
myst:
  html_meta:
    "description": "Fields are objects that have properties and types, and comprise a schema."
    "property=og:description": "Fields are objects that have properties and types, and comprise a schema."
    "property=og:title": "Fields"
    "keywords": "Fields, schema, autoform, supermodel, XML"
---

(backend-fields-label)=

# Fields

This chapter describes the standard schema fields for Plone forms and content types.

The following tables show the most common field types for use in {doc}`/classic-ui/forms` and Dexterity {doc}`/backend/content-types/index`.
See {doc}`schemas </backend/schemas>` for information about how fields compose a schema for a form or content type data model.

```{tip}
In VS Code editor, you can install the [Plone Snippets](https://marketplace.visualstudio.com/items?itemName=Derico.plone-vs-snippets) extension.
This will give you snippets for most fields, widgets, and autoform directives in Python and XML based schemas.
```

## Field properties

You can initialize fields by passing properties into their constructors.
To avoid repeating the available properties for each field, we'll list them once here, grouped into the interfaces that describe them.
You'll see those interfaces again in the tables below that describe the various field types.
Refer to the table below to see what properties a particular interface implies.

| Interface | Property | Type | Description |
| - | - | - | - |
| `IField` | `title` | `int` | The title of the field. Used in the widget. |
| | `description` | `unicode` | A description for the field. Used in the widget. |
| | `required` | `bool` | Whether or not the field is required. Used for form validation. The default is `True`. |
| | `readonly` | `bool` | Whether or not the field is read only. Default is `False`. |
| | `default` | | The default value for the field. Used in forms and sometimes as a fallback value. Must be a valid value for the field if set. The default is `None`.|
| | `defaultFactory` | | The default factory method for the field. Used in forms and sometimes as a fallback value. This is a name of a method which returns a dynamic default value.|
| | `missing_value` | | A value that represents "this field is not set." Used by form validation. Defaults to `None`. For lists and tuples, it is sometimes useful to set this to an empty list or tuple. |
| `IMinMaxLen` | `min_length` | `int` | The minimum required length or minimum number of elements. Used for `string`, sequence, mapping, or `set` fields. Default is `0`. |
| | `max_length `| `int` | The maximum allowed length or maximum number of elements. Used for `string`, sequence, mapping, or `set` fields. Default is `None` (no check). |
| `IMinMax` | `min` | | The minimum allowed value. Must be a valid value for the field, for example, an `int` field should be an integer. Default is `None` (no check). |
| | `max` | | The maximum allowed value. Must be a valid value for the field, for example an `int` field should be an integer. Default is `None` (no check). |
| `ICollection` | `value_type` | | Another `Field` instance that describes the allowable values in a list, tuple, or other collection. Must be set for any collection field. One common usage is to set this to a `Choice` to model a multi-selection field with a {doc}`vocabulary </backend/vocabularies>`. |
| | `unique` | `bool` | Whether or not values in the collection must be unique. Usually not set directly. Use a `Set` or `Frozenset` to guarantee uniqueness in an efficient way. |
| `IDict` | `key_type` | | Another `Field` instance that describes the allowable keys in a dictionary. Similar to the `value_type` of a collection. Must be a `Set`. |
| | `value_type` | | Another `Field` instance that describes the allowable values in a dictionary. Similar to the `value_type` of a collection. Must be a `Set`. |
| `IObject` | `schema` | `Interface` | An interface that must be provided by any object stored in this field. |
| `IRichText` | `default_mime_type` | `str` | Default MIME type for the input text of a rich text field. Defaults to `text/html`. |
| | `output_mime_type` | `str` | Default output MIME type for the transformed value of a rich text field. Defaults to `text/x-html-safe`. There must be a transformation chain in the `portal_transforms` tool that can transform from the input value to the output value for the `output` property of the `RichValue` object to contain a value. |
| | `allowed_mime_types` | `tuple` | A list of allowed input MIME types. The default is `None`, in which case the site-wide settings from the {guilabel}`Markup` control panel will be used. |

See [`IField` interface](https://zopeschema.readthedocs.io/en/latest/api.html#zope.schema.interfaces.IField) and [`field` implementation](https://zopeschema.readthedocs.io/en/latest/api.html#field-implementations) in `zope.schema` documentation for details.


## Field types

The following tables describe the most commonly used field types, grouped by the module from which they can be imported.


(fields-in-zope-schema-label)=

### Fields in `zope.schema`

| Name | Type | Description | Properties |
| - | - | - | - |
| `Choice` | n/a | Used to model selection from a vocabulary, which must be supplied. Often used as the `value_type` of a selection field. The value type is the value of the terms in the vocabulary. | See {doc}`/backend/vocabularies`. |
| `Bytes` | `str` | Used for binary data. | `IField`, `IMinMaxLen` |
| `ASCII` | `str` | ASCII text (multi-line). | `IField`, `IMinMaxLen` |
| `BytesLine` | `str` | A single line of binary data, in other words a `Bytes` with new lines disallowed. | `IField`, `IMinMaxLen` |
| `ASCIILine` | `str` | A single line of ASCII text. | `IField`, `IMinMaxLen` |
| `Text` | `unicode` | Unicode text (multi-line). Often used with a WYSIWYG widget, although the default is a text area. | `IField`, `IMinMaxLen` |
| `TextLine` | `unicode` | A single line of Unicode text. | `IField`, `IMinMaxLen` |
| `Bool` | `bool` | `True` or `False`. | `IField` |
| `Int` | `int`, `long` | An integer number. Both `int`s and `long`s are allowed. | `IField`, `IMinMax` |
| `Float` | `float` | A floating point number. | `IField`, `IMinMax` |
| `Tuple` | `tuple` | A tuple (non-mutable). | `IField`, `ICollection`, `IMinMaxLen` |
| `List` | `list` | A list. | `IField`, `ICollection`, `IMinMaxLen` |
| `Set` | `set` | A set. | `IField`, `ICollection`, `IMinMaxLen` |
| `Frozenset` | `frozenset` | A `frozenset` (non-mutable). | `IField`, `ICollection`, `IMinMaxLen` |
| `Password` | `unicode` | Stores a simple string, but implies a password widget. | `IField`, `IMinMaxLen` |
| `Dict` | `dict` | Stores a dictionary. Both `key_type` and `value_type` must be set to fields. | `IField`, `IMinMaxLen`, `IDict` |
| `Datetime` | `datetime` | Stores a Python `datetime` (not a Zope 2 `DateTime`). | `IField`, `IMinMax` |
| `Date` | `date` | Stores a Python `date`. | `IField`, `IMinMax` |
| `Timedelta` | `timedelta` | Stores a Python `timedelta`. | `IField`, `IMinMax` |
| `SourceText` | `unicode` | A text field intended to store source text, such as HTML or Python code. | `IField`, `IMinMaxLen` |
| `Object` | n/a | Stores a Python object that conforms to the interface given as the `schema`. There is no standard widget for this. | `IField`, `IObject` |
| `URI` | `str` | A URI (URL) string. | `IField`, `MinMaxLen` |
| `Id` | `str` | A unique identifier, either a URI or a dotted name. | `IField`, `IMinMaxLen` |
| `DottedName` | `str` | A dotted name string. | `IField`, `IMinMaxLen` |
| `InterfaceField` | `Interface` | A Zope interface. | `IField` |
| `Decimal` | `Decimal` | Stores a Python `Decimal`. Requires version 3.4 or later of [`zope.schema`](https://pypi.org/project/zope.schema/). Not available by default in Zope 2.10. | `IField`, `IMinMax` |


### Fields in `plone.namedfile.field`

See [`plone.namedfile`](https://pypi.org/project/plone.namedfile/) and [plone.formwidget.namedfile](https://pypi.org/project/plone.formwidget.namedfile/) for more details.

| Name | Type | Description | Properties |
| - | - | - | - |
| `NamedFile` | `NamedFile` | A binary uploaded file. Normally used with the widget from `plone.formwidget.namedfile`. | `IField` |
| `NamedImage` | `NamedImage` | A binary uploaded image. Normally used with the widget from `plone.formwidget.namedfile`. | `IField` |
| `NamedBlobFile` | `NamedBlobFile` | A binary uploaded file stored as a ZODB blob. Requires the `blobs` extra to `plone.namedfile`. Otherwise identical to `NamedFile`. | `IField` |
| `NamedBlobImage` | `NamedBlobImage` | A binary uploaded image stored as a ZODB blob. Requires the `blobs` extra to `plone.namedfile`. Otherwise identical to `NamedImage`. | `IField` |

#### `NamedBlobImage`

The following example shows how to create an `Image` object, and attach the image file to it.

```python
img_obj = api.content.create(
    container=ww_article,
    type="Image",
    id="test.jpg",
    image=NamedBlobImage(
        data=img_file,
        filename="test.jpg",
    )
)
```





### Fields in `z3c.relationfield.schema`

See [`z3c.relationfield`](https://pypi.org/project/z3c.relationfield/) for more details.

| Name | Type | Description | Properties |
| - | - | - | - |
| `Relation` | `RelationValue` | Stores a single `RelationValue`. | `IField` |
| `RelationList` | `list` | A `List` field that defaults to `Relation` as the value type | See {ref}`List <fields-in-zope-schema-label>` |
| `RelationChoice` | `RelationValue` | A `Choice` field intended to store `RelationValue`s | See {ref}`Choice <fields-in-zope-schema-label>` |


(backend-fields-richtext-label)=

### Fields in `plone.app.textfield`

See [`plone.app.textfield`](https://pypi.org/project/plone.app.textfield/) for more details.

| Name | Type | Description | Properties |
| - | - | - | - |
| `RichText` | `RichTextValue` | Stores a `RichTextValue`, which encapsulates a raw text value, the source MIME type, and a cached copy of the raw text transformed to the default output MIME type. | `IField`, `IRichText` |


The `RichText` field allows for alternative markups and content filtering.
The following code sample shows how to create a schema with a `RichText` field.

```python
from plone.app.textfield import RichText
from plone.supermodel import model

class ITestSchema(model.Schema):

    body = RichText(title="Body text")
```

The `RichText` field constructor can take the following arguments, in addition to the usual arguments for a `Text` field.

`default_mime_type`
:   A string representing the default MIME type of the input markup.
    This defaults to `text/html`.

`output_mime_type`
:   A string representing the default output MIME type.
    This defaults to `text/x-html-safe`, which is a Plone-specific MIME type that disallows certain tags.
    Use the {guilabel}`HTML Filtering` control panel in Plone to control the tags.

`allowed_mime_types`
:   A tuple of strings giving a vocabulary of allowed input MIME types.
    If this is `None` (the default), the allowable types will be restricted to those set in Plone's {guilabel}`Markup` control panel.

The *default* field can be set to either a Unicode object (in which case it will be assumed to be a string of the default MIME type) or a {ref}`backend-fields-richtextvalue-label`.


#### reStructuredText transformation

Below is an example of a field that allows StructuredText and reStructuredText, transformed to HTML by default.

```python
from plone.app.textfield import RichText
from plone.supermodel import model

defaultBody = """\
Background
==========

Please fill this in

Details
-------

And this
"""

class ITestSchema(model.Schema):

    body = RichText(
        title="Body text",
        default_mime_type="text/x-rst",
        output_mime_type="text/x-html",
        allowed_mime_types=("text/x-rst", "text/structured",),
        default=defaultBody,
    )
```


(backend-fields-richtextvalue-label)=

#### `RichTextValue`

The `RichText` field usually does not store a string.
Instead, it stores a `RichTextValue` object.
This is an immutable object that has the following properties.

`raw`
:   A Unicode string with the original input markup.

`mimeType`
:   The MIME type of the original markup, for example, `text/html` or `text/structured`.

`encoding`
:   The default character encoding used when transforming the input markup.
    Most likely, this will be UTF-8.

`raw_encoded`
:   The raw input encoded in the given encoding.

`outputMimeType`
:   The MIME type of the default output, taken from the field at the time of instantiation.

`output`
:   A Unicode object representing the transformed output.
    If possible, this is cached persistently, until the `RichTextValue` is replaced with a new one (as happens when an edit form is saved, for example).

The storage of the `RichTextValue` object is optimized for the case where the transformed output will be read frequently (for example, on the view screen of the content object) and the raw value will be read infrequently (for example, on the edit screen).
Because the output value is cached indefinitely, you will need to replace the `RichTextValue` object with a new one if any of the transformation parameters change.
However, as we will see below, it is possible to apply a different transformation on demand, if you need to.

The code snippet below shows how a `RichTextValue` object can be constructed in code.
In this case, we have a raw input string of type `text/plain` that will be transformed to a default output of `text/html`.
Note that we would normally look up the default output type from the field instance.

```python
from plone.app.textfield.value import RichTextValue

context.body = RichTextValue("Some input text", mimeType="text/html", outputMimeType="text/x-html-safe")
```

The standard widget used for a `RichText` field will correctly store this type of object for you, so it is rarely necessary to create one yourself.


##### `RichText` fields in templates

If you use a `DisplayForm`, the display widget for the `RichText` field will render the transformed output markup automatically.
If you write TAL manually, you may try something like the following.

```xml
<div tal:content="structure context/body" />
```

This, however, will render a string as follows.

```html
RichTextValue object. (Did you mean <attribute>.raw or <attribute>.output?)
```

The correct syntax is:

```xml
<div tal:content="structure context/body/output" />
```

This will render the cached, transformed output.
This operation is approximately as efficient as rendering a simple `Text` field, since the transformation is only applied once, when the value is first saved.


##### Alternative transformations

Sometimes, you may want to invoke alternative transformations.
Under the hood, the default implementation uses the `portal_transforms` tool to calculate a transform chain from the raw value's input MIME type to the desired output MIME type.
If you need to write your own transforms, take a look at [Changing Portal Transforms Settings via Python](https://5.docs.plone.org/develop/plone/misc/portal_transforms.html).
This is abstracted behind an `ITransformer` adapter to allow alternative implementations.

To invoke a transformation in code, you can use the following syntax.

```python
from plone.app.textfield.interfaces import ITransformer

transformer = ITransformer(context)
transformedValue = transformer(context.body, "text/plain")
```

The `__call__()` method of the `ITransformer` adapter takes a `RichTextValue` object and an output MIME type as parameters.

If you write a page template, there is an even more convenient syntax.

```xml
<div tal:content="structure context/@@text-transform/body/text/plain" />
```

The first traversal name segment gives the name of the field on the context (`body` in this case).
The second and third segments give the output MIME type.
If the MIME type is omitted, the default output MIME type will be used.

```{note}
Unlike the `output` property, the value is not cached, and so will be calculated each time the page is rendered.
```



### Fields in `plone.schema`

See {ref}`backend-ploneschema-label` for more details.

| Name | Type | Description | Properties |
| - | - | - | - |
| `Email` | str | A field containing an email address  | `IField`, `IMinMaxLen` |
| `JSON` | | | |


(backend-fields-schema-label)=

## Schema

With `plone.autoform` and `plone.supermodel` we can use directives to add information to the schema fields.


(backend-fields-schema-autoform-permission)=

### Protect a field with a permission

By default, fields are included in the form regardless of the user's permissions.
Fields can be protected using the `read_permission` and `write_permission` directives.
The read permission is checked when the field is in display mode, and the write permission is checked when the field is in input mode.
The permission should be given with its Zope 3-style name, such as `cmf.ManagePortal` instead of `Manage portal`.

In this example, the `secret` field is protected by the `cmf.ManagePortal` permission as both a read and write permission.
This means that in both display and input modes, the field will only be included in the form for users who have that permission:

```python
from plone.supermodel import model
from plone.autoform import directives as form

class IMySchema(model.Schema):
    form.read_permission(secret="cmf.ManagePortal")
    form.write_permission(secret="cmf.ManagePortal")
    secret = schema.TextLine(
        title = "Secret",
        )
```

In supermodel XML, the directives are `security:read-permission` and
`security:write-permission`:

```xml
<field type="zope.schema.TextLine"
        name="secret"
        security:read-permission="cmf.ManagePortal"
        security:write-permission="cmf.ManagePortal">
    <title>Secret</title>
</field>
```
