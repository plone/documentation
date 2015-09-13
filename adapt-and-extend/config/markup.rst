Markup
======

.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Markup setup screen
       Go to  ${PLONE_URL}/@@markup-controlpanel
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/markup-setup.png
       ...  css=#content

.. figure:: ../../_robot/markup-setup.png
   :align: center
   :alt: Markup setup configuration

So-called "Markup" languages like `Markdown <https://en.wikipedia.org/wiki/Markdown>`_ and `RestructuredText <https://en.wikipedia.org/wiki/ReStructuredText>`_ are popular with some users, since they can be written using just a keyboard without a mouse or pointing device.

Plone allows these markup languages to be used as text input alternatives, if you so desire.