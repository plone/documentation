======================================
Updating add-on products for Plone 3.0
======================================

.. admonition:: Description

   Plone 3.0 ships with new releases of Zope, CMF and Archetypes.
   When any framework updates, some things will be removed or changed.
   This is a list of the most common updates that need to be applied by product authors to ensure that their products work on Plone 3.0.

.. contents:: :local:

General product development and migration tips for Plone 3.0
============================================================

Before we get started on the specific tips for how to update your product to work with Plone 3, let's mention some general recommendations that might save you time when updating your product in the next versions of Plone (3.5 and 4.0).

Depending on your product, it might be hard to include compatibility for both Plone 2.5 and Plone 3.0 in the same product.
There are several reasons for this, but the main ones are:

* The workflow definition standard in CMF has changed
* The new portlet infrastructure (although it does support old-style portlets, performance will suffer)
* The introduction of viewlets as the main way to render content fragments in the layout

So, the general recommendation is:

* If your product is more complex than a simple type, create two releases — one for Plone 2.5 and one for Plone 3.0.
* If you used ArchGenXML to create your product, you should be able to regenerate your product from the UML model to get a Plone 3.0-compatible version.

Tip
---

To further future-proof your product (for Plone 3.5 and 4.0), try the following:

* Start Zope in debug mode using 'zopectl fg' and use your product normally.
  Check if it outputs any deprecation warnings to the log window.
* Disable the 'plone_deprecated' skin layer and make sure your application still runs without it (this disables deprecated methods and deprecated CSS styles)

Other recommendations and suggestions
-------------------------------------

* You can use the contentmigration product to write migrations for your own products.
  More information on this product can be found in the "RichDocument tutorial":/documentation/tutorial/richdocument/migrations/
* A lot of the new components use Zope 3 views instead of templates.
  These can be customized through-the-web using the 'portal_view_customizations' tool.
* Do not ever rely on the JS libraries in Plone being the same across releases.
  Use the KSS abstractions, the underlying implementation might (and will!) change.

These things are not mandatory yet, but represent best-practice recommendations that will save you from updating these parts in the future:
* QuickInstaller-based installation should use GenericSetup profiles instead
* use events instead of manage\_ methods (which will probably disappear in plone 3.5 or 4.0)


* Packaging technology:

  * Use python packages instead of Zope products
  * Ship packages as eggs and register them with the `PYthon Package Index <https://pypi.python.org/>`__
  * Use `Python Paste <http://pythonpaste.org/>`__ to create new packages


CMFCore.permission import syntax change
=======================================

In later CMF releases, the way to import the permissions module has changed.
Here's how to update your product to support both the new and the old-style syntax.

Typical error message when starting Zope::

    File "Products/PloneHelpCenter/content/HelpCenter.py", line 29, in ?
    from Products.CMFCore import CMFCorePermissions
    ImportError: cannot import name CMFCorePermissions

What's causing it:

The following line is a common statement to get access to the permissions module, typically in the '__init__.py' file::

    from Products.CMFCore import CMFCorePermissions

To make this work with both the new way of importing it and fall back to the old way if you're running an older version, replace the above with::

    try:  # New CMF
        from Products.CMFCore import permissions as CMFCorePermissions
    except ImportError:  # Old CMF
        from Products.CMFCore import CMFCorePermissions

Then you should be all set, and be able to support multiple versions with your product.
Note that the try/except block is only necessary if you want to support Plone 2.1, if you're targeting Plone 2.5 and above, you only have to do the variant listed under "New CMF" in the example above.

To see a live example of this change, consult this `Poi changeset <https://github.com/collective/Products.Poi/commit/4fbca095c64185dda0f7d58a1982c82b89f4012c#diff-8fc1f83856b97f0319c6a954b889e449>`__.

Transaction module is no longer implicitly in Archetypes
========================================================

In Archetypes 1.3 and 1.4, we imported transaction in the main module to work around a Zope 2.7 issue.
Since Zope 2.7 is no longer a supported release, this is no longer the case in Archetypes 1.5 (which is what ships with Plone 3.0).
Here's how to update your code.

