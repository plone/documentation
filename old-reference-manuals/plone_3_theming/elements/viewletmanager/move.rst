Moving, Removing or Hiding a Viewlet Manager
============================================

Some hints on moving or hiding viewlet managers.

Viewlet managers are called by page templates. Moving or removing them
is simply a case of customizing the template. Most are called by the
main\_template, but you may also need to look into specific content
views for some of them.

Quick Cheat Sheet
-----------------

Through the Web
~~~~~~~~~~~~~~~

-  Site Setup > Zope Management Interface > portal\_skins >
   plone\_templates or plone\_content
-  Click the Customize button, and look for

   ::

       <div tal:replace="structure provider:[viewlet manager name]" />

-  (use the Elements key to identify exactly which manager you're
   interested in)

In your own product
~~~~~~~~~~~~~~~~~~~

-  Put your own version of main\_template or of the content views in
   [your theme package]/skins.

