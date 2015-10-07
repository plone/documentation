===============================
JS/CSS Resources
===============================

.. admonition:: Description

    Resources are JavaScript, CSS or LESS resources and their dependencies.
    They add frontend logic and design to Plone.
    There are many different areas where resources are used - like widgets, design styles, behavior logic and single page apps.
    In order to organize them we are using two main standard technologies: require.js and Less.

    The goal of this recipe is to help you confirm that everything is working.

.. contents:: :local:


Introduction to Plone 5 resources
---------------------------------

Plone 5 introduces new concepts, for some, with working with JavaScript and CSS in Plone.
Plone 5 utilizes Asynchronous Module Definition (AMD) with requirejs.
We chose AMD over other module loading implementations(like commonjs) because AMD can be used in non-compiled form in the browser.
This way, someone can click "development mode" in the resource registry control panel and work with the non-compiled JavaScript files directly.

Additionally, Plone 5 streamlines the use of LESS to compile CSS.

These two concepts for JavaScript and CSS are merged into one idea--a resource.


Resources
---------

Resources are the main unit of the resource registry.
A resource consists of a JavaScript file and/or some CSS/Less files.
A resource is identified by a name.

Since this can be a single JavaScript file, there are additional RequireJS options available to be able to customize.
Possible options we have are is shim (export, init and depends) so it can be configured to be exported to the global namespace, init on load and depend on some other resource.

An example of a resource definition on registry.xml:

.. code-block:: xml

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


The possible options of a resource are:

- js : URL of the JavaScript file

- css: List of CSS/Less elements.

- url: Base URL for loading additional resources like text files. See below for an example.


These are the "Shim" options for a resource, where older, non-RequireJS compatible JavaScript code is used. For more information see: http://requirejs.org/docs/api.html#config-shim

- export: Shim export option to define a global variable to where the JavaScript module should be made available.

- depends: Shim depends option to define which other RequireJS resources should be loaded before this shim module.

- init: Shim init option to define some JavaScript code to be run on initialization.


The URL option allows you to define the base url for loading text resources like XML templates.
See the following for an example:

In registry.xml:

.. code-block:: xml

    <records prefix="plone.resources/mockup-patterns-structure"
            interface='Products.CMFPlone.interfaces.IResourceRegistry'>
        <value key="js">++resource++mockup/structure/pattern.js</value>
        <value key="url">++resource++mockup/structure</value>
        <value key="css">
            <element>++resource++mockup/structure/less/pattern.structure.less</element>
        </value>
    </records>


In mockup/patterns/structure/js/views/actionmenu.js::

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
In order to avoid running bower install on each installation of Plone it ships by default a minimal bower components folder on the CMFPlone static folder with the correct versions of the resources that are need to run the default plone js/css.

Plone's default bower components are defined here:

https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/static/bower.json

Plone's resource registration is defined here:

https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/profiles/dependencies/registry.xml


The ++plone++ traversal namespace
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a specific folder type called ++plone++ designed to be similar to ++theme++ but with the difference that you can overwrite an specific file, so its possible to edit a resource TTW.

Example:

.. code-block:: xml

    <plone:static
        directory="static"
        type="plone"
        name="myresources"
        />

This allows you to access resources in this directory by using the URL path ``++plone++myresources/``.


Bundle
------

Bundles are groups of resources that are going to be loaded on your Plone site.
Instead of loading single resources, bundles allow you to group, combine and minify resources and reduce the number of web requests and the responses payload.

In case you develop a specific add-on you might want to create your own bundle.
Alternatively, you can register your add-on code to be included in Plone's default ``plone`` bundle.

For single pages like the theming controlpanel, you can define a customized bundle with only the resources needed for that page.

In development mode, each bundle includes their resources in the rendered site as individual resource with individual requests. This can lead to a lot of requests and high response times.

For production sites, the development mode has to be disabled and all bundles must be compiled.
This can be done Through-The-Web in the resource editor.
There is only one JavaScript and one CSS file included in the output per active bundle.


