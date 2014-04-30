Views 
========

**Browser views with and without templates**


Browser views (or just “views”) are the most common form of display
technology in Zope. When you view a web page in Plone, chances are it
was rendered by a view\ :sup:`[1]`\ .

At the most basic level, a view is a component (in fact, a named
multi-adapter) that is looked up during traversal (i.e. when Zope
interpreters a URL) and then called by the Zope publisher to obtain a
string of HTML to return to the browser. That normally involves a page
template, although it is possible to construct the response in code as
well. Sometimes, the view may not return anything. One reason may be
that it results in a redirect. Furthermore, some views are not designed
to be invoked from URL traversal, instead containing utility methods
which are looked up from other views or components.

Views with templates
--------------------

The most common type of view involves a Python class and an associated
page template. The Python class is used to register the view. An
instance of the class is also available in the template, under the name
*view*. This provides a natural home for “display logic” - calculations
or preparation of data intended only for the view.

.. note::
    As a rule of thumb, try to keep the page template free from complex
    expressions. Python code is much easier to debug and test.

Here is an example of a view class which registers a view and provides
some helper methods and attributes. It also prepares some variables for
the view in the *update()* method, which is called just before the view
is rendered. Obviously, we could have omitted these things if they were
not necessary, in which case the Python class would serve only as a
place to hang the view’s registration.

This class could go in any Python module. For generic views,
*browser.py* is a good choice.

