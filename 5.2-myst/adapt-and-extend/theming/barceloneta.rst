=================
Barceloneta Theme
=================

Barceloneta is the name of the Plone 5 default theme.

It's named after the `Barcelona beach and neighbourhood <https://en.wikipedia.org/wiki/La_Barceloneta,_Barcelona>`_.

Barceloneta is a Diazo theme made from scratch using modern frontend technologies.
It's responsive and spans through all the Plone UI including the CMS backend part.

It's based on `Bootstrap <https://getbootstrap.com/>`_ 3, but it's not dependent of it in any way.

Although it reuses some of the structure and good practices of the original Bootstrap, it has its own personality and is fully adapted to Plone.

Structure
=========

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

They are divided by base styling, layout, function, components and views, so they could be reusable and extended from other themes.
The main LESS resource that imports all the others is ``barceloneta.plone.less``.

It has a set of LESS variables that can be overriden either through the web using the `Theming control panel <http://docs.plone.org/external/plone.app.theming/docs/index.html#using-the-control-panel>`_ or by reusing it in your own theme.
They include colors, sizes, fonts and other useful parameters.

Barceloneta makes use of the new `Diazo bundle <http://docs.plone.org/adapt-and-extend/theming/resourceregistry.html#id26>`_ to expose its resources to Plone using the Resource Registries.
As it is a pure Diazo theme, it keeps a low profile being Plone agnostic and only containing the theme itself.


Regarding markup and comparing to the previous versions of Plone,
Barceloneta introduced lots of changes in the default Plone markup to modernize it and make it more accessible.

There are few parts of rendering Plone that were not updated.

Any class or id that was stripped away from Plone was done with the purpose of making upgrades and adaptations of existing Diazo themes uncomplicated.
Whenever possible additional classes and ids were introduced being always domain namespaced ``plone-*``.

Register LESS Resources
=======================

Barceloneta provides an optional GenericSetup profile that allows you to reuse the resources from the LESS files of your theme.

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
================================================

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

You can define your own Diazo bundle (JavaScript and Less/CSS) in your manifest.cfg file by using the options
``development-js``, ``production-js``, ``development-css`` and ``production-css``.

This bundle will not be included in the backend theme.


Current Issues
--------------

You will still need to include a minimal Plone bundle in your theme for rendering the toolbar correctly.
It is intended in future versions of Plone that this will be available by default and be very minimal making no assumptions about
the JavaScript or CSS of your frontend theme so as not to conflict with it.

Why this is a good idea
^^^^^^^^^^^^^^^^^^^^^^^

- It reduces the effort in theming.
- In most cases your users will never see edit, sharing, sitesetup or other aspects of the Plone backend UI.
- Making those screens work with a new theme is a lot of work.
- The backend pages can include a lot of add on functionality which might be hard to integrate.
- This might not be tested for integration into third-party themes.
- Barceloneta has been tested for UI and to some extend accessibility.
- Retheming could make the UI harder to use for editor.
- The backend UI is more likely to change between versions.
- Theming it means your theme will have to change too.

How this works
^^^^^^^^^^^^^^

- There is a body class tag "frontend".
- This appears when current view or page is unprotected or only protected by a "can view" permisission.
- In most cases this is your "view" of an object, and some extra pages like contact-us, login_form etc.
- Almost everything else is protected by other permissions and are therefore intended to be used by logged in users.
- ``++theme++barceloneta/backend.xml`` is mainly the same as the normal Barceloneta rules except for a few exceptions:

  - It will only apply theming when body.frontend is not present
  - Except it will include the toolbar regardless if body.frontend is there or not.
  - It disables all popups. This makes it possible to switch theme using just the toolbar
  - It removes headers, footers and most "theme" elements from backend pages.


Inheriting a new theme from Barceloneta
---------------------------------------

.. note:: based on `Customize Plone 5 default theme on the fly <http://datakurre.pandala.org/2015/05/customize-plone-5-default-theme-on-fly.html>`_ by Asko Soukka.

If you do not want to build a complete theme from scratch, you can use Barceloneta and just make small changes.

Create a new theme in the theming editor containing the following files:

- ``manifest.cfg``, declaring your theme:

.. code-block:: ini

    [theme]
    title = mytheme
    description =
    development-css = /++theme++mytheme/styles.less
    production-css = /++theme++mytheme/styles.css

- ``rules.xml``, including the Barceloneta rules:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <rules
        xmlns="http://namespaces.plone.org/diazo"
        xmlns:css="http://namespaces.plone.org/diazo/css"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:xi="http://www.w3.org/2001/XInclude">

      <!-- Import Barceloneta rules -->
      <xi:include href="++theme++barceloneta/rules.xml" />

      <rules css:if-content="#visual-portal-wrapper">
        <!-- Placeholder for your own additional rules -->
      </rules>

    </rules>

- a copy of ``index.html`` from Barceloneta (this one cannot be imported or inherited, it must be local to your theme).

- ``styles.less``, importing Barceloneta styles:

.. code-block:: css

    /* Import Barceloneta styles */
    @import "++theme++barceloneta/less/barceloneta.plone.less";

    /* Customize whatever you want */
    @plone-sitenav-bg: pink;
    @plone-sitenav-link-hover-bg: darken(pink, 20%);
    .plone-nav > li > a {
      color: @plone-text-color;
    }

Then you have to compile ``styles.less`` to obtain your ``styles.css`` file using the "Build CSS" button.

Now your theme is ready. You can keep it in the theming editor, or you can export it and put the files in your theme add-on.

This approach applies to both FS based and TTW based themes.
Even when working with a FS bases theme, you can compile your less files using the theming editor: the theming editor allows to inspect FS-based themes and the Build CSS button will return the resulting CSS so you can copy/paste it into your sources.

.. note:: even if this approach is probably fine for a quick fix in a FS theme, it might be painful at start when you develop the all theme. In that case, 2 approaches:

    - either work directly in a TTW theme, entirely with the theming editor, and we you are done, export it as a zip and put it in your sources
    - either put the barceloneta resources in your theme temporarily, change the LESS import path (like @import "++theme++barceloneta/less/barceloneta.plone.less";) temporarily, and when you are done, clean that up.
