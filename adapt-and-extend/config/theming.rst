Theming
=======

.. note::

    Please note that this control panel page will never be themed.
    This is a safety measure, so that even when a Theme is not working correctly you can get back to this screen to disable or edit it.


.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Theme setup screen
       Go to  ${PLONE_URL}/@@theming-controlpanel
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/theme-setup.png
       ...  css=#content

.. figure:: ../../_robot/theme-setup.png
   :align: center
   :alt: Theme configuration

   For a full description on Diazo theming and the Theme editor, see :doc:`this section </adapt-and-extend/theming/index>`