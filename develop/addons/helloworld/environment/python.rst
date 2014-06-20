==============
Build Python
==============

.. admonition:: Description

    A simple tutorial introducing the basics of Plone development.

.. contents:: :local:


The first thing we need to do is build Python.

**Buildout** is a tool to manage a software build. It uses configurations so you can always reproduce the same environment. In these examples, we use it to manage both our Python and Plone builds.

For our buildout configuration, we will use **buildout.python**. It is a project on github that maintains configurations for building different versions of Python. We will use it to build Python 2.7.

- Create a directory for your development environment if you don't already have one, and make it your working directory.::

    mkdir python_dev
    cd python_dev

- Get buildout.python from github.

    - If you have git, you can clone the buildout.python repository.::

        git clone https://github.com/collective/buildout.python.git buildout.python

    - You can also download buildout.python from their web interface. Open https://github.com/collective/buildout.python in your browser, and click on the **Downloads** link on the right hand side.

        .. image:: /develop/addons/helloworld/images/buildout_python-web.png

        On the next page, click on **Download as zip** or **Download as tar.gz** to download the buildout files. When the download is complete, uncompress the file and rename the resulting directory to **buildout.python**.

Whether you cloned with git or downloaded from the webiste, you should end up with a directory named **buildout.python** that contains these items.::

    [michaelc@Cullerton python_dev]$ ll buildout.python
    total 56
    -rw-r--r--   1 michaelc  staff   1895 Aug 25 12:28 README.rst
    -rw-r--r--   1 michaelc  staff   4122 Aug 25 12:28 bootstrap-1.4.4.py
    -rw-r--r--   1 michaelc  staff  10107 Aug 25 12:28 bootstrap.py
    -rw-r--r--   1 michaelc  staff    815 Aug 25 12:28 buildout.cfg
    drwxr-xr-x   6 michaelc  staff    204 Aug 25 12:28 docs
    drwxr-xr-x  30 michaelc  staff   1020 Aug 25 12:28 src


- Bootstrap buildout.python with your system Python.::

    cd buildout.python
    python bootstrap.py


This creates the *bin*, *parts*, *eggs*, and *develop-eggs* directories and adds the *buildout* binary to the bin directory.::

    [michaelc@Cullerton buildout.python]$ ll
    total 56
    -rw-r--r--   1 michaelc  staff   1895 Aug 25 13:31 README.rst
    drwxr-xr-x   3 michaelc  staff    102 Aug 25 13:32 bin
    -rw-r--r--   1 michaelc  staff   4122 Aug 25 13:31 bootstrap-1.4.4.py
    -rw-r--r--   1 michaelc  staff  10107 Aug 25 13:31 bootstrap.py
    -rw-r--r--   1 michaelc  staff    815 Aug 25 13:31 buildout.cfg
    drwxr-xr-x   2 michaelc  staff     68 Aug 25 13:32 develop-eggs
    drwxr-xr-x   6 michaelc  staff    204 Aug 25 13:31 docs
    drwxr-xr-x   4 michaelc  staff    136 Aug 25 13:32 eggs
    drwxr-xr-x   2 michaelc  staff     68 Aug 25 13:32 parts
    drwxr-xr-x  30 michaelc  staff   1020 Aug 25 13:31 src

    [michaelc@Cullerton buildout.python]$ ll bin
    total 8
    -rwxr-xr-x  1 michaelc  staff  301 Aug 25 13:32 buildout

The current version of buildout.python builds Python 2.4, 2.5, 2.6, 2.7, 3.2 and 3.3. This can take a long time. We only need Python 2.7.

We can keep buildout from building the other versions by commenting them out in the buildout.cfg file. We do this by adding a **#** to the beginning of a line we want buildout to ignore.

- To only build Python 2.7, open the **buildout.cfg** file in a text editor,  comment out the other versions in both extends and parts sections, and save your changes.::

    [buildout]
    extends =
        src/base.cfg
        src/readline.cfg
        src/libjpeg.cfg
    #     src/python24.cfg
    #     src/python25.cfg
    #     src/python26.cfg
        src/python27.cfg
    #     src/python32.cfg
    #     src/python33.cfg
        src/links.cfg

    parts =
        ${buildout:base-parts}
        ${buildout:readline-parts}
        ${buildout:libjpeg-parts}
    #     ${buildout:python24-parts}
    #     ${buildout:python25-parts}
    #     ${buildout:python26-parts}
        ${buildout:python27-parts}
    #     ${buildout:python32-parts}
    #     ${buildout:python33-parts}
        ${buildout:links-parts}


- Run buildout to build Python.::

    ./bin/buildout

