================================================
Adding a JavaScript event handler to a form
================================================

.. admonition :: Description

    Need to make your PFG forms more dynamic? It's easy to add JavaScript.

There are two basic steps to injecting JavaScript into a PFG form:

1. Use the Management Interface to create a text file (object type: file; mimetype: text/plain) either inside the form folder or in a skin folder;

2. Use the form folder's edit / overrides pane, header injection field to tell PFG to inject it into the form.

Injection
=========

Let's look at the second step first. Let's say that your JavaScript file is named form_js. Then just specify::

    here/form_js

in the header injections override field.

JavaScript
==========

There are a couple of considerations here:

1. Since this is a header injection, you'll need to supply the ``SCRIPT`` tags;

2. You'll nearly certainly want to use jQuery to attach the event handler, since jQuery is part of Plone.

.. code-block:: html

    <script>
    jQuery(function($) {
        $('#my-questions :input')
            .click(function() {
                alert('checkbox clicked');
            });
    });
    </script>

This code fragment shows off both, and attaches an alert to every input in the ``mqy-questions`` field.

Note the use of the common jQuery idiom:

.. code-block:: javascript

    jQuery(function($) {
        ...
    });

This accomplishes a couple of things:

1. it sets the code up to run once the page is loaded;

2. it aliases "jQuery" to "$" so that we may use common jQuery shorthand.

An alternative injection
========================

If you want to use a separate JavaScript file that is actual JS (no ``script`` tags) and will be shared among forms,
use the header injection override like this::

    string:<script src="form_scripts.js" />

assuming your script is named ``form_scripts.js``. You may make it a little more sophisticated if you need an absolute URL::

    string:<script src="${here/form_scripts.js/absolute_url}" />

using TALES string interpolation.


