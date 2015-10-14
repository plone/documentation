=========================
Plone 5 Resource Registry
=========================

.. admonition:: Description

    For JavaScript and CSS development, Plone 5 makes extensive use of tools like Bower, Grunt, RequireJS and Less for an optimized development process.
    The JavaScript and CSS resources are managed in the Resource Registry.
    The Resource Registry was completly rewritten in Plone 5 to support the new dependency based RequireJS approach.
    It also allows us to build Less and RequireJS bundles Through-The-Web for a low entry barrier.
    This chapter should give you a good understanding of the new Resource Registry.

.. contents:: :local:


Introduction to Plone 5 resources
=================================

Plone 5 introduces new concepts for working with JavaScript and CSS in Plone.

We finally have a solution to define JavaScript modules and their dependencies - in contrast of the previous approach, where all dependencies had to be loaded in order.
We achieve that with the tool RequireJS, which follows the Asynchronous Module Definition (AMD) approach.
We chose AMD over other module loading implementations(like CommonJS) because AMD can be used in non-compiled form in the browser and also compiled Through-The-Web.
This way, we can also support a "development mode" like in Plone versions prior to 5, where changes in the JavaScript sources are instantly reflected.

CSS can be developed with the CSS compiler Less.
Who ever worked with Less probably don't want to edit CSS directly - especially for bigger projects. Less gives us a lot of nice features like inheritance, scoping, functions, mixins and variables, which are not available in pure CSS.
Again, the availability of a JavaScript based compiler made a good reason to choose Less over Sass.

Our concept of a resource is made of a JavaScript and/or some Less or CSS files.


Resources
=========

Resources are the main unit of the resource registry.
A resource consists of a JavaScript file and/or some CSS/Less files.
A resource is identified by RequireJS via a name.

Resources - as well as bundles - are configured by using ``plone.registry``.
From the resource configuration a RequireJS configuration is build to compile
bundles.
Like in RequireJS, we can also include non-module, legacy resources, which do not make use of the RequireJS ``define`` and ``require`` methods.
For this, the "shim" options are available, as explained below.

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

js
    URL of the JavaScript file

css
    List of CSS/Less elements.

url
    Base URL for loading additional resources like text files.
    See below for an example.


These are the "Shim" options for a resource to support JavaScript code, which doesn't define modules or dependencies.
We call them "legacy" JavaScript code, as it doesn't follow our proposed best practices.
For more information see: http://requirejs.org/docs/api.html#config-shim

export
    Shim export option to define a global variable to where the JavaScript module should be made available.
depends
    Shim depends option to define which other RequireJS resources should be loaded before this shim module.
init
    Shim init option to define some JavaScript code to be run on initialization.


The URL option allows you to define the base url for loading text resources like XML templates.
See the following for an example:

In ``registry.xml``:

.. code-block:: xml

    <records prefix="plone.resources/mockup-patterns-structure"
            interface='Products.CMFPlone.interfaces.IResourceRegistry'>
        <value key="js">++resource++mockup/structure/pattern.js</value>
        <value key="url">++resource++mockup/structure</value>
        <value key="css">
            <element>++resource++mockup/structure/less/pattern.structure.less</element>
        </value>
    </records>


In ``mockup/patterns/structure/js/views/actionmenu.js``:

.. code-block:: js

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

    // ...
    });
    return ActionMenu;
    });

Default resources on Plone
--------------------------

Plone 5 ships with a list of Mockup- and Bower components for Plone 5's new
UI.
These resources can be found in the static folder (``Products.CMFPlone.static``), where you can also find the `bower.json <https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/static/bower.json>`_ file.
The resources are preconfigured in the registry (`registry.xml <https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/profiles/dependencies/registry.xml>`_ in ``Products.CMFPlone.profiles.dependencies``).


The ++plone++static traversal namespace
---------------------------------------

We have a new ``plone.resource`` based traversal namespace called ``++plone++static``.
It points to the ``Products.CMFPlone.static`` folder.
The interesting thing with Plone.resource based resources is, that they can be stored in the ZODB (where they are looked up first, by default) or in the filesystem.
This allows us to customize filesystem based resources Through-The-Web.

This is how the ``++plone++static`` directory resource is configured:

.. code-block:: xml

    <plone:static
        directory="static"
        type="plone"
        name="static"
        />

Now we can access the contents within the "static" folder by using the URL part ``++plone++myresources/`` and append the path to the resource under "static".

.. note::

    When providing static resources (JavaScript/Less/CSS) for Plone 5's resource registry, use ``plone.resource`` based resources instead of Zope's browser resources. The latter are cached heavily and you won't get your changes compiled into bundles, even after Zope restarts.


Bundles
=======

A bundle is a set of resources.
Bundles can group resources for different purposes - like the "plone" bundle for all users or "plone-logged-in" for only logged in users.
Only bundles are loaded in a Plone site (well - there is an exception.
You can register individual resources to be loaded for a specific request via an API method.
More on this later).

