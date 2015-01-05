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
* registering Javascript files,
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

* `GenericSetup tutorial <https://plone.org/documentation/tutorial/genericsetup>`_

* `GenericSetup product page <https://pypi.python.org/pypi/Products.GenericSetup/1.4.5>`_.

* `Source code <http://svn.zope.org/Products.GenericSetup/trunk/Products/GenericSetup/README.txt?rev=87436&view=auto>`_.

.. TODO:: should the link be specifically to rev=87436?


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



Add-on-specific issues
======================

Add-on products may contain:

* A default GenericSetup XML profile which is automatically run when the
  product is installed using the quick-installer. The profile name is
  "default".

* Other profiles which the user may install using the ``portal_setup`` *Import* tab, or which can be manually enabled for unit tests.

* An "Import various" step, which runs Python code every time the GenericSetup XML profile is installed.

For more information about custom import steps, see:

* http://n2.nabble.com/indexing-of-content-created-by-Generic-Setup-tp4454703p4454703.html

Listing available profiles
==========================

Example::

        # Run the default quick installer profile
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

PloneTestCase.setupPloneSite
----------------------------

See *Running add-on installers and extensions profiles for unit tests*.

Manually
---------

You might want to install profiles manually if they need to be enabled only for certain tests.

The profile name is in the format ``profile-${product name}:${profile id}``

Unit testing example::

    # Run the extended profile which will create email_catalog
    setup_tool.runAllImportStepsFromProfile('profile-betahaus.emaillogin:exdended')

Upgrade steps
==================

If you need to migrate data or settings on new add-on versions

* http://stackoverflow.com/questions/15316583/how-to-define-a-procedure-to-upgrade-an-add-on

Uninstall profile
==================

For the theory, see:
`<http://blog.keul.it/2013/05/how-to-make-your-plone-add-on-products.html>`_

For an example, see the `collective.pdfpeek source code
<http://svn.plone.org/svn/collective/collective.pdfpeek/trunk/collective/pdfpeek/profiles/>`_.


Dependencies
============

GenericSetup profile can contain dependencies to other add-on product installers and profiles.

* `More information about GenericSetup dependencies <https://plone.org/products/plone/roadmap/195/>`_.

For example, if you want to declare dependency to *collective.basket* add-on product, so that it
is automatically installed when your add-on installed you can use the declaration below.
This way, you can be sure that all layers, portlets, etc. features which require database changes
are usable from *collective.basket* add-on products when your add-on product is run.

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

    The ``Products.*`` Python namespace needs to declare generic setup
    dependencies specially:
    You actually do not mention ``Products.xxx`` space.

To declare dependency to ``Products.Carousel``:

.. code-block:: xml

    <?xml version="1.0"?>
    <metadata>
      <version>1000</version>
      <!-- Install Products.Carousel on the site when this add-on is installed -->
      <dependencies>
        <dependency>profile-Carousel:default</dependency>
      </dependencies>
    </metadata>


Custom installer code (``setuphandlers.py``)
============================================

Besides out-of-the-box XML steps which easily provide both install and uninstall,
GenericSetup provides a way to run a custom Python code when your
add-on product is installed and uninstalled.
This is not very straightforward process, though.

The best practice is to create a ``setuphandlers.py`` file
which contains function ``setupVarious()`` which runs required
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

      <!-- Register the import step -->
      <genericsetup:importStep
          name="your.package"
          title="your.package special import handlers"
          description=""
          handler="your.package.setuphandlers.setupVarious"
          />

    </configure>

``setuphandlers.py`` example

.. code-block:: python

    __docformat__ = "epytext"

    def runCustomCode(site):
        """ Run custom add-on product installation code to modify Plone site object and others

        @param site: Plone site
        """

    def setupVarious(context):
        """
        @param context: Products.GenericSetup.context.DirectoryImportContext instance
        """

        # We check from our GenericSetup context whether we are running
        # add-on installation for your product or any other proudct
        if context.readDataFile('your.package.marker.txt') is None:
            # Not your add-on
            return

        portal = context.getSite()

        runCustomCode(portal)

And add a dummy text file
``your.package/your/package/profiles/default/your.package.marker.txt``::

    This text file can contain any content - it just needs to be present

More information

* http://keeshink.blogspot.com/2009/02/creating-portal-content-in.html

* http://maurits.vanrees.org/weblog/archive/2009/12/catalog (unrelated, but contains pointers)

Overriding import step order
===============================

