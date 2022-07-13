=================
Resource Registry
=================

.. admonition:: Description

    Plone 5 has modernized the JavaScript and CSS development experience by incorporating tools like Bower, Grunt, RequireJS and Less.
    JavaScript and CSS resources for core Plone and add-on packages are managed in the new Plone 5 Resource Registry.

    The Resource Registry was completely rewritten in Plone 5 to support a new dependency-based approach built on RequireJS.
    It also allows developers to create JavaScript and CSS bundles Through-The-Web for a low barrier to entry.

    This chapter will help you to gain a basic understanding of the new Resource Registry.



Introduction To Plone 5 Resources
=================================

Plone 5 introduces new concepts for working with JavaScript and CSS in Plone.

JavaScript And AMD
------------------

Prior to Plone 5, JavaScript resources in Plone have been registered with the ``portal_javascripts`` tool using the Generic Setup import step ``jsregistry.xml``.
This approach allowed a developer to specify the order in which individual JavaScript resources were loaded into an HTML page, and controlled compiling and minifying these resources for production into a minimal set of files.

As the use of JavaScript in front-end development expanded, this model proved insufficient to solve complex dependency management issues.
At the same time, developments in the JavaScript community led to a new approach to handling complex dependencies.

Starting in Plone 5, we use a new `module <http://requirejs.org/docs/why.html>`_-based solution on the `Asynchronous Module Definition <http://requirejs.org/docs/whyamd.html>`_ (AMD) approach.

The new Plone 5 Resource Registry uses `RequireJS <http://requirejs.org/>`_ to allow developers to define individual JavaScript modules and the dependencies they will require.

Because RequireJS uses the AMD approach, these modules and their dependencies can be served in an uncompiled form during development and then compiled and minified Through-The-Web for use in production.
This allows a "development mode" where changes in JavaScript source files are reflected in the browser in near real-time.

It is also possible in the new Resource Registry to provide bundles with simple JavaScript that does not make use of AMD.
See :ref:`bundle_example_non_amd` below for an example of such a bundle.

CSS And Less
------------

Modern web development relies on CSS (Cascading Style Sheets).
To support complex CSS, "preprocessors" have developed that allow a more programmatic way of defining styles and sharing common elements.

Plone 5 has chosen to use the `Less CSS preprocessor <http://lesscss.org/>`_ because it is compiled by JavaScript tools, which fit with the new Plone Resource Registry.

Less provides nice features like inheritance, scoping, functions, mixins and variables, which are not available in pure CSS.


Resources And Bundles
---------------------

In the Plone 5 Resource Registry, JavaScript and CSS are organized into :ref:`resources <resource_registry_resources>` and :ref:`bundles <resource_registry_bundles>`.
A resource consists of one JavaScript and either none, one or multiple Less or CSS files.
A bundle combines several resources into a single unit that is used in a webpage.

In "development mode" the resources for a bundle may be served individually and unminified to facilitate development.
In "production mode" a bundle's resources are compiled and minified to minimize the number of requests needed to deliver the bundle to a client.

In the sections below we will discuss :ref:`resources <resource_registry_resources>` and :ref:`bundles <resource_registry_bundles>` in depth.

.. _resource_registry_resources:

Resources
=========

Resources are the main unit of the resource registry.
A resource may contain at most one JavaScript file and zero or more CSS/Less files.
RequireJS identifies resources by name.

Resources - as well as :ref:`bundles <resource_registry_bundles>` - are registered with a ``records`` element in the ``registry.xml`` Generic Setup import step.

The Plone 5 Resource Registry reads these ``records`` and builds RequireJS configuration for compiling resources into :ref:`bundles <resource_registry_bundles>`.

A resource record element must have two attributes: "prefix" and "interface".
The value of "interface" must be ``Products.CMFPlone.interfaces.IResourceRegistry``.

The value of "prefix" must begin with ``plone.resources/`` followed by a unique value that will be used by RequireJS as the **name** of the resource.

To ensure that your bundle has a unique name, we suggest that you use the name of your package.

You should convert dots to dashes to conform to RequireJS naming standards.
See below for :ref:`some examples <resource_example_records>` of different types of resource records.

JavaScript resources registered should conform to the RequireJS module pattern.

We can also include non-module, legacy resources which do not make use of the RequireJS ``define`` and ``require`` methods.

If you must register such resources, use the :ref:`shim options <resource_shim_options>` defined below.

.. _resource_standard_options:

Resource Options
----------------

Options are defined on a resource record using value elements in the form ``<value name="option_name">option_value</value>``.
The options that may be used on any resource record are:

js
    URL of the JavaScript file.

css
    URLs of CSS/Less elements.

