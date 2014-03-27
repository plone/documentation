====================
 Resource folders
====================

.. admonition:: Description

        How to use resource directories to expose static media files (css, js, other)
        in your Plone add-on product
       
.. contents:: :local: 

Introduction
=============

Resource folders are the Zope Toolkit way to expose static media files to
Plone URL mapping.

Resource folders provide a mechanism which allows conflict free
way to have static media files mapped to Plone URL space.
Each URL is prefixed with ``++resource++your.package``  
resource identified.

ZCML resourceDirectory
======================

If you want to customize media folder mapping point, you need to use
the resourceDirectory directive.

Below is an example how to map *static* folder in your add-on
root folder to be exposed via ++resource++your.product/ URI

.. code-block:: xml

        <configure
            xmlns="http://namespaces.zope.org/zope"
            xmlns:five="http://namespaces.zope.org/five"
            xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
            xmlns:i18n="http://namespaces.zope.org/i18n"
            xmlns:browser="http://namespaces.zope.org/browser"        
            i18n_domain="your.product">
        
                  
                  <!-- Register the installation GenericSetup extension profile
                       (needed for portal_css and portal_javascripts XML import) -->
                  <genericsetup:registerProfile
                      name="default"
                      title="Your add-on product name"
                      directory="profiles/default"
                      description="Your add-on product description"
                      provides="Products.GenericSetup.interfaces.EXTENSION"
                      />
                  
                   <!-- Resource directory for static media files -->
                 <browser:resourceDirectory
                        name="your.product"
                        directory="static"
                        />
                  
                  <!-- -*- extra stuff goes here -*- -->
        
        </configure>

        

Further reading


* `Example <http://www.themeswiki.org/Creating_a_Custom_theme_for_Plone#Image_Resources>`_


Grok static media folder
=========================

Learn more about :doc:`Grok and Plone integration </develop/addons/components/grok>`.

.. warning:: Since five.grok 1.3.0 this method does not work.

The easiest way to manage static resources is to make use of the static resource directory feature in five.grok.
Simply add a directory called static in the package and make sure that the ``<grok:grok package="." />``
line appears in configure.zcml.

Example how to include ``yourproduct.app/static`` folder as ``++resource++yourproduct.app`` URL.

.. code-block:: xml

        <configure
            ...       
            xmlns:grok="http://namespaces.zope.org/grok">
            
          <grok:grok package="." />
           
        </configure>
        
If a ``static`` resource directory in the ``example.conference`` package contains a file called ``conference.css``,
it will be accessible on a URL like ``http://<server>/site/++resource++example.conference/conference.css``.
The resource name is the same as the package name wherein the static directory appears.
