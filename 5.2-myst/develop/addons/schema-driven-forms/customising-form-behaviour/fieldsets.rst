Fieldsets
===========

**Breaking forms into multiple fieldsets**

*z3c.form* supports the grouping of form fields into what is known as
*groups*. A form class may mix in *z3c.form.group.GroupForm* to gain
support for groups, setting the *groups* variable to a list of *Group*
subclasses. The *Group* base class behaves much like the *Form* base
class, but is used only for grouping fields, and cannot have actions.

In Plone, groups are represented as fieldsets. The standard templates
make these look like dynamic tabs, much like those we can find in the
edit forms for most Plone content. For this reason,
*plone.supermodel* provides a directive called *model.fieldset()*,
which can be used to create fieldsets.

.. note::

    The *z3c.form* *Group* idiom is
    still supported, and can be mixed with the more declarative
    *model.fieldset()* approach. However, the latter is usually easier to
    use.

To illustrate fieldsets, let’s give customers the option to leave
feedback on our pizza ordering form. To keep our main form short, we
will put this in a separate fieldset. Note that there is still only one
set of submit buttons, i.e. all fieldsets are submitted at once. This is
purely for aesthetic effect.

::

    from example.dexterityforms.interfaces import MessageFactory as _
    from plone.autoform import directives as form
    from plone.supermodel import model
    from zope import schema

    ...

    class IPizzaOrder(model.Schema):

        # Main form

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
                value_type=schema.Choice(source=availablePizzas)
            )

        form.widget('notes', WysiwygFieldWidget)
        notes = schema.Text(
                title=_(u"Notes"),
                description=_(u"Please include any additional notes for delivery"),
                required=False
        )

        # Feedback fieldset

        model.fieldset(
            'feedback',
            label=_(u"Feedback"),
            fields=['feedbackNote', 'feedbackEmail']
        )

        feedbackNote = schema.Text(
                title=_(u"Feedback"),
                description=_(u"Please provide any feedback below"),
                required=False,
            )

        feebackEmail = schema.TextLine(
                title=_(u"Email address"),
                description=_(u"If you'd like us to contact you, please give us an email address below"),
                required=False,
            )

        ...

.. note::

    Since this approach uses form schema hints, the schema must derive from
    *model.Schema* and the form base class must extend *plone.autoform.AutoExtensibleForm*. In our example, we are using *SchemaForm*,
    a subclass of AutoExtensibleForm.

Above, we have declared a single fieldset, and listed the fields within
it. Those fields not explicitly associated with a fieldset end up in the
“default” fieldset. We also set a fieldset name and label. The label is
optional.

It is possible to use the same fieldset name multiple times in the same
form. This is often the case when we use the *additional\_schemata*
property to set secondary schemata for our form. In this case, the
*label* from the first *fieldset* directive encountered will be used.
