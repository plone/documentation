=======
Toolbar
=======

.. topic:: Description

   How to configure and extend the toolbar


Visibility Of The Default Toolbar
=================================

By default the toolbar is shown to the logged in user.

There are some use-cases where a user, for example one just logs in to view content that otherwise would be hidden, doesn't need the default toolbar.
For those users the full featured toolbar, as it is by default, is not necessary and only takes up space on the screen.

.. versionadded:: 5.1

With the :guilabel:`Show Toolbar` you can show or hide the toolbar accroding to user permissions.
This allows you to show the default toolbar only to certain roles.

If the users role isn't configured to show the default toolbar, a smaller member toolbar with the users personal actions (Personal Preferences, Logout,...) will be displayed at the logation where the login links is.

You can set the visibility on the security tab within the ZMI or you add *rolemap.xml* file to the profile of your site.
See :doc:`Custom permission </develop/plone/security/custom_permission>` for more information.


How To Add A custom Toolbar Menu
================================

Please evaluate first if the extra toolbar entry is really necessary, or if it could fit in one of the existing ones, to not overload the toolbar with entries.

Below is an example on how to extend the toolbar with a custom menu entry.


.. code-block:: python

   from plone.app.contentmenu.interfaces import IActionsMenu
   from plone.app.contentmenu.interfaces import IActionsSubMenuItem
   from plone.app.contentmenu.menu import BrowserMenu
   from plone.app.contentmenu.menu import BrowserSubMenuItem

   @implementer(IActionsSubMenuItem)
   class MyGroupSubMenuItem(BrowserSubMenuItem):

      title = 'Title of menu'
      submenuId = 'my_id'

      extra = {
         'id': 'plone-mymenuid',
         'li_class': 'plonetoolbar-myclass'
      }

      order = 70

      @property
      def action(self):
          return 'url-for-action'

      def available(self):
         if checkPermission('cmf.ModifyPortalContent', self.context):
            return True
        return False

      def selected(self):
        return False


   @implementer(IActionsMenu)
   class MyGroupMenu(BrowserMenu):

      def getMenuItems(self, context, request):
         return [{
            'title': 'Sub menu item',
            'description': '',
            'action': 'url-to-do-something',
            'selected': False,
            'icons': None,
            'extra': {
               'id': 'some-id',
               'separator': None,
               'class': ''
            },
            'submenu': None
         }]

ZCML::

    <browser:menu
        id="my_id"
        title=""
        class=".menu.MyGroupMenu"
        />

    <adapter for="* *"
             name="my_name"
             factory=".menu.MyGroupSubMenuItem"
             provides="plone.app.contentmenu.interfaces.IContentMenuItem" />

For more examples and better understanding please see the ``plone.app.contentmenu`` package.
