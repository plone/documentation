---
myst:
  html_meta:
    "description": "A content type is an object that can store information and is editable by users."
    "property=og:description": "A content type is an object that can store information and is editable by users."
    "property=og:title": "Content Types"
    "keywords": "Content Types"
---

(backend-content-types-label)=

# Content types

This part of the documentation describes how to develop content types in Plone.
Content types are implemented through the {term}`Dexterity` framework.


## What is a content type?

Each item in a Plone site is an instance of a particular content type.
We have different content types to reflect the different kinds of information about which we need to collect and display information.

Pages, news items, events, files (binary), and images are examples of content types.

Lots of things in Plone can be configured to work differently based on the content type.
For example, each content type has:

-   a {ref}`schema <backend-fields-label>` specifying the fields which can be edited for the content type
-   a list of {ref}`behaviors <backend-behaviors-label>` which supply additional functionality that can be attached to the content types for which the behavior is enabled
-   a {ref}`workflow <backend-workflows-label>` controling transitions between publishing states and associated permissions
-   a version policy controling whether to store a revision history

It is common in developing a web site that you'll need customized versions of common content types, or perhaps even entirely new types.


## Topics

This part of the documentation will cover the following topics.

-   Some basic design techniques for solving problems with content types in Plone
-   Setting up a Dexterity development environment
-   Creating a package to house your types
-   Building a custom type based on a schema
-   Creating custom views and forms for your type
-   Advanced customization, including workflow and security
-   Testing your types
-   A quick reference to common fields, widgets, and APIs

```{seealso}
See the chapter {ref}`training:dexterity1-label` from the Mastering Plone 6 Training for a step-by-step tutorial to create a custom content type.
```

```{toctree}
:maxdepth: 2
```
% Uncomment each of the following and move into the toctree above when migrated from Plone 5 documentation
% designing
% prerequisite
% schema-driven-types
% model-driven-types
% custom-views
% advanced/index
% testing/index
% reference/index


## Factory Type Information

```{todo}
Find a new home for this section.
This page is an introduction, whereas FTI is a topic unto itself.
```

A content type is defined by creating a {term}`Factory Type Information` (FTI) object.

To create an FTI in a `GenericSetup` profile, add the content type to the list in `types.xml`.
For example, this adds the standard Plone page (`Document`) content type:

```xml
<object name="portal_types">
  <object name="Document" meta_type="Dexterity FTI" />
</object>
```

Then, add a file to the `types` directory with the same name.
In this example, the file is `types/Document.xml` and contains this XML:

```xml
<?xml version="1.0" encoding="utf-8"?>
<object xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        meta_type="Dexterity FTI"
        name="Document"
        i18n:domain="plone"
>

  <!-- Basic properties -->
  <property name="title"
            i18n:translate=""
  >Page</property>
  <property name="description"
            i18n:translate=""
  />

  <property name="allow_discussion">False</property>
  <property name="factory">Document</property>
  <property name="icon_expr">string:contenttype/document</property>

  <!-- Hierarchy control -->
  <property name="allowed_content_types" />
  <property name="filter_content_types">True</property>
  <property name="global_allow">True</property>

  <!-- Schema, class and security -->
  <property name="add_permission">plone.app.contenttypes.addDocument</property>
  <property name="klass">plone.app.contenttypes.content.Document</property>
  <property name="model_file">plone.app.contenttypes.schema:document.xml</property>
  <property name="model_source" />
  <property name="schema" />

  <!-- Enabled behaviors -->
  <property name="behaviors"
            purge="false"
  >
    <element value="plone.namefromtitle" />
    <element value="plone.allowdiscussion" />
    <element value="plone.excludefromnavigation" />
    <element value="plone.shortname" />
    <element value="plone.dublincore" />
    <element value="plone.richtext" />
    <element value="plone.relateditems" />
    <element value="plone.versioning" />
    <element value="plone.tableofcontents" />
    <element value="plone.locking" />
  </property>

  <!-- View information -->
  <property name="add_view_expr">string:${folder_url}/++add++Document</property>
  <property name="default_view">document_view</property>
  <property name="default_view_fallback">False</property>
  <property name="immediate_view">view</property>
  <property name="view_methods">
    <element value="document_view" />
  </property>

  <!-- Method aliases -->
  <alias from="(Default)"
         to="(dynamic view)"
  />
  <alias from="edit"
         to="@@edit"
  />
  <alias from="sharing"
         to="@@sharing"
  />
  <alias from="view"
         to="(selected layout)"
  />

  <!-- Actions -->
  <action action_id="view"
          category="object"
          condition_expr=""
          icon_expr="string:toolbar-action/view"
          title="View"
          url_expr="string:${object_url}"
          visible="True"
          i18n:attributes="title"
  >
    <permission value="View" />
  </action>
  <action action_id="edit"
          category="object"
          condition_expr="not:object/@@plone_lock_info/is_locked_for_current_user|python:True"
          icon_expr="string:toolbar-action/edit"
          title="Edit"
          url_expr="string:${object_url}/edit"
          visible="True"
          i18n:attributes="title"
  >
    <permission value="Modify portal content" />
  </action>

</object>
```

