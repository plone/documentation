Component Wiring and ZCML
=========================

About components and how they are wired together

|diagram of a component|\ Components are powerful and flexible tools in
Plone 3, but a little more abstract than page templates or Python
scripts. As the diagram on the right attempts to show, they are normally
combinations of Python classes and page templates wired together in Zope
Configuration Language (ZCML) and given a name.

There are two important things to remember about components

Components are compounds of classes, templates, interfaces, permissions etc.
    To track components down you need to look in .zcml files first,
    locate their names, and that will lead you to the classes and
    templates that contribute to them.
Components come into existence when your Zope Instance is started up
    Provided Zope has read the .zcml file, a component will be available
    to use. You can't overwrite existing components, better to create
    your own, reusing some of the parts.

Parts of a Component
--------------------

A component comes into being via a ZCML "directive" (there's an example
of one of these below). The directive will have a series of "attributes"
which will point to the various parts that go into its creation. These
parts have four main functions.

#. To **identify** the component (in the case of a viewlet this will
   usually be done with a "name" attribute).
#. To **compute**\ the information the component is supposed to display
   (this is usually done with a Python class, and pointed to with a
   "class" attribute). For example, in the case of the navigation tree,
   this would be working out which part of the tree should be displayed
   for each page.
#. To **display** the information the component's class has computed
   (this is usually done with a page template).
#. To **restrict** the display of the component. In the case of a
   viewlet, this could be restricting it to display only to certain
   logged-in users (by using the "permission" attribute) or restricting
   it to display only with specific content types (by using the "for"
   attribute).

There's more about this in the :doc:`Components </old-reference-manuals/plone_3_theming/elements/index>`
section.

Zope Configuration Language (ZCML)
----------------------------------

The `Five Tutorial on
WorldCookery.com <http://worldcookery.com/files/ploneconf05-five/step2.html>`_
will walk you through ZCML, and there are plenty of examples in
tutorials on the plone documentation site.

Here's a sample ZCML directive conjuring up the presentation viewlet
(which simply provides a link to a presentation version of a page):

::

    <configure    xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser">  
        <browser:viewlet      
             name="plone.presentation"      
             for="Products.ATContentTypes.interface.IATDocument"      
             manager="plone.app.layout.viewlets.interfaces.IAboveContentBody"      
             class=".presentation.PresentationViewlet"      
             permission="zope2.View"      
        />
    </configure>

There are three things to note:

-  Like any kind of XML, ZCML uses namespaces - watch out for these if
   you're writing your own ZCML file. For theme components, you'll
   mostly use the browser namespace.
-  ZCML attributes often refer to interfaces rather than actual content
   types, classes or components (see the *for* and *manager* attributes
   in the example above). You'll find more about interfaces in a `later
   section <http://plone.org/documentation/manual/theme-reference/buildingblocks/components/componentparts/interfaces>`_.
-  Look at the class attribute and you'll see it begins with a leading
   dot. This means you can find it in the same directory as the ZCML
   file itself. If it isn't within the same directory you'll need to
   give the full name.

You can get detailed information about ZCML directives in the ZCML
Reference section of the Zope 3 API -
`http://apidoc.zope.org/++apidoc++/ <http://apidoc.zope.org/++apidoc++/>`_.
If you want to be very disciplined and tidy, consult the ZCMLStyleGuide
`http://wiki.zope.org/zope3/ZCMLStyleGuide <http://wiki.zope.org/zope3/ZCMLStyleGuide>`_.

 

.. |diagram of a component| image:: /old-reference-manuals/plone_3_theming/images/component.gif
