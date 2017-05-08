======================================================
Add-on Installation And Export framework: GenericSetup
======================================================

.. admonition:: Description

    GenericSetup is a framework to modify the Plone site during add-on package installation and uninstallation.

    It provides XML-based rules to change the site settings.


Introduction
============

GenericSetup is an XML-based way to import and export Plone site configurations.

It is mainly used to prepare the Plone site for add-on packages, by:

* registering CSS files,
* registering JavaScript files,
* setting various properties,
* registering portlets,
* registering portal_catalog search query indexes,
* ... etc ...

GenericSetup is mostly used to apply an add-on's specific changes to the site configuration and to enable specific behaviors when the add-on installer is run.

GenericSetup XML files are usually in a ``profiles/default`` folder inside the add-on package.

All run-time through-the-web (:term:`TTW`) configurable items, like viewlets order through ``/@@manage-viewlets`` page, are made repeatable using GenericSetup profile files.

You do not need to hand-edit GenericSetup profile files.

You can always change the configuration options through Plone or using the Management Interface, and then you export the resulting profile as an XML file, using the *Export* tab in ``portal_setup`` accessible from the Management Interface.

Directly editing XML profile files does not change anything on the site, even after Zope restart.
This is because run-time TTW configurable items are stored in the database.

If you edit profile files, you need to either reimport the edited files using the ``portal_setup`` tool or fully rerun the add-on package installer in Plone control panel.

This import will read XML files and change the Plone database accordingly.

.. note::

    Difference between ZCML and GenericSetup

    ZCML changes affect loaded Python code in **all** sites inside Zope whereas GenericSetup XML files affect only one Plone site and its database.
    GenericSetup XML files are always database changes.

    Relationship between ZCML and site-specific behavior is usually done using :doc:`layers </develop/plone/views/layers>`.
    ZCML directives, like viewlets and views, are registered to be active only on a certain layer using ``layer`` attribute.
    When GenericSetup XML is imported through ``portal_setup``, or the add-on package installer is run for a Plone site, the layer is activated for the particular site only, enabling all views registered for this layer.

.. note::

    The ``metadata.xml`` file (add-on dependency and version information) is read during Plone start-up.
    If this file has problems, your add-on might not appear in the installer control panel.

.. * Not publicly viewable anymore: `GenericSetup tutorial <https://old.plone.org/documentation/tutorial/genericsetup>`_

* `GenericSetup package page <https://pypi.python.org/pypi/Products.GenericSetup>`_.

* `GenericSetup source code <https://github.com/zopefoundation/Products.GenericSetup>`_.


Creating A Profile
==================

You use ``<genericsetup>`` directive in your add-on package's ``configure.zcml``.
The name for the default profile executed by the Plone add-on installer is ``default``.

If you need different profiles, for example for unit testing, you can declare them here.

XML files for the ``default`` profile go in the ``profiles/default`` folder inside your add-on package.

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
        i18n_domain="your.addonpackage">

      <genericsetup:registerProfile
          name="default"
          title="your.addonpackage (installation profile)"
          directory="profiles/default"
          description='Your add-on package installation profile'
          provides="Products.GenericSetup.interfaces.EXTENSION"
          />

    </configure>


Multiple Profiles
-----------------

When you have more than one profile in your add-on package, the add-ons control panel needs to decide which one to use when you install it.

Since Plone 5.1, when there is a ``default`` profile, it is always used as the installation profile, regardless of other profile names.

Exception: when this ``default`` profile is marked in an ``INonInstallable`` utility, it is ignored and Plone falls back to using the first from the alphabetical sorting.

.. note::

    In Plone 5.0 and lower,
    the profiles are sorted alphabetically by id,
    and the first one is chosen.
    If you have profiles ``base`` and ``default``,
    the ``base`` profile is installed.
    It is recommended to let ``default`` be the alphabetically first profile.


Add-on-specific Issues
======================

Add-on packages may contain:

* A default GenericSetup XML profile which is automatically run when the package is installed using the quick-installer.
  The profile name is usually ``default``.

* Other profiles which the user may install using the ``portal_setup`` *Import* tab, or which can be manually enabled for unit tests.

* An "Import various" step, which runs Python code every time the GenericSetup XML profile is installed.
  See :ref:`custominstall`.

* A ``pre_handler`` or ``post_handler`` when you use GenericSetup 1.8.2 or higher.
  See note at :ref:`custominstall`.

For more information about custom import steps, see:

* http://plone.293351.n2.nabble.com/indexing-of-content-created-by-Generic-Setup-td4454703.html


Listing Available Profiles
==========================

Example::

    # List all profiles know to the Plone instance.
    setup_tool = self.portal.portal_setup

    profiles = setup_tool.listProfileInfo()
    for profile in profiles:
       print str(profile)

Sample results:

.. code-block:: python

    {'product': 'PluggableAuthService',
     'description': 'Content for an empty PAS (plugins registry only).',
     'for': <InterfaceClass Products.PluggableAuthService.interfaces.authservice.IPluggableAuthService>,
     'title': 'Empty PAS Content Profile',
     'version': 'PluggableAuthService-1.5.3',
     'path': 'profiles/empty',
     'type': 1,
     'id': 'PluggableAuthService:empty'}
    {'product': 'Products.CMFPlone',
     'description': u'Profile for a default Plone.',
     'for': <InterfaceClass Products.CMFPlone.interfaces.siteroot.IPloneSiteRoot>,
     'title': u'Plone Site',
     'version': u'3.1.7',
     'path': u'/home/moo/sits/parts/plone/CMFPlone/profiles/default',
     'type': 1,
     'id': u'Products.CMFPlone:plone'}
    ...


Installing A Profile
====================

This is usually unit test specific question how to enable certain add-ons for unit testing.


plone.app.testing
-----------------

See `Product and profile installation <http://docs.plone.org/external/plone.app.testing/docs/source/README.html#product-and-profile-installation>`_.


Manually
--------

You might want to install profiles manually if they need to be enabled only for certain tests.

The profile name is in the format ``profile-${package_name}:${profile id}``

Unit testing example::

    # Run the extended profile of the "your.addonpackage" package.
    setup_tool.runAllImportStepsFromProfile('profile-your.addonpackage:extended')

.. versionadded:: 4.3.8

    Since Products.GenericSetup 1.8.0 (Plone 4.3.8, Plone 5.0.0) the ``profile-`` part is optional.
    The code can handle both.


Missing Upgrade Procedure
=========================

In the Add-ons control panel you may see a warning that your add-on package is `missing an upgrade procedure <http://stackoverflow.com/questions/15316583/how-to-define-a-procedure-to-upgrade-an-add-on>`_.

This means you need to write some `Upgrade steps`_.


Uninstall Profile
=================

For the theory, see `<http://blog.keul.it/2013/05/how-to-make-your-plone-add-on-products.html>`_

For an example, see the `collective.pdfpeek source code <https://github.com/collective/collective.pdfpeek/tree/master/collective/pdfpeek/profiles>`_.

When you deactivate an add-on in the control panel, Plone looks for a profile with the name ``uninstall`` and applies it.

.. versionadded:: 5.1

    If there is no ``uninstall`` profile, a warning is displayed before installing the add-on.
    If you do activate the add-on, no deactivate button will be shown.

.. versionadded:: 5.1

    The add-ons control panel no longer does an automatic partial cleanup,
    for example removing added skins and css resources.
    This was always only partial, you could not rely on it to fully cleanup the site.

.. note::

    This method works in Plone 4.3.7 and higher.
    If you need to support older versions, you may need to write an ``Extensions/install.py`` file with an ``uninstall`` method.
    See older versions of this document for more information.


Dependencies
============

GenericSetup profile can contain dependencies to other add-on package installers and profiles.

For example, if you want to declare a dependency to the *your.addonpackage* package, that it is automatically installed when your add-on is installed,
you can use the declaration below.

