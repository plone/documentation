=================
 Creating objects
=================

.. admonition:: Description

    Creating and controlling creation of Plone content items programmatically.


Creating Content Objects
========================

Permission-aware way (Dexterity)
-----------------------------------

These instructions apply for :doc:`Dexterity </develop/plone/content/dexterity>` content
types.

Example::

    from plone.dexterity.utils import createContentInContainer

    # Factory-type information id is the same as in types.xml
    # optionally you can set checkConstraints=False to skip permission checks
    item = createContentInContainer(folder, "your.app.dexterity.fti.information", title=title)


Permission-aware way (Archetypes and Dexterity)
-----------------------------------------------

``invokeFactory()`` is available on all folderish content objects.

``invokeFactory()`` calls the ``portal_factory`` persistent utility to create content item.

Example::

    def createResearcherById(folder, id):
        """ Create one researcher in a folder based on its X id.

        @param id: X id of the researcher

        @returns: Newly created researcher
        """

        # Call X REST service to get JSON blob for this researcher
        # Note: queryById parses JSON back to Python to do some sanity checks for it
        index = XPeopleIndex()
        oraData = index.queryById(id)

        # Need to have temporary id
        id = str(random.randint(0, 99999999))

        folder.invokeFactory("XResearcher", id)
        content = folder[id]

        # XResearcher stores its internal data as JSON
        json_data = json.dumps(oraData)
        content.setXData(json_data)

        # Will finish Archetypes content item creation process,
        # rename-after-creation and such
        content.processForm()

        return content


Example (from unit tests)::

    self.loginAsPortalOwner()
    self.portal.invokeFactory("Folder", "folder")
    self.portal.folder.invokeFactory("Folder", "subfolder")
    self.portal.folder.subfolder.invokeFactory("Document", "doc")

``invokeFactory()`` will raise an ``Unauthorized`` exception if the
logged-in user does not have permission to create content in the folder
(lacks type specific creation permission and ``Add portal content``
permissions).  This exception can be imported as follows::

	from Products.Archetypes.exceptions import AccessControl_Unauthorized

.. note::

    If the content class has  ``_at_rename_after_creation = True``
    (Archetypes-based content) the next call to ``obj.update()`` (edit form
    post) will automatically generate a friendly id for the object based on
    the title of the object.


Bypassing permissions when creating content item
------------------------------------------------

If you need to have special workflows where you bypass the workflow and
logged in users when creating the content item, do as follows::

	def construct_without_permission_check(folder, type_name, id, *args, **kwargs):
	    """ Construct a new content item bypassing creation and content add permissions checks.

	    @param folder: Folderish content item where to place the new content item
	    @param type_name: Content type id in portal_types
	    @param id: Traversing id for the new content
	    @param args: Optional arguments for the construction (will be passed to the creation method if the type has one)
	    @param kwargs: Optional arguments for the construction (will be passed to the creation method if the type has one)
	    @return: Reference to newly created content item
	    """

	    portal_types = getToolByName(folder, "portal_types")

	    # Get this content type definition from content types registry
	    type_info = portal_types.getTypeInfo(type_name)

	    # _constructInstance takes optional *args, **kw parameters too
	    new_content_item = type_info._constructInstance(folder, id)

	    # Return reference to justly created content
	    return new_content_item

.. note::

    The function above only bypasses the content item construction permission check.

    It does not bypass checks for setting field values for initially created content.

There is also an alternative way::

    # Note that by default Add portal member permissions
    # is only for the owner, so we need to by bass it here
    from Products.CMFPlone.utils import _createObjectByType
    _createObjectByType("YourContentType", folder, id)


Manual friendly id generation
==============================