This creates a new python-2.7 directory containing it's own binaries, libraries and include files.::


    [michaelc@Cullerton buildout.python]$ ll
    total 56
    -rw-r--r--   1 michaelc  staff   1895 Aug 25 12:28 README.rst
    drwxr-xr-x   5 michaelc  staff    170 Aug 25 12:44 bin
    -rw-r--r--   1 michaelc  staff   4122 Aug 25 12:28 bootstrap-1.4.4.py
    -rw-r--r--   1 michaelc  staff  10107 Aug 25 12:28 bootstrap.py
    -rw-r--r--@  1 michaelc  staff    835 Aug 25 12:31 buildout.cfg
    drwxr-xr-x   3 michaelc  staff    102 Aug 25 12:30 develop-eggs
    drwxr-xr-x   6 michaelc  staff    204 Aug 25 12:28 docs
    drwxr-xr-x  12 michaelc  staff    408 Aug 25 12:41 eggs
    drwxr-xr-x  10 michaelc  staff    340 Aug 25 12:44 parts
    drwxr-xr-x   5 michaelc  staff    170 Aug 25 12:44 python-2.7
    drwxr-xr-x  32 michaelc  staff   1088 Aug 25 12:44 src

    [michaelc@Cullerton buildout.python]$ ll python-2.7/
    total 0
    drwxr-xr-x  17 michaelc  staff  578 Aug 25 12:44 bin
    drwxr-xr-x   7 michaelc  staff  238 Aug 25 12:44 include
    drwxr-xr-x  11 michaelc  staff  374 Aug 25 12:44 lib

    [michaelc@Cullerton buildout.python]$ ll python-2.7/bin/
    total 8184
    -rw-r--r--  1 michaelc  staff     2228 Aug 25 12:44 activate
    -rw-r--r--  1 michaelc  staff     1115 Aug 25 12:44 activate.csh
    -rw-r--r--  1 michaelc  staff     2423 Aug 25 12:44 activate.fish
    -rw-r--r--  1 michaelc  staff     1129 Aug 25 12:44 activate_this.py
    -rwxr-xr-x  1 michaelc  staff      369 Aug 25 12:44 easy_install
    -rwxr-xr-x  1 michaelc  staff      377 Aug 25 12:44 easy_install-2.7
    -rwxr-xr-x  1 michaelc  staff      230 Aug 25 12:44 pilconvert.py
    -rwxr-xr-x  1 michaelc  staff      228 Aug 25 12:44 pildriver.py
    -rwxr-xr-x  1 michaelc  staff      224 Aug 25 12:44 pilfile.py
    -rwxr-xr-x  1 michaelc  staff      224 Aug 25 12:44 pilfont.py
    -rwxr-xr-x  1 michaelc  staff      226 Aug 25 12:44 pilprint.py
    -rwxr-xr-x  1 michaelc  staff      321 Aug 25 12:44 pip
    -rwxr-xr-x  1 michaelc  staff      329 Aug 25 12:44 pip-2.7
    -rwxr-xr-x  1 michaelc  staff  2065616 Aug 25 12:44 python
    -rwxr-xr-x  1 michaelc  staff  2065616 Aug 25 12:44 python2.7


Buildout also creates the **virtualenv-2.7** script in the bin directory. We will use the *virtualenv-2.7* script in the next tutorial.::

    [michaelc@Cullerton buildout.python]$ ll bin
    total 24
    -rwxr-xr-x  1 michaelc  staff  296 Aug 25 12:41 buildout
    -rwxr-xr-x  1 michaelc  staff  609 Aug 25 12:44 install-links
    -rwxr-xr-x  1 michaelc  staff  155 Aug 25 12:44 virtualenv-2.7


.. Note::

    You can build any of the other versions of Python by uncommenting their lines in the *buidout.cfg* file,::

        [buildout]
        extends =
            src/base.cfg
            src/readline.cfg
            src/libjpeg.cfg
            src/python24.cfg
            src/python25.cfg
            src/python26.cfg
            src/python27.cfg
            src/python32.cfg
            src/python33.cfg
            src/links.cfg

        parts =
            ${buildout:base-parts}
            ${buildout:readline-parts}
            ${buildout:libjpeg-parts}
            ${buildout:python24-parts}
            ${buildout:python25-parts}
            ${buildout:python26-parts}
            ${buildout:python27-parts}
            ${buildout:python32-parts}
            ${buildout:python33-parts}
            ${buildout:links-parts}

    and rerunning buildout.::

        ./bin/buildout

    It just takes a while.


.. Note::

    If you have trouble running buildout, you may need to run the bootstrap step above with the 1.4.4 version.::

        python bootstrap-1.4.4.py
        ./bin/buildout


