===================================================================
General advice for upgrading pre-2.5 releases to the latest release
===================================================================

.. admonition:: Description

   To upgrade a very old version of Plone (2.1, 2.0 or 1.0), we recommend that you upgrade to Plone 3.x first, and *then* upgrade to later releases.

In order to keep the Plone codebase tidy, we periodically remove the code that handles upgrades from very old Plone versions.

As a result, Plone 4.x supports upgrades directly from Plone 2.5 and Plone 3.x, but not from older versions such as Plone 1.0 and Plone 2.1.
If you need to upgrade from an older version of plone, we recommend that you first upgrade to the most recent release of Plone 3.x, and then to Plone 4.x.

As an example, let's say you're running an ancient Plone 2.1 install.
The approach to upgrade to (for example) Plone 4.0 would then be:

#. Back up your setup.
#. Move your Data.fs (and upgraded add-on products) to a Plone 3.3.x install.
#. Follow the general upgrade instructions outlined earlier in this manual.
#. Once you have a running Plone 3.3.x-based version of the install, get the latest 4.0.x release, and upgrade from Plone 3.3.x to Plone 4.0

Upgrades from Plone versions earlier than 2.1 can be handled similarly; however, in this case you should upgrade to Plone 2.5 as the intermediary version before going to Plone 3 or Plone 4, since Plone 3.x doesn't support upgrades from Plone less than 2.1.
