============================================================
 Add-on installation and export framework: GenericSetup
============================================================

.. admonition:: Description

        GenericSetup is a framework to modify the Plone site during add-on
        product installation and uninstallation. It provides XML-based rules
        to change the site settings easily.

.. contents :: :local:

Introduction
=============

GenericSetup is an XML-based way to import and export Plone site configurations.

It is mainly used to prepare the Plone site for add-on products, by:

* registering CSS files,
* registering JavaScript files,
* setting various properties,
* registering portlets,
* registering portal_catalog search query indexes,
* ...and so on...

GenericSetup is mostly used to apply add-on-specific changes to the site
configuration, and to enable add-on-specific behavior when the add-on
installer is run.

GenericSetup XML files are usually in a ``profiles/default`` folder inside
the add-on product.

All run-time configurable items, like viewlets order through
``/@@manage-viewlets`` page, are made repeatable using GenericSetup profile
files.

You do not need to hand-edit GenericSetup profile files.
You can always change the configuration options through Plone
or using the Zope Management Interface. Then you can export the resulting
profile as an XML file, using the *Export* tab in the ``portal_setup`` ZMI
tool.

Directly
editing XML profile files does not change anything on the site, even after
Zope restart. This is because run-time configurable items are stored in the
database. If you edit profile files, you need reimport edited files using
the ``portal_setup`` tool or rerun the add-on product installer in Plone
control panel. This import will read XML files and change Plone database
accordingly.


.. note::

    Difference between ZCML and GenericSetup

    ZCML changes affect loaded Python code in
    **all** sites inside Zope whereas
    GenericSetup XML files affect only one Plone site and its database.
    GenericSetup XML files are always database changes.

    Relationship between ZCML and site-specific behavior is usually done
    using :doc:`layers </develop/plone/views/layers>`. ZCML
    directives, like viewlets and views, are registered
    to be active on a certain layer only using ``layer``
    attribute. When GenericSetup XML is imported
    through ``portal_setup``, or the product add-on installer is
    run for a Plone site, the layer is activated for the
    particular site only, enabling all views registered
    for this layer.

.. note ::

        The ``metadata.xml`` file (add-on dependency and version
        information) is read during Plone start-up.
        If this file has problems your add-on might not appear in the installer control panel.

.. * Not publicly viewable anymore: `GenericSetup tutorial <https://plone.org/documentation/tutorial/genericsetup>`_

* `GenericSetup product page <https://pypi.python.org/pypi/Products.GenericSetup>`_.

* `Source code <https://github.com/zopefoundation/Products.GenericSetup>`_.


Creating a profile
==================

You use ``<genericsetup>`` directive in your add-on product's ``configure.zcml``.
The name for the default profile executed by the Plone add-on installer
is "default". If you need different profiles for e.g. unit testing
you can declare them here.

Profile XML files go in the ``profiles/default`` folder inside your add-on
product.

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
        i18n_domain="gomobile.mobile">

      <genericsetup:registerProfile
          name="default"
          title="Plone Go Mobile"
          directory="profiles/default"
          description='Mobile CMS add-on'
          provides="Products.GenericSetup.interfaces.EXTENSION"
          />

    </configure>

.. note ::

    When you have more than one profile in your package,
    the add-ons control panel needs to decide which one to use when you install it.
    In Plone 5.0 and lower,
    the profiles are sorted alphabetically by id,
    and the first one is chosen.
    So if you have profiles ``base`` and ``default``,
    the ``base`` profile is installed.
    Plone 5.1 is scheduled to prefer the ``default`` profile.
    For more information on this plan,
    see `PLIP 1340 <https://github.com/plone/Products.CMFPlone/issues/1340>`_.


Add-on-specific issues
======================

Add-on products may contain:

* A default GenericSetup XML profile which is automatically run when the
  product is installed using the quick-installer. The profile name is
  "default".

* Other profiles which the user may install using the ``portal_setup`` *Import* tab, or which can be manually enabled for unit tests.

