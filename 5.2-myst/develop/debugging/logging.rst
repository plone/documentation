=======
Logging
=======

.. admonition:: Description

   How to write log output from your Plone add-on program code.


Introduction
-------------

`Python logging package <http://docs.python.org/library/logging.html>`_ is used to log from Plone.


Viewing Logs In Real Time
-------------------------

The best way to trace log messages when developing, is start the Zope instance in foreground mode. Log messages are printed to the console (stdout).

You can of course also view the logs from the logfile

.. code-block:: shell

   tail -f var/log/instance.log

Press ``CTRL+C`` to abort.


The Site Error Log Service
--------------------------

Plone sites contain error log service which is located as *error_log* in the site root. It logs site exceptions and makes
the tracebacks accessible from Plone control panel and the Management Interface.

The service is somewhat archaic and can log exceptions only, not plain error messages.


Log Level
---------

Default log level is ``INFO``. To enable more verbose logging, edit ``buildout.cfg``,

Change log level by editing ``[instance]`` section ``event-log-level``

.. code-block:: shell

   [instance]
   event-log-level = debug

More information

* https://pypi.python.org/pypi/plone.recipe.zope2instance

Logging From Python Code
------------------------

Example

.. code-block:: console

    import logging

    logger = logging.getLogger("Plone")

    class MySomething(object):
        ...
        def function(self):
        logger.info("Reached function()")
            ...

Logging From Page Templates And RestrictedPython Scripts
---------------------------------------------------------

Python ``logging`` module doesn't provide Zope 2 security assertations
and does not work in :doc:`RestrictedPython Python scripts </develop/plone/security/sandboxing>`.

However, you can use ``context.plone_log()`` method logging in the sandboxed execution mode.

Example::

    context.plone_log("This is so fun")

Forcing Log Level And Output
----------------------------

The following snippet forces the log level of Python logging for the duration of the process
by modifying the root logger object::

        # Force application logging level to DEBUG and log output to stdout for all loggers
        import sys, logging

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)

Temporarily Capturing Log Output
----------------------------------

You can capture Python logging output temporarily to a string buffer.
This is useful if you want to use logging module to record
the status of long running operations and later show to the
end user, who does not have access to file system logs,
how the operation proceeded.

Below is an :doc:`BrowserView </develop/plone/views/browserviews>` code example.

Example view code::

        import logging
        from StringIO import StringIO

        from Products.Five import BrowserView

        from xxx.objects.interfaces import IXXXResearcher
        from Products.statusmessages.interfaces import IStatusMessage

        from xxx.objects.sync import sync_with_xxx

        logger = logging.getLogger("XXX sync")


        class SyncAll(BrowserView):
            """
            Update all researcher data on the site from XXX (admin action)
            """

            def sync(self):
                """
                Search all objects of certain type on the site and
                sync them with a remote site.
                """

                brains =  self.context.portal_catalog(object_provides=IXXXResearcher.__identifier__)
                for brain in brains:
                    object = brain.getObject()
                    sync_with_xxx(object, force=True)

            def startCapture(self, newLogLevel = None):
                """ Start capturing log output to a string buffer.

                http://docs.python.org/release/2.6/library/logging.html

                @param newLogLevel: Optionally change the global logging level, e.g. logging.DEBUG
                """
                self.buffer = StringIO()

                print >> self.buffer, "Log output"

                rootLogger = logging.getLogger()

                if newLogLevel:
                    self.oldLogLevel = rootLogger.getEffectiveLevel()
                    rootLogger.setLevel(newLogLevel)
                else:
                    self.oldLogLevel = None

                self.logHandler = logging.StreamHandler(self.buffer)
                formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                self.logHandler.setFormatter(formatter)
                rootLogger.addHandler(self.logHandler)

            def stopCapture(self):
                """ Stop capturing log output.

                @return: Collected log output as string
                """

                # Remove our handler
                rootLogger = logging.getLogger()

                # Restore logging level (if any)
                if self.oldLogLevel:
                    rootLogger.setLevel(self.oldLogLevel)


                rootLogger.removeHandler(self.logHandler)

                self.logHandler.flush()
                self.buffer.flush()

                return self.buffer.getvalue()

            def __call__(self):
                """ Process the form.

                Process the form, log the output and show the output to the user.
                """

                self.logs = None

                if "sync-now" in self.request.form:
                    # Form button was pressed

                    # Open Plone status messages interface for this request
                    messages = IStatusMessage(self.request)

                    try:
                        self.startCapture(logging.DEBUG)

                        logger.info("Starting full site synchronization")

                        # Do the long running,
                        # lots of logging stuff
                        self.sync()

                        logger.info("Successfully done")

                        # It worked! Trolololo.
                        messages.addStatusMessage("Sync done")

                    except Exception, e:
                        # Show friendly error message
                        logger.exception(e)
                        messages.addStatusMessage(u"It did not work out:" + unicode(e))

                    finally:
                        # Put log output for the page template access
                        self.logs = self.stopCapture()
                return self.index()

The related page template

.. code-block:: html

        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
              lang="en"
              metal:use-macro="here/main_template/macros/master"
              i18n:domain="xxx.objects">
        <body>
            <div metal:fill-slot="main">
                <tal:main-macro metal:define-macro="main">

                        <h1 class="documentFirstHeading">
                                XXX site update
                        </h1>

                        <p class="documentDescription">
                              Update all researches from XXX
                        </p>

                        <div tal:condition="view/logs">
                                <p>Sync results:</p>
                                <pre tal:content="view/logs" />
                        </div>

                        <form action="@@syncall" method="POST">
                                <button type="submit" name="sync-now">
                                        Sync now
                                </button>
                        </form>

                </tal:main-macro>
            </div>
        </body>
        </html>


Registering the view in ZCML:

.. code-block:: xml

    <browser:view
            for="Products.CMFPlone.interfaces.IPloneSiteRoot"
            name="syncall"
            class=".views.SyncAll"
            permission="cmf.ManagePortal"
            />


transaction_note()
-------------------

Leave a note on Zope's *History* tab.

* https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/utils.py#L382
