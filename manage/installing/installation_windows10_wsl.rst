================================================================
Installing Plone on a Windows 10 Linux Subsystem for Development
================================================================

A manual for installing a `Plone CLI <https://pypi.org/project/plonecli/>`_ (and Python 3) based development environment into a Windows Linux Subsystem (WSL) under Windows 10.
Ubuntu is used as the Linux distribution.
It is possible to edit the addons created by Plone CLI with an IDE of your choice under Windows.

Introduction
============

The following tutorial will lead you trought all the steps to install and use Plone CLI on your Windows device.

Ubuntu
======

Pre Settings
------------

Before installing the shell to later configure in, the first thing to do is to enable the optional feature for a subsystem on windows.
Therefor, the programm Windows PowerShell has to be launched (as administrator! - right-click the application and choose "launch as admin").
Do not launch the Powershell ISE application, because it won't work.
In the shell the following command has to be entered.

.. code-block :: powershell

    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

If necessary, the device has to be restarted afterwards.

Download And Installing Ubuntu
------------------------------

After giving free the feature for a subsystem, the distribution package of Ubuntu can be downloaded using the following command.

.. code-block :: powershell

    Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile Ubuntu.appx -UseBasicParsing

To install the downloaded package, execute the following command.

.. code-block :: powershell

    Add-AppxPackage .\Ubuntu.appx

Setting Up Ubuntu
-----------------

After installing the application, it can be found in the startmenu or in the apps, or can be found by searching it.
After starting up Ubuntu, it take some time to process futher installation steps and establish the needed components.
An username and password is required, indepentend of the Windows user data.

Because most distributions just deliver an outdated catalog within the download, it is recommended to instantly update the packet.
(You should execute the steps regulary to keep the system up to date).

.. code-block :: console

    sudo apt update && sudo apt upgrade

Windows does not update any components of a Linux subsystem, all have to be carried out manually!

Latest Python On Ubuntu
=======================

Our Linux operating system is installed to author software, so here an explaination how to install the programming language Python.
To install one or more Python versions on the subsystem, a certain management application for it called Pyenv has to be installed.

Install Pyenv
-------------

To install Pyenv, use the command below in the Ubuntu shell.
After completing the download, the shell has to be restarted to take over all changes.

.. code-block :: console

    curl https://pyenv.run | bash

Configure Paths
---------------

To set the right paths for certain activities and enable Pyenv local environment, edit the file ".bashrc" in Ubuntu using the "nano" editor command.

.. code-block :: console

    nano .bashrc

After opening the document, at the end (bottom of code) 3 lines have to be appended:

.. code-block :: bash

    export PATH="$HOME/.pyenv/bin:$HOME/.local/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"

The path is important insofar, because further commands can executed if the paths, where they have to be tapped, are known.
To apply the changes, save the document and activate them by typing the following into the Ubuntu shell.

.. code-block :: console

    source .bashrc

Install Python
--------------

After finishing the setup, it is possible to install the needed version of Python in Ubuntu.
Before installing Python, the system need to be prepared with a C-compiler and some libraries.
To install them, a sudo (superuser do) command (with password, configured when setting up Ubuntu shell) is needed.

.. code-block :: console

    sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

In this case, Python version 3.7.4 is installed.
To use the language version globally, it has to be declared first.

.. code-block :: console

    pyenv install 3.7.4
    pyenv global 3.7.4

Plone CLI
=========

We use Plone CLI here to work with Plone.
Plone CLI is a command line interface for creating Plone packages, as also for building and starting Plone.
Plone CLI need to be installed on the subsystem by typing the following command.

It is installed as a global user-package, so that it can be used for several projects.
Plone CLI's newest release will be pulled immediately.
While at it we install also the latest Pip first.
Pip is a Python package installer.
It pulls released Python packages from the `Python Package Index <https://pypi.org/>`_ and installs them in the current Python environment.

.. code-block :: console

    pip install --upgrade pip
    pip install plonecli --user

Bash Auto Completion
--------------------

To activate the autocomplete function for Plone CLI, again the ``.bashrc`` document has to be opened and a path is inserted ate the bottom of the so far code.

Open editor.

.. code-block :: console

    nano .bashrc

Code to insert.

.. code-block :: bash

    . ~/.local/bin/plonecli_autocomplete.sh

Afterwards, the script has to be applied again.

.. code-block :: console

    source .bashrc

Creating A Plone Add-on
-----------------------

Before creating an add-on, the correct path has to be chosen.

To edit the code under Windows and execute it under Ubuntu with Plone CLI, a shared place accessible from both systems is needed.

Under Ubuntu this location is ``/mnt/c/`` for the Windows C-drive.
I.e. create in Windows a folder ``C:\Plone-Projects`` and in Linux it is located under ``/mnt/c/Plone-Projects``.

Under Ubuntu use the ``cd`` command following with the path chosen to install in.
After entering the path, the add-on can be created.
Plone CLI asks some question to be answered before creating the custom addon.

.. code-block :: console

    cd /mnt/c/Plone-Projects
    plonecli create addon collective.example

Edit and build add-on
---------------------

To add features to the add-on, its directory has to be entered.

.. code-block :: console

    cd /mnt/c/Plone-Projects/collective.example

Then several featuers can be added, for example:

.. code-block :: console

    plonecli add behavior
    plonecli add content_type
    plonecli add theme
    plonecli add view
    plonecli add viewlet
    plonecli add vocabulary

For more information consult the `Plone CLI documentation <https://pypi.org/project/plonecli/>`_.

To build the Plone project some additional libraries have to be installed in the Ubuntu system.

.. code-block :: console

    sudo apt install python3-dev libssl-dev libxml2-dev libxslt1-dev libbz2-dev libjpeg62-dev

After that, the page can be built.

.. code-block :: console

    plonecli build

To start Plone, so that it can be accessed from the webbrowser run:

.. code-block :: console

    plonecli serve

Now, in Windows in your browser of choice got to `http://locahost:8080/ <http://locahost:8080/>`_ and go on creating a Site and use Plone.

To apply future changes to your configuration (buildout), run

.. code-block :: console

    plonecli buildout
