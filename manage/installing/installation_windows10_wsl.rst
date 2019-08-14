Installing a Linux Subsystem with Plonecli on Windows 10 Home
=============================================================

A tutorial for installing Plonecli (and Python) into a linux subsystem on windows using an ubuntu shell

Introduction
============

The following tutorial will lead you trought all the steps to install and use Plonecli on your Windows device.

Ubuntu
======

Pre settings
------------

Before installing the Shell to later configure in, the first thing to do is to enable the optional feature for a subsystem on windows.
Therefor, the programm Windows PowerShell has to be launched (as admin! - right-click the application and choose "launch as admin"). Do not launch the Powershell ISE application, because it won't work.
In the Shell the following command has to be entered.

.. code: powershell

    $ Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

If necessary, the device has to be restarted afterwards.

Download and Installing Ubuntu
------------------------------

After giving free the feature for a subsystem, the distribution package of Ubuntu can be downloaded using the following command.

.. code powershell

    $ Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile Ubuntu.appx -UseBasicParsing

To install the downloaded Data, so that it can be launched, it has to be added by the follwogin command.

.. code powershell

    $ Add-AppxPackage .\Ubuntu.appx

Setting up Ubuntu
-----------------

After installing the application, it can be found in the startmenu or in the apps, or just be found by searching it.
After starting Ubuntu up, some time has to pass so that it can install and establish the needed components.
An username and password is required, indepentend of the Windows user data.

Because most distributions just deliver a small packetcatalog within the download, it is recommended to instantly update the packet.
(And if possible regularly).

.. code: console

    $ sudo apt update && sudo apt upgrade

Windows does not update any components of a linux subsystem, all have to be carried out manually!

Pyenv (used for Python) on Ubuntu
================

Almost every single Linux operating system is installed to write a program, so here an explaination how to install for example the programming language Python.
To install one or more Python versions on the subsystem, a certain management application for it called pyenv has to be established.

install Pyenv
-------------

To install pyenv, use the following command in the Ubunut shell. 
After completing the download, the shell has to be restarted in order to take over all changes of paths and included.

.. code: console

    $ curl https://pyenv.run | bash

configure Paths
---------------

One of the now donwloaded documents has to be configured after, in order to set the right paths for certain activities.
The document ".bashrc" can be opened in Ubuntu using the "nano" command.

.. code: console

    $ nano .bashrc

After opening the document, at the end (Bottom of code) 3 lines have to be added.

.. code: bash

    export PATH="$HOME/.pyenv/bin:$HOME/.local/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"

The path is important insofar, because further commands can only be taken out if the paths, where they have to be tapped, are known.
To apply the changes, save the document and activate them by typing the following into the Ubuntu shell.

.. code: console

    $ source .bashrc

install Python
--------------

After finishing the setup, it is possible to install any version of Python in the shell.
Before installing Python, the system has to know a description of the libraries, therefore a sudo command (with password, configured when setting up Ubuntu shell) is needed.

.. code: console

    sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

In this case, version 3.7.4 is installed. In order to use the language gloablly, it has to be released.

.. code: console

    $ pyenv install 3.7.4

.. code: console

    $ pyenv global 3.7.4

Plonecli
========

Plonecli can be installed on the subsystem by typing the following command. It is installed over the global user-package, so that it can be used in several projects.
Plonecli should be pulled on newest release immediately.

.. code: console

    $ pip install plonecli --user 

.. code: console

    $ pip install --upgrade pip

Bash auto completion
--------------------

To activate the autocomplete function for plonecli, again the .bashrc document has to be opened and a path is inserted ate the bottom of the so far code.
Afterwards, the document has to be applied again.

.. code: console

    $ nano .bashrc

.. code: bash

    $ . ~/.local/bin/plonecli_autocomplete.sh

.. code: console

    $ source .bashrc

Create a plone add-on
---------------------

Before creating an add-on, the correct path has to be chosen. There for type the "cd" command following with the path to be wished to install in.
After chosing the path, the add-on can be created.
Some formal data has to be filled in for the creation.

.. code: console

    $ cd /{PATH}/

.. code: console

    $ plonecli create addon kup.internship

Edit and build add-on
---------------------

To add features to the add-on, its directory has to be opened.

.. code: console

    $ cd /{DIRECTORY/

Then several featuers can be added, for example:

.. code: console

    $ plonecli add behavior
    $ plonecli add content_type
    $ plonecli add theme
    $ plonecli add view
    $ plonecli add viewlet
    $ plonecli add vocabulary

To make it possible to compile for example the documents written in the language "C" and create certain libraries, this command has to be entered before building the package.

.. code: console

    $ sudo apt install python2.7 python2.7-dev python-setuptools python-dev build-essential libssl-dev libxml2-dev libxslt1-dev libbz2-dev libjpeg62-dev

After that, the page can be builded and served, so that it can be accessed from the webbrowser.

.. code: console

    $ plonecli build

.. code: console

    $ plonecli serve







