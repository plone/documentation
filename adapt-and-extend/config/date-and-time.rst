Date and Time
=============

.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Date setup screen
       Go to  ${PLONE_URL}/@@dateandtime-controlpanel
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/date-setup.png
       ...  css=#content

.. figure:: ../../_robot/date-setup.png
   :align: center
   :alt: Date and time setup configuration

You can set the default timezone, which is usually the one your server is in.

If you make more timezones available, users can set their own timezone.
That way, dates and times will be converted to their time zone.

.. note::

   This can be convenient, but potentially confusing.
   Consider announcing a physical Event on your site: the Ritz Theatre, Thursday, 21.00 hours.
   Logged-in visitors who are yet to travel from their timezone to your grand event will see the starting time in their timezone.
