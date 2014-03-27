Installing your Egg-Based Theme Product
=======================================

In this section, we will look at how to install egg-based themes using
buildout. As of Plone 3.1.2, all of the Plone installers create a
buildout that contains your Plone instance. When installing or
developing themes, buildout is highly recommended.

 To install the theme product you created in Practical 1:

-  First, if it isn't already there, copy your theme product to [your
   buildout]/[zinstance\|zeocluster]/src (if you find that this
   directory doesn't exist, you can create it yourself).
-  Then, using a text editor, edit your buildout.cfg (you'll find it in
   [your buildout]/[zinstance\|zeocluster]) and add the following
   information into the buildout, instance, and zcml sections. The
   actual buildout.cfg file will be much longer than the snippets below:

::

    [buildout]
     ...
     develop =
        src/plonetheme.mytheme

    [instance]
     eggs =
     ...
     plonetheme.mytheme

    zcml =
     ...
     plonetheme.mytheme

The last line tells buildout to generate a ZCML snippet (slug) that
tells Zope to recognize your theme product. The dots [...] indicate that
you may have additional lines of ZCML code here.

-  After updating the configuration, stop your site and run the
   ''bin/buildout'' command, which will refresh your buildout.
-  Then, restart your site and go to the 'Site Setup' page in the Plone
   interface and click on the 'Add-on Products' link. The 'Site Setup'
   area is also known as plone\_control\_panel, as this is the URL used
   to get to 'Site Setup'.
-  Choose the product (My Theme 1.0) by selecting the checkbox next to
   it and click the 'Install' button.

Note: You may have to empty your browser cache to see the effects of the
product installation.

Uninstalling a Theme Product
----------------------------

Uninstalling can be done from the 'Site Setup' / 'Add/Remove Products'
page, but only if you installed it from the 'Add/Remove Products'
screen. Not all themes uninstall cleanly, but reinstalling the Default
Plone product generally cures any issues here.
