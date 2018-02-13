==========================
Upgrading Plone 4.x To 5.0
==========================


.. admonition:: Description

   Instructions and tips for upgrading to a newer Plone version.

.. note::

   If you want to upgrade add-ons to Plone 5, also see :doc:`/develop/addons/upgrade_to_50`


General Information
===================

- Before you upgrade read :doc:`../intro` and :doc:`../preparations`.
- Always upgrade from the latest version of 4.x to the latest version of 5.x (at the time of writing 4.3.7 to 5.0.2).
  This will resolve many migration-specific issues.
- If you have problems don't be afraid to ask for help on http://community.plone.org
- There is a `video  <https://youtu.be/bQ-IpO-7F00?t=1m17s>`_ of a talk "How to upgrade sites to Plone 5" and
  `slides <http://de.slideshare.net/derschmock/upgrade-to-plone-5>`_.


Changes Due To Implemented PLIPS
================================

PLIPs are PLone Improvement Proposals.
These are about larger changes to Plone,
discussed beforehand by the community.


PLIP 13350 "Define Extra Member Properties TTW"
-----------------------------------------------

In Plone 5, the custom fields displayed in the user profile form and the registration form are managed
by `plone.schemaeditor`.

They are dynamically editable from the Plone control panel,
and can be imported from a Generic Setup profile file named `userschema.xml`.

If you have some custom member properties in your Plone site, be aware that:

- extra attributes defined in `memberdata_properties.xml` will be preserved,
  but they will not be automatically shown in the user profile form or the registration form,
- if you have implemented some custom forms in order to display your custom member attributes,
  they will not work anymore as `plone.app.users` is now based on `z3c.form`.
  You can replace them by declaring their schema in `userschema.xml`.

.. note::

    When a custom field is defined in `userschema.xml`,
    its corresponding attribute is automatically created in the `portal_memberdata` tool,
    so there is no need to declare it in `memberdata_properties.xml`.

    `memberdata_properties.xml` will only handled attributes that are not related to the user profile form or the registration form.


PLIP 13419 "Improvements For User Ids And Login Names"
------------------------------------------------------

Since Plone 4.0 you could switch to using email as login in the security control panel.
In Plone 5.0 some related improvements were made.
When you are already using email as login,
during the Plone 5.0 migration the login names will be transformed to lowercase.

When the email addresses are not unique,
for example you have both ``joe@example.org`` and ``JOE@example.org``,
the migration will *fail*.

Best is to fix this in your site in Plone 4, by changing email addresses or removing no longer needed users.
When there are only a few users, you can do this manually.
To assist you in sites with many users, in Plone 4.1 and higher,
you can add the `collective.emaillogin4 <https://pypi.python.org/pypi/collective.emaillogin4>`_ package to the eggs of your Plone instance.

With that package, even without installing it in the add-ons control panel,
you can call the ``@@migrate-to-emaillogin`` page to look for duplicate email addresses.

.. note::

   This PLIP basically integrates the ``collective.emaillogin4`` package in Plone 5.



Other PLIP Changes
------------------

PLIPs that resulted in changes that will have to be documented in this upgrade-guide.


plone.api
  Todo: Tell people to use it. Explain how to configure plone.recipe.codeanalysis to check for old-style code
  Roel

plone.app.multilingual
  Todo: How to migrate from LP to PAM

Convert control panels to use z3c.form
  Todo: How to migrate your custom control-panels
  Who: Tisto

Main_template rebirth to HTML5  bloodbare
  Todo: What to do when you customized your main_templates.
  Who: ?

Automatic CSRF Protection
  Todo: How to protect your existing forms
  Who: Nathan

Linkintegrity in Plone 5
  Who: pbauer



Security Setting Changes
~~~~~~~~~~~~~~~~~~~~~~~~

complex, look betas.py **TODO**

Mail Setting Changes
~~~~~~~~~~~~~~~~~~~~

Markup Setting Changes
~~~~~~~~~~~~~~~~~~~~~~

User And Group Setting Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Social Media Changes
~~~~~~~~~~~~~~~~~~~~

Imaging Changes
~~~~~~~~~~~~~~~

Login Setting Changes
~~~~~~~~~~~~~~~~~~~~~