* An "Import various" step, which runs Python code every time the GenericSetup XML profile is installed.

For more information about custom import steps, see:

* http://plone.293351.n2.nabble.com/indexing-of-content-created-by-Generic-Setup-td4454703.html


Listing available profiles
==========================

Example::

        # List all profiles know to the Plone instance.
        setup_tool = self.portal.portal_setup

        profiles = setup_tool.listProfileInfo()
        for profile in profiles:
            print str(profile)

Results::

    {'product': 'PluggableAuthService', 'description': 'Content for an empty PAS (plugins registry only).', 'for': <InterfaceClass Products.PluggableAuthService.interfaces.authservice.IPluggableAuthService>, 'title': 'Empty PAS Content Profile', 'version': 'PluggableAuthService-1.5.3', 'path': 'profiles/empty', 'type': 1, 'id': 'PluggableAuthService:empty'}
    {'product': 'Products.CMFDefault', 'description': u'Profile for a default CMFSite.', 'for': <InterfaceClass Products.CMFCore.interfaces._content.ISiteRoot>, 'title': u'CMFDefault Site', 'version': 'CMF-2.1.1', 'path': u'profiles/default', 'type': 1, 'id': u'Products.CMFDefault:default'}
    {'product': 'Products.CMFPlone', 'description': u'Profile for a default Plone.', 'for': <InterfaceClass Products.CMFPlone.interfaces.siteroot.IPloneSiteRoot>, 'title': u'Plone Site', 'version': u'3.1.7', 'path': u'/home/moo/sits/parts/plone/CMFPlone/profiles/default', 'type': 1, 'id': u'Products.CMFPlone:plone'}
    {'product': 'Products.Archetypes', 'description': u'Extension profile for default Archetypes setup.', 'for': None, 'title': u'Archetypes', 'version': u'1.5.7', 'path': u'/home/moo/sits/parts/plone/Archetypes/profiles/default', 'type': 2, 'id': u'Products.Archetypes:Archetypes'}
    ...

Installing a profile
====================

This is usually unit test specific question how to enable certain add-ons for unit testing.

plone.app.testing
-----------------

See `Product and profile installation <http://docs.plone.org/external/plone.app.testing/docs/source/README.html#product-and-profile-installation>`_.

Manually
---------

You might want to install profiles manually if they need to be enabled only for certain tests.

The profile name is in the format ``profile-${product name}:${profile id}``

Unit testing example::

    # Run the extended profile of the betahaus.emaillogin package.
    setup_tool.runAllImportStepsFromProfile('profile-betahaus.emaillogin:extended')


Missing upgrade procedure
=========================

In the add-ons control panel you may see a warning that your add-on is
`missing an upgrade procedure <http://stackoverflow.com/questions/15316583/how-to-define-a-procedure-to-upgrade-an-add-on>`_.

This means you need to write some `Upgrade steps`_.


Uninstall profile
=================

For the theory, see:
`<http://blog.keul.it/2013/05/how-to-make-your-plone-add-on-products.html>`_

For an example, see the `collective.pdfpeek source code
<https://github.com/collective/collective.pdfpeek/tree/master/collective/pdfpeek/profiles>`_.


Dependencies
============

GenericSetup profile can contain dependencies to other add-on product installers and profiles.

* `More information about GenericSetup dependencies <https://plone.org/products/plone/roadmap/195/>`_.

For example, if you want to declare a dependency to the *collective.basket* add-on product,
so that it is automatically installed when your add-on is installed,
you can use the declaration below.
This way,
you can be sure that all layers, portlets, and other features which require database changes,
are usable from the *collective.basket* add-on product when your add-on product is run.

``metadata.xml``:

.. code-block:: xml

        <?xml version="1.0"?>
        <metadata>
          <version>1000</version>
          <dependencies>
            <dependency>profile-collective.basket:default</dependency>
          </dependencies>
        </metadata>

*collective.basket* declares the profile in its configure.zcml:

