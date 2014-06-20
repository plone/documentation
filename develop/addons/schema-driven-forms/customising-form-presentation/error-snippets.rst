Error snippets
===============

**Customising error messages**

When creating custom validators, as shown earlier in this manual, it is
easy to tailor an error message. However, *zope.schema* and *z3c.form*
already perform a fair amount of validation for us, which results in
generic error messages. For example, if a required field is not
completed, a rather bland error message (“Required input is missing”)
will be shown. Sometimes, we may want to change these messages.

*z3c.form* allows error messages to be customised at various levels of
detail. For example, it is possible to register a
custom *z3c.form.interfaces.IErrorViewSnippet* adapter, which behaves
like a mini-view and can output arbitrary HTML. However, in most cases,
we only want to update the output text string. For this, we use what’s
known as a “value adapter”. This is simply an adapter which *z3c.form*’s
default *IErrorViewSnippet* implementations will look up to determine
which message to show.

The easiest way to create an error message value adapter is to use the
*@form.error\_message()* decorator from *plone.directives.form*. This
decorator should be applied to a function that takes as its only
argument the (invalid) value that was submitted, and return a unicode
string or message indicating the error. To illustrate this, we will add
a new function to *order.py*, just after the interface definition:

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from zope.interface import invariant, Invalid
    from zope.component import queryUtility

    from zope import schema

    from zope.schema.interfaces import IContextSourceBinder
    from zope.schema.interfaces import RequiredMissing
    from zope.schema.vocabulary import SimpleVocabulary

    ...

    from example.dexterityforms.interfaces import MessageFactory as _

    ...

    class IPizzaOrder(model.Schema):

        ...

        telephone = schema.ASCIILine(
                title=_(u"Telephone number"),
                description=_(u"We prefer a mobile number"),
            )

        ...

    @form.error_message(field=IPizzaOrder['telephone'], error=RequiredMissing)
    def telephoneOmittedErrorMessage(value):
        return u"Without your telephone number, we can't contact you in case of a problem."

As with the *@form.validator()* decorator, the *@form.error\_message()*
validator takes a number of keyword arguments, used to control where the
error message is applied. The allowable arguments are:

error
    The type of error, which is normally represented by an exception
    class. The most general type will usually be a
    *zope.schema.interfaces.ValidationError*. See below for a list of
    other common exception types.
request
    The current request. This is normally used to supply a browser layer
    marker interface. This is a good way to ensure a general error
    message is only in force when our product is installed.
widget
    The widget which was used to render the field.
field
    The field to which the error message applies. If this is omitted,
    the message would apply to all fields on the form (provided *form*
    is supplied) of the given error (provided *error* is applied).
form
    The form class. We can use this either to apply a single message to
    a given error across multiple fields in one form (in which case
    *field* would be omitted), or to customise an error message for a
    particular form only if a schema is used in more than one form.
content
    The content item (context) on which the form is being rendered.

.. note::
    In almost all cases, you will want to supply both *field* and *error* at
    a minimum, although if you have multiple fields that may raise a
    particular error, and you want to create a message for all instances of
    that error, you can omit *field* and use *form* instead. If you supply
    just *error*, the validator will apply to all instances of that error,
    on all forms, site-wide, which is probably not a good idea if you intend
    your code to be-usable. At the very least, you should use the *request*
    field to specify a browser layer in this case, and install that layer
    with *browserlayer.xml* in your product’s installation profile.

The exception types which may be used for the *error* discriminator are
field-specific. The standard fields as defined in *zope.schema* use the
following exceptions, all of which can be imported from
*zope.schema.interfaces*:

-  *RequiredMissing*, used when a required field is submitted without a
   value
-  *WrongType*, used when a field is passed a value of an invalid type
-  *TooBig* and *TooSmall*, used when a value is outside the *min*
   and/or *max* range specified for ordered fields (e.g. numeric or date
   fields)
-  *TooLong* and *TooShort*, used when a value is outside the
   *min\_length* and/or *max\_length* range specified for length-aware
   fields (e.g. text or sequence fields)
-  *InvalidValue*, used when a value is invalid, e.g. a non-ASCII
   character passed to an ASCII field
-  *ConstraintNotSatisfied*, used when a *constraint* method returns
   *False*
-  *WrongContainedType*, used if an object of an invalid type is added
   to a sequence (i.e. the type does not conform to the field’s
   *value\_type*)
-  *NotUnique*, used if a uniqueness constraint is violated
-  *InvalidURI*, used for *URI* fields if the value is not a valid URI
-  *InvalidId*, used for *Id* fields if the value is not a valid id
-  *InvalidDottedName*, used for *DottedName* fields if the value is not
   a valid dotted name
