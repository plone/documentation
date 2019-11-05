======================================
Command-line interaction and scripting
======================================

.. admonition:: Description

        How to run command-line Python scripts, timed jobs (cron)
        and batch jobs against Plone sites and Zope application server.

.. contents::
  :local:

Introduction
------------

.. warning::

        Plone code is somewhat ugly and expects you to have real HTTP request lifecycle
        to do many things. For command line scripts, you need to mock up this and mocking
        up often fails. Instead of trying to create a pure command-line script,
        just create a browser view and call that browser view usings wget or
        lynx or similar command line HTTP tool.

Zope provides facilities to run command-line scripts.
or maintenance work, like migration script.

* The output to terminal is instance (Plone buffers HTML output)

* You can stop processing using CTRL+C

* You can integrate scripts with standard UNIX tools, like cron

.. note::

        If the site runs in a single process Zope mode (no ZEO),
        the actual site instance must be stopped to run a command line
        script as the one process locks the database (Data.fs).

Command line scripts are also useful for long-running transaction processing

* A web site runs in multi-client ZEO mode. One client is always offline,
  reserved for running command-line scripts.

* Asynchronous long-running transactions are run from this ZEO client,
  without disturbing the normal site functionality

See also

* `lovely.remotetask package <https://pypi.python.org/pypi/lovely.remotetask>`_
  for more fine-graned control and Zope-based cron jobs


Starting interactive interpreter
--------------------------------

The *bin/instance debug* command starts an interactive interpreter with the Zope application server and
database loaded. You can provide the id of your Plone site with the -O flag to have it available under the
name *obj* and to load :doc:`persistent utilities </develop/addons/components/utilities>`_. The following example assumes
the site is named "Plone". For more infos about command-line options use *bin/instance help debug*.

Example::

    bin/instance -OPlone debug

.. note::

    The instance must be stopped in order to run this.

Running scripts
---------------

Use *bin/instance run* command to run scripts which can interact
with the opened database.

Example::

	bin/instance run src/namespace.mypackage/namespace/mypackage/bin/script.py

The script will have global ``app`` variable assigned to the Zope application server root.
You can use this as a starting point and traverse into your Plone site(s).

Script could look like::

        """

            Instance script for testing a researcher creation

            Execution::

                bin/instance run src/x.y/x/y/testscript.py

        """

        from ora.objects.content.oraresearcher import createResearcherById

        def main(app):
            folder = app.unrestrictedTraverse("x/y/z/cancer")

            # Create a researcher
            createResearcherById(folder, "http://localhost/people/9947603276956765")

            # This script does not commit

        # If this script lives in your source tree, then we need to use this trick so that
        # five.grok, which scans all modules, does not try to execute the script while
        # modules are being loaded on the start-up
        if "app" in locals():
            main(app)

You probably need to spoof your :doc:`security credentials </develop/plone/security/permissions>`.

.. note::

        Instance must be stopped in order to run this.

Cron and timed jobs
-------------------

Cron is UNIX clock daemon for timed tasks.

If you have a ZEO cluster you can have one ZEO client reserved for command line
processing. Cron job will run scripts through this ZEO client.

Alternatively, you can use

* cron to call localhost URL using curl or wget UNIX commands

* Use Zope clock daemon

.. note::

        For long running batch processes it is must that you run your
        site in ZEO mode. Otherwise the batch job will block the site
        access for the duration of the batch job transaction.
        If the batch job takes long to process the site might
        be unavailable for the visitors for a long period.


Scripting context
-----------------

The command line interpreter and scripts gets following global context variables

* *app* global variable which holds the root of Zope application server.

* sys.argv contains command-line parameters after python script name

	* argv[0] = script name

	* arvg[1] = first command line argument


To access your site object, you can traverse down from app::

        app.yoursiteid # This is your Plone site object

        # Perform some stuff here...
        for brain in app.yoursiteid.portal_catalog(portal_type="Document"): print brain["Title"]

Committing transactions
-----------------------

You need to manually commit transactions if you change ZODB data from the command line.

Example how to commit::

        # Commit transaction
        import transaction; transaction.commit()
        # Perform ZEO client synchronization (if running in clustered mode)
        app._p_jar.sync()

