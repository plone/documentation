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


Introduction to Plone 5 resources
---------------------------------

Plone 5 introduces new concepts, for some, with working with JavaScript and CSS in Plone.
Plone 5 utilizes Asynchronous Module Definition (AMD) with requirejs. We chose AMD
over other module loading implementations(like commonjs) because AMD can be used in
non-compiled form in the browser. This way, someone can click "development mode"
in the resource registry control panel and work with the non-compiled JavaScript files directly.

Additionally, Plone 5 streamlines the use of LESS to compile CSS.

These two concepts for JavaScript and CSS are merged into one idea--a resource.


Resources
---------

The main unit of the resource system is a JavaScript file and/or a set of CSS/LESS files.

Since this can be a single JavaScript file, there are additional requirejs
options are available to be able to customize. Possible options we have are
is shim (export, init and depends) so it can be configured to be exported 
o the global namespace, init on load and depend on some other resource.

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

- js : URL of the JavaScript file

- export : shim export option

- init : shim init option

- depends : shim depends option

- css : list of LESS/CS elements

- url : URL that will be defined on the require.js namespace as the resource-url variable

The export/init/depends are the shim option to load the js files in the correct order on the global namespace, for more information : http://requirejs.org/docs/api.html#config-shim

The URL option will you to define the base url in case you want to load txt resources on require js::
        
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
      name="myresources"
      />

will give you ++plone++myresources based urls


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

- compile: the bundle has less/requirejs and needs to be compiled

- jscompilation: URL where the minimized/compiled JavaScript version will be

- csscompilation: URL where the minimized/compiled CSS version will be 

- last_compilation: date of the compilation that is shipped on the compiled URL

- resources: list of resources that are going to be loaded


Decide which bundles are rendered on a specific call
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. One bundle can be enabled or disabled by default.

2. An expression on the bundles enabled to evaluate if it should be used when its enabled on a specific context.

3. The diazo theme can enable or disable on top a specific bundle (no matter if its disabled by default)

4. A browser page can force to load or unload a specific bundle (no matter if its disabled by default)


Compiled bundles
^^^^^^^^^^^^^^^^

In a compiled bundle normally there is only one resource that is going to be loaded for each specific
bundle, this resource will be a JavaScript file with a requirejs wrapper and a less file.

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

On development mode all the less/js resources are going to be retrieved on live so its possible to debug
and modify the filesystem files and see the result on the fly.

In order to provide a compiled version for the production mode there are three possibilities:

- Compile TTW and store on the ZODB (explained later)

- Compile with a generated gruntfile: ./bin/plone-compile-resources --site-id=myplonesite --bundle=mybundle

- Create your own compilation chain: Using the tool you prefer create a compiled version of your bundle with the correct urls.


Non compiled bundles
^^^^^^^^^^^^^^^^^^^^

In case your resources are not using requirejs/less and you just want to group them on bundles to minimize and deliver them in groups you can use
the non compiled bundles. 

They are minimized and stored on the csscompiled/jscompiled URL defined on the bundle for the first request each time:

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
^^^^^^^^^^^^

TODO

Old registry migration and compatibility
----------------------------------------

The deprecated resource registries(and portal_javascripts) has no concept of
dependency management. It simply allowed you to specify an order in which
JavaScript files should be included on your site. It also would combined and
minify them for you in deployment mode.

Prior to Plone 5, JavaScript files were added to the registry by using a Generic
Setup Profile and including a jsregistry.xml file to it. This would add your
JavaScript to the registry, with some options and potentially set ordering.

In Plone 5.0, Plone will still recognize these jsregistry.xml files. Plone
tries to provide a shim for those that are stubborn to migrate. How it does
this is by adding all jsregistry.xml JavaScripts into a "plone-legacy" Resource
Registry bundle. This bundle simply includes a global jQuery object and
includes the resources in sequential order after it.


Updating non-AMD scripts
^^^^^^^^^^^^^^^^^^^^^^^^

If you are not including your JavaScript in the Resource Registries and just
need it to work alongside Plone's JavaScript because you're manually including
the JavaScript files in one way or another(page templates, themes), there are
a number of techniques available to read on the web that describe how to make
your scripts conditionally work with AMD.

For the sake of this post, I will describe one technique used in Plone core to
fix the JavaScript. The change we'll be investigating can be seen with in a commit
to plone.app.registry. plone.app.registry has a control panel that allows some
ajax searching and modals for editing settings.

To utilize the dependency management that AMD provides and have the javascript
depend on jQuery, we can wrap the script in an AMD require function. This function
allows you to define a set of dependencies and a function that takes as arguments,
those dependencies you defined. After the dependencies are loaded, the function
you defined is called.

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

In working with requirejs, you'll likely be aware of the 
`mismatched anonymous define() <http://requirejs.org/docs/errors.html#mismatch>`_
potential misuse of require and define.

Basically, it comes down to, you should not use `define` with script tags. `define`
should only be included in a page by using a `require` call.

How this works with resources and bundles is that bundles should ONLY ever be
'require' calls. If you try to use a JavaScript file that has a `define` call
with a bundle, you'll get the previously mentioned error. Make sure to use
a JavaScript file with a 'require' call to include all your `define` resources.

This is how requirejs works and is normal behavior; however, any novice will likely
come around to noticing this when working with AMD JavaScript. With Plone,
it's one additional caveat you'll need to be aware of when working with the Resource
Registry.