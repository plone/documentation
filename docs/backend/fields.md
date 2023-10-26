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

The following tables show the most common field types for use in {ref}`classic-ui-forms-label` and Dexterity {ref}`backend-content-types-label`.
See {ref}`schemas <backend-schemas-label>` for information about how fields compose a schema for a form or content type data model.

```{note}
In VS Code editor, you can install the [Plone Snippets](https://marketplace.visualstudio.com/items?itemName=Derico.plone-vs-snippets) extension. This will give you snippets for most fields, widgets and autoform directives in Python and XML based schemas.
```

## Field properties

Fields are initialized with properties passed in their constructors.
To avoid having to repeat the available properties for each field, we'll list them once here, grouped into the interfaces that describe them.
You'll see those interfaces again in the tables below that describe the various field types.
Refer to the table below to see what properties a particular interface implies.

| Interface | Property | Type | Description |
| - | - | - | - |
| IField | title | int | The title of the field. Used in the widget. |
| | `description` | unicode | A description for the field. Used in the widget. |
| | `required` | bool | Whether or not the field is required. Used for form validation. The default is `True`. |
| | `readonly` | bool | Whether or not the field is read only. Default is `False`. |
| | `default` | | The default value for the field. Used in forms and sometimes as a fallback value. Must be a valid value for the field if set. The default is `None`.|
| | `defaultFactory` | | The default factory method for the field. Used in forms and sometimes as a fallback value. This is a name of a method which returns a dynamic default value.|
| | `missing_value` | | A value that represents "this field is not set". Used by form validation. Defaults to `None`. For lists and tuples, it is sometimes useful to set this to an empty list or tuple. |
| `IMinMaxLen` | `min_length` | int | The minimum required length or minimum number of elements. Used for `string`, sequence, mapping, or `set` fields. Default is `0`. |
| | `max_length `| int | The maximum allowed length or maximum number of elements. Used for `string`, sequence, mapping, or `set` fields. Default is `None` (no check). |
| `IMinMax` | `min` | | The minimum allowed value. Must be a valid value for the field, for example, an int field should be an integer. Default is `None` (no check). |
| | `max` | | The maximum allowed value. Must be a valid value for the field, for example an int field should be an integer. Default is `None` (no check). |
| `ICollection` | `value_type` | | Another `Field` instance that describes the allowable values in a list, tuple, or other collection. Must be set for any collection field. One common usage is to set this to a `Choice` to model a multi-selection field with a {ref}`vocabulary <backend-vocabularies-label>`. |
| | `unique` | bool | Whether or not values in the collection must be unique. Usually not set directly. Use a `Set` or `Frozenset` to guarantee uniqueness in an efficient way. |
| `IDict` | `key_type` | | Another `Field` instance that describes the allowable keys in a dictionary. Similar to the `value_type` of a collection. Must be set. |
| | `value_type` | | Another `Field` instance that describes the allowable values in a dictionary. Similar to the `value_type` of a collection. Must be set. |
| `IObject` | `schema` | `Interface` | An interface that must be provided by any object stored in this field. |
| `IRichText` | `default_mime_type` | str | Default MIME type for the input text of a rich text field. Defaults to `text/html`. |
| | `output_mime_type` | str | Default output MIME type for the transformed value of a rich text field. Defaults to `text/x-html-safe`. There must be a transformation chain in the `portal_transforms` tool that can transform from the input value to the `output` value for the output property of the `RichValue` object to contain a value. |
| | `allowed_mime_types` | tuple | A list of allowed input MIME types. The default is `None`, in which case the site-wide settings from the {guilabel}`Markup` control panel will be used. |

