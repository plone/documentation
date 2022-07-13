==================================
Modelling using zope.schema
==================================

.. admonition:: Description

    zope.schema package provide a storage-neutral way to define Python object
    models with validators.


Introduction
============

Zope 3 schemas are a database-neutral and form-library-neutral way to
describe Python data models.

Plone uses Zope 3 schemas for these purposes:

* to describe persistent data models;
* to describe HTML form data;
* to describe ZCML configuration data.

Since Zope 3 schemas are not bound to e.g. a SQL database engine, it gives
you very reusable way to define data models.

Schemas are just regular Python classes, with some special attribute
declarations.  They are always subclasses of ``zope.interface.Interface``.
The schema itself cannot be a concrete object instance |---| you need to
either have a ``persistent.Persistent`` object (for database data) or a
``z3c.form.form.Form`` object (for HTML forms).

Zope 3 schemas are used for tasks like:

* defining allowed input data format (string, integer, object, list, etc.)
  for Python class instance attributes;
* specifying required attributes on an object;
* defining custom validators on input data.

The basic unit of data model declaration is the *field*, which specifies what
kind of data each Python attribute can hold.

More info
----------------

* `zope.schema <https://pypi.python.org/pypi/zope.schema>`_ on PyPi

* `zope.schema source code <http://github.com/zopefoundation/zope.schema>`_ - definite source for field types and usage.

``zope.schema`` provides a very comprehensive set of fields out of the box.
Finding good documentation for them, however, can be challenging.  Here are
some starting points:


* :doc:`Dexterity field list </external/plone.app.dexterity/docs/reference/fields>`.


Example of a schema
--------------------

Let's define a data model to store addresses::

    import zope.interface
    from zope import schema

    class ICheckoutAddress(zope.interface.Interface):
        """ Provide meaningful address information.

        This is not 1:1 with getpaid.core interfaces, but
        more like a better guess.
        """

        first_name = schema.TextLine(title=_(u"First name"), default=u"")
        last_name = schema.TextLine(title=_(u"Last name"), default=u"")
        organization = schema.TextLine(title=_(u"Organization"), default=u"")
        phone = schema.TextLine(title=_(u"Phone number"), default=u"")
        country = schema.Choice( title = _(u"Country"),
        vocabulary = "getpaid.countries", required=False, default=None)
        state = schema.Choice( title = _(u"State"),
        vocabulary="getpaid.states", required=False, default=None)
        city = schema.TextLine(title=_(u"City"), default=u"")
        postal_code = schema.TextLine(title=_(u"Postal code"), default=u"")
        street_address = schema.TextLine(title=_(u"Address"), default=u"")

Next, we define a concrete persistent class which uses this data model.  We
can use this class to store data based on our model definition in the ZODB
database.

We use ``zope.schema.fieldproperty.FieldProperty`` to bind
persistent class attributes to the data definition.

Example::

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

For persistent objects, see :doc:`persistent object documentation
</develop/plone/persistency/persistent>`.


Using schemas as data models
============================


Based on the example data model above, we can use it in e.g. content type
:doc:`browser views </develop/plone/views/browserviews>` to store arbitrary data as content
type attributes.

Example::

    class MyView(BrowserView):
        """ Connect this view to your content type using a ZCML declaration.
        """

        def __call__(self):
            # Get the content item which this view was invoked on:
            context = self.context.aq_inner

            # Store a new address in it as the ``test_address`` attribute
            context.test_address = CheckoutAddress()
            context.test_address.first_name = u"Mikko"
            context.test_address.last_name = u"Ohtamaa"

            # Note that you can still add arbitrary attributes to any
            # persistent object.  They are simply not validated, as they
            # don't go through the ``zope.schema`` FieldProperty
            # declarations.
            # Do not do this, you will regret it later.
            context.test_address.arbitary_attribute = u"Don't do this!"


Field constructor parameters
============================

The ``Field`` base class defines a list of standard parameters that you can
use to construct schema fields.  Each subclass of ``Field`` will have its own
set of possible parameters in addition to this.