This way you can be sure that all layers, portlets and other features which require database changes are usable from *your.addonpackage* when it is run.

``metadata.xml``:

.. code-block:: xml

    <?xml version="1.0"?>
    <metadata>
     <version>1000</version>
     <dependencies>
       <dependency>profile-your.addonpackage:default</dependency>
     </dependencies>
    </metadata>

*your.addonpackage* declares the profile in its configure.zcml:

.. code-block:: xml

    <genericsetup:registerProfile
        name="default"
        title="your.addonpackage"
        directory="profiles/default"
        description='Your add-on package installation profile'
        provides="Products.GenericSetup.interfaces.EXTENSION"
        />


.. warning::

   Unlike other GenericSetup XML files, ``metadata.xml`` is read on the start-up and this read is cached.
   Always restart Plone after editing ``metadata.xml``.

   If your ``metadata.xml`` file contains syntax errors or dependencies to a missing or non-existent package (e.g. due to a typo in a name) your add-on will disappear from the installation control panel.

.. note::

   For some old add-ons in the ``Products.*`` Python namespace, you must not include the full package name in the dependencies.

   This is true when this add-on has registered its profile in Python instead of zcml, and there it has used only part of its package name.

   In most cases you *do* need to use the full ``Products.xxx`` name.

To declare a dependency on the ``simple`` profile of ``Products.PluggableAuthService``:

.. code-block:: xml

    <?xml version="1.0"?>
    <metadata>
      <version>1000</version>
      <!-- Install the simple PluggableAuthService profile on the site when this add-on is installed. -->
      <dependencies>
        <dependency>profile-PluggableAuthService:simple</dependency>
      </dependencies>
    </metadata>


Metadata version numbers
========================

Some old add-on packages may have a ``metadata.xml`` without version number, but this is considered bad practice.

What should the version number in your ``metadata.xml`` be?

This mostly matters when you are adding upgrade steps, see also the `Upgrade steps`_ section.

Upgrade steps have a sort order in which they are executed. This used to be alphabetical sorting.

When you had eleven upgrade steps, marked from 1 through 11, alphabetical sorting meant this order: 1, 10, 11, 2, 3, etc.

If you are seeing this, then you are using an old version of GenericSetup.

You want numerical sorting here, which is correctly done currently. Versions with dots work fine too.

They get ordered just like they would when used for packages on PyPI.

Best practice for all versions of GenericSetup is this:

- Start with 1000.
  This avoids problems with ancient GenericSetup that used alphabetical sorting.

- Simply increase the version by 1 each time you need a new metadata version.
  For example: 1001, 1002, etc.

- If your add-on package version number changes, but your profile stays the same and no upgrade step is needed, you should **not** change the metadata version.
  There is no need.

- If you make changes for a new major release, you should increase the metadata version significantly.
  This leaves room for small metadata version increases on a maintenance branch.
  Example:
  You have branch master with version 1025.
  You make backwards incompatible changes and you increase the version to 2000.
  You create a maintenance branch where the next metadata version will be 1026.


.. _custominstall:

Custom Installer Code (``setuphandlers.py``)
============================================

Besides out-of-the-box XML steps which provide both install and uninstall,
GenericSetup provides a way to run custom Python code when your add-on package is installed and uninstalled.

This is not a very straightforward process, though.

.. note::

    An easier way may be possible for you.
    GenericSetup 1.8.2 has an option to point to a function to run before or after applying all import steps for your profile.

    If you do not need to support older versions, this is the easiest way.

    In ``configure.zcml``::

        <configure
            xmlns="http://namespaces.zope.org/zope"
            xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
            i18n_domain="your.addonpackage">

          <genericsetup:registerProfile
              name="default"
              title="Your Add-on Package"
              directory="profiles/default"
              description="A useful package"
              provides="Products.GenericSetup.interfaces.EXTENSION"
              pre_handler="your.addonpackage.setuphandlers.run_before"
              post_handler="your.addonpackage.setuphandlers.run_after"
              />

        </configure>

    In ``setuphandlers.py``::

        def run_before(context):
            # This is run before running the first import step of
            # the default profile.  context is portal_setup.
            # If you need the same context as you would get in
            # an import step, like setup_various below, do this:
            profile_id = 'profile-your.addonpackage:default'
            good_old_context = context._getImportContext(profile_id)
            ...

        def run_after(context):
            # This is run after running the last import step of
            # the default profile.  context is portal_setup.
            ...

The best practice is to create a ``setuphandlers.py`` file which contains a function ``setup_various()`` which runs the required Python code
to make changes to Plone site object.

This function is registered as a custom ``genericsetup:importStep`` in XML.

.. note::

    When you write a custom ``importStep``, remember to write uninstallation code as well.

However, the trick is that all GenericSetup import steps, including your custom step, are run for *every* add-on package when they are installed.

If your need to run code which is **specific to your add-on install only** you need to use a marker text file which is checked by the GenericSetup context.

Also you need to register this custom import step in ``configure.zcml``:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup">

      <genericsetup:importStep
          name="your.addonpackage"
          title="your.addonpackage special import handlers"
          description=""
          handler="your.addonpackage.setuphandlers.setup_various"
          />

    </configure>

You can run other steps before yours by using the ``depends`` directive.

For instance, if your import step depends on a content type to be installed first, you must use:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup">

      <genericsetup:importStep
          name="your.addonpackage"
          title="your.addonpackage special import handlers"
          description=""
          handler="your.addonpackage.setuphandlers.setup_various">
        <depends name="typeinfo" />
      </genericsetup:importStep>

    </configure>

``setuphandlers.py`` example

.. code-block:: python

    __docformat__ = "epytext"

    def run_custom_code(site):
        """Run custom add-on package installation code to modify Plone
           site object and others

        @param site: Plone site
        """

    def setup_various(context):
        """
        @param context: Products.GenericSetup.context.DirectoryImportContext instance
        """

        # We check from our GenericSetup context whether we are running
        # add-on installation for your package or any other
        if context.readDataFile('your.addonpackage.marker.txt') is None:
            # Not your add-on
            return

        portal = context.getSite()

        run_custom_code(portal)

And add a dummy text file
``your.addonpackage/your/addonpackage/profiles/default/your.addonpackage.marker.txt``::

    This text file can contain any content - it just needs to be present

More information

* http://keeshink.blogspot.com/2009/02/creating-portal-content-in.html

* http://maurits.vanrees.org/weblog/archive/2009/12/catalog (unrelated, but contains pointers)


Overriding Import Step Order
============================

If you need to override the order of import steps in a package that is not yours,
it might work if you `use an overrides.zcml <http://plone.293351.n2.nabble.com/Overriding-import-step-order-td2189638.html>`_.


Controlling The Import Step Execution Order
-------------------------------------------

If you need to control the execution order of one of your own custom import steps, you can do this in your import step definition in zcml.

To make sure the catalog and typeinfo steps are run before your own step, use this code:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
        i18n_domain="poi">

      <genericsetup:importStep
          name="poi_various"
          title="Poi various import handlers"
          description=""
          handler="Products.Poi.setuphandlers.import_various">
        <depends name="catalog"/>
        <depends name="typeinfo"/>
      </gs:importStep>

    </configure>

.. note::

    The name that you need, is usually the name of the related xml file, but with the ``.xml`` stripped.
    For the ``catalog.xml`` the import step name is ``catalog``.
    But there are exceptions.

    For the ``types.xml`` and the ``types`` directory, the import step name is ``typeinfo``.

    See the section on `Generic Setup files`_ for a list.

* http://plone.293351.n2.nabble.com/indexing-of-content-created-by-Generic-Setup-td4454703.html


Upgrade Steps
=============

You can define upgrade steps to run code when someone upgrades your package from version *x* to *y*.

As an example, let's say that the new version of your.addonpackage defines a *price* field on a content type *MyType* to be a string,
but previously (version 1.1 and earlier) it was a float.

