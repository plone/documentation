Add forms
=============

**Forms to create new content objects**

An add form, as its name implies, is used to add content to a container.
Add forms are usually registered as views on a container. For generic
CMF or Plone content, the *IFolderish* interface is normally a good
candidate. The fields in an add form usually represent the fields in the
type that is being added.

.. note::
    If you are using Dexterity or Archetypes, these frameworks have their
    own add form factories, which you probably want to use instead of the
    more basic version described here.

Add forms derive from *z3c.form.form.AddForm*, which is extended by
*plone.directives.form.AddForm* and
*plone.directives.form.SchemaAddForm*, adding grok support and standard
Plone semantics.

To use an add form, you must implement two methods - *create()* and
*add()*. The form then takes care of emitting the proper events and
directing the user to the newly added content item. You can also set the
*immediate\_view* property to the URL of a page to visit after adding the
content item.

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from z3c.form import button, field
    from Products.CMFCore.interfaces import IFolderish

    class IMyType(model.Schema):

        ...

    class MyAddForm(form.SchemaAddForm):
        grok.name('add-my-type')
        grok.require('cmf.AddPortalContent')
        grok.context(IFolderish)

        schema = IMyType

        label = _(u"Add my type of content")
        description = _(u"A sample form.")

        def create(self, data):
            type = MyType()
            type.id = data['id']
            type.title = data['title']
            ...

            return type

        def add(self, object):
            self.context._setObject(object.id, object)

*create()* is called after validation, and is passed a dictionary of
marshalled form fields. It should construct and return the object being
added. That object is then passed to *add()* (after an object-created
event has been fired), which should add it, normally to *self.context*
(the container).

A non-schema version would look like this:

::

    from five import grok
    from plone.supermodel import model
    from plone.directives import form

    from z3c.form import button, field
    from Products.CMFCore.interfaces import IFolderish

    class IMyType(model.Schema):

        ...

    class MyAddForm(form.AddForm):
        grok.name('add-my-type')
        grok.require('cmf.AddPortalContent')
        grok.context(IFolderish)

        fields = field.Fields(IMyType)

        label = _(u"Add my type of content")
        description = _(u"A sample form.")

        def create(self, data):
            type = MyType()
            type.id = data['id']
            type.title = data['title']
            ...

            return type

        def add(self, object):
            self.context._setObject(object.id, object)