See the full list `here
<http://docs.zope.org/zope3/Code/zope/schema/_bootstrapfields/Field/index.html>`_.

Title
    field title as unicode string

Description
    field description as unicode string

required
    boolean, whether the field is required

default
    Default value if the attribute is not present

... and so on.

.. warning::

    Do not initialize any non-primitive values using the *default* keyword
    parameter of schema fields.  Python and the ZODB stores objects by
    reference.  Python code will construct only *one* field value during
    schema construction, and share its content across all objects.  This
    is probably not what you intend. Instead, initialize objects in the
    ``__init__()`` method of your schema implementer.

    In particular, dangerous defaults are: ``default=[]``, ``default={}``,
    ``default=SomeObject()``.


Schema introspection
====================

The ``zope.schema._schema`` module provides some introspection functions:

* ``getFieldNames(schema_class)``
* ``getFields(schema_class)``
* ``getFieldNamesInOrder(schema)`` |---| retain the orignal field
  declaration order.
* ``getFieldsInOrder(schema)`` |---| retain the orignal field declaration
  order.

Example::

    import zope.schema
    import zope.interface

    class IMyInterface(zope.interface.Interface):

        text = zope.schema.TextLine()

    # Get list of schema fields from IMyInterface
    fields = zope.schema.getFields(IMyInterface)

Dumping schema data
---------------------

Below is an example how to extract all schema defined fields from an object.

::

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

Finding the schema for a Dexterity type
---------------------------------------

When trying to introspect a Dexterity type, you can get a reference to the schema thus::

    from zope.component import getUtility
    from plone.dexterity.interfaces import IDexterityFTI

    schema = getUtility(IDexterityFTI, name=PORTAL_TYPE_NAME).lookupSchema()

...and then inspect it using the methods above. Note this won't have behavior
fields added to it at this stage, only the fields directly defined in your
schema.

Field order
===========

The ``order`` attribute can be used to determine the order in which fields in
a schema were defined. If one field was created after another (in the same
thread), the value of ``order`` will be greater.


Default values
==============

To make default values of schema effective, class attributes must be
implemented using ``FieldProperty``.

Example::

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


Validation and type constrains
===============================

Schema objects using field properties provide automatic validation
facilities, preventing setting badly formatted attributes.

There are two aspects to validation:

* Checking the type constraints (done automatically).
* Checking whether the value fills certain constrains (validation).

Example of how type constraints work::

    class ICheckoutData(zope.interface.Interface):
        """ This interface defines all the checkout data we have.

        It will also contain the ``billing_address``.
        """

        email = schema.TextLine(title=_(u"Email"), default=u"")


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

Example of validation (email field)::

        from zope import schema


        class InvalidEmailError(schema.ValidationError):
            __doc__ = u'Please enter a valid e-mail address.'


        def isEmail(value):
            if re.match('^'+EMAIL_RE, value):
                return True
            raise InvalidEmailError


        class IContact(Interface):
            email = schema.TextLine(title=u'Email', constraint=isEmail)


Persistent objects and schema
=============================

ZODB persistent objects do not provide facilities for setting field defaults
or validating the data input.

When you create a persistent class, you need to provide field properties for
it, which will sanify the incoming and outgoing data.

When the persistent object is created it has no attributes. When you try to
access the attribute through a named
``zope.schema.fieldproperty.FieldProperty``
accessor, it first checks whether the attribute exists. If the attribute is
not there, it is created and the default value is returned.

