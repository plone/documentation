======================
History and versioning
======================


Introduction
------------

Plone versioning allows you to go back between older edits of the same content object.

`Versioning allows you to restore and diff previous copies of the same content <https://docs.plone.org/working-with-content/managing-content/versioning.html>`_.
More about `CMFEditions here <https://github.com/plone/Products.CMFEditions/tree/master/doc>`_.

See also

* `Versioning tutorial for Dexterity content types <https://pypi.org/project/plone.app.versioningbehavior/>`_
* `Old Versioning tutorial for Archetype custom content types <https://web.archive.org/web/20170909085840/http://www.uwosh.edu/ploneprojects/docs/how-tos/how-to-enable-versioning-history-tab-for-a-custom-content-type/>`_.


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

* https://github.com/plone/Products.CMFEditions/blob/master/doc/DevelDoc.txt

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


