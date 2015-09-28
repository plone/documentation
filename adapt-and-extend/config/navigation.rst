Navigation settings
===================

.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Navigation setup screen
       Go to  ${PLONE_URL}/@@navigation-controlpanel
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/navigation-setup.png
       ...  css=#content

.. figure:: ../../_robot/navigation-setup.png
   :align: center
   :alt: Navigation setup configuration

Plone automatically generates navigation tabs from items you put in the *root*, or top level, of your site. The first two settings allow you to control this:

- do you want them to be generated?
- and if so, should it only be done for Folders or also other items like Pages?

The rest of the options control what items should be visible in the navigation.
The defaults are usually a good choice, although many site administrators turn off "Image".
You can always re-visit this section later.

