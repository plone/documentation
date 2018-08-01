==========================
Automatic Plone (re)starts
==========================


Introduction
============

Tips on how to automatically start Plone on server boot.

This manual assumes that you have installed Plone via the Unified-Installer as ``root install``.

If you used a different installation method, please adjust the examples below to your own needs. For example, the user as which you run Plone may be different.

plonectl script
===============

The general-purpose ``plonectl`` control command for Plone installations is:

.. code-block:: sh

    yourbuildoutfolder/bin/plonectl

``yourbuildoutfolder`` is the topmost folder of your Plone installation.
It will always contain a ``buildout.cfg`` file and a ``bin`` directory.

The ``plonectl`` command is a convenience script that controls standalone or cluster configurations.
In a standalone installation, this will restart the ``instance`` part.
In a ZEO cluster install, it will restart the zeoserver and client parts.

If you have installed Plone in production mode, the Plone server components are meant to be run as a special user, usually ``plone_daemon``. (In older versions, this was typically ``plone``.) In this case, the start, stop, and restart commands are:

.. code-block:: sh

    # start
    sudo -u plone_daemon bin/plonectl start
    #
    # stop
    sudo -u plone_daemon bin/plonectl stop
    #
    # restart
    sudo -u plone_daemon bin/plonectl restart

Starting on boot
================

It is best practice to start Plone service if the server is rebooted.
This way your site will automatically recover from power loss and other causes.

On a Linux or BSD system, you have two major alternatives to arrange automatic starting for a production install:

1. A process control system, like supervisor.

2. Through ``init.d`` (BSD ``rc.d``) scripts.

Using supervisor
----------------

`supervisor <http://supervisord.org/>`_ is a general-purpose process control system that is well-known and highly recommended in the Plone community.

Process control systems generally run their controlled programs as subprocesses.
This means that the controlled program must not detach itself from the console (daemonize).

Zope/Plone's ``start`` command does not work for this purpose.
Instead use ``console``.
Do not use ``fg``, which turns on debug switches that will dramatically slow your site.

Supervisor is well-documented, easy to set up, and included as an installable package with popular Linux and BSD distributions.

Debian LSBInitScripts
---------------------

The following section describes how to make an Init Script LSB.

This example will start a Plone site on boot:

.. code-block:: sh

   #!/bin/sh
   ### BEGIN INIT INFO
   # Provides:          start_plone.sh
   # Required-Start:    $remote_fs $syslog
   # Required-Stop:     $remote_fs $syslog
   # Should-Start:      my plone site
   # Default-Start:     2 3 4 5
   # Default-Stop:      0 1 6
   # Short-Description: Start plone at boot time
   # Description:       Start my plone site at boot time
   #
   #
   #
   #
   ### END INIT INFO

   su - plone_daemon -c "/usr/local/Plone/zeocluster/bin/plonectl start"

Save this script as ``start_plone.sh`` in ``/etc/init.d`` and make it executable.

Add the script to dependency-based booting:

.. code-block:: sh

    insserv start_plone.sh

Where ``start_plone.sh`` is an executable init script placed in ``/etc/init.d``,
``insserv`` will produce no output if everything went OK. Examine the error code in ``$?`` if you want to be sure.

This is another example (``/etc/init.d/plone``):