Typical error message when starting Zope::

    from Products.Archetypes import transaction
    ImportError: cannot import name transaction

Archetypes no longer imports transaction, so you will have to do it in your own module now, if you are using it. Change occurences of::

    from Products.Archetypes import transaction

to::

    import transaction

For a live example, see this `Poi changeset <https://github.com/collective/Products.Poi/commit/4fbca095c64185dda0f7d58a1982c82b89f4012c#diff-83f55ebfdf46ffe7d466bfaf902e682f>`__.

get_transaction module rename
=============================

Zope has changed their syntax for getting transactions, and it has been deprecated in the the previous Zope releases for a while now.
Zope 2.10.x (which is what Plone 3.0 runs on) removes the old syntax, so you have to update your code accordingly.
Here's how.

Typical error message::

    NameError: global name 'get_transaction' is not defined

Just to show you a complete traceback of how this might look, here's the full thing as seen in a typical product install, where it is common to use subtransactions (for completeness and search engines)::

    2007-04-12 23:12:01 ERROR Zope.SiteErrorLog http://localhost:8080/nu/portal_quickinstaller/installProducts
    Traceback (innermost last):
    Module Products.CMFQuickInstallerTool.QuickInstallerTool, line 381, in installProduct
    __traceback_info__: ('Poi',)
    Module Products.ExternalMethod.ExternalMethod, line 231, in __call__
    __traceback_info__: ((<PloneSite at /nu>,), {'reinstall': False}, (False,))
    Module /Users/limi/Projects/Plone/3.0/Products/Poi/Extensions/Install.py, line 65, in install
    NameError: global name 'get_transaction' is not defined
    /Users/limi/Projects/Plone/3.0/Products/CMFQuickInstallerTool/QuickInstallerTool.py:409:
    DeprecationWarning: This will be removed in ZODB 3.7:
    subtransactions are deprecated; use sp.rollback() instead of transaction.abort(1),
    where `sp` is the corresponding savepoint captured earlier
    transaction.abort(sub=True)

To update this, replace::

    get_transaction().commit(1)

with::

    transaction.commit(1)

(keep the '(1)' part if it already exists in the code, omit it otherwise)

You might have to add an 'import transaction' statement at the top of your file if you haven't imported it already.

For a live example, see the Install.py part of this `Poi changeset <https://github.com/collective/Products.Poi/commit/4fbca095c64185dda0f7d58a1982c82b89f4012c#diff-347b4813ab7ff9876b5f5066c175f2b9>`__.

ContentFactoryMetadata deprecation
==================================

CMF deprecated this call a while back, and Plone 3.0 is the first version that ships without this.
Here's how to update your product to use the new syntax.

Typical error message::

    Error Type: exceptions.ImportError
    Error Value: cannot import name ContentFactoryMetadata

What causes this? Somewhere in your code, you have something like::

    from Products.CMFCore.TypesTool import ContentFactoryMetadata

Update this to::

    from Products.CMFCore.TypesTool import FactoryTypeInformation

instead, and you should be good to go. This change should work all the way back to Plone 2.1.

Update your workflows to use GenericSetup profiles
==================================================

To install workflows in Plone 3.0, you have to make use of CMF's GenericSetup profiles.
Installing workflows in any other way is not supported, unfortunately — there are architectural changes in CMF that cannot support both approaches at the same time.

Installing workflows via GenericSetup will make your product work only on Plone 2.5 and upwards, so make sure you create a special release/branch if you want your product to still work on Plone 2.1/2.0 (which are unsupported releases when Plone 3.0 is released).

Typical error message that indicates that you are trying to install workflows not using GenericSetup::

    ImportError: cannot import name addWorkflowFactory

For existing workflows, the easiest way to make the product install use GenericSetup for workflows is:

* Install your product (and its workflows) using Plone 2.5.
* Using the 'portal_setup' tool in the ZMI, export a snapshot of the current site profile:
  * Click the 'Export' tab.
  * Select the parts you want to export the configuration for (in this case, 'Workflow Tool').
  * Click the 'Export Selected Steps' button.
  * You will now get a tar file named something like 'setup_tool-20070424225827.tar'.