.. code-block:: xml

    <genericsetup:registerProfile
        name="default"
        title="collective.basket"
        directory="profiles/default"
        description='Collector portlet framework'
        provides="Products.GenericSetup.interfaces.EXTENSION"
        />


.. warning::

    Unlike other GenericSetup XML files,
    ``metadata.xml`` is read on the start-up and this read is cached.
    Always restart Plone after editing ``metadata.xml``.
    If your ``metadata.xml`` file contains syntax errors
    or dependencies to a missing or non-existent product
    (e.g. due to a typo in a name) your add-on will disappear from the
    installation control panel.

.. note::

    For some old products in the ``Products.*`` Python namespace,
    you must not include the full package name in the dependencies.
    This is true when this product has registered its profile in Python instead of zcml,
    and there it has used only part of its package name.
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

Some old packages may have a ``metadata.xml`` without version number,
but this is considered bad practice.
What should the version number in your ``metadata.xml`` be?
This mostly matters when you are adding upgrade steps,
See also the `Upgrade steps`_ section.
Upgrade steps have a sort order in which they are executed.
This used to be alphabetical sorting.
When you had eleven upgrade steps, marked from 1 through 11,
alphabetical sorting meant this order: 1, 10, 11, 2, 3, etc.
If you are seeing this, then you are using an old version of GenericSetup.
You want numerical sorting here, which is correctly done currently.
Versions with dots work fine too.
They get ordered just like they would when used for packages on PyPI.
So far for the background information.

Best practice for all versions of GenericSetup is this:

- Start with 1000.
  This avoids problems with ancient GenericSetup that used alphabetical sorting.

- Simply increase the version by 1 each time you need a new metadata version.
  So 1001, 1002, etc.

- If your package version number changes, but your profile stays the same and no upgrade step is needed, you should **not** change the metadata version.
  There is simply no need.

- If you make changes for a new major release, you should increase the metadata version significantly.
  This leaves room for small metadata version increases on a maintenance branch.
  Example:
  You have branch master with version 1025.
  You make backwards incompatible changes and you increase the version to 2000.
  You create a maintenance branch where the next metadata version will be 1026.


Custom installer code (``setuphandlers.py``)
============================================

Besides out-of-the-box XML steps which easily provide both install and uninstall,
GenericSetup provides a way to run a custom Python code when your
add-on product is installed and uninstalled.
This is not a very straightforward process, though.

.. note::

    An easier way may be possible for you.
    GenericSetup 1.8.2 (not yet released as of this writing)
    has an option to point to a function to run before or after applying all import steps for your profile.
    If you do not need to support older versions,
    this is the easiest way.

    In ``configure.zcml``::

        <configure
            xmlns="http://namespaces.zope.org/zope"
            xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
            i18n_domain="your.package">

          <genericsetup:registerProfile
              name="default"
              title="My Package"
              directory="profiles/default"
              description="A useful package"
              provides="Products.GenericSetup.interfaces.EXTENSION"
              pre_handler="your.package.setuphandlers.run_before"
              post_handler="your.package.setuphandlers.run_after"
              />

        </configure>

    In ``setuphandlers.py``::

        def run_before(context):
            # This is run before running the first import step of
            # the default profile.  context is portal_setup.
            pass

        def run_after(context):
            # This is run after running the last import step of
            # the default profile.  context is portal_setup.
            pass

The best practice is to create a ``setuphandlers.py`` file
which contains function ``setup_various()`` which runs required
Python code to make changes to Plone site object.
This function is registerd as a custom ``genericsetup:importStep``
in XML.

.. note::

    When you do custom ``importStep``\s, remember to write uninstallation
    code as well.

However, the trick is that all GenericSetup import steps, including
your custom step, are run for *every* add-on product
when they are installed. Thus, if your need to run
code which is specific **during your add-on install only**
you need to use a marker text file which is checked by GenericSetup
context.

Also you need to register this custom import step in ``configure.zcml``

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup">

      <genericsetup:importStep
          name="your.package"
          title="your.package special import handlers"
          description=""
          handler="your.package.setuphandlers.setup_various"
          />

    </configure>