Changed Imports And Functions
=============================


Products.CMFPlone.interfaces.IFactoryTool
-----------------------------------------

This is now moved to ATContentTypes.

Example:

.. code-block:: python

    try:
        # Plone 4
        from Products.CMFPlone.interfaces import IFactoryTool
    except ImportError:
        # Plone 5
        from Products.ATContentTypes.interfaces.factory import IFactoryTool


plone.app.multilingual
======================

.. note::

   The preferred translation add-on for Plone 5 is plone.app.multilingual.
   This package supersedes LinguaPlone.

..  warning::

    This is still work in progress

There are 3 different parts to the migration from LinguaPlone to plone.app.multilingual:

* From LP to PAM 2.X - on Plone 4 and than to Plone 5 (PAM 3.X)

  See: https://github.com/plone/plone.app.multilingual/issues/181

* From PAM 1.X to 2.X - on Plone 4 and than to Plone 5 (PAM 3.X)

  Step 1: plone.multilingual is merged into plone.app.multilingual. Imports in your custom code needs to be changed:
  See:https://github.com/plone/plone.app.multilingual/issues/181#issuecomment-141661848

  Step 2: Removed plone.multilingualbehavior: https://github.com/plone/plone.app.multilingual/issues/183

  Step 3: TODO

* From PAM 2.X on Plone 4 to Plone 5 (PAM 3.X)

  Step 1: plone.multilingual is merged into plone.app.multilingual. Imports in your custom code needs to be changed: See:https://github.com/plone/plone.app.multilingual/issues/181#issuecomment-141661848
  https://github.com/plone/Products.CMFPlone/issues/1187


Archetypes
==========

Plone 5 now uses dexterity as the content type engine instead of Archetypes.

For packages that still use Archetypes, you'll need to install the ATContentTypes base package.

The easiest way to get the dependencies for Archetypes (uuid_catalog, reference_catalog, archetypes_tool) is to add the following profile to your dependencies in ``metadata.xml``:

..  code-block:: xml

    <dependencies>
         ...
        <dependency>Products.ATContentTypes:base</dependency>
    </dependencies>

See https://github.com/smcmahon/Products.PloneFormGen/blob/master/Products/PloneFormGen/profiles/default/metadata.xml for a working example.


Resource Registry
=================

.. seealso::

   http://docs.plone.org/adapt-and-extend/theming/resourceregistry.html

Plone 5 introduces some new concepts, for some, with working with JavaScript in Plone.
Plone 5 utilizes Asynchronous Module Definition (AMD) with `requirejs <http://requirejs.org/>`_.

We chose AMD over other module loading implementations(like commonjs) because AMD can be used in non-compiled form in the browser.

This way, someone can click "development mode" in the resource registry control panel and work with the non-compiled JavaScript files directly.

Getting back on point, much of Plone's JavaScript was or still is using JavaScript in a non-AMD form.
Scripts that expect JavaScript dependency scripts and objects to be globally available
and not loaded synchronously will have a difficult time figuring out what is going on when upgrading to Plone 5.

There are two scenarios where this will happen that we'll tackle in this post.
- 1) You have JavaScript registered in portal_javascripts that are not AMD compatible.
- 2) You have JavaScript included in the head tag of your theme and/or specific page templates that are not AMD compatible.


Working With Deprecated Portal_javascripts
---------------------------------------------

The deprecated resource registries(and portal_javascripts) has no concept of dependency management.
It allowed you to specify an order in which JavaScript files should be included on your site.

It also would combined and minify them for you in deployment mode.

Registration Changes
~~~~~~~~~~~~~~~~~~~~

Prior to Plone 5, JavaScript files were added to the registry by using a `Generic Setup Profile <http://docs.plone.org/develop/addons/components/genericsetup.html>`_ and including a jsregistry.xml file to it.

This would add your JavaScript to the registry, with some options and potentially set ordering.

In Plone 5.0, Plone will still recognize these jsregistry.xml files.
Plone tries to provide a shim for them.
It does this by adding all jsregistry.xml JavaScripts into the "plone-legacy" Resource Registry bundle.

This bundle includes a global jQuery object and includes the resources in sequential order after it.

