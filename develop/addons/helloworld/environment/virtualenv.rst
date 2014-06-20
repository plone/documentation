======================
Create a virtual_env
======================

.. admonition:: Description

    A simple tutorial introducing the basics of Plone development.

.. contents:: :local:

Now that we have a clean install of Python 2.7 we can move on to the second step in our process, creating the virtual_env.

- Use the virtualenv script from the Build Python section above, create our virtual_env directory.::

    # change your working directory to python_dev
    cd ..
    ./buildout.python/bin/virtualenv-2.7 env-27

This creates the env-27 directory.::

    [michaelc@Cullerton python_dev]$ ll
    total 0
    drwxr-xr-x  16 michaelc  staff  544 Aug 25 20:27 buildout.python
    drwxr-xr-x   5 michaelc  staff  170 Aug 25 20:39 env-27

The virtual_env has its own Python bin, include and lib directories.::

    [michaelc@Cullerton python_dev]$ ll env-27/
    total 0
    drwxr-xr-x  12 michaelc  staff  408 Aug 25 20:39 bin
    drwxr-xr-x   3 michaelc  staff  102 Aug 25 20:39 include
    drwxr-xr-x   3 michaelc  staff  102 Aug 25 20:39 lib

In the bin directory, the virtual_env has 2 copies of Python 2.7; **python** and **python2.7**. It also has easy_install and pip, to install Python packages.::

    [michaelc@Cullerton python_dev]$ ll env-27/bin/
    total 8144
    -rw-r--r--  1 michaelc  staff     2227 Aug 25 20:39 activate
    -rw-r--r--  1 michaelc  staff     1114 Aug 25 20:39 activate.csh
    -rw-r--r--  1 michaelc  staff     2422 Aug 25 20:39 activate.fish
    -rw-r--r--  1 michaelc  staff     1129 Aug 25 20:39 activate_this.py
    -rwxr-xr-x  1 michaelc  staff      368 Aug 25 20:39 easy_install
    -rwxr-xr-x  1 michaelc  staff      376 Aug 25 20:39 easy_install-2.7
    -rwxr-xr-x  1 michaelc  staff      320 Aug 25 20:39 pip
    -rwxr-xr-x  1 michaelc  staff      328 Aug 25 20:39 pip-2.7
    -rwxr-xr-x  1 michaelc  staff  2065616 Aug 25 20:39 python
    -rwxr-xr-x  1 michaelc  staff  2065616 Aug 25 20:39 python2.7

.. Note::

    The bin directory also has an **activate** script you can use to isolate your commands within your virtual_env. It modifies your $PATH so its first entry is the virtualenv's bin/ directory

.. Note::

    Now that we have our virtual_env, we won't use *buildout.python* again for these examples. However, you can return there later to create new virtual environments for other Python projects.::

        # from the **python_dev** directory
        ./buildout.python/bin/virtualenv-2.7 some_other_env-27

    You can also build the versions of Python that we skipped in the Build Python section above, and then use them to build new Python virtual_envs.::

         # from the **python_dev** directory
         ./buildout.python/bin/virtualenv-3.2 some_env-32

For more information about virtualenv, see the `virtualenv documentation <http://www.virtualenv.org/en/latest/index.html>`_ .