You can run other steps before yours by using the ``depends`` directive.
For instance, if your import step depends on a content type to be installed first, you must use:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup">

      <genericsetup:importStep
          name="your.package"
          title="your.package special import handlers"
          description=""
          handler="your.package.setuphandlers.setup_various">
        <depends name="typeinfo" />
      </genericsetup:importStep>

    </configure>

``setuphandlers.py`` example

.. code-block:: python

    __docformat__ = "epytext"

    def run_custom_code(site):
        """Run custom add-on product installation code to modify Plone
           site object and others

        @param site: Plone site
        """

    def setup_various(context):
        """
        @param context: Products.GenericSetup.context.DirectoryImportContext instance
        """

        # We check from our GenericSetup context whether we are running
        # add-on installation for your product or any other proudct
        if context.readDataFile('your.package.marker.txt') is None:
            # Not your add-on
            return

        portal = context.getSite()

        run_custom_code(portal)

And add a dummy text file
``your.package/your/package/profiles/default/your.package.marker.txt``::

    This text file can contain any content - it just needs to be present

More information

* http://keeshink.blogspot.com/2009/02/creating-portal-content-in.html

* http://maurits.vanrees.org/weblog/archive/2009/12/catalog (unrelated, but contains pointers)


Overriding import step order
============================

If you need to override the order of import steps in a package that is not yours,
it might work if you `use an overrides.zcml <http://plone.293351.n2.nabble.com/Overriding-import-step-order-td2189638.html>`_.


Controlling the import step execution order
-------------------------------------------

If you only need to control the execution order of one of your own custom import steps,
you can do this in your import step definition in zcml.
To make sure the catalog and typeinfo steps are run before your own step,
use this code:

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

    The name that you need, is usually the name of the related xml file,
    but with the ``.xml`` stripped.
    For the ``catalog.xml`` the import step name is ``catalog``.
    But there are exceptions.
    For the ``types.xml`` and the ``types`` directory,
    the import step name is ``typeinfo``.
    See `Plone GenericSetup Reference`_ for a list.

* http://plone.293351.n2.nabble.com/indexing-of-content-created-by-Generic-Setup-td4454703.html


Upgrade steps
=============

You can define upgrade steps to run code only when someone upgrades your
product from version *x* to *y*.

As an example, let's say that the new version of YOUR.PRODUCT defines a
*price* field on a content type *MyType* to be a string, but previously
(version 1.1.  and earlier) it was a float. Code that uses this field and
assumes it to be a float will break after the upgrade, so you'd like to
automatically convert existing values for the field to string.

(Obviously, you could do this very quickly in a simple script, but having a
GenericSetup upgrade step means non-technical people can do it as well. As it
turns out, once you have the script, it's easy to put its code in an upgrade
step.)


Increment profile version
-------------------------

First increase the number of the version in the ``profiles/default/metadata.xml``.
This version number should be an integer.
Package version are different because they add sense like the status of the addon:
is it stable, is it in dev, in beta, which branch is it.
A profile version indicates only that you have to migrate data in the database.


Add upgrade step
----------------

Next we add an upgrade step:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
        i18n_domain="YOUR.PRODUCT">

      <genericsetup:upgradeStep
          title="Convert Price to strings"
          description="Price was previously a float field, it should be converted to string"
          source="1000"
          destination="1100"
          handler="YOUR.PRODUCT.upgrades.convert_price_to_string"
          sortkey="1"
          profile="YOUR.PRODUCT:default"
          />

    </configure>


* You can use a wildcard character for *source* to indicate an upgrade for any previous version.
  Since Products.GenericSetup 1.7.6 this works fine.
  To run the upgrade step only when upgrading from a specific version, use that version's number.

* The optional *sortkey* can be used to indicate the order in which upgrade steps are run.


Add upgrade code
----------------

