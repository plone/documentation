=================
 Dexterity
=================

.. admonition:: Description

    Dexterity content subsystem for Plone: info for the developers.

.. contents:: :local:

Introduction
===================

Dexterity is a subsystem for content objects. It is intended to replace the
default Archetypes system from Plone 5 and onward and can be already used
with Plone 4.


* :doc:`Dexterity developer manual </external/plone.app.dexterity/docs/index>`

* :doc:`How Dexterity is related to Archetypes </external/plone.app.dexterity/docs/intro>`

ZopeSkel templates
====================

Please see :doc:`ZopeSkel page </develop/addons/paste>` for project skeleton
templates for Dexterity.

Here is an example how to create your own add-on using the buildout below

.. code-block:: console

    cd src
    ../bin/zopeskel dexterity yourcompany.app

Edit ``buildout.cfg`` and add::

    eggs =
        yourcompany.app

    develop =
        src/yourcompany.app

Then rerun buildout to get your new add-on skeleton included in the
configuration

.. code-block:: console

    cd ..
    bin/buildout

Now you can start adding content into your add-on

.. code-block:: console

    cd src/yourcompany.app
    ../../bin/paster # Shows availablility of addcontent command
    ../../bin/paster addcontent -l # Shows available templates (content, field, behavior, etc...)


Buildout example
====================

Below is a sample example which will install

* Plone 4.1 beta 1
* Dexterity 1.0 beta 7
* Paster command + Dexterity templates

Please tune the versions according the latest available releases.

``buildout.cfg``::

    [buildout]
    parts =
        instance
        zopepy
        i18ndude
        zopeskel
        test
        paster
        omelette

    extends =
        http://dist.plone.org/release/4.1b1/versions.cfg
        http://good-py.appspot.com/release/dexterity/1.0b7?plone=4.1b1

    # Add additional egg download sources here. dist.plone.org contains archives
    # of Plone packages.
    find-links =
        http://dist.plone.org/release/4.1b1
        http://dist.plone.org/thirdparty

    extensions =
        mr.developer
        buildout.dumppickedversions
        buildout.threatlevel

    sources = sources

    versions = versions

    # Reference any folders where you have Python egg source code under development here
    # e.g.: develop = src/my.package
    # If you are using the mr.developer extension and have the source code in a
    # repository mr.developer will handle this automatically for you
    develop =


    # Create bin/instance command to manage Zope start up and shutdown
    [instance]
    recipe = plone.recipe.zope2instance
    user = admin:admin
    http-address = 8080
    debug-mode = off
    verbose-security = on
    blob-storage = var/blobstorage

    eggs =
            Plone
            plone.app.dexterity

    # Some pre-Plone 3.3 packages may need you to register the package name here in
    # order their configure.zcml to be run (https://plone.org/products/plone/roadmap/247)
    # - this is never required for packages in the Products namespace (Products.*)
    zcml =


    # zopepy commands allows you to execute Python scripts using a PYTHONPATH
    # including all the configured eggs
    [zopepy]
    recipe = zc.recipe.egg
    eggs = ${instance:eggs}
    interpreter = zopepy
    scripts = zopepy

    # create bin/i18ndude command
    [i18ndude]
    unzip = true
    recipe = zc.recipe.egg
    eggs = i18ndude

    # create bin/test command
    [test]
    recipe = zc.recipe.testrunner
    defaults = ['--auto-color', '--auto-progress']
    eggs =
        ${instance:eggs}

    [paster]
    recipe = zc.recipe.egg
    eggs =
       ZopeSkel
       PasteScript
       PasteDeploy
       zopeskel.dexterity
       ${instance:eggs}
    entry-points = paster=paste.script.command:run

    # create ZopeSkel command
    [zopeskel]
    unzip = true
    recipe = zc.recipe.egg
    eggs =
        ZopeSkel
        ${instance:eggs}

    # symlinks all Python source code to parts/omelette folder when buildout is run
    # windows users will need to install additional software for this part to build
    # correctly.  See https://pypi.python.org/pypi/collective.recipe.omelette for
    # relevant details.
    [omelette]
    recipe = collective.recipe.omelette
    eggs = ${instance:eggs}

    # Put your mr.developer managed source code repositories here, see
    # https://pypi.python.org/pypi/mr.developer for details on format for this part
    [sources]
    collective.developermanual = git git://github.com/collective/collective.developermanual.git

    # Version pindowns for new style products go here - this section extends one provided in http://dist.plone.org/release/
    [versions]


