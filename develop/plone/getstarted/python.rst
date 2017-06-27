=======================
 Python for beginners
=======================

.. admonition:: Description

    The basics of Python programming, and performing Python interpreter installations.

Introduction
=============

`Python <http://python.org>`_ is the programming language used by
`Plone <https://plone.org>`_ and `Zope <http://zope.org>`_. One needs to have at least basic Python experience
before considering building Plone add-ons or customizations.

.. note ::

     You should not try to write programs for Plone before you can program Python on the basic level.

Python tutorials and online classes
====================================

* `Official Python tutorial <http://docs.python.org/tutorial/>`_

* `Google Python classes <http://code.google.com/edu/languages/google-python-class/>`_

* `Free Python books <http://pythonbooks.revolunet.com/>`_

* `Dive into Python book <http://www.diveintopython.net/toc/index.html>`_

* `Python at codeacademy.org <http://www.codecademy.com/#!/exercises/0>`_

Virtualenv
==========
``virtualenv`` is a tool that allows the creation of virtual environments.

A virtual environment is a way to isolate a python installation from other installations as well as the system wide python.

There a plenty of reasons one wants an isolated environment:

- to be able to have different python installations for each project (a Zope 4 project on python 3 and a Plone 5 project on python 2)
- to be able to install dependencies of each project without installing them system wide
- to not have to need administrator permissions to install project dependencies
- to be able to make the environment repeatable (this is key for any serious testing/Continuous Integration effort)

It is so important,
that since Python 3.3 is a standard module: `venv <https://docs.python.org/3/library/venv.html>`_,
see the `PEP405 <https://www.python.org/dev/peps/pep-0405/>`_ that lead to the ``venv`` module for all the details and rationale.

Install virtualenv
------------------
If you plan to use a virtual environment on a Python 3.3+ project you are done!
You don't need to install *anything* in order to use virtual environments.

If you are working on a project prior to Python 3.3,
you need to install `virtualenv <https://pypi.python.org/pypi/virtualenv>`_.
Fortunately, either your system (especially on Linux distributions) has already system packages that install it system wide,
or you can install it with `pip <https://pypi.python.org/pypi/pip>`_.

Use virtualenv
--------------
To create a virtual environment on python 3.3+, do the following:

.. code-block:: shell

    python3 -m venv my-environment

If you use the ``virtualenv`` python package:

.. code-block:: shell

    virtualenv my-environment

Once the folder is created you can enter it and start using it:

.. code-block:: shell

    cd my-environment
    source bin/activate
    pip install zc.buildout setuptools
    *use*
    deactivate

.. note::

   Some developers do not *activate* the virtual environment and rather call directly the tools on the ``bin`` folder.
   This has the advantage that one does not need to activate and deactivate the environment every time.
