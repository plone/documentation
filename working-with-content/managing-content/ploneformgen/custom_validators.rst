==========================
Creating custom validators
==========================

.. admonition :: Description

    PloneFormGen allows you to create a custom field-input validator by specifying a TALES expression that will be used to validate input when it's submitted.
    This how-to explains what that means, and offers a few examples.

`Template Attribute Language Expression Syntax` (TALES) is a simple notation that allows determination of a value via path (as in path/to/object), string or Python expressions.
It is used in `Zope's Template Attribute Language` (TAL), and is ubiquitous in Plone templates.
This how-to does not teach you TALES; for that, try the `Zope Page Templates Reference <https://docs.zope.org/zope2/zope2book/AppendixC.html>`_.

.. warning::

    Please note that it's easy to make a mistake when working with TALES fields that will cause an error when you try to display your form.
    Take note of the error message, and return to the field edit form to fix it. Don't be scared of this kind of error.

The rules for writing a validator are:

* You should validate against the the variable value, which will contain the field input. Note that -- for simple fields -- value will be a string. But, for a lines field, the contents of value will be a list.

* Return False or zero if you wish to accept the input.

* Return a string containing a user-feedback message if you don't wish to accept the input.

* Don't change the value variable. It won't do you any good.

Example
=======

Let's say that you are operating a restaurant that serves only dishes containing spam.
You may wish to check to make sure that the input to a string or text field contains "spam".
You may do that with by setting a custom validator that reads::

    python: 'spam' not in value and 'Input must include spam.'

The odd logic comes from the need to return `False` for valid input.
Look at a couple of examples of validation in action with literal strings.
Remember, we want to force spam on the user:

.. code-block:: pycon

    >>> 'spam' not in "eggs, eggs, bacon" and 'Input must include spam.'
    'Input must include spam.'

    >>> 'spam' not in "eggs, eggs, bacon and spam" and 'Input must include spam.'
    False

The name space
==============

Here are the objects available when your expression is evaluated.

TALES context
-------------

value
    The field input.
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

Using a Python script
=====================

You'll be quickly frustrated if you try to do anything smart in a single TALES expression.
If you need to do something more complicated, add a Python Script to your form folder and call it via TALES.
For example, if you added a script with the id includesSpam, you could call it with the expression::

    python: folder.includesSpam(value)

Make sure your script returns False if you wish to accept the input, or an error string otherwise.

Here's what a validator script to check for spam might look like::

    if 'spam' in value.lower():
        return False
    else:
        return "'%s' doesn't seem to have spam. Try again." % value

Make sure your script parameter list includes value. (Alternatively, you may check the request.form dictionary,
which will include form input.)

.. note::

    Python scripts are not the same as the Custom Script Adapter.
    The latter is meant to make it easy to add a custom adapter that's processed in the same way as the mail or save-data adapter.
    Python scripts Python code fragments that act like functions.
    They are added via the Management Interface.
