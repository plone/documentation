=================
Barceloneta theme
=================

Barceloneta is the name of the Plone 5 default theme.
It's named after the `Barcelona beach and neighbourhood <https://en.wikipedia.org/wiki/La_Barceloneta,_Barcelona>`_.
Barceloneta is a Diazo theme made from scratch using modern frontend technologies.
It's responsive and spans throught all the Plone UI including the CMS backend part.

It's based on Bootstrap 3, but it's not dependent of it in any way.
Although it reuses some of the structure and good practices of the original Bootstrap, it has its own personality and is fully adapted to Plone.

Structure
---------

Barceloneta uses `LESS <http://lesscss.org/>`_ as a pre-processor to generate the resultant stylesheet.
The LESS resources live in the `plonetheme.barceloneta egg <https://github.com/plone/plonetheme.barceloneta/tree/master/plonetheme/barceloneta/theme/less>`_ in the ``plonetheme/barceloneta/theme/less`` directory::

    plonetheme/barceloneta/theme/less
    ├── accessibility.plone.less
    ├── alerts.plone.less
    ├── barceloneta-compiled.css
    ├── barceloneta-compiled.css.map
    ├── barceloneta.css
    ├── barceloneta.plone.export.less
    ├── barceloneta.plone.less
    ├── barceloneta.plone.local.less
    ├── behaviors.plone.less
    ├── breadcrumbs.plone.less
    ├── buttons.plone.less
    ├── code.plone.less
    ├── contents.plone.less
    ├── controlpanels.plone.less
    ├── deco.plone.less
    ├── discussion.plone.less
    ├── dropzone.plone.less
    ├── event.plone.less
    ├── fonts.plone.less
    ├── footer.plone.less
    ├── forms.plone.less
    ├── formtabbing.plone.less
    ├── grid.plone.less
    ├── header.plone.less
    ├── image.plone.less
    ├── loginform.plone.less
    ├── main.plone.less
    ├── mixin.borderradius.plone.less
    ├── mixin.buttons.plone.less
    ├── mixin.clearfix.plone.less
    ├── mixin.forms.plone.less
    ├── mixin.grid.plone.less
    ├── mixin.gridframework.plone.less
    ├── mixin.images.plone.less
    ├── mixin.prefixes.plone.less
    ├── mixin.tabfocus.plone.less
    ├── modal.plone.less
    ├── normalize.plone.less
    ├── pagination.plone.less
    ├── pickadate.plone.less
    ├── plone-toolbarlogo.svg
    ├── portlets.plone.less
    ├── print.plone.less
    ├── roboto
    ├── scaffolding.plone.less
    ├── search.plone.less
    ├── sitemap.plone.less
    ├── sitenav.plone.less
    ├── sortable.plone.less
    ├── states.plone.less
    ├── tables.plone.less
    ├── tablesorter.plone.less
    ├── tags.plone.less
    ├── thumbs.plone.less
    ├── toc.plone.less
    ├── tooltip.plone.less
    ├── tree.plone.less
    ├── type.plone.less
    ├── variables.plone.less
    └── views.plone.less

They are divided by base styling, layout, function, components and views, so they could be easily reusable and extended from other themes.
The main LESS resource that imports all the others is ``barceloneta.plone.less``.

It has a set of LESS variables that can be overriden either through the web using the Theming control panel or by reusing it in your own theme.
They include colors, sizes, fonts and other useful parameters.

Barceloneta makes use of the new Diazo bundle to expose its resources to Plone using the Resource Registries.
As it is a pure Diazo theme, it keeps a low profile being Plone agnostic and only containing the theme itself.

Changes from previous versions of Plone
---------------------------------------

Regarding markup and comparing to the previous versions of Plone, Barceloneta introduced lots of changes in the default Plone markup to modernize it and make it more accessible.
There are few parts of rendering Plone that were not updated.

However, any class or id that was stripped away from Plone was done with the purpose of making upgrades and adaptations of existing Diazo themes easy.
Whenever possible additional classes and ids were introduced being always domain namespaced ``plone-*``.

Register LESS resources profile
-------------------------------

Barceloneta provides an optional GenericSetup profile that allows you to easily reuse the resources from the LESS files of your theme.
This is done by registering all the Barceloneta LESS resources as Plone Resource Registries resources.
This profile is called ``plonetheme.barceloneta:registerless`` and can be imported from an external theme GenericSetup profile ``metadata.xml`` like:

.. code-block:: xml

    <?xml version="1.0"?>
    <metadata>
      <version>1000</version>
      <dependencies>
        <dependency>profile-plone.app.theming:default</dependency>
        <dependency>profile-plonetheme.barceloneta:registerless</dependency>
      </dependencies>
    </metadata>


Using the barceloneta theme only for the backend
------------------------------------------------

You can develop a custom Diazo based theme and use the Barceloneta theme only for the backend like follows shown below:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <rules
        xmlns="http://namespaces.plone.org/diazo"
        xmlns:css="http://namespaces.plone.org/diazo/css"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:xi="http://www.w3.org/2001/XInclude">

      <!-- Include the backend theme -->
      <xi:include href="++theme++barceloneta/backend.xml" />

      <!-- Only theme front end pages -->
      <rules css:if-content="body.frontend#visual-portal-wrapper">

        <theme href="index.html" />

        <!-- Your diazo front end rules go here -->

        </rules>
    </rules>

You can define your own Diazo bundle (JavaScript and Less/CSS) in your manifest.cfg file by using the options ``development-js``, ``production-js``, ``development-css`` and ``production-css``. This bundle will not be included in the backend theme.
