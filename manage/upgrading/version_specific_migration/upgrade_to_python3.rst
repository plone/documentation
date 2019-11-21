===============================
Migrating Plone 5.2 to Python 3
===============================


.. admonition:: Description

   Instructions and tips for porting Plone projects to Python 3

.. note::

   If you want to upgrade add-ons to Python 3, the list of all Plone packages that still need to be ported can be found on the  GitHub project board `Python 3 porting state for Plone add-ons <https://github.com/orgs/collective/projects/1>`_.


Make Custom Packages Python 3 Ready
===================================

Principles
----------

* You should support Python 2 and 3 with the same codebase to allow it to be used in existing versions of Plone.
* Plone 5.2 supports Python 2.7, Python 3.6, and Python 3.7.
* We use `six <https://six.readthedocs.io>`_ and `modernize <https://pypi.python.org/pypi/modernize>`_ to do the first steps towards Python 3.

In general you should follow these steps to port add-ons:

#. Prepare ``buildout`` for the add-on to be ported.
#. Update code with `python-modernize <https://python-modernize.readthedocs.io/en/latest/>`_.
#. Use `plone.recipe.precompiler <https://github.com/plone/plone.recipe.precompiler>`_ (also called ``precompiler`` for brevity) to find syntax errors.
#. Start the instance and find more errors.
#. Test functionality manually.
#. Run and fix all tests.
#. Update package information.
#. Update package buildout and test-setup


1 Preparation
-------------

In the GitHub repository of the add-on:

* Open a ticket with the title "Add support for Python 3".
* Create a new branch named ``python3``.

.. warning::

    The following section is valid until the final release of Plone 5.2.
    Upon the final release of Plone 5.2, something else will take its place.

Using Released Plone 5.2
~~~~~~~~~~~~~~~~~~~~~~~~

Usually it is fine to use the latest Plone 5.2 release.
The version pins for the latest release can be found for pip at `https://dist.plone.org/release/5.2-latest/requirements.txt`_ and for buildout at `https://dist.plone.org/release/5.2-latest/versions.cfg`_.
Install Plone with Python 3.6 or 3.7 and then add your addons as source using ``mr.developer`.

Using Core Development Buildout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With `buildout.coredev <https://github.com/plone/buildout.coredev>`_ the latest development version of Plone can be used.
It contains everything for porting an add-on to Python 3.
Follow these steps:

.. code-block:: shell

    # Clone coredev and use branch 5.2:
    git clone git@github.com:plone/buildout.coredev.git coredev_py3
    cd coredev_py3
    git checkout 5.2
    # Create a py3 virtual environment with either Python 3.6 or 3.7 (they are very similar):
    python3.7 -m venv .
    # Install buildout:
    ./bin/pip install -r requirements.txt

Next create a file called ``local.cfg`` in the root of the buildout.
This file will be used to add your add-on to the buildout.
Add your package as in the following example.
Exchange ``collective.package`` with the name of the add-on you want to port.

.. note::

    This example expects a branch with the name ``python3`` to exist for the package.
    Adapt it for your use case.

.. code-block:: ini

    [buildout]
    extends = buildout.cfg

    always-checkout = true
    allow-picked-versions = true

    custom-eggs +=
        collective.package

    test-eggs +=
        collective.package [test]

    auto-checkout +=
        collective.package

    [sources]
    collective.package = git git@github.com:collective/collective.package.git branch=python3

With the file in place, run buildout.
Then the source of the add-on package will be checked out into the ``src`` folder.

.. note::

    You can also add development tools like `Products.PDBDebugMode <https://pypi.org/project/Products.PDBDebugMode/>`_, `plone.reload <https://pypi.org/project/plone.reload/>`_ and `Products.PrintingMailHost <https://pypi.org/project/Products.PrintingMailHost/>`_ to your buildout.

    Especially ``Products.PDBDebugMode`` will help a lot with issues during porting to Python 3.

    .. code-block:: ini

        custom-eggs +=
            collective.package
            Products.PDBDebugMode
            plone.reload
            Products.PrintingMailHost

        test-eggs +=
            collective.package [test]

        auto-checkout +=
            collective.package

.. code-block:: shell

    ./bin/buildout -c local.cfg

Now everything is prepared to work on the migration of the package.

For small packages or packages that have few dependencies, it is a good idea to try starting your instance now.

.. code-block:: shell

    ./bin/instance fg

If it does not start up, you should continue with the next steps instead of trying to fix each issue as it appears.


2 Automated Fixing With Modernize
---------------------------------

``python-modernize`` is a utility that automatically prepares Python 2 code for porting to Python 3.
After running ``python-modernize``, there is manual work ahead.
There are some problems that ``python-modernize`` can not fix on its own.
It also can make changes that are not really needed.
You need to closely review all changes after you run this tool.

