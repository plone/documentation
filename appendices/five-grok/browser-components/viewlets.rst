Viewlets
===========

**Dynamic snippets with viewlets**

Viewlets, as their name suggests, are “little views” - snippets of HTML
that are rendered at defined location in a view. Behind the scenes, a
viewlet is a named browser component that is registered for a context
and a request (like a view), as well as for a view and a viewlet
manager.

In a page template, you may see something this:

.. code-block:: html

    <div tal:replace="structure provider:plone.belowtitle" />

This tells Zope to look up and render the *content provider* with the
name *plone.belowtitle*. The most common type of content provider is a
*viewlet manager*. When the viewlet manager is rendered, it will look up
any viewlets which are registered for that viewlet manager, and which
are applicable to the current context (content object), request (browser
layer), and view (the same provider expression can be used in multiple
templates, but sometimes we only want a viewlet to show up for a
particular view). These are then rendered into the page template.

Plone comes with a number of standard viewlet managers, covering various
areas of the page which you may want to plug viewlets into. The standard
viewlet managers are all defined in the package
*plone.app.layout.viewlets*. In its *configure.zcml*, you will see a
number of sections like this:

.. code-block:: xml

        <browser:viewletManager
            name="plone.htmlhead"
            provides=".interfaces.IHtmlHead"
            permission="zope2.View"
            class="plone.app.viewletmanager.manager.BaseOrderedViewletManager"
            />

This shows that we have a viewlet manager with the name
*plone.htmlhead*, identifiable via the interface
*plone.app.layout.viewlets.interfaces.IHtmlHead*.

Another way to find viewlet managers is to use the *@@manage-viewlets*
view: simply append */@@manage-viewlets* to the end of the URL of a
content item in Plone, and you will see the viewlet managers and
viewlets that make up various parts of the page. You can find the
various viewlet manager names and interfaces on this screen as well.

Registering a viewlet
---------------------

With five.grok, we can register a viewlet using the *grok.Viewlet* base
class:

