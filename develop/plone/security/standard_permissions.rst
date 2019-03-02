==============================
Standard permissions and roles
==============================

.. admonition:: Description

    Technical overview of Plones standard permissions and roles.


Standard permissions
====================

The standard permissions can be found in ``AccessControl``s and ``Product.CMFCore``\’s ``permissions.zcml``.
Here, you will find a short ``id`` (also known as the *Zope 3 permission id*) and a longer ``title`` (also known as the *Zope 2 permission title*).
For historical reasons, some areas in Plone use the id, whilst others use the title.
As a rule of thumb:

- Browser views defined in ZCML directive use the Zope 3 permission id;
- Security checks using ``zope.security.checkPermission()`` use the Zope 3 permission id;
- Dexterity’s ``add_permission`` FTI variable uses the Zope 3 permission id;
- The ``rolemap.xml`` GenericSetup handler and workflows use the Zope 2 permission title;
- Security checks using ``AccessControl``’s ``getSecurityManager().checkPermission()``,
  including the methods on the ``portal_membership`` tool,
  use the Zope 2 permission title.

The most commonly used permission are shown below.
The Zope 2 permission title is shown in parentheses.

``zope2.View`` (:guilabel:`View`)
    used to control access to the standard view of a content item;

``zope2.DeleteObjects`` (:guilabel:`Delete objects`)
    used to control the ability to delete child objects in a container;

``cmf.ModifyPortalContent`` (:guilabel:`Modify portal content`)
    used to control write access to content items;

``cmf.ManagePortal`` (:guilabel:`Manage portal`)
    used to control access to management screens;

``cmf.AddPortalContent`` (:guilabel:`Add portal content`)
    the standard add permission required to add content to a folder;

``cmf.SetOwnProperties`` (:guilabel:`Set own properties`)
    used to allow users to set their own member properties'

``cmf.RequestReview`` (:guilabel:`Request review`)
    typically used as a workflow transition guard to allow users to submit content for review;

``cmf.ReviewPortalContent`` (:guilabel:`Review portal content`)
    usually granted to the ``Reviewer`` role,
    controlling the ability to publish or reject content.

Standard roles
==============

As with permissions, it is easy to create custom roles
(use the ``rolemap.xml`` GenericSetup import step – see ``CMFPlone``\’s version of this file for an example), although you should use the standard roles where possible.

The standard roles in Plone are:

:guilabel:`Anonymous`
    a pseudo-role that represents non-logged in users.

.. note::

    if a permission is granted to :guilabel:`Anonymous`,
    it is effectively granted to everyone.
    It is not possible to grant permissions to non-logged in users without also granting them to logged in ones.

:guilabel:`Authenticated`
     a pseudo-role that represents logged-in users.

:guilabel:`Owner`
     automatically granted to the creator of an object.

:guilabel:`Manager`
     which represents super-users/administrators.
     Almost all permissions that are not granted to ``Anonymous``
     are granted to ``Manager``.

:guilabel:`Site Manager`
     which represents site/administrators.
     Has permissions needed to fully manage a single Plone site.

:guilabel:`Reviewer`
     which represents content reviewers separately from site administrators.
     It is possible to grant the :guilabel:`Reviewer` role locally on the :guilabel:`Sharing` tab,
     where it is shown as :guilabel:`Can review`.

:guilabel:`Member`
     representing “standard” Plone users.

In addition, there are three roles that are intended to be used as *local roles* only.
These are granted to specific users or groups via the :guilabel:`Sharing` tab,
where they appear under more user friendly pseudonyms.

:guilabel:`Reader`, aka :guilabel:`Can view`,
    confers the right to view content.
    As a rule of thumb,
    the :guilabel:`Reader` role should have the :guilabel:`View` and :guilabel:`Access contents information` permissions if the :guilabel:`Owner` roles does.

:guilabel:`Editor`, aka :guilabel:`Can edit`,
    confers the right to edit content.
    As a rule of thumb,
    the :guilabel:`Editor` role should have the :guilabel:`Modify portal content` permission if the :guilabel:`Owner` roles does.

:guilabel:`Contributor`, aka :guilabel:`Can add`,
    confers the right to add new content.
    As a rule of thumb,
    the :guilabel:`Contributor` role should have the :guilabel:`Add portal content` permission
    and any type-specific add permissions globally
    (i.e. granted in ``rolemap.xml``),
    although these permissions are sometimes managed in workflow as well.
