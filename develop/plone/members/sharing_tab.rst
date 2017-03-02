=======
Sharing
=======

TODO: remove this file, eventually move code example to a "cookbook" section.

.. warning:: Out of date

    This page is out of date. Please visit: :doc:`Local Roles </develop/plone/security/local_roles>`.


.. admonition:: Description

        Customizing the sharing feature of Plone


Introduction
-------------


* `Sharing tab source code <https://github.com/plone/plone.app.workflow/blob/master/plone/app/workflow/browser/sharing.py>`_

* `Default sharing tab role translations <https://github.com/plone/plone.app.workflow/blob/master/plone/app/workflow/configure.zcml>`_



* https://pypi.python.org/pypi/collective.sharingroles

* http://encolpe.wordpress.com/2010/02/08/add-a-new-role-in-the-sharing-tab-for-plone-3/

Setting sharing rights programmatically
----------------------------------------

Complex example: Create one folder per group and add sharing rights
===================================================================

The sample code

* Creates one folder per group, with some groups excluded. The folder is not created if it exists.

* Blocks role inheritance for the group

* Gives edit access to the group through sharing

* Gives view access to the logged in users through sharing

Example is provided as Zope External Method. Create External Method
in the target parent folder through the Management Interface.
Then run "Test" for this external method in the Management Interface.

::

    import traceback
    from StringIO import StringIO
    from zope.component import getUtility
    from plone.i18n.normalizer.interfaces import IURLNormalizer


    block_groups = ["Administrators","opettajat","kouluttajat","yhteyshenkilot"]

    def set_sharing(self):

        try:
            buffer = StringIO()
            context = self
            normalizer = getUtility(IURLNormalizer)

            site  = context.portal_url.getPortalObject()
            acl = site.acl_users
            groups = acl.source_groups.getGroupIds()

            existing_folders = context.objectIds()

            # Create a folder per each group
            for g in groups:

                if g in block_groups:
                    continue

                print >> buffer, "Doing group:" + g

                g = g.decode("utf-8")

                id = normalizer.normalize(g)
                if not id in existing_folders:
                    context.invokeFactory("Folder", id)

                folder = context[id]

                # Set sharing rights
                # - No inheritance
                folder.__ac_local_roles_block__ = True

                # - Group has edit access


                # - Logged in users have view access

        except Exception, e:
            traceback.print_exc(buffer)

        return buffer.getvalue()


General methods to manipulate local roles (sharing)
===================================================

::

    folder.manage_setLocalRoles(userid, ['Reader'])


would grant the role "Reader" (Can View on the Sharing Tab) to userid.

Beware that this will set the local roles for the user to only ['Reader']. If the user already has other local roles, this will (untested) clear those.

It will not affect inherited roles.


