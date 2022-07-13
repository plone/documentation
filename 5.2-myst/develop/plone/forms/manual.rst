=====================================
 Processing raw HTTP post requests
=====================================

.. admonition:: Description

        How to read incoming HTTP POST values without form frameworks

Introduction
-------------

See :doc:`HTTP request object </develop/plone/serving/http_request_and_response>` for basics.

Here is an example view which checks if a form button has been pressed,
and takes action accordingly.

Register the view in ``configure.zcml``::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        xmlns:plone="http://namespaces.plone.org/plone"
        i18n_domain="example.dexterityforms">

        ...

        <browser:page
              for="Products.CMFCore.interfaces.ISiteRoot"
              name="yourviewname"
              permission="zope2.View"
              class=".yourview.YourViewName"
              template="yourview.pt"
              />

    </configure>


Code for the browser view, name the file ``yourview.py``::

    from Products.CMFCore.interfaces import ISiteRoot
    from Products.Five.browser import BrowserView
    from Products.statusmessages.interfaces import IStatusMessage


    class YourViewName(BrowserView):

        def update(self):

            if "button-name" in self.request.form:

                messages = IStatusMessage(self.request)
                try:
                    # do something
                    messages.add("Button pressed")

                except Exception, e:
                    logger.exception(e)
                    messages.add(u"It did not work out. This exception came when processing the form:" + unicode(e))


Page template code, name the file ``yourview.pt``:

.. code-block:: html

        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
              lang="en"
              metal:use-macro="here/main_template/macros/master"
              i18n:domain="ora.objects"
              tal:define="foo view/update">
        <body>
            <div metal:fill-slot="main">
                <tal:main-macro metal:define-macro="main">

                        <h1 class="documentFirstHeading">
                                Sample form
                        </h1>

                        <p class="documentDescription">
                              Form description
                        </p>


                        <form action="@@yourviewname" method="POST">
                                <button type="submit" name="button-name">
                                        Press me
                                </button>
                        </form>

                </tal:main-macro>
            </div>
        </body>
        </html>



Magical Zope form variables
-------------------------------


Zope provides some magical HTTP POST variable names which are automatically
converted to native Python primitives by ZPublisher.

Quick explanation
=============================

If you have HTML::

        <INPUT TYPE="text" NAME="member.age:int"></P><BR>

Then::

        request.form["member.age"]

will return integer 30 instead of string "30".

.. note::

        This behavior is hard-coded to ZPublisher and cannot be extended or disabled. The recommendation is
        not to use it, but do the conversion of data-types yourself or use a more high-level
        form framework like z3c.form.

More information
=============================

* http://www.zope.org/Members/Zen/howto/FormVariableTypes
