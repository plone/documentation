Creating the form view
======================

**Using our schema in a form**

To render our form, we need to create a view that uses a *z3c.form* base
class. The view is registered like any other in ZCML.
It is then configured with the schema to use for form fields, the label
(page title) and description (lead-in text) to show, and actions to
render as buttons.

Still in *order.py*, we add the following:

.. code-block :: py

    class OrderForm(AutoExtensibleForm, form.Form):
        schema = OrderFormSchema
        form_name = 'order_form'

        label = _(u"Order your pizza")
        description = _(u"We will contact you to confirm your order and delivery.")

        def update(self):
            # disable Plone's editable border
            self.request.set('disable_border', True)

            # call the base class version - this is very important!
            super(OrderForm, self).update()

        @button.buttonAndHandler(_(u'Order'))
        def handleApply(self, action):
            data, errors = self.extractData()
            if errors:
                self.status = self.formErrorsMessage
                return

            # Handle order here. For now, just print it to the console. A more
            # realistic action would be to send the order to another system, send
            # an email, or similar

            print u"Order received:"
            print u"  Customer: ", data['name']
            print u"  Telephone:", data['telephone']
            print u"  Address:  ", data['address1']
            print u"            ", data['address2']
            print u"            ", data['postcode']
            print u"  Order:    ", ', '.join(data['orderItems'])
            print u""

            # Redirect back to the front page with a status message

            IStatusMessage(self.request).addStatusMessage(
                    _(u"Thank you for your order. We will contact you shortly"),
                    "info"
                )

            contextURL = self.context.absolute_url()
            self.request.response.redirect(contextURL)

        @button.buttonAndHandler(_(u"Cancel"))
        def handleCancel(self, action):
            """User cancelled. Redirect back to the front page.
            """
            contextURL = self.context.absolute_url()
            self.request.response.redirect(contextURL)

The  form is registered in configure.zcml

.. code-block :: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        xmlns:plone="http://namespaces.plone.org/plone"
        i18n_domain="example.form">

        <!-- Set overrides folder for Just-a-Bunch-Of-Templates product -->
        <include package="z3c.jbot" file="meta.zcml" />
        <browser:jbot
            directory="overrides"
            layer="example.form.interfaces.IExampleFormLayer"
            />

        <!-- Publish static files -->
        <browser:resourceDirectory
            name="example.form"
            directory="static"
            />

        <adapter factory=".order.OrderFormAdapter"/>

        <browser:page
            for="Products.CMFCore.interfaces.ISiteRoot"
            name="order-pizza"
            class=".order.OrderForm"
            permission="zope2.View"
            />

    </configure>


Let’s go through this in some detail:

-  We derive our form view from one of the standard base classes in
   *plone.autoform*. It comes without any of the standard
   actions that can be found on more specialised base classes such as
   *SchemaAddForm* or *SchemaEditForm*. It basically mirrors the
   *z3c.form.form.Form* base class.
-  Next, we specify the schema via the *schema* attribute.
-  We set *ignoreContext* to *True*. This tells *z3c.form* not to
   attempt to read the current value of any of the form fields from the
   context. The default behaviour is to attempt to adapt the context
   (the Plone site root in this case) to the schema interface and read
   the schema attribute value from this adapter when first populating
   the form. This makes sense for edit forms and things like control
   panels, but not for a standalone form like this.
-  We then set a *label* and *description* for the form. In the standard
   form template, these are rendered as a page header and lead-in text,
   respectively.
-  We override the *update()* method to set the *disable\_border*
   request variable. This hides the editable border when rendering the
   form. We then call the base class version of *update()*. This is
   crucial for the form to work! *update()* is a good place to perform
   any pre-work before the form machinery kicks in (before calling the
   base class version) or post-processing afterwards (after calling the
   base class version). See the section on the form rendering lifecycle
   later in this manual for the gory details.
-  Finally, we define two actions, using the
   *@button.buttonAndHandler()* decorator. Each action is rendered as a
   button (in order). The argument is a (translated) string that will be
   used as a button label. The decorated handler function will be called
   when the button is clicked.
-  We then use the standard way to register the view via zcml:
   *name* gives it a friendly name (used as a path segment
   in the URL); *for* sets the type of context where the form
   is available (here, we make it available on the Plone site root,
   though any interface or class may be passed; to make the form
   available on any context, use * as *for*); *permission* specifies a permission which the user must
   have to be able to view the form (here, we use the standard
   *zope2.View* permission).

For the purposes of this test, the actual work we do with the main
handler is relatively contrived. However, the patterns are generally
applicable.

The second button (cancel) is the simpler of the two. It performs no
validation and simply redirects to the context’s default view, i.e. the
portal front page in this case.

The first button actually extracts the data from the form, using
*self.extractData()*. This returns a tuple of the form data, which has
been converted to the field’s underlying type by each widget (thus, the
value corresponding to the *Set* field contains a *set*) and any errors.
If there are errors, we abort, setting *self.status* to confer an error
message at the top of the page. Otherwise, we use the form data (here
just printing the output to the console - you need to run Zope in
foreground mode to see these messages), add a cookie-tracked status
message (so that it can appear on the next page) and redirect the user
to the context’s default view. In this case, that means the portal front
page.


.. _five.grok: https://pypi.python.org/pypi/five.grok
