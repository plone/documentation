================
z3c.form library
================

.. admonition:: Description

    ``z3c.form`` is flexible and powerful form library for Zope 3 applications.
    It is the recommended way to create complex Python-driven forms for
    Plone 4 and later versions.


Introduction
=============

Plone uses *z3c.form* library with the following integration steps

* `plone.app.z3cform <https://pypi.python.org/pypi/plone.app.z3cform>`_ provides
  Plone specific widgets and main template

* `plone.z3cform <https://pypi.python.org/pypi/plone.z3cform>`_ integrates *z3c.form*
  with applications using Zope 2 mechanisms like acquisition

* `z3c.form <https://pypi.python.org/pypi/z3c.form/>`_ is a form library which can be
  used with any Python application using Zope 3 HTTP requests objects

* (Plone 4.4+ only) `plone.app.widgets <https://github.com/plone/plone.app.widgets/>`_
  provide a better widget set over *z3c.form* default with more JavaScript-enabled
  features

Forms are modelled using :doc:`zope.schema </develop/plone/forms/schemas>` models written as Python classes.
Widgets for modelled data are set by using either *plone.directives.form* hints set onto
schema class or in ``z3c.form.form.Form`` based classes body.

Starting points to learn *z3c.form* in Plone

* Read about :doc:`creating schema-driven forms with Dexterity content subsystem </develop/addons/schema-driven-forms/index>`

* `Plone training manual <http://training.plone.org/5>`__

Other related packages you might want to take a closer look

* Extra, more powerful widgets, from `collective.z3cform.widgets <https://github.com/collective/collective.z3cform.widgets>`_

* Tabular data edit `collective.z3cform.datagridfield <https://github.com/collective/collective.z3cform.datagridfield>`_

* Build JavaScript interfaces with `plone.app.jqueryui <https://github.com/plone/plone.app.jqueryui>`_

* Handling image and file fields with `plone.namedfile <https://github.com/plone/plone.namedfile>`_

* Configuring forms with `plone.directives.form <https://pypi.python.org/pypi/plone.directives.form>`_

``z3c.form`` big picture
========================

The form model consists of:

``self.request``
    The incoming HTTP request.

``self.context``
    The Plone content item which was associated with the form view when URL
    traversing was done.

``self.getContent()``
    The actual object extracted from context and manipulated by the form if
    ``ignoreContext`` is not ``False``.

``self.status``
    A message displayed at the top of the form to the user when the form is
    rendered. Usually it will be "Please correct the errors below".

The call-chain for a form goes like this:

* ``Form.update()`` is called

    * [``plone.autoform``-based forms only]
      Calls ``Form.updateFields()`` - this will set widget factory
      methods for fields. If you want to customize the type
      of the widget associated with the field, do it here. If
      your form is not ``plone.autoform``-based you need to
      edit ``form.schema`` widget factories on the module level code
      after the class has been constructed. The logic
      mapping widget hints to widgets is in ``plone.autoform.utils``.

    * Calls ``Form.updateWidgets()`` - you can customize widgets at this
      point, if you override this method. The ``self.widgets`` instance
      is created based on the ``self.fields`` property.

    * Calls ``Form.updateActions()``

        * Calls the action handler (the handler for the button which was
          clicked)

        * If it's an edit form, the action handler calls ``applyChanges()``
          to store new values on the object and returns ``True``
          if any value was changed.

* ``Form.render()`` is called

    * This renders the form as HTML, based on widgets and their templates.

Form
====

Simple boilerplate
------------------

Here is a minimal form implementation using ``z3c.form`` and Dexterity:

* Include Dexterity in your buildout as instructed by Dexterity manual

* Create Plone add-on product using `Paster <http://docs.plone.org/4/en/develop/addons/paste.html>`_

.. deprecated:: may_2015
    Use :doc:`bobtemplates.plone </develop/addons/bobtemplates.plone/README>`

* Register the form in ``configure.zcml``::



    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        xmlns:five="http://namespaces.zope.org/five"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
        xmlns:i18n="http://namespaces.zope.org/i18n"
        i18n_domain="example.dexterityforms">

      ...

        <browser:page
              for="Products.CMFCore.interfaces.ISiteRoot"
              name="my-form"
              permission="zope2.View"
              class=".form.MyForm"
              />

    </configure>


* Toss ``form.py`` into your add-on product::

    """

        Simple sample form

    """

    from plone.directives import form

    from zope import schema
    from z3c.form import button

    from Products.CMFCore.interfaces import ISiteRoot
    from Products.statusmessages.interfaces import IStatusMessage


    class IMyForm(form.Schema):
        """ Define form fields """

        name = schema.TextLine(
                title=u"Your name",
            )

    class MyForm(form.SchemaForm):
        """ Define Form handling

        This form can be accessed as http://yoursite/@@my-form

        """

        schema = IMyForm
        ignoreContext = True

        label = u"What's your name?"
        description = u"Simple, sample form"

        @button.buttonAndHandler(u'Ok')
        def handleApply(self, action):
            data, errors = self.extractData()
            if errors:
                self.status = self.formErrorsMessage
                return

            # Do something with valid data here

            # Set status on this form page
            # (this status message is not bind to the session and does not go thru redirects)
            self.status = "Thank you very much!"

        @button.buttonAndHandler(u"Cancel")
        def handleCancel(self, action):
            """User cancelled. Redirect back to the front page.
            """


Setting form status message
---------------------------

The form's global status message tells whether the form action succeeded or
not.

The form status message will be rendered only on the form.
If you want to set a message which will be visible even if the user renders
another page after submitting the form,
you need to use ``Products.statusmessage``.

To set the form status message::

    form.status = u"My message"


Emulating form HTTP POST in unit tests
--------------------------------------

* The HTTP request must include at least one buttons field.

* Form widget naming must match HTTP post values. Usually widgets have
  ``form.widgets`` prefix.

* You must emulate the ZPublisher behavior
  which automatically converts string input to Python primitives.
  For example, all choice/select values are Python lists.

* Some ``z3c`` widgets, like ``<select>``, need to have
  ``WIDGETNAME-empty-marker`` value set to
  the integer 1 to be processed.

* Usually you can get the dummy HTTP request object via acquisition from
  ``self.portal.REQUEST``

Example (incomplete)::

    layout = "accommondationsummary_view"

    # Zope publisher uses Python list to mark <select> values
    self.portal.REQUEST["form.widgets.area"] = [SAMPLE_AREA]
    self.portal.REQUEST["form.buttons.search"] = u"Search"
    view = self.portal.cards.restrictedTraverse(layout)

    # Call update() for form
    view.process_form()
    print view.form.render()

    # Always check form errors after update()
    errors = view.errors
    self.assertEqual(len(errors), 0, "Got errors:" + str(errors))

A more complete example::

    # -*- coding: utf-8 -*-
    from freitag.membership.testing import FREITAGMEMBERSHIP_INTEGRATION_TESTING
    from z3c.form.interfaces import IFormLayer
    from zope.interface import alsoProvides

    import unittest

    FORM_ID = 'password_reset'


    class TestPasswordReset(unittest.TestCase):

        layer = FREITAGMEMBERSHIP_INTEGRATION_TESTING

        def setUp(self):
            self.portal = self.layer['portal']

        def test_nonexisting_fridge_rand(self):
            # create a password reset form
            self.portal.REQUEST["form.widgets.password"] = u'tatatata'
            self.portal.REQUEST["form.widgets.password_repeat"] = u'tatatata'
            self.portal.REQUEST["form.widgets.fridge_rand"] = 'nonexisting'
            self.portal.REQUEST["form.buttons.submit"] = u"Whatever"
            alsoProvides(self.portal.REQUEST, IFormLayer)
            form = self.portal.password_resetter.restrictedTraverse(FORM_ID)
            form.update()

            # data, errors = resetForm.extractData()
            data, errors = form.extractData()
            self.assertEqual(len(errors), 0)

