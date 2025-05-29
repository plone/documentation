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

Plone coredev specific features extend on that using [`plone.releaser`](https://github.com/plone/plone.releaser).

Anyone with necessary PyPI permissions must be able to make a new release by running the `fullrelease` command.
This command includes the following requirements.

```{note}
All files mentioned in this list may be written in Markdown or reStructuredText and have the appropriate file name suffix.
```

-   All releases must be hosted on PyPI.
-   All versions must be tagged in version control.
-   Each package must have a {file}`README` file with links to the version control repository and issue tracker.
-   {file}`CHANGES` (or {file}`docs/HISTORY`) must be always up-to-date and must contain list of functional changes which may affect package users.
-   {file}`CHANGES` must contain release dates.
-   {file}`README` and {file}`CHANGES` must be visible on PyPI.
-   Released eggs must contain generated gettext `.mo` files, but these files must not be committed to the repository.
    The `.mo` files can be created with the `zest.pocompile` add-on, which should be installed together with `zest.releaser`.
-   `.gitignore` and `MANIFEST.in` must reflect the files going in to the package (must include page template and `.po` files).


## Special packages

The Plone Release Team releases the core Plone packages.
Several other people also have the rights to release individual packages on [PyPI](https://pypi.org).
If you have those rights on your account, you should feel free to make releases.

Some packages need special care, or should be done only by specific people, as they know what they are doing.
These are:

`Products.CMFPlone`, `Plone`, and `plone.app.upgrade`
:   Please leave these to the release managers, Eric Steele and Maurits van Rees.

`plone.app.locales`
:   Please leave this to the i18n team lead, Mikel Larreategi `@erral`.
`plone.staticresources`, `mockup`, `plonetheme.barceloneta`, `plone.classicui`:
:   Please leave this to the Classic UI team, especially Peter Mathis `@petschki`, Johannes Raggam `@thet`, and Maik Derstappen `@MrTango`.

`plone.restapi` and `plone.volto`:
:   Please leave these to Timo Stollenwerk `@tisto` or David Glick `@davisagli`.


## Plone core release process checklist

1.  Check Jenkins status.
    Check the latest Plone coredev job on [Jenkins](https://jenkins.plone.org).
    It should be green, but if it is not, fix the problem first.

1.  Clone `buildout.coredev`, then check out and build the version to be released.

    ```shell
    git clone git@github.com:plone/buildout.coredev.git
    cd buildout.coredev
    git checkout 6.1
    ./bootstrap.sh
    bin/buildout -c buildout.cfg
    ```

1.  Check packages for updates.
    Add to or remove from `checkouts.cfg` accordingly.
    This script may help:

    ```shell
    bin/manage report --interactive
    ```

    This step should not be needed, because we do the check for every single commit, but people may still have forgotten to add a package to the `checkouts.cfg` file.

1.  Check packages individually.

    Use the `bin/fullrelease` script from the core development buildout.
    This includes extra checks that we have added in `plone.releaser`.
    It guides you through all the next steps.

    1.  Check changelog.
        Check if `CHANGES` is up-to-date.
        All changes since the last release should be included.
        A "Fixes" or "New" header should be included, with the relevant changes under it.
        Upgrade notes are best placed here as well.
        Compare `git log HEAD...<LAST_RELEASE_TAG>` with `CHANGES`, or from `zest.releaser` use the command `lasttaglog <optional tag if not latest>`.
    1.  Run [pyroma](https://pypi.org/project/pyroma/).
    1.  Run [check-manifest](https://pypi.org/project/check-manifest/).
    1.  Check package "best practices" (`README`, `CHANGES`, `src` directory).
    1.  Check if the version in `setup.py` is correct and follows our versioning best practice.
    1.  Make a release with `zest.releaser`: `bin/fullrelease`.
    1.  Remove packages from the `auto-checkout` section in `checkouts.cfg`, and update `versions.cfg`.

1.  Make sure `plone.app.upgrade` contains an upgrade step for the future Plone release.
1.  Update CMFPlone version in `profiles/default/metadata.xml`.
1.  Create an issue in https://github.com/collective/plone.app.locales/issues to ask the i18n team lead `@erral` to do a `plone.app.locales` release.
1.  Create a pending release (directory) on [dist.plone.org](https://dist.plone.org/).

    1.  Copy all core packages there.
    1.  Possibly make an alpha or beta release of CMFPlone.
    1.  Copy the `versions.cfg` file from coredev to there.

1.  Write an email to the Plone developers list announcing a pending release.
1.  Create a post on the Plone Community Forum announcing a pending release.
1.  Update `plone.app.locales` version.
1.  Create a unified changelog.

    ```shell
    bin/manage changelog
    ```

1.  Make the final release on [dist.plone.org](https://dist.plone.org/) (remove "-pending")
1.  Update the "-latest" link on [dist.plone.org](https://dist.plone.org/).
1.  For Plone 5.x versions only, create the new release on [Launchpad](https://launchpad.net/plone/).
1.  Create a release page on [plone.org](https://plone.org/download/releases)
1.  Wait for installers to be uploaded to Launchpad, with a link to the [plone.org](https://plone.org/download/releases) release page.
1.  Publish release page on [plone.org](https://plone.org/).
1.  Update [plone.org](https://plone.org/) homepage links to point to the new release.
1.  Send out announcement to the plone-announce email distribution list for the final release.
1.  Create a post on the Plone Community Forum announcing the final release.
1.  Ask the security team to update the [Hotfixes](https://plone.org/security/hotfixes/) page in the configuration control panel.