.. code-block:: python

    from five import grok
    from Acquisition import aq_inner

    class AsMessage(grok.View):
        """Render a document as a message
        """
        
        grok.context(IDocument)
        grok.require('zope2.View')
        grok.name('as-message')
        
        def update(self):
            context = aq_inner(self.context)
            self.message = IMessage(context)
        
        def truncatedBody(self, maxLength=1000):
            return self.message.body[:maxLength

The automatically associated template is shown below. If the Python
module was *browser.py*, this would be found in a directory
*browser\_templates/asmessage.pt* in the same package. The directory
name is taken from the module name (with *\_templates* appended); the
filename is taken from the class name (in all lowercase, with a *.pt*
extension).

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:metal="http://xml.zope.org/namespaces/metal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="example.conference">

    <body>

    <metal:main fill-slot="main">
        <tal:main-macro metal:define-macro="main">

        <div tal:replace="structure provider:plone.abovecontenttitle" />

        <h1 class="documentFirstHeading">Message view</h1>

        <div tal:replace="structure provider:plone.belowcontenttitle" />
        
        <p class="documentDescription">This is the message view of the content object</p>

        <div tal:replace="structure provider:plone.abovecontentbody" />

        <div>
            <label>Subject:</label> <span tal:content="view/message/subject" />
        </div>
        <div>
            <label>Body:</label> <span tal:content="view/truncatedBody" />
        </div>
            
        <div tal:replace="structure provider:plone.belowcontentbody" />

        </tal:main-macro>
    </metal:main>

    </body>
    </html>

If we now had a content object providing *IDocument* reachable at
*http://example.org/my-document*, we would be able to invoke this view
using a URL like *http://example.org/my-document/@@as-message*. See the
:doc:`Dexterity Developer Manual </external/plone.app.dexterity/docs/index>` for more information about how to register
default and alternative views for content items.

Notes:

-  The class will grokked as a view because it derives from *grok.View*.
   This in turn defines a constructor which saves the context content
   object as *self.context* and the request as *self.request*.
-  We register the view for a specific type of content object using
   *grok.context()*, which we have already seen in the context of
   adapters. Here, we have used the *IDocument* interface from earlier
   in this manual. If there is a module-level context, this can be
   omitted.
-  We give the view a name using *grok.name()*. This corresponds to the
   path segment in the URL. This directive is optional. The default view
   name is the name of the class in all lowercase, e.g. *“asmessage”* in
   this case.
-  We specify a permission required to access the view using
   *grok.require()*. This directive is required. You can pass
   *“zope2.Public”* to indicate that the view does not require any
   permissions at all. Other common permissions include *zope2.View*,
   *cmf.ModifyPortalContent* and *cmf.ManagePortal*. See the :doc:`Dexterity
   Developer Manual </external/plone.app.dexterity/docs/index>` for more information about permissions and
   workflow.
-  We override the *update()* method, which is called by the base class
   before the view is rendered. This is a good place to pre-calculate
   values used in the template and process any request variables (see
   the section on forms below). Since views are transient objects
   instantiated on the fly, we can safely store values on the view
   object itself. Here, we have looked up an *IMessage*adapter (from the
   adapter examples earlier in this manual) and stored it in
   *self.message*. This is available in the template as *view/message*.
-  In the *update()* method, we use the *aq\_inner()* function on
   *self.context* to avoid possible problems with the view being part of
   the acquisition chain of *self.context*. If that didn’t make any
   sense, better not to worry about why this is necessary. Nine times of
   out ten, you won’t have a problem if you just use *self.context*
   directly, but since the tenth time is quite hard to debug, it’s a
   good habit to get into.
-  We have also defined a custom method, which we use in the template
   via a TAL expression.
-  In the template, we use the *master* macro of Plone’s
   *main\_template* to get the standard Plone look-and-feel, and include
   a number of standard viewlet managers (see the section on viewlets
   later in this manual) to provide standard UI elements.
-  We use a number of TAL expressions to render information from the
   context (the *IDocument* object) and the view instance (in
   particular, the *view.message* object we set in the *update()*
   method). See the `ZPT reference`_ for more details on the TAL syntax.

Views without templates
-----------------------

Sometimes, we do not need a template. In this case, we can override the
*render()* method of the *grok.View* base class to return a string,
which is then returned to the browser as the response body.

Below is an example that builds a CSV file of the recipients of the
message representation of the context. By setting appropriate response
headers, this view ensures that the browser will attempt to download
that generated file, rather than display a plain text response.

.. code-block:: python

    from StringIO import StringIO
    import csv

    from five import grok
    from Acquisition import aq_inner

    class MessageRecipients(grok.View):
        """Return a CSV file with message recipients
        """
        
        grok.context(IDocument)
        grok.require('zope2.View')
        grok.name('message-recipients')
        
        def update(self):
            context = aq_inner(self.context)
            self.message = IMessage(context)
        
        def render(self):
        out = StringIO()
        context = aq_inner(self.context)
        writer = csv.writer(out)
        
        # Write header
        writer.writerow(('Email address', 'Subject'))
        
        subject = self.message.subject
        
        # Write body
        for recipient in self.message.recipients:
            writer.writerow((recipient, subject,))
        
        # Prepare response
        
        filename = "Recipients for %s.csv" % context.title
        
        self.request.response.setHeader('Content-Type', 'text/csv')
        self.request.response.setHeader('Content-Disposition', 'attachment; filename="%s"' % filename)
        
        return out.getvalue()

Notes:

-  We use the Python *csv* module to build the output string.
-  We return a string, which represents the response body.
-  We set the *Content-Type* repsonse header to indicate to the browser
   that the return value should be opened as a spreadsheet.
-  We set the *Content-Disposition* response header to indicate that the
   return value should be treated as a separate file rather than opened
   in the browser, and suggest a filename for the download.

Implementing simple forms
-------------------------

Dexterity uses the powerful `z3c.form`_ library to provide forms based
on schemata defined in Python or through-the-web, including validation
and standardised widgets. Sometimes, though, we just want a simple HTML
form and a bit of logic to process request parameters. One common way to
implement this is with a view that defines a form, which submits back to
itself. The form is processed in the *update()* method of the view
class.

The example below shows a simple form which allows users to subscribe to
a content object with an email address. The list of subscribers is
stored in an annotation (as described earlier in this manual).

.. code-block:: python

    from five import grok
    from Acquisition import aq_inner

    from BTrees.OOBTree import OOSet

    from zope.annotation.interfaces import IAnnotatablel, IAnnotations

    class Subscribe(grok.View):
        """Allow users to subscribe to an item
        """
        
        grok.context(IAnnotatable)
        grok.require('zope2.View')
        
        def update(self):
            context = aq_inner(self.context)
            
            # A dictionary of items submitted in a POST request
            form = self.request.form
        
            self.errors = {}

            if 'form.button.Subscribe' in self.request:
                email = self.request.get('email', None)
                if email is None:
                    self.errors['email'] = "Email address is required"

                else:
                    annotations = IAnnotations(context)
                    addresses = annotations.setdefault('example.grok.subscriptions',  OOSet())
                
                    if email in addresses:
                        self.errors['email'] = "Email address already subscribed"
                    else:
                        addresses.add(email)
                        self.request.response.redirect(self.context.absolute_url() + "/view")

Here is the form template. Assuming the view was put in a module
*subscription.py*, the template would be in
*subscription\_templates/subscribe.pt*.

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:metal="http://xml.zope.org/namespaces/metal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="example.conference">

    <body>

    <metal:main fill-slot="main">
        <tal:main-macro metal:define-macro="main">

        <div tal:replace="structure provider:plone.abovecontenttitle" />

        <h1 class="documentFirstHeading">Subscribe</h1>

        <div tal:replace="structure provider:plone.belowcontenttitle" />
        
        <div tal:replace="structure provider:plone.abovecontentbody" />

        <form tal:attributes="action request/URL" method="post">
        
            <div class="field">
                <div class="error"
                    tal:condition="view/errors/email|nothing"
                    tal:content="view/errors/email|nothing" />
                <label for="email">Email address:</label>
                <input type="text" id="email" name="email" />
            </div>
        
        </form>
            
        <div tal:replace="structure provider:plone.belowcontentbody" />

        </tal:main-macro>
    </metal:main>

    </body>
    </html>

To make the example more realistic, we would obviously also need to
write some code to help manage the list of subscribers, allowing users
to un-subscribe and so on, as well as some functionality to actually use
the list. These could potentially be created as other views in the same
module. Their templates would then also go in the
*subscription\_templates* directory.

Notes:

-  We’ve omitted the *grok.name()* directive, so the view name will be
   *@@subscribe*.
-  We register the form for a generic interface so that it can be used
   on any annotatable context.
-  We use a redirect if the form is successfully submitted. The
   *grok.View* base class is smart enough to avoid invoking any
   associated template or overridden *render()* method if a redirect
   takes place.
-  We use *self.request.form* to inspect the submitted form. This
   dictionary contains form values submitted via a POST request. For a
   GET request, use *self.request.get()* to obtain parameters.
-  We use an *OOSet* as an efficient persistent storage of subscription
   email addresses.

Utility views
-------------

Not all views are meant to be rendered. Sometimes, a view provides
utility methods that may be used from other views. Plone has a few such
views in the *plone.app.layout.globals* package:

-  *plone\_portal\_state*, which gives access to site-wide information,
   such as the URL of the navigation root.
-  *plone\_context\_state*, which gives access to context-specific
   information, such as an item’s URL or title.
-  *plone\_tools*, which gives access to common tools, such as
   *portal\_membership* or *portal\_catalog*.

See the *interfaces.py* module in *plone.app.layout.globals* for
details. In a template, we would look up these with a TAL expression
like:

.. code-block:: html

    <div tal:define="context_state nocall:context/@@plone_context_state;
                     viewUrl context_state/view_url;">
        <a tal:attributes="href viewUrl">View URL</a>
    </div>

In code, we could perform the same lookup like so (note that we need a
context object and the request; in a view, we’d normally get these from
*self.context* and *self.request*):

::

    >>> from zope.component import getMultiAdapter
    >>> context_state = getMultiAdapter((context, request,), name=u"plone_context_state")
    >>> viewUrl = context_state.view_url()

A utility view is registered like any other view. If you are using
*grok.View* to register one, you should return an empty string from the
*render()* method. You also should not use *update()*, since it may not
be called for you. Instead, define methods and attributes that can be
accessed independently. Here is an example:

.. code-block:: python

    from five import grok
    from Acquisition import aq_inner

    from plone.memoize import view
    from Products.CMFCore.interfaces import IContentish

    class MessageInfo(grok.View):
        """Utility view to quickly access message aspects of
        an object.
        """
        
        grok.context(IContentish)
        grok.require('zope2.View')
        grok.name('message-info')
        
        def render(self):
            """No-op to keep grok.View happy
            """
            return ''

        @view.memoize
        def recipients(self):
            message = self._message()
            if message is None:
                return None
            return message.recipients
            
        ...

        @view.memoize
        def _message(self):
            """Get the message representation of the context
            """
            context = aq_inner(self.context)
            return IMessage(context, None)

Notes:

-  We have implemented an empty *render()* method to satisfy
   *grok.View*.
-  We have used `plone.memoize`_ to lazily cache variables. The
   *@view.memoize* decorator will cache each value for the duration of
   the request. See *plone.memoize*’s *interfaces.py* for more details.
-  We’re being defensive and returning *None* in the cases where the
   *IMessage* adapter cannot be looked up.

Overriding views
----------------

Recall that views are implemented behind the scenes as named
multi-adapters. One consequence if this is that it is possible to
override a view with a given name by using the more-specific adapter
concept. You can:

-  Register a view with the same name as an existing view, specifying a
   more specific context interface with *grok.context()*
-  Register a view with the same name as an existing view, specifying a
   more specific type of request with *grok.layer()*.

The term “layer” here relates to the concept of a “browser layer”. Upon
traversal, the request may be marked with one or more marker interfaces.
In Plone, this normally happens in one of two ways:

-  A browser layer can be automatically associated with the currently
   active Plone theme. This magic is performed using the `plone.theme`_
   package.
-  One or more browser layers can be activated when a particular product
   is installed in a Plone site. The `plone.browserlayer`_ package
   supports this via the *browserlayer.xml* GenericSetup syntax. See the
   :doc:`Dexterity Developer Manual </external/plone.app.dexterity/docs/index>` for more information about creating a
   GenericSetup profile.

For example, the following class (view implementation and template not
shown) could be used to override a view for a specific layer:

.. code-block:: python

    from five import grok

    ...

    class AsMessage(grok.View):
        """Render a document as a message
        """
        
        grok.context(IDocument)
        grok.layer(IMessageOverrides)
        grok.require('zope2.View')
        grok.name('as-message')
        
        ...

Notes:

-  The *grok.layer()* directive takes an interface as its only argument.
   This should be a layer marker interface. In this case, we have
   assumed that we have an *IMessageOverrides* layer.
-  We’ve used the same name and context as the default implementation of
   the view.
-  We’ve also used the same permission. It is possible to change the
   permission, but in most cases this would just be confusing.
-  We will also sometimes use layers not to override an existing view,
   but to ensure that the view is not available until a package has been
   installed into a Plone site (in the case of a layer registered with
   *browserlayer.xml*) or a given theme is active (in the case of a
   theme-specific layer).

.. note::
    You can use five.grok to override any browser view, not just those
    registered with five.grok. For a simpler way to override templates (but
    not Python logic), you may also want to look into `z3c.jbot`_.



[1] As of Plone 3, that’s not entirely true: an older technology known
as skin layer templates are used for many of the standard pages, but the
principles behind them are the same.

.. _plone.memoize: https://pypi.python.org/pypi/plone.memoize
.. _plone.theme: https://pypi.python.org/pypi/plone.theme
.. _plone.browserlayer: https://pypi.python.org/pypi/plone.browserlayer
.. _z3c.jbot: https://pypi.python.org/pypi/z3c.jbot
.. _z3c.form: https://pypi.python.org/pypi/z3c.form
.. _ZPT reference: http://docs.zope.org/zope2/zope2book/AppendixC.html