``python-modernize`` will warn you, when it is not sure what to do with a possible problem.
Check this `Cheat Sheet <http://python-future.org/compatible_idioms.html>`_  with idioms for writing Python 2/3 compatible code.

``python-modernize`` adds an import of the compatibility library ``six`` if needed.
The import is added as the last import, therefore it is often necessary to reorder the imports.
The easiest way is to use `isort <https://pypi.python.org/pypi/isort>`_, which does this for you automatically.
Check the `Python style guide for Plone <https://docs.plone.org/develop/styleguide/python.html#grouping-and-sorting>`_ for information about the order of imports and an example configuration for ``isort``.

If ``six`` is used in the code, make sure that ``six`` is added to the ``install_requires`` list in the ``setup.py`` of the package.

Installation
~~~~~~~~~~~~

Install ``modernize`` into your Python 3 environment with ``pip``.

.. code-block:: shell

    ./bin/pip install modernize

Install ``isort`` into your Python 3 environment with ``pip``.

.. code-block:: shell

    ./bin/pip install isort


Usage
~~~~~

The following command is a dry-run. I shows all changes that ``modernize`` would make.

.. code-block:: shell

    ./bin/python-modernize -x libmodernize.fixes.fix_import  src/collective.package

.. note::

    The ``-x`` option is used to exclude certain fixers.
    The one that adds ``from __future__ import absolute_import`` should not be used.
    See ``./bin/python-modernize -l`` for a complete list of fixers and the `fixers documentation <https://python-modernize.readthedocs.io/en/latest/fixers.html>`_.

The following command applies all fixes to the files:

.. code-block:: shell

    ./bin/python-modernize -wn -x libmodernize.fixes.fix_import  src/collective.package

You can use ``isort`` to fix the order of imports:

.. code-block:: shell

    ./bin/isort -rc src/collective.package

After you run the commands above, you need to review all changes and fix what ``modernizer`` did not get right.

3 Use ``precompiler``
---------------------

You can make use of ``plone.recipe.precompiler`` to identify syntax errors quickly.
This recipe compiles all Python code already at buildout-time, not at run-time.
You will see right away when there is some illegal syntax.

Add the following line to the section ``[buildout]`` in ``local.cfg``.
Then run ``./bin/buildout -c local.cfg`` to enable and use ``precompiler``.

.. code-block:: ini

    parts += precompiler

``precompile`` will be run every time you run buildout.
If you want to avoid running the complete buildout every time, you can use the ``install`` keyword of buildout like this as a shortcut:

.. code-block:: shell

    ./bin/buildout -c local.cfg  install precompiler


4 Start The Instance
---------------------

As a next step we recommend that you try to start the instance with your add-on.
This will fail on all import errors (e.g., relative imports that are not allowed in Python 3).
If it works then you can try to install the add-on.

You need to fix all issues that appear before you can do manual testing to check for big, obvious issues.


Common Issues during startup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following issues will abort your startup.
You need to fix them before you are able to test the functionality by hand or run tests.


A - Class Advice
^^^^^^^^^^^^^^^^

This kind of error message:

.. code-block:: shell

    TypeError: Class advice impossible in Python3.  Use the @implementer class decorator instead.

tells you that there is a class that is using an ``implements`` statement which needs to be replaced by the ``@implementer`` decorator.

For example, code that is written as follows:

.. code-block:: python

    from zope.interface import implements

    class Group(form.BaseForm):
        implements(interface.IGroup)

needs to be replaced with:

.. code-block:: python

    from zope.interface import implementer

    @implementer(interfaces.IGroup)
    class Group(form.BaseForm):

The same is the case for ``provides(IFoo)`` and some other Class advices.
These need to be replaced with their respective decorators like ``@provider``.


B - Relative Imports
^^^^^^^^^^^^^^^^^^^^

Relative imports like ``import permissions`` are no longer permitted.
Instead use fully qualified import paths such as ``from collective.package import permissions``.