However, you should consider at least migrating your resources as described
in https://github.com/collective/example.p4p5 to gain control over your dependencies or
if you want to keep backward compatibility to older Plone versions in your Add-ons.


Old Style jsregistry.xml
~~~~~~~~~~~~~~~~~~~~~~~~

An old style Resource Registry would look like this:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_javascripts">
      <javascript
        id="++resource++foobar.js"
        inline="False"
      />
    </object>


To migrate this to Plone 5, resource registrations are all done in the
`Configuration Registry <https://pypi.python.org/pypi/plone.app.registry>`_.

New Style With registry.xml
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The new registration will look something like:

.. code-block:: xml

    <?xml version="1.0"?>
    <registry>
      <records prefix="plone.resources/foobar"
               interface='Products.CMFPlone.interfaces.IResourceRegistry'>
        <value key="js">.++resource++foobar.js</value>
        <value key="deps">jquery</value>
      </records>
    </registry>

Notice how I've now added the deps property of "jquery".
This is not necessary -- I'm just giving an example that this script needs a global jQuery available.

This alone will not get your JavaScript included however.
In order to modernize our JavaScript stack, Plone needed to make some changes with how it included JavaScript.
All we've done so far is define a resource.

For a resource to be included, it needs to be part of a bundle.
A bundle defines a set of resources that should be compiled together and distributed to the browser.

You either need to add your resource to an existing bundle or create your own bundle.

In this post, we'll describe the process of creating your own bundle. Again, we use registry.xml for configuration:

.. code-block:: xml

    <records prefix="plone.bundles/foobar"
             interface='Products.CMFPlone.interfaces.IBundleRegistry'>
      <value key="resources">
        <element>foobar</element>
      </value>
      <value key="enabled">True</value>
      <value key="jscompilation">++resource++foobar-compiled.min.js</value>
      <value key="last_compilation">2015-02-06 00:00:00</value>
    </records>

One important aspect here is the "jscompilation" settings.
This defines the compiled resource used in production mode.


But, It's A Bit More Work
~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, we know. We tried very hard to figure out the easiest way to modernize Plone's JavaScript development stack.
The old, sequential inclusion is not useful these days.

That being said, adding resources, bundles and compiling them can all be done Through The Web(TTW) in the new Resource Registries configuration panel.
That way you can turn on development mode, compile your resources and then copy that
compiled version into your package for distribution and not need to know any newfangled
nodejs technologies like grunt, gulp, bower, npm, etc.


Updating Non-AMD Scripts
------------------------

If you are not including your JavaScript in the Resource Registries and
need it to work alongside Plone's JavaScript because you're manually including the JavaScript
files in one way or another(page templates, themes), there are a number of techniques available
to read on the web that describe how to make your scripts conditionally work with AMD.

For the sake of this post, I will describe one technique used in Plone core to fix the JavaScript.

The change we'll be investigating can be seen with `in a commit to plone.app.registry <https://github.com/plone/plone.app.registry/commit/ad904f2d55ea6e45bb983f1fcc12ead7a191f50a>`_.

plone.app.registry has a control panel that allows some Ajax searching and modals for editing settings.

To utilize the dependency management that AMD provides and have the JavaScript depend on jQuery,
we can wrap the script in an AMD `require` function.

This function allows you to define a set of dependencies and a function that takes as arguments,
those dependencies you defined. After the dependencies are loaded, the function you defined is called.

Example:

.. code-block:: javascript

    require([
      'jquery',
      'pat-registry'
    ], function($, Registry) {
      'use strict';
      ...
      // All my previous JavaScript file code here
      ...
    });

Here, the two dependencies we have are jQuery and the pattern registry.
I will not get into the pattern registry as it's off topic for this discussion
--it is basically a registry of JavaScript components.

The necessity for using it here is with Ajax calls and binding new DOM elements dynamically added to the page.

Additionally, above this `require` call, I provide some backward compatible code that you can inspect.

It's not necessary in this case but I added it to show how someone could make
their script work when requirejs was available and when it was not.


Caveats
-------

Compilation
~~~~~~~~~~~

Prior to Plone 5, when a resource was changed or added to the JavaScript registry,
the registry would automatically re-compile all your JavaScript files.

