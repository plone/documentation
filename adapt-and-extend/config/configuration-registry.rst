Configuration Registry
======================

Users with role "Manager" can directly see, and change, many variables that influence Plone.

As you can see, there is a large number of these, and finding the right one is quicker done by filtering or selecting a prefix.
(Add-on packages will also create their own prefix)

.. note::

   Setting variables directly here is *not* recommended as part of regular maintenance.
   It is a useful tool for *inspecting* variables for expert users.

.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Configuration Registry screen
       Go to  ${PLONE_URL}/portal_registry
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/configuration-registry.png
       ...  css=#content

.. figure:: ../../_robot/configuration-registry.png
   :align: center
   :alt: Configuration Registry