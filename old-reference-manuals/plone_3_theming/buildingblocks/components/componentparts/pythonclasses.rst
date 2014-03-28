Python Classes
==============

You'll have noticed that Python classes are often part of the wiring of
Components, and you will find that you can't really avoid understanding
a little bit about them, particularly if you want to make your own
viewlets.

Having to deal with something as advanced as Python classes can be
daunting for the non-developer. The good news is that using Python
classes will be more a case of copying and changing little bits of code
than writing anything from scratch.

What's a Class?
---------------

It's best to think of a class as a discrete piece of code containing a
collection of methods ('actions' of some sort) and attributes
('variables' which can hold a value).

In the case of components, the main purpose of a class is to compute the
pieces of information a component needs to display. The class for the
logo viewlet is a good example. You can find it in:

-  [your egg location]/plone/app/layout/viewlets/common.py - look for
   LogoViewlet

After a bit of preparatory work, the LogoViewlet class first finds out
the name of the image that is to be used for the logo (and is defined in
the base\_properties property sheet):

::

    logoName = portal.restrictedTraverse('base_properties').logoName

Then it works out the logo's vital statistics, size, alt text etc and
turns this into an HTML anchor tag:

::

    self.logo_tag = portal.restrictedTraverse(logoName).tag()

Finally, just in case you might need it, it looks up the title of the
site:

::

    self.portal_title = self.portal_state.portal_title()

In the page template associated with this viewlet you can get hold of
this information (self.logo\_tag, self.portal\_title) using the variable
"view":

::

    <img src="logo.jpg" alt=""
             tal:replace="structure view/logo_tag" />

Do I have to use Classes?
-------------------------

Viewlets tend to be wired up with a Python class which points to a template.
So, even though you might only want to create a new template,
you'll find that you have to write a class to point to your new
template. 
The :doc:`Elements </old-reference-manuals/plone_3_theming/elements/index>`
section of this manual should help you by giving you a snippet of code
for each element to copy and paste into your own product.

Here's an example. The standard logo template doesn't actually make use
of view/portal\_title. So if you wanted to incorporate this into your
logo in some way, then you would need to write your own template and
then also your own class:

::

    from plone.app.layout.viewlets.common import LogoViewlet
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

    class [your class name](LogoViewlet):
        render = ViewPageTemplateFile('[your template name]')

-  First, pull in ("import") all the bits and pieces with which to build
   your class using from ….. import …… .

-  Next, define your class. The important thing here is to base it on a
   pre-existing class so that you don't have to start from scratch. Put
   the name of the pre-existing class in brackets after your class name
   (make sure that you've imported it first). Don't forget the colon!
-  Finally, rewrite any of the methods or attributes you need. Here,
   we've just rewritten the *render* method to display our own template.

Note: indenting is very important in Python code, the convention is to
use four spaces (rather than a tab). If you are having problems, double
check the indentation first.

-  `http://wiki.python.org/moin/HowToEditPythonCode <http://wiki.python.org/moin/HowToEditPythonCode>`_

If you're feeling brave or want to know more, a straightforward
introduction is here:
`<http://www.diveintopython.org/object_oriented_framework/defining_classes.html>`_

-  `Dive Into Python - Defining
   Classes <http://www.diveintopython.org/object_oriented_framework/defining_classes.html>`_


