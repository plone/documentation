Managing Users and Groups
=========================

.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Users setup screen
       Go to  ${PLONE_URL}/@@usergroup-userprefs
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/users-setup.png
       ...  css=#content

       Go to  ${PLONE_URL}/@@usergroup-groupprefs
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/groups-setup.png
       ...  css=#content
       Go to  ${PLONE_URL}/@@usergroup-controlpanel
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/users-settings.png
       ...  css=#content
       Go to  ${PLONE_URL}/@@member-fields
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/users-fields.png
       ...  css=#content

User setup
----------

.. figure:: ../../_robot/users-setup.png
   :align: center
   :alt: Users setup configuration

Here you can search for existing users, and add a new user.
When you search for existing users you can edit their properties (if you have the Manager role)


.. note::

   Many large organisations use a form of centralised user management, such as Active Directory or LDAP.
   In that case, it may not be possible to define users and/or groups here.

Group setup
-----------

.. figure:: ../../_robot/groups-setup.png
   :align: center
   :alt: Groups setup configuration

This gives an overview of the current groups, and allows you to define new ones.
Also sets the security mapping: here you map Groups to Roles.

As also seen in the guide on :doc:`Sharing and collaborating </working-with-content/collaboration-and-workflow/collaboration-through-sharing>` it's useful to connect Roles (who have permissions) to Groups rather than to individual users. This will make site maintenance easier.

Settings for many users/groups
------------------------------

These options will simply optimize the presentation of users and groups according to the size of your website. If you have thousands or hundreds of thousands of users, you don't want to see them in a list. You will be presented with a searchbox instead.

.. figure:: ../../_robot/users-settings.png
   :align: center
   :alt: usersettings setup configuration

Member data (information about users)
-------------------------------------

Here you can define what information you want to store about users.
There is a range of fields to choose from, from images to numbers to multiple choice.
Each of these fields can be made *required* or not.

Examples could be

- a "choice" field for dietary preferences and restrictions
- Twitter handle
- whatever else you can think of, or your organisation requires!


.. figure:: ../../_robot/users-fields.png
   :align: center
   :alt: Member field setup configuration
