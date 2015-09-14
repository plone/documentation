Social Media metadata
=====================

.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show socialmedia setup screen
       Go to  ${PLONE_URL}/@@social-controlpanel
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/social-setup.png
       ...  css=#content

.. figure:: ../../_robot/social-setup.png
   :align: center
   :alt: Social Media setup configuration


Enabling this setting will add social media meta-tags (OpenGraph and Twitter) to pages, so that when you share a Plone webpage on services like Facebook, Twitter etcetera the links will be formatted nicer.

.. note::

   This **does not** add any kind of "sharing buttons", nor will it connect to the social media networks itself. That is often unacceptable in corporate or Intranet settings. There is a variety of Add-ons that will provide this functionality.

