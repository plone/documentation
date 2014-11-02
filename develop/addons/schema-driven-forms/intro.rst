Introduction
=============

**What is z3c.form all about?**

HTML forms are the cornerstone of modern web applications. When you interact with Plone, you use forms all the time - to search the content store, to edit content items, to fill in your personal details. You will notice that most of these forms use the same layout and conventions, and that they all rely on common patterns such as server-side validation and different buttons resulting in different actions.

Over the years, several approaches have evolved to deal with forms. A few of the most important ones are:


-  Creating a simple view with an HTML form that submits to itself (or
   another view), where the request is validated and processed in custom
   Python code. This is very flexible and requires little learning, but
   can also be fairly cumbersome, and it is harder to maintain a common
   look and feel and behaviour across all forms. See the :doc:`Views and viewlets </develop/plone/views/index>` for some hints on one way to build such views.
-  Using the *CMFFormController* library. This relies on special page
   objects known as “controller page templates” that submit to
   “controller python scripts”. The form controller takes care of the
   flow between forms and actions, and can invoke validator scripts.
   This only superficially addresses the creation of standard form
   layouts and widgets, however. It is largely deprecated, although
   Plone still uses it internally in places.
-  Using *zope.formlib*. This is a library which ships with Zope. It is
   based on the principle that a *schema interface* defines a number of
   form fields, constraints and so on. Special views are then used to
   render these using a standard set of widgets. Formlib takes care of
   page flow, validation and the invocation of *actions* - methods that
   correspond to buttons on the form. Formlib is used for Plone’s
   control panels and portlets. However, it can be cumbersome to use,
   especially when it comes to creating custom widgets or more dynamic
   forms.
-  Using *`z3c.form`_*. This is a newer library, inspired by formlib,
   but more flexible and modern.

This manual will show you how to use *z3c.form* in a Plone context.
It will use tools and patterns that are consistent with those used for Dexterity development, as shown in the :doc:`Dexterity developer manual </external/plone.app.dexterity/docs/index>`, but the information contained herein is not Dexterity specific. Note that Dexterity’s standard add and edit forms are all based on *z3c.form*.


Tools
-----

As a library, *z3c.form* has spawned a number of add-on modules, ranging
from new field types and widgets, to extensions that add functionality
to the forms built using the framework. We will refer to a number of
packages in this tutorial. The most important packages are:

-  `z3c.form`_ itself, the basic form library. This defines the standard
   form view base classes, as well the default widgets. The *z3c.form*
   `documentation <http://docs.zope.org/z3c.form>`_ applies to the forms created here, but some of the
   packages below simplify or enhance the integration experience.
-  `plone.z3cform`_ makes *z3c.form* usable in Zope 2. It also adds a
   number of features useful in Zope 2 applications, notably a mechanism
   to extend or modify the fields in forms on the fly.
-  `plone.app.z3cform`_ configures *z3c.form* to use Plone-looking
   templates by default, and adds few services, such as a widget to use
   Plone’s visual editor and “inline” on-the-fly validation of forms.
   This package must be installed for *z3c.form*-based forms to work in
   Plone.
-  `plone.autoform`_ improves *z3c.form*’s ability to create a form from
   a schema interface. By using the base classes in this package,
   schemata can be more self-describing, for example specifying a custom
   widget, or specifying relative field ordering. We will use
   *plone.autoform* in this tutorial to simplify form setup.
-  `plone.directives.form`_ provides tools for registering forms using
   convention-over-configuration instead of ZCML. We
   will use *plone.directives.form* to configure our forms in this
   manual.

A note about versions
---------------------

This manual is targeted at Plone 4.1 and above (Zope 2.13).

.. _plone.z3cform: https://pypi.python.org/pypi/plone.z3cform
.. _plone.app.z3cform: https://pypi.python.org/pypi/plone.app.z3cform
.. _plone.autoform: https://pypi.python.org/pypi/plone.autoform
.. _plone.directives.form: https://pypi.python.org/pypi/plone.directives.form
.. _z3c.form: https://pypi.python.org/pypi/z3c.form