C - Syntax Error On Importing Async
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Python 3.7 you can no longer have a module called ``async`` (see https://github.com/celery/celery/issues/4849).
You need to rename all such files, folders or packages (like ``zc.async`` and ``plone.app.async``).


5 Test functionality manually
-----------------------------

Now that the instance is running you should do the following and fix all errors as they appear.

* Install the add-on.
* Test basic functionality (e.g., adding and editing content-types and views).
* Uninstall the add-on.

For this step it is recommended that you have installed ``Products.PDBDebugMode`` to help debug and fix issues.


6 Run Tests
------------

.. code-block:: shell

    $ ./bin/test --all -s collective.package

Remember that you can run ``./bin/test -s collective.package -D`` to enter a ``pdb`` session when an error occurs.

With some luck, there will not be too many issues left with the code at this point.

It you are unlucky then you have to fix Doctests.
These should be changed so that Python 3 is the default.
For example, string types (or text) should be represented as ``'foo'``, not ``u'foo'``, and bytes types (or data) should be represented as ``b'bar'``, not ``'bar'``.
Search for examples of ``Py23DocChecker`` in Plone's packages to find a pattern which allows updated doctests to pass in Python 2.

*   To test your code against ``buildout.coredev``, start by browsing to `Add-ons [Jenkins] <https://jenkins.plone.org/view/Add-ons/>`_.
*   Note there are jobs set up for Plone 4.3, 5.1, and 5.2 on Python 2, and two jobs that run tests for Plone 5.2 on Python 3.6 and Python 3.7.
*   Click the link :guilabel:`log in` on Jenkins website (top right). For the first login, you must authorize Jenkins to have access to your GitHub account to authenticate.
*   Click the link for the job you want to run, for example, :guilabel:`Test add-on against Plone 5.2 on Python3.7`.
*   Choose the link :guilabel:`Build with parameters` in the menu on the left-hand side.
*   Fill the fields :guilabel:`ADDON_URL` and :guilabel:`ADDON_BRANCH` with your repository's URL and the branch name ("python3" if you followed these instructions).
*   Start the build with the :guilabel:`Build` button.

.. note::



7 Update Add On Information
---------------------------

Add the following three entries of the classifiers list in setup.py:

.. code-block:: python

    "Framework :: Plone :: 5.2",
    # ...
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",

Make an entry in the ``CHANGES.rst`` file.


8 Create A Test Setup That Tests In Python 2 And Python 3
----------------------------------------------------------

You need to update the buildout of the add-on you are migrating to also support Plone 5.2 and Python 3.
Since the buildout of most add-ons are different we cannot offer advice that works for all add-ons.

But it is be a good idea to create a empty new package with :py:mod:`bobtemplates.plone` and either copy the code of the add-on in there or the new skeleton-files into the old add-on. The least you can do is look at the files created by :py:mod:`bobtemplates.plone` and copy whatever is appropriate to the add-on you are working on.

.. code-block::

    $ ./bin/pip install bobtemplates.plone
    $ ./bin/mrbob -O some.addon bobtemplates.plone:addon

Always use the newest version of :py:mod:`bobtemplates.plone`!

Add-ons created like this contain a setup that allows testing in Python 2 and Python 3 and various Plone versions locally and on travis-ci using :py:mod:`tox`. Look at the files `tox.ini` and `travis.yml`.


9 Frequent Issues
-----------------

Text and Bytes
~~~~~~~~~~~~~~

This is by far the biggest issue when porting to Python 3.
Read the `Conservative Python 3 Porting Guide, Strings <https://portingguide.readthedocs.io/en/latest/strings.html>`_ to be prepared.

.. note::

    As a rule of thumb, you can assume that in Python 3 everything should be text.
    Only in very rare cases will you need to handle bytes.

``python-modernize`` will **not** fix all your text/bytes issues.
It only replaces all cases of ``unicode`` with ``six.text_type``.
You need to make sure that the code you are porting will remain unchanged in Python 2 and (at least in most cases) use text in Python 3.

Try to modify the code in such a way that when dropping support for Python 2 you will be able to delete while lines.
For example:

.. code-block:: python

   if six.PY2 and isinstance(value, six.text_type):
       value = value.encode('utf8')
   do_something(value)

You can use the helper methods ``safe_text`` and ``safe_bytes`` (``safe_unicode`` and ``safe_encode`` in Plone 5.1).

``python-modernize`` also does not touch the import statement ``from StringIO import StringIO`` even though this works only in Python 2.
You have to check whether you are dealing with text or binary data and use the appropriate import statement from ``six`` (https://six.readthedocs.io/#six.StringIO).

.. code-block:: python

    # For textual data
    from six import StringIO
    # For binary data
    from six import BytesIO

.. seealso::

    Here is a list of helpful references on the topic of porting Python 2 to Python 3.

    - https://portingguide.readthedocs.io/en/latest/index.html
    - https://eev.ee/blog/2016/07/31/python-faq-how-do-i-port-to-python-3/
    - http://getpython3.com/diveintopython3/
    - https://docs.djangoproject.com/en/1.11/topics/python3/
    - https://docs.ansible.com/ansible/latest/dev_guide/developing_python_3.html
    - https://docs.python.org/2/library/doctest.html#debugging