If you are creating Plone objects by hand e.g. in a batch
job and Plone automatic id generation does not kick in,
you can use the following example to see how to create friendly
object ids manually::

    from zope.component import getUtility
    from plone.i18n.normalizer.interfaces import IIDNormalizer

    import transaction

    def createResearcherById(folder, id):
        """ Create one researcher in a folder based on its ORA id.

        @param id: X id of the researcher

        @returns: Newly created researcher
        """

        # Call X REST service to get JSON blob for this researcher
        # Note: queryById parses JSON back to Python to do some sanity checks for it
        index = XPeopleIndex()

        # Need to have temporary id
        id = str(random.randint(0, 99999999))

        folder.invokeFactory("XResearcher", id)
        content = folder[id]

        # XXX: set up content item data

        # Will finish Archetypes content item creation process,
        # rename-after-creation and such
        content.processForm()

        # make _p_jar on content
        transaction.savepoint(optimistic=True)

        # Need to perform manual normalization for id,
        # as we don't have title available during the creation time
        normalizer = getUtility(IIDNormalizer)
        new_id = normalizer.normalize(content.Title())

        if new_id in folder.objectIds():
            raise RuntimeError("Item already exists:" + new_id + " in " + folder.absolute_url())

        content.aq_parent.manage_renameObject(id, new_id)

        return content


PortalFactory
-------------

``PortalFactory`` (only for Archetypes) creates the object in a temporary
folder and only moves it to the real folder when it is first saved.

.. note::

    To see if content is still temporary, use ``portal_factory.isTemporary(obj)``.

Restricting Creating On Content Types
=====================================

Plone can restrict which content types are available for creation in a
folder via the :guilabel:`Add` menu.

Restricting available types per content type
--------------------------------------------

``portal_types`` defines which content types can be created inside a folderish content type.

By default, all content types which have the ``global_allow`` property set can be added.

The behavior can be controlled with ``allowed_content_types`` setting.

* You can change it through the ``portal_types`` management interface.

* You can change it in your add-on installer :doc:`GenericSetup
  </develop/addons/components/genericsetup>` profile.

Example for :doc:`Dexterity content type </develop/plone/content/dexterity>`. The file
would be something like
``profiles/default/types/yourcompany.app.typeid.xml``::

    <!-- List content types we allow here -->
    <property name="filter_content_types">True</property>
    <property name="allowed_content_types">
          <element value="yourcompany.app.courseinfo" />
    </property>
    <property name="allow_discussion">False</property>


Example for :doc:`Archetypes content </develop/plone/content/archetypes/index>`. The file
would be something like ``profiles/default/types/YourType.xml``::

    <property name="filter_content_types">True</property>

    <property name="allowed_content_types">
            <element value="YourContentTypeName" />
            <element value="Image" />
            <element value="News Item" />
            ...
    </property>

Restricting available types per folder instance
-----------------------------------------------

In the UI, you can access this feature via the :guilabel:`Add` menu :guilabel:`Restrict` option.

Type contraining is managed by the ``ATContentTypes`` product:

* https://github.com/plone/Products.ATContentTypes/blob/master/Products/ATContentTypes/lib/constraintypes.py


Example::

    # Set allowed content types
    from Products.ATContentTypes.lib import constraintypes

    # Enable contstraining
    folder.setConstrainTypesMode(constraintypes.ENABLED)

    # Types for which we perform Unauthorized check
    folder.setLocallyAllowedTypes(["ExperienceEducator"])

    # Add new... menu  listing
    folder.setImmediatelyAddableTypes(["ExperienceEducator"])

You can also override the ``contraintypes`` accessor method to have
programmable logic regarding which types are addable and which not.



Other restrictions
------------------

See this discussion thread:

* http://plone.293351.n2.nabble.com/Folder-constraints-not-applicable-to-custom-content-types-tp6073100p6074327.html

Creating OFS objects
====================

Zope has facilities for basic folder and contained objects using the
`IObjectManager definition <http://svn.zope.org/Zope/trunk/src/OFS/interfaces.py?rev=96262&view=auto>`_
subsystem. You do not need to work with raw objects unless you are doing
your custom lightweight, Plone-free, persistent data.


Object construction life cycle
==============================

.. note::

    The following applies to Archetypes-based objects only. The process
    might be different for Dexterity-based content.

Archetypes content construction has two phases:

#. The object is created using a ``?createType=`` URL or a
   ``Folder.invokeFactory()``
   call.  If ``createType`` is used then the object is given a temporary id.
   The object has an "in creation" flag set.

#. The object is saved for the first time and the final id is generated
   based on the object title. The object is renamed. The creation flag is
   cleared.

You are supposed to call either ``object.unmarkCreationFlag()`` or
``object.processForm()`` after content is created manually using
``invokeFactory()``.