See [IField interface](https://zopeschema.readthedocs.io/en/latest/api.html#zope.schema.interfaces.IField) and [field implementation](https://zopeschema.readthedocs.io/en/latest/api.html#field-implementations) in `zope.schema` documentation for details.

## Field types

The following tables describe the most commonly used field types, grouped by the module from which they can be imported.


### Fields in `zope.schema`

| Name | Type | Description | Properties |
| - | - | - | - |
| Choice | N/A | Used to model selection from a vocabulary, which must be supplied. Often used as the `value_type` of a selection field. The value type is the value of the terms in the vocabulary. | See {ref}`backend-vocabularies-label`. |
| Bytes | str | Used for binary data. | IField, IMinMaxLen |
| ASCII | str | ASCII text (multi-line). | IField, IMinMaxLen |
| BytesLine | str | A single line of binary data, in other words a `Bytes` with new lines disallowed. | IField, IMinMaxLen |
| ASCIILine | str | A single line of ASCII text. | IField, IMinMaxLen |
| Text | unicode | Unicode text (multi-line). Often used with a WYSIWYG widget, although the default is a text area. | IField, IMinMaxLen |
| TextLine | unicode | A single line of Unicode text. | IField, IMinMaxLen |
| Bool | bool | `True` or `False`. | IField |
| Int | int, long | An integer number. Both ints and longs are allowed. | IField, IMinMax |
| Float | float | A floating point number. | IField, IMinMax |
| Tuple | tuple | A tuple (non-mutable). | IField, ICollection, IMinMaxLen |
| List | list | A list. | IField, ICollection, IMinMaxLen |
| Set | set | A set. | IField, ICollection, IMinMaxLen |
| Frozenset | frozenset | A frozenset (non-mutable). | IField, ICollection, IMinMaxLen |
| Password | unicode | Stores a simple string, but implies a password widget. | IField, IMinMaxLen |
| Dict | dict | Stores a dictionary. Both `key_type` and `value_type` must be set to fields. | IField, IMinMaxLen, IDict |
| Datetime | datetime | Stores a Python `datetime` (not a Zope 2 `DateTime`). | IField, IMinMax |
| Date | date | Stores a python `date`. | IField, IMinMax |
| Timedelta | timedelta | Stores a python `timedelta`. | IField, IMinMax |
| SourceText | unicode | A textfield intended to store source text, such as HTML or Python code. | IField, IMinMaxLen |
| Object | N/A | Stores a Python object that conforms to the interface given as the `schema`. There is no standard widget for this. | IField, IObject |
| URI | str | A URI (URL) string. | IField, MinMaxLen |
| Id | str | A unique identifier, either a URI or a dotted name. | IField, IMinMaxLen |
| DottedName | str | A dotted name string. | IField, IMinMaxLen |
| InterfaceField | Interface | A Zope interface. | IField |
| Decimal | Decimal | Stores a Python `Decimal`. Requires version 3.4 or later of [`zope.schema`](https://pypi.org/project/zope.schema/). Not available by default in Zope 2.10. | IField, IMinMax |


### Fields in `plone.namedfile.field`

See [`plone.namedfile`](https://pypi.org/project/plone.namedfile/) and [plone.formwidget.namedfile](https://pypi.org/project/plone.formwidget.namedfile/) for more details.

| Name | Type | Description | Properties |
| - | - | - | - |
| NamedFile | NamedFile | A binary uploaded file. Normally used with the widget from `plone.formwidget.namedfile`. | IField |
| NamedImage | NamedImage | A binary uploaded image. Normally used with the widget from `plone.formwidget.namedfile`. | IField |
| NamedBlobFile | NamedBlobFile | A binary uploaded file stored as a ZODB blob. Requires the `blobs` extra to `plone.namedfile`. Otherwise identical to `NamedFile`. | IField |
| NamedBlobImage | NamedBlobImage | A binary uploaded image stored as a ZODB blob. Requires the `blobs` extra to `plone.namedfile`. Otherwise identical to `NamedImage`. | IField |


### Fields in `z3c.relationfield.schema`

See [`z3c.relationfield`](https://pypi.org/project/z3c.relationfield/) for more details.

| Name | Type | Description | Properties |
| -------------- | ------------- | ------------------------------------------------------------ | ------------ |
| Relation | RelationValue | Stores a single `RelationValue`. | IField |
| RelationList | list | A `List` field that defaults to `Relation` as the value type | See `List` |
| RelationChoice | RelationValue | A `Choice` field intended to store `RelationValue`'s | See `Choice` |


### Fields in `plone.app.textfield`

See [`plone.app.textfield`](https://pypi.org/project/plone.app.textfield/) for more details.

| Name | Type | Description | Properties |
| -------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| RichText | RichTextValue | Stores a `RichTextValue`, which encapsulates a raw text value, the source MIME type, and a cached copy of the raw text transformed to the default output MIME type. | IField, IRichText |


### Fields in `plone.schema`

See {ref}`backend-ploneschema-label` for more details.

| Name | Type | Description | Properties |
| ----- | ---- | ----------------------------------- | ------------------ |
| Email | str | A field containing an email address  | IField, IMinMaxLen |
| JSON  |     |                                      |                    |


(backend-fields-schema-label)=

## schema


(backend-fields-schema-autoform-label)=

### autoform (directives) schema ordering, filtering, and permissions


(backend-fields-supermodel-label)=

## supermodel (xml)


(backend-fields-supermodel-autoform-label)=

### autoform (directives) supermodel ordering, filtering, and permissions
