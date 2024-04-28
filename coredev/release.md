---
myst:
  html_meta:
    "description": "Plone release process"
    "property=og:description": "Plone release process"
    "property=og:title": "Plone release process"
    "keywords": "Plone, release, process"
---

# Plone release process

This chapter describes the process to release Plone and its packages.


## Release process for Plone packages

To keep the Plone software stack maintainable, the Python egg release process must be automated to a high degree.
This happens by enforcing Python packaging best practices, and then making automated releases using [`zest.releaser`](https://github.com/zestsoftware/zest.releaser/).

This is extended with Plone coredev specific features by [`plone.releaser`](https://github.com/plone/plone.releaser).

Anyone with necessary PyPI permissions must be able to make a new release by running the `fullrelease` command.
This command includes the following requirements.

```{note}
All files mentioned in this list may be written in Markdown or reStructuredText and have the appropriate file name suffix.
```

-   All releases must be hosted on PyPI.
-   All versions must be tagged in version control.
-   Each package must have a {file}`README` file with links to the version control repository and issue tracker.
-   {file}`CHANGES` ({file}`docs/HISTORY`) must be always up-to-date and must contain list of functional changes which may affect package users.
-   {file}`CHANGES` must contain release dates.
-   {file}`README` and {file}`CHANGES` must be visible on PyPI.
-   Released eggs must contain generated gettext `.mo` files, but these files must not be committed to the repository.
    The `.mo` files can be created with the `zest.pocompile` add-on, which should be installed together with `zest.releaser`.
-   `.gitignore` and `MANIFEST.in` must reflect the files going in to the egg (must include page template, po files).

```{seealso}
[High quality automated package releases for Python with `zest.releaser`](https://opensourcehacker.com/2012/08/14/high-quality-automated-package-releases-for-python-with-zest-releaser/).
```


## Special packages

The Plone Release Team releases the core Plone packages.
Several others also have the rights to release individual packages on [PyPI](https://pypi.org/).
If you have those rights on your account, you should feel free to make releases.

Some packages need special care, or should be done only by specific people, as they know what they are doing.
These are:

`Products.CMFPlone`, `Plone`, and `plone.app.upgrade`
:   Please leave these to the release manager, Eric Steele.

`plone.app.locales`
:   Please leave this to the i18n team lead, Vincent Fretin.


## Plone core release process checklist

1.  Check Jenkins status.
    Check the latest Plone coredev job on [Jenkins](https://jenkins.plone.org/).
    It should be green, but if it is not, fix the problem first.

2.  Check out `buildout.coredev`.

    ```shell
    git clone git@github.com:plone/buildout.coredev.git
    cd buildout.coredev
    git checkout 5.1
    python bootstrap.py
    bin/buildout -c buildout.cfg
    ```

3.  Check packages for updates.
    Check all packages for updates, add to or remove from `checkouts.cfg` accordingly.
    This script may help:

    ```shell
    bin/manage report --interactive
    ```
    
    This step should not be needed, because we do the check for every single commit, but people may still have forgotten to add a package to the `checkouts.cfg` file.

4.  Check packages individually.

    Use the `bin/fullrelease` script from the core development buildout.
    This includes extra checks that we have added in `plone.releaser`.
    It guides you through all the next steps.

    1.  Check changelog.
        Check if `CHANGES` is up-to-date.
        All changes since the last release should be included.
        A "Fixes" or "New" header should be included, with the relevant changes under it.
        Upgrade notes are best placed here as well.
        Compare `git log HEAD...<LAST_RELEASE_TAG>` with `CHANGES`, or from `zest.releaser` use the command `lasttaglog <optional tag if not latest>`.
    2.  Run [pyroma](https://pypi.org/project/pyroma/).
    3.  Run [check-manifest](https://pypi.org/project/check-manifest/).
    4.  Check package "best practices" (`README`, `CHANGES`, `src` directory).
    5.  Check if the version in `setup.py` is correct and follows our versioning best practice.
    6.  Make a release (zest.releaser: `bin/fullrelease`)
    7.  Remove packages from auto-checkout section in `checkouts.cfg` and update `versions.cfg`.

5.  Make sure `plone.app.upgrade` contains an upgrade step for the future Plone release.
6.  Update CMFPlone version in `profiles/default/metadata.xml`.
7.  Create an issue in <https://github.com/collective/plone.app.locales/issues> to ask the i18n team lead @vincentfretin to do a `plone.app.locales` release.
8.  Create a pending release (directory) on [dist.plone.org](https://dist.plone.org/).
    
    1.  Copy all core packages there.
    2.  Possibly make an alpha or beta release of CMFPlone.
    3.  Copy the `versions.cfg` file from coredev to there.

9.  Write an email to the Plone developers list announcing a pending release.
10. Update `plone.app.locales` version.
11. Create a unified changelog.

    ```shell
    bin/manage changelog
    ```

12. Make the final release on dist.plone.org (remove "-pending")
13. Update the "-latest" link on [dist.plone.org](https://dist.plone.org/).
14. For Plone 5.x versions only, create the new release on [Launchpad](https://launchpad.net/plone/).
15. Create a release page on [plone.org](https://plone.org/download/releases)
16. Send links to the installers list at plone-installers@lists.sourceforge.net.
17. Wait for installers to be uploaded to Launchpad, with a link to the plone.org release page.
18. Publish release page on plone.org.
19. Update plone.org homepage links to point to the new release.
20. Send out announcement to the plone-announce email distribution list.
21. Update #plone topic (obsolete? maybe announce to Discord?)
22. Ask the security team to update the [Hotfixes](https://plone.org/security/hotfixes/) page in the configuration control panel.
