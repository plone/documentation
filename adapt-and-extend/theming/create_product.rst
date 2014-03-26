Create a Plone Theme product with Diazo
=======================================

Introduction
------------

Creating a theme product with the Diazo inline editor is an easy way to start
and to test, but it is not a solid long term solution.

Even if ``plone.app.theming`` allows to import and export a Diazo theme as a ZIP
archive, it might be prefereable to manage your theme into an actual Plone
product.

One of the most obvious reason is it will allow you to override Plone elements
that are not accessible from the pure Diazo features (like overloading content
views templates, viewlets, configuration settings, etc.).

Create a product to handle your Diazo theme
-------------------------------------------

Create a module
+++++++++++++++

To create a blank module, you will use ZopeSkel. ZopeSkel is part of the
executables files deployed in ``./bin`` on a standard UnifiedInstaller install
once you have run the develop.cfg buildout::

    bin/buildout -Nc develop.cfg

ZopeSkel allows to initialize Python modules based on different templates.

You will use the template named ``plone``.

Into your Plone install, go to src/, and launch the following command::

    $ ../bin/zopeskel plone

Give a name to your module (for instance: projectname.theme).
And just accept all the default choices but::

    Register Profile (Should this package register a GS Profile) [False]: True

The module is created in ``src/projectname.theme``.

Declare this new module in your ``buildout.cfg``::

    develop =
        ...
        src/projectname.theme

    eggs =
        ...
        projectname.theme

And run buildout::

    $ bin/buildout -Nv

Put your Diazo theme in the module
++++++++++++++++++++++++++++++++++

Create a folder for the Diazo resources::

    $ mkdir src/projectname.theme/projectname/theme/static

Download your theme created using the inline editor and unzip it in that folder.

Modify the ``configure.zcml`` file to declare this ``static`` folder::

    <configure
        ...
        xmlns:plone="http://namespaces.plone.org/plone"
        >

        ...

        <plone:static name="projectname.theme" directory="static" type="theme" />

        ...

    </configure>

Update the GenericSetup profile
+++++++++++++++++++++++++++++++

In ``src/projectname.theme/projectname/theme/profiles/default/``, you have to:

- Add the dependency with ``plone.app.theming`` in ``metadata.xml``::

    <?xml version="1.0"?>
    <metadata>
      <version>1000</version>
      <dependencies>
        <dependency>profile-plone.app.theming:default</dependency>
      </dependencies>
    </metadata>

- Declare the theme by creating ``theme.xml``::

    <?xml version="1.0"?>
    <theme>
      <name>projectname.theme</name>
      <enabled>true</enabled>
    </theme>

Then you can restart Zope, and install the new product to activate the theme.

Override the Plone skin
-----------------------

Diazo allows to control the global rendering of the Plone pages.

But if you need to change elements which are deeply melt into the Plone
generated content, or which are not easily accessible using a CSS selector, or
maybe an image (for instance, the members default portrait, ``defaultUser.png``)
which are provided by the Plone skin, you will have to override the Plone skin.

.. note::
    that is basically what you do when you go to ZMI / portal_skins and 
    click on the ``Customize`` button. But here, you will do that from the sources.

To override Plone skin elements from our product, you will need to:

    Create a folder
    ``src/projectname.theme/projectname/theme/skins/projectname_custom`` and put
    the needed resources in that folder (like your new version of
    ``defaultUser.png``). It can be anything, you just need to make sure it as
    the very same name as the original one.

    Declare that folder in configure.zcml::

        <configure

            ...

            xmlns:cmf="http://namespaces.zope.org/cmf"
            >

          ...
          
          <cmf:registerDirectory name="projectname_custom"/>

        </configure>

    And move it in first position compare to the other existing skin layers by
    creating
    ``src/projectname.theme/projectname/theme/profiles/default/skins.xml``::

        <?xml version="1.0"?>
        <object name="portal_skins" allow_any="False" cookie_persistence="False" default_skin="projectname.theme">

          <object name="projectname_custom"
              meta_type="Filesystem Directory View"
              directory="projectname.theme:skins/projectname_custom"/>
          <skin-path name="projectname.theme" based-on="Sunburst Theme">
            <layer name="projectname_custom"
                insert-after="custom"/>
          </skin-path>

        </object>

    You can now restart Zope and re-install your product from the Plone control
    panel (Site Setup > Add-ons), once done, the elements contained in 
    ``projectname_custom`` will take priority on the corresponding elements from
    the Plone skin (or any other add-on skin).

Override Plone BrowserViews with jbot
-------------------------------------

A large part of the Plone UI are not provided by the portal_skins layers but by
BrowserViews.

That is the case for viewlets (all the blocks you can see when you call the url
``./@@manage-viewlets``).

