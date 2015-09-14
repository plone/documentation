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


As you can see, there is not much to do here with Plone manager permissions.

If you have *Zope manager* permissions, there is one extra option here: to *pack* your database. However, in any normal deploying setup, you would want to automate that task via a cronjob or similar mechanism.