For production environments you will want to compile your bundles and combine and minify all the necessary resources including their dependencies (which are now well defined) into a single JavaScript and CSS file.
This minimizes the number of web requests and the payload of data send over the network.
In Production mode, only one or two files are included in the output: a JavaScript and a CSS file.

In development mode, each bundle includes all of their resources in the rendered site as individual resource with individual requests.
This can lead to a lot of requests and high response times, though the RequireJS loads its dependencies asynchronously.
In development mode, modifications to the resources are instantly reflected without the need to compile a bundle beforehand.

When developing an add-on you might want to create your own bundle Alternatively, you can register your add-on code to be included in Plone's default ``plone`` bundle.

If you need a bundle for a single page, you can define an extra bundle and only include it there. The ``resourceregistry`` bundle for example is only used for the ``@@resourceregistry-controlpanel`` view. (see the section `Adding or removing bundles from a request`_ for more information)

.. note::

    A bundle can depend on another one.
    This is mainly used for the order of inclusion in the rendered content and mostly relevant for legacy bundles.
    Currently, bundle dependencies don't make use of RequireJS dependencies.
    This means, each bundle gets all of their dependencies compiled in, even if it was already used for another bundle.
    This raises the response payload unnecessarily.
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


The possible options for a bundle are:

- enabled: Enable or disable the bundle.

- depends: Dependency on another bundle.

- resources: List of resources that are included in this bundle.

- compile: Compilation is necessary, if the bundle has any Less or RequireJS resources.
  Set to false, if compilation should not be done.
  Then this bundle can be combined with any other non-compilable bundles.

- expression: TALES expression for conditional inclusion.

- conditionalcomment: Conditional Comment for Internet Explorer hacks.


The following are for pre-compiled bundles and are automatically set, when the bundle is build Through-The-Web:

- jscompilation: URL of the compiled and minified JavaScript file.

- csscompilation: URL of the compiled and minified CSS file.

- last_compilation: Date of the last compilation time.


Bundle compilation
------------------

In order to provide a compiled version for the production mode there are three possibilities:

- Compile Through-The-Web and store on the ZODB.
  This is done via the resource control panel.

- Compile with a generated Grunt file: ``./bin/plone-compile-resources --site-id=myplonesite --bundle=mybundle``

- Create your own compilation chain: Using the tool you prefer create a compiled version of your bundle with the correct URLs.


Default Plone bundles
---------------------

There are three main Plone bundles by default:

- plone: This is the main compiled bundle with all the JavaScript and CSS components required for the Plone Toolbar and the main Mockup patterns.

- plone-logged-in: This one is only included for logged in users and contains patterns like the "tinymce" pattern, the "querystring" pattern for collection edit forms and others.

- plone-legacy: This one is a non compiled bundle with code, that doesn't use RequireJS and Less.
  Also, Addons which install resources to ``portal_javascripts`` or ``portal_css`` are registered as resources in the plone-legacy bundle automatically.


The legacy bundle
-----------------

Code which cannot migrated to use RequireJS or uses RequireJS in a way, which is incompatible with Plone's use of it (e.g. it is using its own RequireJS setup) can be included in the legacy bundle.

.. note::

    Some JavaScript uses its own setup of RequireJS.
    Others - like Leaflet 0.7 or DataTables 1.10 - try to register themselves for RequireJS which lead to the infamous "mismatched anonymous define" errors (see below).
    You can register those scripts in the legacy bundle.
    The ``define`` and ``require`` methods are unset before these scripts are included in the output and reset again after all scripts have been included.
    See yourself: https://github.com/plone/Products.CMFPlone/pull/870/files

Resources, which are registered into ``portal_javascripts`` or ``portal_css`` registries via an addon are automatically registered in the legacy bundle and cleared from ``portal_javascripts`` and ``portal_css``.

.. note::

    JavaScript, which doesn't use RequireJS can still be managed by it by including it and configuring shim options for it.

The resources of non-compiled bundles are all combined and minified.

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


Adding or removing bundles from a request
-----------------------------------------

Besides of using the bundle options ``enabled`` and ``expression``, where you can globally or conditionally control the inclusion of bundles you also have these options:

- Controlling via Diazo: Diazo include or exclude specific bundles, no matter if its disabled by default.
  This can be done in the theme's ``manifest.cfg`` file via the options ``enabled-bundles`` and ``disabled-bundles``.
  Those options get a comma separated list of bundle names (TODO: verify "comma separated list").

- A browser page can include or exclude a specific bundle by using the API methods from ``Products.CMFPlone.resources``, no matter if its disabled by default.

These are the ``Products.CMFPlone.resources`` API methods:

- ``add_bundle_on_request(request, bundle)``: Add a bundle to the current request by specifying its name.

- ``remove_bundle_on_request(request, bundle)``: Remove a bundle to the current request by specifying its name.

