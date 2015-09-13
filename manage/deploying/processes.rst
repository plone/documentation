Starting, stopping and restarting
=================================

If you're using a stand-alone Zope/Plone installation (not a ZEO cluster), starting and stopping Plone is easy.
A production ZEO cluster deployment adds some complexity because you'll now be controlling several process: a ZEO server and several ZEO clients.

If you check the "bin" directory of your buildout after building a cluster, you'll find control commands for the server and each client.
They're typically named zeoserver, client1, client2, client#.
You can do a quick start with the command sequence::

    cd /var/db/your_plone_build
    sudo -u plone_daemon bin/zeoserver start
    sudo -u plone_daemon bin/client1 start
    sudo -u plone_daemon bin/client2 start
    ...

If you've set all this up with the Unified Installer, you'll have a convenience controller script named "plonectl" that will start all your components with one command::

    cd /var/db/your_plone_build
    sudo -u plone_daemon bin/plonectl start

Each "start" command will run the program in "daemon" mode: after a few startup messages, the program will disconnect from the console and run in the background.

The daemon mode start will write a process ID (pid) file in your buildout's "var" directory; that pid may be used to control the background process.
It's automatically used by "stop" and "restart" commands.

Starting and stopping Plone with the server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can start and stop Plone with your server by adding an init.d (Linux and other sys v heritage systems) or rc.d (BSD heritage) script that accepts start and stop commands.

The Unified Installer has an init_scripts directory that contains sample initialization/stop scripts for several platforms.
If you didn't use that installer, you may find the scripts on `github <https://github.com/plone/Installers-UnifiedInstaller/blob/master/init_scripts>`_.

Process control with Supervisor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A much better alternative to custom init scripts is to use a process-control system like `Supervisor <http://supervisord.org/>`_. Supervisor is well-known by the Plone community, and you should have no trouble getting community support for it.
It's available as a package or port on most Linux and BSD systems (look for supervisor, supervisord or supervisor-python).
Installing the port or package will typically activate supervisor.
You then just add the Zope/Plone commands to the supervisor configuration file.

Process-control system's like supervisor typically require the controlled application to run in foreground or console mode.
Don't confuse this with the Zope/Plone "fg" command, which runs the application in debug mode (which is *very* slow).
Instead, use "console" for clients. Use "fg" for the zeoserver; it doesn't have the "console" command, but its performance is unhindered.

Here's a sample program-configuration stanza for supervisor, controlling both a ZEO server and client::

    [program:plone_zeoserver]
    command=/var/db/plone/zeocluster/bin/zeoserver fg
    user=plone_daemon
    directory=/var/db/plone/zeocluster
    stopwaitsecs=60

    [program:plone41_client1]
    command=/var/db/plone41/zeocluster/bin/client1 console
    user=plone_daemon
    directory=/var/db/plone41/zeocluster
    stopwaitsecs=60

Note the "stopwaitsecs" setting. When trying to stop a program, supervisor will ordinarily wait 10 seconds before trying aggressive measures to terminate the process.
Since it's entirely possible for a ZEO client to take longer than this to stop gracefully, we increase the grace period.

When running a ZEO cluster through a process-control system such as supervisor, you should always use the system's own control mechanisms (supervisorctl for supervisor) to start, stop, and status-check cluster components.

Cluster restarts
~~~~~~~~~~~~~~~~

Using multiple ZEO clients and a load balancer makes it possible to eliminate downtime due to ZEO client restarts.
There are many reasons why you might need to restart clients, the most common being that you have added or updated an add-on product. (You should, of course, have tested the new or updated package on a staging server.)

The basic procedure is simple: just restart your clients one at a time with a pause between each restart. This is usually scripted.

Load balancers, however, may raise issues.
If your load balancer does not automatically handle temporary node downtime, you'll need to add to your client restart recipe a mechanism to mark clients as in down or maintenance mode, then mark them "up" again after a delay.

If your load balancer does handle client downtime, you may still need to make sure that it doesn't decide the client is "up" too early.
Zope instances have a "fast listen" mode that causes them to accept HTTP requests very early in the startup process -- many seconds before they can actually furnish a response.
This may lead your load balancer to diagnose the client as "up" and include it in the cluster. This can lead to some very slow responses.
To improve the situation, turn off the "fast listen" mode in your client setup::

    [client1]
    recipe = plone.recipe.zope2instance
    ...
    http-fast-listen = off
    ...

If you are unable to tolerate slow responses during restarts, even this may not be good enough.
Even after a Zope client is able to respond to requests, its first few page renderings will be slow while client database caches are primed.
When speed sensitivity is this important, you'll want to add to your restart script a command-line request (via wget or curl) for a few sample pages.
Do this after client restart and before marking the client "up" in the cluster. This is not commonly required.