Code that uses this field and assumes it to be a float will break after the upgrade, you'd like to automatically convert existing values for the field to string.

You could do this in a script, but having a GenericSetup upgrade step means non-technical people can do it as well.

Once you have the script, it's code can be to put in an upgrade step.


Increment Profile Version
-------------------------

First increase the number of the version in the ``profiles/default/metadata.xml``.
This version number should be an integer.

Package version are different because they add sense like the status of the add-on: is it stable, is it in development, in beta, which branch is it.

A profile version indicates only that you have to migrate data in the database.


Add Upgrade Step
----------------

Next we add an upgrade step:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
        i18n_domain="your.addonpackage">

      <genericsetup:upgradeStep
          title="Convert Price to strings"
          description="Price was previously a float field, it should be converted to string"
          source="1000"
          destination="1100"
          handler="your.addonpackage.upgrades.convert_price_to_string"
          sortkey="1"
          profile="your.addonpackage:default"
          />

    </configure>


* You can use a wildcard character for *source* to indicate an upgrade for any previous version.
  Since Products.GenericSetup 1.7.6 this works fine.
  To run the upgrade step only when upgrading from a specific version, use that version's number.

* The optional ``sortkey`` can be used to indicate the order in which upgrade steps from the same source to destination are run.


Add Upgrade Code
----------------

The code for the upgrade method itself is best placed in a *upgrades.py* module::

    from plone import api
    import logging

    PROFILE_ID = 'profile-your.addonpackage:default'


    def convert_price_to_string(context, logger=None):
        """Method to convert float Price fields to string.

        When called from the import_various method, 'context' is
        the plone site and 'logger' is the portal_setup logger.

        But this method will be used as upgrade step, in which case 'context'
        will be portal_setup and 'logger' will be None."""

        if logger is None:
            # Called as upgrade step: define our own logger.
            logger = logging.getLogger('your.addonpackage')

        # Run the catalog.xml step as that may have defined new metadata
        # columns.  We could instead add <depends name="catalog"/> to
        # the registration of our import step in zcml, but doing it in
        # code makes this method usable as upgrade step as well.
        # Remove these lines when you have no catalog.xml file.
        setup = api.portal.get_tool('portal_setup')
        setup.runImportStepFromProfile(PROFILE_ID, 'catalog')

        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='MyType')
        count = 0
        for brain in brains:
            current_price = brain.getPrice
            if type(current_price) != type('a string'):
                obj = brain.getObject()
                obj.setPrice(str(current_price))
                obj.reindexObject()
                count += 1

        setup.runImportStepFromProfile(PROFILE_ID, 'catalog')
        logger.info('%s fields converted.' % count)

Other examples of using generic setup to run import steps are below.

If you want to call ``types.xml`` use ``typeinfo``::

        setup.runImportStepFromProfile(PROFILE_ID, 'typeinfo')

If you want to call ``workflow.xml`` use ``workflow``::

        setup.runImportStepFromProfile(PROFILE_ID, 'workflow')

The ids of the various default import steps are defined in several places.

Some of the most used ones are here:

* https://github.com/zopefoundation/Products.CMFCore/blob/master/Products/CMFCore/exportimport/configure.zcml

* https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/exportimport/configure.zcml

After restarting Zope, your upgrade step should be visible in the Management Interface:
the ``portal_setup`` tool has a tab ``Upgrades``.

Select your package profile to see which upgrade steps Zope knows about for your add-on.


upgradeDepends
--------------

In an upgrade step you can apply a specific import step from your profile:

.. code-block:: xml

    <genericsetup:upgradeDepends
        source="3900"
        destination="4000"
        profile="your.addonpackage:default"
        title="Apply rolemap.xml.
               This is implicitly taken from the profile this upgradeStep is defined for."
        import_steps="rolemap" />

You can apply multiple steps, separated by a space:

.. code-block:: xml

    <genericsetup:upgradeDepends
        source="3900"
        destination="4000"
        profile="your.addonpackage:default"
        import_steps="cssregistry jsregistry" />

You can apply steps from a different profile:

.. code-block:: xml

    <genericsetup:upgradeDepends
        source="3900"
        destination="4000"
        profile="your.addonpackage:default"
        title="Apply skins.xml from our plone4 profile"
        import_profile="your.addonpackage:plone4"
        import_steps="skins" />

You can apply a complete profile:

.. code-block:: xml

    <genericsetup:upgradeDepends
        source="3900"
        destination="4000"
        profile="your.addonpackage:default"
        title="Install our complete cache profile"
        import_profile="your.addonpackage:cache" />


Combining Upgrade Steps
-----------------------

You can create many upgrade steps under one migration.

This is useful when you want to have the ability to re-run some parts of the migration and make your code more re-useable (for example cook css resource of your theme).

Here is an example of many upgrade steps you can have to achieve on a site policy:

.. code-block:: xml

    <genericsetup:upgradeSteps
        source="3900"
        destination="4000"
        profile="your.addonpackage:default">

      <genericsetup:upgradeStep
          title="Upgrade addons"
          description="Install and upgrades add-ons"
          handler=".v4.upgrade_addons"
          />

      <genericsetup:upgradeStep
          title="Remove LDAP PAS Plugin"
          description="Execute this upgrade after the plonesite upgrade"
          handler=".v4.upgrade_pas"
          />

      <genericsetup:upgradeDepends
          title="Apply skins.xml from our plone4 profile"
          import_profile="your.addonpackage:plone4"
          import_steps="skins"
          />

      <genericsetup:upgradeDepends
          title="Install our complete cache profile"
          import_profile="your.addonpackage:cache"
          />

      <genericsetup:upgradeDepends
          title="Apply rolemap.xml.
                 This is implicitly taken from the profile the upgradeSteps are defined for: the default"
          import_steps="rolemap"
          />

    </genericsetup:upgradeSteps>


Add-on Package Appears Twice In The Installer List
==================================================

This happens if you are developing your own add-on and keep changing things.

You have an error in your add-on package ZCML code which causes portal_quickinstaller to have two entries.

More information

* http://plone.293351.n2.nabble.com/Product-twice-in-quickinstaller-td5345492.html#a5345492


Preventing Uninstall
====================

You might want to prevent your add-on package uninstall for some reason.

Example:

.. code-block:: python

        from zExceptions import BadRequest


        def uninstall(self, reinstall):
            if reinstall == False:
                raise BadRequest('This package cannot be uninstalled!')

.. deprecated:: 5.1

    This example is for Extensions/install.py, an old Plone 2 way of writing installers and uninstallers.
    It is still working in Plone 5.0, but will likely go away in Plone 5.1.
    In Plone 5.1 you can decide not to create an uninstall profile.


Best Practices
==============

The ``purge`` attribute
-----------------------

When importing items such as property sheets, make sure not to override other profile settings: set the ``purge`` attribute to False.

This will *add* the listed items to the property instead of resetting the property.

Example:

.. code-block:: xml

    <property name="metaTypesNotToList" type="lines" purge="False">
      <element value="File"/>
      <element value="Image"/>
    </property>


The ``remove`` Attribute
------------------------

The ``remove`` attribute can be used to remove an item.

.. code-block:: xml

    <property name="allowAnonymousViewAbout" type="boolean" remove="true" />

There are dangers:

- Some importers do not support the ``remove`` keyword.
  They ignore it and add the item blindly.
  This should be regarded as a bug in the importer.
  Please report it.

- Some importers check the truth value of the attribute, some just check the presence.
  ``remove="false"`` may mean the item stays and may mean it gets removed.
  Best is to either use ``remove="true"`` or leave the entire keyword away.


Only Use The Configuration That You Need
----------------------------------------

When you export your site's configuration, it will include things that you don't need.

For example, if you only need to change the 'Allow anonymous to view about' property, this is what your ``propertiestool.xml`` should look like:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_properties" meta_type="Plone Properties Tool">
      <object name="site_properties" meta_type="Plone Property Sheet">
        <property name="allowAnonymousViewAbout" type="boolean">True</property>
      </object>
    </object

