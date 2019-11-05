=========================================
Installing add-on packages using buildout
=========================================

These instructions cover add-on installation process for Plone 5, while mostly being valid for Plone 4 and 3.3 as well.
Legacy systems are not covered in these instructions.

.. note::

   Not all add-ons have currently (status: 2015-10-31) been upgraded to work with Plone 5. Take care when trying on add-ons. If an add-on has not yet received a Plone 5-compatible release, it may be that there is already a so-called 'branch' of the sourcecode that is being worked upon, or it may be that the add-on has been superseded. See the "further help" section.


Introduction
------------

Plone uses `Buildout <http://www.buildout.org/>`_ for installing add-on packages.
See :doc:`installation instructions </manage/installing/installation>` for how to create a Plone installation suitable for development.

Prerequisites
-------------

What do you need to know in order to install add-ons for Plone?

- How to use command line of your operating system.
  This is a hard requirement - you cannot achieve your goal unless you know how to interact with the command line.
  Here are basics tutorials for `Windows <http://www.hacking-tutorial.com/tips-and-tricks/16-steps-tutorial-basic-command-prompt/>`_ and `Linux <http://linuxcommand.org/learning_the_shell.php>`_
- Working with plain text based configuration files and editing them with a text editor like Notepad
- First create a :doc:`development / back-up copy </manage/deploying/copy>` of your site. Never install to the working production server directly, without first testing the add-on on a test instance.


Discovering Plone add-ons and other python packages
---------------------------------------------------

The community maintains a list of Popular Plone `Add-ons <https://plone.org/download/add-ons/>`_ .

However, not all Plone packages out there are listed here.

A lot more packages can be found in the `PyPI (the Python Package index) <https://pypi.python.org/pypi?:action=browse&show=all&c=518>`_.

.. note::

   Always check if a third-party add-on is up to date and compatible with your version of Plone.
   Most packages will have different versions; sometimes their version 1.x is meant for use with Plone 4, and version 2.x is meant for Plone 5.
   See the documentation of the add-on in question.


Background
----------

Plone installations are managed using :term:`Buildout`.
Plone add-ons are distributed as Python modules, also known as eggs.

- Popular Plone `Add-ons <https://plone.org/download/add-ons/>`_ contains a overview about popular add-ons for `Plone <https://plone.org>`_ .
- Add-on file downloads are hosted on the `PyPi Python package repository <https://pypi.python.org/pypi>`_ - along with many other Python software modules.
- the buildout.cfg file in your Plone configuration defines which add-ons are available for your sites to install in Site Setup > Add-ons control panel
- the bin/buildout command (or bin/buildout.exe on Windows) in your Plone installation reads buildout.cfg and automatically downloads required packages when run - you do not need to download any Plone add-ons manually
- Plone site setup -> Add ons control panel defines which add-ons are installed for the current Plone site (remember, there can be many Plone sites on a single Zope application server)

.. note::

    Plone add-ons, though Python eggs, must be installed through buildout as only buildout will regenerate the config files reflecting newly downloaded and installed eggs. Other Python installation methods like easy_install and pip do not apply for Plone add-ons.


Installing add-ons using buildout
---------------------------------

Add-on packages which are uploaded to `PyPI <https://pypi.python.org>`_ can be installed by buildout.

Edit your `buildout.cfg` file and add the add-on package to the list
of eggs:

.. code:: ini

    [buildout]
    ...
    eggs =
        ...
        Products.PloneFormGen
        collective.supercool

.. note::

    The above example works for the buildout created by the unified installer.
    If you however have a custom buildout you might need to add the egg to the *eggs* list in the *[instance]* section rather than adding it in the *[buildout]* section.


For the changes to take effect you need to re-run buildout from your console:

.. code:: console

    bin/buildout


Restart your instance for the changes to take effect:

.. code:: console

    bin/instance restart



Pinning add-on versions
-----------------------

As mentioned above, always make sure to test add-ons, and see if you have the right version for your specific version of Plone.

It is **standard, and highly recommended practice** to pick specific versions of add-ons. This practice is called "pinning".

If you don't *pin* a specific version, a run of ``bin/buildout`` might download a newer version of an add-on, that in turn might depend on newer other software. This can lead to breakage of your site.

Therefore, always put the specific version number of the add-on into the section of buildout.cfg called "versions", or into the separate file "versions.cfg" if your buildout has one.
An example of version-pinning would be to have:

.. code:: ini

    [versions]
      Products.PloneFormGen = 1.7.17
      collective.supercool = 2.3

When :doc:`upgrading add-ons </manage/upgrading/addon_upgrade>` also don't just upgrade to an unspecified 'newest' version, but to a specific newer version that you have previously tested.


Installing development version of add-on packages
-------------------------------------------------

If you need to use the latest development version of an add-on package you can get the source in your development installation using the buildout extension `mr.developer <https://pypi.python.org/pypi/mr.developer>`_.

'mr.developer' can install, or *checkout* from various places: github, gitlab, subversion, private repositories etcetera.
You can pick specific tags and branches to checkout.

For managing the sources it is recommended to create a `sources.cfg` which you can include in your buildout.

.. code:: ini

    [buildout]
    extends = http://plonesource.org/sources.cfg
    extensions = mr.developer

    auto-checkout =
        Products.PloneFormGen
        collective.supercool

Adding add-on package names to the **auto-checkout** list will make buildout check out the source to the `src` directory upon next buildout run.

.. note::

    It is not recommended to use `auto-checkout = *`, especially when you extend from a big list of sources, such as the plonesource.org list.

.. note::

    The `auto-checkout` option only checks out the source.
    It is also required to add the package to the `eggs` list for getting it installed, see above.

After creating a `sources.cfg` you need to make sure that it gets loaded by the `buildout.cfg`.
This is done by adding it to the `extends` list in your `buildout.cfg`:

.. code:: ini

    [buildout]
    extends =
        base.cfg
        versions.cfg
        sources.cfg

As always: after modifying the buildout configuration you need to rerun buildout and restart your instance:

.. code:: console

    bin/buildout -N
    bin/instance restart


Further help
-------------

More detailed instructions for installing Plone add-ons are available for dealing with legacy systems.

To ask if a particular add-on has already been updated to Plone 5, you can go to `community.plone.org <https://community.plone.org>`_


Please visit the  :doc:`help asking guidelines</askforhelp>` and `Plone support <https://plone.org/support>`_ options page to find further help if these instructions are not enough.
Also, contact the add-on author, as listed on Plone product page, to ask specific instructions regarding a particular add-on.