- ``add_resource_on_request(request, bundle)``: Add an individual resource to the current request by specifying its name.


Diazo Bundles
=============

The point with Diazo is to create standalone static themes which work without Plone.
Diazo themes can use - and will use -their own resources and compiling systems.

Diazo was extended to support bundles.
Bundles can be defined in the theme ``barceloneta/theme/manifest.cfg`` file::

    enabled-bundles =
    disabled-bundles =

    development-css = /++theme++barceloneta/less/barceloneta.plone.less
    production-css = /++theme++barceloneta/less/barceloneta-compiled.css
    tinymce-content-css = /++theme++barceloneta/less/barceloneta-compiled.css

    development-js =
    production-js =

The configured bundles in the ``manifest.cfg`` file are included in the output by the renderer additionally to the ones registered in the resource registry.
This allows us to just overwrite or drop the ``link`` and ``script`` tags from the theme but still include the theme-specific resources without having them to register in the resource registry.

The options are:

- enabled-bundles / disabled-bundles: List of bundles that should be added or disabled when rendering the Diazo theme.

- development-css / development-js: Uncompiled/unminified Less/CSS file and RequireJS file, which should be included in development environments.
  The compilation is done on the browser side on the fly.

- production-css / production-js: Compiled bundles that should be included in production mode.

- tinymce-content-css: CSS file to include for the TinyMCE editor, so that TinyMCE gives you a best possible WYSIWYG experience.

.. note::

    You have to use your own compilation environment to compile the Diazo bundles.
    This cannot be done via the Resouce Registry or the ``plone-compile-resources`` script.


Migrating older code to the new resource registry
=================================================

Old registry migration and compatibility
----------------------------------------

The deprecated resource registries ``portal_css`` and ``portal_javascripts`` have no concept of dependency management.
They simply allowed you to specify an order in which JavaScript and CSS files should be included the rendered site.
Of course it was combined and minified for production mode, which was very handy.
But even here the order did matter a lot.
If there were conditional include statements per resource in the middle of the ordered resources, Plone had to split up the merged resources in separate ones which immediately generated additional requests.

The old way to add these resources to the registry was by registering them with Generic Setup using ``jsregistry.xml`` and ``cssregistry.xml`` profile files.

In Plone 5.0, Plone will still recognize these ``jsregistry.xml`` and ``cssregistry.xml`` files.
Plone tries to provide a shim for those that are stubborn to migrate.

Plone does this by adding all ``jsregistry.xml`` JavaScripts and ``cssregistry.xml`` CSS into a "plone-legacy" Resource Registry bundle.

This bundle simply includes a global jQuery object and includes the resources in sequential order after it.


Updating non-AMD scripts
------------------------

Updating your existing JavaScript files to make use of RequireJS should be quite easy.
Just wrap your code into the recipe shown below.
You can define any dependencies via its RequireJS name identifier.
Those dependencies are injected into the anonymous function, which follows the dependency list, like shown for jQuery.

Example:

.. code-block:: javascript

      require([
        'jquery'
      ], function($) {
        'use strict';
        ...
        // All my previous JavaScript file code here
        ...
      });

Then you need to register this resource in the resource registry and add it to a bundle as described above.

.. note::

    When using ``require`` instead of ``define``, the anonymous function is immediately called.
    If you would use ``define`` instead, you'd have to make a ``require`` call somewhere, with the dependency to your resource.


Usage of ``define`` and ``require`` and the ``mismatched anonymous define`` error
---------------------------------------------------------------------------------

When working with RequireJS, you'll likely be aware of the `mismatched anonymous define() <http://requirejs.org/docs/errors.html#mismatch>`_ potential misuse of require and define.

Basically it comes down to, that you should not use ``define`` with script tags - code that is rendered without being loaded via RequireJS ``require`` calls.
``define`` should only be included in a page by using a ``require`` call.

Applied to the concept of resources and bundles this means, that bundles should _only_ ever be ``require`` calls.
If you try to use a JavaScript file that has a ``define`` call with a bundle, you'll likely get the previously mentioned error.
Make sure to use a JavaScript file with a ``require`` call to include all your ``define`` resources.

This is just how RequireJS works and is normal behavior.
Being aware of this saves you some headache.


Including non-RequireJS scripts in a Diazo theme
------------------------------------------------

We already described how to add resources to the legacy bundle and that the legacy bundle unsets the ``define`` and ``require`` statements.

If you have scripts in your Diazo theme, that you just don't want to register with the resource registry and which are not compatible with RequireJS, you can add those below the Plone scripts and unset ``define`` and ``require`` yourself.

Example:

.. code-block:: xml

      <before theme="/html/head/script[1]">    <!-- ... before your own scripts -->
          <xsl:apply-templates select="/html/head/script" />    <!-- include the Plone scripts -->
          <script>    <!-- and unset require and define -->
              require = undefined
              define = undefined
          </script>
      </before>
