==============================
Available Permissions In Plone
==============================

.. admonition:: Description

   What Zope security permissions you have available for your Plone coding

Listing Different Available Permissions
=======================================

Each permission name is a string.

To see available permissions, click Security tab at your site root in the Management Interface.

In programming, use pseudo-constants instead of permission string values:

* See `CMFCore.permissions <https://github.com/zopefoundation/Products.CMFCore/blob/master/src/Products/CMFCore/permissions.py>`_

* See `AccessControl.Permissions <https://github.com/zopefoundation/AccessControl/blob/master/src/AccessControl/Permissions.py>`_

For available ZCML permission mappings see:

* `Products/Five/permissions.zcml <https://github.com/zopefoundation/Zope/blob/master/src/Products/Five/permissions.zcml>`_

	* Permissions such as ``cmf.ModifyPortalContent``, ``zope2.View``

* `zope/security/permissions.zcml <https://github.com/zopefoundation/zope.security/blob/master/src/zope/security/permissions.zcml>`_

	* ``zope.Public``

or search for the string ``<permission`` in ``*.zcml`` files in the *eggs*
folder of your Plone development deployment.

Example using UNIX grep tool:

.. code-block:: console

	grep -C 3 -Ri --include=*.zcml "<permission" *

Useful Permissions
==================

Permissions are shown by their verbose name in the Management Interface.

``View``
    This governs whether you are allowed to view some content.
``Access Contents Information``
    This permission allows access to an object, without necessarily viewing
    the object. For example, a user may want to see the object's title in a
    list of results, even though the user can't view the contents of that
    file.
``List folder contents``
    This governs whether you can get a listing of the contents of a folder;
    it doesn't check whether you have the right to view the objects listed.
``Modify Portal Content``
    This governs whether you are allowed to modify some content.
``Manage Portal``
    This permission allows you to manage the portal.
    A number of views in the plone control panel are protected with this view.
    If you plan to write a reusable product, be very hesitant to use this permission, check whether a custom permission might make more sense.

There is no single permission for adding content. Every content type has its own permission.
If you create your own content type, create a custom add permission for it.

.. table:: Permissions

    =========================== ===================================
    Permission name             Permission name for ZCML
    =========================== ===================================
    View                        zope2.View
    Access contents information zope2.AccessContentsInformation
    List folder contents        cmf.ListFolderContents
    Modify portal content       cmf.ModifyPortalContent
    Manage portal               cmf.ManagePortal
    =========================== ===================================

To reference a permission in code, you need the name as a string.
Using strings is a bad convention, all common permissions have a constant in Products.CMFCore.permissions.
To perform a permission check propery, you do something like this::

    from AccessControl import getSecurityManager
    from AccessControl import Unauthorized
    from Products.CMFCore import permissions

    if not getSecurityManager().checkPermission(permissions.ModifyPortalContent, object):
        raise Unauthorized("You may not modify this object")

All standard permissions from above can be referenced by their Permission name without spaces.

More info:

* http://markmail.org/thread/3izsoh2ligthfcou
