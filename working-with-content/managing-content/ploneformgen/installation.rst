=======================
Installing PloneFormGen
=======================

.. admonition:: Description

    PloneFormGen is a Plone add-on product, and is not included with Plone. Fortunately, it's easy to install.

PFG installs just like most other Plone add ons. Edit the buildout.cfg file at the top of your Plone instance and look for the ``eggs =`` section that specified Python Packages that you with to include. Add PloneFormGen:

.. code-block:: ini

    eggs =
        Plone
        ...
        Products.PloneFormGen

Run bin/buildout and restart your Plone instance. Dependencies will be loaded automatically.

After restarting Plone, visit your site-setup page and use the "add on" configuration page to activate PloneFormGen.
