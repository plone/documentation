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

    cd ~/buildouts # or wherever you want to put things
    git clone -b 5.2 https://github.com/plone/buildout.coredev ./plone5devel
    cd plone5devel
    ./bootstrap.sh
    bin/buildout -c experimental/i18n.cfg
    bin/instance fg

To update the buildout later:

.. code-block:: shell

    git pull
    bin/buildout -c experimental/i18n.cfg

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

Resyncing translations
======================

When an i18n fix is done in the code, you need to regenerate the pot file and resync the po files from this pot file.

There is a *bin/i18n* command to resync the po files for the different i18n domains. `Read more on this doc how to use it <
https://github.com/collective/plone.app.locales/blob/master/utils/README.txt>`_.

To release a new plone.app.locales version, `please read this doc <https://github.com/collective/plone.app.locales/blob/master/utils/RELEASING.rst>`_

Support
=======

Please ask questions on the Plone Community Forum category `Translations and i18n/l10 <https://community.plone.org/c/development/i18nl10n>`_.
