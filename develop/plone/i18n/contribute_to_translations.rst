============================================
How To Contribute To Plone Core Translations
============================================

.. topic:: Description

    How to contribute to the Plone translations.


Introduction
============

You might want to have write access to https://github.com/collective/plone.app.locales to be able to commit your translation directly.

For that, `join the collective GitHub organization <https://collective.github.io/>`_.

You can fork the repository and work from there (more about it below).

Updating Translations
=====================

If you want to test your latest translation with unreleased packages containing i18n fixes,
get the buildout like this:

.. code-block:: shell

    git clone git://github.com/plone/buildout.coredev.git
    cd buildout.coredev
    python2.7 bootstrap.py
    bin/buildout -c experimental/i18n.cfg
    rm .mr.developer.cfg
    ln -s experimental/.mr.developer.cfg
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
- ``locales-addons`` used for some add-ons packages.

Open the po file with `poedit <https://poedit.net/>`_, `kbabel <http://docs.translatehouse.org/projects/localization-guide/en/latest/guide/kbabel.html>`_ or any other i18n tool.

For example for French:

.. code-block:: shell

    poedit locales/fr/LC_MESSAGES/plone.po

Please do a ``git pull`` before editing a po file to be sure you have the latest version.

Committing Directly
-------------------

You can commit your translation from this locales directory:

.. code-block:: shell

    git commit -a -m "Updated French translation"
    git push


Creating A Pull Request
-----------------------

If you do not have commit access on GitHub `collective group <https://github.com/collective>`_,
you can do the following:

- Login to GitHub.
- Go to GitHub `plone.app.locales <https://github.com/collective/plone.app.locales>`_
- Press :guilabel:`Fork`.
  Now GitHub creates a copy of ``plone.app.locales`` package for you.
- Then on your computer in ``plone.app.locales`` do a special git push to your own repository::

    git push git@github.com:YOURUSERNAMEHERE/plone.app.locales.git

- Go to GitHub ``https://github.com/YOURUSERNAME/plone.app.locales``
- Press :guilabel:`Create Pull request`.
  Fill it in.

The request will appear for *plone.app.locales* authors.

If it does not get merged in timely manner, ask on `Plone forums <https://community.plone.org/c/development/i18nl10n>`_.

Support
=======

Please ask questions on the `plone-i18n mailing-list <https://plone.org/support/forums/i18n>`_,
or the `Plone Gitter online chat <https://gitter.im/plone/public>`_.