More info

* http://www.enfoldsystems.com/software/server/docs/4.0/enfolddebuggingtools.html

zopepy
------

zopepy buildout recipe creating bin/zopepy command which you can use to run Python scripts in Zope environment set-up
(PYTHONPATH, database connection, etc.)

* https://pypi.python.org/pypi/zc.recipe.egg

buildout.cfg example::

	[zopepy]
	# For more information on this step and configuration options see:
	#
	recipe = zc.recipe.egg
	eggs = ${client1:eggs}
	interpreter = zopepy
	extra-paths = ${zope2:location}/lib/python
	scripts = zopepy

Then running::

	bin/zopepy path/to/myscript.py

...or if you want to run a script outside buildout folder::

        cd /tmp
        /srv/plone/site/bin/zopepy pack2.py


Setting up ZEO for command line-processing
------------------------------------------

Plone site HTTP requests are processed by one process per requests.
One process cannot handle more than one request once.
If you need to have long-running transactions you need to at least two front end processes, ZEO clients, so that long-running transactions won't block your site.

* `Converting instance to ZEO based configuration <http://docs.plone.org/4/en/old-reference-manuals/buildout/zope_to_zeo.html>`_

Your code might want to call transaction.commit() now and then to commit the current transaction.

Posing as user
--------------

Zope functionality often assumes you have logged in as certain
user or you are anonymous user. Command-line scripts
do not have user information set by default.

How to set the effective Zope user to a regular user using
:doc:`plone.api context managers </develop/plone.api/docs/env>`::

    from plone import api
    from zope.component.hooks import setSite

    # Sets the current site as the active site
    setSite(app['Plone'])

    # Enable the context manager to switch the user
    with api.env.adopt_user(username="admin"):
        # You're now posing as admin!
        portal.restrictedTraverse("manage_propertiesForm")


Spoofing HTTP request
---------------------

When running from command-line, HTTP request object is not available.
Some Zope code might expect this and you need to spoof the request.

Below is an example command line script which set-ups faux HTTP request
and portal_skins skin layers::

        """

            Command-line script to be run from a ZEO client:


            bin/command-line-client src/yourcode/mirror.py

        """

        import os
        from os import environ
        from StringIO import StringIO
        import logging

        from AccessControl.SecurityManagement import newSecurityManager
        from AccessControl.SecurityManager import setSecurityPolicy
        from Testing.makerequest import makerequest
        from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy, OmnipotentUser

        # Force application logging level to DEBUG and log output to stdout for all loggers
        import sys, logging

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)

        def spoofRequest(app):
            """
            Make REQUEST variable to be available on the Zope application server.

            This allows acquisition to work properly
            """
            _policy=PermissiveSecurityPolicy()
            _oldpolicy=setSecurityPolicy(_policy)
            newSecurityManager(None, OmnipotentUser().__of__(app.acl_users))
            return makerequest(app)

        # Enable Faux HTTP request object
        app = spoofRequest(app)

        # Get Plone site object from Zope application server root
        site = app.unrestrictedTraverse("yoursiteid")
        site.setupCurrentSkin(app.REQUEST)

        # Call External Method defined in the skins layers
        # Note that native python __getattr__ traversing does not work... you must access things using unrestrictedTraverse()
        # You could also use @@viewname for browserviews
        script = site.unrestrictedTraverse("someScriptName")
        script()



More info

* http://wiki.zope.org/zope2/HowToFakeREQUESTInDebugger

Creating Plone site in buildout
-------------------------------

You can pre-generate the site from the buildout run.

* https://pypi.python.org/pypi/collective.recipe.plonesite#example

screen
------

screen is an UNIX command to start a virtual terminal. Screen lets processes
run even if your physical terminal becomes disconnected. This effectively
allows you to run long-running command line jobs over a crappy Internet
connection.

Start new screen
================

Type command::

        screen

If you have sudo'ed to another user you first need to run::

        script /dev/null

* http://dbadump.blogspot.com/2009/04/start-screen-after-sudo-su-to-another.html

Attach to an existing screen
============================

Type command::

        screen -x


