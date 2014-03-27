Skin or Components?
===================

You’ll have noticed that you can turn any template or css file, or any
directory containing these into a component. So why bother with the Skin
building block?

The product created by the plone3\_theme paster template does the
following:

-  **overrides and rewrites** of the standard Plone Default templates
   and CSS files go in the **Skin** section – the skins directory.
-  **new** style sheets and images go in the **Components** section –
   the browser directory.

This manual suggests putting all your templates, style sheets and images
in the Skin section - leaving just the viewlet and portlet templates in
the components. There are a few reasons for this

-  it is simpler to do this when you're just starting out
-  it follows the way in which Plone Default is constructed
-  it makes it quick and easy to adjust your theme on-the-fly after it's
   installed. At that point, you can make further customizations of the
   Skin through the Zope Management Interface.

At the time of writing there's a `big
discussion <http://www.openplans.org/projects/ootb-plone-themes/lists/ootb-plone-themes-discussion/archive/2008/05/1209686168874/forum_view>`_
going on about this very question.

 

If you want to strip the browser resources out of the product created by
the plone3\_theme paster template

-  remove the images and stylesheets directories in the [your theme
   package]/browser
-  remove the <browser:resourceDirectory /> entries in [your theme
   package]/browser/configure.zcml
-  remove the register stylesheet entry for main.css in [your theme
   package]/profiles/default/cssregistry.xml
-  if you have already installed your product you may need to check the
   CSS registry in the Zope Management Interface (portal\_css) and
   delete the main.css entry there too

 
