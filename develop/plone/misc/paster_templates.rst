======================================================
 Creating your own Paster templates
======================================================

.. admonition:: Description

	How to create Paster code skeleton templates to easily add your
	own add-on product types or code inside your add-on porduct.

Introduction
------------

Plone CMS and Python extensively use :doc:`paster code templating system </develop/addons/paste>`
to aid add-on product development.

Paster allows you to create code from code skeleton templates,
automatically filling in your company name etc.

Default Plone templates are in `ZopeSkel <http://plone.org/products/zopeskel>`_ package.

* This document tells how to create your own paster templates

* For information how to use paster please refer to :doc:`paster section in tutorials </develop/addons/paste>`

More information

* http://wiki.pylonshq.com/display/pylonscookbook/Creating+Templates+For+The+paster+create+Command

* http://plone.org/products/zopeskel

* http://svn.plone.org/svn/collective/collective.dexteritypaste/trunk

* http://svn.plone.org/svn/collective/ZopeSkel/trunk/zopeskel/

Extending ZopeSkel
------------------

First you need to create a Python egg where your templates will be contained.
We use ZopeSkel's *plone* template, but generic Python template should do as well.

	paster create -t plone gomobile.templates

.. note ::

	You do not need tests.py or configure.zcml files in the template package itself.

setup.py entries
================

Then we edit ``setup.py`` and add paster template entry points::

      install_requires=[
          'setuptools',
          'PasteScript',
          'ZopeSkel',
          # -*- Extra requirements: -*-
      ],

      entry_points="""
              # These will declare what templates paster create command can find
              # -*- Entry points: -*-
              [paste.paster_create_template]
              dexterity = gomobile.templates.theme:Theme
              """,

You could also have "subtemplates" with local paster commands which add more code
into existing code skeletons::

      [zopeskel.zopeskel_sub_template]
      dexterity_content = collective.dexteritypaste.localcommands.dexterity:DexterityContent
      dexterity_behavior = collective.dexteritypaste.localcommands.dexterity:DexterityBehavior
      dexterity_view = collective.dexteritypaste.localcommands.dexterity:DexterityView

Entry points
+++++++++++++

Entrypoints allow different plug-in systems through using the standard Python eggs and ``setup.py`` file.
Plone 3.3+ picks Plone add-ons through this way and ``paster`` command pick available templates
from all available eggs this way.

More information

* http://wiki.pylonshq.com/display/pylonscookbook/Using+Entry+Points+to+Write+Plugins

Template class
==============

Paster template is defined with a class referred from the entry point.
Here is an example how we extend the existing Plone template class

Variables and asking for the user input
=======================================

*ZopeSkel* contains facilities how to ask template input from the user who is running Paster.
It provides some sane way to give defaults and validate the input.

Examples

* http://svn.plone.org/svn/collective/ZopeSkel/trunk/zopeskel/abstract_buildout.py

.. note ::

    ZopeSkel input definitions should work both on command line and on the web based generator.

Pre- and postcondition triggers
===============================

If you want to run special code before the templates are run and after they have successfully
complete, ZopeSkel provides some logic for this.

More information

* http://svn.plone.org/svn/collective/ZopeSkel/trunk/zopeskel/hosting.py

* http://pythonpaste.org/script/paste/script/templates.py.html?f=11&l=143#11

Template folder structure
=========================

All templates should go to ``templates`` folder in your ZopeSkel extension namespace.

Filenames and folder names can contain variable substitues as::

    templates/yourtemplatename/+namespace_package+/

will be mapped to::

    yourcompany.package/yourcompany/

Template files
==============

Files having special ``_tmpl`` extension will have string substitution performed on then.
Paster supports `Cheetah templates <http://packages.python.org/Cheetah/users_guide/index.html>`_
(default) and
`Python string templates <http://docs.python.org/release/2.5.2/lib/node40.html>`_

Example:

* http://svn.plone.org/svn/collective/collective.dexteritypaste/trunk/collective/dexteritypaste/templates/dexterity/setup.py_tmpl

The best way to get the initial template files and folders for your add-on template is to
checkout some existing ZopeSkel package, like *collective.dexteritypaste* and export its
*templates* folder to your own add-on template.

.. note ::

        As writing of this I am not aware of any meta-template to create paster templates.
        But should thing would be greatly beneficial.


Variable substitution
=====================

Simple string variable substitution is like::

        from ${dotted_name} import ${portlet_filename}
        from ${dotted_name}.tests.base_${portlet_filename} import TestCase

More information

* http://svn.plone.org/svn/collective/ZopeSkel/trunk/zopeskel/localcommands/templates/plone/portlet/tests/test_+portlet_filename+.py_tmpl

Default variables
+++++++++++++++++

Defaulte template variables are inherited from various base classes of ZopeSkel templates.
One good place to look them is ``basic_namespace.py`` template declaration.

Useful snippets::

        ${namespace_package}.${package}


More information

* http://svn.plone.org/svn/collective/ZopeSkel/trunk/zopeskel/basic_namespace.py

Variable preparation
+++++++++++++++++++++

