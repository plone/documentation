=========================================
Installing add-on packages using buildout
=========================================


.. contents:: :local:


Introduction
------------

Plone uses `Buildout <http://www.buildout.org/>`_ for installing add-on packages.
See :doc:`installation instructions </getstarted/installation>` for
how to create a Plone installation suitable for development.


Discovering Plone add-ons and other python packages
---------------------------------------------------

The `plone.org Products <http://plone.org/products>`_ is a directory
of Plone add-on packages where a lot of add-on packages for Plone are
listed.

A lot more packages can be found in the `PyPI (the Python Package
index) <http://pypi.python.org>`_, although most of the packages might
not be Plone specific.


Installing add-ons using buildout
---------------------------------

Add-on packages which are uploaded to `PyPI <http://pypi.python.org>`_
or `plone.org <http://plone.org/products>`_ as *egg* can be installed
by buildout.

Edit your `buildout.cfg` file and add the add-on package to the list
of eggs:

.. code:: ini

    [buildout]
    ...
    eggs =
        ...
        Products.PloneFormGen
        solgema.fullcalendar

.. note ::

    The above example works for the buildout created by the unified
    installer. If you however have a custom buildout you might need to
    add the egg to the *eggs* list in the *[instance]* section rather
    than adding it in the *[buildout]* section.


For the changes to take effect you need to re-run buildout from your
console:

.. code:: console

    bin/buildout


Restart your instance for the changes to take effect:

.. code:: console

    bin/instance restart


Installing development version of add-on packages
-------------------------------------------------

If you need to use the latest development version of an add-on package
you can easily get the source in your development installation using
the buildout extension `mr.developer
<http://pypi.python.org/pypi/mr.developer>`_.

For managing the sources it is recommended to create a `sources.cfg`
which you can include in your buildout.

.. code:: ini

    [buildout]
    extends = http://plonesource.org/sources.cfg
    extensions = mr.developer

    auto-checkout =
        Products.PloneFormGen
        solgema.fullcalendar

Adding add-on package names to the **auto-checkout** list will make
buildout check out the source to the `src` directory upon next
buildout run.

.. note ::

    It is not recommended to use `auto-checkout = *`, especially when
    you extend from a big list of sources, such as the plonesource.org
    list.

.. note ::

    The `auto-checkout` option only checks out the source. It is also
    required to add the package to the `eggs` list for getting it
    installed, see above.

After creating a `sources.cfg` you need to make sure that it gets
loaded by the `buildout.cfg`. This is done by adding it to the
`extends` list in your `buildout.cfg`:

.. code:: ini

    [buildout]
    extends =
        base.cfg
        versions.cfg
        sources.cfg

As always: after modifying the buildout configuration you need to
rerun buildout and restart your instance:

.. code:: console

    bin/buildout -N
    bin/instance restart
