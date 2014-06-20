Validation
============

**How to validate a form prior to processing**

All forms apply some form of validation. In *z3c.form,* validators can
be executed in action handlers. If the validation fails, the action
handler can choose how to proceed. For “submit” type buttons, that
typically means showing error messages next to the relevant form fields.
For “cancel” type buttons, the validation is normally skipped entirely.

Form validation takes two forms: field-level validation, pertaining to
the value of an individual field, and form-level validation, pertaining
to the form as a whole. Form-level validation is less common, but can be
useful if fields have complex inter-dependencies.

Field-level validation
----------------------

The simplest field-level validation is managed by the fields themselves.
All fields support a *required* attribute, defaulting to *True*. The
default field validator will return an error if a required field is not
filled in. Some fields also support more specific properties that affect
validation:

-  Text fields like *Bytes, BytesLine, ASCII, ASCIILine, Text*and
   *TextLine*, as well as sequence fields like *Tuple, List,
   Set,**Frozenset* and *Dict* all support two properties, *min\_length*
   and *max\_length*, which can be set to control the minimum and
   maximum allowable length of the field’s value.
-  Numeric fields like *Int, Float* and *Decimal*, as well as temporal
   fields like *Date*, *Datetime* and *Timedelta* all support two
   properties, *min* and *max*, setting minimum and maximum (inclusive)
   allowable values. In this case, the min/max value needs to be of the
   same type as field, so for an *Int* field, the value of this property
   is an integer, whereas for a *Datetime* field, it is a Python
   *datetime* object.
-  A *Choice* field only allows values in a particular vocabulary. We
   will cover vocabularies in the next section.

Constraints
~~~~~~~~~~~

If you require more specific validation, and you have control over the
schema, you can specify a *constraint* function. This will be passed the
submitted value (which is converted to a value appropriate for the
field, so that e.g. a *List* field is passed a list). If the value is
acceptable, the function should return *True*. If not, it should raise a
*zope.schema.Invalid* exception or a derivative (returning *False* will
also result in an error, but one without a meaningful error message).

Here is the order form schema again, this time with a constraint
function:

::

    from five import grok
    from plone.supermodel import model

    from zope.interface import Invalid
    from zope import schema
    from z3c.form import button

    from Products.CMFCore.interfaces import ISiteRoot
    from Products.statusmessages.interfaces import IStatusMessage

    from example.dexterityforms.interfaces import MessageFactory as _

    def postcodeConstraint(value):
        """Check that the postcode starts with a 6
        """
        if not value.startswith('6'):
            raise Invalid(_(u"We can only deliver to postcodes starting with 6"))
        return True

    class IPizzaOrder(model.Schema):

        name = schema.TextLine(
                title=_(u"Your full name"),
            )

        address1 = schema.TextLine(
                title=_(u"Address line 1"),
            )

        address2 = schema.TextLine(
                title=_(u"Address line 2"),
                required=False,
            )

        postcode = schema.TextLine(
                title=_(u"Postcode"),
                constraint=postcodeConstraint,
            )

        telephone = schema.ASCIILine(
                title=_(u"Telephone number"),
                description=_(u"We prefer a mobile number"),
            )

        orderItems = schema.Set(
                title=_(u"Your order"),
                value_type=schema.Choice(values=[_(u'Margherita'), _(u'Pepperoni'), _(u'Hawaiian')])
            )

Notice how the *postcodeConstraint()*function is passed a value (a
unicode string in this case, since the field is a *TextLine*), which we
validate. If we consider the value to be invalid, we raise an *Invalid*
exception, with the error message passed as the exception argument.
Otherwise, we return *True*.

Field widget validators
~~~~~~~~~~~~~~~~~~~~~~~

Constraints are relatively easy to write, but they have two potential
drawbacks: First of all, they require that we change the underlying
interface. This is no problem if the interface exists only for the form,
but could be a problem if it is used in other contexts as well. Second,
if we want to re-use a validator for multiple forms, we would need to
modify multiple schemata.

z3c.form’s field widget validators address these shortcomings. These are
specific to the form; by contrast, constraints are a feature of
*zope.interface* interfaces and apply in other scenarios where
interfaces are used as well. *plone.directives.form* provides a
convenience decorator for creating simple field validators.