Note that you will need to set ``IFormLayer`` on the request,
to prevent a ``ComponentLookupError``.


Changing form ACTION attribute
------------------------------

By default, the HTTP ``POST`` request is made to ``context.absolute_url()``.
However you might want to make the post go to an external server.

* See `how to set <form> action attribute <https://pypi.python.org/pypi/plone.app.z3cform#form-action>`_

Customizing form inner template
-------------------------------

If you want to change the page template producing ``<form>...</form>``
part of the HTML code, follow the instructions below.

.. note:: Generally, when you have a template which extends Plone's
   ``main_template`` you need to use the
   ``Products.Five.browser.pagetemplatefile.ViewPageTemplateFile``
   class.

Example::

    # Do not mix with Products.Five.browser.pagetemplatefile.ViewPageTemplateFile
    from zope.app.pagetemplate import ViewPageTemplateFile as Zope3PageTemplateFile

    class AddHeaderAnimationForm(crud.AddForm):
        """ Present form for adding a header animation """

        template = Zope3PageTemplateFile("custom-form-template.pt")


Customizing form frame
----------------------

Please see `plone.app.z3cform README <https://github.com/plone/plone.app.z3cform>`__.

Rendering a form manually
-------------------------

You can directly create a form instance and call it's ``form.render()`` method.
This will output the full page HTML. However, there is a way to only render the form
body payload.

First create a form and ``update()``::

       view.form = MyFormClass(self.context, self.request)
       view.form.update()

Then you can invoke ``plone.app.z3cform`` macros directly to render the form body
in your view's page template.

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:metal="http://xml.zope.org/namespaces/metal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          metal:use-macro="here/main_template/macros/master"
          i18n:domain="plone.app.widgets"
          lang="en"
          >
    <body>

        <metal:main fill-slot="main">
            <tal:main-macro metal:define-macro="main">

              <h1 class="documentFirstHeading">Plone fields and widgets demo</h1>

              <div id="skel-contents">
                <tal:form repeat="form view/demos">

                    <!-- plone.app.z3cform package provides view ploneform-macros
                         which come with a helpers to render forms. This one
                         will render the form body only. It also makes an assumption
                         that form is presented in "view" TAL variable.

                      -->
                    <tal:with-form-as-view define="view nocall:form">
                        <metal:block use-macro="form/@@ploneform-macros/titlelessform" />
                    </tal:with-form-as-view>

                </tal:form>
              </div>

            </tal:main-macro>
        </metal:main>
    </body>
    </html>

Fields
======

A field is responsible for:
1) pre-populating form values from context
2) storing data to context after successful ``POST``.

Form fields are stored in the ``form.fields`` variable,
which is an instance of the ``Fields`` class (ordered, dictionary-like).

Creating a field
----------------

Fields are created by adapting one or more ``zope.schema`` fields
for ``z3c.form`` using the ``Fields()`` constructor.

Example of creating one field::

    import zope.schema
    import z3c.form.field

    schema_field = zope.schema.TextLine()
    form_fields = z3c.form.field.Fields(schema_field)

    # This is a reference to newly created z3c.form.field.Field object
    one_form_field = zfields.values()[0]

Another example::

    import zope.schema
    import z3c.form.field

    ...

    field = zope.schema.Bool(
                    __name__ = "death_autofill",
                    title=_(u"Fill missing timepoints"),
                    description=_(u"Automatically fill information in missing timepoints if they occur after the death time"),
                    required=False,
                    default=True)

    # Construct z3c.form field
    fields_objects = z3c.form.field.Fields(field)

    # We can perform autofill only if we know the treatment time
    form.fields += fields_objects

Adding a field to a form
------------------------

Use the overridden ``+=`` operator of a ``Fields`` instance.
Fields instances can be added to existing Fields instances.

Example::

    self.form.fields += z3c.form.Fields(schema_field)

Modifying a field
-----------------

Fields can be accessed by their name in ``form.fields``. Example::

    self.form.fields["myfieldname"].name = u"Foobar"

Accessing the schema of the field
---------------------------------

A ``zope.schema`` Field is stored as a ``field`` attribute of a field.
Example::

    textline = self.form.fields["myfieldname"].field # zope.schema.TextLine

.. note::

    There exist only one singleton instance of a schema during run-time.
    If you modify the schema fields, the changes are reflected to
    all subsequent form updates and other forms which use the
    same schema.

Read-only fields
----------------

There is ``field.readonly`` flag.

Example code:

