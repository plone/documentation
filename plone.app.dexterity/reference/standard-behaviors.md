---
myst:
  html_meta:
    "description": "Standard behaviors of content types in Plone"
    "property=og:description": "Standard behaviors of content types in Plone"
    "property=og:title": "Standard behaviors of content types in Plone"
    "keywords": "Plone, standard, behaviors, content types"
---

# Standard behaviors

This chapter lists common behaviors that ship with Plone and Dexterity.

Plone and Dexterity ships with several standard behaviors.
The following table shows the shortnames you can list in the FTI `behaviors` properties and the resultant form fields and interfaces.

| Short Name | Interface | Description |
| - | - | - |
| plone.allowdiscussion | plone.app.dexterity.behaviors.discussion.IAllowDiscussion | Allow discussion on this item. |
| plone.basic | plone.app.dexterity.behaviors.metadata.IBasic | Basic metadata: Adds `title` and `description` fields. |
| plone.categorization | plone.app.dexterity.behaviors.metadata.ICategorization | Categorization: Adds `keywords` and `language` fields. |
| plone.collection | plone.app.contenttypes.behaviors.collection.Collection | Collection behavior with `querystring` and other related fields. |
| plone.dublincore | plone.app.dexterity.behaviors.metadata.IDublinCore | Dublin Core metadata: Adds standard metadata fields. Shortcut for (and same as) `plone.basic` + `plone.categorization` + `plone.publication` + `plone.ownership`) |
| plone.excludefromnavigation | plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation | Exclude From navigation: Allow items to be excluded from navigation. |
| plone.leadimage | plone.app.contenttypes.behaviors.leadimage.ILeadImage | Adds a `LeadImage` field like used for News item. |
| plone.namefromfilename | plone.app.dexterity.behaviors.filename.INameFromFileName | Name from file name: Automatically generate short URL name for content based on its primary field file name. Not a form field provider. |
| plone.namefromtitle | plone.app.content.interfaces.INameFromTitle | Name from title: Automatically generate short URL name for content based on its initial title. Not a form field provider. |
| plone.navigationroot | plone.app.layout.navigation.interfaces.INavigationRoot | Navigation root: Make all items of this type a navigation root. Not a form field provider. |
| plone.nextpreviousenabled | plone.app.dexterity.behaviors.nextprevious.INextPreviousEnabled | Next/previous navigation: Enable next/previous navigation for all items of this type. Not a form field provider. |
| plone.nextprevioustoggle | plone.app.dexterity.behaviors.nextprevious.INextPreviousToggle | Next/previous navigation toggle: Allow items to have next/previous navigation enabled. |
| plone.ownership | plone.app.dexterity.behaviors.metadata.IOwnership | Ownership: Adds creator, contributor, and rights fields. |
| plone.publication | plone.app.dexterity.behaviors.metadata.IPublication | Date range for publication: Adds effective date and expiration date fields. |
| plone.relateditems | plone.app.relationfield.behavior.IRelatedItems | Adds the `Related items` field to the `Categorization` fieldset. |
| plone.richtext | plone.app.contenttypes.behaviors.richtext.IRichText | Rich text field with a WYSIWIG editor. |
| plone.selectablecontrainstypes | Products.CMFPlone.interfaces.constrains.ISelectableConstrainTypes | Folder Addable Constrains: Restrict the content types that can be added to folderish content. |
| plone.shortname | plone.app.dexterity.behaviors.id.IShortName | Short name: Gives the ability to rename an item from its edit form. |
| plone.tableofcontents | plone.app.contenttypes.behaviors.tableofcontents.ITableOfContents | Table of contents. |
| plone.thumb_icon | plone.app.contenttypes.behaviors.thumb_icon.IThumbIconHandling | Adds options to suppress thumbs (preview images) or icons and to override thumb size in listings or tables. |
