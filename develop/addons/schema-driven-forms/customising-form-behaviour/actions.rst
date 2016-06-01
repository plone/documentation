Actions (buttons)
=================

**Defining form buttons and executing code when they are clicked**

*z3c.form* defines a rich framework for defining, processing and
executing *actions*, an abstraction of the “outcome” of a form. Actions
are not necessarily related to form buttons, but for the vast majority
of use cases, we can think of forms buttons as a special type of widget
that represents an underlying action. Such “button actions” are usually
the only type of action we will ever use. Actions are nearly always
associated with a handler method, which will be called by the framework
when a form was submitted in response to a click of a particular button.

The usual way to define actions and buttons is to use the
*@button.buttonAndHandler()* decorator. This takes as a minimum the
button title as an argument. We have already seen two examples of this
in our pizza order form:

::

        @button.buttonAndHandler(_(u'Order'))
        def handleApply(self, action):
            ...

        @button.buttonAndHandler(_(u"Cancel"))
        def handleCancel(self, action):
            ...

The name of the method is not particularly important, but it needs to be
unique. The body of the handler function may react to the button however
is appropriate for the form’s use case. It may perform a redirect or
update form properties prior to re-rendering of the form. It should not
return anything. Use the *self.extractData()* helper to return a tuple
of the form’s submitted data and any errors, as shown in the preceding
examples.

The *action* argument is the action that was executed. We normally
ignore this, but it may be introspected to find out more about the
action. The *isExecuted()* method can be used to determine if the
corresponding button was indeed clicked, and would normally be *True*
within any action handler that is called by the framework. The *title*
attribute contains the button title as shown to the user.

Access keys
-----------

To define a HTML access key for a button, use the *accessKey* keyword
argument:

::

    @button.buttonAndHandler(_(u'Order'), accessKey=u"o")
        def handleApply(self, action):
            ...

Conditional actions
-------------------

If a button should only be shown in some cases, we can use the
*condition* keyword argument, passing a function that takes as its only
parameter the form to which the button belongs. If this does not return
*True*, the button will be omitted from the form:

.. code-block:: python

    ...

    import datetime

    def daytime(form):
        hour = datetime.datetime.now().hour
        return hour >= 9 and hour <= 17:


    class MyForm(form.SchemaForm)

        ...

        @button.buttonAndHandler(_(u'Give me a call'), condition=daytime)
        def handleCallBackRequest(self, action):
            ...

Updating button properties
--------------------------

As with regular widgets, it is sometimes useful to set properties on
buttons after they have been instantiated by *z3c.form*. One common
requirement is to add a CSS class to the button. The standard edit form
in *plone.dexterity* does this, for example, to add Plone’s
standard CSS classes. The usual approach is to override
*updateActions()*, which is called during the form update cycle:

::

        def updateActions(self):
            super(AddForm, self).updateActions()
            self.actions["save"].addClass("context")
            self.actions["cancel"].addClass("standalone")

Notice how we call the base class version first to ensure the actions
have been properly set up. Also bear in mind that if a button is
conditional, it may not be in *self.actions* at all.

Buttons are really just HTML input widgets, so you can set other
properties too, including attributes like onclick or ondblclick to
install client-side JavaScript event handlers.
