Installation and Bootstrapping
==============================


Normal Installation
-------------------

The normal way to install `Mockup` is to directly install it to your system,
using the system's `Node` version and other tools. If this is not possible,
because you are using Windows or don't want to pollute your System with
libraries not necessarily needed, use the :ref:`vagrant_installation` method.

Prerequisites
~~~~~~~~~~~~~

To build and hack on Mockup you will need recent versions of ``git``, ``node``,
``npm``, ``PhantomJS`` and ``make``.

- Installing Node: You need to have Node 0.10 or newer. Normally, NPM is
  installed together with node. For installation instructions see `Installation
  via package manager
  <https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager>`_
  or `Building Node <https://github.com/joyent/node/wiki/Installation>`_.

- Installing PhantomJS: Use your package manager or `download and
  install <http://phantomjs.org/download.html>`_).

.. note::
    There is a useful tool, which helps you to install different versions of
    Node, if you need it. The `Node Version Manager
    <https://github.com/creationix/nvm>`_, ``nvm``. Try it, if you run into
    problems with your system's Node version.

Right now development of this project is being done primarily on Linux and OS X,
so setting up the tooling on MS Windows might be an adventure for you to explore --
though, all of the tools used have equivalent versions for that platform,
so with a little effort, it should work!


Installing Mockup
~~~~~~~~~~~~~~~~~

Installing `Mockup` is as easy as cloning and then running `make bootstrap`::

    $ git clone https://github.com/plone/mockup.git
    $ cd mockup
    $ make bootstrap

This bootstraps the whole application. It cleans up the directory and installs
node and bower dependencies.


.. _vagrant_installation:

Installing Mockup with Vagrant
------------------------------

Vagrant is a scripting environment for virtual machine hosts like VirtualBox.
There are two configuration files, ``Vagrantfile`` and ``provision.sh`` which
are used to bootstrap a whole system including any dependencies, which should
be installed on the guest system.

Vagrant can be a great choice, if you don't want to install Mockup and its
dependencies directly to your machine, possibly polluting your environment
(but normally, Mockup doesn't install anything globally). Vagrant is also a
great choice, if you want to provide the same environment for every developer.
Therefore we chose it as the recommended installation method for our Mockup
training.

With this method, Mockup is installed by installing a virtual machine with
Vagrant by using the ``Vagrantfile`` and ``provision.sh`` files, which are
included in Mockup. A guest VM (Ubuntu 14.04) is started with the Vagrantfile
and provisioned with Mockup prerequisites. Then a bootstrap script is run on
the guest VM. Follow these steps:

1. Install VirtualBox: https://www.virtualbox.org. Use your system's package
   manager, if you have one. 

2. Install Vagrant: http://www.vagrantup.com. If you have such a thing
   like a system package manager, I recommend to use it only, if it includes a
   recent version of Vagrant.

3. If you are using Windows, install the Putty ssh kit:
   http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html. Install all
   the binaries, or at least putty.exe and plink.exe.


Now we can install Mockup itself:

.. code-block:: bash

    $ # Run the following on the host OS:
    $ git clone https://github.com/plone/mockup.git
    $ cd mockup
    $ vagrant up

Now, go for lunch or a long coffee break. "vagrant up" is going to download a
virtual box kit (unless you already happen to have a match Windows, it will
also generate an ssh key pair that's usable with Putty.

.. note::
    While running "vagrant up", feel free to ignore messages like "stdin: is
    not a tty" and "warning: Could not retrieve fact fqdn". They have no
    significance in this context.

Look to see if the install ran well. The virtual machine should be running at
this point:

.. code-block:: bash

    $ vagrant reload
    $ vagrant ssh


Now you are logged into your virtual machine:

.. code-block:: bash

    $ # Run the following on the guest VM:
    $ cd /vagrant
    $ git pull
    $ make bootstrap

Now you have the complete source code for all Patterns from Mockup.
From here on you generate bundles of common functionality and minify them.

You're ready to start working on testable, modular and beautiful JavaScript!

.. note::
    Parts of this instructions are based on the `plonedev.vagrant README.rst
    <https://github.com/plone/plonedev.vagrant/blob/master/README.rst>`_. Have
    a look for it, if you need more information and troubleshooting
    instructions.


Using Vagrant
~~~~~~~~~~~~~

Understanding Vagrant in depth is out of this document scope. The most
important commands for using vagrant are listed below.

- ``vagrant up``

    This command will start the virtual environment. When running it for the first
    time it will install and configure all needed packages.  NOTE: Some of the
    output will be in red, this is normal.

- ``vagrant reload``

    This command will make the virtual environment restart. You need to do
    this the first time

- ``vagrant ssh``

    Once the virtual environment is up and running, this command will ssh into
    the machine. This is like ssh'ing into any computer, all you need to do to
    exit is "Ctrl + D"

- ``vagrant halt``

    This command will turn off the virtual machine, issuing an ACPI shutdown,
    so it's safe to use it at any time.

- ``vagrant destroy``

    This command will destroy the virtual environment. Be aware that this will
    remove the entire virtual machine. Be careful and know when you're using
    it.

For additional reading, go to `Vagrant homepage <https://www.vagrantup.com/>`_.
