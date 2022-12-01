=====================================
Overriding field defaults dynamically
=====================================

.. admonition :: Description

    PloneFormGen allows you to supply dynamic field defaults by specifying a TALES expression in the Default Expression field of the overrides fieldset (sub-form). This how-to explains what that means, and offers a few examples.

Creating a dynamic field default means to have a form field's initial value change with context. We might, for example, wish to use a member's e-mail address, which would vary with the user. Or, we might be looking up some data via a catalog or RDBMS query, and wish to supply that to the user for correction.

`Template Attribute Language Expression Syntax` (TALES) is a simple notation that allows determination of a value via path (as in path/to/object), string or Python expressions. It is used in `Zope's Template Attribute Language` (TAL), and is ubiquitous in Plone templates. This how-to does not teach you TALES; for that, try the `Zope Page Templates Reference <https://docs.zope.org/zope2/zope2book/AppendixC.html>`_.

.. warning::

    Please note that it's easy to make a mistake when working with TALES fields that will cause an error when you try to display your form. Stay calm! Take note of the error message, and return to the field edit form to fix it. Don't be scared of this kind of error.

Example
=======

Let's say you wish to put the member's id in a string field default. You may do that with the TALES expression::

  member/id

This is a path expression. "id" is found in the "member" object and returned.

There's a gotcha here. What if the form is viewed by an anonymous visitor? They'll receive an error message. We can avoid that with the expression::

  member/id | nothing

The vertical bar (|) marks alternate expression that is used if the left-hand expression is empty or can't be evaluated. Here we're saying to show nothing if member/id can't be evaluated.
Using Python

You may also use Python expressions::

  python: 5 + 3

would supply a value of 8. This is trivial, but what about::

  python: DateTime() + 7

This would supply the current date/time plus seven days.

The name space
==============

Here are the objects available when your expression is evaluated.

TALES context
-------------

here
    The current object. A bit dangerous since this varies depending on context.
folder
    This will be your form folder.
portal
    The portal object.
request
    The REQUEST object. Note that request/form contains form input.
member
    The authenticated user's member data -- if any.
nothing
    Equivalent to Python None.
folder_url
    URL of the form folder.
portal_url
    URL of the site.
modules
    Module importer.

.. note::

    Some of these identifiers are supplied by PloneFormGen and are not available in other contexts.

When you compose your TALES expression, keep in mind that it will need to return different types of data for different types of fields. For simple field defaults, return a string value; for the lines field, return a list or tuple.

Calling a Python script
=======================

You'll be frustrated fast if you try to do anything smart in a single TALES expression. If you need to do something more complicated, add a Python Script to your form folder and call it via TALES. For example, if you added a script with the id getEmail, you could call it with the expression::

    folder/getEmail

Make sure your script returns the value you wish to use as a field default, in the appropriate format.

Setting Many Defaults With One Script

If you need to dynamically set several fields, you may do it with one script. Call the script by specifying it in the Form Setup Script field of the form folder's overrides fieldset.

Set the form fields by putting them in the request/form dictionary. Make sure you don't overwrite anything that's already in the dictionary, as that is probably previously submitted input.

For example, we could create a Python Script (using the Management Interface) in the form folder:

.. code-block:: python

    request = container.REQUEST

    request.form.setdefault('topic', 'value from python script')

If the script id was setTopicDefault, we'd call it by putting::

    here/setTopicDefault

in the `Form Setup Script` field of the form folder's overrides fieldset.
