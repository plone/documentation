=================================
Deploy Plone app to Digital Ocean
=================================

.. admonition:: Description

    Since deploying a Plone site might be a challenge for new Plone users, this tutorial aims for solving those difficulties.


Introduction
============

There are many ways to deploy a Plone site. 
However, we sometimes would want to deploy our Plone sites for testing and developing Plone before we can find services that fit our need.
Therefore, this tutorial will show how to deploy Plone on Digital Ocean, 
which is a popular platform for development.

In addition, Digital Ocean is a service that provides VPS and root access for users, 
which makes it very convenient since there are services that do not give full control over the VPS.
Because it is cheap and reliable, we will choose Digital Ocean for our development environment in this tutorial.


Setting up accounts and droplets
================================

First of all, we will need to set up your Digital Ocean account at `Digital Ocean <https://www.digitalocean.com/>`_, 
using our **email** and **email password** to sign up.

After having your account ready, we will need to create a droplet.
A droplet is the way Digital Ocean calls its own Virtual Private Server (VPS). 
Click on the Create Droplet button on the right corner of the screen.

.. image:: /_static/create_droplet.png
    :alt: Create droplet

We will be redicrect to the droplet selection page. 
In here, we need to check the OS for your Droplet. In this tutorial, we choose the Ubuntu 16.04 OS for our VPS.

.. image:: /_static/create_dropletos.png
    :alt: Choose droplet OS

After that, we need to choose the plan for your Droplet. 
Usually, we will use the $10/month since it provides good space for caching.
In addition, this plan also prevents some errors that we might get into while deploying our Plone sites.

.. image:: /_static/create_dropletsize.png
    :alt: Choose droplet size

.. note::
    In case you want to deploy your app using a specific domain name, you can learn how to set it up at `Digital Ocean documentation <https://www.digitalocean.com/community/tutorials/how-to-set-up-a-host-name-with-digitalocean>`_.


Sign in to your Droplet 
=======================

Mac and Linux
-------------

If you are using Mac or Linux environment, you will have to turn on the terminal and type in:

.. code-block:: shell

    ssh root@[your-droplet-ip-adress]

It will ask you to fill in your password. When you created a droplet, an email should be sent to you. 
It contains the password for your droplet. 
Use this password to log in to your droplet through the terminal and change your password.

Windows
-------

On Windows, you will have to download `Putty <http://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>`_.
Run the setup. When you are done, start Putty.
Use your droplet ip address, port 22 and hit enter. It should open a linux terminal for you to fill in your username and password.
Log in to your droplet with the password from the email that you received.

.. image:: /_static/winputty.png
    :alt: Windows putty setup

When you are done, it shold ask you to change the password.


Deploy Plone to VPS
===================

When you are in, make sure that you are at the root directory then
start installing Plone by following the instruction at :doc:`Installing Plone </manage/installing/installation>`.

.. note::
    For deployment on Digital Ocean, you should run the Installer with default installation path, which is /opt/plone

After the installer has successfully installed Plone on our VPS, we will run the buildout and test the server.

.. code-block:: shell

    cd /opt/plone/zinstance
    sudo -u plone_buildout bin/buildout
    ./bin/instance fg

We now can see that our Plone app is running at [your-droplet-id]:8080.
For more information on how to make the app run along with the server, 
follow from step 3 :doc:`Ubuntu Production deployment </manage/deploying/production/ubuntu_production>`.

.. note::
    You will have to replace the path specified in step 3 with your Plone app path. In this case, it should be /opt/plone/zinstance

When you finish step 5, you should have your Plone app running at [your-host-name].com.


Common errors
=============

Cannot install lxml==3.5.0
--------------------------

**Traceback**::

  Getting distribution for 'lxml==3.5.0'.
  x86_64-linux-gnu-gcc: internal compiler error: Killed (program cc1)
  Please submit a full bug report,
  with preprocessed source if appropriate.
  See <file:///usr/share/doc/gcc-5/README.Bugs> for instructions.
  /tmp/easy_install-2kIfB2/lxml-3.5.0/temp/xmlXPathInitjW78Bn.c:2:1: warning: return type defaults to ‘int’ [-Wimplicit-int]
  main (int argc, char **argv) {
  ^
  Building lxml version 3.5.0. 
  Building without Cython.
  Using build configuration of libxslt 1.1.28
  Compile failed: command 'x86_64-linux-gnu-gcc' failed with exit status 4
  error: Setup script exited with error: command 'x86_64-linux-gnu-gcc' failed with exit status 4
  An error occurred when trying to install lxml 3.5.0. Look above this message for any errors that were output by easy_install.
  While:
    Installing instance.
    Getting distribution for 'lxml==3.5.0'.
  Error: Couldn't install: lxml 3.5.0

This error will show up when you use the Unified Installer on the $5/month plan droplet. 
You will need to have the $10/month in order to run the Unified Installer. 
After finishing the setup, you can resize the droplet to 5$/month plan if you want.

The Installer does not generate all the Plone files
---------------------------------------------------

.. image:: /_static/errorDO.png
    :alt: droplet installation error

This error happens when the default installation path in Unified Installer has been modified.

.. note::
    Run the Unified Installer again. But you need to leave the installation path as default. 