.. original content from http://www.sixfeetup.com/company/technologies/plone-content-management-new/quick-reference-cards/swag/swag-images-files/generic_setup.pdf


i18n domains in GenericSetup xml files
--------------------------------------

In your GenericSetup profile you can have several xml files.
In some of these it makes sense to do translations.

In most of those cases you must use the ``plone`` domain, but in some you can use your own domain.

.. note::

   You are always allowed to use the ``plone`` domain, but if the xml file supports a separate domain it is best to use that.

- ``actions.xml``: use **your own** domain.

Example::

    <object name="ducktest" meta_type="CMF Action" i18n:domain="your.addonpackage">
      <property name="title" i18n:translate="">Duck Test</property>
      <property name="description" i18n:translate="">Action: test a duck</property>
      ...
    </object>

.. note::

   In the portal_actions tool, in the Management Interface, you will see an i18n domain specified for each action.

- ``catalog.xml``: no i18n needed

- ``componentregistry.xml``: no i18n needed

- ``contenttyperegistry.xml``: no i18n needed

- ``controlpanel.xml``: use **your own** domain.

Example::

    <?xml version="1.0"?>
    <object name="portal_controlpanel" meta_type="Plone Control Panel Tool"
            i18n:domain="your.addonpackage" xmlns:i18n="http://xml.zope.org/namespaces/i18n">
      <configlet title="Your Add-on Package Configuration Panel" action_id="your.addonpackage" appId="your.addonpackage"
                 category="Products" condition_expr=""
                 icon_expr="string:$portal_url/your_addonpackage_icon.png"
                 url_expr="string:${portal_url}/prefs_install_products_form"
                 visible="True" i18n:attributes="title">
        <permission>Manage portal</permission>
      </configlet>
    </object>

- ``cssregistry.xml``: no i18n needed

- ``diff_tool.xml``: no i18n needed

- ``factorytool.xml``: no i18n needed

- ``jsregistry.xml``: no i18n needed

- ``kssregistry.xml``: no i18n needed

- ``mailhost.xml``: no i18n needed

- ``memberdata_properties.xml``: no i18n needed

- ``metadata.xml``: no i18n needed

- ``portal_atct.xml``: use the **plone** domain.

.. note::

   This has no influence on the Collections panel in Site Setup.

   It is only used on the edit and criteria pages of an old-style Collection.

- ``portlets.xml``: use the **plone** domain.

- ``properties.xml``: no i18n needed

- ``propertiestool.xml``: no i18n needed

- ``rolemap.xml``: no i18n needed

- ``skins.xml``: no i18n needed

- ``toolset.xml``: no i18n needed

- ``types``: use **your own** domain

- ``viewlets.xml``: no i18n needed

- ``workflows``: use the **plone** domain

.. original content from http://maurits.vanrees.org/weblog/archive/2010/10/i18n-plone-4


Generic Setup Files
===================

.. note:

    When you are developing, changes you make to an xml file are immediately available when you apply the profile.
    You don't need to restart your Plone instance.
    Exception: for changes to ``metadata.xml`` you *do* need to restart Plone.


actionicons.xml
---------------

.. deprecated:: 4.0.

    Plone 5 no longer reads this file, because ``Products.CMFActionIcons`` is not included.
    The icons should go in ``actions.xml`` directly.


actions.xml
-----------

Install actions in the ``portal_actions`` tool.

Example:

.. code-block:: xml

  <?xml version="1.0"?>
  <object name="portal_actions" meta_type="Plone Actions Tool"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n">
    <object name="object_buttons" meta_type="CMF Action Category">
      <object name="iterate_checkin" meta_type="CMF Action" i18n:domain="plone">
        <property name="title" i18n:translate="">Check in</property>
        <property name="description" i18n:translate=""></property>
        <property name="url_expr">string:${object_url}/@@content-checkin</property>
        <property name="icon_expr">string:${portal_url}/++resource++checkout.png</property>
        <property name="available_expr">python:path('object/@@iterate_control').checkin_allowed()</property>
        <property name="permissions">
          <element value="View"/>
        </property>
        <property name="visible">True</property>
      </object>
    </object>
  </object>

These actions are used in various parts of Plone.

These are the object categories in standard Plone:

``document_actions``
    Document actions, like rss and print.

``site_actions``
    Site actions, like sitemap, accessibility, contact.

``object``
    Object tabs, like contents, sharing tab.

``object_buttons``
    Object buttons, like delete, rename.

``portal_tabs``
    Portal tabs, like Home.

``user``
    User actions, like preferences, login, join.

For adding controlpanel actions, see controlpanel.xml_ instead.

The objects support ``insert-before`` and ``insert-after`` for inserting the action object before or after another action object.

For removing, use ``remove="true"`` (or ``True``).

Uninstall example:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_actions" meta_type="Plone Actions Tool"
            xmlns:i18n="http://xml.zope.org/namespaces/i18n">
      <object name="object_buttons" meta_type="CMF Action Category">
        <object name="iterate_checkin" remove="true" />
      </object>
    </object>

.. note::

    You can use your own i18n domain.


browserlayer.xml
----------------

This registers a specific browser layer, which allows components to be available only when your add-on package is installed.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <layers>
      <layer name="your.addonpackage"
          interface="your.addonpackage.interfaces.IYourAddonPackageLayer" />
    </layers>

For removing, use ``remove="true"`` (or ``True``).

Uninstall example:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <layers>
      <layer name="your.addonpackage" remove="true" />
    </layers>


componentregistry.xml
---------------------

Setup items in the local component registry of the Plone Site.
The items can be adapters, subscribers or utilities.

This can also be done in zcml, which puts it in the global registry that is defined at startup.

The difference is, when you put it in xml, the item is only added to a specific Plone Site when you install the package in the add-ons control panel.

Both have their uses.

Example:

.. code-block:: xml

    <?xml version="1.0"?>
    <componentregistry>
      <adapters>
         <adapter
           for="archetypes.multilingual.interfaces.IArchetypesTranslatable"
           provides="plone.app.multilingual.interfaces.ITranslationCloner"
           factory="archetypes.multilingual.cloner.Cloner"
         />
      </adapters>
      <subscribers>
        <subscriber
          for="archetypes.multilingual.interfaces.IArchetypesTranslatable
               zope.lifecycleevent.interfaces.IObjectModifiedEvent"
          handler="archetypes.multilingual.subscriber.handler"
          />
      </subscribers>
      <utilities>
        <utility
          interface="Products.ATContentTypes.interface.IATCTTool"
          object="portal_atct"/>
      </utilities>
    </componentregistry>

.. note::
   A subscriber can either have a handler or a factory, not both.
   A factory must have a provides and may have a name.
   A subscriber will fail with a provides.

.. note::
    If something does not get added, its provider is probably blacklisted.
    This list is defined by ``Products.GenericSetup.interfaces.IComponentsHandlerBlacklist`` utilities.
    In standard Plone 5, these interfaces are blacklisted as providers:

    - ``Products.GenericSetup.interfaces.IComponentsHandlerBlacklist``

    - ``plone.portlets.interfaces.IPortletManager``

    - ``plone.portlets.interfaces.IPortletManagerRenderer``

    - ``plone.portlets.interfaces.IPortletType``

Uninstall example:

.. code-block:: xml

    <?xml version="1.0"?>
    <componentregistry>
      <adapters>
        <adapter
          remove="true"
          for="archetypes.multilingual.interfaces.IArchetypesTranslatable"
          provides="plone.app.multilingual.interfaces.ITranslationCloner"
          factory="archetypes.multilingual.cloner.Cloner"
        />
      </adapters>
      <subscribers>
        <subscriber
          remove="true"
          for="archetypes.multilingual.interfaces.IArchetypesTranslatable
               zope.lifecycleevent.interfaces.IObjectModifiedEvent"
          handler="archetypes.multilingual.subscriber.handler"
          />
      </subscribers>
      <utilities>
        <utility
          remove="true"
          interface="Products.ATContentTypes.interface.IATCTTool"
          object="portal_atct"/>
      </utilities>
    </componentregistry>

