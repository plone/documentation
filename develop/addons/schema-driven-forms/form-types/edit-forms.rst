Edit forms
===========

**Forms that edit something**

Edit forms, unsurprisingly, are used to edit content objects or other
contexts. They derive from *z3c.form.form.EditForm*, which is extended
by *plone.directives.form.EditForm* and
*plone.directives.form.SchemaEditForm*, adding grok support and Plone
semantics. The edit form takes care of firing object-modified events,
and implements default save and cancel actions.

.. note::
    As with add forms, frameworks like Archetypes and Dexterity provide
    their own default edit forms, which should use for editing content
    objects built with those frameworks.

The schema of an edit form is normally a content object schema, which
normally also describes the context of the form view. That is, the edit
form is normally a view on the object that is being edited

That said, we can implement *getContent()* to supply a different
context. This would normally provide the schema interface, but it does
not need to. As with any form, the context need only be adaptable to the
interface(s) associated with its fields.

A simple edit form in a view called *@@edit* that edits a content object
providing *IMyType* would look like this:

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from z3c.form import button, field
    from Products.CMFCore.interfaces import IFolderish

    class IMyType(form.Schema):

        ...

    class MyAddForm(form.SchemaEditForm):
        grok.name('edit')
        grok.require('cmf.ModifyPortalContent')
        grok.context(IMyType)

        schema = IMyType

        label = _(u"Edit my type")
        description = _(u"Make your changes below.")

There is no need to define any actions or implement any methods. The
default save button handler will adapt the context to *IMyType* and then
set each field in the interface with the submitted form values.

A non-schema example would look like:

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from z3c.form import button, field
    from Products.CMFCore.interfaces import IFolderish

    class IMyType(model.Schema):

        ...

    class MyAddForm(form.EditForm):
        grok.name('edit')
        grok.require('cmf.ModifyPortalContent')
        grok.context(IMyType)

        fields = field.Fields(IMyType)

        label = _(u"Edit my type")
        description = _(u"Make your changes below.")

As a slightly ore interesting example, here is one adapted from
*plone.app.registry*’s control panel form base class:

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from zope.component import getUtility

    from z3c.form import button, field
    from Products.CMFCore.interfaces import ISiteRoot

    from plone.registry.interfaces import IRegistry

    class IMySettings(model.Schema):

        ...

    class MyAddForm(form.EditForm):
        grok.name('edit')
        grok.require('zope2.View')
        grok.context(IMyType)

        fields = field.Fields(IMyType)

        label = _(u"Edit my type")
        description = _(u"Make your changes below.")

    class EditSettings(form.SchemaEditForm):
        grok.name('edit-my-settings')
        grok.require('cmf.ManagePortal')
        grok.context(ISiteRoot)

        schema = IMySettings

        label = _(u"Edit settings")

        def getContent(self):
            return getUtility(IRegistry).forInterface(self.schema)


The idea here is that *IMySettings*, which is set as the schema for this
schema edit form, is installed in the registry as a set of records. The
*forInterace()* method on the *IRegistry* utility returns a so-called
records proxy object, which implements the interface, but reads/writes
values from/to the configuration registry. The form view is registered
on the site root, but we override *getContent()* to return the records
proxy. Hence, the initial form values is read from the proxy, and when
the form is successfully submitted, the proxy (and hence the registry)
is automatically updated.