``processForm()`` will perform the following tasks:

- unmarks creation flag;
- renames object according to title;
- reindexes object;
- invokes the ``after_creation`` script and fires the ``ObjectInitialized``
  event.

If you don't want some particular step to be executed, study
``Archetypes/BaseObject.py`` and call only what you really want.  But unless
``unmarkCreationFlag()`` is called, the object will behave strangely after
the first edit.

Rename after creation
---------------------

To prevent the automatic rename on the first through-the-web save, add the
following attribute to your class::

    _at_rename_after_creation = False



Factory type information
========================

Factory type information (FTI) is responsible for content creation in the
portal.  It is independent from content type (Archetypes, Dexterity)
subsystems.

.. warning::

    The FTI codebase is old (updated circa 2001). Useful documentation
    might be hard to find.

FTI is responsible for:

* Which function is called when new content type is added;
* icons available for content types;
* creation views for content types;
* permission and security;
* whether discussion is enabled;
* providing the ``factory_type_information`` dictionary. This is used
  elsewhere in the code (often in ``__init__.py`` of a product) to set the
  initial values for a *ZODB Factory Type Information* object (an object in
  the ``portal_types`` tool).

See:

* `FTI source code <http://svn.zope.org/Products.CMFCore/trunk/Products/CMFCore/TypesTool.py?rev=101748&view=auto>`_.

* `Scriptable Types Information HOW TO <http://www.zope.org/Products/CMF/docs/devel/using_scriptable_type_info/view>`_

* `Notes Zope types mechanism <http://www.zope.org/Products/CMF/docs/devel/taming_types_tool/view>`_

Content does not show in :guilabel:`Add` menu, or ``Unauthorized`` errors
=========================================================================

These instructions are for Archetypes content to debug issues
when creating custom content types which somehow fail to become creatable.

When creating new content types, many things can silently fail due to human
errors in the complex content type setup chain and security limitations.
The consequence is that you don't see your content type in the :guilabel:`Add`
drop-down menu.  Here are some tips for debugging.

* Is your product broken due to Python import time errors?
  Check the Management Interface: :guilabel:`Control panel` -> :guilabel:`Products`.
  Turn on Zope debugging mode to trace import errors.

* Have you rerun the quick installer (``GenericSetup``) after
  creating/modifying the content type?

* Do you have a correct :guilabel:`Add` permission for the product? Check
  ``__init__.py`` ``ContentInit()`` call.

* Does it show up in the portal factory?
  Check the Management Interface: :guilabel:`portal_factory` and ``factorytool.xml``.

* Is it corretly registered as a portal type and implictly addable?
  Check the Management Interface: :guilabel:`portal_types`.
  Check ``default/profiles/type/yourtype.xml``.

* Does it have correct product name defined?
  Check the Management Interface: :guilabel:`portal_types`.

* Does it have a proper factory method?
  Check Management Interface: :guilabel:`portal_types`.
  Check Zope logs for ``_queryFactory`` and import errors.

* Does it register itself with Archetypes?
  Check the Management Interface: :guilabel:`archetypes_tool`.
  Make sure that you have ``ContentInit`` properly run in your
  ``__init__.py``. Make sure that all modules having Archetypes content
  types defined and ``registerType()`` call are imported in ``__init__py``.

Link to creation page
=====================

* The :guilabel:`Add` menu contains links for creating individual content types.
  Copy the URLs that you see there.

* If you want to the user to have a choice about which content type to
  create, you can link to ``/folder_factories`` page. (This is also the
  creation page when JavaScript is disabled).

Populating folder on creation
=============================

Archetypes have a hook called ``initializeArchetype()``. Your content type
subclass can override this.

Example::

    class LandingPage(folder.ATFolder):
        """Landing page"""

        def initializeArchetype(self, **kwargs):
            """
            Prepopulate folder during the creation.

            Create five subfolders of "BigBlock" type, with title and id preset.
            """
            folder.ATFolder.initializeArchetype(self, **kwargs)

            for i in range(0, 5):
                id = "container" + str(i)
                self.invokeFactory("BigBlock", id, title="Big block " + str(i+1))
                item = self[id]

                # Clear creation flag
                item.markCreationFlag()


Creating content from PloneFormGen
=========================================