For example:

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from zope.interface import Invalid
    from zope import schema
    from z3c.form import button

    from Products.CMFCore.interfaces import ISiteRoot
    from Products.statusmessages.interfaces import IStatusMessage

    from example.dexterityforms.interfaces import MessageFactory as _

    ...


    class IPizzaOrder(model.Schema):

        ...

    class OrderForm(form.SchemaForm):

        ...

    @form.validator(field=IPizzaOrder['name'])
    def validateName(value):
        """Ensure names have a space (indicating a first name and surname)
        """

        if ' ' not in value:
            raise Invalid(_(u"Please give a full name"))

The *@form.validator()* decorator registers a validator adapter. When
the validation is invoked, the decorated function will be called with
the field’s value as an argument and given an opportunity to raise a
validation error, much like the constraint above. Again like the
constraint, the default validator is called first, so things like the
required flag and indeed any custom constraint are processed first.

The *@form.validator()* decorator can take keyword arguments to make the
validator more specific or more generic. The valid values are:

context
    The form’s context, typically an interface. This allows a validator
    to be invoked only on a particular type of content object.
request
    The form’s request. Normally, this is used to specify a browser
    layer.
view
    The form view itself. This allows a validator to be invoked for a
    particular type of form. As with the other options, we can pass
    either a class or an interface.
field
    A field instance, as illustrated above, or a field *type*, e.g. an
    interface like *zope.schema.IInt*.
widget
    The widget being used for the field

It is important to realise that if we don’t specify the *field*
discriminator, or if we pass a field type instead of an instance, the
validator will be used for all fields in the form (of the given type).
Also note how we had to define the constraint function before the form
schema interface (since it was referenced in the schema itself), but we
define this validator after the schema and form, since here we need the
interface to have been defined before we use it.

Advanced field widget validators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

z3c.form validators are in fact a little more powerful than what we have
seen above. A validator is registered as a multi-adapter providing
*z3c.form.interfaces.IValidator* and adapting the objects *(context,
request, view, field, widget)*, corresponding to the discriminants seen
above. You may wish to register an adapter directly instead of using the
*@form.validator()* decorator if you:

