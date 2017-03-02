===================================================
Tutorial: Installing Plone for Production on Ubuntu
===================================================

.. admonition:: Description

    A step-by-step guide to installing Plone 5.x on a recent Ubuntu LTS [14.04] server installation.


Introduction
============

This tutorial walks you step-by-step through a minimum responsible installation of Plone for production on a recent Ubuntu LTS server.

The installation includes Plone itself; nginx for a reverse-proxy; a send-only mail-transfer agent; and firewall rules.
We'll set Plone to start with server startup and will add cron jobs to periodically pack the database and create snapshot backups.

This minimal install will work for production for a smaller Plone site, and will provide a good base for scaling up for a larger site.

Requirements
------------

1. A clean installation of a recent Ubuntu server. The tutorial has been tested on cloud and virtual box servers. The install described here will run in 512 MB RAM. More RAM will be needed for larger or busy sites.

2. A hostname for the new site. You or your DNS admin should have already created a hostname (e.g., www.yoursite.com) and a host record pointing to the new server.

3. Unix command-line and basic system administrator skills. You should know how to use `ssh` to create a terminal session with your new server. You should know how to use `vi` or some other terminal editor.

4. An Internet connection.

Step 1: Platform preparation
============================

Get to the point where you can ssh to the server as a non-root user and use `sudo` to gain root permissions.

First step with any new server is to update the already installed system libraries:

.. code-block:: console

    sudo apt-get update
    sudo apt-get upgrade

Then, install the platform's build kit, nginx, and supervisor

.. code-block:: console

    sudo apt-get install build-essential python-dev libjpeg-dev libxslt-dev supervisor nginx

Step 2: Install Plone
=====================

Please take some time and read the chapter about :doc:`installation </manage/installing/installing/index>`.

.. note::

    Note that this is `root` installation `sudo ./install.sh`.
    The installer will create special system users to build and run Plone.

.. note::

    This creates a `zeo` installation with two Plone clients.
    We will only connect one of those clients to the Internet.
    The other will be reserved for debugging and administrator access.
    If you know this is a larger site and wish to use load balancing, you may create more clients with the `--clients=##` command-line argument to create more clients.
    They're also easy to add later.

If you hit an "lxml" error during installation (ie the log shows "Error: Couldn't install: lxml 2.3.6") you may need :doc:`additional libraries </manage/installing/requirements>`.


When the install completes, you'll be shown the preset administrative password.
**Record it !**
If you lose it, you may see it again:

.. code-block:: shell

    sudo cat /usr/local/Plone/zeocluster/adminPassword.txt

Step 3: Set Plone to start with the server
==========================================

We're going to use `supervisor` to start Plone with the server. To do so, we'll create a supervisor configuration file:

.. code-block:: shell

    sudo vi /etc/supervisor/conf.d/plone5.conf

Specify that supervisor should start the database server and client1 automatically::

    [program:plone5server]
    user=plone_daemon
    directory=/usr/local/Plone/zeocluster
    command=/usr/local/Plone/zeocluster/bin/zeoserver fg

    [program:plone5client1]
    user=plone_daemon
    directory=/usr/local/Plone/zeocluster
    command=/usr/local/Plone/zeocluster/bin/client1 console
    stopwaitseconds=30

When that file is saved you're set to start on server start.
To start immediately, tell supervisor about the new components:

.. code-block:: shell

    sudo supervisorctl
    supervisor> reread
    supervisor> add plone5server
    plone5server: added process group
    supervisor> add plone5client1
    plone5client1: added process group
    supervisor> status
    plone5client1                    RUNNING    pid 32327, uptime 0:00:02
    plone5server                     RUNNING    pid 32326, uptime 0:00:08

Step 4: Create a Plone site
===========================

At this point, you should be able to open a web browser and point it to port 8080 on your new server.
Do so, and use your administrative password to create a Plone site with the id "Plone".
(Feel free to use a different ID, just remember it below when you set up virtual hosting rules.)

Step 5: Set up virtual hosting
==============================

We're going to use nginx as a reverse proxy. Virtual hosting will be established by rewrite rules.
You need two bits of information: 1) the hostname you want to use (for which DNS records should already be set up); 2) the id of the Plone site you created.

