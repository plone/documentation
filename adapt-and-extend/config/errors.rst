Error log
=========


.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Error log setup screen
       Go to  ${PLONE_URL}/prefs_error_log_form
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/errorlog-setup.png
       ...  css=#content

.. figure:: ../../_robot/errorlog-setup.png
   :align: center
   :alt: Error log setup configuration


From this screen you can see the most recent errors and *exceptions*.

Remember: not all 'exceptions' are harmful or indications of potential problems.
It can be that visitors just mis-typed a URL, or many other reasons.

But in case of trouble, or if you are trying to find out if your permissions are working correctly, this should be your first port of call.

