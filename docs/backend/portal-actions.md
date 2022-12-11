---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(backend-portal-actions-label)=

# Portal Actions

## What are "Actions" in Plone

Actions are links or buttons that allow users to perform specific actions on your site.
These actions can be anything from viewing a content item to editing a page, to accessing a specific feature of your site.

```{note}
There are at least two providers for actions, the `portal_actions` tool and the content type actions defined in the several Factory Type Information's under the `portal_workflow` tool.
Here the portal actions are described.
```

Portal actions are typically displayed in the site's navigation menu or toolbar and can be accessed by users with the appropriate permissions.

Portal actions are managed using the "Portal Actions" control panel in Plone.
This control panel allows you to add, edit, and delete actions, as well as organize them into categories and control where they are available on your site.

## Anatomy of a Portal action

A portal action in Plone consists of a few different components, including the category, title, description, URL, and control parameters.

The action title is the text that is displayed for the action in the site's navigation menu or toolbar.
This text should be descriptive and indicate what the action does.
The description is used as an additional text shown when hovering over the link.
The title and description can be translated using the translation system of Plone.
Therefore the i18n domain can be set here.

The Action URL is the address of the page or feature that the action will access when it is clicked.
This can be an internal page on your site or an external page on another website.

The "Condition" controls whether to show the action or not.

You can use expressions in the URL of an action to make the action more dynamic and flexible. Expressions are also used for the "Condition".

The permissions chosen also control the visibility of an action.

Visibility can be used to hide actions.
This can be handy to disable default actions or temporarily disable actions.

The "Position" is used to order action within their category and is numbered starting with "1".

Together, these components make up a portal action in Plone.

You can use the "Portal Actions" control panel to manage and organize your site's actions.

## Action categories

Several different action categories are used for different purposes.
These categories include:

- *Object Actions*: actions that are available when viewing a specific content item
- *Object Buttons*: actions that are displayed as buttons when viewing a specific content item
- *Portal Tabs*: actions that are displayed as tabs on the top of the page
- *Site Actions*: actions that are available on every page of your site
- *User Actions*: actions that are available to users when they are logged in to your site

Each of these action categories serves a different purpose and is intended for use in specific areas of the site.
For example, object actions are intended for actions that are specific to a particular content item, while site actions are intended for actions that are available on every page of your site.

## Expressions

An expression is a piece of code that is evaluated at runtime and can be used to insert dynamic values into the URL or provide the decision for the condition.

```{todo}
Contribute to this documentation!
A chapter about expressions is missing. As soon as it exists a link to this chapter needs to be placed here.
See issue [Backend > missing chapter Expressions needs content](https://github.com/plone/documentation/issues/1370).
```

## Adding or editing portal actions

To add or edit portal actions, you can use the "Portal Actions" control panel.
To access this, log in to your Plone site as a user with the appropriate permissions, and then go to the "Site Setup" page.
From there, click on the "Portal Actions" link in the "Plone Configuration" section.

Once you are on the "Actions" control panel, you will see a list of all the existing portal actions for your site.
To add a new action, click on the "Add new action" button at the top of the page.
This will open a form where you can enter the details for your new action, such as the action name, URL, and any additional parameters.

To edit an existing action, click on the action name in the list to open the action's details page.
From there, you can edit the action's properties, such as the name, URL, and parameters.

It's important to note that the ability to add or edit portal actions is only available to users with the appropriate permissions.
If you do not have the necessary permissions, you will not be able to access the "Portal Actions" control panel.

## Exporting or importing portal actions

You can export action configuration to XML using the built-in GenericSetup export.

Then this XML can be imported again within a profile of an add-on package.
Place the file as `actions.xml` in the profile of an add-on.
You can cut out snippets from this file for creating `actions.xml` containing only changed or added parts.

To export all actions:

- Go to "Site Setup" and choose "Management Interface"
- Go to "portal_setup"
- Click the tab "Export"
- Choose "Actions Providers"
- Click the "Export selected steps" button at the end of the page

