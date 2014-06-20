=========================
Product package layout
=========================

.. admonition:: Description

    Conventions and techniques for organizing the package for an AT product.

Following Zope, Plone and AT’s conventions, the content of our example
product pakage will look like this:

::

    - __init__.py
    - configure.zcml
    - config.py
    - interfaces.py
    - content
        - __init__.py
        - message.py
    - profiles
        - default
    - browser
        - __init__.py
        - configure.zcml
        - instantmessage.pt
    - tests
        - __init__.py
        - base.py
        - test_setup.py

What is the purpose of these files and directories?

-  \_\_init\_\_.py: The usual “Python package” initialization module;
-  configure.zcml: Using Zope’s new Configuration Markup Language
   (ZCML), this file configures the services or behaviour the Zope
   server needs to load at startup;
-  config.py: Provides configuration variables for the product;
-  interfaces.py: Where you define interfaces describing what the
   packages’ classes will do;
-  content: Contains the modules providing the implementation of the
   content types. In this case, it contains the message.py file where
   the ‘InstantMessage’ class should be defined;
-  profiles/default: Contains a set of XML files that are needed to
   provide the settings that will be used by Plone’s Quick-Installer
   tool when installing the product within Plone; this is what we call
   an *Extension Profile*, an artifact of Zope CMF’s GenericSetup
   technology. *Note that this replaces the old way of doing based on
   the Extensions/Install*. More precisely, since Plone 3.0, you do not
   need that old-style technique;
-  browser: The sub-package where the developer can add specific
   presentation code such as browser views and templates; the contained
   configure.zcml is used to provide these components registration.
-  tests: Contains the unit tests code for the product.

If you have ZopeSkel installed, you can use the following command to
create a similar structure:

::

    paster create -t archetype example.archetype

Now we will go through the files one by one and add what we need to
produce our application.

