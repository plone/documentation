---
myst:
  html_meta:
    "description": "How to store markup (such as HTML or reStructuredText) and render it with a transformation"
    "property=og:description": "How to store markup (such as HTML or reStructuredText) and render it with a transformation"
    "property=og:title": "How to store markup (such as HTML or reStructuredText) and render it with a transformation"
    "keywords": "Plone, content types, rich text, markup, and transformations"
---

# Rich text, markup, and transformations

This chapter describes how to store markup (such as HTML or reStructuredText) and render it with a transformation.

Many content items need to allow users to provide rich text in some kind of markup, be that HTML (perhaps entered using a "What You See Is What You Get" or WYSIWYG editor), reStructuredText, Markdown, or some other format.
This markup typically needs to be transformed into HTML for the view template, but we also want to keep track of the original raw markup so that it can be edited again.
Even when the input format is HTML, there is often a need for a transformation to tidy up the HTML and strip out tags that are not permitted.

It is possible to store HTML in a standard `Text` field.
You can even get a WYSIWYG widget, by using a schema such as the following.

```python
from plone.autoform import directives as form
from plone.supermodel import model
from zope import schema
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

class ITestSchema(model.Schema):

    form.widget('body', WysiwygFieldWidget)
    body = schema.Text(title="Body text")
```

(richtext-label)=

However, this approach does not allow for alternative markups or any form of content filtering.
For that we need to use a more powerful field, `RichText`, from the [`plone.app.textfield`](https://pypi.org/project/plone.app.textfield/) package.

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

The *default* field can be set to either a Unicode object (in which case it will be assumed to be a string of the default MIME type) or a `RichTextValue` object (see below).

Below is an example of a field that allows StructuredText and reStructuredText, transformed to HTML by default.

```python
from plone.app.textfield import RichText
from plone.supermodel import model

defaultBody = """\
Background
==========

Please fill this in

Details
=======

And this
"""

class ITestSchema(model.Schema):

    body = RichText(
        title="Body text",
        default_mime_type='text/x-rst',
        output_mime_type='text/x-html',
        allowed_mime_types=('text/x-rst', 'text/structured',),
        default=defaultBody,
    )
```


## The RichTextValue

The `RichText` field does not store a string.
Instead, it stores a `RichTextValue` object.
This is an immutable object that has the following properties.

`raw`
:   A Unicode string with the original input markup.

`mimeType`
:   The MIME type of the original markup, for example `text/html` or `text/structured`.

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

The code snippet belows shows how a `RichTextValue` object can be constructed in code.
In this case, we have a raw input string of type `text/plain` that will be transformed to a default output of `text/html`.
Note that we would normally look up the default output type from the field instance.

```python
from plone.app.textfield.value import RichTextValue

context.body = RichTextValue("Some input text", 'text/plain', 'text/html')
```

Of course, the standard widget used for a `RichText` field will correctly store this type of object for you, so it is rarely necessary to create one yourself.


## Using rich text fields in templates

What about using the text field in a template?
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


## Alternative transformations

Sometimes, you may want to invoke alternative transformations.
Under the hood, the default implementation uses the `portal_transforms` tool to calculate a transform chain from the raw value's input MIME type to the desired output MIME type.
If you need to write your own transforms, take a look at [this tutorial](https://5.docs.plone.org/develop/plone/misc/portal_transforms.html).
This is abstracted behind an `ITransformer` adapter to allow alternative implementations.

To invoke a transformation in code, you can use the following syntax.

```python
from plone.app.textfield.interfaces import ITransformer

transformer = ITransformer(context)
transformedValue = transformer(context.body, 'text/plain')
```

The `__call__()` method of the `ITransformer` adapter takes a `RichTextValue` object and an output MIME type as parameters.

If you write a page template, there is an even more convenient syntax.

```xml
<div tal:content="structure context/@@text-transform/body/text/plain" />
```

The first traversal name gives the name of the field on the context (`body` in this case).
The second and third give the output MIME type.
If the MIME type is omitted, the default output MIME type will be used.

```{note}
Unlike the `output` property, the value is not cached, and so will be calculated each time the page is rendered.
```
