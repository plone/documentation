Introduction
============

.. image:: https://secure.travis-ci.org/plone/bobtemplates.plone.png?branch=master
    :target: http://travis-ci.org/plone/bobtemplates.plone

.. image:: https://pypip.in/d/bobtemplates.plone/badge.png
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: Downloads

.. image:: https://pypip.in/v/bobtemplates.plone/badge.png
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: Latest Version

.. image:: https://pypip.in/egg/bobtemplates.plone/badge.png
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: Egg Status

.. image:: https://pypip.in/license/bobtemplates.plone/badge.png
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: License

``bobtemplates.plone`` provides a `mr.bob`_ template to generate packages for Plone projects.

To create a package like ``collective.myaddon``::

    $ mrbob -O collective.myaddon bobtemplates:plone_addon

You can also create a package with nested namespace::

    $ mrbob -O collective.foo.myaddon bobtemplates:plone_addon


Options
=======

On creating a package you can choose from the following options. The default value is in [square brackets]:


Author's name
    Should be something like 'John Smith'.

Author's email
    Should be something like 'john@plone.org'.

Author's github username
    Should be something like 'john'.

Package description [An add-on for Plone]
    One-liner describing what this package does. Should be something like 'Plone add-on that ...'.

Package keywords [Plone Python]
    Keywords/categoris describing this package. Should be something like 'Plone Python Diazo...'.

Version of the package [0.1]
    Should be something like '0.1'.

License of the package [GPL]
    Should be something like 'GPL'.

Plone version [4.3.4]
    Which Plone version would you like to use?

Add locales? [False]
    Do you want to add translations to this package?

Add example view? [True]
    Do you want to register a browser view 'demoview' as an example?

Use generic setup profile? [True]
    Do you want the package to have a generic setup profile? If you select False all following questions will be skipped.

Add setuphandlers? [True]
    Do you want the package to have a setuphander.py to run cusotm code during install?

Add a diazo-theme? [False]
    Do you want to add a empty theme using diazo/plone.app.theming to the package?

Add tests? [True]
    Do you want to add a basic setup for tests, robot-tests and travis-integration?

Prepare Travis Integration? [False]
    Should the package be prepared to be integrated into travis (http://travis-ci.org)? If you select False all following questions will be skipped.

Type of Travis CI notifications [email]
    Should be something like 'email' or 'irc', see : http://about.travis-ci.org/docs/user/notifications for more information.

Destination for Travis CI notifications
    Should be something like 'travis-reports@example.com' or 'irc.freenode.org#plone'.


Compatibility
=============

Addons created with ``bobtemplates.plone`` are tested to work in Plone 4.3.x and Plone 5.
They should also work with older versions but that was not tested.


Installation
============

Use in a buildout
-----------------

::

    [buildout]
    parts += mrbob

    [mrbob]
    recipe = zc.recipe.egg
    eggs =
        mr.bob
        bobtemplates.plone


This creates a mrbob-executeable in your bin-directory.
Call it from the ``src``-directory of your Plone project like this.::

    $ ../bin/mrbob -O collective.foo bobtemplates:plone_addon


Installation in a virtualenv
----------------------------

You can also install ``bobtemplates.plone`` in a virtualenv.::

    $ pip install mr.bob

    $ pip install bobtemplates.plone

Now you can use it like this::

    $ mrbob -O collective.foo bobtemplates:plone_addon

See `mr.bob`_ documentation for further information : http://mrbob.readthedocs.org/en/latest/

.. _mr.bob: http://mrbob.readthedocs.org/en/latest/
