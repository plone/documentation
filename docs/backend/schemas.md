---
myst:
  html_meta:
    "description": "A Zope schema provides a storage-neutral way to define Python object models with validators."
    "property=og:description": "A Zope schema provides a storage-neutral way to define Python object models with validators."
    "property=og:title": "Schemas"
    "keywords": "Fields, schema, autoform, supermodel, XML"
---

(backend-schemas-label)=

# Schemas

[Zope schemas](https://zopeschema.readthedocs.io/en/latest/) are a database-neutral and form-library-neutral way to describe Python data models.
Schemas extend the notion of interfaces to detailed descriptions of attributes (but not methods).
Every schema is an interface and specifies the public fields of an object.
A field roughly corresponds to an attribute of a Python object.
But a field provides space for at least a title and a description.
It can also constrain its value and provide a validation method.
You can optionally specify characteristics, such as its value being read-only or not required.

Plone uses Zope schemas to describe:

-   persistent data models
-   HTML form data
-   Plone configuration data
-   ZCML configuration data

Since Zope schemas aren't bound to any persistent storage, such as an SQL database engine, it gives you a reusable way to define data models.

Schemas are just regular Python classes, with some special attribute declarations.
They're always subclasses of `zope.interface.Interface`.
The schema itself can't be a concrete object instance.
You need to either have a `persistent.Persistent` object (for database data) or a `z3c.form.form.Form` object (for HTML forms).

Zope schemas are used for tasks such as:

-   defining allowed input data format (string, integer, object, list, and others) for Python class instance attributes
-   specifying required attributes on an object
-   defining custom validators on input data

The basic unit of data model declaration is the {doc}`field </backend/fields>`, which specifies what kind of data each Python attribute can hold.


(backend-ploneschema-label)=

## `plone.schema` versus `zope.schema`

The main package is [`zope.schema`](https://github.com/zopefoundation/zope.schema).
We can also use [`plone.schema`](https://github.com/plone/plone.schema), which provides additional fields and widgets for `z3c.form` and optional integration with Plone.

Additional features include:

-   Email field and widget
-   JSON field and widget
-   URI field and widget
-   `IPath` as `IChoice` derivative (and implementation)
-   integration with `plone.supermodel`, optional (extra `supermodel`)
-   integration with `plone.schemaeditor`, optional (extra `schemaeditor`)


## Example of a schema

```{tip}
In VS Code editor, you can install the [Plone Snippets](https://marketplace.visualstudio.com/items?itemName=Derico.plone-vs-snippets) extension.
This will give you snippets for most fields, widgets, and autoform directives in Python and XML based schemas.
```

Define a schema for a data model to store addresses:

```python
import zope.interface
from zope import schema

class ICheckoutAddress(zope.interface.Interface):
    """ Provide meaningful address information.
    """

    first_name = schema.TextLine(title=_("First name"), default="")
    last_name = schema.TextLine(title=_("Last name"), default="")
    organization = schema.TextLine(title=_("Organization"), default="")
    phone = schema.TextLine(title=_("Phone number"), default="")
    country = schema.Choice(
        title = _("Country"),
        vocabulary = "getpaid.countries",
        required=False,
        default=None,
    )
    state = schema.Choice(
        title = _("State"),
        vocabulary="getpaid.states",
        required=False,
        default=None,
    )
    city = schema.TextLine(title=_("City"), default="")
    postal_code = schema.TextLine(title=_("Postal code"), default="")
    street_address = schema.TextLine(title=_("Address"), default="")
```

This schema can be used in {doc}`/classic-ui/forms` and Dexterity {doc}`/backend/content-types/index` data models.

```{note}
In Dexterity {doc}`/backend/content-types/index`, the base class for a schema is `plone.supermodel.model.Schema`.
```


## Field constructor parameters

The `Field` base class defines a list of standard parameters that you can use to construct schema fields.
Each subclass of `Field` will have its own set of possible parameters in addition to this.
The following is a list of a few of the most common parameters.

`title`
:   field title as Unicode string

`description`
:   field description as Unicode string

`required`
:   boolean, whether the field is required

`default`
:   Default value if the attribute isn't present

```{seealso}
See [`IField` interface](https://zopeschema.readthedocs.io/en/latest/api.html#zope.schema.interfaces.IField) and [field implementation](https://zopeschema.readthedocs.io/en/latest/api.html#field-implementations) in the `zope.schema` documentation for details.
```

```{warning}
Do not initialize any non-primitive values using the `default` keyword parameter of schema fields.
Python and the ZODB stores objects by reference.
Python code will construct only _one_ field value during schema construction, and share its content across all objects.
This is probably not what you intend.
Instead, initialize objects in the `__init__()` method of your schema implementer.

In particular, dangerous defaults are `default=[]`, `default={}`, and `default=SomeObject()`.

Use `defaultFactory=get_default_name` instead.
```


## Schema introspection

The `zope.schema._schema` module provides some introspection functions:

-   `getFieldNames(schema_class)`
-   `getFields(schema_class)`
-   `getFieldNamesInOrder(schema)` retains the original field declaration order.
-   `getFieldsInOrder(schema)` retains the original field declaration order.

Example:

```python
import zope.schema
import zope.interface

class IMyInterface(zope.interface.Interface):

    text = zope.schema.TextLine()

# Get list of schema fields from IMyInterface
fields = zope.schema.getFields(IMyInterface)
```


### Dump schema data

Below is an example of how to extract all schema defined fields from an object.

```python
from collections import OrderedDict

import zope.schema


def dump_schemed_data(obj):
    """
    Prints out object variables as defined by its zope.schema Interface.
    """
    out = OrderedDict()

    # Check all interfaces provided by the object
    ifaces = obj.__provides__.__iro__

    # Check fields from all interfaces
    for iface in ifaces:
        fields = zope.schema.getFieldsInOrder(iface)
        for name, field in fields:
            # ('header', <zope.schema._bootstrapfields.TextLine object at 0x1149dd690>)
            out[name] = getattr(obj, name, None)

    return out
```


### Find the schema for a Dexterity type

When trying to introspect a Dexterity type, you can get a reference to the schema as follows:

```python
from zope.component import getUtility
from plone.dexterity.interfaces import IDexterityFTI

schema = getUtility(IDexterityFTI, name=PORTAL_TYPE_NAME).lookupSchema()
```

Then you can inspect it using the methods above.
Note this won't have behavior fields added to it at this stage, only the fields directly defined in your schema.

### More schema resources

- [`zope.schema`](https://pypi.org/project/zope.schema/) on PyPI
- [`zope.schema` source code](https://github.com/zopefoundation/zope.schema) is the definitive source for field types and usage.
- [`zope.schema` documentation](https://zopeschema.readthedocs.io/en/latest/)
- [`plone.schema`](https://github.com/plone/plone.schema)
- {doc}`reference list of fields used in Plone </backend/fields>`


(backend-schemas-directives-label)=

## Schema directives

With `plone.autoform` and `plone.supermodel`, we can use directives to add information to the schema fields.


### Omit fields

A field can be omitted entirely from all forms, or from some forms, using the `omitted` and `no_omit` directives.
In this example, the `dummy` field is omitted from all forms, and the `edit_only` field is omitted from all forms except those that provide the `IEditForm` interface:

```{code-block} python
:emphasize-lines: 7,12,13
:linenos:

from z3c.form.interfaces import IEditForm
from plone.supermodel import model
from plone.autoform import directives as form

class IMySchema(model.Schema):

    form.omitted("dummy")
    dummy = schema.Text(
        title="Dummy"
        )

    form.omitted("edit_only")
    form.no_omit(IEditForm, "edit_only")
    edit_only = schema.TextLine(
        title = "Only included on edit forms",
        )
```

In supermodel XML, this can be specified as:

```{code-block} xml
:emphasize-lines: 3,9

<field type="zope.schema.TextLine"
        name="dummy"
        form:omitted="true">
    <title>Dummy</title>
</field>

<field type="zope.schema.TextLine"
        name="edit-only"
        form:omitted="z3c.form.interfaces.IForm:true z3c.form.interfaces.IEditForm:false">
    <title>Only included on edit form</title>
</field>
```

`form:omitted` may be either a single boolean value, or a space-separated list of `<form_interface>:<boolean>` pairs.


### Reorder fields

A field's position in the form can be influenced using the `order_before` and `order_after` directives.
In this example, the `not_last` field is placed before the `summary` field, even though it is defined afterward:

```{code-block} python
:emphasize-lines: 12
:linenos:

from plone.supermodel import model
from plone.autoform import directives as form

class IMySchema(model.Schema):

    summary = schema.Text(
        title="Summary",
        description="Summary of the body",
        readonly=True
        )

    form.order_before(not_last="summary")
    not_last = schema.TextLine(
        title="Not last",
        )
```

The value passed to the directive may be either `*`, indicating before or after all fields, or the name of another field.
Use `.<fieldname>` to refer to the field in the current schema or a base schema.
Prefix with the schema name, such as `IDublinCore.title`, to refer to a field in another schema.
Use an unprefixed name to refer to a field in either the current or default schema for the form.

In supermodel XML, the directives are called `form:before` and `form:after`.
For example:

```{code-block} xml
:emphasize-lines: 3

<field type="zope.schema.TextLine"
        name="not_last"
        form:before="*">
    <title>Not last</title>
</field>
```


### Organizing fields into fieldsets

Fields can be grouped into fieldsets, which will be rendered within an HTML `<fieldset>` tag.
In this example the `footer` and `dummy` fields are placed within the `extra` fieldset:

```{code-block} python
:emphasize-lines: 6-9
:linenos:

from plone.supermodel import model
from plone.autoform import directives as form

class IMySchema(model.Schema):

    model.fieldset("extra",
        label="Extra info",
        fields=["footer", "dummy"]
        )

    footer = schema.Text(
        title="Footer text",
        )

    dummy = schema.Text(
        title="Dummy"
        )
```

In supermodel XML, fieldsets are specified by grouping fields within a `<fieldset>` tag:

```xml
<fieldset name="extra" label="Extra info">
    <field name="footer" type="zope.schema.TextLine">
        <title>Footer text</title>
    </field>
    <field name="dummy" type="zope.schema.TextLine">
        <title>Dummy</title>
    </field>
</fieldset>
```


## Advanced

```{note}
Most examples in this section are low level Zope stuff.
In Plone, you rarely have to deal with it.
But we keep it here for those who are interested in how things work internally.
```

We can use a schema class to store data based on our model definition in the ZODB database.

We use `zope.schema.fieldproperty.FieldProperty` to bind persistent class attributes to the data definition.

Example:

```python
from persistent import Persistent # Automagical ZODB persistent object
from zope.schema.fieldproperty import FieldProperty

class CheckoutAddress(Persistent):
    """ Store checkout address """

    # Declare that all instances of this class will
    # conform to the ICheckoutAddress data model:
    zope.interface.implements(ICheckoutAddress)

    # Provide the fields:
    first_name = FieldProperty(ICheckoutAddress["first_name"])
    last_name = FieldProperty(ICheckoutAddress["last_name"])
    organization = FieldProperty(ICheckoutAddress["organization"])
    phone = FieldProperty(ICheckoutAddress["phone"])
    country =  FieldProperty(ICheckoutAddress["country"])
    state = FieldProperty(ICheckoutAddress["state"])
    city = FieldProperty(ICheckoutAddress["phone"])
    postal_code = FieldProperty(ICheckoutAddress["postal_code"])
    street_address = FieldProperty(ICheckoutAddress["street_address"])
```

For persistent objects, see the [persistent object documentation](https://5.docs.plone.org/develop/plone/persistency/persistent).


### Use schemas as data models

Based on the example data model above, we can use it in content type {doc}`browser views </classic-ui/views>` to store arbitrary data as content type attributes.

Example:

```python
class MyView(BrowserView):
    """ Connect this view to your content type using a ZCML declaration.
    """

    def __call__(self):
        # Get the content item which this view was invoked on:
        context = self.context.aq_inner

        # Store a new address in it as the ``test_address`` attribute
        context.test_address = CheckoutAddress()
        context.test_address.first_name = "Mikko"
        context.test_address.last_name = "Ohtamaa"

        # Note that you can still add arbitrary attributes to any
        # persistent object.  They are simply not validated, as they
        # don't go through the ``zope.schema`` FieldProperty
        # declarations.
        # Do not do this, you will regret it later.
        context.test_address.arbitary_attribute = "Don't do this!"
```


### Field order

The `order` attribute can be used to determine the order in which fields in a schema were defined.
If one field was created after another (in the same thread), the value of `order` will be greater.


### Default values

To make default values of schema effective, class attributes must be implemented using `FieldProperty`.

Example:

```python
import zope.interface
from zope import schema
from zope.schema.fieldproperty import FieldProperty


class ISomething(zope.interface.Interface):
    """ Sample schema """
    some_value = schema.Bool(default=True)


class SomeStorage(object):

    some_value = FieldProperty(ISomething["some_value"])


something = SomeStorage()
assert something.some_value == True
```


### Validation and type constraints

Schema objects using field properties provide automatic validation facilities for the prevention of setting badly formatted attributes.

There are two aspects to validation:

-   Checking the type constraints (done automatically).
-   Checking whether the value fills certain constraints (validation).

Example of how type constraints work:

```python
class ICheckoutData(zope.interface.Interface):
    """ This interface defines all the checkout data we have.

    It will also contain the ``billing_address``.
    """

    email = schema.TextLine(title=_("Email"), default="")


class CheckoutData(Persistent):

    zope.interface.implements(ICheckoutData)

    email = FieldProperty(ICheckoutData["email"])


def test_store_bad_email(self):
    """ Check that we can't put data to checkout """

    data = getpaid.expercash.data.CheckoutData()

    from zope.schema.interfaces import WrongContainedType, WrongType, NotUnique

    try:
        data.email = 123 # Can't set email field to an integer.
        raise AssertionError("Should never be reached.")
    except WrongType:
        pass
```

Example of validation (email field):

```python
from zope import schema


class InvalidEmailError(schema.ValidationError):
    __doc__ = "Please enter a valid e-mail address."


def isEmail(value):
    if re.match("^"+EMAIL_RE, value):
        return True
    raise InvalidEmailError


class IContact(Interface):
    email = schema.TextLine(title="Email", constraint=isEmail)
```


### Persistent objects and schema

ZODB persistent objects don't provide facilities for setting field defaults or validating the data input.

When you create a persistent class, you need to provide field properties for it, which will sanitize the incoming and outgoing data.

When the persistent object is created, it has no attributes.
When you try to access the attribute through a named `zope.schema.fieldproperty.FieldProperty` accessor, it first checks whether the attribute exists.
If the attribute isn't there, it's created and the default value is returned.

Example:

```python
from persistent import Persistent
from zope import schema
from zope.interface import implements, alsoProvides
from zope.component import adapts
from zope.schema.fieldproperty import FieldProperty

# ... other implementation code ...

class IHeaderBehavior(form.Schema):
    """ Sample schema """
    inheritable = schema.Bool(
            title="Inherit header",
            description="This header is visible on child content",
            required=False,
            default=False)

    block_parents = schema.Bool(
            title="Block parent headers",
            description="Do not show parent headers for this content",
            required=False,
            default=False)

    # Contains list of HeaderAnimation objects
    alternatives = schema.List(
            title="Available headers and animations",
            description="Headers and animations uploaded here",
            required=False,
            value_type=schema.Object(IHeaderAnimation))

alsoProvides(IHeaderAnimation, form.IFormFieldProvider)


class HeaderBehavior(Persistent):
    """ Sample persistent object for the schema """

    implements(IHeaderBehavior)
    #
    # zope.schema magic happens here - see FieldProperty!
    #
    # We need to declare field properties so that objects will
    # have input data validation and default values taken from schema
    # above
    inheritable = FieldProperty(IHeaderBehavior["inheritable"])
    block_parents = FieldProperty(IHeaderBehavior["block_parents"])
    alternatives = FieldProperty(IHeaderBehavior["alternatives"])
```

Now you see the magic:

```python
header = HeaderBehavior()
# This  triggers the ``alternatives`` accessor, which returns the default
# value, which is an empty list
assert header.alternatives = []
```


### Collections (and multiple choice fields)

Collections are fields composed of several other fields.
Collections also act as multiple choice fields.

For more information see:

-   [Using Zope schemas with a complex vocabulary and multi-select fields](https://web.archive.org/web/20161227025947/http://www.upfrontsystems.co.za/Members/izak/sysadman/using-zope-schemas-with-a-complex-vocabulary-and-multi-select-fields)
-   Collections section in [`zope.schema` documentation](https://zopeschema.readthedocs.io/en/latest/fields.html#collections)
-   Schema [field sources documentation](https://zopeschema.readthedocs.io/en/latest/sources.html#sources-in-fields)
-   [Choice field](https://zopeschema.readthedocs.io/en/latest/fields.html#choice)


#### Single choice example

Only one value can be chosen.

Below is code to create a Python logging level choice:

```python
import logging

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

def _createLoggingVocabulary():
    """ Create zope.schema vocabulary from Python logging levels.

    Note that term.value is int, not string.

    _levelNames looks like::

        {0: "NOTSET", "INFO": 20, "WARNING": 30, 40: "ERROR", 10: "DEBUG", "WARN": 30, 50:
        "CRITICAL", "CRITICAL": 50, 20: "INFO", "ERROR": 40, "DEBUG": 10, "NOTSET": 0, 30: "WARNING"}

    @return: Iterable of SimpleTerm objects
    """
    for level, name in logging._levelNames.items():

        # logging._levelNames dictionary is bidirectional, let's
        # get numeric keys only

        if type(level) == int:
            term = SimpleTerm(value=level, token=str(level), title=name)
            yield term

# Construct SimpleVocabulary objects of log level -> name mappings
logging_vocabulary = SimpleVocabulary(list(_createLoggingVocabulary()))

class ISyncRunOptions(Interface):

    log_level = schema.Choice(vocabulary=logging_vocabulary,
                              title="Log level",
                              description="One of python logging module constants",
                              default=logging.INFO)
```


#### Multiple choice example

Using `zope.schema.List`, many values can be chosen once.
Each value is atomically constrained by the `value_type` schema field.

Example:

```python
from zope import schema
from plone.supermodel import model
from plone.autoform import directives as form

from z3c.form.browser.checkbox import CheckBoxFieldWidget

class IMultiChoice(model.Schema):
    # ...

    # Contains lists of values from Choice list using special "get_field_list" vocabulary
    # We also give a ``plone.autoform.directives`` hint to render this as
    # multiple checbox choices
    form.widget(yourField=CheckBoxFieldWidget)
    yourField = schema.List(title="Available headers and animations",
                               description="Headers and animations uploaded here",
                               required=False,
                               value_type=zope.schema.Choice(source=yourVocabularyFunction),
                               )
```


### Dynamic schemas

Schemas are singletons, as there exists only one class instance per Python run time.
For example, if you need to feed schemas generated dynamically to a form engine, then consider the following.

-   If the form engine, such as `z3c.form`, refers to schema fields, then replace these references with dynamically generated copies.
-   Generate a Python class dynamically.
    Output Python source code, then `eval()` it.
    Using `eval()` is almost always considered a bad practice.

```{warning}
Though it is possible, you should not modify `zope.schema` classes in-place, as the same copy is shared between different threads.
If there are two concurrent HTTP requests, problems may occur.
```


#### Replace schema fields with dynamically modified copies

Below is an example for `z3c.form`.
It uses the Python `copy` module to copy the `f.field` reference, which points to the `zope.schema` field.
For this field copy, we modify the `required` attribute, based on input.

Example:

```python
@property
def fields(self):
    """ Get the field definition for this form.

    Form class's fields attribute does not have to
    be fixed. It can also be a property.
    """

    # Construct the Fields instance as we would
    # normally do in more static way
    fields = z3c.form.field.Fields(ICheckoutAddress)

    # We need to override the actual required from the
    # schema field which is a little tricky.
    # Schema fields are shared between instances
    # by default, so we need to create a copy of it
    if self.optional:
        for f in fields.values():
            # Create copy of a schema field
            # and force it unrequired
            schema_field = copy.copy(f.field) # shallow copy of an instance
            schema_field.required = False
            f.field = schema_field
```


