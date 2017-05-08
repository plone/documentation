=======================
Zope Application Server
=======================

.. admonition:: Description

    Plone is usually run via the Zope application server.
    This document covers control and configuration of parts
    of the application server.


Introduction
============

This page contains instructions how to configure Zope application server.

Zope control command
====================

The command for Zope tasks is ``bin/instance`` in buildout-based Plones
(depending on how the part(s) for the Zope instance(s) was named in the
buildout configuration file; here, it's ``instance``).

List available commands::

    bin/instance help

For older Plone releases, the command is ``zopectl``.

If you have installed a ZEO cluster, you may have multiple instances, typically named client1, client2 ....
Substitute ``client#`` for ``instance`` below.
The zeoserver part must be running before you may directly use a client command::

    bin/zeoserver start
    bin/client1 help

Adding users from command-line
==============================

In case you need to reset/recover the ``admin`` password/access.

.. note::

    You cannot override an existing ``admin`` user, so you probably want to add ``admin2``.

You need to do this when you forget the admin password or the database is
damaged.

Add user with Zope Manager permissions.

.. code-block:: shell

    bin/instance stop # stop the site first
    bin/instance adduser $USERNAME $PASSWORD
    bin/instance start

More info

* https://plone.org/documentation/faq/locked-out

Timezone
========

Add to the ``[instance]`` part in ``buildout.cfg``:

.. code-block:: cfg

    environment-vars =
            TZ Europe/Helsinki

Log level
=========

The default log level in Zope is ``INFO``. This causes a lot of
logging that is usually not needed.

To reduce the size of log files and improve performance, add
the following to the ``[instance]`` part (the part(s) that specify
your Zope instances) in ``buildout.cfg``:

.. code-block:: cfg

    event-log-level = WARN
    z2-log-level = CRITICAL


Creating additional debug instances
===================================

You might want to keep your production ``buildout.cfg`` and development
configuration
in sync automatically as possible.

A good idea is to use the same ``buildout.cfg`` for every Plone environment.
For conditional things, such as turning debug mode on, extend the buildout
sections, which in turn create scripts to launch additional Zope clients in
the ``bin/`` folder:

.. code-block:: cfg

    [instance]
    recipe = plone.recipe.zope2instance
    zope2-location = ${zope2:location}
    user = admin:x
    http-address = 8080
    debug-mode = off
    verbose-security = off

    ...

    environment-vars =
        PTS_LANGUAGES en fi

    #
    # Create a launcher script which will start one Zope instance in debug mode
    #
    [debug-instance]
    # Extend the main production instance
    <= instance

    # Here override specific settings to make the instance run in debug mode
    debug-mode = on
    verbose-security = on
    event-log-level = DEBUG

And now you can start your **development** Zope as:

.. code-block:: shell

    bin/debug-instance fg

And your main Zope instance stays in production mode:

.. code-block:: shell

    bin/instance

.. note::

    Starting Zope with the ``fg`` command forces it into debug mode,
    but does not change the log level.

Virtual hosting
===============

Zope has a component called Virtual Host Monster
which does the virtual host mapping inside Zope. More information can be found in the `zope book <http://docs.zope.org/zope2/zope2book/VirtualHosting.html>`_

Suppressing virtual host monster
--------------------------------

If you ever mess up your virtual hosting rules so that Zope locks you out
of the management interface,
you can add ``_SUPPRESS_ACCESSRULE`` to the URL to disable
VirtualHostMonster.

Import and export
=================

Zope application server allows copying parts of the tree structure via
import/export feature.
The exported file is basically a Python pickle containing the chosen node
and all child nodes.

Importable ``.zexp`` files must be placed on ``/parts/instance/import``
buildout folder on the server.
If you are using  clustered ZEO set-up, always run imports through a
specific front-end instance
by using direct port access. Note that ``parts`` folder structure is pruned
on each buildout run.

When files are placed on the server to correct folder, the :guilabel:`Import/Export` tab
in the Management Interface will pick them up in the selection drop down. You do not need to restart Zope.

More information

* http://quintagroup.com/services/support/tutorials/import-export-plone/

Regular database packing
========================

The append-only nature of the :doc:`ZODB </develop/plone/persistency/database>`
makes the database grow continuously even
if you only edit old information and don't add any new content.
To make sure your server's hard disk does not fill up,
you need to pack the ZODB automatically and regularly.

More info

* http://stackoverflow.com/questions/5300886/what-is-the-suggested-way-to-cron-automate-zodb-packs-for-a-production-plone-ins/

Copying a remote site database
==============================

Below is a UNIX shell script to copy a remote Plone site(s) database to
your local computer. This is useful for synchronizing the
development copy of a site from a live server.

``copy-plone-site.sh``

.. code-block:: bash

    #!/bin/sh
    #
    # Copies a Plone site data from a remote computer to a local computer
    #
    # Copies
    #
    # - Data.fs
    #
    # - blobstorage
    #
    # Standard var/ folder structure is assumed in the destination
    # and the source
    #

    if [ $# -ne 2 ] ; then
    cat <<EOF
    $0
    Copy a remote Plone site database to local computer over SSH
    Error in $0 - Invalid Argument Count
    Syntax: $0 [SSH-source to buildout folder] [buildout target folder]
    Example: ./copy-plone-site.sh yourserver.com:/srv/plone/mysite .
    EOF
    exit 64 # Command line usage error
    fi

    SOURCE=$1
    TARGET=$2

    STATUS=`$TARGET/bin/instance status`

    if [ "$STATUS" != "daemon manager not running" ] ; then
        echo "Please stop your Plone site first"
        exit 1
    fi

    rsync -av --progress --compress-level=9 "$SOURCE"/var/filestorage/Data.fs "$TARGET"/var/filestorage

    # Copy blobstorage on rsync pass
    # (We don't need compression for blobs as they most likely are compressed images already)
    rsync -av --progress "$SOURCE"/var/blobstorage "$TARGET"/var/


Pack and copy big ``Data.fs``
=============================

Pack ``Data.fs`` using the `pbzip2 <http://compression.ca/pbzip2/>`_,
efficient multicore bzip2 compressor, before copying:

.. code-block:: sh

    # Attach to a screen or create new one if not exist so that
    # the packing process is not interrupted even if you lose a terminal
    screen -x

    # The command won't abort in the middle of the run if terminal lost
    cd /srv/plone/yoursite/zeocluster/var/filestorage
    tar -c --ignore-failed-read Data.fs | pbzip2 -c > /tmp/Data.fs.tar.bz2

    # Alternative version using standard bzip2
    # tar -c --ignore-failed-read -jf /tmp/Data.fs.tar.bzip2 Data.fs

Then copy to your own computer:

.. code-block:: shell

    scp unixuser@server.com:/tmp/Data.fs.tar.bz2 .

... or using ``rsync`` which can resume:

.. code-block:: shell

    rsync -av --progress --inplace --partial user@server.com:/tmp/Data.fs.tar.bz2 .

Creating a sanitized data drop
==============================

A *sanitized* data drop is a Plone site where:

* all user passwords have been reset to one known one;

* all history information is deleted (packed), so that it does not contain
  anything sensitive;

* other possible sensitive data has been removed.

It should safe to give a sanitized copy to a third party.

Below is a sample script which will clean a Plone site in-place.

.. note::

    Because sensitive data varies depending on your site this script is
    an example.

How to use:

* Create a temporary copy of your Plone site on your server, running on a
  different port.

* Run the cleaner by entering the URL. It is useful to run the temporary
  copy in foreground to follow the progress.

* Give the sanitized copy away.

This script has two options for purging data:

* *Safe purge* using the Plone API (slow, calls all event handlers).

* *Unsafe purge* by directly pruning data, rebuilding the catalog without
  triggering the event handlers.

The sample ``clean.py``:

.. code-block:: python

    """ Pack Plone database size and clean sensitive data.
        This makes output ideal as a development drop.

        It also resets all kinds of users password to "admin".

        Limitations:

        1) Assumes only one site per Data.fs

        TODO: Remove users unless they are whitelisted.

    """

    import logging
    import transaction

    logger = logging.getLogger("cleaner")

    # Folders which entries are cleared
    DELETE_POINTS = """
    intranet/mydata

    """
    # Save these folder entries as sampple
    WHITELIST = """
    intranet/mydata/sample-page
    """

    # All users will receive this new password
    PASSWORD="123123"

    def is_white_listed(path):
        """
        """
        paths = [ s.strip() for s in WHITELIST.split("\n") if s.strip() != ""]

        if path in paths:
            return True
        return False

    def purge(site):
        """
        Purge the site using standard Plone deleting mechanism (slow)
        """
        i = 0
        for dp in DELETE_POINTS.split("\n"):

            dp = dp.string()
            if dp == "":
                continue

            folder = site.unrestrictedTraverse(dp)

            for id in folder.objectIds():
                full_path = dp + "/" + id
                if not is_white_listed(full_path):
                    logger.info("Deleting path:" + full_path)
                    try:
                        folder.manage_delObjects([id])
                    except Exception, e:
                        # Bad delete handling code - e.g. catalog indexes b0rk out
                        logger.error("*** COULD NOT DELETE ***")
                        logger.exception(e)
                    i += 1
                    if i % 100 == 0:
                        transaction.commit()

    def purge_harder(site):
        """
        Purge using forced delete and then catalog rebuild.

        Might be faster if a lot of content.
        """
        i = 0

        logger.info("Kill it with fire")
        for dp in DELETE_POINTS.split("\n"):

            if dp.strip() == "":
                continue
            folder = site.unrestrictedTraverse(dp)

            for id in folder.objectIds():
                full_path = dp + "/" + id
                if not is_white_listed(full_path):
                    logger.info("Hard deleting path:" + full_path)
                    folder._delObject(id, suppress_events=True)

                    i += 1
                    if i % 100 == 0:
                        transaction.commit()

        site.portal_catalog.clearFindAndRebuild()


    def pack(app):
        """
        @param app Zope application server root
        """
        logger.info("Packing database")
        cpanel = app.unrestrictedTraverse('/Control_Panel')
        cpanel.manage_pack(days=0, REQUEST=None)

    def change_zope_passwords(app):
        """
        """
        logger.info("Changing Zope passwords")
        # Products.PluggableAuthService.plugins.ZODBUserManager
        users = app.acl_users.users
        for id in users.listUserIds():
            users.updateUserPassword(id, PASSWORD)

    def change_site_passwords(site):
        """
        """
        logger.info("Changing Plone instance passwords")
        # Products.PlonePAS.plugins.ufactory
        users = site.acl_users.source_users
        for id in users.getUserIds():
            users.doChangeUser(id, PASSWORD)

    def change_membrane_password(site):
        """
        Reset membrane passwords (if membrane installed)
        """

        if not "membrane_users" in site.acl_users.objectIds():
            return

        logger.info("Changing membrane passwords")
        # Products.PlonePAS.plugins.ufactory
        users = site.acl_users.membrane_users
        for id in users.getUserNames():
            try:
                users.doChangeUser(id, PASSWORD)
            except:
                # XXX: We should actually delete membrane users before content folders
                # or we will break here
                pass

    class Cleaner(object):
        """
        Clean the current Plone site for sensitive data.

        Usage::

            http://localhost:8080/site/@@create-sanitized-copy

        or::

            http://localhost:8080/site/@@create-sanitized-copy?pack=false

        """

        def __init__(self, context, request):
            self.context = context
            self.request = request

        def __call__(self):
            """
            """
            app = self.context.restrictedTraverse('/') # Zope application server root
            site = self.context.portal_url.getPortalObject()

            purge_harder(site)
            change_zope_passwords(app)
            change_site_passwords(site)
            #change_membrane_password(site)

            if self.request.form.get("pack", None) != "false":
                pack(app)

            # Obligatory Die Hard quote
            return "Yippikayee m%&€/ f/€%&/€%&/ Remember to login again with new password."


Example view registration in ZCML requiring admin privileges to run the
cleaner:

.. code-block:: xml

    <browser:page
     for="Products.CMFCore.interfaces.ISiteRoot"
     name="create-sanitized-copy"
     class=".clean.Cleaner"
     permission="cmf.ManagePortal"
    />

Log rotate
==========

Log rotation prevents log files from growing indefinitely by creating a new
file for a certain timespan and dropping old files.

Basic Log rotation for buildout users
-------------------------------------

If you are using buildout and the plone.recipe.zope2instance (>= 4.2.5) to create your
zope installation, two parameters are available to enable log rotation.
For example:

* event-log-max-size = 10mb

* event-log-old-files = 3

This will rotate the event log when it reaches 10mb in size. It will retain a
maximum of 3 files. Similar directives are also available for the access log.

* access-log-max-size = 100mb

* access-log-old-files = 10

Using the unix tool ''logrotate''
---------------------------------

You need to rotate Zope access and error logs, plus possible front-end web
server logs. The latter is usually taken care of your operating system.

To set-up log rotation for Plone:

* Install ``logrotate`` on the system (if you don't already have one).

* You need to know the effective UNIX user as which Plone processes run.

* Edit log rotation configuration files to include Plone log directories.

* Do a test run.

To add a log rotation configuration file for Plone add a file
``/etc/logrotate.d/yoursite`` as root.

.. note::

    This recipe applies only for single-process Zope installs.  If you use
    ZEO clustering you need to do this little bit differently.

The file contains:

.. code-block:: bash

    # This is the path + selector for the log files
    /srv/plone/yoursite/Plone/zinstance/var/log/instance*.log {
            daily
            missingok
            # How many days to keep logs
            # In our cases 60 days
            rotate 60
            compress
            delaycompress
            notifempty
            # File owner and permission for rotated files
            # For additional safety this can be a different
            # user so your Plone UNIX user cannot
            # delete logs
            create 640 root root

            # This signal will tell Zope to open a new file-system inode for the log file
            # so it doesn't keep reserving the old log file handle for evenif the file is deleted
            postrotate
                [ ! -f /srv/plone/yoursite/Plone/zinstance/var/instance.pid ] || kill -USR2 `cat /srv/plone/yoursite/Plone/zinstance/var/instance.pid`
            endscript
    }

Then do a test run of logrotate, as root:

.. code-block:: console

    # -f = force rotate
    # -d = debug mode
    logrotate -f -d /etc/logrotate.conf

And if you want to see the results right away:

.. code-block:: console

    # -f = force rotate
    logrotate -f /etc/logrotate.conf

In normal production, logrotate is added to your operating system *crontab*
for daily runs automatically.

More info:

* http://linuxers.org/howto/howto-use-logrotate-manage-log-files

* http://docs.zope.org/zope2/zope2book/MaintainingZope.html

* http://serverfault.com/questions/57993/how-to-use-wildcards-within-logrotate-configuration-files

Log rotate and chroot
---------------------

.. note::

    In this example we are using the package 'shroot'
    Please make sure you have it installed

``chroot``'ed environments don't usually get their own cron.
In this case you can trigger the log rotate from the parent system.

Add in the parent ``/etc/cron.daily/yourchrootname-logrotate``

.. code-block:: bash

    #!/bin/sh
    schroot -c yoursitenet -u root -r logrotate /etc/logrotate.conf

Log rotate generation via buildout using UNIX logrotate command
---------------------------------------------------------------

``buildout.cfg``:

.. code-block:: ini

    [logrotate]
    recipe = collective.recipe.template
    input =  ${buildout:directory}/templates/logrotate.conf
    output = ${buildout:directory}/etc/logrotate.conf

``templates/logrotate.conf``::

    rotate 4
    weekly
    create
    compress
    delaycompress
    missingok

    ${buildout:directory}/var/log/instance1.log ${buildout:directory}/var/log/instance1-Z2.log {
        sharedscripts
        postrotate
            /bin/kill -USR2 $(cat ${buildout:directory}/var/instance1.pid)
        endscript
    }

    ${buildout:directory}/var/log/instance2.log ${buildout:directory}/var/log/instance2-Z2.log {
        sharedscripts
        postrotate
            /bin/kill -USR2 $(cat ${buildout:directory}/var/instance2.pid)
        endscript
    }

More info:

* http://stackoverflow.com/a/9437677/315168

Log rotate on Windows
---------------------

Use ``iw.rotatezlogs``

* http://stackoverflow.com/a/9434150/315168

Email notifications for errors
------------------------------

Please see:

* http://stackoverflow.com/questions/5993334/error-notification-on-plone-4

Adding multiple file storage mount points
-----------------------------------------

* https://pypi.python.org/pypi/collective.recipe.filestorage
