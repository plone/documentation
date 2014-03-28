Customizing through Order of Precedence
=======================================

How skin layers work and how they can be used in customization.

If you've worked with Plone 2, you'll be familiar with this type of
customization. As we mentioned earlier, the order of layers in a skin
determines which page templates, CSS files and Python scripts are
processed first.

To inspect the order of precedence:

-  Site > Zope Management Interface > portal\_skins
-  click the Properties tab

You should see the layers of the Plone Default skin listed there. Layers
such as 'plone\_templates' come from the main Plone theme but there will
also be layers providing templates from specific add-on products (the
visual editor kupu for instance).

|screenshot of Skin layers in the ZMI|\ When asked to process a specific
template, Plone will work from the top of this list downwards, looking
in each layer in turn to retrieve the template.

At the top is a custom layer; any template placed in here will be found
and used first. So, to create your own version of a Plone template or
CSS file, give it the same name as the Plone version but put it in the
custom layer.

This is the simplest approach, but just ensuring that your version lives
in a layer higher in the order of precedence in a skin than the main
Plone theme layers will be enough to ensure that Plone finds it first
and ignores the original version.

This technique can be used in two ways

using the custom folder
    through the Zope Management Interface, you can add your own versions
    of templates, style sheets etc to the custom folder. This always
    comes at the top, so you can be sure your versions will be found
    first.
adding your own skin layers
    in your own theme product on the file system, create one or two skin
    layers, and ensure that on installation these layers are put just
    below the custom folder in the order or precedence. There's more
    information on how to do this in the next section.

Probably the most comprehensive description of skins, layers and order
or precedence can be found in the first two sections of `Chapter 7 of
The Definitive Guide to
Plone <http://docs.neuroinf.de/PloneBook/ch7.rst>`_ (note that most of
this book refers to Plone 2, but these sections are still relevant for
Plone 3).

.. |screenshot of Skin layers in the ZMI| image:: /old-reference-manuals/plone_3_theming/images/order_of_precedence.gif