In switching to AMD, the compile step is much more resource intensive.
It takes so long, there is no way we could do this real-time.
Additionally, it can not be done in Python.

When changes are made to existing bundles, re-compilation will need to be done TTW (Trough-The-Web)
in the Resource Registries control panel.

There is a build button next to each bundle.
For advanced users, compilation can be done using a tool like grunt in your development environment.

Conditional Resources
~~~~~~~~~~~~~~~~~~~~~

In Plone 5, individual resources can not be registered conditionally to certain page.
This is due to the way we build JavaScript with AMD.

Instead we have Python helper-methods in the Resource Registry to add custom JS and CSS to your views or forms.

Instead of using the legacy fill-slot like this (Plone 4):

..  code-block:: xml

    <metal:slot fill-slot="javascript_head_slot">
      ...
    </metal:slot>
    <metal:slot fill-slot="css_slot">
      ...
    </metal:slot>

In Plone 5 it’s recommended to instead use the new Python methods you can find in ``Products.CMFPlone.resources``:

..  code-block:: python

    from Products.CMFPlone.resources import add_bundle_on_request
    from Products.CMFPlone.resources import add_resource_on_request

    add_resource_on_request(self.request, 'jquery.recurrenceinput')
    add_bundle_on_request(self.request, 'thememapper')

This is better than always loading a resource or bundle for your whole site.

Only bundles can be conditionally included.
If you have a resource that needs to be conditionally included, it will likely need its own bundle.


Control Panel
=============

In Plone 4.x, the Plone configuration settings have been stored as portal properties spread across the Management Interface.
In Plone 5, those settings are all stored as plone.app.registry entries in registry.xml.

There are now sections in the control panel, this can be set from the controlpanel.xml.
See the current definitions for more information.

The display of icons for control panels is now controlled by css.
The name of the control panel is normalized into a css class, which is applied to the link in the main layout of all control panels.

For example, if the “appId” of your control panel (as set in controlpanel.xml in your install profile)
is “MyPackage” then the css class that will be generated is “.icon-controlpanel-MyPackage”.

To have an icon for your control panel you must make sure that a css rule exists for that generated css class.

An example might be

.. code-block:: css

    .icon-controlpanel-MyPackage:before { content: ‘\e844’; }

The value you use for this css rule should identify one of the fontello icons included in Plone,
or a font-based icon provided by your package itself.

It is not possible at this time to set an icon for your add-on package control panels without including css in your package.

For documentation on how to use it in your own add-ons see http://training.plone.org/5/registry.html

Properties
----------

In the past editor settings were part of the portal properties which contained a site properties object with the relevant attributes.

site properties allowed direct attribute access, so you could access the available_editors via::

    ptools.site_properties.available editors

Now you can access the property via get_registry_record()

.. code-block:: python

    >>> from plone import api
    >>> api.portal.get_registry_record('plone.available_editors')

The keys mostly the same, they are only prefixed with `plone.` now.
Normally, you do not modify or access these records.

Instead you change the settings in your genericsetup profile in the file `propertiestool.xml`