.. note::

   The presence of the ``remove`` keyword is enough.
   Even if it is empty or contains ``false`` as value, the item is removed.

Code is in ``Products.GenericSetup.components``.


contentrules.xml
----------------

Code is in ``plone.app.contentrules.exportimport.rules``.


Content Generation
------------------

Code is in ``Products.GenericSetup.content``:

.. automodule:: Products.GenericSetup.content
  :members: FolderishExporterImporter


controlpanel.xml
----------------

.. code-block:: xml

    <?xml version="1.0"?>
    <object
        name="portal_controlpanel"
        xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        i18n:domain="plone.app.caching">

      <configlet
          title="Caching"
          action_id="plone.app.caching"
          appId="plone.app.caching"
          category="plone-advanced"
          condition_expr=""
          icon_expr="string:$portal_url/++resource++plone.app.caching.gif"
          url_expr="string:${portal_url}/@@caching-controlpanel"
          visible="True"
          i18n:attributes="title">
        <permission>Manage portal</permission>
      </configlet>

    </object>

This creates an action in the Site Setup control panel in Plone.
Actions are bundled in categories.

The only categories supported in standard Plone 5 are:

- ``Member`` (My Preferences)
- ``Plone`` (Plone Configuration)
- ``plone-advanced`` (Advanced)
- ``plone-content`` (Content)
- ``plone-general`` (General)
- ``plone-security`` (Security)
- ``plone-users`` (Users)
- ``Products`` (Add-on Configuration)

Any other categories are not displayed in the overview control panel.
Note that in Plone 4, only ``Member``, ``Plone`` and ``Products`` were supported.
For add-ons, the category ``Products`` is recommended.

The ``action_id`` must be unique over all categories.

Only one permission is allowed.

Uninstall example:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_controlpanel">
      <configlet action_id="plone.app.caching" remove="true" />
    </object>

.. note::

    The action is removed if the ``remove`` keyword is ``true``.
    Upper or lower case does not matter.

    The action is visible if the ``visible`` keyword is ``true``.
    Upper or lower case does not matter.

.. note::

    You can use your own i18n domain.

Code is in ``Products.CMFPlone.exportimport.controlpanel`` and ``Products.CMFPlone.PloneControlPanel``.


cssregistry.xml
---------------

.. deprecated:: 5.0.

    This still works in Plone 5, but it is deprecated.

For the old way, see: :doc:`Front-end: templates, CSS and JavaScript </adapt-and-extend/theming/templates_css/index>`.

For the new way, see: doc:`Plone 5 Resource Registry </adapt-and-extend/theming/resourceregistry>`.


diff_tool.xml
-------------

This is the configuration from ``plone.app.contenttypes``:

.. code-block:: xml

    <?xml version="1.0"?>
    <object>
      <difftypes>
        <type portal_type="Document">
          <field name="any" difftype="Compound Diff for Dexterity types"/>
        </type>
        <type portal_type="Event">
          <field name="any" difftype="Compound Diff for Dexterity types"/>
        </type>
        <type portal_type="File">
          <field name="any" difftype="Compound Diff for Dexterity types"/>
        </type>
        <type portal_type="Folder">
          <field name="any" difftype="Compound Diff for Dexterity types"/>
        </type>
        <type portal_type="Image">
          <field name="any" difftype="Compound Diff for Dexterity types"/>
        </type>
        <type portal_type="Link">
          <field name="any" difftype="Compound Diff for Dexterity types"/>
        </type>
        <type portal_type="News Item">
          <field name="any" difftype="Compound Diff for Dexterity types"/>
        </type>
      </difftypes>
    </object>

This configures how the difference between two versions of a field are shown on the history tab.

The configuration is stored in the ``portal_diff`` tool.

For Archetypes content, you need a different ``difftype``:

.. code-block:: xml

    <type portal_type="Document">
      <field name="any" difftype="Compound Diff for AT types"/>
    </type>

A new ``difftype`` can be registered by calling ``Products.CMFDiffTool.CMFDiffTool.registerDiffType``.
The ``difftypes`` in standard Plone 5 are:

- ``Lines Diff``
- ``Compound Diff for AT types``
- ``Binary Diff``
- ``Field Diff``
- ``List Diff``
- ``HTML Diff``
- ``Compound Diff for Dexterity types``

.. note::

    There is no uninstall version.
    The ``remove`` keyword is not supported.
    The ``portal_diff`` tool does not show configuration for portal_types that no longer exist.

Code is in ``Products.CMFDiffTool.exportimport.difftool``.


factorytool.xml
---------------

This is only needed for Archetypes content types.
It makes sure when you start adding a content item but don't finish it, that no half created item lingers.

This is not needed for Dexterity items.

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_factory" meta_type="Plone Factory Tool">
      <factorytypes>
        <type portal_type="Document"/>
        <type portal_type="Event"/>
        <type portal_type="File"/>
        <type portal_type="Folder"/>
        <type portal_type="Image"/>
        <type portal_type="Link"/>
        <type portal_type="News Item"/>
        <type portal_type="Topic"/>
      </factorytypes>
    </object>

.. note::

    The ``remove`` keyword is not supported.

Code is in ``Products.ATContentTypes.exportimport.factorytool``.


jsregistry.xml
--------------

.. deprecated:: 5.0.

    This still works in Plone 5, but it is deprecated.

For the old way, see: :doc:`Front-end: templates, CSS and JavaScript </adapt-and-extend/theming/templates_css/index>`.

For the new way, see: doc:`Plone 5 Resource Registry </adapt-and-extend/theming/resourceregistry>`.


kssregistry.xml
---------------

.. deprecated:: 4.3

    Instead of these Kinetic Style Sheets you should use javascript.


metadata.xml
------------

The ``metadata.xml`` file is read during Plone start-up.

If this file has problems your add-on package might not appear in the installer control panel.

The ``metadata.xml`` file contains add-on dependency and version information.

.. code-block:: xml

    <?xml version="1.0"?>
    <metadata>
      <version>1000</version>
      <dependencies>
        <dependency>profile-your.addonpackage:default</dependency>
      </dependencies>
    </metadata>

The dependencies are optional.

There is no import step that reads this file.
The ``portal_setup`` tool uses this information when installing a profile.

It installs the profiles that are listed as dependencies, before installing your own profile.

Since ``Products.GenericSetup`` 1.8.0, dependency profiles that are already installed, are not installed again.

Instead, their upgrade steps, are applied, if they have them.

After your profile is installed, ``portal_setup`` stores the version number.
This is used when determining if any upgrade steps are available for your profile.

When you search for ``metadata.xml`` in the documentation, you will find more information in context.

.. note::

    There is no uninstall version of ``metadata.xml``.
    An ``uninstall`` profile can have its own ``metadata.xml`` with a version and even profiles.
    But for dependencies no ``purge`` or ``remove`` keyword is supported.


portal_atct.xml
---------------

.. deprecated:: 4.2

    This was used for Archetypes Topics, the old-style Collections.
    Since Plone 4.2 you can use new-style Collections.
    Please use those.