url
    Base URL for loading additional resources like text files.
    See below for :ref:`an example <resource_url_option>`.

For these options, the URL you provide as a value must point to a file in a :doc:`resource folder <templates_css/resourcefolders>`.

Optionally, you may choose to register a directory in your package using the :ref:`++plone++static <plone_static_traversal_namespace>` traversal namespace.


.. _resource_shim_options:

Shim Resources
--------------

If the JavaScript you wish to register does not follow the RequireJS module pattern (using ``define`` and ``require``), you may still register it in a resource.

You will need to use the ``shim`` options for your resource record.
We refer to this kind of JavaScript as "legacy", as it doesn't follow our proposed best practices.

For more information on configuring shims in RequireJS, see: http://requirejs.org/docs/api.html#config-shim

export
    Shim export option to define a global variable where the JavaScript module should be made available.

deps
    Shim depends option to define which other RequireJS resources should be loaded before this shim module.

init
    Shim init option to define some JavaScript code to be run on initialization.


.. _resource_example_records:

Example Resource Records
------------------------

Here are some examples of different types of resource records (all examples below are from ``Products.CMFPlone``).

An example of a resource record for a single JavaScript module:

.. code-block:: xml

    <records prefix="plone.resources/mockup-router"
             interface='Products.CMFPlone.interfaces.IResourceRegistry'>
      <value key="js">++resource++mockupjs/router.js</value>
    </records>

An example of a resource record for a single Less file:

.. code-block:: xml

    <records prefix="plone.resources/bootstrap-variables"
             interface='Products.CMFPlone.interfaces.IResourceRegistry'>
        <value key="css">
          <element>++plone++static/components/bootstrap/less/variables.less</element>
        </value>
    </records>

An example of a resource for multiple Less files:

.. code-block:: xml

    <records prefix="plone.resources/bootstrap-basic"
             interface='Products.CMFPlone.interfaces.IResourceRegistry'>
        <value key="css">
          <element>++plone++static/components/bootstrap/less/utilities.less</element>
          <element>++plone++static/components/bootstrap/less/forms.less</element>
          <element>++plone++static/components/bootstrap/less/navs.less</element>
          <element>++plone++static/components/bootstrap/less/navbar.less</element>
        </value>
    </records>

An example of a resource combining JavaScript and Less/CSS:

.. code-block:: xml

    <records prefix="plone.resources/picker.date"
             interface='Products.CMFPlone.interfaces.IResourceRegistry'>
        <value key="js">++plone++static/components/pickadate/lib/picker.date.js</value>
        <value key="css">
          <element>++plone++static/components/pickadate/lib/themes/classic.date.css</element>
        </value>
        <value key="deps">picker</value>
    </records>

.. note::

   Please note that because a resource may contain at most one JavaScript file, the url for that file is placed directly into the ``<value key="js" />`` option.
          However, as a resource may contain any number of CSS/Less files, each url must be added to the ``<value key="css" />`` in an ``<element />`` tag.

.. _resource_url_option:

The URL Resource Option
***********************

The URL option allows you to define the base URL for loading other resources needed by your JavaScript.

In the following example from the ``mockup`` package, the ``url`` option is used to register a URL base from which an XML template may be loaded.
The name of the resource is set as ``mockup-patterns-structure``.


In the resource is register in ``registry.xml`` (from  ``Products.CMFPlone``):

.. code-block:: xml

    <records prefix="plone.resources/mockup-patterns-structure"
            interface='Products.CMFPlone.interfaces.IResourceRegistry'>
        <value key="js">++resource++mockup/structure/pattern.js</value>
        <value key="url">++resource++mockup/structure</value>
        <value key="css">
            <element>++resource++mockup/structure/less/pattern.structure.less</element>
        </value>
    </records>

Then in ``mockup/configure.zcml`` we register a resource directory called ``mockup``.

The resource traversal namespace ``++resource++mockup`` points to the filesystem directory ``mockup/patterns``.

.. code-block:: xml

    <browser:resourceDirectory
        name="mockup"
        directory="./patterns" />


Finally, in ``mockup/patterns/structure/js/views/actionmenu.js``, we can list a `text dependency <http://requirejs.org/docs/api.html#text>`_.

The URL base for the dependency is listed as ``mockup-patterns-structure-url``.

The path that follows will be resolved from the registered resource directory set in the URL option for this resource record: ``mockup/patterns/structure``.

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


Shim Resource Examples
**********************

Here is an example of a resource record using shim options (from ``Products.CMFPlone.profiles.dependencies``).

