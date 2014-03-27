======================================
Why learn how to use a new framework?
======================================

.. admonition:: Description

  You may be wondering why should you learn how to use a new forms
  framework if you already know how to use the CMF Form Controller
  Tool (Form Controller).


Why should you use a forms framework at all? You could always write
your own HTML form snippets and use the request dictionary to
retrieve and handle data.

The reason is simple: you'll end up writing a lot of boilerplate
code to collect, validate and build the response. It would be
better if you could just define the fields and metadata of the form
and re-use a set of base classes to do the repetitive work behind
the scenes, i.e., a forms framework.

One of these frameworks is the Form Controller Tool, which is not
bad, but has some disadvantages over formlib:


-  First, the Form Controller spreads the form logic across several
   files so it can be hard to follow it.
-  Second, the From Controller doesn't handle the creation and
   display of the widgets, so you have to create them manually, what
   could become *especially* unmantainable when using choice-type
   fields.
-  Last, the Form Controller doesn't work with Zope 3 schema
   interfaces nor views. Using a Zope 3 schema can help you creating
   add and edit forms.

However, the Form Controller can be useful and even preferable when
you need to implement a complex page flow, or if you want to
customize Plone forms that use it; e.g. the ''Send this page to
someone'' form.

Beginning with Zope 2.9.3 (Plone 2.5) zope.formlib is being
distributed with Zope 2. Five >= 1.4 is required to make use of
this Zope 3 package.

Note: Where do I place the code?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can place the code wherever you want: all in the same file,
each class in a file, in several directories, utilities in a
``utilities.py`` file, etc. Just keep in mind two things:


-  If you write several pieces of code (functions, classes) in
   separate files, remember to import them whenever you use them, as
   you would do in any other Python program.
-  The ZCML statements have to be placed into a file called
   ``configure.zcml`` in the root of your package, or in any other
   file included from it.

Said that, the author reccommends putting all the Python code in a
file named ``browser.py`` in this tutorial to avoid confusion.
