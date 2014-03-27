Permission
==========

The permission attribute can be used to restrict visibility of a
component.

When a user logs in to a site, they will be given a role ('manager' or
'editor' for instance). This role is, effectively, a set of permissions,
giving them particular rights over particular aspects of the site.

To find out more about permissions consult the Understanding Permissions
and Security Tutorial:

-  `http://plone.org/documentation/tutorial/understanding-permissions/ <http://plone.org/documentation/tutorial/understanding-permissions/>`_

In the case of components, the permission attribute allows the site to
decide whether a user has a right to see, or interact with a component.
Most viewlets have the permission Zope2.View or Zope2.Public, which are
permissions assigned to everyone, even anonymous visitors. However, look
at the Lock Info viewlet:

::

    <browser:viewlet
            name="plone.lockinfo"
            manager=".interfaces.IAboveContent"
            class="plone.locking.browser.info.LockInfoViewlet"
            permission="cmf.ModifyPortalContent"
            for="plone.locking.interfaces.ITTWLockable"
            />

By using cmf.ModifyPortalContent, this viewlet is restricted only to
those who have the right to edit content (those who don't wouldn't be
interested in whether an item was locked or not).

The list of available permissions is buried rather deeply in the Five
product which comes with your installation of Zope - look in
permissions.zcml for the most up-to-date list.

 

zope2.Public

Public, everyone can access

zope2.Private

Private, only accessible from trusted code

zope2.AccessContentsInformation

Access contents information

zope2.ChangeImagesFiles

Change Images and Files

zope2.ChangeConfig

Change configuration

zope2.ChangePermissions

Change permissions

zope2.CopyOrMove

Copy or Move

zope2.DefinePermissions

Define permissions

zope2.DeleteObjects

Delete objects

zope2.FTPAccess

FTP access

zope2.ImportExport

Import/Export objects

zope2.ManageProperties

Manage properties

zope2.ManageUsers

Manage users

zope2.Undo

Undo changes

zope2.View

View

zope2.ViewHistory

View History

zope2.ViewManagementScreens

View management screens

zope2.WebDAVLock

WebDAV Lock items

zope2.WebDAVUnlock

WebDAV Unlock items

zope2.WebDAVAccess

WebDAV access

cmf.ListFolderContents

List folder contents

cmf.ListUndoableChanges

List undoable changes

cmf.AccessInactivePortalContent

Access inactive portal content

cmf.ManagePortal

Manage portal

cmf.ModifyPortalContent

Modify portal content

cmf.ManageProperties

Manage properties

cmf.ListPortalMembers

List portal members

cmf.AddPortalFolders

Add portal folders

cmf.AddPortalContent

Add portal content

cmf.AddPortalMember

Add portal member

cmf.SetOwnPassword

Set own password

cmf.SetOwnProperties

Set own properties

cmf.MailForgottonPassword

Mail forgotten password

cmf.RequestReview

Request review

cmf.ReviewPortalContent

Review portal content

cmf.AccessFuturePortalContent

Access future portal content

 