PloneFormGen is a popular add-on for Plone.

Below is a snippet for a ``Custom Script Adapter`` which allows to create
content straight out of PloneFormGen in the *pending* review state (it is
not public and will appear in the review list)::

    # Folder id where we create content is "directory" under site root
    target = context.portal_url.getPortalObject()["directory"]

    # The request object has an dictionary attribute named
    # form that contains the submitted form content, keyed
    # by field name
    form = request.form

    # We need to engineer a unique ID for the object we're
    # going to create. If your form submit contained a field
    # that was guaranteed unique, you could use that instead.
    from DateTime import DateTime
    uid = str(DateTime().millis())

    # We use the "invokeFactory" method of the target folder
    # to create a content object of type "Document" with our
    # unique ID for an id and the form submission's topic
    # field for a title.

    # Field id have been set in Form Folder Contents view,
    # using rename functionality
    target.invokeFactory("Document", id=uid,
                         title=form['site-name'],
                         description=form['site-description'],
                         remoteUrl=form["link"]
                         )

    # Find our new object in the target folder
    obj = target[uid]

    # Trigger rename-after-creation behavior
    # where actual id is generated from the title
    obj.processForm()

    # Make item to pending state
    portal_workflow = context.portal_workflow
    portal_workflow.doActionFor(obj, "submit")

More info:

* https://plone.org/products/ploneformgen/documentation/how-to/creating-content-from-pfg

* https://plone.org/products/ploneformgen/documentation/how-to/creating-content-from-pfg

Creating content using Generic Setup
====================================

Purpose
-------

You want your product to create default content in the site.  (For example,
because you have a product which adds a new content type, and you want to
create a special folder to put these items in.)

You could do this programmatically, but if you don't want anything fancy (see
"Limitations" below), Generic Setup can also take care of it.

Step by step
------------

* In your product's ``profiles/default`` folder, create a directory called ``structure``.

* To create a top-level folder with id ``my-folder-gs-created``, add a directory of that name to the structure folder.

* Create a file called .objects in the ``structure`` directory

* Create a file called .properties in the ``my-folder-gs-created`` directory

* Create a file called .preserve in the ``structure`` directory

* ``.objects`` registers the folder to be created::

    my-folder-gs-created,Folder

* ``.properties`` sets properties of the folder to be created::

    [DEFAULT]
    description = Folder for imported Projects
    title = My folder (created by generic setup)

* ``.preserve`` will make sure the folder isn't overwritten if it already exists::

    my-folder-gs-created

Limitations
-----------

* This will only work for Plone's own content types

* Items will be in their initial workflow state

If you want to create objects of a custom content type, or manipulate them
more, you'll have to write a setuphandler. See below under "Further
Information".

Troubleshooting
---------------

I don't see titles in the navigation, only ids
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You may notice that the new generated content's title appears to be set to its
id. In this case, the catalog needs to be updated. You can do this through the
Management Interface, in ``portal_catalog``.

You could automate this process by adding a GS import step in configure.zcml, which looks like this::

  <genericsetup:importStep
         name="my.policy_updateCatalog"
         title="Update catalog"
         description="After creating content (from profiles/default/structure), the catalog needs to be updated."
         handler="my.policy.setuphandlers.updateCatalog">
       <depends name="content"/>
     </genericsetup:importStep>

This is the preferred way to define dependencies for import profiles: The
import step declares its dependency on the content import step. 'content' is
the name for the step which creates content from ``profiles/default/structure``.
You could then add a method which updates the catalog in the product's
``setuphandlers.py``::

  def updateCatalog(context, clear=True):
      portal = context.getSite()
      logger = context.getLogger('my.policy updateCatalog')
      logger.info('Updating catalog (with clear=%s) so items in profiles/default/structure are indexed...' % clear )
      catalog = portal.portal_catalog
      err = catalog.refreshCatalog(clear=clear)
      if not err:
          logger.info('...done.')
      else:
          logger.warn('Could not update catalog.')

Further information
-------------------

* Original manual:
  http://vanrees.org/weblog/creating-content-with-genericsetup
* If you want to do things like workflow transitions or setting default views
  after creating, read
  http://keeshink.blogspot.de/2011/05/creating-plone-content-when-installing.html
