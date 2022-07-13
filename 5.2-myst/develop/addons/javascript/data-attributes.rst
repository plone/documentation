======================
Custom data attributes
======================

.. topic:: Description

   How to add custom data attributes on the ``<body>`` tag.

Plone adds a few data attributes on the ``<body>`` element.
It's a handy way to pass some information to JavaScript.

This way, the JavaScript code is made more flexible and the values can be changed on the fly through the web.

Add custom data attributes
==========================

There's two ways to add custom data attributes to Plone:

Plone registry
--------------

Add the key and values needed on ``plone.patternoptions`` registry key.

.. note::

   If done like this, all options will be prefixed ``data-pat-``.
   This is the standard way to configure/tweak mockup/patternslib patterns (hence the ``pat-`` prefix)

Adapter
-------

If the ``data-pat-`` prefix does not suite you, or you want complete freedom on what to add,
you can create a ZCA adapter.

The gist of it is:
- register the adapter (in ZCML)
- create the adapter object per se (in python)

ZCML:

.. code-block:: xml

    <adapter
        for="* * *"
        factory="my.package.adapters.JavaScriptSettings"
        provides="Products.CMFPlone.interfaces.IPatternsSettings"
        name="freitag_notifications" />


Python:

.. code-block:: python

    # -*- coding: utf-8 -*-
    from plone import api


    class JavaScriptSettings(object):

        def __init__(self, context, request, field):
            self.request = request
            self.context = context
            self.field = field

        def __call__(self):
            return {
                'data-my-data': 'some-value',
                'data-another-data': 'another-value',
            }

As soon as you reload Plone (due to the ZCML changes) there should be two new data attributes on the ``<body>`` element.