.. note:: to override them from the ZMI, you can go to ``./portal_view_customizations``.

To overrides them from your theme product, the easiest way is to use
``z3c.jbot`` (Just a Bunch of Templates).

First of all you need to add this module in ``buildout.cfg``::

    eggs =
        ...
        z3c.jbot

And run buildout::

    $ bin/buildout -Nv

Then create a folder
``src/projectname.theme/projectname/theme/static/overrides``.

And declare that folder as a jbot folder:

- modify configure.zcml::

    <configure

        ...

        xmlns:browser="http://namespaces.zope.org/browser"
        >

        ...
      
        <include package="z3c.jbot" file="meta.zcml" />
        <interface name="projectname.theme"
            interface="projectname.theme.interfaces.IThemeSpecific"
            type="zope.publisher.interfaces.browser.IBrowserSkinType"
            />
        <browser:jbot directory="static/overrides" />

    </configure>

- create ``interfaces.py``::

    from plone.theme.interfaces import IDefaultPloneLayer

    class IThemeSpecific(IDefaultPloneLayer):
        """Marker interface that defines a Zope 3 browser layer and a plone skin marker.
        """

- and declare a layer by creating ``src/projectname.theme/projectname/theme/profiles/default/browserlayer.xml``::

    <?xml version="1.0"?>
    <layers>

      <layer name="projectname.theme" interface="projectname.theme.interfaces.IThemeSpecific"/>

    </layers>

Then, you can put in
``src/projectname.theme/projectname/theme/static/overrides`` all the templates
you want to override but you will need to name them by prefixing the template
name by its complete path to its original version.

For instance, to override ``colophon.pt`` from plone.app.layout, knowing this
template in a subfolder named ``viewlets``, you need to name it
``plone.app.layout.viewlets.colophon.pt``.

.. note:: ZMI > portal_view_customizations is an handy way to find the template path.

You can now restart Zope and re-install your product from the Plone control
panel (Site Setup > Add-ons).

Manage CSS and JS in registries
-------------------------------

For performances reasons, it is recommended to minimize the amount of JS and CSS
files loaded in you pages.

To do that, Plone offers two registries, ``portal_javascript`` and
``portal_css``, which allow to:

    - declare resources you want to load,
    - sort them,
    - if needed, specify conditions to decide when a resource must be loaded or not.

Using those information, Plone will inject the corresponding tags (``<script>``,
``<link>``, etc.) in the ``<head>``, and if Zope does not run in debug mode, the
different files will be merged and compressed.

It is obviously important to manage your theme's main CSS and JS that way.

To do so, you first need to **remove them from your theme HTML templates** (so
you do not make things worse by loading them twice).

Then, declare them to the registries:

    Create a file
    ``src/projectname.theme/projectname/theme/profiles/default/jsregistry.xml``::

        <?xml version="1.0"?>
        <object name="portal_javascripts">

            <javascript id="++theme++projectname.theme/js/theme.js"
                cacheable="True"
                compression="none"
                cookable="True"
                enabled="True"
                expression="request/HTTP_X_THEME_ENABLED | nothing"
                inline="False"
                insert-after="++resource++collective.js.leaflet/leaflet.js"
            />

        </object>

    And a file
    ``src/projectname.theme/projectname/theme/profiles/default/cssregistry.xml``::

        <?xml version="1.0"?>
        <object name="portal_css">

          <stylesheet
            id="++theme++projectname.theme/css/theme.css"
            applyPrefix="1"
            media=""/>

          <stylesheet
            id="++theme++projectname.theme/bootstrap/css/bootstrap.css"
            applyPrefix="1"
            media=""/>

        </object>

You can now restart Zope and re-install your product from the Plone control
panel (Site Setup > Add-ons).

.. note:: the expression ``request/HTTP_X_THEME_ENABLED | nothing`` returns True only if the page is served through Diazo (it allows to avoid to load the resources when the Diazo theme is not active).

You have to be careful about the resources order and their conditions: resources
are merged together in the order they are declared with as far as the condition
are the same.

If the next resource as a different condition, it will end the current merged
set of resources, and start a new one.

So if you want to minimize the total number of resulting files, you have to:

    - declare as few conditions as possible,
    - when you have to declare a condition, try to make them identical if possible,
    - and re-order the resources in such a way that similar conditions are consecutives.

Regarding the JS or CSS which are not used globally into the web site, but just 
in a very specific template, it might be better to not declare them in the
registries, and let them declared manually into the static HTML /template.

.. note:: if you use a responsiveCSS framework, it is often useful to deactivate the Plone ``mobile.css`` file which might produces bad formatting (typically with Boostrap). To do so, you add the following to ``cssregistry.xml``::

        <stylesheet id="mobile.css" enabled="False" />
