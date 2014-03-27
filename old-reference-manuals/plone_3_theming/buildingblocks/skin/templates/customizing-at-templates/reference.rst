Reference
=========

A reference for customizing Archetypes view templates

View Templates
--------------

View templates are named according to the ``portal_type`` of the class.
To create the name for a view template, follow these steps to create the
name of the template:

#. Change the ``portal_type`` to lowercase.
#. Replace all spaces with underscores (``_``).
#. Append ``_view`` to the end of the name.

Archetypes will automatically locate templates with names created
according to the above steps, and will make use of the macros defined
within the template. View templates can define one or more of the
following macros:

``css``
    A macro for inserting type-specific CSS code, including ``<link>``
    tags pointing to custom CSS files. There is no default macro for
    this within Archetypes; Archetypes uses the existing CSS styles in
    Plone to render AT-based objects.
``header``
    This macro, by default, generates the ``<h1>`` tag containing the
    object's title and the document actions (print, rss, e.g.)
``body``
    The location where the fields and values are displayed by default.
    When rendering fields using the existing widget mechanism, be sure
    to ``tal:define`` the variable ``field`` as the current field; the
    widget templates depend on this variable being set.
``folderlisting``
    This is the folder listing display when viewing the ``view`` tab of
    a folderish object. This is **not** the same as the ``contents``
    view.
``footer``
    By default, this is where Archetypes puts the byline.
``label``
    This template generates field labels.

For any of these macros that is not defined in the custom view template,
Archetypes will use the default behavior in its place, taken from
``base`` or ``widgets/field``.

Widget Templates
----------------

Use custom widget templates by naming them in the schema - insert a
``macro`` parameter into the widget's constructor in the schema, and set
the value to the name of the template. For example,
``macro="my_widget_template"``. Widget templates must have the following
three macros:

-  ``view``
-  ``edit``
-  ``search``

Widget templates have the following local variables available within
TALES expressions:

``accessor``
    The accessor method for the current field. The code
    ``<p tal:content="accessor" />`` will cause the field's value to be
    written within the ``<p>`` tag.
``fieldName``
    The name of the field.
``widget``
    The widget object for the field.
``mode``
    Will always be ``view`` for view templates, but is useful for, say,
    error checking.