Here, the variable ``tinyMCE`` is exported as an attribute of ``window``, the global JavaScript namespace.
The ``init`` option is used to define a simple function that will be executed when the ``tinymce.js`` JavaScript file has been loaded.

TODO: Verify that the above description is true.

.. code-block:: xml

  <records prefix="plone.resources/tinymce"
           interface='Products.CMFPlone.interfaces.IResourceRegistry'>
    <value key="js">++plone++static/components/tinymce/tinymce.js</value>
    <value key="export">window.tinyMCE</value>
    <value key="init">function() { this.tinyMCE.DOM.events.domLoaded = true; return this.tinyMCE; }</value>
    <value key="css">
      <element>++plone++static/components/tinymce/skins/lightgray/skin.min.css</element>
      <element>++plone++static/components/tinymce/skins/lightgray/content.inline.min.css</element>
    </value>
  </records>

In this example, we configure the shim for the ``backbone`` resource.
This resource exports the backbone javascript library as the ``Backbone`` attribute of ``window``, the global JavaScript namespace.
The ``deps`` option is used to list two resources required by backbone: ``underscore`` and ``jquery``.
Note that the format for ``deps`` is a comma-separated list of resource names.
All resources named in ``deps`` must also be registered with the Plone 5 Resource Registry.

.. code-block:: xml

    <records prefix="plone.resources/backbone"
             interface='Products.CMFPlone.interfaces.IResourceRegistry'>
        <value key="js">++plone++static/components/backbone/backbone.js</value>
        <value key="export">window.Backbone</value>
        <value key="deps">underscore,jquery</value>
    </records>

Default Resources In Plone
--------------------------

Plone 5 ships with a list of Mockup and Bower components for Plone 5's new UI.

These resources can be found in the static folder (``Products.CMFPlone.static``), where you can also find the `bower.json <https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/static/bower.json>`_ file.

These resources are preconfigured in the registry (`registry.xml <https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/profiles/dependencies/registry.xml>`_ in ``Products.CMFPlone.profiles.dependencies``).

.. _plone_static_traversal_namespace:

The ++plone++ Traversal Namespace
---------------------------------

We have a new ``plone.resource`` based traversal namespace called ``++plone++``.
Plone registers the ``Products.CMFPlone.static`` folder for this traversal namespace.

Resource contained in this namespace can be stored in the ZODB (where they are looked up first, by default) or in the filesystem.
This allows us to customize filesystem based resources Through-The-Web.
One advantage of this new namespace over the existing ``++resource++`` and ``++theme++`` namespaces is that you may override resources in this namespace one file at a time, rather than needing to override the entire directory.

You may configure a folder in your add-on package to be included in this namespace.
To configure a directory in your package, add the following ZCML:

.. code-block:: xml

    <plone:static
        directory="static"
        type="plone"
        name="myresources"
        />

Now we can access the contents of the "static" folder in your package by using a URL that starts with ``++plone++myresources/``.

Additional path segments in your URL will be resolved within the "static" folder in your package.

For example, ``++plone++myresources/js/my-package.js`` will correspond to ``static/js/my-package.js`` within your package.

.. note::

   When providing static resources (JavaScript/Less/CSS) for Plone 5's resource registry, use ``plone.resource`` based resources instead of Zope's browser resources.

   The latter are cached heavily and you won't get your changes compiled into bundles, even after Zope restarts.


.. _resource_registry_bundles:

Bundles
=======

A bundle combines multiple :ref:`resources <resource_registry_resources>` into a single unit, identified by a name.
Bundles can be used to group resources for different purposes.

For example, the "plone" bundle provides resources that could be of use to any client, but the "plone-logged-in" bundle supplies resources needed only for those who are logged in to the Plone site.

Generally speaking, when a Plone page is delivered to a client, only bundles will be loaded.
There are exceptions, you can register individual resources to be loaded for a specific request via an API method.

We will discuss this :ref:`a bit later <bundles_request_api>`.

Like :ref:`resources <resource_registry_resources>`, bundles are registered with a ``records`` element in the ``registry.xml`` Generic Setup import step.

A bundle record element must have two attributes: "prefix" and "interface".
The value of "interface" must be ``Products.CMFPlone.interfaces.IBundleRegistry``.
The value of "prefix" must begin with ``plone.bundles/`` followed by a unique value that will be used as the name of the bundle.
See below for :ref:`some examples <bundle_example_records>` of different types of resource records.

When developing an add-on you will create your own bundle.
Your bundle should include all resources required for your JavaScript or CSS/Less to work properly.

If your bundle will be used only on a single page, you can define it to include it only there.
You can use the "expression" option to control including an enabled bundle.
You can also use API methods from ``Products.CMFPlone.resources`` to add disabled bundles to a single request.
For example, the ``resourceregistry`` bundle is only used for the ``@@resourceregistry-controlpanel`` view.
(see the section :ref:`bundles_request_api` for more information)

