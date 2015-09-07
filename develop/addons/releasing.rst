==================
Releasing an addon
==================

Your addon should be listed and hosted on PyPI if you want other people to use your addon.

.. warning::

    Everything on PyPI is public.
    Be careful not to hard-code passwords in *any* file.


Setup necessary packages
========================

To setup all needed packages you need to run the following command.

.. code-block:: console

    pip install zest.releaser zest.pocompile check-manifest


This takes care of everything you should do:
- Check if all files will be in the package.
- Set the version number
- Tag the release
- Compile any .mo file to .po files
- Make the actual release
- Bump the version.

.. note::

    This installs the packages into your global python installation.
    An alternative would be installing the packages in a :doc:`virtualenv </develop/plone/getstarted/python>`.


Releasing a package
===================

Use the ``fullrelease`` command in the root of your checkout.

.. code-block:: console

        $ fullrelease


.. seealso::

    :doc:`how to use virtualenv controlled non-system wide Python </develop/plone/getstarted/python>`

    Full zest.releaser documentation http://zestreleaser.readthedocs.org/en/latest/

    :doc:`plone.api coding conventions </develop/plone.api/docs/contribute/conventions>`"

    http://opensourcehacker.com/2012/08/14/high-quality-automated-package-releases-for-python-with-zest-releaser/
