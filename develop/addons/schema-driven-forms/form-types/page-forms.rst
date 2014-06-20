Page forms
===========

**The most basic type of form**

A page form, or simply “form”, is a basic, “standalone” form. The pizza
order example in this manual is a page form.

Page forms derive from *z3c.form.form.Form*, which is extended by
*plone.directives.form.Form* and *plone.directives.form.SchemaForm* as
described in this manual. They will typically have actions, and be
registered as a view for some context. For a completely standalone form,
the site root is often good choice.

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from z3c.form import button, field
    from Products.CMFCore.interfaces import ISiteRoot

    class IMyForm(model.Schema):

        ...

    class MyForm(form.SchemaForm):
        grok.name('my-form')
        grok.require('zope2.View')
        grok.context(ISiteRoot)

        schema = IMyForm
        ignoreContext = True

        label = _(u"My form")
        description = _(u"A sample form.")

        @button.buttonAndHandler(_(u'Ok'))
        def handleOk(self, action):
            data, errors = self.extractData()

            if errors:
                self.status = self.formErrorsMessage
                return

            ...

        @button.buttonAndHandler(_(u"Cancel"))
        def handleCancel(self, action):
            ...

A non-schema version would look like this:

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from z3c.form import button, field
    from Products.CMFCore.interfaces import ISiteRoot

    class IMyForm(model.Schema):

        ...

    class MyForm(form.Form):
        grok.name('my-form')
        grok.require('zope2.View')
        grok.context(ISiteRoot)

        fields = field.Fields(IMyForm)
        ignoreContext = True

        label = _(u"My form")
        description = _(u"A sample form.")

        @button.buttonAndHandler(_(u'Ok'))
        def handleOk(self, action):
            data, errors = self.extractData()

            if errors:
                self.status = self.formErrorsMessage
                return

            ...

        @button.buttonAndHandler(_(u"Cancel"))
        def handleCancel(self, action):
            ...

Many “standalone” page forms will set *ignoreContext = True*. If it is
*False* (the default), the form will read the current value of each
field from the context, by attempting to adapt it to the form schema, as
described in the previous section.

Sometimes, we want to populate the form with initial values that are not
attributes of the context (or an adapter thereof). *z3c.form* allows us
to change the object from which the form’s data is read, by overriding
the *getContent()* method. We can return another object that provides or
is adaptable to the schema interface(s) associated with the form’s
fields, but we can also return a dictionary with keys that match the
names of the fields in the form schema. This is usually easier than
creating an adapter on some arbitrary context (e.g. the site root)
solely for the purpose of pre-populating form values. It also makes it
easy to construct the form’s initial values dynamically.

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from zope import schema

    from z3c.form import button, field
    from Products.CMFCore.interfaces import ISiteRoot

    ...

    class IMyForm(model.Schema):

        foo = schema.TextLine(title=_(u"Foo"))
        bar = schema.TextLine(title=_(u"Bar"))

    class MyForm(form.SchemaForm):
        grok.name('my-form')
        grok.require('zope2.View')
        grok.context(ISiteRoot)

        schema = IMyForm
        ignoreContext = True

        label = _(u"My form")
        description = _(u"A sample form.")

        def getContent(self):
            data = {}
            data['foo'] = u"Foo"
            data['bar'] = u"Bar"
            return data

        @button.buttonAndHandler(_(u'Ok'))
        def handleOk(self, action):
            data, errors = self.extractData()

            if errors:
                self.status = self.formErrorsMessage
                return

            ...

        @button.buttonAndHandler(_(u"Cancel"))
        def handleCancel(self, action):
            ...

Note how the fields in the *data* dictionary returned by *getContent()*
correspond to the fields of the schema interface from which the form’s
fields are built. If we had fields from multiple interfaces (e.g. using
the *additional\_schemata* tuple), we would need to populate keys based
on the fields from all interfaces.

Also note that the values in the dictionary must be valid for the
fields. Here, we have used *TextLine* fields, which expect unicode
string values. We would likely get an error if the value was a byte
string or integer, say.
