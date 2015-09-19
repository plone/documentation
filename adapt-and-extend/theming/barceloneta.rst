=================
Barceloneta theme
=================

Barceloneta is the name of the Plone 5 default theme. It's named after the `Barcelona beach and neighbourhood`_. Barceloneta is a Diazo theme made from scratch using modern frontend technologies. It's responsive and spans throught all the Plone UI including the CMS backend part.

It's based on Bootstrap 3, but it's not dependent of it in any way. Although it reuses some of the structure and good practices of the original Bootstrap, it has its own personality and is fully adapted to Plone.

Structure
---------

Barceloneta uses LESS as a pre-processor to generate the resultant stylesheet. The LESS resources live in the `plonetheme.barceloneta egg`_ in the `plonetheme/barceloneta/theme/less`directory::

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

They are divided by base styling, layout, function, components and views, so they could be easily reusable and extended from other themes. The main LESS resource that imports all the others is `barceloneta.plone.less`.

It has a set of LESS variables that you can be overriden either through the web using the Theming control panel or by reusing it in your own theme. They include colors, sizes and other useful parameters.

Barceloneta makes use of the new Diazo bundle to expose their resources to Plone using the Resource Registries. As it is a pure Diazo theme, it keeps a low profile being Plone agnostic and only containing the theme itself.

Changes from previous versions of Plone
---------------------------------------
Regarding markup and comparing to the previous versions of Plone, Barceloneta introduced lots of changes in the default Plone markup to modernize it and make it more accessible. There is little parts of Plone that were not updated.

However, any class or id was stripped away from Plone in order to make easy upgrades and adaptations of existing Diazo themes. Whenever possible additional classes and ids were introduced being always domain namespaced `plone-*`.

Register LESS resources profile
-------------------------------
Barceloneta provides an optional GenericSetup profile that allows you to easily reuse their resources from the LESS files of your theme. This is done by register all the Barceloneta LESS resources as Plone Resource Registries resources. This profile is called `plonetheme.barceloneta:registerless` and can be imported from an external theme GenericSetup profile `metadata.xml` like::

    <?xml version="1.0"?>
    <metadata>
      <version>1000</version>
      <dependencies>
        <dependency>profile-plone.app.theming:default</dependency>
        <dependency>profile-plonetheme.barceloneta:registerless</dependency>
      </dependencies>
    </metadata>


.. _`Barcelona beach and neighbourhood`: https://en.wikipedia.org/wiki/La_Barceloneta,_Barcelona

.. _`plonetheme.barceloneta egg`: https://github.com/plone/plonetheme.barceloneta/tree/master/plonetheme/barceloneta/theme/less