.. code-block:: xml

    <?xml version="1.0"?>
    <atcttool
        xmlns:i18n="http://xml.zope.org/namespaces/i18n">
      <topic_indexes i18n:domain="plone">
        <index name="allowedRolesAndUsers"
               description="The roles and users with View permission on an item"
               enabled="False" friendlyName="Internal Security"
               i18n:attributes="description; friendlyName" />
        <index name="created" description="The time and date an item was created"
               enabled="True" friendlyName="Creation Date"
               i18n:attributes="description; friendlyName">
          <criteria>ATFriendlyDateCriteria</criteria>
          <criteria>ATDateRangeCriterion</criteria>
        </index>
      </topic_indexes>
      <topic_metadata i18n:domain="plone">
        <metadata name="created"
                  description="The time and date an item was created"
                  enabled="False" friendlyName="Creation Date"
                  i18n:attributes="description; friendlyName" />
      </topic_metadata>
      <property name="title">ATContentTypes Tool</property>
      <property name="image_types">
        <element value="Image"/>
        <element value="News Item"/>
      </property>
      <property name="folder_types">
        <element value="Image"/>
      </property>
      <property name="album_batch_size">30</property>
      <property name="album_image_scale">thumb</property>
      <property name="single_image_scale">preview</property>
    </atcttool>


portal_placeful_workflow
------------------------

This handles the ``portal_placeful_workflow.xml`` file and the ``portal_placeful_workflow`` directory.

This install or configures a placeful workflow.

For this to work, you must install Workflow Policy Support (CMFPlacefulWorkflow) in the Add-ons control panel. This package is included in standard Plone, but does not come installed by default.

Standard ``portal_placeful_workflow.xml`` from ``Products.CMFPlacefulWorkflow``:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_placeful_workflow" meta_type="Placeful Workflow Tool">
      <property name="title"></property>
      <property name="max_chain_length" type="int">1</property>
      <object name="intranet" meta_type="WorkflowPolicy"/>
      <object name="old-plone" meta_type="WorkflowPolicy"/>
      <object name="one-state" meta_type="WorkflowPolicy"/>
      <object name="simple-publication" meta_type="WorkflowPolicy"/>
    </object>

Standard ``portal_placeful_workflow/simple-publication.xml`` from ``Products.CMFPlacefulWorkflow``:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="simple-publication" meta_type="WorkflowPolicy">
      <property name="title">Simple publication</property>
      <bindings>
        <default>
          <bound-workflow workflow_id="simple_publication_workflow"/>
        </default>
        <type default_chain="true" type_id="Document"/>
        <type default_chain="true" type_id="Event"/>
        <type type_id="File">
        </type>
        <type default_chain="true" type_id="Folder"/>
        <type type_id="Image">
        </type>
        <type default_chain="true" type_id="Link"/>
        <type default_chain="true" type_id="News Item"/>
        <type default_chain="true" type_id="Collection"/>
      </bindings>
    </object>

Uninstall example:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_placeful_workflow" meta_type="Placeful Workflow Tool">
      <object name="old-plone" meta_type="WorkflowPolicy" remove="true" />
    </object>

The import handler is in ``Products.CMFPlacefulWorkflow.exportimport.importWorkflowPolicies``.


portlets.xml
------------

Code is in ``plone.app.portlets.exportimport.portlets``.

.. automodule:: plone.app.portlets.exportimport.portlets


propertiestool.xml
------------------

.. deprecated:: 5.0

    Most properties are now handled in the configuration registry and can be configured in ``registry.xml``.

In ``propertiestool.xml`` you can change all values of the ``portal_properties`` tool.
Example:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_properties" meta_type="Plone Properties Tool">
      <object name="site_properties" meta_type="Plone Property Sheet">
        <property name="use_email_as_login" type="boolean">False</property>
        <property name="default_editor" type="string">TinyMCE</property>
      </object>
    </object>

Uninstall example:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <object name="portal_properties" meta_type="Plone Properties Tool">
      <object name="site_properties" meta_type="Plone Property Sheet">
        <property name="default_page_types" type="lines" purge="False">
          <element value="UninstallTest" remove="True" />
        </property>
      </object>
    </object>


pluginregistry.xml
------------------

This configures PAS plugin orderings and active plugins.
It isn't part of Plone itself, it is used by other frameworks and can be used in Plone with a little extra configuration.

First, you need a monkey patch in your ``__init__.py``` to point the importer at where Plone keeps its PAS plugins.

.. code-block:: python

    from Products.PluginRegistry import exportimport
    from Products.PluginRegistry.interfaces import IPluginRegistry


    def getRegistry(site):
        return IPluginRegistry(site.acl_users.plugins)

    exportimport._getRegistry = getRegistry

Secondly, code to handle the import step needs to be activated in Plone:

.. code-block:: xml

    <genericsetup:importStep
        name="PAS Plugin Registry"
        title="PAS Plugin Registry"
        description=""
        handler="Products.PluginRegistry.exportimport.importPluginRegistry"
        />

Now you can use ``pluginregistry.xml`` in your generic setup profiles:

.. code-block:: xml

    <?xml version="1.0"?>
    <plugin-registry>
        <plugin-type id="IAuthenticationPlugin"
                title="authentication"
                description="Authentication plugins are responsible for validating credentials generated by the Extraction Plugin."
                interface="Products.PluggableAuthService.interfaces.plugins.IAuthenticationPlugin">
            <plugin id="source_users"/>
            <plugin id="session"/>
            <plugin id="sql"/>
        </plugin-type>

        <plugin-type id="IPropertiesPlugin" title="properties"
                description="Properties plugins generate property sheets for users."
                interface="Products.PluggableAuthService.interfaces.plugins.IPropertiesPlugin">
            <plugin id="sql" />
            <plugin id="mutable_properties"/>
        </plugin-type>

        <plugin-type id="IRolesPlugin" title="roles"
                description="Roles plugins determine the global roles which a user has."
                interface="Products.PluggableAuthService.interfaces.plugins.IRolesPlugin">
            <plugin id="portal_role_manager"/>
            <plugin id="sql"/>
        </plugin-type>


        <plugin-type id="IUserEnumerationPlugin"
                title="user_enumeration"
                description="Enumeration plugins allow querying users by ID, and searching for users who match particular criteria."
                interface="Products.PluggableAuthService.interfaces.plugins.IUserEnumerationPlugin">
            <plugin id="source_users"/>
            <plugin id="mutable_properties"/>
            <plugin id="sql"/>
        </plugin-type>

        <plugin-type id="IUserAdderPlugin" title="user_adder"
                description="User Adder plugins allow the Pluggable Auth Service to create users."
                interface="Products.PluggableAuthService.interfaces.plugins.IUserAdderPlugin">
        </plugin-type>
    </plugin-registry>


registry.xml
------------

This edits the configuration registry.

.. note::

    The name of this import step is ``plone.app.registry``, **not** ``registry``.

Example for adding all records of an interface:

.. code-block:: xml

    <?xml version="1.0"?>
    <registry>
      <records interface="plone.app.iterate.interfaces.IIterateSettings" />
    </registry>

Example for adding an individual record:

.. code-block:: xml

    <?xml version="1.0"?>
    <registry>
      <record name="your.addonpackage.timeout">
        <field type="plone.registry.field.Int">
          <title>Timeout</title>
          <min>0</min>
        </field>
        <value>100</value>
      </record>
    </registry>

Uninstall example:

.. code-block:: xml

    <?xml version="1.0"?>
    <registry>
      <records interface="plone.app.iterate.interfaces.IIterateSettings" remove="true" />
      <record name="your.addonpackage.timeout" remove="true" />
    </registry>

The item is removed if the ``remove`` keyword is ``true``.
Upper or lower case does not matter.

Existing values of lists are purged by default.
The values are not purged if the ``purge`` keyword is ``false``.

Upper or lower case does not matter.

For more examples, see the `plone.app.registry documentation <https://pypi.python.org/pypi/plone.app.registry#using-genericsetup-to-manipulate-the-registry>`_.

Code is in ``plone.app.registry.exportimport.handler``.


repositorytool.xml
------------------

This handles the versioning policy of content.

The default configuration in Plone is:

