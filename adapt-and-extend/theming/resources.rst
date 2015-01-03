===============================
JS/CSS Resources
===============================

.. admonition:: Description

    Resources are js/css and its dependencies to add the frontend logic and design
    on top of Plone. There are so many different kind of resources like widgets, design styles,
    behavior logic and single page apps. In order to organize them we are using two
    main standard technologies: require.js and less.

    The goal of this recipe is to help you confirm that everything is working.

.. contents:: :local:

Resources
---------

The main unit of the resource system, its a js and some css that are going to be identified on a name.

As possible options we have the shim (export, init and depends) so it can be configured to be exported to the global namespace, init on load and depend on some other resource.

An example of a resource definition on registry.xml::

  <records prefix="plone.resources/tinymce"
            interface='Products.CMFPlone.interfaces.IResourceRegistry'>
      <value key="js">++plone++static/components/tinymce/tinymce.js</value>
      <value key="export">window.tinyMCE</value>
      <value key="init">function () { this.tinyMCE.DOM.events.domLoaded = true; return this.tinyMCE; }</value>
      <value key="css">
        <element>++plone++static/components/tinymce/skins/lightgray/skin.min.css</element>
        <element>++plone++static/components/tinymce/skins/lightgray/content.inline.min.css</element>
      </value>
  </records>


The options are :

- js : URL of the js file

- export : shim export option

- init : shim init option

- depends : shim depends option

- css : list of css elements

- url : url that will be defined on the require.js namespace as the resource-url variable

The export/init/depends are the shim option to load the js files in the correct order on the global namespace, for more information : http://requirejs.org/docs/api.html#config-shim