.. code-block:: sh

    #!/bin/sh

    ### BEGIN INIT INFO
    # Provides:          plone
    # Required-Start:    $syslog $remote_fs
    # Required-Stop:     $syslog $remote_fs
    # Should-Start:      $remote_fs
    # Should-Stop:       $remote_fs
    # Default-Start:     2 3 4 5
    # Default-Stop:      0 1 6
    # Short-Description: Start plone instances
    # Description:       Start the instances located at /srv/Plone/zeocluster/bin/plonectl
    ### END INIT INFO

    PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

    [ -f /usr/local/Plone/zeocluster/bin/plonectl ] || exit 0

    DAEMON=/usr/local/Plone/zeocluster/bin/plonectl
    NAME="plone "
    DESC="daemon zeoserver & client"

    . /lib/lsb/init-functions

    case "$1" in
        start)
            log_daemon_msg "Starting $DESC" "$NAME"
            if start-stop-daemon --quiet --oknodo --chuid plone:plone \
                                 --exec ${DAEMON} --start start
            then
                log_end_msg 0
            else
                log_end_msg 1
            fi
            ;;

        stop)
            log_daemon_msg "Stopping $DESC" "$NAME"
            if start-stop-daemon --quiet --oknodo --chuid plone:plone \
                                 --exec ${DAEMON} --start stop
            then
                log_end_msg 0
            else
                log_end_msg 1
            fi
            ;;

        restart)
            log_daemon_msg "Restarting $DESC" "$NAME"
            if start-stop-daemon --quiet --oknodo --chuid plone:plone \
                                 --exec ${DAEMON} --start restart
            then
                log_end_msg 0
            else
                log_end_msg 1
            fi
            ;;

        status)
            start-stop-daemon --chuid plone:plone \
                                --exec ${DAEMON} --start status
            ;;

        force-reload)
            echo "Plone doesn't support force-reload, use restart instead."
            ;;

        *)
            echo "Usage: /etc/init.d/plone {start|stop|status|restart}"
            exit 1
            ;;
    esac

    exit 0

Make sure to read:

https://wiki.debian.org/LSBInitScripts

Upstart
-------
Upstart is an event-based replacement for the ``/sbin/init`` daemon which handles starting of tasks and services during boot, stopping them during shutdown, and supervising them while the system is running.
It was originally developed for the Ubuntu distribution, but is intended to be suitable for deployment in all Linux distributions as a replacement for the venerable System-V init.

Example of a ``plone.conf`` file in ``/etc/init/`` -> ``/etc/init/plone.conf``:

.. code-block:: sh

        # Plone - Web-Content Management System
        #
        # Based on Python and ZOPE

        description "start plone"
        author "Josh Sehn based on previous work by Christoph Glaubitz"
        version "0.3"

        console none
        respawn

        start on (local-filesystems and net-device-up and runlevel [2345])
        stop on runlevel [!2345]

        exec sudo -u plone_daemon /usr/local/Plone/zeocluster/bin/plonectl start

Make sure to read: http://upstart.ubuntu.com/

Also check the original source of this sample file: http://chrigl.de/posts/2011/11/10/my-plone-configuration.html

The above sample has not been extensively tested and is intended for use in a zeocluster configuration.
To use the above sample for a normal (non-root) user installation, replace the last line with:

.. code-block:: sh

        exec /home/$USERID/Plone/plonectl start

Systemd
-------
Create a services file ``plone.service`` in ``/etc/systemd/system``:

.. code-block:: ini

    [Unit]
    Description=Plone content management system
    After=network.target

    [Service]
    Type=forking
    ExecStart=/usr/local/Plone/zeocluster/bin/plonectl start
    ExecStop=/usr/local/Plone/zeocluster/bin/plonectl stop
    ExecReload=/usr/local/Plone/zeocluster/bin/plonectl restart

    [Install]
    WantedBy=multi-user.target

Make ``systemd`` aware of it:

.. code-block:: sh

    systemctl daemon-reload

Activate a service immediately:

.. code-block:: sh

    systemctl start plone.service

Check status of a service:

.. code-block:: sh

    systemctl status plone.service

Enable a service to be started on bootup:

.. code-block:: sh

    systemctl enable plone.service

More detailed log information:

.. code-block:: sh

    systemd-journalctl -a

Make sure to read: https://www.freedesktop.org/wiki/Software/systemd/


Crontab
-------

These instructions apply for Debian-based Linuxes.

Example crontab of *yourploneuser*:

.. code-block:: console

    @reboot /usr/local/Plone/zeocluster/bin/plonectl start

``rc.local`` script
-------------------

For Debian-based Linuxes, add the following line to the ``/etc/rc.local`` script:

.. code-block:: sh

    /usr/local/Plone/zeocluster/bin/plonectl restart