.. note::

    A bundle can depend on another.
    This is mainly used for the order of inclusion in the rendered content.
    Currently, it doesn't hook in the require js dependency mechanism.
    This means, each bundle gets all their dependencies compiled in, which raise the response payload unnecessarily.
    To avoid this, add your resources to existing bundles, like the "plone" bundle.


Examples:

.. code-block:: xml

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


The possible options of a bundle are:

- enabled: Enable of disable the bundle.

- depends: Dependency on another bundle.

- resources: List of resources that are included in this bundle.

- compile: Compilation is necessary, if the bundle has any Less or RequireJS resources.

- expression: Python expression for conditional inclusion.

- conditionalcomment: Conditional Comment for Internet Explorer hacks.


The following are for pre-compiled bundles and are automatically set, when the bundle is build Through-The-Web:

- jscompilation: URL of the compiled and minified JS file.

- csscompilation: URL of the compiled and minified CSS file.

- last_compilation: Date of the last compilation time.


Decide which bundles are rendered on a specific call
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. One bundle can be enabled or disabled by default.

2. An expression on the bundles enabled to evaluate if it should be used when its enabled on a specific context.

3. The diazo theme can enable or disable on top a specific bundle (no matter if its disabled by default)

4. A browser page can force to load or unload a specific bundle (no matter if its disabled by default)


Compiled bundles
^^^^^^^^^^^^^^^^

In a compiled bundle normally there is only one resource that is going to be loaded for each specific bundle, this resource will be a JavaScript file with a requirejs wrapper and a less file.

When the site is in development mode the files are delivered as they are on stored and will get its dependencies asynchronously (AMD and LESS).

The main feature of the compiled bundles is that the list of real resources that are going to be loaded on the site are defined on the JavaScript and LESS files.

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

On development mode all the less/js resources are going to be retrieved on live so its possible to debug and modify the filesystem files and see the result on the fly.

In order to provide a compiled version for the production mode there are three possibilities:

- Compile TTW and store on the ZODB (explained later)

- Compile with a generated gruntfile: ``./bin/plone-compile-resources --site-id=myplonesite --bundle=mybundle``

- Create your own compilation chain: Using the tool you prefer create a compiled version of your bundle with the correct urls.


Non compiled bundles
^^^^^^^^^^^^^^^^^^^^

In case your resources are not using Requirejs/Less and you just want to group them on bundles to minimize and deliver them in groups you can use the non compiled bundles.

They are minimized and stored on the csscompiled/jscompiled URL defined on the bundle for the first request each time:

- its on production mode

- a package with jsregistry/cssregistry is installed

You can also force to create a new minimized version TTW.

Example:

.. code-block:: xml

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

There are three main plone bundles by default: plone and plone-legacy.

- plone bundle : is a compiled bundle with the main components required to run the toolbar and main mockup patterns with only the css needed by that elements

- plone logged in bundle : is a compiled bundle that is only included for logged in users

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

This options allow us to define to plone that the js/css renderer will add the diazo one so we will be able to overwrite the <link> <script> tags from the theme with the plone ones loading the diazo resources.

As on the native plone bundles its possible to define a development/production set (less/requirejs) so it integrates with the resource compilation system in plone.

The options are :

- enabled-bundles / disabled-bundles : list of bundles that should be added or disabled when we are rendering throw that diazo theme

- development-css / development-js : less file and requirejs file that should be used on the compilation on browser system

- production-css / production-js : compiled versions that should be delivered on production. There is no aid system to compile them, you can compile it with you prefered system.

- tinymce-content-css : css version of the tinymce component, an exception to define the css on the tinymce


Diazo frontend - barceloneta backend
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using diazo rules you can theme the frontend of your site how you like, and use the default Barceloneta theme for the backend.