-  want to skip the default validation of field properties like
   *required* or *min*/*max*
-  need to access the context, request, form, field and/or widget
   instances to validate the value

We won’t show a full example here, but as an outline, consider the
following code snippet:

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from z3c.form import validator

    ...

    class SampleValidator(validator.SimpleFieldValidator):

        def validate(self, value):
            super(SampleValidator, self).validate(value)

            # validate here

    validator.WidgetValidatorDiscriminators(SampleValidator, field=IPizzaOrder['orderItems'], view=OrderForm)
    grok.global_adapter(SampleValidator)

This registers an adapter, extending the SimpleFieldValidator base
class, and calling the superclass version of validate() to gain the
default validation logic. In the validate() method, we can use variables
like self.context, self.request, self.view, self.field and self.widget
to access the adapted objects. The WidgetValidatorDiscriminators class
takes care of preparing the adapter discriminators. It takes the same
keyword arguments as @form.validator() seen above.

Form-level validation
---------------------

Form level validation is less common than field-level validation, but is
useful if your fields are inter-dependent in any ways. As with
field-level validation, there are two options:

-  Invariants are specified at the interface level. As such, they are
   analogous to constraints.
-  Widget manager validators are standalone adapters that are specific
   to *z3c.form*. As such, they are analogous to field widget
   validators.

Invariants
~~~~~~~~~~

Invariants work much like constraints, in that they are called during
the form validation cycle and may raise *Invalid* exceptions to indicate
a validation problem. Because they are not tied to fields specifically,
an error resulting from an invariant check is displayed at the top of
the form.

Invariants are written as functions inside the interface definition,
decorated with the *zope.interface.invariant* decorator. They are passed
a data object that provides the schema interface. In the case of a
*z3c.form* form, this is actually a special object that provides the
values submitted in the request being validated, rather than an actual
persistent object.

For example:

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from zope.interface import invariant, Invalid
    from zope import schema
    from z3c.form import button

    from Products.CMFCore.interfaces import ISiteRoot
    from Products.statusmessages.interfaces import IStatusMessage

    from example.dexterityforms.interfaces import MessageFactory as _

    ...

    class IPizzaOrder(model.Schema):

        name = schema.TextLine(
                title=_(u"Your full name"),
            )

        address1 = schema.TextLine(
                title=_(u"Address line 1"),
            )

        address2 = schema.TextLine(
                title=_(u"Address line 2"),
                required=False,
            )

        postcode = schema.TextLine(
                title=_(u"Postcode"),
                constraint=postcodeConstraint,
            )

        telephone = schema.ASCIILine(
                title=_(u"Telephone number"),
                description=_(u"We prefer a mobile number"),
            )

        orderItems = schema.Set(
                title=_(u"Your order"),
                value_type=schema.Choice(values=[_(u'Margherita'), _(u'Pepperoni'), _(u'Hawaiian')])
            )

        @invariant
        def addressInvariant(data):
            if data.address1 == data.address2:
                raise Invalid(_(u"Address line 1 and 2 should not be the same!"))

Here we have defined a single invariant, although there is no limit to
the number of invariants that you can use.

Widget manager validators
~~~~~~~~~~~~~~~~~~~~~~~~~

Invariants have most of the same benefits and draw-backs as constraints:
they are easy to write, but require modifications to the schema
interface, and cannot be generalised beyond the interface. Not
surprisingly therefore, *z3c.form* provides another option, in the form
of a widget manager validator. This is a multi-adapter for *(context,
request, view, schema, widget manager*) providing
*z3c.form.interfaces.IManagerValidator*. The default simply checks
invariants, although you can register your own override.

That said, overriding the widget manager validator is not particularly
common, because if you need full-form validation and you don’t want to
use invariants, it is normally easier to place validation in the action
handler, as we will see next.

Invoking validators
-------------------

Unlike some of the earlier form libraries, *z3c.form* does not
automatically invoke validators on every form submit. This is actually a
good thing, because it makes it much easier to decide when validation
makes sense (e.g. there is no need to validate a “cancel” button).

We have already seen the most common pattern for invoking validation in
our handler for the “order” button:

::

        @button.buttonAndHandler(_(u'Order'))
        def handleApply(self, action):
            data, errors = self.extractData()
            if errors:
                self.status = self.formErrorsMessage
                return

            # Handle order here. For now, just print it to the console. A more
            # realistic action would be to send the order to another system, send
            # an email, or similar

            ...

Notice how we call *extractData()*, which returns both a dictionary of
the submitted data (for valid fields, converted to the underlying field
value type) and a dictionary of errors (which is empty if all fields are
valid).

Validating in action handlers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes, it may be useful to perform additional validation in the
action handler itself. We can inspect the *data* dictionary, as well as
any other aspect of the environment (like *self.context*, the context
content object, or *self.request*, the request), to perform validation.

To signal an error, we use one of two exception types:

-  *z3c.form.interfaces.ActionExecutionError*, for generic, form-wide
   errors
-  *z3c.form.interfaces.WidgetActionExecutionError*, for
   field/widget-specific errors

In both cases, these exceptions wrap an *Invalid* exception. Let’s add
two examples to our action handler.

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from zope.interface import invariant, Invalid
    from zope import schema

    from z3c.form import button
    from z3c.form.interfaces import ActionExecutionError, WidgetActionExecutionError

    from Products.CMFCore.interfaces import ISiteRoot
    from Products.statusmessages.interfaces import IStatusMessage

    from example.dexterityforms.interfaces import MessageFactory as _


    ...


    class OrderForm(form.SchemaForm):

        ...

        @button.buttonAndHandler(_(u'Order'))
        def handleApply(self, action):
            data, errors = self.extractData()

            # Some additional validation
            if 'address1' in data and 'address2' in data:

                if len(data['address1']) < 2 and len(data['address2']) < 2:
                    raise ActionExecutionError(Invalid(_(u"Please provide a valid address")))
                elif len(data['address1']) < 2 and len(data['address2']) > 10:
                    raise WidgetActionExecutionError('address2', Invalid(u"Please put the main part of the address in the first field"))

            if errors:
                self.status = self.formErrorsMessage
                return

Notice how we perform the check after the *extractData()* call, but
before the possible premature return in case of validation errors. This
is to ensure all relevant errors are displayed to the user. Also note
that whilst the invariant is passed an object providing the schema
interface, the *data* dictionary is just that - a dictionary. Hence, we
use “dot notation” (*data.address1*) to access the value of a field in
the invariant, but “index notation” (*data[‘address1’]*)**to access the
value of a field in the handler.
