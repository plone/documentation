Resource Registries
===================

.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Resource Registry screen
       Go to  ${PLONE_URL}/@@resourceregistry-controlpanel
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/resource-registry.png
       ...  css=#content
       Click link  Less Variables
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/less-variables.png
       ...  css=#content

The Resource Registry allows access to JavaScript, CSS and LESS resources.

.. figure:: ../../_robot/resource-registry.png
   :align: center
   :alt: Resource Registry


LESS variables
--------------

Particularly useful are the many LESS variables that affect the theme of a site:


.. figure:: ../../_robot/less-variables.png
   :align: center
   :alt: Less variables