+--------------------+-----------------------------------+-----------------------------------------+
| Old Property Sheet | Old Key                           | New Property                            |
+--------------------+-----------------------------------+-----------------------------------------+
| navtree_properties | sortAttribute                     | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| navtree_properties | sortOrder                         | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| navtree_properties | sitemapDepth                      | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| navtree_properties | root                              | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| navtree_properties | currentFolderOnlyInNavtree        | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| navtree_properties | includeTop                        | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| navtree_properties | topLevel                          | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| navtree_properties | bottomLevel                       | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| navtree_properties | showAllParents                    | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| navtree_properties | idsNotToList                      | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| navtree_properties | parentMetaTypesNotToQuery         | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| navtree_properties | metaTypesNotToList                | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| navtree_properties | enable_wf_state_filtering         | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| navtree_properties | wf_states_to_show                 | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | allowAnonymousViewAbout           | plone.allow_anon_views_about            |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | displayPublicationDateInByline    | plone.display_publication_date_byline   |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | default_language                  | plone.default_language                  |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | default_charset                   | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | ext_editor                        | plone.ext_editor                        |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | available_editors                 | plone.available_editors                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | default_editor                    | plone.default_editor                    |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | allowRolesToAddKeywords           | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | autho_cookie_length               | plone.auth_cookie_length                |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | calendar_starting_year            | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | calender_future_years_available   | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | invalid_ids                       | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | default_page                      | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | search_results_description_length | plone.search_results_description_length |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | ellipsis                          | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | typesLinkToFolderContentsInFC     | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | visible_ids                       | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | exposeDCMetaTags                  | plone.exposeDCMetaTags                  |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | types_not_searched                | plone.types_not_searched                |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | search_review_state_for_anon      | **REMOVED**                             |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | search_enable_description_search  | **REMOVED**                             |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | search_enable_sort_on             | **REMOVED**                             |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | search_enable_batch_size          | **REMOVED**                             |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | search_collapse_options           | **REMOVED**                             |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | disable_folder_section            | **SPECIAL**                             |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | disable_nonfolderish_sections     | **REMOVED**                             |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | typesUseViewActionInListings      | plone.types_use_view_action_in_listings |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | verify_login_name                 | plone.verify_login_name                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | many_users                        | plone.many_users                        |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | many_groups                       | plone.many_groups                       |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | enable_livesearch                 | plone.enable_livesearch                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | default_page_types                | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | use_folder_contents               | **REMOVED**                             |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | forbidden_contenttypes            | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | default_contenttype               | **REMOVED**                             |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | enable_sitemap                    | plone.enable_sitemap                    |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | number_of_days_to_keep            | **REMOVED**                             |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | enable_inline_editing             | **REMOVED**                             |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | lock_on_ttw_edit                  | plone.lock_on_ttw_edit                  |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | enable_link_integrity_checks      | plone.enable_link_integrity_checks      |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | webstats_js                       | plone.webstats_js                       |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | external_links_open_new_window    | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | icon_visibility                   | plone.icon_visibility                   |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | mark_special_links                | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | redirect_links                    | **TBD**                                 |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | use_email_as_login                | plone.use_email_as_login                |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | user_registration_fields          | **SPECIAL**                             |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | allow_external_login_sites        | plone.allow_external_login_sites        |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | external_login_url                | plone.external_login_url                |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | external_logout_url               | plone.extenal_logout_url                |
+--------------------+-----------------------------------+-----------------------------------------+
| site_properties    | external_login_iframe             | plone.external_login_iframe             |
+--------------------+-----------------------------------+-----------------------------------------+

disable_folder_sections
-----------------------

This property has been removed and the logic is different.
You can influence the portal tab generation with the property `plone.generate_tabs`
This controls, if the tabs are generated from the content in the root folder.

In addition, you can control if non folders will create entries or not with the property `plone.nonfolderish_tabs`.
If you want to disable_folder_sections, you will want to set `plone.generate_tabs` to false.

Generic Setup
-------------

All settings for control panels are stored in the registry.xml Generic Setup file.
This file can be exported through the Management Interface.

Go to the Plone Site Setup, choose :guilabel:`Management Interface` from the "Advanced" section.
Click on :guilabel:`portal_setup`.
Go to the "export" tab.
Choose the :guilabel:`Export the configuration registry schemata` check-box and
click the :guilabel:`Export selected steps` button.

The registry.xml file will contain entries like this

.. code-block:: xml

  <record name="plone.available_editors"
          interface="Products.CMFPlone.interfaces.controlpanel.IEditingSchema" field="available_editors">
    <value>
      <element>TinyMCE</element>
      <element>None</element>
    </value>
  </record>

  <record name="plone.available_languages" interface="Products.CMFPlone.interfaces.controlpanel.ILanguageSchema" field="available_languages">
    <value>
      <element>en-us</element>
    </value>
  </record>

Drop the settings you want to change into registry.xml in you Generic Setup profile folder.

Re-install your add-on product and the settings will be available.


Python Code
-----------

All Generic Setup settings can be looked up with Python code.

First we lookup the registry utility

.. code-block:: python

   >>> from zope.component import getUtility
   >>> from plone.registry.interfaces import IRegistry
   >>> registry = getUtility(IRegistry)

