============================================
How to contribute to Plone core translations
============================================

.. admonition:: Description

    How to contribute to the Plone translations.

.. contents:: :local:

Introduction
============

You need to have write access to
https://github.com/collective/plone.app.locales to be able to commit
your translation directly.
You can also update a po file online and make a pull request.


Updating translations for Plone 5
=================================

If you want to test your latest translation with unreleased packages
containing i18n fixes for Plone 5, get the buildout like this:

.. code-block:: shell

    git clone -b 5.0 git://github.com/plone/buildout.coredev.git
    cd buildout.coredev
    python2.7 bootstrap.py
    bin/buildout -c experimental/i18n.cfg
    bin/instance fg

To update the buildout later:

.. code-block:: shell

    git pull
    bin/develop up -f

To update your translation, you can go there:

.. code-block:: shell

    cd src/plone.app.locales/plone/app/locales/

Here you have the following directories:

- ``locales`` used for core Plone translations.
- ``locales-addons`` used for some addons packages.

Open the po file with poedit, kbabel or any other i18n tool. For example for
French:

.. code-block:: shell

    poedit locales/fr/LC_MESSAGES/plone.po

Please do a ``git pull`` before editing a po file to be sure you have the latest
version.

Committing directly (commit access)
-----------------------------------

You can commit your translation from this locales directory:

.. code-block:: shell

    git commit -a -m "Updated French translation"
    git push


Creating a pull request (no commit access)
------------------------------------------

If you do not have commit access on GitHub `collective group <https://github.com/collective>`_.
you can do the following:

Login to GitHub. Go to GitHub `plone.app.locales <https://github.com/collective/plone.app.locales>`_

Press *Fork*. Now GitHub creates a copy of ``plone.app.locales`` package for you.

Then on your computer in ``plone.app.locales`` do a special git push to your own repository::

    git push git@github.com:YOURUSERNAMEHERE/plone.app.locales.git

Go to GitHub ``https://github.com/YOURUSERNAME/plone.app.locales``

Press button *Create Pull request*. Fill it in.

The request will appear for *plone.app.locales* authors.
If it does not get merged in timely manner, poke people on the #plone IRC channel
or the mailing list below (sometimes requests go unnoticed).

If you want to resync the po files
==================================

If you want to resync the po files, see the documentation in
src/plone.app.locales/utils/README.txt

Support
=======

Please ask questions on the `plone-i18n mailing-list <https://plone.org/support/forums/i18n>`_.