The URL option allow you to define the base url in case you want to load txt resources on require js::
        
    registry.xml 

    <records prefix="plone.resources/mockup-patterns-structure"
            interface='Products.CMFPlone.interfaces.IResourceRegistry'>
        <value key="js">++resource++mockup/structure/pattern.js</value>
        <value key="url">++resource++mockup/structure</value>
        <value key="css">
            <element>++resource++mockup/structure/less/pattern.structure.less</element>
        </value>
    </records>

    ...

    mockup/patterns/structure/js/views/actionmenu.js

    define([
      'jquery',
      'underscore',
      'backbone',
      'mockup-ui-url/views/base',
      'mockup-utils',
      'text!mockup-patterns-structure-url/templates/actionmenu.xml',
      'bootstrap-dropdown'
    ], function($, _, Backbone, BaseView, utils, ActionMenuTemplate) {
    'use strict';

    var ActionMenu = BaseView.extend({
        className: 'btn-group actionmenu',
        template: _.template(ActionMenuTemplate),

    ...


Default resources on Plone
^^^^^^^^^^^^^^^^^^^^^^^^^^

Plone loads a group of mockup components and bower components as resources on the registry. 
In order to avoid running bower install on each installation of Plone it ships by default a minimal
bower components folder on the CMFPlone static folder with the correct versions of the resources
that are need to run the default plone js/css.

The default bower components shipped are on : 

https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/static/bower.json

The group of resources registered on CMFPlone are :

https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/profiles/dependencies/registry.xml


The ++plone++ traversal namespace
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a specific folder type called ++plone++ designed to be similar to ++theme++ but with the difference that
you can overwrite an specific file, so its possible to edit a resource TTW.

Example::

    <plone:static
      directory="static"
      type="plone"
      name="static"
      />


Bundle
------

Mainly bundles are groups of resources that are going to be loaded on your plone site. Instead of loading single resources we can group them by our possible needs. In case you
develop an specific add-on you will need to create your own bundle, if you want to load a single page you will create a bundle, if you want to define some group of js/css that
will be rendered on some page you need a bundle. 

Each bundle will be delivered on a production site as a standalone resource: two http calls (js/css) for each bundle

Examples::

    <records prefix="plone.bundles/plone"
                interface='Products.CMFPlone.interfaces.IBundleRegistry'>
        <value key="resources">
            <element>plone</element>
        </value>
        <value key="enabled">True</value>
        <value key="jscompilation">++plone++static/plone-compiled.js</value>
        <value key="csscompilation">++plone++static/plone-compiled.css</value>
        <value key="last_compilation">2014-08-14 00:00:00</value>
    </records>

    <records prefix="plone.bundles/plone-legacy"
                interface='Products.CMFPlone.interfaces.IBundleRegistry'>
        <value key="resources" purge="false">
            <element>plone_javascript_variables</element>
            <element>unlockOnFormUnload</element>
            <element>table_sorter</element>
            <element>inline-validation</element>
            <element>jquery-highlightsearchterms</element>
        </value>
        <value key="depends">plone</value>
        <value key="jscompilation">++plone++static/plone-legacy-compiled.js</value>
        <value key="csscompilation">++plone++static/plone-legacy-compiled.css</value>
        <value key="last_compilation">2014-08-14 00:00:00</value>
        <value key="compile">False</value>
        <value key="enabled">True</value>
    </records>

The options are :

- enabled: the bundle its enabled by default

- depends: the bundle depends on another bundle

- compile: the bundle has less/requirejs

- jscompilation: url where the minimized/compiled js version will be

- csscompilation: url where the minimized/compiled css version will be 

- last_compilation: date of the compilation that is shipped on the compiled url

- resources: list of resources that are going to be loaded


Decide which bundles are rendered on a specific call
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. One bundle can be enabled or disabled by default.

2. An expression on the bundles enabled to evaluate if it should be used when its enabled on a specific context.

3. The diazo theme can enable or disable on top a specific bundle (no matter if its disabled by default)

4. A browser page can force to load or unload a specific bundle (no matter if its disabled by default)


Compiled bundles
^^^^^^^^^^^^^^^^

In a compiled bundle normaly there is only one resource that is going to be loaded for each specific bundle, this resource will be
a js with a requirejs wrapper and a less file.

When the site is in development mode the files are delivered as they are on stored and will get its dependencies asyncronous (AMD-LESS).

The main feature of the compiled bundles is that the list of real resources that are going to be loaded on the site are defined on the js and less files.

Example::

    plone.js

    require([
      'jquery',
      'mockup-registry',
      'mockup-patterns-base',
      'mockup-patterns-select2',
      'mockup-patterns-pickadate',
      'mockup-patterns-relateditems',
      'mockup-patterns-querystring',
      'mockup-patterns-tinymce',
      'plone-patterns-toolbar',
      'mockup-patterns-accessibility',
      'mockup-patterns-autotoc',
      'mockup-patterns-cookietrigger',
      'mockup-patterns-formunloadalert',
      'mockup-patterns-preventdoublesubmit',
      'mockup-patterns-inlinevalidation',
      'mockup-patterns-formautofocus',
      'mockup-patterns-modal',
      'mockup-patterns-structure',
      'bootstrap-dropdown',
      'bootstrap-collapse',
      'bootstrap-tooltip'
    ], function($, Registry, Base) {
    ...

    plone.less

    ...
    @import url("@{mockup-patterns-select2}");
    @import url("@{mockup-patterns-pickadate}");
    @import url("@{mockup-patterns-relateditems}");
    @import url("@{mockup-patterns-querystring}");
    @import url("@{mockup-patterns-autotoc}");
    @import url("@{mockup-patterns-modal}");
    @import url("@{mockup-patterns-structure}");
    @import url("@{mockup-patterns-upload}");
    @import url("@{plone-patterns-toolbar}");
    @import url("@{mockup-patterns-tinymce}");
    ...

On development mode all the less/js resources are going to be retrived on live so its possible to debug
and modify the filesystem files and see the result on the fly.

In order to provide a compiled version for the production mode there are three possiblities:

- Compile TTW and store on the ZODB (explained later)

- Compile with a generated guntfile: There is a python scripts that extracts all the information from an existing plone and generates a gruntfile - https://github.com/plone/buildout.coredev/blob/5.0/generate_gruntfile.py

- Create your own compilation chain: Using the tool you prefer create a compiled version of your bundle with the correct urls.


Non compiled bundles
^^^^^^^^^^^^^^^^^^^^

In case your resources are not using requirejs/less and you just want to group them on bundles to minimize and deliver them in groups you can use
the non compiled bundles. 

They are minimized and stored on the csscompiled/jscompiled url defined on the bundle for the first request each time:

- its on production mode

- a package with jsregistry/cssregistry is installed

You can also force to create a new minimized version TTW.

Example::

  <records prefix="plone.bundles/plone-legacy"
            interface='Products.CMFPlone.interfaces.IBundleRegistry'>
    <value key="resources" purge="false">
      <element>plone_javascript_variables</element>
      <element>unlockOnFormUnload</element>
      <element>table_sorter</element>
      <element>inline-validation</element>
      <element>jquery-highlightsearchterms</element>
    </value>
    <value key="depends">plone</value>
    <value key="jscompilation">++plone++static/plone-legacy-compiled.js</value>
    <value key="csscompilation">++plone++static/plone-legacy-compiled.css</value>
    <value key="last_compilation">2014-08-14 00:00:00</value>
    <value key="compile">False</value>
    <value key="enabled">True</value>
  </records>


Default Plone bundles
^^^^^^^^^^^^^^^^^^^^^

There are two main plone bundles by default: plone and plone-legacy.

- plone bundle : is a compiled bundle with the main components required to run the toolbar and main mockup patterns with only the css needed by that elements

- plone legacy bundle : is a non compiled bundle that gets all the jsregistry and cssregistry that are loaded on the addons that are installed so they are minified


Diazo Bundles
^^^^^^^^^^^^^

Diazo enables us to define a static theme outside Plone with its own resources and its own compiling system.

In order to allow to have a complete theme its possible to define a bundle in diazo in the manifest::

    barceloneta/theme/manifest.cf

    enabled-bundles =
    disabled-bundles =

    development-css = /++theme++barceloneta/less/barceloneta.plone.less
    production-css = /++theme++barceloneta/less/barceloneta-compiled.css
    tinymce-content-css = /++theme++barceloneta/less/barceloneta-compiled.css

    development-js = 
    production-js = 

This options allow us to define to plone that the js/css renderer will add the diazo one so we will be able to overwrite the 
<link> <script> tags from the theme with the plone ones loading the diazo resources.

As on the native plone bundles its possible to define a development/production set (less/requirejs) so it integrates with the
resource compilation system in plone.

The options are :

- enabled-bundles / disabled-bundles : list of bundles that should be added or disabled when we are rendering throw that diazo theme

- development-css / development-js : less file and requirejs file that should be used on the compilation on browser system

- production-css / production-js : compiled versions that should be delivered on production. There is no aid system to compile them, you can compile it with you prefered system.

- tinymce-content-css : css version of the tinymce component, an exception to define the css on the tinymce


Diazo frontend - barceloneta backend
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using diazo rules you can define a frontend and a backend separatelly defining which bundles you want to load.

TODO


Browser Page bundle
^^^^^^^^^^^^^^^^^^^

If you want that your browser page loads or unloads an specific bundle when its rendered you can use::

TODO


Development vs Production
-------------------------

TODO


Resource registry controlpanel - TTW edit / compilation / overwrite
-------------------------------------------------------------------

TODO

Plone resources/bundles
^^^^^^^^^^^^^^^^^^^^^^^

Diazo themes
^^^^^^^^^^^


Old registry migration and compatibility
----------------------------------------

TODO

