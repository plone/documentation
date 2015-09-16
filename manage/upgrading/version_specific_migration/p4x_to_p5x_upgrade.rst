=========================================================
Upgrading Plone 4.x to 5.0
=========================================================


.. admonition:: Description

   Instructions and tips for upgrading to a newer Plone version.

.. contents:: :local:

Changes due to implemented PLIPS
================================

PLIP 13350 "Define extra member properties TTW"
-----------------------------------------------

In Plone 5, the custom fields displayed in the user profile form and the
registration form are managed by `plone.schemaeditor`. They are dynamically
editable from the Plone control panel, and can be imported from a Generic Setup
profile file named `userschema.xml`.

If you have some custom member properties in your Plone site, be aware that:

- extra attributes defined in `memberdata_properties.xml` will be preserved, but
  they will not be automatically shown in the user profile form or the
  registration form,
- if you have implemented some custom forms in order to display your custom
  member attributes, they will not work anymore as `plone.app.users` is now
  based on `z3c.form`. You can easily replace them by declaring their schema in
  `userschema.xml`.

.. note::

    When a custom field is defined in `userschema.xml`, its corresponding
    attribute is automatically created in the `portal_memberdata` tool, so there
    is no need to declare it in `memberdata_properties.xml`.
    `memberdata_properties.xml` will only handled attributes that are not
    related to the user profile form or the registration form.


Changed imports and functions
========================================


Products.CMFPlone.interfaces.IFactoryTool
-----------------------------------------

This is now moved to ATContentTypes.

Example::

    try:
        # plone 4
        from Products.CMFPlone.interfaces import IFactoryTool
    except ImportError:
        # plone 5
        from Products.ATContentTypes.interfaces.factory import IFactoryTool



Archetypes
========================================

Plone 5 now uses dexterity as the content type engine instead of Archetypes.

For packages that still use Archetypes, you'll need to install the ATContentTypes
base package.

In your package, in a setuphandler, the code might look something like this::


    from Products.CMFPlone.utils import getFSVersionTuple
    if getFSVersionTuple()[0] == 5:
        # if plone 5, we need to make sure archetypes related tools is installed
        qi = getToolByName(site, 'portal_quickinstaller')
        # install ATContentTypes if it isn't installed
        if not qi.isProductInstalled('ATContentTypes'):
            qi.installProducts(['ATContentTypes'])



Resource Registry
========================================

Plone 5 introduces some new concepts, for some, with working with JavaScript in Plone. Plone 5 utilizes Asynchronous Module Definition (AMD) with `requirejs <http://requirejs.org/>`_. We chose AMD over other module loading implementations(like commonjs) because AMD can be used in non-compiled form in the browser. This way, someone can click "development mode" in the resource registry control panel and work with the non-compiled JavaScript files directly.

Getting back on point, much of Plone's JavaScript was or still is using JavaScript in a non-AMD form. Scripts that expect JavaScript dependency scripts and objects to be globally available and not loaded synchronously will have a difficult time figuring out what is going on when upgrading to Plone 5.

There are two scenarios where this will happen that we'll tackle in this post. 1) You have JavaScript registered in portal_javascripts that are not AMD compatible. 2) You have JavaScript included in the head tag of your theme and/or specific page templates that are not AMD compatible.


1) Working with deprecated portal_javascripts
---------------------------------------------

The deprecated resource registries(and portal_javascripts) has no concept of dependency management. It simply allowed you to specify an order in which JavaScript files should be included on your site. It also would combined and minify them for you in deployment mode.

Registration changes
~~~~~~~~~~~~~~~~~~~~

Prior to Plone 5, JavaScript files were added to the registry by using a `Generic Setup Profile <http://docs.plone.org/develop/addons/components/genericsetup.html>`_ and including a jsregistry.xml file to it. This would add your JavaScript to the registry, with some options and potentially set ordering.

In Plone 5.0, Plone will still recognize these jsregistry.xml files. Plone tries to provide a shim for those that are stubborn to migrate. How it does this is by adding all jsregistry.xml JavaScripts into a "plone-legacy" Resource Registry bundle. This bundle simply includes a global jQuery object and includes the resources in sequential order after it.

Old style jsregistry.xml
~~~~~~~~~~~~~~~~~~~~~~~~

