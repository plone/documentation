================
Getting started
================

How to get started with Plone development.


Introduction
------------

Plone is developed in the :doc:`Python </develop/plone/getstarted/python>` programming language. :doc:`You should master Python basics </develop/plone/getstarted/python>`
before you can efficiently customize Plone. If you are very new to Python, Plone or software development,
it is suggested that you read the `Professional Plone 4 Development book
<http://www.packtpub.com/professional-plone-4-development/book>`_
before you attempt to develop your own solutions.

Plone runs on the top of the `Zope 2 application server <zope2.zope.org/>`_, meaning that one Zope 2 server process
can contain and host several Plone sites. Plone also uses Zope 3 components. Zope 3 is not an upgrade for Zope 2,
but a separate project.

Internally, Plone uses the objected-oriented :doc:`ZODB </develop/plone/persistency/index>` database and the development
mindset greatly differs from that of SQL based systems. SQL backends can still be integrated with Plone,
like for any other Python application, but this is a more advanced topic.


Training
--------

A number of Plone trainers have joined forces to create completely open  `Training materials <http://training.plone.org/5>`_.

While following a real-life course is the best way to get up to speed with Plone, the material is also very useful for self-study.
You will find separate chapters on creating packages, writing your own theme and much more here.

Installing Plone
----------------

It is recommended that you do Plone development on Linux or OS X. Development on Windows is possible,
but you need to have much more experience dealing with Python and Windows related problems, so starting
on Windows is not so easy.

See :doc:`installation instructions </manage/installing/installation>` for how to create a Plone installation
suitable for development.

Non-programming approaches for customizing Plone
------------------------------------------------

If you lack programming skill or resources, you can still get some things done in Plone:

* `Plomino is a a powerful and flexible web-based application builder for Plone <http://www.plomino.net>`_

* `PloneFormGen allows you to build forms in a web browser <https://plone.org/products/ploneformgen>`_

* Plone comes with through-the-web Dexterity content type editor

However, for heavy customization, Python, JavaScript, TAL page templates and CSS programming is needed.

Enabling debug mode
-------------------

By default, Plone runs in a *production mode* where changed files in the file system
are not reflected in the served HTML. When you start developing Plone you need to
first :doc:`put it into a debug mode </develop/plone/getstarted/debug_mode>`.

Plone add-ons as Python packages
--------------------------------

Plone sites can be customized by installing *Plone add-ons*, which add or customize functionality.
You can install existing add-ons that others have developed or you can develop and install your own add-ons.
Add-ons are developed and distributed as
`Python packages <http://packages.python.org/distribute/setuptools.html>`_. Many open-source Python packages,
including Plone add-ons, are available from `PyPI (the Python Package index) <https://pypi.python.org>`_.

Plone uses a tool called `Buildout <http://www.buildout.org/>`_ to manage the set of Python packages
that are part of your Plone installation.
Using Buildout involves using the ``buildout.cfg`` configuration file and the ``bin/buildout`` command.


Finding and installing add-on packages
--------------------------------------

Plone add-ons can be found at the `plone.org Products
<https://plone.org/products>`_ page or at the  `PyPI (the Python
Package index) <https://pypi.python.org>`_.

See the :doc:`Installing add-on packages using buildout
</manage/installing/installing_addons>` section for more details.


Creating your first add-on
--------------------------

Since Python egg package structure is little bit complex, to get started with your first add-on you can create a code skeleton (scaffold) for it using :doc:`bobtemplates for Plone </develop/addons/bobtemplates.plone/README>`.

* Mr.Bob with the bobtemplates.plone generates a basic Python egg package with some Plone files in-place.

* This package is registered to buildout as a development egg in the ``buildout.cfg`` file.

* Buildout is rerun which regenerates your ``bin/instance`` script with the new set of Python eggs.

* You start your Plone instance in debug mode.

* You install your add-on through ``Add/remove add-ons``

If you want to create a package with Dexterity content types please read about :doc:`Setting up a Dexterity project</external/plone.app.dexterity/docs/prerequisite>`.

Plone development workflow
--------------------------

You never edit Plone files directly. Everything under ``parts`` and ``eggs``
folders in your Plone installation is downloaded from the Internet and dynamically generated by Buildout,
based on ``buildout.cfg``.
Buildout is free to override these files on any update.

You need to have your own add-on in the ``src/`` folder as created above.
There you overlay changes to the existing Plone core through extension mechanisms provided by Plone:

* :doc:`Layers </develop/plone/views/layers>`

* :doc:`Adapters </develop/addons/components/adapters>`

* :doc:`Installation profiles </develop/addons/components/genericsetup>`

Plone development always happens on your local computer or the development server.
The changes are moved to production through version control system like Git or Subversion.

**The best practice is that you install Plone on your local computer for development**.

Plone add-on features
---------------------

.. note::

	Explain that Archetypes are old and basically there to support upgraded sites, but that new development should use Dexterity, maybe remove them even ?

Plone add-ons usually:

* Create custom :doc:`content types </develop/plone/content/index>` or extend existing ones for your specialized need. Plone has
  two subsystems for <content types: :doc:`Dexterity</develop/plone/content/dexterity>`.

* Add new :doc:`views </develop/plone/views/browserviews>` for your site and its content.

* Create Python-processed :doc:`forms </develop/plone/forms/index>` on your site.

* Theme your site

* etc.

A lot of Plone functionality is built on :doc:`Zope 3 development patterns </develop/addons/components/index>`
like adapters and interfaces.
These design patterns take some time to learn, but they are crucial in complex component based software like Plone.


Development mode restarts
-------------------------

Plone must be started in the development mode using ``bin/instance fg`` command. Then

* JavaScript files are in debug mode and automatically loaded when you hit refresh

* CSS files are in debug mode and automatically loaded when you hit refresh

* TAL page templates (.pt files) are automatically reloaded on every request

* :doc:`GenericSetup XML files are reloaded </develop/addons/components/genericsetup>`

Please note that Plone development mode does not reload ``.py`` or ``.zcml`` files by default.
This is possible, however.
Use the `sauna.reload <https://pypi.python.org/pypi/sauna.reload/>`_ package to make Plone reload your Python code automatically when it is changed.

Through-the-web customizations
------------------------------

Some aspects of Plone can be changed through the Management Interface.
Documentation here does not focus on extending functionality through the Management Interface
because this method is severely limited and usually can take you only half way there.

Plone resources
---------------

* `Plone Issue Tracker <https://github.com/plone/Products.CMFPlone/issues>`_ contains bug reports, Plone source
  code and commits.
  Useful when you encounter a new exception or you are looking for a reference on how to use the API.

* `Plone source code in version control system <https://github.com/plone>`_.

* `Plone API (in development) <http://docs.plone.org/develop/plone.api/docs/index.html>`_.


Zope resources
---------------

* `Zope source code in version control system <https://github.com/zopefoundation>`_.

* `Zope 2 book <http://docs.zope.org/zope2/zope2book/>`_.
  This describes old Zope 2 technologies. The book is mostly good for explaining some old things,
  but '''do not''' use it as a reference for building new things.

  The chapters on Zope Page Templates however are still the best reference on the topic.

Python resources
----------------

.. toctree::
   :maxdepth: 2

   python

Debug mode explained
--------------------


.. toctree::
   :maxdepth: 2

   debug_mode
