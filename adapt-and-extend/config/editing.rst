Editing
=======


.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Editing setup screen
       Go to  ${PLONE_URL}/@@editing-controlpanel
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/editing-setup.png
       ...  css=#content

.. figure:: ../../_robot/editing-setup.png
   :align: center
   :alt: Editing setup configuration

"Link Integrity Checks" means that users will be warned if they try to delete an item that is being linked to from another content item.
This setting is usually best left "on"

Likewise, it is best to leave the "Enable locking" setting on.