.. note::

    A bundle can depend on other bundles.
    Declaring such a dependency only controls the order in which bundles are loaded and is mostly relevant for legacy bundles.
    Currently, bundle dependencies don't make use of RequireJS dependencies or AMD.
    Each bundle will be compiled with all dependencies, even if a dependency was already used for another bundle.
    This raises the response payload unnecessarily.

    To avoid this, use the ``stub_js_modules`` option for your bundle record listed in :ref:`resource_bundle_options` below.

Development VS. Production Mode
-------------------------------

In development mode, each bundle loads all of its resources individually.
This allows modifications to resources to be immediately available.

You do not need to compile any bundles beforehand.

You should be aware that this feature does lead to a lot of requests and slow response times, even though RequireJS loads dependencies asynchronously.

In production environments you will compile your bundles to combine and minify all the necessary resources into a single JavaScript and CSS file.
Since the dependencies of each resource in the bundle are all now well-defined, they can all be included in these files.
Compiling bundles minimizes the number of web requests and the payload of data sent over the network.
In Production mode, only one or two files are included in the output for each active bundle: a JavaScript and a CSS file.

.. _resource_bundle_options:

Bundle Options
--------------

Options are defined on a bundle record using value elements in the form ``<value name="option_name">option_value</value>``.
The possible options for a bundle are:

enabled
    Enable or disable the bundle.

depends
    List other bundles as dependencies of this bundle.
    Currently used for the order of inclusion in the rendered content.
    The defined bundle will only be included in a page after any bundles listed.

resources
    List the resources that are included in this bundle.

compile
    Set the value to ``True`` or ``False``.
    Your bundle must be compiled if it has any Less or RequireJS resources.
    If you wish, you may precompile your bundles using command line tools provided by Plone or your own preferred toolchain.
    For more information, :ref:`see below <bundles_compiling_bundles>`.

    If this value is ``False``, no button will be provided to compile this bundle Through-The-Web (eg. used for the ``plone-legacy`` :ref:`bundle <bundles_legacy_bundle>`).

expression
    A TALES expression.
    If the expression evaluates as ``True``, the bundle will be included.

merge_with
    Indicate in which of the bundle aggregations this bundle should be included.
    The valid values for this option are ``default`` or ``logged-in``.
    (:ref:`see below <resource_bundle_aggregation>`).

conditionalcomment
    Provide a conditional comment for Internet Explorer hacks.

stub_js_modules
    Provide a list of resources that are required by this bundle, but already provided by another active bundle.
    This prevents the stub module from being included multiple times and can reduce the download size of bundles.

    .. versionadded:: 5.0.1


The following options are used when you provide a pre-compiled bundle.
The values will be automatically set when the bundle is built Through-The-Web.
If you use the ``plone-compile-resources`` script, or your own custom toolchain to compile your own bundle JS or CSS, you will need to manage these values yourself.

jscompilation
    URL of the compiled and minified JavaScript file.

csscompilation
    URL of the compiled and minified CSS file.

last_compilation
    Date of the last compilation time.
    The value of this option is automatically used as version parameter for cache-busting in production mode.
    (eg. ``plone-logged-in-compiled.min.js?version=2015-05-07%2000:00:00.000003``)


.. _bundles_compiling_bundles:

Compiling Bundles
-----------------

There are three ways to provide a compiled version of a bundle for production:

**Compile the bundle Through-The-Web and store it in the ZODB**

When using this option, all an add-on developer or an integrator needs to do is register a bundle with the "compile" option set to ``True``.
In the Plone 5 Resource Registry control panel, a button will be available to compile the bundle.
Pressing this button will compile the bundle and store it for production delivery.

**Compile the bundle from the command line**:

Plone provides a script which will compile a specific bundle available in the resource registry.
To use this option, you must specifically request the script in your buildout.
Add a new part called "resources" and list it in your buildout "parts", then re-run buildout.
You will find the ``plone-compile-resources`` script in your buildout ``bin`` directory.

.. code-block:: ini

    [resources]
    recipe = zc.recipe.egg
    eggs = 
        plone.staticresources
    scripts = plone-compile-resources

Once the script has been created you may invoke it.
You will need to provide options indicating the ID of the Plone site in which your package is installed, and the name of the bundle you wish to compile:

.. code-block:: console

   ./bin/plone-compile-resources --site-id=myplonesite --bundle=mybundle

This script will start up your Plone site, extract the required information and compile the bundle.
Because of this, you will need to stop a Plone instance before running this script.