Example::

    from persistent import Persistent
    from zope import schema
    from zope.interface import implements, alsoProvides
    from zope.component import adapts
    from zope.schema.fieldproperty import FieldProperty

    # ... other implementation code ...

    class IHeaderBehavior(form.Schema):
        """ Sample schema """
        inheritable = schema.Bool(
                title=u"Inherit header",
                description=u"This header is visible on child content",
                required=False,
                default=False)

        block_parents = schema.Bool(
                title=u"Block parent headers",
                description=u"Do not show parent headers for this content",
                required=False,
                default=False)

        # Contains list of HeaderAnimation objects
        alternatives = schema.List(
                title=u"Available headers and animations",
                description=u"Headers and animations uploaded here",
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

Now you see the magic::

    header = HeaderBehavior()
    # This  triggers the ``alternatives`` accessor, which returns the default
    # value, which is an empty list
    assert header.alternatives = []


Collections (and multichoice fields)
====================================

Collections are fields composed of several other fields.
Collections also act as multi-choice fields.

For more information see:

* `Using Zope schemas with a complex vocabulary and multi-select fields <http://www.upfrontsystems.co.za/Members/izak/sysadman/using-zope-schemas-with-a-complex-vocabulary-and-multi-select-fields>`_

* Collections section in `zope.schema documentation <http://docs.zope.org/zope3/Code/zope/schema/fields.txt/index.html>`_

* Schema `field sources documentation <http://docs.zope.org/zope3/Code/zope/schema/sources.txt/index.html>`_

* `Choice field <http://docs.zope.org/zope3/Code/zope/schema/_field/Choice/index.html>`_

* `List field <http://docs.zope.org/zope3/Code/zope/schema/_field/List/index.html>`_.


Single-choice example
---------------------

Only one value can be chosen.

Below is code to create Python logging level choice::

    import logging

    from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

    def _createLoggingVocabulary():
        """ Create zope.schema vocabulary from Python logging levels.

        Note that term.value is int, not string.

        _levelNames looks like::

            {0: 'NOTSET', 'INFO': 20, 'WARNING': 30, 40: 'ERROR', 10: 'DEBUG', 'WARN': 30, 50:
            'CRITICAL', 'CRITICAL': 50, 20: 'INFO', 'ERROR': 40, 'DEBUG': 10, 'NOTSET': 0, 30: 'WARNING'}

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
                                  title=u"Log level",
                                  description=u"One of python logging module constants",
                                  default=logging.INFO)

Multi-choice example
--------------------

Using zope.schema.List, many values can be chosen once.
Each value is atomically constrained by *value_type* schema field.

Example::

    from zope import schema
    from plone.supermodel import model
    from plone.autoform import directives as form

    from z3c.form.browser.checkbox import CheckBoxFieldWidget

    class IMultiChoice(model.Schema):
        ...

        # Contains lists of values from Choice list using special "get_field_list" vocabulary
        # We also give a plone.autoform.directives hint to render this as
        # multiple checbox choices
        form.widget(yourField=CheckBoxFieldWidget)
        yourField = schema.List(title=u"Available headers and animations",
                                   description=u"Headers and animations uploaded here",
                                   required=False,
                                   value_type=zope.schema.Choice(source=yourVocabularyFunction),
                                   )

Dynamic schemas
===============

Schemas are singletons, as there only exist one class instance
per Python run-time. For example, if you need to feed schemas generated dynamically
to form engine, you need to

* If the form engine (e.g. z3c.form refers to schema fields, then
  replace these references with dynamically generated copes)

* Generate a Python class dynamically. Output Python source code,
  then ``eval()`` it. Using ``eval()`` is almost always considered
  as a bad practice.

.. warning ::

    Though it is possible, you should not modify zope.schema classes
    in-place
    as the same copy is shared between different threads and
    if there are two concurrent HTTP requests problems occur.

Replacing schema fields with dynamically modified copies
---------------------------------------------------------

The below is an example for z3c.form. It uses Python ``copy``
module to copy f.field reference, which points to zope.schema
field. For this field copy, we modify *required* attribute based
on input.

Example::

        @property
        def fields(self):
            """ Get the field definition for this form.

            Form class's fields attribute does not have to
            be fixed, it can be property also.
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

Don't use dict {} or list [] as a default value
--------------------------------------------------

Because how Python object construction works, giving [] or {}
as a default value will make all created field values to share this same object.

http://effbot.org/zone/default-values.htm

Use value adapters instead

* https://pypi.python.org/pypi/plone.directives.form#value-adapters

.. |---| unicode:: U+02014 .. em dash