Now we use the schema 'ISearchSchema' to lookup for a RecordProxy object with
all fields

.. code-block:: python

   >>> from Products.CMFPlone.interfaces import ISearchSchema
   >>> search_settings = registry.forInterface(ISearchSchema, prefix='plone')

Now we an get and set all fields of the schema above like

.. code-block:: python

   >>> search_settings.enable_livesearch
   True

If you want to change a setting, change the attribute

.. code-block:: python

   >>> search_settings.enable_livesearch = False

Now the enable_livesearch should disabled

.. code-block:: python

   >>> search_settings.enable_livesearch
   False


Editing Control Panel
---------------------

Plone 5.x

.. code-block:: python

   >>> from Products.CMFPlone.interfaces import IEditingSchema
   >>> editing_settings = registry.forInterface(IEditingSchema, prefix='plone')

  >>> editing_settings.default_editor
  u'TinyMCE'

  >>> editing_settings.ext_editor
  False

  >>> editing_settings.enable_link_integrity_checks
  True

  >>> editing_settings.lock_on_ttw_edit
  True


Language Control Panel
----------------------

All settings were managed with the tool `portal_languages` and with the GenericSetup file portal_languages.xml.
Now these attributes are managed with Plone properties.

As Plone 5 has full migration during an upgrade, please perform the upgrade and
export the registry settings in GenericSetup to get the right settings.

If you access attributes directly in your code, you must change your accessors.
You know already how to get attributes from the `portal_languages` tool.

The new attributes can be accessed via plone.api as described above.

+-----------------------------------------------------------------------------------+-----------------------------------+
| old attribute                                                                     | new attribute                     |
+-----------------------------------------------------------------------------------+-----------------------------------+
| root.portal_languages.supported_langs                                             | plone.available_languages         |
+-----------------------------------------------------------------------------------+-----------------------------------+
| site.portal_properties.site_properties.default_language or  site.default_language | plone.default_language            |
+-----------------------------------------------------------------------------------+-----------------------------------+
| root.portal_languages.use_combined_language_codes                                 | plone.use_combined_language_codes |
+-----------------------------------------------------------------------------------+-----------------------------------+
| root.portal_languages.display_flags                                               | plone.display_flags               |
+-----------------------------------------------------------------------------------+-----------------------------------+
| portal_languages.use_path_negotiation                                             | plone.use_path_negotiation        |
+-----------------------------------------------------------------------------------+-----------------------------------+
| portal_languages.use_content_negotiation                                          | plone.use_content_negotiation     |
+-----------------------------------------------------------------------------------+-----------------------------------+
| portal_languages.use_cookie_negotiation                                           | plone.use_cookie_negotiation      |
+-----------------------------------------------------------------------------------+-----------------------------------+
| portal_languages.set_cookie_everywhere                                            | plone.set_cookie_always           |
+-----------------------------------------------------------------------------------+-----------------------------------+
| portal_languages.authenticated_users_only                                         | plone.authenticated_users_only    |
+-----------------------------------------------------------------------------------+-----------------------------------+
| portal_languages.use_request_negotiation                                          | plone.use_request_negotiation     |
+-----------------------------------------------------------------------------------+-----------------------------------+
| portal_languages.use_cctld_negotiation                                            | plone.use_cctld_negotiation       |
+-----------------------------------------------------------------------------------+-----------------------------------+
| portal_languages.use_subdomain_negotiation                                        | plone.use_subdomain_negotiation   |
+-----------------------------------------------------------------------------------+-----------------------------------+
| portal_languages.always_show_selector                                             | plone.always_show_selector        |
+-----------------------------------------------------------------------------------+-----------------------------------+

Plone 5.x

.. code-block:: python

   >>> from Products.CMFPlone.interfaces import ILanguageSchema
   >>> language_settings = registry.forInterface(ILanguageSchema, prefix='plone')

   >>> language_settings.available_languages
   ['en']

Mail Control Panel
------------------

All settings were managed with the tool `MailHost` and with the GenericSetup file portal_languages.xml.
Now these attributes are managed with Plone properties.

As Plone 5 has full migration during an upgrade,
please perform the upgrade and export the registry settings in GenericSetup to get the right settings.