**Use your own compilation chain**

The Plone 5 Resource Registry can be used with your favorite build system.
Use the tool you prefer create a compiled version of your bundle.
Your bundle registration must provide a URL for the "jscompilation" and "csscompilation" options.
Your compiled files must be in the filesystem locations that are indicated by these values.

Default Plone Bundles
---------------------

There are three main bundles defined by Plone:

plone:
    This is the main compiled bundle with all the JavaScript and CSS components required for the Plone Toolbar and the main Mockup patterns.

plone-logged-in:
    This bundle is only included for logged in users.
    It contains patterns like the "tinymce" pattern, the "querystring" pattern for collection edit forms and others.

plone-legacy:
    This bundle is not compiled and contains code that doesn't use RequireJS or Less.
    Addons which continue to install resources to ``portal_javascripts`` or ``portal_css`` are registered as resources in the plone-legacy bundle automatically.

.. _bundles_legacy_bundle:

The Legacy Bundle
-----------------

The legacy bundle exists to support packages with code that does not work with the new Plone 5 Resource Registry.
Code that cannot be migrated to use RequireJS can be included in the legacy bundle.

Code that uses RequireJS in a way which is incompatible with Plone's use of it (e.g. it's using its own RequireJS setup) can be included in the legacy bundle.

.. note::

    Some JavaScript use its own setup of RequireJS.
    Others - like Leaflet 0.7 or DataTables 1.10 - try to register themselves for RequireJS.
    This can lead to the infamous "mismatched anonymous define" errors (:ref:`see below <resource_registry_error_anon_define>`).
    You can register such scripts in the ``plone-legacy`` bundle by including them in the ``jsregistry.xml`` import step.
    The ``define`` and ``require`` methods are unset before these scripts are included in the output and reset again after all scripts have been included.
    See yourself: https://github.com/plone/Products.CMFPlone/pull/870/files

Resources which are registered into ``portal_javascripts`` or ``portal_css`` registries via an addon are automatically registered in the legacy bundle and cleared from ``portal_javascripts`` and ``portal_css``.

.. note::

    JavaScript which doesn't use RequireJS can still be managed by it by including it as a resource with configured shim options.

The plone-legacy bundle treats resources differently: they are not compiled, but simply concatenated and minified.


.. _bundle_example_records:

Example Bundle Records
----------------------

Here are some examples of Bundle records from Plone and popular add-ons

The record for Plone's ``plone`` bundle names a single resource, ``plone``.
This is a good example of using a single resource with a ``require`` call to bundle a number of other resources, many of which use ``define``, in order to avoid :ref:`resource_registry_error_anon_define`.
(see ``Products/CMFPlone/profiles/dependencies/registry.xml`` and ``Products/CMFPlone/static/plone.js``, and for an example of the bundled resources ``mockup/patterns/autotoc/pattern.js``)

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

The record for the ``plone-legacy`` bundle names the only javascript resource left in Plone that does not work with the Resource registry.
Note that any JavaScript or CSS registered with the old ``portal_javascripts`` or ``portal_css`` tools will be included automatically in this bundle.

Note too that the ``plone-legacy`` bundle declares a dependency on the ``plone`` bundle, which ensures only that the ``plone`` bundle will be loaded into the page before this one.

.. code-block:: xml

    <records prefix="plone.bundles/plone-legacy"
              interface='Products.CMFPlone.interfaces.IBundleRegistry'>
      <value key="resources" purge="false">
        <element>jquery-highlightsearchterms</element>
      </value>
      <value key="depends">plone</value>
      <value key="jscompilation">++plone++static/plone-legacy-compiled.js</value>
      <value key="csscompilation">++plone++static/plone-legacy-compiled.css</value>
      <value key="last_compilation">2014-08-14 00:00:00</value>
      <value key="compile">False</value>
      <value key="enabled">True</value>
    </records>

A bundle is registered in the Plone add-on package `Plomino <https://github.com/plomino/Plomino>`_.
Here, a number of resources are aggregated and compiled via the ``plone-compile-resources`` script.
They may also be compiled Through-The-Web, using the Resource Registry.
Notice that in contrast to the ``plone`` bundle, the resources combined here all use ``require`` at the top level to avoid :ref:`resource_registry_error_anon_define`.
(see ``Products/CMFPlomino/profiles/default/registry.xml`` and for an example of the resources included ``Products/CMFPlomino/browser/static/js/table.js``)

