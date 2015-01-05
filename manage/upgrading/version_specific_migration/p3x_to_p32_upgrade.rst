=========================================================
Upgrading from 3.x to 3.2
=========================================================


.. admonition:: Description

   Steps for minor upgrades from Plone 3.x to Plone 3.2.

.. contents:: :local:


**Plone 3.2 is the first fully egg-based Plone release.**

Beginning with Plone 3.2, Plone will be available as a Python package and via installers. It will no longer be distributed as a tarball of old-fashioned Zope products. The change to standard Python packaging will improve dependency handling and make future installations easier. But, it will require some adjustments for those used to installing via a tarball of products. The 3.2.x installation will also require some slight changes in the buildout configuration file for those who have already been using buildout configuration management in the 3.x series.

Plone's installers take care of all this for you, but if you aren't using one of the installers you'll need to learn buildout - a Python configuration management tool we highly recommend - or use the Python package installer, easy_install, to install Plone. Both methods are discussed below.


Windows Updates
================

Users of past Windows installers should note: you should not try to simply install on top of your old Windows installation. That might have worked in the past, but it won't work with this upgrade. The move to a buildout-based installer has changed the layout of the subdirectories inside the installation. **Do a new installation, get it working with all required products, then copy your old Data.fs file over the matching file in the new installation.**


Buildout
================

All Plone's current installers use Buildout for configuration management. You should too, unless you're very experienced with Python packages. Buildout is the de facto standard for deploying Zope applications in a repeatable and easy way.  The description of what will be installed is defined by a buildout configuration file, buildout.cfg.
Out of the box, Plone's Unified Installer includes a *buildout.cfg*.

If you're upgrading using buildout for the first time, take a look at :doc:`General advice on updating from a non-buildout to buildout-based installation. </manage/upgrading/non_buildout_to_buildout_upgrade>`

https://plone.org/documentation/manual/upgrade-guide/general-advice-on-updating-from-a-non-buildout-to-buildout-based-installation

If you're updating an existing buildout, please note that the buildout files for 3.2.x look slightly different to those for 3.0 and 3.1 - they don't need a custom plone installation step as buildout can now handle it directly, here's an example of the relevant parts of *buildout.cfg*::

    [buildout]

    # parts: note that the plone part is no longer necessary.
    parts =
        zope2
        instance
        ... Any other parts you've been using except "plone"

    # find-links: only the new dist.plone.org URL is needed.
    find-links =
        http://dist.plone.org/

    # New: this will pick up version settings for all the components.
    # Modify the "3.2.x" to match the version you're seeking, e.g., 3.2.2.
    extends = http://dist.plone.org/release/3.2.x/versions.cfg
    versions = versions

    # eggs: Plone is now specified in the egg section. All the
    # dependencies are automatically handled.
    eggs =
        Plone

    # zope part: Note the new fake-eggs settings. This is required
    # for Zope dependencies to be resolved during buildout.
    [zope2]
    recipe = plone.recipe.zope2install
    url = ${versions:zope2-url}
    fake-zope-eggs = true
    additional-fake-eggs =
        ZConfig
        ZODB3
        pytz

    # Everything else can usually be the same.
    [instance]
    recipe = plone.recipe.zope2instance
    zope2-location = ${zope2:location}
    ...
    # remove any reference to the plone part: e.g., ${plone:eggs} or ${plone:products}


If you have already modified your buildout.cfg file, for example to install new add-ons, remember to copy what you added to the eggs = and zcml = lines into the [instance] section.

If you've installed "old style" products you'll need to copy the productdistros section and add it to parts too.

After doing this, run ``bin/buildout -n``, and your instance should update itself.


Old buildouts
================

There's been a recent change to the fake eggs mechanism that may cause a buildout error unless you delete the "develop-eggs" folder (or just its contents) from your buildout folder. It'll be recreated.


Custom buildout
================

To convert your existing custom buildout to Plone 3.2.x is very easy. The above example should be enough to make it clear what's needed, but in summary:

1. Remove the [plone] section and its entry from parts =. Also, remove all existing ${plone:...} references, including the ones inside the [zope2] and [instance] parts.

2. Add the Plone egg to the eggs specification. Note that "Plone" is capitalized.

3. Copy the extends = and versions = directives from above into your buildout, updating the version number to the target release.

4. Modify the dist.plone.org line in find-links to match the version, as above.

5. Add the two "fake-eggs" specifications above to the zope part specification.


easy_install and virtualenv
================================

If you have special reasons for using a different or no python package manager you can install Plone via easy_install alone. **If you choose this route we highly recommend that you use virtualenv to create an isolated Python instance before proceeding.** Python libraries - and different versions of the same library - often conflict.

Plone is built on-top of the Zope application server and requires it to be installed for you to use Plone.  You can install Plone directly into a python environment using the easy_install utility.::

    easy_install Plone

If you have multiple versions of Python installed you will need to use the easy_install that points to the same Python as your custom Zope install.


Version migration
================================

No matter which technique you use to ugrade your Plone version, you'll need to use the portal_migrations tool in the Zope Management Interface to update your object database. This step is unchanged from past installations; see the general procedure.


A word on warnings
================================

Whenever you run buildout and load new packages that have skin layers, you're likely to receive warnings indicating "'return' outside function." Ignore them, they're harmless. The warnings are produced when Python attempts to compile skin-layer Python scripts, which do indeed contain 'return' outside of function, but run in a context in which this is OK.
