======================
History and versioning
======================

.. contents :: :local:

Introduction
------------

Plone versioning allows you to go back between older edits of the same content object.

`Versioning allows you to restore and diff previous copies of the same content <http://plone.org/documentation/manual/plone-3-user-manual/managing-content/versioning-plone-v3.0-plone-v3.2>`_.
More about `CMFEditions here <http://plone.org/products/cmfeditions/documentation/refmanual/cmfeditionoverview>`_.

See also

* `Versioning tutorial for custom content types <http://www.uwosh.edu/ploneprojects/docs/how-tos/how-to-enable-versioning-history-tab-for-a-custom-content-type/>`_.

Enabling versioning on your custom content type (Plone 3 ONLY)
----------------------------------------------------------------

.. note ::

         This information applies for Plone 3 only.

By default, version history is not enabled for custom content types.
Below are some notes how to enable it.

* Inherit HistoryAwareMixin in your content type class::

    from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

    ..

    class CustomContent(base.ATCTContent, HistoryAwareMixin):

* Add versioning migration code to your setuphandlers.py / custom import steps::


    from Products.CMFCore.utils import getToolByName
    from Products.CMFEditions.setuphandlers import VERSIONING_ACTIONS, ADD_POLICIES, DEFAULT_POLICIES

    class DPSetup(object):

        def configureVersioning(self,portal):
           """
           Importing various settings
           Big thanks to amir toole from plone-users
           """

           for versioning_actions in ('MyositisPatient','MyositisVisit','MyositisOrdination','MyositisSeriousadverseevent','MyositisAdhoc','MyositisAdhoc1','MyositisAdhoc2','MyositisAdhoc3','MyositisAdhoc4'):
            VERSIONING_ACTIONS[versioning_actions] = 'version_document_view'
            portal_repository = getToolByName(portal, 'portal_repository')
            portal_repository.setAutoApplyMode(True)
            portal_repository.setVersionableContentTypes(VERSIONING_ACTIONS.keys())
            portal_repository._migrateVersionPolicies()
            portal_repository.manage_changePolicyDefs(ADD_POLICIES)
            for ctype in VERSIONING_ACTIONS:
             for policy_id in DEFAULT_POLICIES:
                 portal_repository.addPolicyForContentType(ctype, policy_id)

      ...

      def importFinalSteps(context):
        """
        The last bit of code that runs as part of this setup profile.
        """
        site = context.getSite()
        configurator = DPSetup()
        configurator.configureVersioning(site)

* To see which fields differ between versions, diff tool must be configured to support your custom content types.
  GenericSetup support is available after Plone 3.2. For older you must manually create entries in portal_diff_tool.
  Example GenericSetup difftool.xml::

    <?xml version="1.0"?>

    <object>

      <difftypes>
          <type portal_type="Presentation">
            <!-- Field any will match all field names, otherwise you need to specify the field name in schema -->
            <field name="any" difftype="Compound Diff for AT types"/>
          </type>
      </difftypes>
    </object>



* If you have customized the edit process of your content type,
  make sure that your edit action traverses to update_version_before_edit.cpt. For hints how to do this,
  see portal_form_controller actions tab. Example::


    ## Script (Python) "diagnose_content_edit"
    ##title=Custom editing script for diagnose content type
    ##bind container=container
    ##bind context=context
    ##bind namespace=
    ##bind script=script
    ##bind state=state
    ##bind subpath=traverse_subpath
    ##parameters=id=''
    ##

    context.plone_log("Diagnose edit by doctor")

    #
    # TODO:
    # No freaking idea which of the update_version handlers is supposed to be run and when
    #

    # Run versioning support code
    # context.update_version_before_edit()

    state = context.content_edit_impl(state, id)

    # Run versioning support code
    context.update_version_on_edit()

    context.plone_log("Done")


    # Automatically trigger the workflow state change on edit
    context.portal_workflow.doActionFor(context, "push_to_review")

    return state


* If you are using custom roles you need to have at least CMFEditions: Save new version
  permission enabled for the roles or you'll get exception::

    ...

    * Module Products.PythonScripts.PythonScript, line 327, in _exec
    * Module None, line 36, in update_version_before_edit
      <ControllerPythonScript at /xxx/update_version_before_edit used for /xxx/yyy>
      Line 36
    * Module Products.CMFEditions.CopyModifyMergeRepositoryTool, line 287, in save
    * Module Products.CMFEditions.CopyModifyMergeRepositoryTool, line 408, in _assertAuthorized

    Unauthorized: You are not allowed to access 'save' in this context

* If your content type contains blob fields you want to version, you will need to edit
  portal_modifier/CloneBlobs entry and add your portal type to the condition field.

For more information

* http://plone.org/documentation/manual/developer-manual/archetypes/appendix-practicals/enabling-versioning-on-your-custom-content-types

Checking whether versioning is enabled
--------------------------------------

The following check is performed by update_versioning_before_edit and update_versioning_on_edit scripts::

    pr = context.portal_repository

    isVersionable = pr.isVersionable(context)

    if pr.supportsPolicy(context, 'at_edit_autoversion') and isVersionable:
        # Versioning should work
        pass
    else:
        # Something is wrong....
        pass