.. code-block:: xml

    <records prefix="plone.bundles/plomino"
             interface='Products.CMFPlone.interfaces.IBundleRegistry'>
      <value key="resources">
        <element>plominoformula</element>
        <element>plominotable</element>
        <element>plominodesign</element>
        <element>plominodynamic</element>
      </value>
      <value key="enabled">True</value>
      <value key="depends">plone</value>
      <value key="jscompilation">++resource++Products.CMFPlomino/js/plomino-compiled.js</value>
      <value key="csscompilation">++resource++Products.CMFPlomino/css/plomino-compiled.css</value>
      <value key="last_compilation">2015-12-08 00:00:00</value>
    </records>

In `Rapido <https://github.com/plomino/rapido.plone>`_, another Plone add-on, the JavaScript registered for the bundle is manually compiled.
By listing the ``plone`` default bundle as a dependency, this JavaScript is able to rely on Plone default resources such as ``jQuery``, ``mockup`` and the patterns registry being present.
(see ``rapido/plone/profiles/default/registry.xml`` and ``rapido/plone/browser/rapido.js``)

.. code-block:: xml

    <records prefix="plone.bundles/rapido"
             interface='Products.CMFPlone.interfaces.IBundleRegistry'>
      <value key="enabled">True</value>
      <value key="jscompilation">++resource++rapido.js</value>
      <value key="csscompilation"></value>
      <value key="last_compilation">2019-11-26 00:00:00</value>
      <value key="compile">False</value>
      <value key="depends">plone</value>
    </records>

.. _bundle_example_non_amd:

Non-AMD Bundles
***************

Sometimes it may be useful to register a simple javascript without using the AMD pattern.
An example of such a bundle is provided in the `example.p4p5 <https://github.com/collective/example.p4p5>`_ package.
In this case, there is a simple JavaScript which appends a status div to a chart (``example/p4p5/browser/static/chart.js``):

.. code-block:: javascript

    $(document).ready(function() {
        var chart = $('#chart');
        var done = parseInt(chart.attr('done'));
        var inprogress = parseInt(chart.attr('inprogress'));
        var total = done + inprogress;
        if(total == 0) {
            total = 1;
        }
        var done_rate = Math.round(100 * done / total);
        var inprogress_rate = Math.round(100 * inprogress / total);
        chart.append('<div class="done" style="width:'+done_rate+'%">&nbsp;</div>');
        chart.append('<div class="inprogress" style="width:'+inprogress_rate+'%">&nbsp;</div>');
    });

In this case, the JavaScript is dependent only on a global `$` which is expected to be bound to jQuery.
Plone provides this in the ``plone`` bundle, so that is the only dependency we need to specify.
For such a case, the package can register this JavaScript in ``jsregistry.xml`` for Plone versions before 5.0.
And in Plone 5, the following bundle record added in ``registry.xml`` will do the trick (``example/p4p5/profiles/plone5/registry.xml``):

.. code-block:: xml

    <records prefix="plone.bundles/examplep4p5"
             interface='Products.CMFPlone.interfaces.IBundleRegistry'>
      <value key="enabled">True</value>
      <value key="jscompilation">++resource++example.p4p5/chart.js</value>
      <value key="csscompilation">++resource++example.p4p5/chart.css</value>
      <value key="last_compilation">2016-01-01 00:00:00</value>
      <value key="compile">False</value>
      <value key="depends">plone</value>
    </records>

Notice that this bundle provides *no resources*.
The JavaScript file from the package is provided as the value of the ``jscompilation`` option.
The CSS file is likewise provided as a pre-compiled value.
Finally the value of the ``compile`` option is set to ``False``.
This ensures that the Resource Registry will make no attempt to re-compile this bundle.

.. _bundles_request_api:

Controlling Resource And Bundle Rendering
=========================================

To control whether a bundle is included in a rendered page, we have already discussed several options.
You may globally enable or disable a bundle using the ``enabled`` option of the bundle record.
You may conditionally render the bundle using the ``expression`` option of the bundle record.

A Diazo Theme may also include or exclude specific bundles, regardless of whether they are enabled or disabled in the Resource Registry.
To do so, use the ``enabled-bundles`` or ``disabled-bundles`` settings in the ``manifest.cfg`` file for the theme.
These settings take a comma separated list of the names of bundles.

A browser page can include or exclude a specific bundle by using the API methods from ``Products.CMFPlone.resources``.
This will override the value of ``enabled`` in the Resource Registry for the named bundle.

Here are the API methods (from ``Products.CMFPlone.resources``):

``add_bundle_on_request(request, bundle)``:
    The value provided for the ``bundle`` parameter must be the name of a bundle.
    The named bundle will be added to the provided request.

``remove_bundle_on_request(request, bundle)``:
    The value provided for the ``bundle`` parameter must be the name of a bundle.
    The named bundle will be removed from the provided request if it is present.