The code for the upgrade method itself is best placed in a *upgrades.py* module::

    from plone import api
    import logging

    PROFILE_ID = 'profile-YOUR.PRODUCT:default'


    def convert_price_to_string(context, logger=None):
        """Method to convert float Price fields to string.

        When called from the import_various method, 'context' is
        the plone site and 'logger' is the portal_setup logger.

        But this method will be used as upgrade step, in which case 'context'
        will be portal_setup and 'logger' will be None."""

        if logger is None:
            # Called as upgrade step: define our own logger.
            logger = logging.getLogger('YOUR.PRODUCT')

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
                voorstelling = brain.getObject()
                voorstelling.setPrice(str(current_price))
                voorstelling.reindexObject()
                count += 1

        setup.runImportStepFromProfile(PROFILE_ID, 'catalog')
        logger.info("%s fields converted." % count)

Other examples of using generic setup to run import steps are below

If you want to call types.xml use typeinfo::

        setup.runImportStepFromProfile(PROFILE_ID, 'typeinfo')

If you want to call workflow.xml use workflow::

        setup.runImportStepFromProfile(PROFILE_ID, 'workflow')

The ids of the various default import steps are defined in several places.
Some of the most used ones are here:

* https://github.com/zopefoundation/Products.CMFCore/blob/master/Products/CMFCore/exportimport/configure.zcml

* https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/exportimport/configure.zcml

After restarting Zope, your upgrade step should be visible in the ZMI: The
*portal_setup* tool has a tab *Upgrades*. Select your product profile to see
which upgrade steps Zope knows about for your product.

You can create many upgrade steps under one migration. This is useful when
you want to have the ability to re-run some parts of the migration and make
your code more re-useable (for example cook css resource of your theme).

Here is an example of many upgrade steps you can have to achieve on a
site policy:

.. code-block:: xml

    <genericsetup:upgradeSteps
        source="3900"
        destination="4000"
        profile="project.policy:default">

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

      <genericsetup:upgradeStep
          title="Upgrade resources"
          description="Update javascripts and css"
          handler=".v4.upgrade_resources"
          />

      <genericsetup:upgradeStep
          title="Apply new steps of of policy"
          description=""
          handler=".v4.upgrade_of_policy"
          />

      <genericsetup:upgradeStep
          title="upgrade rules"
          description="collective.contentrules.mail is deprecated, replace with default"
          handler=".v4.upgrade_contentrules"
          />

      <genericsetup:upgradeStep
          title="upgrade views"
          description="get ride of dot in viewname zone1.html -> zone1_view"
          handler=".v4.upgrade_views"
          />

      <genericsetup:upgradeStep
          title="remove instance of deprecated portlets"
          description=""
          handler=".v4.remove_portlets"
          />

    </genericsetup:upgradeSteps>


Add-on product appears twice in the installer list
===================================================

This happens if you are developing your own add-on and keep changing things.
You have an error in your add-on product ZCML code which causes
portal_quickinstaller to have two entries.

More information

* http://plone.293351.n2.nabble.com/Product-twice-in-quickinstaller-td5345492.html#a5345492


Preventing uninstall
====================

You might want to prevent your add-on product uninstall for some reason.

Example:

.. code-block:: python

        from zExceptions import BadRequest


        def uninstall(self, reinstall):
            if reinstall == False:
                raise BadRequest('This product cannot be uninstalled!')


.. note ::

    This example is for Extensions/install.py, an old Plone 2 way of writing installers and uninstallers.
    It is still working in Plone 5.0,
    but will likely go away in Plone 5.1.


Best Practices
==============

The ``purge`` attribute
-----------------------

When importing items such as property sheets,
make sure not to override other profile settings:
set the ``purge`` attribute to False.
This will *add* the listed items to the property instead of resetting the property.
Example:

.. code-block:: xml

    <property name="metaTypesNotToList" type="lines" purge="False">
      <element value="File"/>
      <element value="Image"/>
    </property>


The ``remove`` attribute
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
  So ``remove="false"`` may mean the item stays and may mean it gets removed.
  Best is to either use ``remove="true"`` or leave the entire keyword away.


Only use the configuration that you need
----------------------------------------