* Unpack the tar file, and put the resulting files and directories in a directory 'profiles/default/' in the root of your product.
* Remove the workflow directories in 'workflow/' that are not part of your product, and edit 'workflows.xml' so that it only has the information for your workflows.
* Delete your old '.py'-based workflow definitions in 'Extensions', but make sure you keep any workflow scripts, since these will be referenced from the profile definitions.
* Add a 'configure.zcml' file in the root of your product that registers the default profile.
* Remove the redundant code from 'Extensions/Install.py' and add the boilerplate code to invoke the GS setup.

For a full example, see this big `Poi changeset <https://github.com/collective/Products.Poi/commit/ed9a931aa0c291fcf929a652b25df2d086edb1ee>`__.

This process is also the same for any code you want to move to GenericSetup, in the Poi example, we also moved the catalog metadata and various other things to use GenericSetup profiles, and could get rid of most of 'Install.py' in the process.

Portlets have a new infrastructure
==================================

In Plone 3.0, portlets are no longer simple page templates, but objects with behaviour, logic and possibilities for advanced behaviour like per-portlet caching.

Portlets have been re-implemented using the Zope 3 component architecture.
Change custom portlets to use plone.app.portlets if possible.
Check the Portlets Developer Manual to learn about the new portlets architecture.

Old portlets are supported via a fallback mechanism called Classic Portlet; the portlet management screen has functionality for doing inline migration for old portlets.
Note that using the old portlets mechanism will affect your site performance negatively, since they will load up the old global_defines.

How to add a Classic Portlet
----------------------------

You will see in the Add portlet pull-down menu on the Manage portlets page an item called Classic Portlet. This item allows you to use portlets created for earlier versions of Plone.

For instance, suppose you have a Classic Portlet that you have created in *your-site-instance/portal_skins/custom* in the Zope Management Interface (ZMI) that displays "Hello world", using a Page Template named portlet1 with the following code::

    <html>
      <body>
        <div metal:define-macro="portlet">
          <p>hello world</p>
        </div>
      </body>
    </html>

Here's how you can include this portlet in your site:

#. Login as an user with the Manage Portlets permission.
#. Click the manage portlets link.
#. Select Classic Portlet from the pull-down menu.
#. Type the template id in the Add Classic Portlet form. In the example, portlet1.
#. Leave the macro as portlet.

   .. image:: images/image_preview.png

#. Click save.

This is all you have to do to add the Classic Portlet to your folder, page, or content type.

main_template now uses Zope 3 viewlets
======================================

Plone 3 has switched to use Zope 3 viewlet components instead of the old macro include approach.
Any customizations of main_template.pt or header.pt will need to be updated to use the new approach.

If have previously shipped customized versions of templates like header.pt, viewThreadsAtBottom.pt or global_contentmenu.pt to get things into the page, please switch to viewlets instead, as it makes it much easier for multiple products to co-exist without stepping on each others changes.

Documentation and examples can be found in `this section <http://docs.plone.org/develop/plone/views/viewlets.html>`__.

Plone 3 does not create member folders by default
=================================================

With release 3.0, member folders are optional, and not created by default.
This means that you can't rely on member folders to store data in or in any other way assume that there will be a members folder present.

While this was always considered bad practice, it's now official. Don't do it. :)

Using a tableless layout
========================

The languishing tableless version of the Plone default theme has finally been removed from Plone 3.0.
However, a product exists which can be used as a substitute.

For people who want to use tableless, you can simply install the `Plone Tableless <https://plone.org/products/plone-tableless/>`_ product on top of your site.

If you are submitting a theme to plone.org for public consumption, please specify this as a dependency in your theme product's README.txt file.

Document Actions now use Zope 3 viewlets
========================================

If you were modifying or shipping custom templates for the document actions area of a Plone page, now's the time to stop.

The new approach uses viewlets, and its default position has also been moved to the bottom of the page. It also defaults to a text-based representation instead of the icons that it was using earlier, since document actions are often too abstract to create good icons for.

Products installing workflows may need to add permissions
=========================================================

If your product wants to make use of the new "Editor" role that ships with Plone 3, you will have to add explicit permissions to any workflows you add.