An old style Resource Registry would look like this::

    <?xml version="1.0"?>
    <object name="portal_javascripts">
      <javascript
        id="++resource++foobar.js"
        inline="False"
      />
    </object>


To migrate this to Plone 5, resource registrations are all done in the `Configuration Registry <https://pypi.python.org/pypi/plone.app.registry>`_.

New style with registry.xml
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The new registration will look something like::

    <?xml version="1.0"?>
    <registry>
      <records prefix="plone.resources/foobar"
               interface='Products.CMFPlone.interfaces.IResourceRegistry'>
        <value key="js">.++resource++foobar.js</value>
        <value key="deps">jquery</value>
      </records>
    </registry>

Notice how I've now added the deps property of "jquery". This is not necessary--I'm just giving an example that this script needs a global jquery available.

This alone will not get your JavaScript included however. In order to modernize our JavaScript stack, Plone needed to make some changes with how it included JavaScript. All we've done so far is define a resource. In order for a resource to be included, it needs to be part of a bundle. A bundle defines a set of resources that should be compiled together and distributed to the browser. So you either need to add your resource to an existing bundle or create your own bundle.

In this post, we'll describe the process of creating your own bundle. Again, we use registry.xml for configuration::

    <records prefix="plone.bundles/foobar"
             interface='Products.CMFPlone.interfaces.IBundleRegistry'>
      <value key="resources">
        <element>foobar</element>
      </value>
      <value key="enabled">True</value>
      <value key="jscompilation">++resource++foobar-compiled.min.js</value>
      <value key="last_compilation">2015-02-06 00:00:00</value>
    </records>

One important aspect here is the "jscompilation" settings. This defines the compiled resource used in production mode. 


But, it's a bit more work
~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, we know. We tried very hard to figure out the easiest way to modernize Plone's JavaScript development stack. The old, sequential inclusion is not useful these days.

That being said, adding resources, bundles and compiling them can all be done Through The Web(TTW) in the new Resource Registries configuration panel. That way you can turn on development mode, compile your resources and then copy that compiled version into your package for distribution and not need to know any newfangled nodejs technologies like grunt, gulp, bower, npm, etc.


Updating non-AMD scripts
------------------------

If you are not including your JavaScript in the Resource Registries and just need it to work alongside Plone's JavaScript because you're manually including the JavaScript files in one way or another(page templates, themes), there are a number of techniques available to read on the web that describe how to make your scripts conditionally work with AMD.

For the sake of this post, I will describe one technique used in Plone core to fix the JavaScript. The change we'll be investigating can be seen with `in a commit to plone.app.registry <https://github.com/plone/plone.app.registry/commit/ad904f2d55ea6e45bb983f1fcc12ead7a191f50a>`_. plone.app.registry has a control panel that allows some ajax searching and modals for editing settings.

To utilize the dependency management that AMD provides and have the javascript depend on jQuery, we can wrap the script in an AMD `require` function. This function allows you to define a set of dependencies and a function that takes as arguments, those dependencies you defined. After the dependencies are loaded, the function you defined is called.

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

Here, the two dependencies we have are jQuery and the pattern registry. I will not get into the pattern registry as it's off topic for this discussion--it is basically a registry of JavaScript components. The necessity for using it here is with ajax calls and binding new DOM elements dynamically added to the page.

Additionally, above this `require` call, I provide some backward compatible code that you can inspect. It's not necessary in this case but I added it to show how someone could make their script work when requirejs was available and when it was not.


Caveats
-------

Compilation
~~~~~~~~~~~

Prior to Plone 5, when a resource was changed or added to the javascript registry, the registry would automatically re-compile all your JavaScript files.

In switching to AMD, the compile step is much more resource intensive. It takes so long, there is no way we could do this real-time. Additionally, it can not be done in Python.

When changes are made to existing bundles, re-compilation will need to be done TTW in the Resource Registries control panel. There is a build button next to each bundle. For advanced users, compilation can be done using a tool like grunt in your development environment.

Conditional resources
~~~~~~~~~~~~~~~~~~~~~

In Plone 5, individual resources can not be conditionally added to every page. This is due to the way we build JavaScript with AMD. Only bundles can be conditionally included. So if you have a resource that needs to be conditionally included, it will likely need it's own bundle.


