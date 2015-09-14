Dexterity Content Types
=======================


.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Dexterity setup screen
       Go to  ${PLONE_URL}/@@dexterity-types
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/dexterity-setup.png
       ...  css=#content

.. figure:: ../../_robot/dexterity-setup.png
   :align: center
   :alt: Dexterity setup configuration

TODO:

Documentation for TTW *("through the web")* configuration of dexterity content types is under development.