.. code-block:: xml

    <?xml version="1.0"?>
    <repositorytool>
      <policies purge="true">
        <policy name="at_edit_autoversion"
                title="Create version on edit (AT objects only)"
                class="Products.CMFEditions.VersionPolicies.ATVersionOnEditPolicy"/>
        <policy name="version_on_revert" title="Create version on version revert"/>
      </policies>
      <policymap purge="true">
        <type name="ATDocument">
          <policy name="at_edit_autoversion"/>
          <policy name="version_on_revert"/>
        </type>
        <type name="ATNewsItem">
          <policy name="at_edit_autoversion"/>
          <policy name="version_on_revert"/>
        </type>
        <type name="Document">
          <policy name="at_edit_autoversion"/>
          <policy name="version_on_revert"/>
        </type>
        <type name="Event">
          <policy name="at_edit_autoversion"/>
          <policy name="version_on_revert"/>
        </type>
        <type name="Link">
          <policy name="at_edit_autoversion"/>
          <policy name="version_on_revert"/>
        </type>
        <type name="News Item">
          <policy name="at_edit_autoversion"/>
          <policy name="version_on_revert"/>
        </type>
      </policymap>
    </repositorytool>

Code is in ``Products.CMFEditions.exportimport.repository``.


rolemap.xml
-----------

In ``rolemap.xml`` you define new roles and grant permissions.
Both are optional.

.. code-block:: xml

    <?xml version="1.0"?>
    <rolemap>
      <roles>
        <role name="Anonymous"/>
        <role name="Authenticated"/>
        <role name="Manager"/>
        <role name="Site Administrator"/>
        <role name="Member"/>
        <role name="Owner"/>
        <role name="Reviewer"/>
        <role name="Reader" />
        <role name="Editor" />
        <role name="Contributor" />
      </roles>
      <permissions>
        <permission name="Pass the bridge"
                    acquire="True">
          <role name="Manager"/>
          <role name="Site Administrator"/>
        </permission>
      </permissions>
    </rolemap>

The roles above are the standard roles in Plone 5.
In your profile you only need to list other roles.

The permission must already exist on the Zope level, otherwise you get an error when installing your profile::

  ValueError: The permission <em>Pass the bridge</em> is invalid.

A permission is created on the Zope level when it is used in code.
See :doc:`Creating permissions </develop/plone/security/permissions>`.

When a role in a permission does not exist, it is silently ignored.
The roles listed in a permission are not added.

They replace all existing roles.

With ``acquire="true"`` (or ``True``, ``yes``, ``1``) roles are also acquired from the Zope root.

.. note::

    There is no uninstall version for ``rolemap.xml``.
    ``purge`` and ``remove`` are not supported.
    You can set different values for a permission if this makes sense in your case.
    This will reset the permission to the same settings as on the Zope level:

    .. code-block:: xml

        <permission name="Pass the bridge" acquire="True" />

.. automodule:: Products.GenericSetup.rolemap
  :members: importRolemap RolemapImportConfigurator


sharing.xml
-----------

The sharing.xml file let you add custom roles to the sharing tab.
For reference, visit: :doc:`Local Roles </develop/plone/security/local_roles>`.


skins.xml
---------

Skins are old fashioned, you may not need this.
The more modern way is: use browser views and static directories.
But skins are still installed by several add-on packages.

Example:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_skins" meta_type="Plone Skins Tool">
      <object name="ATContentTypes" meta_type="Filesystem Directory View"
          directory="Products.ATContentTypes:skins/ATContentTypes"/>
      <skin-path name="*">
        <layer name="ATContentTypes" insert-after="custom"/>
      </skin-path>
    </object>

- The ``object`` is added to the Contents tab of ``portal_skins``.

- The ``layer`` is added to one or more skin selections on the Properties tab of ``portal_skins``.

- The ``skin-path`` name is usually ``*`` to add the skin layer to all skin selections (old style themes in ``portal_skins``).
  It can also contain a specific skin, for example ``Plone Default``, ``Sunburst Theme``, ``Plone Classic Theme``.

You can set a few properties on the ``portal_skins`` object.
``Products.CMFPlone`` sets good defaults which you should keep:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_skins"
       meta_type="Plone Skins Tool"
       default_skin="Plone Default"
       allow_any="False"
       cookie_persistence="False"
       request_varname="plone_skin">
    </object>

- The ``meta_type`` should always be ``Plone Skins Tool`` or be removed.
  It is ignored.

- ``default_skin`` is the name of the default skin selection.

- ``allow_any`` indicates whether users are allowed to use arbitrary skin paths.

- ``cookie_persistence`` indicates whether the skins cookie is persistent or not.

- ``request_varname`` gets the variable name to look for in the request.

The ``allow_any``, ``cookie_persistence`` and ``request_varname`` options are old functionality and seem not well supported anymore.
No cookie is set.
You can choose a skin path even when ``allow_any`` is false.

The idea is:
if you have the Sunburst Theme as default,
and also have the Plone Classic Theme available,
you can view the site in the classic theme by visiting this link:
http://localhost:8080/Plone?plone_skin=Plone%20Classic%20Theme

Uninstall example:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_skins" meta_type="Plone Skins Tool">
     <object name="ATContentTypes" remove="true" />
     <skin-path name="*">
      <layer name="ATContentTypes" remove="true" />
     </skin-path>
    </object>

.. note::

    For removing the layer ``remove=""`` is sufficient.
    For removing the object ``remove="true"`` is required.
    Recommended is to use the full ``remove="true"`` in both cases.


tinymce.xml
-----------

.. deprecated:: 5.0

    Since Plone 5.0 this is done in ``registry.xml`` instead.
    The fields are defined in ``Products.CMFPlone.interfaces.controlpanel``.

Import TinyMCE settings.

Code is in ``Products.TinyMCE.exportimport``.


toolset.xml
-----------

This is used to add a tool to the site.

.. warning::

    This is an old way and should not be used in new code.
    You should probably register a utility instead of a tool.
    ``componentregistry.xml`` might be an alternative, but registering a utility in zcml would be better.
    If the utility needs configuration, you can use ``registry.xml``.

Example:

.. code-block:: xml

    <?xml version="1.0"?>
    <tool-setup>
     <required tool_id="portal_atct"
               class="Products.ATContentTypes.tool.atct.ATCTTool"/>
     <required tool_id="portal_factory"
               class="Products.ATContentTypes.tool.factory.FactoryTool"/>
     <required tool_id="portal_metadata"
               class="Products.ATContentTypes.tool.metadata.MetadataTool"/>
    </tool-setup>

Uninstall example:

.. code-block:: xml

    <?xml version="1.0"?>
    <tool-setup>
     <forbidden tool_id="portal_atct" />
     <forbidden tool_id="portal_factory" />
     <forbidden tool_id="portal_metadata" />
    </tool-setup>

.. note::

  Adding a forbidden tool that was first required, like in the example above, is only supported since Products.GenericSetup 1.8.3.

Code is in:

- ``Products.GenericSetup.registry._ToolsetParser``
- ``Products.GenericSetup.registry.ToolsetRegistry``
- ``Products.GenericSetup.tool.importToolset``


typeinfo
--------

This handles the ``types.xml`` file and the ``types`` directory.

.. note::

    The name of this import step is ``typeinfo``, **not** ``types``.

Partial example from ``plone.app.contenttypes``:

.. code-block:: xml

    <?xml version="1.0"?>
    <object meta_type="Plone Types Tool" name="portal_types">
      <object meta_type="Dexterity FTI" name="Collection" />
      <object meta_type="Dexterity FTI" name="Document" />
      <object meta_type="Dexterity FTI" name="Folder" />
      <object meta_type="Dexterity FTI" name="Link" />
      <object meta_type="Dexterity FTI" name="File" />
      <object meta_type="Dexterity FTI" name="Image" />
      <object meta_type="Dexterity FTI" name="News Item" />
      <object meta_type="Dexterity FTI" name="Event" />
      <object name="Plone Site"
          meta_type="Factory-based Type Information with dynamic views"/>
    </object>

This adds content types in the ``portal_types`` tool.
The ``meta_type`` can be:

- ``Dexterity FTI`` for Dexterity content.
  This is probably what you want.
