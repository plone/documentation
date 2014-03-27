Move viewlet
========================

A cheat sheet of what you need to do to move viewlets in your page
layout, or remove or hide them from your page.

You'll find detailed information and a tutorial on how to move viewlets
here:

-  `http://plone.org/documentation/tutorial/customizing-main-template-viewlets/reordering-and-hiding-viewlets <http://plone.org/documentation/manual/tutorial/customizing-main-template-viewlets/reordering-and-hiding-viewlets>`_

Quick Cheat Sheet of the Basics
-------------------------------

Through the Web
~~~~~~~~~~~~~~~

-  Add @@manage-viewlets to your site URL.
-  If you want to move viewlets that only appear on a page, be sure to
   append @@manage-viewlets to the URL of the page.
-  You will find that you can move, hide or remove viewlets with this
   method, but that you cannot move them from one viewlet manager to
   another.

In your own product
~~~~~~~~~~~~~~~~~~~

Moving or removing viewlets is part of your site configuration:

-  Add or edit [your theme package]/profiles/default/viewlets.xml

You'll find general information about the site configuration in the
`Configuration <http://plone.org/documentation/manual/theme-reference/elements/buildingblocks/configuration>`_\ section
of this manual. It's worth reading this through before you launch in
here, as configuring viewlets and viewlet managers can be a bit tricky.
It will tell you

-  how you can get the Generic Setup tool to write out the configuration
   for you
-  why things might not be working as you expect

`GloWorm <http://plone.org/products/gloworm>`_ is a useful tool here
too. It will help you move the viewlets around through the Plone user
interface and inspect the resulting configuration.

Removing a viewlet from a viewlet manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can't do anything more than hide your viewlet in the viewlet manager

::

    <object>
        <hidden manager="[Viewlet Manager Name]" skinname="[your skin name]">
            <viewlet name="[Viewlet Name]" />
        </hidden>
    </object>

Note that you can do this process through the web and then get the
Generic Setup tool to write out the configuration for you to transfer
into your own theme package.

Moving a viewlet within a viewlet manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    <object>
        <order manager="[Viewlet Manager Name]" skinname="[your skin name]">
    Specify all the viewlets you want to see in this viewlet
    in the order you want them with this directive:
            <viewlet name="[Viewlet Name]">
        </order>
    </object>

Note that you can do this process through the web and then get the
Generic Setup tool to write out the configuration for you to transfer
into your own theme package.

Moving a viewlet from one viewlet manager to another
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are basing your theme on the Plone Default theme, then you'll
find that reassigning a Plone Default viewlet is a two step process

-  hide it in its current viewlet manager
-  add it and give it a position in a different viewlet manager

::

    <object>
    Hide it from the current viewlet manager
        <hidden manager="[current Viewlet Manager Name]" skinname="[your skin name]">
            <viewlet name="[Viewlet Name]" />
        </hidden>
    Add it to a different viewlet manager
        <order manager="[a different Viewlet Manager]" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[Viewlet Name]"
                     insert-before="[Name of Viewlet Below]" />
        </order>
    OR Add it to your own viewlet manager
        <order manager="[Your Viewlet Manager]" skinname="[your skin name]">
            <viewlet name="[Viewlet Name]"/>
        </order>
    </object>

-  you can also use 'insert-after="[Name of Viewlet Above]"' or use an
   asterisk to place the viewlet at the top or bottom of the manager
   (e.g 'insert-after'=\*).
-  based-on="Plone Default" means that it will take the Plone Default
   ordering and then apply the insert-after and insert-before
   adjustments you've specified.

Registering a viewlet / non-std. theme
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If youare basing your theme on the Plone Default theme, then you'll
find that reassigning a Plone Default viewlet is a two step process
\* hide it in its current viewlet manager
\* add it and give it a position in a different viewlet manager
If your theme is not based on Plone Default you need `to register the
viewlet in your
theme <http://collective-docs.readthedocs.org/en/latest/views/viewlets.html#creating-a-viewlet-manager-zcml-way>`_.