You need ``import_steps.xml``.

More information

* http://plone.293351.n2.nabble.com/Overriding-import-step-order-td2189638.html

* http://dev.communesplone.org/trac/browser/communesplone/urban/trunk/profiles/default/import_steps.xml?rev=5652

Controlling the import step execution order
-------------------------------------------

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

First increase the number of the version in the ``profiles/default/metadata.xml``. This version
number should be an integer. Package version are different because they
add sens like the status of the addon: is it stable, is it in dev, in beta,
which branch it is. A profile version indicate only that you have to migrate
data in the database.

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


* You can use a wildcard character for *source* to indicate an upgrade for any
  previous version. To run the upgrade step only when upgrading from a specific
  version, use that version's number.

* A *sortkey* can be used to indicate the order in which upgrade steps are
  run.

Add upgrade code
----------------

The code for the upgrade method itself is best placed in a *upgrades.py* module::

    import logging
    PROFILE_ID='profile-YOUR.PRODUCT:default'

    def convert_price_to_string(context, logger=None):
        """Method to convert float Price fields to string.

        When called from the import_various method, 'context' is
        the plone site and 'logger' is the portal_setup logger.

        But this method will be used as upgrade step, in which case 'context'
        will be portal_setup and 'logger' will be None.

        """
        if logger is None:
            # Called as upgrade step: define our own logger.
            logger = logging.getLogger('YOUR.PRODUCT')

        # Run the catalog.xml step as that may have defined new metadata
        # columns.  We could instead add <depends name="catalog"/> to
        # the registration of our import step in zcml, but doing it in
        # code makes this method usable as upgrade step as well.
        # Remove these lines when you have no catalog.xml file.
        setup = getToolByName(context, 'portal_setup')
        setup.runImportStepFromProfile(PROFILE_ID, 'catalog')

        catalog = getToolByName(context, 'portal_catalog')
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

The ids of the various default import steps are defined in the import_steps.xml of CMFDefault.
visit it at http://svn.zope.org/CMF/branches/2.1/CMFDefault/profiles/default/import_steps.xml?logsort=date&rev=78624&view=markup

XXX Fix the link above

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

    This example if for Extensions/install.py, old Plone 2 way of writing installers



Plone GenericSetup Reference
============================

portlets.xml
------------

.. automodule:: plone.app.portlets.exportimport.portlets

viewlets.xml
------------

.. automodule:: plone.app.viewletmanager.exportimport.storage

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

Resource Registries
-------------------

.. automodule:: Products.ResourceRegistries.exportimport.resourceregistry
  :members: ResourceRegistryNodeAdapter

Content Generation
------------------

.. automodule:: Products.GenericSetup.content
 :members: FolderishExporterImporter


Generic Setup files
===================

sharing.xml
-----------

The sharing.xml file let you add custom roles to the sharing tab.
For reference, visit: :doc:`Local Roles </develop/plone/security/local_roles>`.

tinymce.xml
-----------

propertiestool.xml
------------------
In the propertiestool.xml you can change all values of the portal_properties.

take a look at: https://plone.org/documentation/manual/developer-manual/generic-setup/reference/properties-ref

metadata.xml
------------

actions.xml
-----------

skins.xml
---------

workflows.xml
-------------

.. automodule:: Products.DCWorkflow.exportimport

repositorytool.xml
------------------

.. autoclass:: Products.CMFEditions.exportimport.repository.RepositoryToolXMLAdapter


contentrules.xml
----------------

.. automodule:: plone.app.contentrules.exportimport


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


Best Practices
--------------

When importing items such as property sheets, make sure not to
override other profile settings by setting the purge attribute to False.
This will add the items listed to the property instead of resetting the
property. Example:

.. code-block:: xml

    <property name="metaTypesNotToList" type="lines" purge="False">
      <element value="File"/>
      <element value="Image"/>
    </property>

Only use the configuration that you need. When you export your site's
configuration, it will include things that you don't need. For example,
if you needed to change only the 'Allow anonymous to view about'
property, this is what your propertiestool.xml would look like:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_properties" meta_type="Plone Properties Tool">
      <object name="site_properties" meta_type="Plone Property Sheet">
        <property name="allowAnonymousViewAbout" type="boolean">True</property>
      </object>
    </object

.. original content from http://www.sixfeetup.com/company/technologies/plone-content-management-new/quick-reference-cards/swag/swag-images-files/generic_setup.pdf