- ``Factory-based Type Information with dynamic views`` for Archetypes content and for the Plone Site itself
- ``Factory-based Type Information`` for Archetypes content that does not need dynamic views,
  the ability to choose a view in the ``display`` menu.

The ``types.xml`` should be accompanied by a ``types`` folder with details information on the new types.
If you are editing an already existing type, then ``types.xml`` is not needed:
a file in the ``types`` folder is enough.

If the object name in ``types.xml`` is ``Collection`` then you must add a file ``types/Collection.xml``.
This file is in ``plone.app.contenttypes``:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="Collection"
            meta_type="Dexterity FTI"
            i18n:domain="plone" xmlns:i18n="http://xml.zope.org/namespaces/i18n">

      <!-- Basic metadata -->
      <property name="title" i18n:translate="">Collection</property>
      <property name="description"
                i18n:translate="">Collection</property>
      <property name="global_allow">True</property>
      <property name="filter_content_types">False</property>
      <property name="allowed_content_types" />
      <property name="allow_discussion">False</property>
      <property name="add_permission">plone.app.contenttypes.addCollection</property>
      <property name="klass">plone.app.contenttypes.content.Collection</property>
      <property name="schema"></property>
      <property name="model_source"></property>
      <property name="model_file">plone.app.contenttypes.schema:collection.xml</property>
      <property name="behaviors" purge="false">
        <element value="plone.app.content.interfaces.INameFromTitle"/>
        <element value="plone.app.contenttypes.behaviors.collection.ICollection"/>
        <element value="plone.app.dexterity.behaviors.discussion.IAllowDiscussion"/>
        <element value="plone.app.dexterity.behaviors.id.IShortName"/>
        <element value="plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation"/>
        <element value="plone.app.dexterity.behaviors.metadata.IDublinCore"/>
        <element value="plone.app.contenttypes.behaviors.richtext.IRichText"/>
        <element value="plone.app.relationfield.behavior.IRelatedItems"/>
        <element value="plone.app.lockingbehavior.behaviors.ILocking" />
      </property>

      <!-- View information -->
      <property name="default_view">listing_view</property>
      <property name="default_view_fallback">False</property>
      <property name="view_methods">
        <element value="listing_view"/>
        <element value="summary_view"/>
        <element value="tabular_view"/>
        <element value="full_view"/>
        <element value="album_view"/>
        <element value="event_listing"/>
      </property>

      <!-- Method aliases -->
      <alias from="(Default)" to="(dynamic view)"/>
      <alias from="edit" to="@@edit"/>
      <alias from="sharing" to="@@sharing"/>
      <alias from="view" to="(selected layout)" />

      <!-- Actions -->
      <action title="View" action_id="view" category="object" condition_expr=""
              url_expr="string:${object_url}" visible="True">
        <permission value="View"/>
      </action>

      <action title="Edit" action_id="edit" category="object" condition_expr=""
              url_expr="string:${object_url}/edit" visible="True">
        <permission value="Modify portal content"/>
      </action>

    </object>

For comparison, here is the ``types.xml`` from ``plone.app.collection`` which has an old style Archetypes Collection:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_types">
      <!-- We remove the existing FTI since it could be Dexterity-based and would
           not be compatible in that case.  You get this error when installing:
           ValueError: undefined property 'content_meta_type' -->
      <object name="Collection" remove="True"/>
      <object name="Collection"
              meta_type="Factory-based Type Information with dynamic views" />
    </object>

And here is the ``types/Collection.xml`` from ``plone.app.collection``:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="Collection"
            meta_type="Factory-based Type Information with dynamic views"
            i18n:domain="plone" xmlns:i18n="http://xml.zope.org/namespaces/i18n">
      <property name="title" i18n:translate="">Collection</property>
      <property name="description"
                i18n:translate="">Collection of searchable information</property>
      <property name="icon_expr"></property>
      <property name="content_meta_type">Collection</property>
      <property name="product">plone.app.collection</property>
      <property name="factory">addCollection</property>
      <property name="immediate_view">standard_view</property>
      <property name="global_allow">True</property>
      <property name="filter_content_types">True</property>
      <property name="allowed_content_types"/>
      <property name="allow_discussion">False</property>
      <property name="default_view">standard_view</property>
      <property name="view_methods">
        <element value="standard_view" />
        <element value="summary_view" />
        <element value="all_content" />
        <element value="tabular_view" />
        <element value="thumbnail_view" />
      </property>
      <alias from="(Default)" to="(dynamic view)" />
      <alias from="edit" to="atct_edit" />
      <alias from="sharing" to="@@sharing" />
      <alias from="view" to="(selected layout)" />
      <action title="View" action_id="view" category="object" condition_expr=""
              url_expr="string:${object_url}/" visible="True">
        <permission value="View" />
      </action>
      <action title="Edit" action_id="edit" category="object" condition_expr=""
              url_expr="string:${object_url}/edit" visible="True">
        <permission value="Modify portal content" />
      </action>
    </object>

Uninstall example:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_types">
      <object name="Collection" remove="true"/>
    </object>

.. note::

    The ``remove`` keyword is supported for actions.
    ``remove=""`` is enough, but recommended is to use ``remove="true"``.

    The ``view_methods`` property is a list that is always imported fresh.
    Elements that are not in the list, are removed.
    If you only want to add an element and want to keep any existing elements,
    you can tell it not to purge:

    .. code-block:: xml

       <property name="view_methods" purge="False">
         <element value="new_view" />
       </property>

    This does not work for the ``allowed_content_types``: they are always purged.

.. note::

    You can use your own i18n domain.


viewlets.xml
------------

.. automodule:: plone.app.viewletmanager.exportimport.storage


workflows.xml
-------------

This handles the ``workflows.xml`` file and the ``workflows`` directory.

Example from ``Products/CMFPlone/profiles/default/workflows.xml`` in Plone 5.0:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_workflow" meta_type="Plone Workflow Tool">
      <property
          name="title">Contains workflow definitions for your portal</property>
      <object name="folder_workflow" meta_type="Workflow"/>
      <object name="intranet_folder_workflow" meta_type="Workflow"/>
      <object name="intranet_workflow" meta_type="Workflow"/>
      <object name="one_state_workflow" meta_type="Workflow"/>
      <object name="plone_workflow" meta_type="Workflow"/>
      <object name="simple_publication_workflow" meta_type="Workflow"/>
      <bindings>
        <default>
          <bound-workflow workflow_id="simple_publication_workflow"/>
        </default>
        <type type_id="ATBooleanCriterion"/>
        <type type_id="ATCurrentAuthorCriterion"/>
        <type type_id="ATDateCriteria"/>
        <type type_id="ATDateRangeCriterion"/>
        <type type_id="ATListCriterion"/>
        <type type_id="ATPathCriterion"/>
        <type type_id="ATPortalTypeCriterion"/>
        <type type_id="ATReferenceCriterion"/>
        <type type_id="ATRelativePathCriterion"/>
        <type type_id="ATSelectionCriterion"/>
        <type type_id="ATSimpleIntCriterion"/>
        <type type_id="ATSimpleStringCriterion"/>
        <type type_id="ATSortCriterion"/>
        <type type_id="Discussion Item"/>
        <type type_id="File"/>
        <type type_id="Image"/>
        <type type_id="Plone Site"/>
      </bindings>
    </object>

This adds six workflows in the ``portal_workflow`` tool.
It sets the default workflow to ``simple_publication_workflow``.

It sets several types to not use any workflow.

Next to this, the ``workflows`` directory is checked.
This contains sub directories with the same name as the workflows.
Each sub directory contains a file ``definition.xml`` with the definition for this workflow.

See `the Plone workflows <https://github.com/plone/Products.CMFPlone/tree/5.0.x/Products/CMFPlone/profiles/default/workflows>`_.

Code is in ``Products.DCWorkflow.exportimport``.
