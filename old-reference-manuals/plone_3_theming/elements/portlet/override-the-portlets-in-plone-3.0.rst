Override the portlets in Plone 3.0
==================================

Customizing the portlets is a regular task, working with Plone theme. In
this how-to we will find out how-to do this in Plone 3.0 with it's new
mechanism for managing portlets (contributed by Denys Mishunov)

Purpose
~~~~~~~

It was pretty easy to customize one of the standard portlet in times of
Plone versions prior 3.0. You just had to copy a page template for
appropriate portlet to your theme product and do whatever you want,
changing it's XHTML. You could also create a new portlet the same easy
way - just create a template for the new portlet and register this
portlet with your site's Properties.

In Plone 3.0 portlets became slightly more complex. But don't be afraid.
They became much more powerful at the same time! The advantage becomes
obvious now, right? ;) They are served from separate python package and
have really flexible management possibilities. So, it's worth to try
this new mechanism to realize how powerful it is.

Prerequisities
~~~~~~~~~~~~~~

First thing we should mention - this is not about TTW (Through The Web)
customization. If you need a fast and dirty trick, have a look at
portal\_view\_customizations tool. This how-to assumes you want to have
your changes in a repeatable way, so that you could have the same
changes on any site where you install your product.

Another thing you might consider is worth a mentioning - you don't need
this technique in **any** case you want to customize a portlet in Plone
3.0. If you have hardly customized portlets used in previous versions of
Plone or you want to continue using portlets in "pre-3.0-era-way" (that
we strongly don't recommend) you might need to have a look at
ClassicPortlet that is shipped with Plone 3.0. It deals with the regular
page templates the same way you have worked with portlets before Plone
3.0.

And the last before we move on. If you want to customize any of the
standard portlets removing all back-end logic from it (making a static
portlet), don't do this. We mean that - **don't** do this. Wise people
thought about you. Better install plone.portlet.static and play with it,
creating the static portlets when you need it.

So, for all those who are still with us... we move on finally.

We assume you have created **MyTheme** Plone 3 theme with either
DIYPloneStyle or ZopeSkel generators. We do not cover explanations of
all aspects of creating a theme for Plone 3.0. To find out more about
core ideas of making a theme, managing the viewlets in Plone 3.0 and
many more, check an excellent tutorial by David Convent - `Customizing
the viewlets in
main\_template <http://plone.org/how-to/override-the-portlets-in-plone-3.0/.org/documentation/tutorial/customizing-main-template-viewlets>`_.

The key concept in working with portlets in Plone 3.0 is the use of Zope
3 skin layer - the same as we have when overriding a viewlet. We assume
you have at least the following minimum set of files in
**MyTheme/browser** folder:

::

    - browser/    - __init__.py    - configure.zcml    - interfaces.py

In common, portlets' overriding process looks like this:

-  choose the portlet you want to override;
-  register a skin layer if you don't have one yet in **interfaces.py**;
-  add the special <plone:portletRenderer/> directive to
   **MyTheme/browser/configure.zcml**;
-  define **portlet** attribute for <plone:portletRenderer /> directive.
   This is a portlet data provider type for which this override is used.
   This can be either class or interface. For example
   plone.app.portlets.portlets.navigation.INewsPortlet;
-  define a new **template** attribute for <plone:portletRenderer />
   directive. When you add this the default renderer for portlet you are
   overriding will be used, but with your template;
-  in case you need to customize the default behavior for the portlet,
   you should use **class** attribute instead of simple template. This
   new class will be acting as the renderer for the portlet instead of
   the default one;
-  define **layer** attribute for <plone:portletRenderer /> directive
   with **MyTheme** browser layer. The **layer** attribute of the
   portletRenderer attribute associates a particular IPortletRenderer
   with a particular browser layer (**MyTheme** layer in our case). When
   our layer is in effect (i.e. MyTheme is installed) the new renderer
   will be used instead of the default one;
-  add a new template to **MyTheme/browser** that will implement the
   renderer;
-  restart Zope and enjoy.

Step by step
~~~~~~~~~~~~

1. Choose the portlet
^^^^^^^^^^^^^^^^^^^^^

First of all we should decide what portlet we would like to customize.
Let's choose the News portlet. If you will have a look at the standard
news portlet, you will see those news\_icon images in-front of the
titles. Let's get rid of them in the XHTML just for the test.

Plone default portlets are declared in the
**plone.app.portlets.portlets** package. The core Plone 3.0 portlets can
be found in **$INSTANCE\_HOME/lib/python/plone/app/portlets/portlets/**.
It might be located somewhere else in the $PYTHONPATH though. Depending
on the zope installation (win32 or unix like operating system,
installation from source, installer, eggs or else…), you may need to use
the search tools available in your operating system to locate the
package.

**plone.app.portlets.portlets** package contains python modules, page
templates and ZCML configuration file - **configure.zcml**. This file
contains a set of <plone:portlet /> directives that define the standard
portlets like this:

::

    <plone:portlet    name="portlets.News"    interface=".news.INewsPortlet"    assignment=".news.Assignment"    renderer=".news.Renderer"    addview=".news.AddForm"    editview=".news.EditForm"    />

Attributes in the above code are pretty self-explanatory. But if they
are not clear to you or you want to know more about additional
attributes for <plone:portlet />, have a look at **IPortletDirective**
interface in **metadirectives** module inside the plone.app.portlets
package.

2. Register a skin layer if you don't have one yet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can register an override for a portlet only for one theme (one skin
selection) thanks to the **plone.theme** package. Thanks to
**plone.theme**, we can set a Zope 3 skin layer that corresponds to a
particular skin selection in portal\_skins (a theme).

Add the following code to **MyTheme/browser/interfaces.py** if you don't
have it yet:

::

    from plone.theme.interfaces import IDefaultPloneLayerclass IThemeSpecific(IDefaultPloneLayer):    """Marker interface that defines a Zope 3 skin layer bound to a Skin       Selection in portal_skins.    """

3. Add the directive to configure.zcml with appropriate attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Along with <plone:portlet /> directive, plone.app.portlets package
defines another one - <plone:portletRenderer />. The last one is used to
override the portlets, defined in your site. It has quite a few possible
attributes that can be found in **metadirectives** module inside the
plone.app.portlets package. We will not list them all here, so just
spend 5 minutes and have a look at those attributes, so that you could
understand the following code...

... 5 minutes later...

Ok, let's get back to work. So, to override the standard News portlet
for MyTheme product we should add <plone:portletRenderer /> directive to
**MyTheme/browser/configure.zcml**. Let's have a look how this should
look like (be sure you have
xmlns:plone="http://namespaces.plone.org/plone" namespace defined in
your **<configure>** top node.):

::

    <include package="plone.app.portlets" /><interface   interface=".interfaces.IThemeSpecific"   type="zope.publisher.interfaces.browser.IBrowserSkinType"   name="My Theme"   /><plone:portletRenderer   portlet="plone.app.portlets.portlets.news.INewsPortlet"   template="mytheme_news.pt"   layer=".interfaces.IThemeSpecific"   />

First of all we include plone.app.portlets package to be sure that
default portlets are enabled before we override anything.

Then we make browser layer interface for **MyTheme**, defined in
**MyTheme/browser/interfaces.py**, available. If you have customized any
viewlet you should already have this in **configure.zcml** so no need to
add it twice in the same theme.

Next, let's sort out what attributes we use here:

-  **portlet** - define the portlet that we are going to override. In
   our case we define the full dotted path to INewsPortlet interface,
   that is implemented by news portlet;
-  **template** - the name of a template that implements the renderer.
   The default renderer for this news portlet will be used, but with
   "mytheme\_news.pt template instead of the default one.
-  **layer** - our browser layer for which this renderer is used.
-  one more attribute you might need to remember here is **class**. You
   will need to use it in case you want to change the default behavior
   of the portlet. This attribute will define the class that will be
   used as a renderer for this portlet instead of the default one.

That's it with **configure.zcml**. Let's move on.

4. Add a new template for portlet's renderer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

So, in previous part we have defined mytheme\_news.pt as a value for
**template** attribute. But we don't have that template on file-system.
Let's add it to **MyTheme/browser/**. Just copy **news.pt** template for
news portlet from **plone.app.portlets.portlets** to
**MyTheme/browser/** and rename it to mytheme\_news.pt. Open this
template in your favorite editor and let's play with it a little bit.

As you remember we should get rid of standard news\_icon.gif icons we
get for news items by default. Find the following line in your template:

::

    <img tal:replace="structure item_icon/html_tag" />

and comment it out so that we do not un-recoverable steps and could
revert our changes later. So, we get:

::

    <!-- <img tal:replace="structure item_icon/html_tag" /> -->

That's all folks!
^^^^^^^^^^^^^^^^^

So, that's it. Restart your Zope and have a look at your news items
portlet - no images! Cool! Yeah! Actually not that cool just to remove
the images, that might be useful for community portals :)

What's next?
^^^^^^^^^^^^

This example is really simple and not pretty useful for sure. But you
definitely can do much better customizations now. When using **class**
attribute in <plone:portletRenderer/> directive you can do portlets that
will really differ from default one. And that's where the beauty of
portlets in Plone 3.0 goes - you will not need to put a load of python
to your page templates as you had to do before. All python will be
exactly where it should be - in python class. And template will just get
the results from different python methods within that class.

Enjoy!