.. code-block:: python

    from five import grok
    from plone.app.layout.viewlets.interfaces import IAboveContent

    ...

    class MessageViewlet(grok.Viewlet):
        """Display the message subject
        """

        grok.name('example.messaging.MessageViewlet")
        grok.context(IDocument)
        grok.require('zope2.View')
        grok.viewletmanager(IAboveContent)

        def update(self):
            self.message = IMessage(self.context)

Notes:

-  We use *grok.name()* to give the viewlet a name. If this were
   omitted, the name would be taken from the class name, in all
   lowercase. The name is primarily useful for overriding the viewlet
   for a more specific context or layer later, but it must be unique, so
   it is a good idea to use a dotted name based on the package name.
-  We use *grok.context()* to limit this viewlet to a particular content
   type, described by the *IDocument* interface from earlier examples
   (not shown). We could omit this, in which case the viewlet would be
   shown for any type of context where the viewlet manager is rendered.
-  As with a view, we have to specify a permission required to see the
   viewlet, using *grok.require()*. If the user does not have the
   required permission, the viewlet will simply be omitted.
-  We override the *update()* method to prepare some data for the
   template, much like we did for the view in the previous section. We
   could also define additional properties or methods on the viewlet
   class.
-  We specify the viewlet manager using *grok.viewletmanager()*.
-  As with a view, the context is available as *self.context* and the
   request as *self.request*. In addition, there is *self.view*, the
   current view, and *self.viewletmanager*, the viewlet manager.

To render the viewlet, we could either override the *render()* method
and return a string, or use a page template. A page template will be
automatically associated using the rules that apply views. Thus, if the
viewlet was defined in *browser.py*, the template would be found in
*browser\_templates/messageviewlet.pt*. In the template, the variable
*view* refers to the current view, and the variable *viewlet* refers to
an instance of the viewlet class. For example:

.. code-block:: html

    <div class="messageViewlet">
      <span>The message subject for this document would be </span>
      <span tal:content="viewlet/message/subject" />
    </div>

Notes:

-  Viewlet templates tend to be short, and never include the full *<html
   />* wrapper.
-  For the page template to be valid, there must be exactly one root
   node, a *<div />* in this case.
-  It is a good idea to apply a CSS class to the outer element of the
   viewlet, so that it can be styled easily.
-  The *viewlet*variable refers to an instance of the viewlet class.
   There is also *view*, the current view; *context*, the context
   content object; and *request*, the current request.

Viewlet ordering
----------------

By default, the order of viewlets in a viewlet manager is arbitrary.
Plone’s viewlet managers, however, add ordering support, as well as the
ability to temporarily hide particular viewlets. You can control the
order through-the-web using the *@@manage-viewlets* view described
above.

A more robust and repeatable option, however, is to configure ordering
at product installation time using Generic Setup, by adding a
*viewlets.xml* to your *profiles/default* directory.

For example, to ensure that our new viewlet appeared first in the
*plone.abovecontent* manager, we could use a *viewlets.xml* file like
this:

.. code-block:: xml

    <?xml version="1.0"?>
    <object>
      <order manager="plone.abovecontent" skinname="*">
        <viewlet name="example.messaging.MessageViewlet" insert-before="*"/>
      </order>

    </object>

See `this tutorial <https://plone.org/documentation/kb/customizing-main-template-viewlets>`_ for more detail about the syntax of this file.

Overriding an existing viewlet
------------------------------

Just like a view, a viewlet with a particular name can be overridden
based on the type of context, using the *grok.context()* directive, or a
browser layer, using the *grok.layer()* directive.

Here is an example using a more-specific context override:

.. code-block:: python

    from five import grok
    from plone.app.layout.interfaces import IAboveContent

    ...

    class SilentMessageViewlet(grok.Viewlet):
        """Don't get in the way of important documents
        """

        grok.name('example.messaging.MessageViewlet")
        grok.context(IImportantDocument)
        grok.require('zope2.View')
        grok.viewletmanager(IAboveContent)

        def update(self):
            self.message = IMessage(self.context)

        def render(self):
            return ''

Notes:

-  The viewlet name and manager are the same as those used in the
   original registration, allowing this viewlet to act as an override
   for the one defined previously.
-  Here, the viewlet is registered for a more-specific context, using
   *grok.context()*.
-  In this case, there is no page template. Instead, we return an empty
   string from *render()*. This has the effect of hiding the viewlet for
   documents providing *IImpotantDocument*(from the examples earlier in
   the manual, this is a marker interface that can be applied to
   *IDocument* instances). We could of course have used a template as
   well, as shown above.

Restricting a viewlet to the canonical view
-------------------------------------------

A viewlet may be registered to appear only when a particular type of
view is being rendered, using the *grok.view()* directive. You can pass
either the view class itself, or an interface it implements, to this
directive. One common example of this is the *IViewView* marker
interface, which Plone applies to the canonical view (i.e. the one you
get when clicking the *View* tab) of a content object.

Here is a refined version of our original viewlet, applied to the
canonical view only (template not shown again):

.. code-block:: html

    <div tal:replace="structure provider:example.messaging.MessageArea" />

.. note::
    this will cause an error if the viewlet manager is not
    available for the current context and view.

We need to register some viewlets before this would actually display
anything. Previously, we used an interface provided by the viewlet
manager to register a viewlet for that manager. We could define such an
interface and use *grok.implements()* on the viewlet manager class to
associate it with the manager class. However, we can also use the
viewlet manager class directly:

.. code-block:: python

    class DummyViewlet(grok.Viewlet):
        grok.name('example.messaging.DummyViewlet')
        grok.require('zope2.View')
        grok.viewletmanager(MessageAreaViewletManager)

        def render(self):
            return "<p>Dummy</p>"

It would of course be better to use a page template, but this would be
enough for a quick test.
