---
myst:
  html_meta:
    "description": "Plone upgrade preparations"
    "property=og:description": "Plone upgrade preparations"
    "property=og:title": "Plone upgrade preparations"
    "keywords": "Plone, upgrade, preparations"
---


(upgrade-preparations-label)=

# Preparations

This chapter lists things to do before you migrate Plone.


(upgrade-gather-informationlabel)=

## Gather information

-   Read the "What's new in..." for your relevant Plone version, and read the release notes.
    You will find these in the {file}`CMFPlone` directory of the distribution of the new version of Plone.

-   Make sure to check installed add-ons.
    If you **do not** need certain add-ons anymore, deactivate and uninstall them.

-   Check for dependencies.

    -   Read the release notes for the Plone release you are upgrading to, in particular:
    
        -   What version of Python is required?
        
        -   What version of Zope is required?
        
        -   Do you need any new Python libraries?
    
    -   Make sure all the add-on products you are using have been updated to support the version of Plone to which you are upgrading.
    
    -   Start with the third-party products that are in use on your site.
        Verify that they have been updated or verified to work on the new version, and get them upgraded in your existing instance before you start the Plone/Zope/Python upgrade, if possible.
    
    -   If Zope depends on a newer version of Python, install the new version of Python first.
    
    -   If the newer version of Plone depends on a newer version of Zope, you will need to install that before proceeding with the Plone upgrade.

        ```{note}
        Zope has its own migration guidelines, which you will find in the release notes of the version you are migrating to.
        
        If Plone is being upgraded at the same time as a Zope version, Plone will usually handle the Zope upgrade with its own migration script.
        ```

-   Read the following files in the {file}`CMFPlone` directory of the distribution of the new version of Plone to which you want to update.

    -   `README.txt`
    
    -   `INSTALL.txt`
    
    -   `UPGRADE.txt` (although this usually contains only the general procedure outlined above)

    These files may contain important last-minute information, and might be more specific than the relevant sections of this reference manual.


(upgrade-back-up-your-Plone-site-label)=

## Back up your Plone site

```{danger}
Always back up your Plone site before upgrading.
```

```{seealso}
See Plone 5.2 documentation, [Backing up your Plone deployment](https://docs.plone.org/manage/deploying/backup.html).
```

```{todo}
Migrate the Plone 5.2 docs for Backing up your Plone deployment into Plone 6 docs.
```


(upgrade-setup-a-test-environment-to-rehearse-the-upgrade-label)=

## Setup a test environment to rehearse the upgrade

```{danger}
Never work directly on your live site until you know that the upgrade was successful.
```

Always create a test environment to rehearse the upgrade.
Copy your instance into a new environment and upgrade the copy.
This is a good way of working through your third-party products and dependencies in preparation for the final upgrade of the live site.