Example:

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

            <!-- Include basic plone/toolbar bundles -->
            <after css:theme-children="head" css:content="head link[data-bundle='basic'], head link[data-bundle='plone'], head link[data-bundle='plone-logged-in'], head link[data-bundle='diazo']" />
            <after css:theme-children="head" css:content="head script[data-bundle='basic'], head script[data-bundle='plone'], head script[data-bundle='plone-logged-in'], script link[data-bundle='diazo']" />

            <!-- Insert the toolbar -->
            <before css:theme-children="body" css:content-children="#edit-bar" css:if-not-content=".ajax_load" css:if-content=".userrole-authenticated" />

            <!-- Your diazo front end rules go here -->

        </rules>
    </rules>

You can define your own diazo bundle in your manifest.cfg (by using development-js, production-js and css options). This diazo bundle will not be included in the backend theme.


Browser Page bundle
^^^^^^^^^^^^^^^^^^^

If you want that your browser page loads or unloads an specific bundle when its rendered you can use:

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
^^^^^^^^^^^^

TODO

Old registry migration and compatibility
----------------------------------------

The deprecated resource registries(and portal_javascripts) has no concept of dependency management.
It simply allowed you to specify an order in which JavaScript files should be included on your site.
It also would combined and minify them for you in deployment mode.

Prior to Plone 5, JavaScript files were added to the registry by using a Generic Setup Profile and including a jsregistry.xml file to it.
This would add your JavaScript to the registry, with some options and potentially set ordering.

In Plone 5.0, Plone will still recognize these jsregistry.xml files.
Plone tries to provide a shim for those that are stubborn to migrate.
How it does this is by adding all jsregistry.xml JavaScripts into a "plone-legacy" Resource Registry bundle.
This bundle simply includes a global jQuery object and includes the resources in sequential order after it.


Updating non-AMD scripts
^^^^^^^^^^^^^^^^^^^^^^^^

If you are not including your JavaScript in the Resource Registries and just need it to work alongside Plone's JavaScript because you're manually including the JavaScript files in one way or another(page templates, themes), there are a number of techniques available to read on the web that describe how to make your scripts conditionally work with AMD.

For the sake of this post, I will describe one technique used in Plone core to fix the JavaScript.
The change we'll be investigating can be seen with in a commit to plone.app.registry.
plone.app.registry has a control panel that allows some ajax searching and modals for editing settings.

To utilize the dependency management that AMD provides and have the javascript depend on jQuery, we can wrap the script in an AMD require function. This function allows you to define a set of dependencies and a function that takes as arguments, those dependencies you defined. After the dependencies are loaded, the function you defined is called.

Example::


      require([
        'jquery',
        'pat-registry'
      ], function($, Registry) {
        'use strict';
        ...
        // All my previous JavaScript file code here
        ...
      });


requirejs require/define and resource/bundle
--------------------------------------------

In working with requirejs, you'll likely be aware of the `mismatched anonymous define() <http://requirejs.org/docs/errors.html#mismatch>`_ potential misuse of require and define.

Basically, it comes down to, you should not use `define` with script tags.
`define` should only be included in a page by using a `require` call.

How this works with resources and bundles is that bundles should ONLY ever be 'require' calls.
If you try to use a JavaScript file that has a `define` call with a bundle, you'll get the previously mentioned error.
Make sure to use a JavaScript file with a 'require' call to include all your `define` resources.

This is how requirejs works and is normal behavior; however, any novice will likely come around to noticing this when working with AMD JavaScript.
With Plone, it's one additional caveat you'll need to be aware of when working with the Resource Registry.

Including non-requirejs scripts with Plone
------------------------------------------

If you have scripts that cannot be updated to use requirejs, it may be possible to include both.

After the Plone scripts, you can unset the require and define variables which should allow your scripts to run normally.

Example:

.. code-block:: xml

      <!-- Plone bundles here -->
      <script>
        require = undefined
        define = undefined
      </script>
      <script>
        // Your javascript here
      </script>

You can add the Plone resources to your theme before your own javascript.

Example:

.. code-block:: xml

      <before theme="/html/head/script[1]">
          <xsl:apply-templates select="/html/head/script" />
          <script>
              require = undefined
              define = undefined
          </script>
      </before>
