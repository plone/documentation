===========================
Clock and asyncronous tasks
===========================


.. admonition:: Description

        How to run background tasks or cron jobs with Zope

Cron jobs
=========

You can use simple UNIX cron + wget combo to make timed jobs in Plone.

If you need to authenticate, e.g. as an admin, Zope users (not Plone users)
can be authenticated using HTTP Basic Auth.

* Create user in Zope root (not Plone site root) in acl_users folder

* Call it via HTTP Basic Auth

       http://username:password@localhost:8080/yoursideid/@@clock_view_name

* The ``--auth-no-challenge`` option to the wget command will authenticate even
  if the server doesn't ask you to authenticate. It might come in handy, as
  Plone does not ask for HTTP authentication, and will just serve Unauthorized
  if permissions aren't sufficient.

Clock server
============

You can make Zope to make regular calls to your views.

Add in buildout.cfg::

        zope-conf-additional =
                <clock-server>
                   method /xxx/feed-mega-update
                   period 3600
                   user zopeuser
                   password 123123
                   host xxx.com
                </clock-server>

                <clock-server>
                   method /yyy/feed-mega-update
                   period 3600
                   user zopeuser
                   password 123123
                   host yyy.com
                </clock-server>

Create a corresponding user in Management Interface.

In detail:

* method - Path from root to an executable Zope method (Python script, external method, etc.) The method must receive no arguments.
* period - Seconds between each call to the method. Typically, at least 30 specified.
* user - a Zope Username
* password - The password of this user Zope
* host - The name of the host that is in the header of a request as host: is specified.

To check whether the server clock is running, restart the instance or the ZEO
client in the foreground and see if a message similar to the following is
displayed::

    2009-03-03 19:57:38 INFO ZServer Clock server for "/ mysite / do_stuff" started (user: admin, period: 60)

If you are using a public source control repository for your ``buildout.cfg`` you
might want to put zope-conf-additional= to ``secret.cfg`` which lies only on the
production server and is never committed to the version control::

        # Change the number here to change the version of Plone being used
        extends =
                http://dist.plone.org/release/4.1rc3/versions.cfg
                http://good-py.appspot.com/release/dexterity/1.0?plone=4.1rc3
                http://plonegomobile.googlecode.com/svn/gomobile.buildout/gomobile.plone-4.trunk.commit-access.cfg
                secret.cfg

Creating a separate ZEO instance for long running tasks
-------------------------------------------------------

Below is an example how to extend a single process Plone instance buildout to
contain two ZEO front end processes, client1 and client2 and dedicate client2
for long running tasks. In this example, ``Products.feedfeeder`` RSS zopeuser is set to run on
client2.

* Client1 keeps acting like standalone instance, in the same port as instance used to be

* Clocked tasks are run on client2 - it does not serve other HTTP requests.
  Clocked tasks are done using Zope clock server.

The purpose of this is that client2 does heavy writes to the database, potentially
blocking the normal site operation of the site if we don't have a separate client for it.

We create additional ``production.cfg`` file which extends the default ``buildout.cfg`` file.
You still can use ``buildout.cfg`` as is for the development, but on the production server
your buildout command must be run for the ZEO server enabled file.

Actual clock server jobs, with usernames and passwords, are stored in a separate ``secret.cfg``
file which is only available on the production server and is not stored in the version control system.
The user credentials for a specially created Zope user, not Plone user.
This user can be created through ``acl_users`` in the Management Interface.

We also include ``plonectl`` command for easy management of ZEO server, client1 and client2.

``production.cfg`` (note - you need to run this with ``bin/buildout -c production.cfg``)::

        [buildout]

        extends =
                buildout.cfg
                secret.cfg

        # Add new stuff to be build out when run bin/buildout -c production.cfg

        parts +=
                client1
                client2
                zeoserver
                plonectl
                crontab_zeopack

        # Run our database and stuff
        [zeoserver]
        recipe = plone.recipe.zeoserver
        zeo-address = 9998

        # In ZEO server mode, client1 is clone of standalone
        # [instance] running in ZEO mode, different port
        [client1]
        <= instance
        recipe = plone.recipe.zope2instance
        zeo-client = on
        shared-blob = on
        http-address = 9999

        # Client2 is like client1, just different port.
        # This client is reserved for running clocked tasks (feedfeeder update)
        [client2]
        <= client1
        http-address = 9996

        # Tune down cache-size as we don't operate normally,
        # so we have smaller memory consumption (default: 10000)
        zodb-cache-size = 3000

        [plonectl]
        recipe = plone.recipe.unifiedinstaller
        clients =
                client1
                client2
        user = admin:admin

        # pack your ZODB each Sunday morning and hence make it smaller and faster
        [crontab_zeopack]
        recipe = z3c.recipe.usercrontab
        times = 0 1 * * 6
        command = ${buildout:directory}/bin/zeopack

``secret.cfg`` contains actual clocked jobs. This file contains passwords so it is not
recommended to put it under the version control::

    [client2]
    zope-conf-additional =
        <clock-server>
           method /plonecommunity/feed-mega-update
           period 3600
           user zopeuser
           password secret
           host plonecommunity.mobi
        </clock-server>

        <clock-server>
           method /plonecommunity/@@feed-mega-cleanup?days=14
           period 85000
           user zopeuser
           password secret
           host plonecommunity.mobi
        </clock-server>

        <clock-server>
           method /mobipublic/feed-mega-update
           period 3600
           user zopeuser
           password secret
           host mobipublic.com
        </clock-server>

        <clock-server>
           method /mobipublic/@@feed-mega-cleanup?days=14
           period 84000
           user zopeuser
           password secret
           host mobipublic.com
        </clock-server>

        <clock-server>
           method /mobipublic/find-it/events/@@event-cleanup?days=1
           period 84000
           user zopeuser
           password secret
           host mobipublic.com
        </clock-server>


Asynchronous
============

Asyncronous tasks are long-running tasks which are run on their own thread.

lovely.remotetask
-----------------

``lovely.remotetask`` is worked based long-running task manager for Zope 3.

.. TODO:: NO WORKING EXAMPLES HOW TO USE THIS

* `lovely.remotetask package <https://pypi.python.org/pypi/lovely.remotetask>`_ package page

* http://tarekziade.wordpress.com/2007/09/28/a-co-server-for-zope/

* http://swik.net/Zope/Planet+Zope/Trying+lovely.remotetask+for+cron+jobs/c1kfs

* http://archives.free.net.ph/message/20081015.201535.2d147fec.fr.html
