==========================
Create an add-on package
==========================

.. admonition:: Description

    A simple tutorial introducing the basics of Plone development.

.. contents:: :local:

Before extending Plone, we need to create an add-on package to hold our changes. It's possible you would have more than one add-on package. One popular approach is to have a theme product and a product containing your business logic.

We will use ZopeSkel to create a skeleton template for the project. For more information on ZopeSkel, see the section on `Bootstrapping Plone add-on development <http://docs.plone.org/4/en/develop/addons/paste.html>`_.

.. note::

    Using paster is deprecated instead you should use :doc:`bobtemplates.plone </develop/addons/bobtemplates.plone/README>`


.. deprecated:: may_2015
    Use :doc:`bobtemplates.plone </develop/addons/bobtemplates.plone/README>` instead

Put your projects in the src directory of your buildout directory.

- Change your working directory to the src directory of your buildout.::

     # from your buildout directory
     cd src


- Create a project using ZopeSkel 2.21.2 from our virtual_env. Here, we create an archetypes based project in a directory named example.helloworld.::

    ../../bin/zopeskel archetype example.helloworld

- ZopeSkel will ask you a series of questions. For now, you can use the defaults for Expert Mode and Version. Use *Hello World* for the Project Title. We will reference it in another step below.::

    Expert Mode? (What question mode would you like? (easy/expert/all)?) ['easy']:
    Project Title (Title of the project) ['Example Name']: Hello World
    Version (Version number for project) ['1.0']:
    Description (One-line description of the project) ['']: Simple Hello World Example

The zopeskel command creates a directory in the src directory named **example.helloworld**.::

    [michaelc@Cullerton src]$ ll
    total 8
    -rw-r--r--   1 michaelc  staff   62 Aug 25 21:25 README.txt
    drwxr-xr-x  12 michaelc  staff  408 Aug 28 23:33 example.helloworld

Before we move one, lets examine our directory structure. We have **env-27**, our virtual_env. It contains **hello_world**, our Plone installation. We also call this the **buildout directory**. The *buildout directory* contains the **buildout.cfg** file. It also contains the **src** directory, which contains our project **example.helloworld**.

.. image:: /develop/addons/helloworld/images/directory_structure.png
   :alt: image of directory structure

Looking further into *example.helloworld*, we have the **example** directory which contains the **helloworld** directory.

In the examples below, we sometimes refer to the *helloworld* directory as the **product directory**. It contains the **browser** directory. Most of the changes we make take place in the *browser* directory.

Here it is from the command-line.::

    [michaelc@Cullerton src]$ ll example.helloworld/
    total 48
    -rw-r--r--   1 michaelc  staff    94 Aug 28 23:31 CHANGES.txt
    -rw-r--r--   1 michaelc  staff    12 Aug 28 23:31 CONTRIBUTORS.txt
    -rw-r--r--   1 michaelc  staff    47 Aug 28 23:31 MANIFEST.in
    -rw-r--r--   1 michaelc  staff   371 Aug 28 23:31 README.txt
    drwxr-xr-x   6 michaelc  staff   204 Aug 28 23:31 docs
    drwxr-xr-x   5 michaelc  staff   170 Aug 28 23:32 example
    drwxr-xr-x  11 michaelc  staff   374 Aug 28 23:31 example.helloworld.egg-info
    -rw-r--r--   1 michaelc  staff    33 Aug 28 23:31 setup.cfg
    -rw-r--r--   1 michaelc  staff  1858 Aug 28 23:31 setup.py

    [michaelc@Cullerton src]$ ll example.helloworld/example
    total 16
    -rw-r--r--   1 michaelc  staff  244 Aug 28 23:31 __init__.py
    -rw-r--r--   1 michaelc  staff  410 Aug 28 23:32 __init__.pyc
    drwxr-xr-x  16 michaelc  staff  544 Aug 28 23:50 helloworld

    [michaelc@Cullerton src]$ ll example.helloworld/example/helloworld/
    total 64
    -rw-r--r--  1 michaelc  staff  2093 Aug 28 23:31 README.txt
    -rw-r--r--  1 michaelc  staff  2079 Aug 28 23:31 __init__.py
    -rw-r--r--  1 michaelc  staff  1513 Aug 28 23:41 __init__.pyc
    drwxr-xr-x  5 michaelc  staff   170 Aug 28 23:42 browser
    -rw-r--r--  1 michaelc  staff   133 Aug 28 23:31 config.py
    -rw-r--r--  1 michaelc  staff   326 Aug 28 23:41 config.pyc
    -rw-r--r--@ 1 michaelc  staff  1054 Aug 28 23:42 configure.zcml
    drwxr-xr-x  5 michaelc  staff   170 Aug 28 23:42 content
    drwxr-xr-x  3 michaelc  staff   102 Aug 28 23:31 interfaces
    -rw-r--r--@ 1 michaelc  staff  1377 Aug 28 23:53 person.py
    -rw-r--r--  1 michaelc  staff  2838 Aug 28 23:50 person.pyc
    drwxr-xr-x  5 michaelc  staff   170 Aug 28 23:42 portlets
    drwxr-xr-x  3 michaelc  staff   102 Aug 28 23:31 profiles
    drwxr-xr-x  5 michaelc  staff   170 Aug 28 23:31 tests


To use the code in your project, you'll need to reference it in your buildout.cfg file.

- Edit the *buildout.cfg* file.

    Add *example.helloworld* to the *eggs* section.::

        eggs =
            PIL
            Plone
            example.helloworld

    Add *src/example.helloworld* to the *develop* section.::

        develop =
            src/example.helloworld

    Then save your changes.

- You need to rerun buildout for the changes to take effect.::

    # from your buildout directory
    ./bin/buildout

- Then start or restart your Plone instance.::

    # from your buildout directory
    ./bin/instance start
    or
    ./bin/instance restart

Note::

    If you are running ZEO instead of a stand-alone instance you'll need to use something like::

        ./bin/client1 restart

Now you can install your product from the **Add-ons** are of **Site Setup**. You can access Site Setup from the **admin** menu in the top right corner of your Plone site.

    .. image:: /develop/addons/helloworld/images/sitesetup.png

You can also access Site Setup using an url like

    *http://localhost:8080/Plone/plone_control_panel*

- Select *Add-ons* from the *Site Setup* page. On the Add-ons page, select the *Hello World* add-on and click on *Activate*.

    .. image:: /develop/addons/helloworld/images/addons.png

Now that you created and installed an add-on package, you can use it to extend Plone.


