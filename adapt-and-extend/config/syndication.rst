Syndication settings
====================

.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Syndication setup screen
       Go to  ${PLONE_URL}/@@syndication-controlpanel
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/syndication-setup.png
       ...  css=#content

.. figure:: ../../_robot/syndication-setup.png
   :align: center
   :alt: Syndication setup configuration

These settings will allow you to enable syndication of your content via various standard protocols.

By default, the well-supported RSS (versions 1 and 2), Atom and iTunes formats are supported.

You can enable these settings side-wide, or just for a specific Folder or Collection, for instance one that you create with the latest News items, press releases, or blog posts.