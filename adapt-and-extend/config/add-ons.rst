Add-ons
=======

.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Date setup screen
       Go to  ${PLONE_URL}/prefs_install_products_form
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/addon-setup.png
       ...  css=#content

.. figure:: ../../_robot/addon-setup.png
   :align: center
   :alt: Add-on configuration

Here you can activate and deactivate add-ons.

.. note::

   Before an add-on will show up here, you will first have to *install* it. See the :doc:`section on installing add-ons </adapt-and-extend/install_add_ons>`

If you have *upgraded* add-ons, there are often *upgrade steps* to bring all configuration of your add-on to the new standard. This is also where you will be doing that.