The new "Editor" (aka. "Can Edit" on the Sharing page) in Plone 3.0 makes it easy to let people collaborate on content authoring.
In some cases, editing also means the ability to add new objects inside the object people are editing.

For this to work, third party content types that add custom workflows will have to either use one of the standard "add content" permissions or explicitly give Editor the Add portal content role.

See `Ticket #6265 <http://dev.plone.org/plone/ticket/6265>`__ for the full explanation.

Indexes declared in Archetypes schemata need to be moved to GenericSetup
========================================================================

If you have declared indexes or metadata directly on the Archetypes field declarations, and you are using GenericSetup to install your types/FTIs, you will need to move them to GenericSetup.

This applies if you have moved from using 'install_types()' in
'Extensions/Install.py', to installing new content types/FTIs with
GenericSetup using a 'types.xml' import step.  Take this example from
`PoiIssue.py r40594 <https://github.com/collective/Products.Poi/blob/4fbca095c64185dda0f7d58a1982c82b89f4012c/Products/Poi/content/PoiIssue.py#L77>`__::

    StringField(
        name='release',
        default="(UNASSIGNED)",
        index="FieldIndex:schema",
        widget=SelectionWidget(
            label="Version",
            description="Select the version the issue was found in.",
            condition="object/isUsingReleases",
            label_msgid='Poi_label_release',
            description_msgid='Poi_help_release',
            i18n_domain='Poi',
        ),
        required=True,
        vocabulary='getReleasesVocab'
    ),

You need to move the creation to catalog.xml with GenericSetup. If there is ``index="FieldIndex"``, that means you need a new index, of type FieldIndex, with the name being the name of the accessor method::

    <index name="getRelease" meta_type="FieldIndex">
      <indexed_attr value="getRelease"/>
    </index>

If there is also ``:schema`` or ``:metadata``, e.g. ``index="FieldIndex:schema"``, you also need a metadata column::

    <column value="getRelease"/>

This is necessary because the schema does not really exist at install time, so there is no way GenericSetup can inspect it and configure new indexes. This was a bad design from the start, as portal-wide indexes do not belong in type-specific schemata anyway.

The "Sharing" tab is now a global action
========================================

You should no longer have a 'sharing' action in the portal_types entry for a custom content type.

The "Sharing" tab now points to the '@@sharing' view, and is defined as a global action in the 'object' category.
If you have a custom content type and you have set up the 'local_roles' action, which would normally be pointing to the 'folder_localrole_from' template, you should remove it.
It will be removed from existing, installed types during migration.

If you do not remove the action, the user will see two "Sharing" tabs.

For an example of the canonical set of actions and aliases, see `the GenericSetup definition of the Document FTI <https://github.com/plone/Products.CMFPlone/blob/3.0/profiles/default/types/Document.xml>`__.
Of course, you may not need the 'References', 'History' or 'External Edit' actions in your own types.

Multi page schemas
==================

By default, Archetypes fields in different schemas in Plone 3.0 will be loaded all at once, without page reloads between the 'schematas'.

In Plone 3.0, all fields from all schematas will be loaded at once.
If you depend on your schematas (fieldsets) to be processed one page after the other, you'll need to mark your Archetypes content type that uses it (not the schema itself) with the IMultiPageSchema interface.

The interface lives in Products.Archetypes.interfaces.IMultiPageSchema.
The code to mark your content type would look like this::

    from zope import interface
    from Products.Archetypes.interfaces import IMultiPageSchema
    # ...
    interface.classImplements(MyContentType, IMultiPageSchema)


Enable inline editing (aka. QuickEdit)
======================================

Once you have your product updated, you might want to add support for inline editing of your type. Fortunately, this is very easy.

Adding inline editing and validation support to your view templates is as easy as calling the Archetypes widgets in view mode. As an example, consider the following typical code from Plone 2.5::

    Variable goes here

Now, to render the same thing, with an h1 tag and a class on it, you do::

    Variable goes here

This will keep whatever tags and styling you want around the item, and render the inline editing inside of it.
It's also backwards compatible with earlier Plone versions — although these don't get the inline editing, obviously.
