Widgets
==========

**Changing the widget used to render a field**

Like most form libraries, *z3c.form* separates a field – a
representation of the value being provided by the form – from its widget
– a UI component that renders the field in the form. In most cases, the
widget is rendered as a simple HTML *<input />* element, although more
complex widgets may use more complex markup.

The simplest widgets in *z3c.form* are field-agnostic. However, we
nearly always work with *field widgets*, which make use of field
attributes (e.g. constraints or default values) and optionally the
current value of the field (in edit forms) during form rendering.

Most of the time, we don’t worry too much about widgets: each of the
standard fields has a default field widget, which is normally
sufficient. If we need to, however, we can override the widget for a
given field with a new one.

Selecting a custom widget using form directives
-----------------------------------------------

*plone.directives.form* provides a convenient way to specify a custom
widget for a field, using the *form.widget()* directive:

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from zope import schema

    from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

    ...

    class IPizzaOrder(model.Schema):

        ...

        form.widget('notes', WysiwygFieldWidget)
        notes = schema.Text(
                title=_(u"Notes"),
                description=_(u"Please include any additional notes for delivery"),
                required=False
        )

The argument can be either a field widget factory, as shown here, or the
full dotted name to one (*plone.app.z3cform.wysiwyg.WysiwygFieldWidget*
in this case).

Updating widget settings
~~~~~~~~~~~~~~~~~~~~~~~~

All widgets expose properties that control how they are rendered. You
can set these properties by passing them to the widget directive:

::

    class IPizzaOrder(model.Schema):

        ...

        form.widget('postcode', size=4)
        postcode = schema.TextLine(
            title=_(u"Postcode"),
            )

.. note::

    Support for specifying widget properties was added in plone.autoform 1.4.

Some of the more useful properties are shown below. These generally
apply to the widget’s *<input />* element.

-  *klass*, a string, can be set to a CSS class.
-  *style*, a string, can be set to a CSS style string
-  *title*, a string, can be used to set the HTML attribute with the
   same name
-  *onclick*, *ondblclick*, etc can be used to associate JavaScript code
   with the corresponding events
-  *disabled* can be set to True to disable input into the field

Other widgets also have attributes that correspond to the HTML elements
they render. For example, the default widget for a *Text* field renders
a *<textarea />* , and has attributes like *rows* and *cols*. For a
*TextLine*, the widget renders an *<input type=“text” />*, which
supports a *size* attribute, among others.

Take a look at *z3c.form*’s *browser/interfaces.py* for a full list of
attributes that are used.


Supplying a widget factory
~~~~~~~~~~~~~~~~~~~~~~~~~~

Later in this manual, we will learn how to set up the *fields* attribute
of a form manually, as is done in “plain” *z3c.form*, instead of using
the *schema* shortcut that is provided by *plone.autoform*. If you are
using this style of configuration (or simply looking at the basic
*z3c.form* documentation), the syntax for setting a widget factory is:

::

    class OrderForm(Form):

        fields = field.Fields(IPizzaOrder)
        fields['notes'].widgetFactory = WysiwygFieldWidget

        ...


Widget reference
----------------

You can find the default widgets in the *browser* package in *z3c.form*.
The *z3c.form* `documentation`_ contains a `listing`_ of all the default
widgets that shows the HTML output of each.

In addition, the Dexterity manual contains :doc:`an overview of common custom widgets </external/plone.app.dexterity/docs/reference/widgets>`.

.. _documentation: https://pythonhosted.org/z3c.form/
.. _listing: https://pythonhosted.org/z3c.form/browser/README.html
