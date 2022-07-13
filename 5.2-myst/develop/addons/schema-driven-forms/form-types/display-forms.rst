Display forms
==============

**Using widgets in display mode**

Both forms and widgets support the concept of a “mode”. The form’s mode
acts as a default for its widgets. The most commonly used mode is
*‘input’*, as indicated by the constant
*z3c.form.interfaces.INPUT\_MODE*, but there is also *‘hidden’*
(*HIDDEN\_MODE*) and *‘display’* (*DISPLAY\_MODE*). The latter is the
form mode for *display forms*.

Display forms derive from *z3c.form.display.DisplayForm*, which is
extended by *plone.directives.dexterity.DisplayForm*. This also mixes in
*plone.autoform.view.WidgetsView*, which provides various conveniences
for dealing with display mode widgets and fieldsets (groups). Note that
this is a “schema form”, i.e. we must set the *schema* property (and
optionally *additional\_schemata*) to a schema deriving from
*form.Schema*.

.. note::
    If you require a grokked alternative that is not a schema form, you can
    derive from *z3c.form.form.DisplayForm* and
    *plone.directives.form.form.GrokkedForm*.

Display forms are not very common outside framework code. In most cases,
it is easier to just create a standard view that renders the context. In
a framework such as Dexterity, display forms are used as the default
views of content items. The main reason to use display forms for
anything bespoke is to use a complex widget that has a display mode
rendering that is difficult to replicate in a custom template.

It is also possible to put some widgets into *input* mode (by setting
the *mode* attribute in the *updateWidgets()* hook), thus placing a
widget into a form that is otherwise not managed by *z3c.form*.

Display forms are used much like standard views. For example:

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import dexterity, form

    ...

    class IMyContent(model.Schema):

        ...

    class MyDisplayForm(dexterity.DisplayForm):
        grok.name('view')
        grok.require('zope2.View')
        grok.context(IMyContent)

There would typically also be a template associated with this class.
This uses standard five.grok view semantics. If the display form above
was in a module called *display.py*, a template may be found in
*display\_templates/mydisplayform.pt*.

The *DisplayForm* base class in *plone.directives.form* makes the
following view attributes available to the template:

-  *view.w* is a dictionary of all the display widgets, keyed by field
   names. This includes widgets from alternative fieldsets.
-  *view.widgets* contains a list of widgets in schema order for the
   default fieldset.
-  *view.groups* contains a list of fieldsets in fieldset order.
-  *view.fieldsets* contains a dict mapping fieldset name to fieldset
-  On a fieldset (group), you can access a *widgets* list to get widgets
   in that fieldset

The *w* dict is the mostly commonly used. To render a widget named *foo*
in the template, we could do:

::

    <span tal:replace="structure view/w/foo/render" />