When you export your site's configuration, it will include things that you don't need.
For example,
if you needed to change only the 'Allow anonymous to view about' property,
this is what your propertiestool.xml should look like:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_properties" meta_type="Plone Properties Tool">
      <object name="site_properties" meta_type="Plone Property Sheet">
        <property name="allowAnonymousViewAbout" type="boolean">True</property>
      </object>
    </object

.. original content from http://www.sixfeetup.com/company/technologies/plone-content-management-new/quick-reference-cards/swag/swag-images-files/generic_setup.pdf


Generic Setup files
===================


actions.xml
-----------


componentregistry.xml
---------------------

Setup items in the local component registry of the Plone Site.
The items can be adapters, subscribers, or utilities.
This can also be done in zcml, which puts it in the global registry that is defined at startup.
The difference is:
when you put it in xml, the item is only added to a specific Plone Site when you install the package in the add-ons control panel.
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

.. automodule:: Products.GenericSetup.components
  :members: ComponentRegistryXMLAdapter importComponentRegistry


contentrules.xml
----------------

.. automodule:: plone.app.contentrules.exportimport


Content Generation
------------------

.. automodule:: Products.GenericSetup.content
 :members: FolderishExporterImporter


cssregistry.xml
---------------

see :ref:`resourceregistries`


jsregistry.xml
--------------

see :ref:`resourceregistries`


kssregistry.xml
---------------

see :ref:`resourceregistries`

.. _resourceregistries:


metadata.xml
------------

This is a special one.
The ``metadata.xml`` file is read during Plone start-up.
If this file has problems your add-on might not appear in the installer control panel.
The ``metadata.xml`` file contains add-on dependency and version information.

.. code-block:: xml

    <?xml version="1.0"?>
    <metadata>
     <version>1000</version>
     <dependencies>
       <dependency>profile-collective.basket:default</dependency>
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


portlets.xml
------------

.. automodule:: plone.app.portlets.exportimport.portlets


propertiestool.xml
------------------
In the propertiestool.xml you can change all values of the portal_properties.

take a look at: https://plone.org/documentation/manual/developer-manual/generic-setup/reference/properties-ref


pluginregistry.xml
------------------

This configures PAS plugin orderings and active plugins. It isn't part of Plone
itself, it is used by other frameworks and can be used in Plone with a little
extra configuration.

First, you need a monkey patch in your ``__init__.py``` to point the importer at
where Plone keeps its PAS plugins.

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


repositorytool.xml
------------------

.. autoclass:: Products.CMFEditions.exportimport.repository.RepositoryToolXMLAdapter


Resource Registries
-------------------

.. automodule:: Products.ResourceRegistries.exportimport.resourceregistry
  :members: ResourceRegistryNodeAdapter


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

The permission must already exist on the Zope level,
otherwise you get an error when installing your profile::

  ValueError: The permission <em>Pass the bridge</em> is invalid.

A permission is created on the Zope level when it is used in code.
See :doc:`Creating permissions </develop/plone/security>`.

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

Skins are old fashioned, so you may not need this.
The more modern way is: use browser views and static directories.
But skins are still installed by several packages.

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
``Products.CMFPlone`` set good defaults:

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


toolset.xml
-----------

This is used to add a tool to the site.

.. warning::

    This is an old way and should not be used in new code.
    You should probably register a utility instead of a tool.
    ``componentregistry.xml`` might be an alternative,
    but registering a utility in zcml would be better.
    If the utility needs configuration,
    you can use ``registry.xml``.

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

  Adding a forbidden tool that was first required,
  like in the example above,
  is not yet supported.
  See https://github.com/zopefoundation/Products.GenericSetup/pull/26

.. automodule:: Products.GenericSetup.registry
 :members: _ToolsetParser ToolsetRegistry

.. automodule:: Products.GenericSetup.tool
 :members: importToolset


viewlets.xml
------------

.. automodule:: plone.app.viewletmanager.exportimport.storage


workflows.xml
-------------

.. automodule:: Products.DCWorkflow.exportimport
