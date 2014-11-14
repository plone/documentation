Working with Mockup
===================

Building the documentation and examples
---------------------------------------

To see it in action, you must compile everything once with:

.. code-block:: bash

    $ make docs

Then, start the python test server like so:

.. code-block:: bash

    $ python -m SimpleHTTPServer

After that, access the served site in a web browser via the url http://localhost:8000


Running tests
-------------

Run tests with PhantomJS and continue to listen for changes:

.. code-block:: bash

    $ make test

Run tests with Chrome:

.. code-block:: bash

    $ make test-dev

Or run the tests for an individual plugin:

.. code-block:: bash

    $ make test-once pattern=select2


.. _makefile-commands:

More Makefile commands
----------------------

The ``Makefile`` provides this list of commands::

    all                 Tests everything once, creates all default bundles and builds the documentation.
    bootstrap           Bootstrap Mockup. Cleans the environment (deletes node_modules and bower_components) and installs npm and bower dependencies.
    bootstrap-common    Common tasks for other bootstrap tasks. Not intended to be run manually.
    bootstrap-nix       Bootstraps Mockup for NixOS environments. It installs all dependencies via the nix package manager. For nix users.
    bundle-filemanager  Builds the resourceeditor filemanager bundle.
    bundle-plone        Builds the Plone bundle.
    bundle-resourceregistry Builds the bundle for the new resource registry.
    bundle-structure    Builds the structure bundle (wildcard.foldercontents content browser).
    bundle-widgets      Builds the widgets bundle.
    bundles             Builds all the default bundles (bundle-widgets, bundle-structure, bundle-plone).
    clean               Clean the environment by removing the build, node_modules and bower_components directory.
    clean-deep          Clean the environment like with ``clean`` and additionally clean bower's and node's cache.
    docs                Builds the Mockup documentation.
    jshint              Run the code quality suite (jshint and jscs).
    publish-docs        Publish the github pages documentation.
    test                Run Mockup's tests and keep watching for file changes. Accepts the option [--pattern=PATTERNNAME] to define a specific pattern.
    test-ci             Run the tests on the Continious Integration server environment.
    test-dev            Run Mockup's tests in the Chromium browser and keep watching for file changes. Accepts the [--pattern=PATTERNNAME] option to define a specific pattern.
    test-once           Run Mockup's tests only once. Accepts the [--pattern=PATTERNNAME] option to define a specific pattern.
    watch               Watches for file changes and rebuilds Mockup.

All tests also accept the experimental ``--debug`` and ``--verbose`` options to
help with debugging by changing the verbosity of the log messages.


Using Bower directly
--------------------

After making changes to bower.json, you don't have to run ``make bootstrap``, which
wipes all dependencies and starts installing them all over again. You can use
bower directly:

.. code-block:: bash

    $ bower search PACKAGENAME  # search online for a package in the bower registry
    $ bower list  # list all dependencies and possible updates
    $ bower install  # install all dependencies listed in bower.json
    $ bower update  # update all dependencies to the versions specified in bower.json

For more information, see the `bower API documentation <http://bower.io/docs/api/>`_.


Including a local mockup-core checkout for developing
-----------------------------------------------------

If you want to also hack on `mockup-core
<https://github.com/plone/mockup-core>`_ together with mockup, clone
mockup-core into a directory on your machine and just symlink it into
bower_components::

    $ cd ..
    $ git clone https://github.com/plone/mockup-core
    $ cd mockup/bower_components
    $ rm -R mockup-core
    $ ln -s ../../mockup-core .

.. note::
    You can also point bower.json to a local git checkout. You have to point
    bower directly to the `.git` subdirectory and declare the branch name in
    order to be able to use a local checkout. For that, replace the
    `mockup-core` line in `bower.json` with something like the following::

        "mockup-core": "file:///PATH/TO/mockup-core/.git/#master"

    Please note, you have to commit any changes on mockup-core and then run
    ``bower install``, ``bower update`` or ``make bootstrap`` in mockup again.