You can also prepare template variables in Python code
in your Paster template class's ``pre()`` method::

        class Portlet(PloneSubTemplate):
            """
            A plone 3 portlet skeleton
            """
            _template_dir = 'templates/plone/portlet'
            summary = "A Plone 3 portlet"

            vars = [
              var('portlet_name', 'Portlet name (human readable)',  default="Example portlet"),
              var('portlet_type_name', 'Portlet type name (should not contain spaces)', default="ExamplePortlet"),
              var('description', 'Portlet description', default=""),
                   ]

            def pre(self, command, output_dir, vars):
                """
                you can use package_namespace, package_namespace2, package
                and package_dotted_name of the parent package here. you get them
                for free in the vars argument
                """
                vars['portlet_filename'] = vars['portlet_type_name'].lower()

More information

* http://svn.plone.org/svn/collective/ZopeSkel/trunk/zopeskel/localcommands/plone.py

Escaping strings
++++++++++++++++

If you have any page template (``*.pt``) files you need to templatetize you will
encounter problem that both Cheetah and Zope Page Templates use the similar
string expansion syntax causing a conflict.

You can use \ (backslash) before dollar sign to escape it.

Example::

         <script tal:attributes="src string:\${viewlet/portal_url}/++resource++${namespace_package}.${package}/theme.js" type="text/javascript"></script>

Conditions and branching
=========================

If you need to have if, for and buddies in the templates see Cheetah manual.

Example

* http://svn.plone.org/svn/collective/ZopeSkel/trunk/zopeskel/templates/plone/+namespace_package+/+package+/configure.zcml_tmpl

Local commands
==============

Local commands define insert snippets which will be injected to the existing files.

The marker for snippet injects is::

	  -*- extra stuff goes here -*-

You need to put it to the comment format of the file type. Example for XML would be (``configure.zcml_tmpl``)::

  	  <!-- -*- extra stuff goes here -*- -->

Local command injection templates have ``_insert`` in their filename extension.
Then the local command injection snippet ``configure.zcml_insert`` look like::

            <plone:behavior
                title="${behavior_name}"
                description="${behavior_description}"
                provides="${behavior_short_dottedinterface}"
                factory="${behavior_short_dottedadapter}"
                for="plone.dexterity.interfaces.IDexterityContent"
                />

More information

* http://pythonpaste.org/script/developer.html#what-do-commands-look-like

Some examples

* http://svn.plone.org/svn/collective/collective.dexteritypaste/trunk/collective/dexteritypaste/templates/dexterity/+namespace_package+/+package+/configure.zcml_tmpl

* http://svn.plone.org/svn/collective/collective.dexteritypaste/trunk/collective/dexteritypaste/localcommands/templates/dexterity/behavior/behavior/configure.zcml_insert

Testing the templates
=====================

ZopeSkel provides some doctest based testing facilities to hook your templates
to automatic testing facilities, mainly for the regression testing.

Examples

* http://svn.plone.org/svn/collective/ZopeSkel/trunk/zopeskel/docs/plone3_buildout.txt

* http://svn.plone.org/svn/collective/ZopeSkel/trunk/zopeskel/docs/localcommands.txt

Developing template egg with paster and buildout.cfg
----------------------------------------------------

The preferred method to run paster with Plone is to have it
automatically pulled in and configured for you by :doc:`buildout </old-reference-manuals/buildout/index>`.

develop-eggs
============

You need to specially mention to buildout which Python eggs are
in source code form.

* You can use ``develop-eggs`` directive

* You can use buildout extensions designed for source code and version
  control management, like `mr.developer <https://pypi.python.org/pypi/mr.developer>`_.

Then you need to declare ``[paster]`` part and section in ``buildout.cfg``::

        parts =
            ...
            paster

        develop-eggs =
                src/yourcompany.templates

        [paster]
        recipe = zc.recipe.egg
        # Include your own template egg here.
        # Note that ${instance} section name should be the section name
        # for plone.recipe.zope2instance from your buildout.cfg
        eggs =
                PasteScript
                ZopeSkel
                yourcompany.templates
                ${instance:eggs}

Rerun buildout.

Now when you run paster command it should show your custom template::

        bin/paster create --list-templates
        ...
        Available templates:
          archetype:          A Plone project that uses Archetypes content types
          basic_namespace:    A basic Python project with a namespace package
          basic_package:      A basic setuptools-enabled package
          basic_zope:         A Zope project
          gomobile_theme:     A theme for Go Mobile for Plone <---- you should see yours somewhere here
          kss_plugin:         A project for a KSS plugin

Testing the generated product
=============================

This checks that your template generates viable code.
We use package called ``gomobiletheme.yourcompany`` in this examples.

Steps

Generate a product skeleton using ``paster`` in non-interactive mode

.. code-block:: console

        rm -rf src/gomobiletheme.yourcompany ; bin/paster create --no-interactive -v -f -o src -t gomobile_theme gomobiletheme.yourcompany

.. note ::

        Use -f switch or you might encounter problems with template inheritance.

`See paster bug regarding template inheritance and -f switch <http://trac.pythonpaste.org/pythonpaste/ticket/445>`_.

Put the newly created add-on skeleton to ``buildout.cfg`` in develop eggs and eggs::

        eggs =
                gomobiletheme.yourcompany

        develop-eggs =
                src/gomobiletheme.yourcompany

Run buildout

.. code-block:: console

        bin/buildout

Run :doc:`testrunner </manage/deploying/testing_tuning/testing_and_debugging/unit_testing>` for the created add-on

.. code-block:: console

        bin/test -s gomobiletheme.yourcompany

See ``bin/paste create --help`` for other useful debug switches.



