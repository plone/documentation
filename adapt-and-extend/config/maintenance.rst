Maintenance and packing
=======================

.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show ZODB maintenance setup screen
       Go to  ${PLONE_URL}/@@maintenance-controlpanel
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/zodb-setup.png
       ...  css=#content

.. figure:: ../../_robot/zodb-setup.png
   :align: center
   :alt: ZODB maintenance configuration


The only option you should use here, is regularly *pack* the database.

.. note::

   When deploying a Plone site for production, of course it makes much more sense to automate this via a cronjob or similar.