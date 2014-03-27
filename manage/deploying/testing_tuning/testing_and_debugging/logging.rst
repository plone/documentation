==============
Logging
==============

.. admonition:: Description

        How to write log output from your Plone add-on program code

.. contents:: :local:

Introduction
-------------

`Python logging package <http://docs.python.org/library/logging.html>`_ is used to log from Plone.

Log file location
==================

By default, logs go to ``var/log`` folder under buildout. 

If Zope instance is started in the foreground mode
logs will be printed in the console (stdout).

Plone log filename varies depending on the installation mode (Zope, ZEO cluster).
But for each instance there are two log files

* Event logs (errors), normally called *instance.log*

* HTTP request log (Apache compatible), normally called *Z2.log*

Viewing logs in real time
===========================

UNIX'y way for your terminal.

Open error log viewer using ``tail`` command (print content from file end) and wait for further file writes 

.. code-block:: console
    
     tail -f var/log/instance.log 


Press CTRL+C to abort.

Log level 
=========

Default log level is ``INFO``. To enable more verbose logging, edit ``buildout.cfg``,

Change log level by editing ``[instance]`` section ``event-log-level``::

        [instance]
        event-log-level = debug

More information 

* http://pypi.python.org/pypi/plone.recipe.zope2instance

Logging from Python code
------------------------

Example::

    import logging

    logger = logging.getLogger("Plone")

    class MySomething(object):
        ...
        def function(self):
            logger.info("Reached function()")
            ...

Logging from page templates and RestrictedPython scripts
--------------------------------------------------------

Python ``logging`` module doesn't provide Zope 2 security assertations
and does not work in :doc:`RestrictedPython Python scripts </develop/plone/security/sandboxing>`.

However, you can use ``context.plone_log()`` method logging in the sandboxed execution mode.

Example::

    context.plone_log("This is so fun")

Forcing log level and output
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

Temporarily capturing log output
----------------------------------

You can capture Python logging output temporarily to a string buffer.
This is useful if you want to use logging module to record
the status of long running operations and later show to the 
end user, who does not have access to file system logs,
how the operation proceeded.

Below is an Grok view code example. 

Example view code::

        import logging
        from StringIO import StringIO
        
        from five import grok
        
        from xxx.objects.interfaces import IXXXResearcher
        from Products.CMFCore.interfaces import ISiteRoot
        from Products.statusmessages.interfaces import IStatusMessage
        
        from xxx.objects.sync import sync_with_xxx
        
        grok.templatedir("templates")
        
        logger = logging.getLogger("XXX sync")
                

        class SyncAll(grok.View):
            """
            Update all researcher data on the site from XXX (admin action)
            """
        
            grok.context(ISiteRoot)
        
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
                
            def update(self):        
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

transaction_note()
-------------------

Leave a note on Zope's *History* tab.

* https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/utils.py#L382



