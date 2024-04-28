---
myst:
  html_meta:
    "description": "Troubleshooting a Plone upgrade"
    "property=og:description": "Troubleshooting a Plone upgrade"
    "property=og:title": "Troubleshooting a Plone upgrade"
    "keywords": "Troubleshooting, upgrade, Plone, Zope, add-ons"
---

(upgrading-troubleshooting-an-upgrade-label)=

# Troubleshooting an upgrade

This chapter covers troubleshooting a Plone upgrade.

When a problem occurs during the migration we recommend that you take the following steps.


(upgrading-troubleshooting-check-the-log-files-label)=

## Check the log files

When a site error occurs, or Zope fails to start, there is probably an informative error message in the log files.
The log files are located in your project's `var/log` directory.
Inspect `instance.log`.
Ignore irrelevant warnings, and perform a case-insensitive search for words such as "error", "exception", and "traceback".

When Zope does not start and there is no useful information in the log file, you can start Zope interactively.

Plone 6 command:

```shell
make start-backend
```

Plone 5.2 and earlier command:

```shell
bin/instance fg
```

Watch for error messages in the console.

You may be able to find more information about the error messages in the following documents.

-   {doc}`Version-specific migration tips </backend/upgrading/version-specific-migration/index>` for your version of Plone
-   [Error Reference](https://5.docs.plone.org/appendices/error-reference.html)

```{todo}
See https://github.com/plone/documentation/issues/1323
```


(upgrading-troubleshooting-test-without-customizations-label)=

## Test without customizations

When you have customized page templates or Python scripts, your changes may interfere with changes in the new version of Plone.
It is important to rule out this possibility.
Your customizations are unique to your site, and no one on the planet will be able to help you solve it.

Temporarily remove your customizations.
Remove your layers from `portal_skins`.
Remove files from these layers on the file system.
If the problem disappears, you will need to double-check your customizations.
It is usually best to copy the original files of the new version of Plone to your skin, and re-customize those.


(upgrading-troubleshooting-test-without-add-ons-label)=

## Test without add-ons

Bugs or compatibility problems in add-ons that you have installed may cause problems in Plone.
Go to {guilabel}`Site Setup > Add-ons`, and deactivate all add-ons that are not distributed with Plone.
Remove the deactivated add-ons from the packages of your Zope instance.

If the problem disappears, you will need to double-check the offending product.

-   Does it support the new version of Plone, Zope, and Python?
    Check the product's `README.txt` or other informational files or pages.
-   Does the product require any additional migration procedures?
    Check the product's `INSTALL.txt`, `UPGRADE.txt`, or other informational files or pages.
-   Does the product install properly?
    Re-install it and check the installation log.


(upgrading-troubleshooting-test-with-a-fresh-plone-instance-label)=

## Test with a fresh Plone instance

Create a new Plone site with your new version of Plone.
You do not need a new Zope instance, because you can add another Plone site in the root of Zope.
If the problem does not occur in a fresh site, the cause of your problem is most likely a customization, an installed product, or content that was not migrated properly.


(upgrading-troubleshooting-make-the-problem-reproducible-label)=

## Make the problem reproducible

Before you go out and [ask for help](https://plone.org/support/how-to-ask-for-help), you should be able to describe your problem in such a way that others can reproduce it in their environment.

-   Reduce the problem to the smallest possible domain.
-   Eliminate products and customizations that are not part of the problem.

This makes it easier for others to reproduce the problem, and it increases your chances of meeting others with the same problem or even a solution.
The more complex your story, the more likely that it is unique to your situation and impenetrable to others.


(upgrading-troubleshooting-ask-for-help-label)=

## Ask for help

[Ask for help](https://plone.org/support/how-to-ask-for-help) in the [Plone Community Forum](https://community.plone.org/) or request paid commercial support from [Plone service providers](https://plone.org/providers).
Be sure to do the following.

-   Provide relevant source code for your customizations that are part of the problem.
-   Describe the exact configuration, software versions, migration history, error messages, and so on.


(upgrading-troubleshooting-report-a-bug-label)=

## Report a bug

Once you have investigated, analyzed, identified, and confirmed the cause of your problem, and you are convinced it is a bug, go to the appropriate bug tracker and report it.

-   Add-ons: the README usually tells how to report bugs.
-   [Plone issue tracker](https://github.com/plone/Products.CMFPlone/issues).

Do not abuse the issue trackers by asking for support.