.. code-block:: python

    class AREditForm(crud.EditForm):
        """ Form whose fields are dynamically constructed """

        def ar_editable(self):
            """ Arbitrary condition deciding whether fields on this form are
            patient=self.__parent__.__parent__
            if patient.getConfirmedAR()  in (None,'','EDITABLE_AR'):
                return True
            return False


        @property
        def fields(self):
            """
            Dynamically create field data based on run-time constructed schema.

            Instead using static ``fields`` attribute, we use Python property
            which allows us to generate z3c.form.fields.Fields instance for the
            for run-time.
            """


            constructor = ARFormConstructor(self.context, self.context.context, self.request)

            # Create z3c.form.field.Fields object instance
            fields = constructor.getFields()

            if not self.ar_editable():
                # Disable all fields in edit mode if this form is locked out
                for f in fields.values():
                    f.mode = z3c.form.interfaces.DISPLAY_MODE

            return fields

You might also want to disable the *edit* button if none of the fields are
editable::

    # Make the edit button conditional
    AREditSubForm.buttons["apply"].condition = lambda form: form.has_edit_button()

.. note::

    You can also set ``z3c.form.interfaces.DISPLAY_MODE`` in
    ``updateWidgets()``
    if you are not dynamically poking form fields themselves.

.. warning::

    Do not modify fields on singleton instances (form or fields objects are
    shared between all forms).
    This causes problems on concurrent access.

.. note::

    ``zope.schema.Field`` has a ``readonly`` property.
    ``z3c.form.field.Field`` does not have this property,
    but has the ``mode`` property. Do not confuse these two.

Dynamic schemas
---------------

Below is an example of how to include new schemas on the fly:

.. code-block:: python

    class EditForm(dexterity.EditForm, Helper):

        grok.context(IFlexibleContent)

        def updateFields(self):

            super(dexterity.EditForm, self).updateFields()
            sections = self.getSections()

            # See plone.app.z3cform.fieldsets.extensible for more examples
            for s in sections:

                # s = {'schema': <InterfaceClass your.app.content.flexiblecontent.IBodyText>, 'id': u'title', 'name': u'Title'}
                if s == None:
                    # This section has been removed from available flexi_blocks
                    continue

                # convert zope schema interface to z3c.form.Fields instance
                schema = s["schema"]

                if not schema.providedBy(self.context):
                    # We need to force the content item to provide
                    # custom for interfaces or datamanger is not happy
                    #   Module z3c.form.datamanager, line 51, in adapted_context
                    #   TypeError: ('Could not adapt', <Item at /xxx/tydryd>, <InterfaceClass xxx.app.content.flexiblecontent.IColumns>)
                    alsoProvides(self.context, schema) # XXX: This is persistent change?

                # We need to manually apply hints from plone.directives.form, as
                # updateFields() does it for base schema earlier
                processFields(self, schema, permissionChecks=True)

            print "Final results"
            for name, field in self.fields.items():
                print str(name) + " " + str(field)

Date and time
-------------

Example:

.. code-block:: python

    class IDeal(form.Schema):
        """
        Deals and discounts item
        """

        validUntil = schema.Datetime(title=u"Valid until")

See

* http://stackoverflow.com/questions/5776498/specify-datetime-format-on-zope-schema-date-on-plone

* http://svn.zope.org/zope.schema/trunk/src/zope/schema/tests/test_datetime.py?rev=113055&view=auto

Making boolean field required
-----------------------------

E.g. to make "Accept Terms and Conditions" checkbox

* http://stackoverflow.com/questions/9670819/how-do-i-make-a-boolean-field-required-in-a-z3c-form

Widgets
=======

Widget are responsible for
1) rendering HTML code for input;
2) parsing HTTP post input.

Widgets are stored as the ``widgets`` attribute of a form.
It is presented by an ordered dict-like ``Widgets`` class.

Widgets are only available after the form's ``update()`` and
``updateWidgets()`` methods have been called.
``updateWidgets()`` will bind widgets to the form context.
For example, vocabularies defined by name are resolved at this point.

A widget has two names:

    * ``widget.__name__`` is the name of the corresponding field.
      Lookups from ``form.widgets[]`` can be done using this name.

    * ``widget.name`` is the decorated name used in HTML code.
      It has the format
      ``${form name}.${field set name}.${widget.__name__}``.

The Zope publisher will also mangle widget names based on what kind of input
the widget takes. When an HTTP ``POST`` request comes in,
Zope publisher automatically converts ``<select>`` dropdowns to lists and so
on.

Setting a widget for a field
----------------------------

Using plone.directives.form schema hints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example::

    from plone.directives import form
    from zope import schema
    from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

    class ISampleSchema(form.Schema):

        # A fieldset with id 'extra' and label 'Extra information' containing
        # the 'footer' and 'dummy' fields. The label can be omitted if the
        # fieldset has already been defined.

        form.fieldset('extra',
                label=u"Extra information",
                fields=['footer', 'dummy']
            )

        # Here a widget is specified as a dotted name.
        # The body field is also designated as the priamry field for this schema

        form.widget(body='plone.app.z3cform.wysiwyg.WysiwygFieldWidget')
        form.primary('body')
        body = schema.Text(
                title=u"Body text",
                required=False,
                default=u"Body text goes here"
            )

More info

* :doc:`Form schema hints </external/plone.app.dexterity/docs/reference/form-schema-hints>`


Setting widget for z3c.form plain forms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can set field's widgetFactory after fields have
been declared in form class body.

Example::

    import zope.schema
    import zope.interface

    import z3c.form
    from z3c.form.browser.checkbox import CheckBoxFieldWidget


    class IReportSchema(zope.interface.Interface):
        """ Define reporter form fields """

        variables = zope.schema.List(
            title=u"Variables",
            description=u"Choose which variables to include in the output report",
            required=False,
            value_type=zope.schema.Choice(vocabulary="output_variables"))


    class ReportForm(z3c.form.form.Form):
        """ A form to output a HTML report from chosen parameters """

        fields = z3c.form.field.Fields(IReportSchema)

        fields["variables"].widgetFactory = CheckBoxFieldWidget



Setting widget dynamically Form.updateWidgets()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Widget type can be set dynamically based on external conditions.

::

    class EditForm9(EditForm):
        label = u'Rendering widgets as blocks instead of cells'

        grok.name('demo-collective.z3cform.datagrid-block-edit')

        def updateWidgets(self):
            super(EditForm9, self).updateWidgets()
            # Set a custom widget for a field for this form instance only
            self.fields['address'].widgetFactory = BlockDataGridFieldFactory


Accessing a widget
------------------

A widget can be accessed by its field's name. Example::

    class MyForm(z3c.form.Form):

        def update(self):
            z3c.form.Form.update(self)
            widget = form.widgets["myfieldname"] # Get one widget

            for w in widget.items(): print w # Dump all widgets


Introspecting form widgets
--------------------------

Example::

    from z3c.form import form

    class MyForm(form.Form):

        def updateWidgets(self):
            """ Customize widget options before rendering the form. """
            form.Form.updateWidgets(self)

            # Dump out all widgets - note that each <fieldset> is a subform
            # and this function only concerns the current fieldset
            for i in self.widgets.items():
                print i

Reordering and hiding widgets
-----------------------------

With Dexterity forms you can use
`plone.directives.form <https://pypi.python.org/pypi/plone.directives.form>`_::

    from z3c.form.interfaces import IAddForm, IEditForm

    class IFlexibleContent(form.Schema):
        """
        Description of the Example Type
        """

        # -*- Your Zope schema definitions here ... -*-
        form.order_before(sections='title')
        form.mode(sections='hidden')
        form.mode(IEditForm, sections='input')
        form.mode(IAddForm, sections='input')
        sections = schema.TextLine(title=u"Sections")



Modifying a widget
------------------

Widgets are stored in the ``form.widgets`` dictionary, which maps
*field name* to *widget*.
The widget label can be different than the field name.

Example::

    from z3c.form import form

    class MyForm(form.Form):

        def updateWidgets(self):
            """ Customize widget options before rendering the form. """

            self.widgets["myfield"].label = u"Foobar"

If you want to have a completely different Python class
for a widget, you need to override field's widget factory in
the module body code after fields have been constructed in the class,
or in the ``update()`` method for dynamically constructed fields::

   def updateWidgets(self):
        self.fields["animation"].widgetFactory = HeaderFileFieldWidget

Reorder form widgets
--------------------

``plone.z3cform`` allows you to reorder the field widgets by overriding the
``update`` method of the form class.

Example::

    from z3c.form import form
    from plone.z3cform.fieldsets.utils import move

    class MyForm(form.Form):

        def update(self):
        super(MyForm, self).update()
        move(self, 'fullname', before='*')
        move(self, 'username', after='fullname')
        super(ProfileRegistrationForm, self).update()

For more information about how to reorder fields see the ``plone.z3cform``
page at PyPI:

<https://pypi.python.org/pypi/plone.z3cform#fieldsets-and-form-extenders>`_


Hiding fields
-------------

Here's how to do it in pure ``z3c.form``::

    import z3c.form.interfaces
    ...

        def updateWidgets(self):
            self.widgets["getAvailability"].mode = z3c.form.interfaces.HIDDEN_MODE

If you want to hide a widget that is part of a group, you cannot use the updateWidgets method.
The groups and their widgets get initialized after the widgets have been updated.
Before that, the groups variable is just a list of group factories.
During the update method though, the groups have been initialized and have their own widget list each.
For hiding widgets there, you have to access the group in the update method like so::


    import z3c.form.interfaces
    ...

        def update(self):
            for group in self.groups:
                if 'xxx' in group.widgets:
                    group.widgets['xxx'].mode = z3c.form.interfaces.HIDDEN_MODE

groups itself is a list like object, you can also remove a complete group by removing it from the group dictionary.

Unprefixing widgets
-------------------

By default each form widget gets a name prefixed by the form id.
This allows you to combine several forms on the same page.

You can override this behavior in ``updateWidgets()``::

    # Remove prefix from form widget names, so that
    # the names are actual names on the remote server
    for widget in self.widgets.values():
        # form.widgets.foobar -> foobar
        widget.id = widget.name = widget.field.__name__

.. note::

    Some templates, like ``select_input.pt``, have hard-coded
    name suffixes like ``:list`` to satisfy ZPublisher machinery.
    If you need to get rid of these, you need to override the template.

Making widgets required conditionally
-------------------------------------

If you want to avoid hardwired ``required`` on fields
and toggle then conditionally, you need to supply
a dynamically modified schema field to the
``z3c.form.field.Fields`` instance of the form.

Example::

    class ShippingAddressForm(CheckoutSubform):
        ignoreContext = True
        label = _(u"Shipping address")

        # Distinct fields on same <form> HTML element
        prefix = "shipping"

        def __init__(self, optional, content, request, parentForm):
            """
            @param optional: Whether shipping address should be validated or not.
            """
            subform.EditSubForm.__init__(self, content, request, parentForm)
            self.optional = optional

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

            return fields

Setting widget types
--------------------

By default, widgets for form fields are determined by ``FieldWidget``
adapters (defined in :term:`ZCML`).
You can override adapters per field using field's ``widgetFactory`` property.

Below is an example which creates a custom widget, its ``FieldWidget``
factory, and uses it for one field in one form::

    from zope.component import adapter, getMultiAdapter
    from zope.interface import implementer, implements, implementsOnly

    from z3c.form.interfaces import IFieldWidget
    from z3c.form.widget import FieldWidget

    from plone.formwidget.namedfile.widget import NamedFileWidget, NamedImageWidget

    class HeaderFileWidget(HeaderWidgetMixin, NamedFileWidget):

        # Get download url for HeaderAnimation object's file.
        # Download URL is set externally by edit sub form and
        download_url = None

    class HeaderImageWidget(HeaderWidgetMixin, NamedImageWidget):
        pass

    @implementer(IFieldWidget)
    def HeaderFileFieldWidget(field, request):
        """ Factory for creating HeaderFileWidget which is bound to one field
        """
        return FieldWidget(field, HeaderFileWidget(request))

    class EditHeaderAnimationSubForm(crud.EditSubForm):
        """
        """

        def updateWidgets(self):
            """ Enforce custom widget types which get file/image attachment URL right """
            # Custom widget types are provided by FieldWidget factories
            # before updateWidgets() is called
            self.fields["animation"].widgetFactory = HeaderFileFieldWidget

            crud.EditSubForm.updateWidgets(self)

            # Make edit form aware of correct image download URLs
            self.widgets["animation"].download_url = "http://mymagicalurl.com"


Alternatively, you can use
`plone.directives.form <https://pypi.python.org/pypi/plone.directives.form>`_
to add widget hints to form schema.

Widget save
-----------

After ``form.update()`` if the request was *save* and all data was valid,
``form.applyChanges(data)`` is called.

By default widgets use ``datamanger.AttributeField`` and try to store their
values as a member attribute of the object returned by ``form.getContent()``.

.. TODO:: How do add custom DataManager

Widget value
------------

The widget value, either from form ``POST`` or previous context data,
is available as ``widget.value`` after the ``form.update()`` call.


Adding a CSS class
------------------

Widgets have a method ``addClass()`` to add extra CSS classes.
This is useful if you have
JavaScript/JQuery associated with your special form::

    widget.addClass("myspecialwidgetclass")

Note that these classes are directly applied to ``<input>``, ``<select>``,
etc. itself, and not to the wrapping ``<div>`` element.

Accessing the schema of the field
---------------------------------

A ``zope.schema`` Field is stored as a ``field`` attribute of a widget.
Example::

    textline = form.widgets["myfieldname"].field # zope.schema.TextLine

.. warning::

    ``Widget.field`` is not a ``z3c.form.field.Field`` object.

Getting selection widget vocabulary value as human readable text
----------------------------------------------------------------

Example::

    widget = self.widgets["myselectionlist"]

    token = widget.value[0] # widget.value is list of unicode strings, each is token for the vocabulary

    user_readable = widget.terms.getTermByToken(token).title

Example (page template)

.. code-block:: html

    <td tal:define="widget view/widgets/myselectionlist">
        <span tal:define="token python:widget.value[0]"
              tal:content="python:widget.terms.getTermByToken(token).title" />
    </td>

Setting widget templates
------------------------

You might want to customize the template of a widget to have custom HTML
code for a specific use case.

Setting the template of an individual widget
============================================

First copy the existing page template code of the widget.
For basic widgets you can find the template in the
`z3c.form source tree
<http://svn.zope.org/z3c.form/trunk/src/z3c/form/browser/>`_.

``yourwidget.pt`` (text area widget copied over an example text)

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          tal:omit-tag="">

    <!-- Sections widget custom templates -->

    <textarea
       id="" name="" class="" cols="" rows=""
       tabindex="" disabled="" readonly="" accesskey=""
       tal:attributes="id view/id;
                       name view/name;
                       class view/klass;
                       style view/style;
                       title view/title;
                       lang view/lang;
                       onclick view/onclick;
                       ondblclick view/ondblclick;
                       onmousedown view/onmousedown;
                       onmouseup view/onmouseup;
                       onmouseover view/onmouseover;
                       onmousemove view/onmousemove;
                       onmouseout view/onmouseout;
                       onkeypress view/onkeypress;
                       onkeydown view/onkeydown;
                       onkeyup view/onkeyup;
                       disabled view/disabled;
                       tabindex view/tabindex;
                       onfocus view/onfocus;
                       onblur view/onblur;
                       onchange view/onchange;
                       cols view/cols;
                       rows view/rows;
                       readonly view/readonly;
                       accesskey view/accesskey;
                       onselect view/onselect"
       tal:content="view/value" />
    </html>

Now you can override the template factory in the ``updateWidgets()`` method
of your form class

.. code-block:: python

    from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile as Z3ViewPageTemplateFile
    from z3c.form.interfaces import INPUT_MODE

    class AddForm(DefaultAddForm):

        def updateWidgets(self, prefix=None):
            """ """
            # Call parent to set-up initial widget data
            DefaultAddForm.updateWidgets(self, prefix=prefix)

            # Note we need to be discreet to different form modes (view, edit, hidden)
            if self.fields["sections"].mode == INPUT_MODE:

                # Modify a widget with certain name for our purposes
                widget = self.widgets["sections"]

                # widget.template is a template factory -
                # Widget.render() will associate later this factory with the widget
                widget.template = Z3ViewPageTemplateFile("templates/sections.pt")

You can also interact with your ``form`` class instance from the widget
template

.. code-block:: html

    <!-- Some hidden JSON data for our Javascripts by calling a method on our form class -->
    <span style="display:none" tal:content="view/form/getBlockPlanJSON" />


Setting template for your own widget type
=========================================

You can set the template used by the widget with the
``<z3c:widgetTemplate>`` ZCML directive

.. code-block:: xml

    <z3c:widgetTemplate
        mode="display"
        widget=".interfaces.INamedFileWidget"
        layer="z3c.form.interfaces.IFormLayer"
        template="file_display.pt"
        />

You can also enforce the widget template in the ``render()`` method of the
widget class::

    from zope.component import adapter, getMultiAdapter
    from zope.interface import implementer, implements, implementsOnly
    from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

    from z3c.form.interfaces import IFieldWidget, INPUT_MODE, DISPLAY_MODE, HIDDEN_MODE
    from z3c.form.widget import FieldWidget

    from plone.formwidget.namedfile.widget import NamedFileWidget, NamedImageWidget

    class HeaderFileWidget(NamedFileWidget):
        """ Subclass widget a use a custom template """

        display_template = ViewPageTemplateFile("header_file_display.pt")

        def render(self):
            """See z3c.form.interfaces.IWidget."""

            if self.mode == DISPLAY_MODE:
                # Enforce template and do not query it from the widget template factory
                template = self.display_template

            return NamedFileWidget.render(self)

Widget template example::

    <span id="" class="" i18n:domain="plone.formwidget.namedfile"
          tal:attributes="id view/id;
                          class view/klass;
                          style view/style;
                          title view/title;
                          lang view/lang;
                          onclick view/onclick;
                          ondblclick view/ondblclick;
                          onmousedown view/onmousedown;
                          onmouseup view/onmouseup;
                          onmouseover view/onmouseover;
                          onmousemove view/onmousemove;
                          onmouseout view/onmouseout;
                          onkeypress view/onkeypress;
                          onkeydown view/onkeydown;
                          onkeyup view/onkeyup"
            tal:define="value view/value;
                        exists python:value is not None">
        <span tal:define="fieldname view/field/__name__ | nothing;
                          filename view/filename;
                          filename_encoded view/filename_encoded;"
                tal:condition="python: exists and fieldname">
            <a tal:content="filename"
               tal:attributes="href string:${view/download_url}">Filename</a>
            <span class="discreet"> &mdash; <span tal:define="sizekb view/file_size" tal:replace="sizekb">100</span> KB</span>
        </span>
        <span tal:condition="not:exists" class="discreet" i18n:translate="no_file">
            No file
        </span>
    </span>

Setting widget frame template
-----------------------------

You can change how the frame around each widget is rendered
in the widget rendering loop. This frame has elements like
label, required marker, field description and so on.

For instructions see `plone.app.z3cform README <https://github.com/plone/plone.app.z3cform/>`__

Combined widgets
----------------

You can combine multiple widgets to one with ``z3c.form.browser.multil.MultiWidget`` and ``z3c.form.browser.object.ObjectWidget`` classes.

Example how to create a min max input widget.

Python code to setup the widget:

.. code-block:: python

    import zope.interface
    import zope.schema
    from zope.schema.fieldproperty import FieldProperty

    import z3c.form
    from z3c.form.object import registerFactoryAdapter


    class IMinMax(zope.interface.Interface):
        """ Helper schema for min and max fields """

        min = zope.schema.Float(required=False)

        max = zope.schema.Float(required=False)


    @zope.interface.implementer(IMinMax)
    class MinMax(object):
        """ Store min-max field values """
        min = FieldProperty(IMinMax['min'])
        max = FieldProperty(IMinMax['max'])


    registerFactoryAdapter(IMinMax, MinMax)

    ....

    field = zope.schema.Object(__name__='mixmax', title=label, schema=IMinMax, required=False)

Then we do some widget marking in ``updateWidgets()``::

    def updateWidgets(self):
        """
        """

        super(FilteringGroup, self).updateWidgets()

        # Add min and max CSS class rendering hints
        for widget in self.widgets.values():
            if isinstance(widget, z3c.form.browser.object.ObjectWidget):
                widget.template = Z3ViewPageTemplateFile("templates/minmax.pt")
                widget.addClass("min-max-widget")
                zope.interface.alsoProvides(widget, IFilterWidget)

And then the page template which renders both 0. widget  (min) and 1. widget (max)
on the same line.

.. code-block:: html

    <div class="min-max-widget"
         tal:define="widget0 python:view.subform.widgets.values()[0]; widget1 python:view.subform.widgets.values()[1];">

        <tal:comment>
            <!-- Use label from the first widget -->
        </tal:comment>

        <div class="label">
          <label tal:attributes="for widget0/id">
            <span i18n:translate=""
                tal:content="widget0/label">label</span>
          </label>
        </div>

        <div class="widget-left" tal:define="widget widget0">

            <div tal:content="structure widget/render">
              <input type="text" size="24" value="" />
            </div>


        </div>

        <div class="widget-separator">
        -
        </div>

        <div class="widget-right" tal:define="widget widget1">

            <div class="widget" tal:content="structure widget/render">
              <input type="text" size="24" value="" />
            </div>

        </div>


        <div tal:condition="widget0/error"
             tal:replace="structure widget/error/render">error</div>

        <div class="error" tal:condition="widget1/error"
                 tal:replace="structure widget1/error/render">error</div>


        <div style="clear: both"><!-- --></div>

        <input name="field-empty-marker" type="hidden" value="1"
               tal:attributes="name string:${view/name}-empty-marker" />

    </div>


Buttons
=======

Buttons enable actions in forms. ``AddForm`` and ``EditForm``
base classes come with default buttons (:guilabel:`Save`).

More information in ``z3c.form`` documentation

* http://packages.python.org/z3c.form/button.html

Adding a button to form
-----------------------

The easiest way to add handlers for buttons is to use
a function decorator ``z3c.form.button.buttonAndHandler()``.

The first parameter is the user visible label and
the second one is the ``<input>`` name.

Example::

    from z3c.form import button

    class Form(...):

        @button.buttonAndHandler(_('Add'), name='add')
        def handle_add(self, action):
            data, errors = self.extractData()
            if errors:
                self.status = "Please correct errors"
                return

            self.applyChanges(data)
            self.status = _(u"Item added successfully.")


The default ``z3c.form.form.AddForm`` and ``z3c.form.form.EditForm``
:guilabel:`Add` and :guilabel:`Save` button handler calls are good code
examples.

* https://github.com/zopefoundation/z3c.form/blob/master/src/z3c/form/form.py

If you created a form based on another form, the buttons defined on that other form get lost.
To prevent that, you must explicitly add the buttons of the base class in your form class::

    from z3c.form import button
    from z3c.form.form import EditForm

    class Form(EditForm):

        buttons = EditForm.buttons.copy()

        @button.buttonAndHandler(...)
        def handle_add(...):
            ...

Adding buttons conditionally
----------------------------

The ``buttonAndHandler`` decorator can accept a condition argument.
The condition should be a function that accepts the form as an argument and returns a boolean.
Example, a button that only shows when a condition is met::

    @button.buttonAndHandler(
        u"Delete Event",
        name="handleDelete",
        condition=lambda form: form.okToDelete()
        )
    def handleDelete(self, action):
        """
            Delete this event.
        """

        ...

        self.status = "Event deleted."


Manipulating form buttons programmatically
------------------------------------------

You want to manipulate buttons if you want to hide buttons dynamically,
manipulate labels, etc.

Buttons are stored in ``buttons`` class attribute.

.. warning::

    Button storage is shared between all form instances,
    do not mutate its content. Instead create a copy
    of it if you wish to have form-specific changes.

Reading buttons
^^^^^^^^^^^^^^^

Example::

    self.mobile_form_instance = MobileForm(self.context, self.request)

    for i in self.mobile_form_instance.buttons.items(): print i
    ('apply', <Button 'apply' u'Apply'>)


Removing or hiding buttons
^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is an example how to hide all buttons from a certain form instance.

Example::

    import copy

    def update(self):
            # Hide form buttons

            # Create immutable copy which you can manipulate
            self.mobile_form_instance.buttons = copy.deepcopy(self.mobile_form_instance.buttons)

            # Remove button using dictionary style delete
            for button_id in self.mobile_form_instance.buttons.keys():
                del self.mobile_form_instance.buttons[button_id]


Adding buttons dynamically
^^^^^^^^^^^^^^^^^^^^^^^^^^

In the example below, the ``Buttons`` array is already constructed
dynamically
and we can manipulate it::

    def setActions(self):
        """ Add button to the form based on dynamic conditions. """

        if self.isSaveEnabled():

            but = button.Button("save", title=u"Save")
            self.form.buttons += button.Buttons(but)

            self.form.buttons._data_keys.reverse() # Fix Save button to left

            handler = button.Handler(but, self.form.__class__.handleSave)
            self.form.handlers.addHandler(but, handler)


Subforms
========

Subforms are embedded ``z3c`` forms inside a master form.

Subforms may have their own
buttons or use the controls from the master form.
You need to call ``update()`` manually for subforms.

More info

* http://packages.python.org/z3c.form/subform.html

Adding an action to parent and subform
--------------------------------------

Parent and subform actions must be linked.

Example::

    class CheckoutForm(z3c.form.form.EditForm):


        @button.buttonAndHandler(_('Continue'), name='continue')
        def handleContinue(self, action):
            """ Extract the checkout data to session and redirect to payment Arbitrary checkout screen.

            Note:

            """

            # Following has been copied from z3c.form.form.EditForm
            data, errors = self.extractData()
            if errors:
                self.status = self.formErrorsMessage
                return

            changes = self.applyChanges(data)

            if changes:
                self.status = self.successMessage
            else:
                self.status = self.noChangesMessage


    class CheckoutSubform(subform.EditSubForm):
        """ Add support for continue action. """

            def execute(self):
                """
                Make sure that the form is refreshed when parent
                form Continue is pressed.
                """

                data, errors = self.extractData()
                if errors:
                    self.errors = errors
                    self.status = self.formErrorsMessage
                    return errors

                content = self.getContent()
                z3c.form.form.applyChanges(self, content, data)

                return None

            @button.handler(CheckoutForm.buttons['continue'])
            def handleContinue(self, action):
                """ What happens when the parent form button is pressed """
                self.execute()

Creating subforms at run-time
=============================

Below is an example how to convert existing form instance to
be used as an subform in another form::

    def convertToSubForm(self, form_instance):
        """
        Make existing form object behave like subform object.

        * Do not render <form> frame

        * Do not render actions

        @param form_instance: Constructed z3c.form.form.Form object
        """

        # Create mutable copy which you can manipulate
        form_instance.buttons = copy.deepcopy(form_instance.buttons)

        # Remove subform action buttons using dictionary style delete
        for button_id in form_instance.buttons.keys():
            del form_instance.buttons[button_id]

        if HAS_WRAPPER_FORM:
            # Plone 4 / Plone 3 compatibility
            zope.interface.alsoProvides(form_instance, IWrappedForm)

        # Use subform template - this prevents getting embedded <form>
        # elements inside the master <form>
        import plone.z3cform
        #from zope.pagetemplatefile import ViewPageTemplateFile as Zope3PageTemplateFile
        from zope.app.pagetemplate import ViewPageTemplateFile as Zope3PageTemplateFile
        from zope.app.pagetemplate.viewpagetemplatefile import BoundPageTemplate
        template = Zope3PageTemplateFile('subform.pt', os.path.join(os.path.dirname(plone.z3cform.__file__), "templates"))
        form_instance.template = BoundPageTemplate(template, form_instance)

.. note::

    If possible, try to construct your form class hierarchy so that
    you can use the same class mix-in for normal forms and subforms.

CRUD form
=========

CRUD (Create, read, update, delete) forms manage list of objects.

CRUD form elements:

* Add form creates new objects and renders the form below the table

* Edit sub-form edits existing object and renders one table row

* Edit form lists all objects and allows deleting them (table master)

* CRUD form orchestrates the whole thing and renders add and edit forms

* ``view_schema`` outputs read-only fields in CRUD table

* ``update_schema`` outputs editable fields in CRUD table.
  Usually you want either ``view_schema`` or ``update_schema``.

* ``add_schema`` outputs add form.

.. Note:: the ``context`` attribute of add and edit form is the parent CRUD
    form. The ``context`` attribute of an edit subform is the edit form.

Examples
--------

* https://pypi.python.org/pypi/plone.z3cform#crud-create-read-update-and-delete-forms

Displaying the status message in a non-standard location
========================================================

By default, the status message is rendered inside ``plone.app.z3cform``
``macros.pt`` above the form:

.. code-block:: html

    <metal:define define-macro="titlelessform">

        <tal:status define="status view/status" condition="status">
            <dl class="portalMessage error" tal:condition="view/widgets/errors">
                <dt i18n:domain="plone" i18n:translate="">
                    Error
                </dt>
                <dd tal:content="status" />
            </dl>
            <dl class="portalMessage info" tal:condition="not: view/widgets/errors">
                <dt i18n:domain="plone" i18n:translate="">
                    Info
                </dt>
                <dd tal:content="status" />
            </dl>
        </tal:status>

We can decouple the status message from the form,
without overriding all the templates,
by copying status message variable to another variable and then playing
around with it in our wrapper view template.

Form class::

    class HolidayServiceSearchForm(form.Form):
        """
        """

        @button.buttonAndHandler(_(u"Search"))
        def searchHandler(self, action):
            """ Search form submit handler for product card search.
            """

            data, errors = self.extractData()
            if len(self.search_results) == 0:
                self.status = _(u"No holiday services found.")
            else:
                msgid = _("found_results", default=u"Found ${results} holiday services.", mapping={u"results" : len(self.search_results)})
                self.status = self.context.translate(msgid)

            ...

            # Use non-standard location to display the status
            # for success messages
            if len(self.widgets.errors) == 0:
                self.result_message = self.status
                self.status = None

    class HolidayServiceSearchView(FormWrapper):
        """ HolidayService browser view
        """

        form = HolidayServiceSearchForm

        def result_message(self):
            """ Display result message in non-standard location """

            if len(self.form_instance.widgets.errors) == 0:
                # Do not display form highlight errors here
                return self.form_instance.result_message

... and then we can use a special ``result_message`` view accessor in our
view template code

.. code-block:: xml

    <tal:comment replace="nothing">Form submit anchor</tal:comment>
    <a name="searched" />

    <tal:status define="status view/result_message" condition="python:status != None">
        <dl class="portalMessage info">
            <dt i18n:domain="plone" i18n:translate="">
                Info
            </dt>
            <dd tal:content="status" />
        </dl>
    </tal:status>


Storage format and data managers
================================

By default, ``z3c.form`` reads incoming context values as the object
attributes.
This behavior can be customized using data managers.

You can, for example, use Python dictionaries to read and store form data.

* http://packages.python.org/z3c.form/datamanager.html

Custom content objects
----------------------

The following hack can be used if you have an object which does not conform
your form interface and you want to expose only certain object attribute to
the form to be edited.

Example::

    class ISettings(zope.interface.Interface):

        # This maps to Archetypes field confirmedAR on SitsPatient
        confirmedAR = zope.schema.Choice(
                title=_(u"Confirm adherse reactions"),
                description=_(u"Confirm that all adherse reactions regarding the patient life cycle have been entered here and there will be no longer adherse reaction data"),
                vocabulary=make_zope_schema_vocabulary(ADVERSE_STATUS_VOCABULARY))

    class ARSettingsForm(form.Form):
        """ General settings for all adherse reactions """

        fields = Fields(ISettings)

        def getContent(self):
            """ """

            # Create a temporary object holding the settings values out of the patient

            class TemporarySettingsContext(object):
                zope.interface.implements(ISettings)

            obj = TemporarySettingsContext()

            # Copy values we want to expose to the form from Plone context item to the temporary object
            obj.confirmedAR = self.context.confirmedAR

            return obj

.. note::

    Since ``getContent()`` is also used in ``applyChanges()``, you need to
    override ``applyChanges()`` as well
    to save values correctly to a persistent object.

Custom change applying
----------------------

The default, the behavior of the ``z3c.form`` edit form is to write incoming
data as the attributes of the object returned by ``getContent()``.

You can override this behavior by overriding ``applyChanges()`` method.

Example::

    def applyChanges(self, data):
        """
        Reflect confirmed status to Archetypes schema.

        @param data: Dictionary of cleaned form data, keyed by field
        """


        # This is the context given to the form when the form object was constructed
        patient = self.context

        assert ISitsPatient.providedBy(patient) # safety check

        # Call archetypes field mutator to store the value on the patient object
        patient.setConfirmedAR(data["confirmedAR"])

WYSIWYG widgets
===============

By using `plone.directives.form <https://pypi.python.org/pypi/plone.directives.form>`_
and `plone.app.z3cform <https://pypi.python.org/pypi/plone.app.z3cform>`_ packages you can do::

    from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

    from mfabrik.plonezohointegration import _

    class ISettings(form.Schema):
        """ Define schema for settings of the add-on product """

        form.widget(contact_form_prefix=WysiwygFieldWidget)
        contact_form_prefix = schema.Text(
                title=_(u"Contact form top text"),
                description=_(u"Custom text for the long contact form upper part"),
                required=False,
                default=u"")


More information

* https://pypi.python.org/pypi/plone.directives.form

Wrapped and non-wrapped forms
=============================

A ``z3c.form.form.Form`` object is "wrapped" when it is
rendered inside Plone page frame and having
acquisition chain in intact.

Since ``plone.app.z3cform`` 0.5.0 the behavior goes like this:

* Plone 3 forms are automatically wrapped

* Plone 4 forms are unwrapped

The wrapper is a ``plone.z3cform.interfaces.IWrappedForm``
:doc:`marker interface </develop/addons/components/interfaces>`
on the form object, applied it after the form instance has been constructed.
If this marker interface is not applied,
``plone.z3cform.ZopeTwoFormTemplateFactory``
tries to embed the form into Plone page frame.
If the form is not intended to be rendered as a full page form,
this usually leads to the following exception::

    *** ContentProviderLookupError: plone.htmlhead

The form tries to render the full Plone page.
Rendering this page needs an acquisition
chain set-up for the view and the template. Embedded forms do not have this,
or it would lead to recursion error.

If you are constructing form instances manually and want to render them
without Plone page decoration,
you must make sure that automatic form wrapping does not take place::

    import zope.interface
    from plone.z3cform.interfaces import IWrappedForm

    class SomeView(BrowserView):

        def init(self):
            """ Constructor embedded sub forms """

            # Construct few embedded forms
            self.mobile_form_instance = MobileForm(
                    self.context, self.request)
            zope.interface.alsoProvides(
                    self.mobile_form_instance, IWrappedForm)

            self.publishing_form_instance = PublishingForm(
                    self.context, self.request)
            zope.interface.alsoProvides(
                    self.publishing_form_instance, IWrappedForm)

            self.override_form_instance = getMultiAdapter(
                    (self.context, self.request),
                    IOverrideForm)
            zope.interface.alsoProvides(
                    self.override_form_instance, IWrappedForm)

Embedding z3c.form forms in portlets, viewlets and views
========================================================

By default, when ``plone.app.z3cform`` is installed through
the add-on installer, all forms have full Plone page frame.
If you are rendering forms inside non-full-page objects,
you need to change the default template.

Below is an example how to include a ``z3c.form``-based form in a portlet.

.. note::

    ``plone.app.z3cform`` version 0.5.1 or later is needed,
    as older versions do not support overriding ``form.action``
    property.

You need the following:

* a ``z3c.form`` class

* the viewlet/portlet class

* A form wrapper template which renders the frame around the form.
  The default version renders the whole Plone page frame ---
  you don't want this when the form is embedded,
  otherwise you get infinite recursion
  (plone page having a form having a plone page...)

* Portlet/viewlet template which refers to the form

* ZCML to register all components

Portlet code::

    from plone.z3cform.layout import FormWrapper

    class PortletFormView(FormWrapper):
         """ Form view which renders z3c.forms embedded in a portlet.

         Subclass FormWrapper so that we can use custom frame template. """

         index = ViewPageTemplateFile("formwrapper.pt")

    class Renderer(base.Renderer):
        """ z3c.form portlet renderer.

        Instiate form and wrap it to a special layout template
        which will give the form suitable frame to be used in the portlet.

        We also set a form action attribute, so that
        the browser goes to another page after the form has been submitted
        (we really don't know what kind of page the portlet is displayed
        and is it safe to submit forms there, so we do this to make sure).
        The action page points to a browser:page view where the same
        form is displayed as full-page form, giving the user to better
        user experience to fix validation errors.
        """

        render = ViewPageTemplateFile('zohocrmcontact.pt')

        def __init__(self, context, request, view, manager, data):
            base.Renderer.__init__(self, context, request, view, manager, data)
            self.form_wrapper = self.createForm()

        def createForm(self):
            """ Create a form instance.

            @return: z3c.form wrapped for Plone 3 view
            """

            context = self.context.aq_inner

            returnURL = self.context.absolute_url()

            # Create a compact version of the contact form
            # (not all fields visible)
            form = ZohoContactForm(context, self.request, returnURLHint=returnURL, full=False)

            # Wrap a form in Plone view
            view = PortletFormView(context, self.request)
            view = view.__of__(context) # Make sure acquisition chain is respected
            view.form_instance = form

            return view

        def getContactFormURL(self):
            """ For rendering the form link at the bottom of the portlet.

            @return: URL leading to the full contact form
            """
            return self.form_wrapper.form_instance.action

``formwrapper.pt`` is just a dummy form view template which wraps the form.
This differs from standard form wrapper by *not* rendering Plone
main layout around the form.

.. code-block:: html

    <div class="portlet-form">
       <div tal:replace="structure view/contents" />
    </div>

Then the portlet template itself (``zohoportlet.pt``) renders the portlet.
The form is rendered using:
``<form tal:replace="structure view/form_wrapper" />``.

.. code-block:: html

    <dl class="portlet portletZohoCRMContact"
        i18n:domain="mfabrik.plonezohointegration">

        <dt class="portletHeader">
            <span class="portletTopLeft"></span>
            <span i18n:translate="portlet_title">
               Contact Us
            </span>
            <span class="portletTopRight"></span>
        </dt>

        <dd class="portletItem odd">
            <form tal:replace="structure view/form_wrapper" />
        </dd>

        <dd class="portletFooter">
            <span class="portletBottomLeft"></span>
            <a href=""
               tal:attributes="href view/getContactFormURL"
               i18n:translate="box_more_news_link">
              Longer contact form&hellip;
            </a>
            <span class="portletBottomRight"></span>
        </dd>

    </dl>

.. note::

    Viewlets behave a little differently, since they do some acquisition
    chain mangling when you assign variables to ``self``. Thus you should
    never have ``self.view = view`` or ``self.form = form`` in a viewlet.

Template example for viewlet (don't do ``sel.form_wrapper``)

.. code-block:: html

    <div id="my-viewlet">
        <form tal:replace="structure python:view.createForm()()" />
    </div>

Then the necessary parts of form itself::

    class IZohoContactForm(zope.interface.Interface):
        """ Form field definitions for Zoho contact forms """

        first_name = schema.TextLine(title=_(u"First name"))

        last_name = schema.TextLine(title=_(u"Last name"))

        company = schema.TextLine(title=_(u"Company / organization"), description=_(u"The organization which you represent"))

        email = schema.TextLine(title=_(u"Email address"), description=_(u"Email address we will use to contact you"))

        phone_number = schema.TextLine(title=_(u"Phone number"),
                                       description=_(u"Your phone number in international format. E.g. +44 12 123 1234"),
                                       required=False,
                                       default=u"")


        returnURL = schema.TextLine(title=_(u"Return URL"),
                                    description=_(u"Where the user is taken after the form is successfully submitted"),
                                    required=False,
                                    default=u"")

    class ZohoContactForm(Form):
        """ z3c.form used to handle the new lead submission.

        This form can be rendered

        * standalone (@@zoho-contact-form view)

        * embedded into the portlet

        ..note::

            It is recommended to use a CSS rule
            to hide form descriptions when rendered in the portlet to save
            some screen estate.

        Example CSS::

            .portletZohoCRMContact .formHelp {
               display: none;
            }
        """

        fields = Fields(IZohoContactForm)

        label = _(u"Contact Us")

        description = _(u"If you are interested our services leave your contact information below and our sales representatives will contact you.")

        ignoreContext = True

        def __init__(self, context, request, returnURLHint=None, full=True):
            """

            @param returnURLHint: Should we enforce return URL for this form

            @param full: Show all available fields or just required ones.
            """
            Form.__init__(self, context, request)
            self.all_fields = full

            self.returnURLHint = returnURLHint

        @property
        def action(self):
            """ Rewrite HTTP POST action.

            If the form is rendered embedded on the others pages we
            make sure the form is posted through the same view always,
            instead of making HTTP POST to the page where the form was rendered.
            """
            return self.context.portal_url() + "/@@zoho-contact-form"

        def updateWidgets(self):
            """ Make sure that return URL is not visible to the user.
            """
            Form.updateWidgets(self)

            # Use the return URL suggested by the creator of this form
            # (if not acting standalone)
            self.widgets["returnURL"].mode = z3c.form.interfaces.HIDDEN_MODE
            if self.returnURLHint:
                self.widgets["returnURL"].value = self.returnURLHint

            # Prepare compact version of this formw
            if not self.all_fields:
                # Hide fields which we don't want to bother user with
                self.widgets["phone_number"].mode = z3c.form.interfaces.HIDDEN_MODE


        @button.buttonAndHandler(_('Send contact request'), name='ok')
        def send(self, action):
            """ Form button hander. """

            data, errors = self.extractData()

            if not errors:

                settings = self.getZohoSettings()
                if settings is None:
                    self.status = _(u"Zoho is not configured in Site Setup. Please contact the site administration.")
                    return

                crm = CRM(settings.username, settings.password, settings.apikey)

                # Fill in data going to Zoho CRM
                lead = {
                    "First Name" : data["first_name"],
                    "Last Name" : data["last_name"],
                    "Company" : data["company"],
                    "Email" : data["email"],
                }

                phone = data.get("phone_number", "")
                if phone != "":
                    # Only pass phone number to Zoho if it's set
                    lead["Phone"] = phone

                # Pass in all prefilled lead fields configured in the site setup
                lead.update(self.parseExtraFields(settings.crm_lead_extra_data))

                # Open Zoho API connection
                try:
                    # This will raise ZohoException and nuke the request
                    # if Zoho credentials are wrong
                    crm.open()

                    # Make sure that wfTrigger is true
                    # and Zoho does workflow actions for the new leads
                    # (like informing sales about the availability of the lead)
                    crm.insert_records([lead], {"wfTrigger" : "true"})
                except IOError:
                    # Network down?
                    self.status = _(u"Cannot connect to Zoho servers. Please contact web site administration")
                    return

                ok_message = _(u"Thank you for contacting us. Our sales representatives will come back to you in few days")


                # Check whether this form was submitted from another page
                returnURL = data.get("returnURL", "")

                if returnURL != "" and returnURL is not None:

                    # Go to page where we were sent and
                    # pass the confirmation message as status message (in session)
                    # as we are not in the control of the destination page
                    from Products.statusmessages.interfaces import IStatusMessage
                    messages = IStatusMessage(self.request)
                    messages.addStatusMessage(ok_message, type="info")
                    self.request.response.redirect(returnURL)
                else:
                    # Act standalone
                    self.status = ok_message
            else:
                # errors on the form
                self.status = _(u"Please fill in all the fields")

Further reading
---------------

This example code was taken from the ``mfabrik.plonezohointegration``
product which is in the Plone collective.



Validators
==========

Introduction
------------

There are three kind of validation hooks you can use with z3c.form

* zope.schema field parameter specific

* zope.schema @invariant (validation is model specific)

* zope.schema constraint (validation is model specific)

* z3c.form (validation is bound to the form instance)


Field specific internal validators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you define your field with *zope.schema* you can enable flags for field internal validation.
This include e.g.

* ``required`` is field required on the form or not

* ``min`` and ``max`` for number based fields

Example:

.. code:: python

    class LocalizationOfStenosisForm(form.Schema):

        degreeOfStenosis = schema.Float(
            title=u'Degree of stenosis %',
            required=False,
            min=0.0,
            max=100.0
        )

For available internal validation options, see the field source code in zope.schema package.

Constraint validators
^^^^^^^^^^^^^^^^^^^^^

zope.schema fields take a callable argument ``constraint`` which defines a Python function validating the incoming value.

.. code:: python

    import zope.interface

    def lastNameConstraint(value):
         if value and value == value.lower():
             raise zope.interface.Invalid(u"Name must have at least one capital letter")
         return True

    class IPerson(zope.interface.Interface):

         lastName = zope.schema.TextLine(
             title=u'Last Name',
             description=u'The person's last name.',
             default=u'',
             required=True,
             constraint=lastNameConstraint)

For more information, see ``zope.schema`` documentation.

Invariant validators
^^^^^^^^^^^^^^^^^^^^

Invariants validator do validations between fields.
They are checked after the single field validations are processed.

Example: With invariants it is possible to check if ``start`` date is before ``end`` date:

.. code:: python

    from zope.interface import Invalid
    from zope.interface import invariant

    @provider(IFormFieldProvider)
    class ISomeDates(form.Schema):

        @invariant
        def start_before_end(data):
            if data.start > data.end:
                raise Invalid(_(u'Start must be before end!'))


Form widget validators
^^^^^^^^^^^^^^^^^^^^^^

Example: How to use widget specific validators with ``z3c.form``:

.. code:: python

    from z3c.form import validator
    import zope.component

    class IZohoContactForm(form.Schema):
        """ Form field definitions for Zoho contact forms """

        phone_number = schema.TextLine(
            title=_(u'Phone number'),
            description=_(u'Your phone number in international format. E.g. +44 12 123 1234'),
                        required=False,
                        default=u''
            )

    class PhoneNumberValidator(validator.SimpleFieldValidator):
        """ z3c.form validator class for international phone numbers """

        def validate(self, value):
            """ Validate international phone number on input """
            allowed_characters = '+- () / 0123456789'

            if value is None:
                return

            value = value.strip()

            if not value:
                # Assume empty string = no input
               return

            # The value is not required
            for ch in value:
                if ch not in allowed_characters:
                    raise zope.interface.Invalid(
                        _(u'Phone number contains bad characters')
                    )

            if len(value) < 7:
                raise zope.interface.Invalid(_(u'Phone number is too short'))

    # Set conditions for which fields the validator class applies.
    # This is convinience and in fact does the same as an @adapter decorator
    # on the PhoneNumberValidator class with the needed interfaces/classes
    validator.WidgetValidatorDiscriminators(
        PhoneNumberValidator,
        field=IZohoContactForm['phone_number']
    )

In ``configure.zcml`` add an adapter registration like so:

.. code:: xml

    <adapter factory=".myform.PhoneNumberValidator" />


More info

* original documentation: ``z3c.form`` `validators documentation <http://packages.python.org/z3c.form/validator.html>`_.
* http://docs.plone.org/develop/addons/schema-driven-forms/customising-form-behaviour/validation.html#field-widget-validators
* http://www.jowettenterprises.com/blog/an-image-dimension-validator-for-plone-4


Custom field specific validation in form action handlers and update()
---------------------------------------------------------------------

* http://stackoverflow.com/a/17466776/315168

Customizing and translating error messages
------------------------------------------

If you want to custom error messages on per-field level:

.. code:: python

    from zope.schema._bootstrapinterfaces import RequiredMissing
    RequiredMissingErrorMessage = error.ErrorViewMessage(_(u'Required value is missing.'), error=RequiredMissing, field=IEmailFormSchema['email'])
    zope.component.provideAdapter(RequiredMissingErrorMessage, name='message')

Leave ``field`` parameter out if you want the new error message to apply to all fields.


Read-only and disabled fields
-----------------------------

Read-only fields are not rendered in form edit mode:

.. code:: python

    courseModeAccordion = schema.TextLine(
        title=u"Courses by mode accordion",
        default=u"Automatically from database",
        readonly=True
    )

If the widget mode is ``display`` then it is rendered as in form view mode,
so that the user cannot edit:

.. code:: python

    form.mode(courseModeAccordion="display")
    courseModeAccordion = schema.TextLine(
        title=u"Courses by mode accordion",
        default=u"Automatically from database",
    )