The `name` attribute on the root element in the XML must match the name in the filename and the name listed in `types.xml`.

Set the `i18n:domain` to the i18n domain which includes translations for this content type.
This is usually the same as the name of the Python package which contains the content type.


(global-fti-properties-label)=

### Global FTI properties

The XML sets a number of FTI properties that are used globally, in both Classic UI and Volto:

`action` elements
:   Defines additional {doc}`actions </backend/portal-actions>` which are available for this content type.

`add_permission`
:   Id of the permission controlling whether the current user has permission to add this content type.

`allow_discussion`
:   Boolean.
    Controls whether Plone's commenting system is enabled by default for this content type.

`allowed_content_types`
:   List of content types which can be added inside this one.
    Only used if `filter_content_types` is True.

`behaviors`
:   List of {doc}`behaviors </backend/behaviors>` enabled for this content type.

`description`
:   Short description displayed in the UI.

`factory`
:   Name of the factory adapter used to create new instances of the content type.
    Usually the same as the content type name.

`filter_content_types`
:   Boolean.
    Controls which content types can be added inside this one.
    If `True`, allow only the types listed in `allowed_content_types`.
    If `False`, allow any content type that the user has permission to add.

`global_allow`
:   Boolean.
    Set to `True` to allow adding the content type anywhere in the site where the user has permission.
    Set to `False` to only allow adding it inside other content types that include this one in `allowed_content_types`.

`klass`
:   Dotted path to the Python class for this content type.

`model_file`
:   Location of an XML file to load as the content type's schema.
    This is an alternative to `schema` and `model_source`.

`model_source`
:   Inline XML schema for the content type.
    This is an alternative to `schema` and `model_file`.

`schema`
:   Dotted path to the Python schema for this content type.
    One of `model_file`, `model_source`, and `schema` must be set.
    `schema` is the most commonly used.

`title`
:   The name of the content type displayed in the UI.


(classic-ui-only-fti-properties-label)=

### Classic UI only FTI properties

The following FTI properties are used only in Classic UI:

`add_view_expr`
:   {term}`TALES` expression returning the URL for the form to add a new item of this content type.

`alias` elements
:   Controls a mapping from URL to views.
    It's not common to change this.

`default_view`
:   Name of the default view used to display this content type.

`default_view_fallback`
:   Boolean.
    If `True`, the `default_view` will be used if the assigned view is not found.

`icon_expr`
:   {term}`TALES` expression returning the name of one of the registered icons.
    See {doc}`/classic-ui/icons`.

`immediate_view`
:   Name of the view alias to display after a new item is added.

`view_methods`
:   List of views which can be selected to display this content type.