Content creation permissions
=============================

By default, (global) Dexterity content types are addable to a folder if the
editor has the ``cmf.AddPortalContent`` permission.

You might want to fine-tune permissions so that only certain privileged
members are allowed to create certain content types.

.. note:: This behavior differs from Archetypes behavior where each content
   type was automatically assigned a permission for controlling its
   creation.

Create a permission with
:doc:`collective.autopermission </develop/plone/security/permissions>` in
``configure.zcml``

.. code-block:: xml

    <include package="collective.autopermission" />
    <permission id="yourcompany.app.AddSuperContent" title="yourcompany.app: Add Super Content" />

Make sure that this permission becomes available on your site by adding the following to ``rolemap.xml``

.. code-block:: xml

    <?xml version="1.0"?>
    <rolemap>
       <permissions>
             <permission
             name="yourcompany.app: Add Super Content"
             acquire="True">
             <role name="Manager" />
             </permission>
      </permissions>
    </rolemap>

Add in your content type GenericSetup XML

.. code-block:: xml

    <!-- add permission -->
    <property name="add_permission">yourcompany.app.AddSuperContent</property>

Reinstall your add-on.

Confirm that the new permission appears on the :guilabel:`Security` tab in
the :term:`ZMI` root.

Exclusion from navigation
===========================

This must be enabled separately for Dexterity content types with a behavior.

.. code-block:: xml

    <property name="behaviors">
        <element value="plone.app.content.interfaces.INameFromTitle" />
        <element value="plone.app.dexterity.behaviors.metadata.IBasic"/>
        <element value="plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation"/>
    </property>

Then you can manually also check this property::

    for t in self.tabs:
        nav = None
        try:
            nav = IExcludeFromNavigation(t)
        except:
            pass
        if nav:
            if nav.exclude_from_nav == True:
                # FAQ page - do not show in tabs
                continue


Custom add form/view
======================

Dexterity relies on ``++add++yourcontent.type.name`` traverser hook defined
in ``Products/CMFCore/namespace.py``.

It will look up a multi-adapter using this expression::

    if ti is not None:
        add_view = queryMultiAdapter((self.context, self.request, ti),
                                     name=ti.factory)
        if add_view is None:
            add_view = queryMultiAdapter((self.context, self.request, ti))

The ``name`` parameter is the ``portal_types`` id of your content type.

You can register such an adapter in ``configure.zcml``

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        >

        <adapter
            for="Products.CMFCore.interfaces.IFolderish
                 Products.CMFDefault.interfaces.ICMFDefaultSkin
                plone.dexterity.interfaces.IDexterityFTI"
            provides="zope.publisher.interfaces.browser.IBrowserPage"
            factory=".flexicontent.AddView"
            name="your.app.flexiblecontent"
            />

    </configure>


Then you can inherit from the proper ``plone.dexterity`` base classes::

    from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView

    class AddForm(DefaultAddForm):

        def update(self):
            DefaultAddForm.update(self)

        def updateWidgets(self):
            """ """
            # Some custom code here

        def getBlockPlanJSON():
            return getBlockPlanJSON()

    class AddView(DefaultAddView):
        form = AddForm

See also:

* :doc:`FTI </develop/plone/content/types>`

* :doc:`z3c.form </develop/plone/forms/z3c.form>`


Custom edit form
====================

Example::

    from five import grok
    from plone.directives import dexterity

    class EditForm(dexterity.EditForm):

        grok.context(IFlexibleContent)

        def updateWidgets(self):
            """ """
            dexterity.EditForm.updateWidgets(self)

            # XXX: customize widgets here

Registering an edit form works by registering a normal browser page.

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        >

        <browser:page
            for="your.app.flexiblecontent"
            class=".flexicontent.EditView"
            name="edit"
            />

    </configure>

In the example above it is important, that you give the browser page the name "edit".
