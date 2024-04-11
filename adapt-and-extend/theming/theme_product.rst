======================================
Create a Plone 5 theme product (addon)
======================================

Introduction
------------

Creating a theme product with the Diazo inline editor is an easy way to start and to test, but it is not a solid long term solution.

Even if ``plone.app.theming`` allows to import and export a Diazo theme as a ZIP archive, it might be prefereable to manage your theme in an actual Plone product.

One of the most obvious reason is it will allow you to override Plone elements that are not accessible from the pure Diazo features (like overloading content views templates, viewlets, configuration settings, etc.).

Create a product to handle your Diazo theme
-------------------------------------------

To create a Plone 5 theme skeleton, you will use mrbob's templates for Plone.

Install mr.bob and bobtemplates.plone
+++++++++++++++++++++++++++++++++++++

To install mr.bob you can do::

   $ pip install mr.bob

and to install the needed bobtemplates for Plone, do::

   $ pip install bobtemplates.plone

Create a Plone 5 theme product skeleton with mrbob::

   $ mrbob -O plonetheme.tango bobtemplates.plone:addon

It will ask you some questions::

   --> What kind of package would you like to create? Choose between 'Basic', 'Dexterity', and 'Theme'. [Basic]: Theme

here choose Theme and fill out the rest of the questions as you like::

   --> Author's name [MrTango]:

   --> Author's email [md@derico.de]:

   --> Author's github username: MrTango

   --> Package description [An add-on for Plone]: Plone theme tango

   --> Plone version [4.3.6]: 5.0b3

   Generated file structure at /home/maik/develop/plone/plonetheme.tango

Now you have a new python package in your current folder::

   (mrbob)maik@planetmobile:~/develop/plone/plonetheme.tango
   $ ls
   bootstrap-buildout.py   buildout.cfg  CONTRIBUTORS.rst  MANIFEST.in  setup.py  travis.cfg
   bootstrap-buildout.pyc  CHANGES.rst   docs              README.rst   src

You can run::

   $ python bootstrap-buildout.py
   Creating directory '/home/maik/develop/plone/plonetheme.tango/bin'.
   Creating directory '/home/maik/develop/plone/plonetheme.tango/parts'.
   Creating directory '/home/maik/develop/plone/plonetheme.tango/develop-eggs'.
   Generated script '/home/maik/develop/plone/plonetheme.tango/bin/buildout'.

Then you can run::

   $ ./bin/buildout

This will create the whole develoment environment for your package::

   $ ls bin/
   buildout                          code-analysis-hasattr               develop        pildriver.py
   code-analysis                     code-analysis-imports               flake8         pilfile.py
   code-analysis-clean-lines         code-analysis-jscs                  fullrelease    pilfont.py
   code-analysis-csslint             code-analysis-jshint                instance       pilprint.py
   code-analysis-debug-statements    code-analysis-pep3101               lasttagdiff    postrelease
   code-analysis-deprecated-aliases  code-analysis-prefer-single-quotes  lasttaglog     prerelease
   code-analysis-find-untranslated   code-analysis-utf8-header           longtest       release
   code-analysis-flake8              code-analysis-zptlint               pilconvert.py  test

You can run::

   $ ./bin/instance fg

to start a Plone instance and play with your packaged.

Your package source code is in the src folder::

   $ tree src/plonetheme/tango/
   src/plonetheme/tango/
   ├── browser
   │   ├── configure.zcml
   │   ├── __init__.py
   │   ├── __init__.pyc
   │   ├── overrides
   │   └── static
   ├── configure.zcml
   ├── __init__.py
   ├── interfaces.py
   ├── locales
   │   ├── plonetheme.tango.pot
   │   └── update.sh
   ├── profiles
   │   ├── default
   │   │   ├── browserlayer.xml
   │   │   ├── metadata.xml
   │   │   ├── plonethemetango_default.txt
   │   │   └── theme.xml
   │   └── uninstall
   │       ├── browserlayer.xml
   │       ├── plonethemetango_uninstall.txt
   │       └── theme.xml
   ├── setuphandlers.py
   ├── testing.py
   ├── tests
   │   ├── __init__.py
   │   ├── __init__.pyc
   │   ├── robot
   │   │   └── test_example.robot
   │   ├── test_robot.py
   │   └── test_setup.py
   └── theme
       ├── index.html
       ├── manifest.cfg
       ├── rules.xml
       └── template-overrides

   11 directories, 25 files

As you see, the packages contains already a Diazo theme::

   $ tree src/plonetheme/tango/theme/
   src/plonetheme/tango/theme/
   ├── index.html
   ├── manifest.cfg
   ├── rules.xml
   └── template-overrides

Here you can build your Diazo theme. For details how to do that, look at :doc:`plone.app.theming</external/plone.app.theming/docs/index>` and :doc:`Diazo</external/diazo/docs/index>`.


Override Plone BrowserViews with jbot
-------------------------------------

A large part of the Plone UI is provided by BrowserView or Viewlet templates.

That is the case for viewlets (all the blocks you can see when you call the url
``./@@manage-viewlets``).

.. note::

   To override them from the Management Interface, you can go to ``./portal_view_customizations``.

To override them from your theme product, the easiest way is to use
``z3c.jbot`` (Just a Bunch of Templates).

Since jbot is already included in the skeleton, you can just start using it, by putting in ``src/plonetheme/tango/browser/overrides/`` all the templates you want to override.
But you will need to name them by prefixing the template name by its complete path to its original version.

For instance, to override ``colophon.pt`` from plone.app.layout, knowing this template in a subfolder named ``viewlets``, you need to name it ``plone.app.layout.viewlets.colophon.pt``.

.. note::

   Management Interface > portal_view_customizations is a handy way to find the template path.

You can now restart Zope and re-install your product from the Plone control panel (Site Setup > Add-ons).


