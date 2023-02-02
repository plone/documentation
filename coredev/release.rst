.. -*- coding: utf-8 -*-

=========================
The Plone release process
=========================


Release process for Plone packages
==================================

To keep the Plone software stack maintainable, the Python egg release process must be automated to high degree.
This happens by enforcing Python packaging best practices and then making automated releases using the `zest.releaser <https://github.com/zestsoftware/zest.releaser/>`_  tool.

This is extended with Plone coredev specific features by `plone.releaser <https://github.com/plone/plone.releaser>`.

* Anyone with necessary PyPi permissions must be able to make a new release by running the ``fullrelease`` command

... which includes ...

* All releases must be hosted on PyPi

* All versions must be tagged at version control

* Each package must have README.rst with links to the version control repository and issue tracker

* CHANGES.rst (docs/HISTORY.rst respectively .txt in some packages) must be always up-to-date and must contain list of functional changes which may affect package users.

* CHANGES.rst must contain release dates

* README.rst and CHANGES.rst must be visible on PyPI

* Released eggs must contain generated gettext .mo files,
  but these files must not be committed to the repository.
  The .mo files can be created with the ``zest.pocompile`` add-on,
  which should be installed together with ``zest.releaser``.

* ``.gitignore`` and ``MANIFEST.in`` must reflect the files going to egg (must include page template, po files)

More information:

* `High quality automated package releases for Python with zest.releaser <http://opensourcehacker.com/2012/08/14/high-quality-automated-package-releases-for-python-with-zest-releaser/>`_.


Special packages
================

The Plone Release Team releases the core Plone packages.
Several others also have the rights to release individual packages on https://pypi.python.org.
If you have those rights on your account, you should feel free to make releases.

Some packages need special care or should be done only by specific people as they know what they are doing.
These are:

``Products.CMFPlone``, ``Plone``, and ``plone.app.upgrade``:
  Please leave these to the release manager, Eric Steele.

``plone.app.locales``:
  Please leave this to the i18n team lead, Vincent Fretin.


Plone core release process checklist
====================================

1. Check Jenkins Status

Check latest Plone coredev job on jenkins.plone.org, it should be green, if it is not, fix the problem first.

2. Check out buildout.coredev

::

  git clone git@github.com:plone/buildout.coredev.git
  cd buildout.coredev
  git checkout 5.1
  python bootstrap.py
  bin/buildout -c buildout.cfg

3. Check Packages for Updates

Check all packages for updates, add to/remove from checkouts.cfg accordingly.

This script may help::

  bin/manage report --interactive

This step should not be needed, because we do the check for every single commit,
but people may still have forgotten to add a package to the ``checkouts.cfg`` file.

4. Check packages individually

  Use the ``bin/fullrelease`` script from the core development buildout.
  This includes extra checks that we have added in ``plone.releaser``.
  It guides you through all the next steps.

  a) Check changelog

     Check if CHANGES.rst is up-to-date,
     all changes since the last release should be included,
     a Fixes and/or New header should be included,
     with the relevant changes under it.
     Upgrade notes are best placed here as well.
     Compare ``git log HEAD...<LAST_RELEASE_TAG>`` with ``CHANGES.rst``.
     Or from zest.releaser: ``lasttaglog <optional tag if not latest>``.

  b) Run `pyroma <https://pypi.python.org/pypi/pyroma/>`_

  c) Run `check-manifest <https://pypi.python.org/pypi/check-manifest/>`_

  d) Check package "best practices" (README.rst, CHANGES.rst, src directory)

    - Check if version in setup.py is correct and follows our versioning best practice

  e) Make a release (zest.releaser: ``bin/fullrelease``)

  f) Remove packages from auto-checkout section in ``checkouts.cfg`` and update ``versions.cfg``.

5. Make sure ``plone.app.upgrade`` contains an upgrade step for the future Plone release.

6. Update CMFPlone version in ``profiles/default/metadata.xml``

7. Create an issue in https://github.com/collective/plone.app.locales/issues to ask the i18n team lead @vincentfretin to do a plone.app.locales release.

8. Create a pending release (directory) on dist.plone.org

  a) Copy all core packages there.

  b) Possibly make an alpha/beta release of CMFPlone.

  c) Copy the versions.cfg file from coredev there.


9. Write an email to the Plone developers list announcing a pending release.

10. Update plone.app.locales version.

11. Create a unified changelog

::

  bin/manage changelog

12. Make final release on dist.plone.org (remove "-pending")

13. Update the "-latest" link on dist.plone.org

14. Create new release on launchpad (https://launchpad.net/plone/)

15. Create release page on http://plone.org/products/plone/releases

16. Send links to installers list
    (plone-installers@lists.sourceforge.net <mailto:plone-installers@lists.sourceforge.net>)

17. Wait for installers to be uploaded to Launchpad,
    link on plone.org release page

18. Publish release page on plone.org

19. Update plone.org homepage links to point to new release

20. Send out announcement to plone-announce

21. Update #plone topic

22. Ask the security team to update the https://plone.org/security/hotfixes/ page in the configuration control panel.
