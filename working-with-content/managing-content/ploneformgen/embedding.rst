============================
Embedding PloneFormGen forms
============================

.. admonition:: Description

   PloneFormGen forms may be rendered from other templates, viewlets, and portlets.


*Caveat*: This feature should be considered beta quality.
I've written code that takes advantage of it, and you shouldn't be afraid of it, but take care to test
thoroughly.
There may be certain types of contexts for rendering the form with implications that I haven't taken into consideration.

To insert the form into an arbitrary template, use the 'embedded' browser view::

    <tal:block tal:replace="structure path/to/form/@@embedded"/>

If you are including the form on a page that features another form, you'll probably
need to set a prefix on the 'embedded' view to disambiguate submissions::

    <tal:block tal:define="form nocall:path/to/form/@@embedded;
                       dummy python:form.setPrefix('mypfg')"
           tal:replace="structure form"/>

Or if you are using a view class, you could define a method like::

    from Products.CMFCore.utils import getToolByName
    def render_form(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        form_view = portal.restrictedTraverse('path/to/form/@@embedded')
        form_view.prefix = 'mypfg'
        return form_view()

(Note that restrictedTraverse expects a path relative to the object you are
calling it on, with no initial slash.)  And then in the associated template::

    <tal:block tal:replace="structure view/render_form"/>

By default the embedded form uses the current URL as the form's 'action' parameter.
When the form is rendered upon submission, it will perform validation, run the normal
action adapters, and redirect to the success page as normal.  If you want to submit to
the form's real location or somewhere else, you can override the action by setting the
'action' attribute on the 'embedded' view.

*Known limitation*: Embedded forms have no way of injecting JavaScript or CSS into
the page head like their standalone counterparts.
