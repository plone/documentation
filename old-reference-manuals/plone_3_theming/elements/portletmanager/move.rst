Moving or Removing a Portlet Manager
====================================

Tips on how to move or remove portlet managers.

Portlet managers are called by main\_template. Moving or removing them
is simply a case of customizing the template.

Through the Web
~~~~~~~~~~~~~~~

-  Site Setup > Zope Management Interface > portal\_skins >
   plone\_templates > main\_template
-  Customize this, and look for

   ::

       <div tal:replace="structure provider:[portlet manager name]" />

-  (use the Elements key to identify exactly which manager you're
   interested in)

In your own product
~~~~~~~~~~~~~~~~~~~

-  Put your own version of main\_template in
   [your theme product]/skins.