Inspecting versioning policies
------------------------------

Example::

    portal_repository = context.portal_repository
    map = portal_repository.getPolicyMap()
    for i in map.items(): print i

Will output (inc. some custom content types)::

    ('File Disease Description', ['at_edit_autoversion', 'version_on_revert'])
    ('Document', ['at_edit_autoversion', 'version_on_revert'])
    ('Free Text Disease Description', ['at_edit_autoversion', 'version_on_revert'])
    ('ATDocument', ['at_edit_autoversion', 'version_on_revert'])
    ('Diagnose Description', ['at_edit_autoversion', 'version_on_revert'])
    ('ATNewsItem', ['at_edit_autoversion', 'version_on_revert'])
    ('Link', ['at_edit_autoversion', 'version_on_revert'])
    ('News Item', ['at_edit_autoversion', 'version_on_revert'])
    ('Event', ['at_edit_autoversion', 'version_on_revert'])

How versioning (CMFEditions) works
----------------------------------

* http://svn.zope.de/plone.org/collective/Products.CMFEditions/trunk/doc/DevelDoc.html

.. note::

        You might actually want to check out the package to get your web browser to
        properly read the file.

Getting the complete revision history for an object
---------------------------------------------------

You may find yourself needing to (programmatically) get some/all of a content
object's revision history. The content history view can be utilised to do this;
this view is the same one that is visible through Plone's web interface at
``@@contenthistory`` (or indirectly on ``@@historyview``).  This code works
with Plone 4.1 and has been utilised for exporting raw content modification
information:

.. code-block:: python

    from plone.app.layout.viewlets.content import ContentHistoryView
    context = portal['front-page']
    print ContentHistoryView(context, context.REQUEST).fullHistory()

If you want to run this from somewhere without a ``REQUEST`` available, such
as the *Plone/Zope debug console*, then you'll need to fake a request and access
level accordingly. Note the subtle change to using ``ContentHistoryViewlet``
rather than ``ContentHistoryView`` - we need to avoid initialising an entire
view because this involves component lookups (and thus, pain).  We also need to
fake our security as well to avoid anything being left out from the history.

.. code-block:: python

    from plone.app.layout.viewlets.content import ContentHistoryViewlet
    from zope.publisher.browser import TestRequest
    from AccessControl.SecurityManagement import newSecurityManager

    admin = app.acl_users.getUser('webmaster')
    request = TestRequest()
    newSecurityManager(request,admin)

    portal = app.ands
    context = portal['front-page']
    chv = ContentHistoryViewlet(context, request, None, None)
    #These attributes are needed, the fullHistory() call fails otherwise
    chv.navigation_root_url = chv.site_url = 'http://www.foo.com'
    print chv.fullHistory()

The end result should look something like this, which has plenty of tasty
morsels to pull apart and use::

    [{'action': u'Edited',
      'actor': {'description': '',
                'fullname': 'admin',
                'has_email': False,
                'home_page': '',
                'language': '',
                'location': '',
                'username': 'admin'},
      'actor_home': 'http://www.foo.com/author/admin',
      'actorid': 'admin',
      'comments': u'Initial revision',
      'diff_current_url': 'http://foo/Plone5/front-page/@@history?one=current&two=0',
      'preview_url': 'http://foo/Plone5/front-page/versions_history_form?version_id=0#version_preview',
      'revert_url': 'http://foo/Plone5/front-page/revertversion',
      'time': 1321397285.980262,
      'transition_title': u'Edited',
      'type': 'versioning',
      'version_id': 0},
     {'action': 'publish',
      'actor': {'description': '',
                'fullname': '',
                'has_email': False,
                'home_page': '',
                'language': '',
                'location': '',
                'username': 'admin'},
      'actor_home': 'http://www.foo.com/author/admin',
      'actorid': 'admin',
      'comments': '',
      'review_state': 'published',
      'state_title': 'Published',
      'time': DateTime('2011/11/15 09:49:8.023381 GMT+10'),
      'transition_title': 'Publish',
      'type': 'workflow'},
     {'action': None,
      'actor': {'description': '',
                'fullname': '',
                'has_email': False,
                'home_page': '',
                'language': '',
                'location': '',
                'username': 'admin'},
      'actor_home': 'http://www.foo.com/author/admin',
      'actorid': 'admin',
      'comments': '',
      'review_state': 'private',
      'state_title': 'Private',
      'time': DateTime('2011/11/15 09:49:8.005597 GMT+10'),
      'transition_title': u'Create',
      'type': 'workflow'}]

For instance, you can determine who the last person to modify this Plone
content was by looking at the first list element (and get all their details
from the actor information). Refer to the source of
``plone.app.layout.viewlets.content`` for more information about
``ContentHistoryView``, ``ContentHistoryViewlet`` and
``WorkflowHistoryViewlet``.  Using these other class definitions, you can see
that you can get just the workflow history using ``.workflowHistory()`` or just
the revision history using ``.revisionHistory()``.

Purging history
--------------------

* http://stackoverflow.com/questions/9683466/purging-all-old-cmfeditions-versions