A browser page may also force the rendering of an individual resource on a particular request.
Thus specific resources may be included regardless of whether they are included in a rendered bundle.

Here is the API method to do so (from ``Products.CMFPlone.resources``):

``add_resource_on_request(request, resource)``:
    The value provided for ``resource`` must be the name of a resource.
    The named resource will be added to the current request.

.. _resource_bundle_aggregation:

Aggregate Bundles For Production
================================

Plone defines several bundles.
Add-ons that you include in your Plone site may also define bundles of their own.
In production, *each* of these bundles will result in the loading of one JavaScript and one CSS file.
To reduce the number of loaded files to an absolute minimum, we use "bundle aggregation".

There are two bundle aggregations available in Plone.
A first aggregation named ``default`` contains all the bundles that must be available at all times.
It creates 2 output files (one JavaScript and one CSS).
A second aggregation named ``logged-in`` contains bundles only needed for authenticated users.
It also creates 2 output files (one JavaScript and one CSS).

Aggregation of bundles is triggered by the ``registry.xml`` Generic Setup import step.
Installing any profile containing a ``registry.xml`` file will automatically refresh the current aggregations.
Any bundles declared in that file will be included, if they declare that they should be merged with one of the two available aggregations.

As bundles can be defined or modified Through-The-Web, Plone also provides a "Merge bundles for production" button in the Resource Registry.
This allows us to re-generate the aggregations manually after any Through-The-Web modifications have been made.

Declare An Aggregation
----------------------

Custom bundles from an add-on or from a theme may be aggregated with the standard Plone bundles.
To do so, use the ``merge_with`` option in your bundle declaration in ``registry.xml``.
The valid values are ``default`` or ``logged-in``.
If the ``merge_with`` option is not present or is empty, the bundle will not be aggregated and is published separately.

.. code-block:: xml

  <records prefix="plone.bundles/my-bundle"
            interface='Products.CMFPlone.interfaces.IBundleRegistry'>
    <value key="merge_with">logged-in</value>
    ...
  </record>

.. note:: Bundles cannot be conditionally included in an aggregation.
          If the value of the `merge_with` option is `default` or `logged-in`, the value of the `expression` option **will be ignored**.

.. note:: In Development mode, aggregation is disabled, all bundles are published separately.

Diazo Bundles
=============

The point with Diazo is to create standalone static themes which work without Plone.
Diazo themes can use - and will use - their own resources and compiling systems.

Diazo was extended to support bundles.
Bundles can be defined in the theme's ``manifest.cfg`` file.

Bundles configured in the ``manifest.cfg`` file are included in the output by the renderer additionally to the ones registered in the resource registry.
This allows us to just overwrite or drop the ``link`` and ``script`` tags from the theme but still include the theme-specific resources without having to register them in the resource registry.

The options are:

enabled-bundles / disabled-bundles:
    A comma-separated list of Resource Registry bundles that should be included or excluded when rendering the Diazo theme.
    See :ref:`bundles_request_api`.

development-css / development-js:
    Uncompiled/unminified Less/CSS file and RequireJS files which should be included in development environments.
    Any required compilation will be handled by the browser on the fly.

production-css / production-js:
    Compiled CSS or JavaScript files that will be included in production mode.

tinymce-content-css:
    A CSS file to include for the TinyMCE editor.
    This allows theme developers to ensure that TinyMCE gives you the best possible WYSIWYG experience.

.. note::

    Files referenced by ``production-css`` and ``production-js`` must be present in the theme and pre-compiled.
    Less and RequireJS files named in Diazo Bundles cannot be compiled by the Resource Registry Through-The-Web.
    Nor can they be compiled by the ``plone-compile-resources`` script.
    For Diazo Bundles, the theme must provide its own compilation toolchain.

Example ``manifest.cfg``
------------------------

This example is from ``plonetheme.barceloneta``, the default theme in Plone 5 (``plonetheme/barceloneta/theme/manifest.cfg``).
Here, a Less file for development, a compiled CSS file for production and a second compiled CSS file meant specifically for use with TinyMCE are all named.
The `package itself <https://github.com/plone/plonetheme.barceloneta>`_ provides a ``Gruntfile.js`` and ``package.json`` file for compiling Less to CSS.

.. code-block:: ini

    [theme]
    title = Barceloneta Theme
    description = The default theme for Plone 5
    preview = preview.png
    rules = /++theme++barceloneta/rules.xml
    prefix = /++theme++barceloneta
    doctype = <!DOCTYPE html>
    enabled-bundles =
    disabled-bundles =

    development-css = /++theme++barceloneta/less/barceloneta.plone.less
    production-css = /++theme++barceloneta/less/barceloneta-compiled.css
    tinymce-content-css = /++theme++barceloneta/less/barceloneta-compiled.css

    development-js =
    production-js =