We'll set up nginx by adding a new configuration file:

.. code-block:: shell

    sudo vi /etc/nginx/sites-available/plone5.conf

Add the contents

.. code-block:: ini

    server {
      server_name www.yourhostname.com;
      listen 80;

      location / {
        rewrite ^/(.*)$ /VirtualHostBase/http/www.yourhostname.com:80/Plone/VirtualHostRoot/$1 break;
        proxy_pass http://localhost:8080;
      }
      location ~* manage_ {
        deny all;
      }
    }

    server {
      server_name yourhostname.com;
      listen 80;
      access_log off;
      rewrite ^(/.*)$  http://www.yourhostname.com$1 permanent;
    }

And save.

.. note::

    The `location ~* manage_` rule will deny access to most of the Management interface.
    (You'll get to that by bypassing nginx.)

.. note::

    The second server stanza sets up an automatic redirect that will transfer requests for the bare hostname to its `www.` form.
    You may not want or need that.

Enable the new nginx site configuration:

.. code-block:: shell

    cd /etc/nginx/sites-enabled
    sudo ln -s /etc/nginx/sites-available/plone5.conf

And, tell nginx to reload the configuration:

.. code-block:: shell

    sudo service nginx configtest
    sudo service nginx reload

Try out your virtual hosting.

Step 6: Set up packing and backup
=================================

We want the Zope database to be packed weekly. We'll do so by setting up a `cron` job:

.. code-block:: shell

    sudo vi /etc/cron.d/zeopack

Add the contents::

    57 22 * * 5 plone_daemon /usr/local/Plone/zeocluster/bin/zeopack

And save.

.. note::

    Pick a time when your system can take some extra load. Don't use the day/time above.

Let's also create a daily snapshot of the database:

.. code-block:: shell

    sudo vi /etc/cron.d/plonebackup

Add the contents below, adjust the time, and save::

    37 0 * * * plone_daemon /usr/local/Plone/zeocluster/bin/snapshotbackup

.. note::

    This snapshot will give you a stable copy of the database at a particular time.
    You'll need a separate strategy to backup the server's file system, including the snapshot.

Step 7: Add a send-only Mail Transfer Agent
===========================================

You don't need this step if you have an MTA on another server, or are using a mail-send service.
If you don't have that available, this step will create a localhost, port 25, MTA that you may use with Plone's mail setup.

We're going to use Postfix. There are lots of alternatives.

Add the Postfix package and edit its main configuration file:

.. code-block:: shell

    sudo apt-get install postfix
    sudo vi /etc/postfix/main.cf

Change the bottom section to turn off general mail in::

    myhostname = www.yourhostname.com
    alias_maps = hash:/etc/aliases
    alias_database = hash:/etc/aliases
    myorigin = yourhostname.com
    mydestination =
    relayhost =
    mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
    mailbox_size_limit = 0
    recipient_delimiter = +
    inet_interfaces = loopback-only

Tell postfix to restart:

.. code-block:: shell

    sudo /etc/init.d/postfix restart

Step 8: Set up a firewall
=========================

You *must* set up a firewall.
But, you may be handling that outside the system, for example via AWS security groups.

If you want to use a software firewall on the machine, you may use `ufw` to simplify rule setup.

.. code-block:: shell

    sudo apt-get install ufw
    sudo ufw limit 22/tcp
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw enable

.. note::

    This blocks everything but SSH and HTTP(S).

You may be wondering, how do you do Management Interface administration?
SSH port forwarding will allow you to build a temporary encrypted tunnel from your workstation to the server.

Execute on your workstation the command:

.. code-block:: shell

    ssh yourloginid@www.yourhostname.com -L:8080:localhost:8080

Now, ask for http://localhost:8080/ in your workstation web browser, and you'll be looking at the Management Interface.

Scaling up
==========

This installation will do well on a minimum server configuration (512MB RAM).
If you've a larger site, buy more memory and set up reverse-proxy caching and load balancing.

:doc:`Deploying and installing Plone in production </manage/deploying/index>` is a good introduction to scaling topics.