If you access attributes directly in your code, you must change your accessors.

You know already how to get attributes from the `portal_languages` tool.
The new attributes can be accessed via plone.api as described above.

+-----------------------------+--------------------------+
| old attribute               | new attribute            |
+-----------------------------+--------------------------+
| MailHost.smtp_host          | plone.smtp_host          |
+-----------------------------+--------------------------+
| MailHost.smtp_port          | plone.smtp_port          |
+-----------------------------+--------------------------+
| MailHost.smtp_user_id       | plone.smtp_user_id       |
+-----------------------------+--------------------------+
| MailHost.smtp_pass          | plone.smtp_pass          |
+-----------------------------+--------------------------+
| MailHost.email_from_address | plone.email_from_address |
+-----------------------------+--------------------------+
| MailHost.email_from_name    | plone.email_from_name    |
+-----------------------------+--------------------------+


Maintenance Control Panel
-------------------------

Plone 5.x

.. code-block:: python

   >>> from Products.CMFPlone.interfaces import IMaintenanceSchema
   >>> maintenance_settings = registry.forInterface(IMaintenanceSchema, prefix='plone')

   >>> maintenance_settings.days
   7


Navigation Control Panel
------------------------

Plone 5.x

.. code-block:: python

   >>> from Products.CMFPlone.interfaces import INavigationSchema
   >>> navigation_settings = registry.forInterface(INavigationSchema, prefix='plone')

   >>> navigation_settings.generate_tabs
   True

   >>> navigation_settings.nonfolderish_tabs
   True

   >>> navigation_settings.displayed_types
   ('Image', 'File', 'Link', 'News Item', 'Folder', 'Document', 'Event')

   >>> navigation_settings.filter_on_workflow
   False

   >>> navigation_settings.workflow_states_to_show
   ()

   >>> navigation_settings.show_excluded_items
   True


Search Control Panel
--------------------

Plone 5.x

.. code-block:: python

   >>> from Products.CMFPlone.interfaces import ISearchSchema
   >>> search_settings = registry.forInterface(ISearchSchema, prefix='plone')

   >>> search_settings.enable_livesearch
   False

   >>> search_settings.types_not_searched
   (...)


Site Control Panel
------------------

Plone 4.x

.. code-block:: python

   >>> portal = getSite()
   >>> portal_properties = getToolByName(portal, "portal_properties")
   >>> site_properties = portal_properties.site_properties

  >>> portal.site_title = settings.site_title
   >>> portal.site_description = settings.site_description
   >>> site_properties.enable_sitemap = settings.enable_sitemap
   >>> site_properties.exposeDCMetaTags = settings.exposeDCMetaTags
   >>> site_properties.webstats_js = settings.webstats_js

   >>> settings.enable_sitemap -> plone.app.layout

Plone 5.x

.. code-block:: python

   >>> from Products.CMFPlone.interfaces import ISiteSchema
   >>> site_settings = registry.forInterface(ISiteSchema, prefix='plone')

   >>> site_settings.site_title
   u'Plone site'

   >>> site_settings.exposeDCMetaTags
   False

   >>> site_settings.enable_sitemap
   False

   >>> site_settings.webstats_js
   u''


Overview Control Panel
----------------------

Plone 5.x

.. code-block:: python

   >>> from Products.CMFPlone.interfaces.controlpanel import IDateAndTimeSchema
   >>> tz_settings = registry.forInterface(IDateAndTimeSchema, prefix='plone')

   >>> tz_settings.portal_timezone = 'UTC'


Markup Control Panel
--------------------

Plone 5.x

.. code-block:: python

   >>> from Products.CMFPlone.interfaces import IMarkupSchema
   >>> markup_settings = registry.forInterface(IMarkupSchema, prefix='plone')

   >>> markup_settings.default_type
   u'text/html'

   >>> markup_settings.allowed_types
   ('text/html', 'text/x-web-textile')


User and Groups Control Panel
-----------------------------

Plone 5.x

.. code-block:: python

   >>> from Products.CMFPlone.interfaces import IUserGroupsSettingsSchema
   >>> usergroups_settings = registry.forInterface(IUserGroupsSettingsSchema, prefix='plone')

   >>> usergroups_settings.many_groups
   False

   >>> usergroups_settings.many_users
   False