.. _resource_migrate_add_ons:

Migrating Older Add-ons
=======================

Many add-ons in the Plone ecosystem include JavaScript and CSS resources.
To take advantage of the dependency management capabilities of the new Resource Registry, they will need to be migrated.

.. _resource_old_registry_compatibility:

Compatibility With Deprecated Registries
----------------------------------------

The ``portal_css`` and ``portal_javascript`` registries have been deprecated in Plone 5.
Older Add-ons register CSS and JavaScript resource with these registries using the ``cssregistry.xml`` and ``jsregistry.xml`` Generic Setup import steps.
Plone 5 will still recognize these import steps, and resources registered with them will be added to the :ref:`plone-legacy bundle <bundles_legacy_bundle>`.

Thus, older add-ons with JavaScript and CSS have a reasonable chance of working without migrating...yet.

However, scripts included in this fashion receive none of the dependency management benefits of the new Resource Registry.
The ``plone-legacy`` bundle includes a global jQuery object and then includes bundled resources in order.
The ``define`` and ``require`` APIs from RequireJS are unset before the ``plone-legacy`` bundle is included, and then re-defined after.

Updating non-AMD Scripts
------------------------

To take advantage of the dependency management of the new Resource Registry, you should upgrade your existing JavaScript files to use the AMD pattern.
To do so, wrap existing JavaScript using this recipe:

.. code-block:: javascript

      require([
        'jquery',
        'other-library'
      ], function($, otherLibrary) {
        'use strict';
        ...
        // All the previous JavaScript file code here
        ...
      });

(For a description of the ``require(Array, Function)`` used here, `See the AMD API documentation <https://github.com/amdjs/amdjs-api/blob/master/require.md#requirearray-function->`_)

Dependencies required by your JavaScript code must be listed in the ``Array`` argument to the ``require`` API.
You must use the RequireJS name identifiers of your dependencies here.
These will be the names of the Plone Resources which provide those JavaScript modules.

Listed dependencies are be passed to the ``Function`` argument as parameters.
They will be available to the code inside this function.

Register your modeified files as :ref:`resources <resource_registry_resources>` in ``registry.xml``.
Finally, register a :ref:`bundle <resource_registry_bundles>` in ``registry.xml`` which includes any of your resources.

.. note::

    When using ``require`` instead of ``define``, the anonymous function is immediately called.
    If you would use ``define`` instead, you'd have to make a ``require`` call somewhere, with the dependency to your resource.

This recipe should work for many JavaScript files.
Other patterns for module definition may be found in the `AMD API definitions <https://github.com/amdjs/amdjs-api>`_ or the `RequireJS API documentation <http://requirejs.org/docs/api.html#define>`_.

.. _resource_registry_error_anon_define:

The ``mismatched anonymous define`` error
-----------------------------------------

If you have worked with RequireJS before, you are likely to be aware of the `mismatched anonymous define() <http://requirejs.org/docs/errors.html#mismatch>`_ error.
It arises from misuse of the ``require`` and ``define`` APIs.

To work in RequireJS, code that uses a call to ``define`` must be loaded into a page **only** through a call to ``require``.
You may not load such code using a ``<script>`` tag.

When applied to the concept of resources and bundles this means that bundles should **only** ever be ``require`` calls.
If you try to use a JavaScript file that has a ``define`` call with a bundle, you'll likely cause the ``mismatched anonymous define()`` error.
Make sure to use a JavaScript file with a ``require`` call to include all your ``define`` resources.

This is a fact of how RequireJS works.
It is normal behavior.
Keeping it in mind can save you headaches.


Including non-RequireJS Scripts In A Diazo Theme
------------------------------------------------

We have already described how to add resources to the legacy bundle.
We have also discussed that the legacy bundle unsets the ``define`` and ``require`` statements before loading its resources so as to avoid the :ref:`mismatched anonymous define() <resource_registry_error_anon_define>` error and other possible problems.

If you have scripts in your Diazo theme that you don't want to register with the resource registry and which are not compatible with RequireJS, you can take a similar approach.
Add these scripts below the Plone scripts and unset ``define`` and ``require`` yourself.

Here is an example Diazo rule which does so:

.. code-block:: xml

      <before theme="/html/head/script[1]">                     <!-- ... before your own scripts -->
          <xsl:apply-templates select="/html/head/script" />    <!-- include the Plone scripts -->
          <script>                                              <!-- and then unset require and define -->
              require = undefined
              define = undefined
          </script>
      </before>
