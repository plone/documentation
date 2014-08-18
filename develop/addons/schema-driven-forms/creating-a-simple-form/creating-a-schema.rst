Creating a schema
=================

**The starting point for our form**

With the form package created and installed, we can create our form
schema. Whilst it is strictly not necessary yet, we will use the
*Schema* interface base from *plone.autoform.* This lets us use
schema directives (as seen in Dexterity content type schemata) to
configure custom widgets, set up hidden fields and so on. Later in this
manual, we will cover in more detail how you can perform these
operations imperatively in Python code.

The example we’ll use for this form is a pizza ordering form. We’ll
build on this form over the coming sections, so if you look at the
example source code, you may find a few extra bits. However, the basics
are simple enough.

We’ll create a module called *order.py* inside our package
(*example/dexterityforms/order.py)*, and add the following code to it:

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from zope import schema
    from z3c.form import button

    from Products.CMFCore.interfaces import ISiteRoot
    from Products.statusmessages.interfaces import IStatusMessage

    from example.dexterityforms.interfaces import MessageFactory as _

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
            )
        
        telephone = schema.ASCIILine(
                title=_(u"Telephone number"),
                description=_(u"We prefer a mobile number"),
            )

        orderItems = schema.Set(
                title=_(u"Your order"),
                value_type=schema.Choice(values=[_(u'Margherita'), _(u'Pepperoni'), _(u'Hawaiian')])
            )

For now, this form is quite simple. The list of pizzas is hard-coded,
and we can only choose one of each type. We will make it (a little) more
realistic later by adding a better vocabulary, creating a custom widget
for the pizza order part, and improving the look and feel with a custom
template.

At the top, we have included a number of imports. Some of these pertain to the form view, which will be described next.
Other than that, we have simply defined a schema that describes the form’s fields. The *title* and *description* of each field are used as label and help text, respectively.
The *required* attribute can be set to *False* for optional fields. 
For a full field and widgets reference, see the :doc:`Dexterity developer manual </external/plone.app.dexterity/docs/index>`. 
(It is no accident that the Dexterity content type fields and widgets are defined in the same manner as those of a standalone form!)

Also notice how all the user-facing strings are wrapped in the message
factory to make them translatable. The message factory is imported as
*\_*, which helps tools like *gettext* extract strings for translation.
If you are sure your form will never need to be translated, you can skip
the message factory in *interfaces.py* and use plain unicode strings,
i.e. *u“Postcode”* instead of *\_(u“Postcode”)*

We are almost done with our most basic form. Before we can use the form,
however, we need to create a form view and define some actions
(buttons). That is the subject of the next section.


