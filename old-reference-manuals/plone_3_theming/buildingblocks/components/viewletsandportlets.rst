Viewlets, Portlets and Other Components
=======================================

Types of component.

Viewlet
=======

This is a new feature in Plone 3 and is used to provide aspects of the
page furniture - those elements of the page which generally don't change
throughout the site. These are organized by another type of component -
a Viewlet Manager.

For more information you can look at

-  `Anatomy of a
   Viewlet <http://plone.org/documentation/manual/theme-reference/elements/viewlet/anatomy>`_
   section in this reference manual
-  `http://plone.org/documentation/tutorial/customizing-main-template-viewlets <http://plone.org/documentation/tutorial/customizing-main-template-viewlets>`_
-  `http://plone.org/documentation/tutorial/customization-for-developers/viewlets/ <http://plone.org/documentation/tutorial/customization-for-developers/viewlets/>`_

Portlet
-------

Portlets in Plone are boxes of information, usually in the right or left
column of a page, containing aggregated content or additional
information, which may or may not be directly relevant to the content
item being displayed. Behind the scenes these used to be constructed
from ordinary page templates, but now, in Plone 3, they are wired
together as components and are managed by another component - a Portlet
Manager.

For more information take a look at:

-  The `Anatomy of a
   Portlet <http://plone.org/documentation/manual/theme-reference/elements/portlet/anatomy>`_
   section of this manual
-  `http://plone.org/documentation/how-to/override-the-portlets-in-plone-3.0/ <http://plone.org/documentation/how-to/override-the-portlets-in-plone-3.0/>`_
-  `http://plone.org/documentation/tutorial/customization-for-developers/portlet-renderers/ <http://plone.org/documentation/tutorial/customization-for-developers/portlet-renderers/>`_
   (for a much more technical explanation)
-  `http://plone.org/documentation/how-to/adding-portlet-managers <http://plone.org/documentation/how-to/adding-portlet-managers>`_

View (Browser View)
-------------------

We gave one definition of the term "view" above in the `skin
section <http://plone.org/documentation/manual/theme-reference/buildingblocks/skin>`_.
However, behind the scenes, in the context of components, View has a
more technical meaning. It refers to a component which is usually made
up of a Python class or a template or both and, put simply, processes
the data from a content item before it reaches the page. There's a
`technical
explanation <http://plone.org/plone-developer-reference/patterns/views/>`_
in the Plone Developer Manual.

You'll sometimes see it referred to as BrowserView or <browser:page> and
in templates you'll see a browser view's name prefaced by @@. We look at
browser views again in the section on `putting a page
together <http://plone.org/documentation/manual/theme-reference/page>`_.

    Note that the term browser and the browser namespace are used to
    demarcate presentational components – that is, those bits of code
    which go to make up elements which will find their way to a web
    browser at some point.

Resource (Browser Resource) & ResourceDirectory
-----------------------------------------------

Although we've indicated that the skin and layers are the usual home of
page templates, images and style sheets, it is also possible to turn
them into components by registering them in ZCML. In this case you'll
see them referred to like this ++resource++[resource name]. The same can
be done for a directory containing templates and style sheets.

“Oh great”, I can hear you saying, “so which should I use, components or
skins?” Go to the section `Skin or
Components? <http://plone.org/documentation/manual/theme-reference/buildingblocks/components/skinorcomponents>`_
for a discussion of the pros and cons. At the time of writing we suggest
the simpler option is to keep your templates, images and style sheets in
your skin. We're just mentioning browser resources so that you know what
they are if you encounter them.
