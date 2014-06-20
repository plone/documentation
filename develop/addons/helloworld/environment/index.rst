==============================
Build development environment
==============================

.. admonition:: Description

    A simple tutorial introducing the basics of Plone development.

.. toctree::
   :maxdepth: 1

   python
   virtualenv
   plone

In this tutorial, we build a Python development environment suitable for Plone. The environment should also be useful for any other Python development projects you have.

In these examples, the **python_dev** directory contains our entire development environment. This makes the examples easier, but may not work for everyone. You may need to adapt these examples to fit your situation.

There are 3 main steps in building our development environment; build Python 2.7, create a virtual_env, and install Plone. These correspond to 3 directories in our development environment:

- **buildout.python** sits inside *python_dev*. It contains our build of Python 2.7
- **env-27** sits inside *python_dev*. It is our virtual_env.
- **hello_world** is our Plone installation. It sits inside *env-27*.

The *python_dev* directory can sit anywhere on your filesystem that makes sense.
