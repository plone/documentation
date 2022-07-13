===================
What's in a Request
===================

.. admonition:: Description

    If you're trying to use PloneFormGen overrides, you're going to need to use the request object. Here's a quick trick for exploring it.

As a page is assembled by Zope and Plone following a browser request, information about that request is bundled into a non-persistent, pseudo-global request object. This object is available in the scripts, templates and TALES expressions you may use in creating PloneFormGen overrides. It will contain the form input submitted by the user.

To effectively write more complex overrides, you're going to need to know how to get information out of the request object.

.. note::

    The Request class itself is well-documented in the Zope help system (API section) and in the source at Products.OFSP-2.13.2-py2.X/Products/OFSP/help/Request.py.

Here's a quick recipe that will help you examine the form input contained in the request.

*   Jump into the Management Interface and navigate to your PFG Form Folder.
    Inside it, create a Page Template named showrequest. Now, just before </body>, add::

        <div tal:replace="structure request" />

    Note: when the request object is called, it renders a readable, HTML version of the data. We use "structure" to prevent escaping the HTML.

* Give your template a title and save it away.

* Return to Plone and your form folder. Edit it, and on the form's [overrides] pane, set a Custom Success Action of::

    traverse_to:string:showrequest

Note that this will override any thanks page you've specified. Just clear it when you're done developing.

Now, just fill out your form, and submit it. You should see the contents of the request object. Take a particular look at the form section. That's a dictionary available as request.form when you're composing an override.
