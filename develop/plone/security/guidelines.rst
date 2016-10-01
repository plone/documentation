======================
Programming Guidelines
======================


Use of structure in page templates
----------------------------------

Do not use the `structure` page template feature with unfiltered input.
This can lead to XSS attacks.

Example potentially dangerous page template snippet:

.. code-block:: xml

    <figcaption tal:content="structure context/image_caption" />

The reason this snippet is dangerous is because `image_caption` is not filtered input/output.


Manual filtering
~~~~~~~~~~~~~~~~

If you need to use structure with unfiltered input, you can manually run Plone's output filtering engine on arbitrary html.

Example:

.. code-block:: python

    from plone import api

    def get_safe_html(context):
        transforms = api.portal.get_tool('portal_transforms')
        data = transforms.convertTo('text/x-html-safe', context.image_caption, mimetype='text/html',
                                    context=context)
        return data.getData()


Persistent traversable object methods
-------------------------------------

Any persistent objects that can be traversed to (by accessing them via URL), needs to have careful consideration when writing methods.

A legacy artifact of Zope2 is that it automatically published methods with doc strings.
If you forgot to specify permissions on a persistent traversable object, and it does writes on the database or discloses information it should not, you could be causing a security issue.


Do not:

.. code-block:: python

    class MyContent(DexterityItem):
        def foobar(self):
            """My doc string. This method is public!"""
            self.x = 'foobar'  # mutation

Do this:

.. code-block:: python

    class MyContent(DexterityItem):
        def foobar(self):
            # My doc string.
            self.x = 'foobar'  # mutation

Or this:

.. code-block:: python

    class MyContent(DexterityItem):
        security = ClassSecurityInfo()
        security.declarePrivate('foobar')
        def foobar(self):
            """My doc string. This method is public!"""
            self.x = 'foobar'  # mutation


Untrusted JavaScript Input
--------------------------

This isn't a Plone specific guideline, this is for ALL JavaScript people write anywhere.

If you build HTML from user input, make sure to always escape the input.

A common pitfall in jQuery will look like this:

.. code-block:: javascript

    var value = '<script>alert("hi")</script>';
    $('body').append($(value));


By default, jQuery is not safe. To do the previous example in jQuery, you could:

.. code-block:: javascript

    var $el = $('<div/>');
    var value = '<script>alert("hi")</script>';
    $el.text(value);
    $('body').append($el);


In underscorejs templates make sure to use:

.. code-block:: javascript

    <%- … %>

Do not(underscorejs):

.. code-block:: javascript

    <%= … %>


Other considerations
~~~~~~~~~~~~~~~~~~~~

Many modern frameworks are safe by default.
For example, it is difficult to render untrusted, raw HTML in the ReactJS framework.
