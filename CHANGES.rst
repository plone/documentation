=========
Changelog
=========

Unreleased
==========

- New documentation how to develop on Windows 10 with WSL [nilshofer]
- Fix #1109 Update import statement in example 'Bypassing permission checks' [1letter]
- Fix broken link [ale-rt]

20190728
========

- Extend ZODB migration documentation about importance of packing [agitator]
- Update the ZODB py2-py3 migration guide and move to own document [jensens]
- explain how to find available image scales
  [tkimnguyen]
- Documentation for Thumbs and Iconhandling in Plone
  https://github.com/plone/Products.CMFPlone/issues/1995
  [fgrcon]
- New metadata catalog column `mime_type`
  https://github.com/plone/Products.CMFPlone/issues/1995
  [fgrcon]
- Add security guidelines for developers[vangheem]
- Overhaul of vocabularies section. [jensens]
- Remove Deliverance info for theming and refer to diazo.org deployment [fredvd]
- Improve ReStructuredText Style Guide [svx]
- Add documentation about TinyMCE styles and formats [davilima6]
- Improve Editor Guide [tmassman]
- Overhaul of Files and images chapter. [jensens]


20160606
========

- Improve documentation about PFG custom mailer [terapyon]
- Update documentation about forms in add-ons [staeff]
- Update documentation about add-on installation [svx]
- Made isort.cfg more readable by adding spaces [mauritsvanrees]
- Various .rst style fixes [svx]
- Add documentation about browserlayer.xml [davilima6]
- Add better examples for installation on various operating systems [svx]
- Improve documentation about dexterity AddCoustomView and ZCML [terapyon]
- Improve 'ask for help' docs [svx]
- Improve wording and rst on various places [svx]
- Improve docs about GenericSetup [mauritsvanrees]
- Fix link [icemac]
- Cleanup grok [staeff]
- Update index.rst [fgrcon]
- Fix various links [polyester]
- Fix various links [gforcada]
- Fix various typos [svx]
- Fix various typos [gforcada]
- Fix various typos [sverbois]
- Fix various typos [staeff]
- Add more docs about ZCML registration features [davidjb]
- Various typo fixes [jianaijun]



20160409
========

- Improve chapter about image handling [jensens]
- Improve rst style guide [svx]
- Fix 588 [svx]
- Fix 582 [svx]


20160405
========

- Fix #584 [svx]
- Update install docs to 5.0.3 [svx]
- Fix #579 [rnixx] [svx]
- Fix #583 [polyester]
- Fix 'Feedback widget' [svx]


20160330
========

- Improved styleguide [svx]
- Fixed robot tests [polyester]
- Fixed pep8 of example code [laulaz]
- Fixed links to plone.org [svx]
- Fixed #546 [svx]
- Fixed broken links, typos and rst syntax in about/contributing [svx]
- Fixed broken link to docs about ContentFilter class [do3cc]
- Added docs about 'theming' based on barceloneta [ebrehault]
- Updated python-styleguide [thet]
- Fixed wording in contribute_to_translations [svx]
- Added mention about etRolesInContext to /security/local_roles [tkimnguyen]
- Fixed typo in zope deprecation docs [thet]
- Improved docs about z3cfrom [do3cc]
- Fixed wrong imports and old references to plone.multilingual [dmunicio]
- Moved Changelog out of the documentation [svx]
- Added upgrade hint for migrate-to-emaillogin page [mauritsvanress]
- Improved docs about resource registry [cewing]
- Added Deprecation Best Practices [thet] [jensens]
- Minor additions and a typo fixes [jensens]
- Added information on how to deprecate methods and properties [thet]
- Replaced tutorial link with a current working one [staeff]
- Added note about advanced settings tab only for current theme [thet]


20151208
========

- **Removed Plone 3 parts and ponit people to plone.app.testing**

    *@lentinj* removed old Plone 3 docs, from the testing documentation and added a pointer to plone.app.testing.

- **Added documentation on <title> element**

    *@fulv* updated the docs about what a title from a content item is.

- **Provided one more example for the Title**

    *@fulv* provided more examples about titles in content items.

- **Fix outdated links**

    *@polyester* fixed many outdated and broken links

- **rst syntax fixes**

    *@polyester* fixed various rst syntax errors


20150518
========

- **Added twitter and trello account info**

        *@svx* added information about the docs twitter account and our trello board.

- **Added OmniMarkupPreviewer Plug-in**

        *@svx* added information about a sublime [editor] helper tool for writing documentation.

- **Initial barceloneta and resources doc**

        *@bloodbare* started with initial documentation about the new default theme for Plone 5.

- **Update vim plug-in part**

        *@svx* updated the documentation about vim as you editor of choice for writing documentation.

- **Add word-list for spell check**

        *@svx* added some more 'known words' to the list for spell check to avoid false positives.

- **More work on resource registry documentation**

        *@vangheem* worked on updating the resource registry documentation for Plone 5.

- **Added bobtemplates to 5.0 docs**

        *@svx* started to add bobtemplates.plone docs to the documentation for Plone 5.

- **Improved example for 'Specify files and code from another package'**

        *@pysailor* improved some examples we have in the docs for specify files and code from another package.

- **Removed plone3_theming out of 5 branch**

        *@svx* removed old parts about 'theming' which only applies to Plone 3 from the Plone 5 docs.

- **Removed old-reference/testing from 5.0 branch**

        *@svx* removed old parts about testing, which are not 'best practices' anymore and were used in Plone 3 from the Plone 5 docs.

- **Fixed RST for removed template list.**

        *@mauritsvanrees* fixed the .rst syntax of the file *updating addons*.

- **Removed old stuff about archgenxml from Plone 5 docs**

        *@svx* removed old and not valid for Plone 5 docs about archgenxml.

- **Updated to PLone 5**

        *@svx* updated *Installing Plone for Production* on Ubuntu for Plone 5.

        *@svx* updated *Installation* for Plone 5.

- **Removed paster part Plone 5 installation [WIP]**

        *@svx* started to work on removing paster documentation for out Plone 5 documentation, this is still work in progress.

- **Fixed no :term: in headers, and deleting an invisible utf-8 char**

        *@polyester* fixed a lot of issues in our headers about wrong written .rst.

- **Updated** emacs part in helper tools

        *@svx* updated the part about using emacs as editor of choice for writing documentation.

- **Clarified  style-guide**

        *@polyester* clarified the  style-guide for documentation, this fixed also issue #226.

- **Added link to zope.component docs**

        *@djowett* added a link that show how you can also register utilities, and so vocabularies with a factory.

- **Added  docs about upgrading a custom add-on to 5.0**

        *@ebrehault* wrote documentation how to upgrade a custom add-on to Plone 5.

- **Updated styleguide with gists info**

        *@svx* and *@polyester*  added docs on how to use gists.

- **Added document where to find hotfixes**

        *@polyester* wrote documentation about where user can find information about security hotfixes.

- **Corrected ZEXP export/import**

        *@thet* fixed documentation about export and import of ZEXP.

- **Sublime helpers**

        *@polyester* added more documentation about Sublime add-ons for writing good documentation.