portal_languages is now a utility
=================================

Part of the work on PLIP 13091 (plone.app.multilingual) required to move ``portal_languages`` to a utility.

Code that used to look like this::


  # OLD 4.x approach
  portal.portal_languages.getDefaultLanguage()

Now it should look like this::

  # NEW in 5.0
  language_tool = api.portal.get_tool('portal_languages')
  language_tool.getDefaultLanguage()


Tests Changes
=============

In Plone 4.x a date or date time widget used to be rendered as a set of input fields

.. code-block:: python

   # OLD 4.x approach
   browser_manager.getControl(name='form.widgets.IPublication.effective-year').value = '2015'
   browser_manager.getControl(name='form.widgets.IPublication.effective-month').value = ['10']
   browser_manager.getControl(name='form.widgets.IPublication.effective-day').value = '11'
   browser_manager.getControl(name='form.widgets.IPublication.effective-hour').value = '15'
   browser_manager.getControl(name='form.widgets.IPublication.effective-min').value = '14'

Now the same input field will be rendered as a single string input

.. code-block:: python

   # NEW in 5.0
   browser_manager.getControl(name='form.widgets.IPublication.effective').value = '2015-10-11 15:14'


Deprecation Of ``portal_properties.xml``
========================================

``portal_properties.xml`` Generic Setup import step is now deprecated and has been moved to plone.registry.


parentMetaTypesNotToQuery
-------------------------

.. code-block:: xml

  # OLD 4.x approach
  <object name="portal_properties">
    <object name="navtree_properties">
      <property name="parentMetaTypesNotToQuery" purge="false">
        <element value="my.hidden.content.type" />
      </property>
    </object>
  </object>

Now in ``registry.xml`` should look like

.. code-block:: xml

  # NEW in 5.0
  <?xml version="1.0"?>
  <registry>
    <record
        name="plone.parent_types_not_to_query"
        interface="Products.CMFPlone.interfaces.controlpanel.INavigationSchema"
        field="parent_types_not_to_query">
      <value>
        <element value="my.hidden.content.type" />
      </value>
    </record>
  </registry>

metaTypesNotToList
------------------

.. code-block:: xml

  # OLD 4.x approach
  <?xml version="1.0"?>
  <object name="portal_properties">
    <object name="navtree_properties">
      <property name="metaTypesNotToList" purge="false">
        <element value="my.hidden.content.type" />
      </property>
  </object>

*nothing* should  be done in Plone 5.

The new setting is on ``Products.CMFPlone.interfaces.controlpanel.INavigationSchema.displayed_types``
and it works the other way around.

Instead of blacklisting content types it whitelists them,
if you don't want your content type to show there's nothing to do.

typesLinkToFolderContentsInFC
-----------------------------

.. code-block:: xml

  # OLD 4.x approach
  <?xml version="1.0"?>
  <object name="portal_properties">
    <object name="site_properties">
      <property name="typesLinkToFolderContentsInFC" purge="false">
        <element value="my.fancy.content.type" />
      </property>
    </object>
  </object>

Now in ``registry.xml`` should look like

.. code-block:: xml

  # NEW in Plone 5
  <record
      name="plone.types_use_view_action_in_listings"
      interface="Products.CMFPlone.interfaces.controlpanel.ITypesSchema"
      field="types_use_view_action_in_listings">
    <value>
      <element>my.fancy.content.type</element>
    </value>
  </record>


types_not_searched
------------------

.. code-block:: xml

  # OLD 4.x approach
  <?xml version="1.0"?>
  <object name="portal_properties">
    <object name="site_properties">
      <property name="types_not_searched" purge="false">
        <element value="my.fancy.content.type" />
      </property>
    </object>
  </object>


Now in ``registry.xml`` should look like

.. code-block:: xml

  # NEW in Plone 5
  <?xml version="1.0"?>
  <registry>
    <record
        name="plone.types_not_searched"
        interface="Products.CMFPlone.interfaces.controlpanel.ISearchSchema"
        field="types_not_searched">
      <value>
        <element>my.fancy.content.type</element>
      </value>
    </record>
  </registry>
