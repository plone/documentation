Image handling
==============

.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Image handling setup screen
       Go to  ${PLONE_URL}/@@imaging-controlpanel
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/imaging-setup.png
       ...  css=#content

.. figure:: ../../_robot/imaging-setup.png
   :align: center
   :alt: Imaging setup configuration


Here you can define what scales of images will be available to content editors.
Plone automatically creates these image scales on the fly.

The value '88' for image quality is a good compromise between speed and quality.