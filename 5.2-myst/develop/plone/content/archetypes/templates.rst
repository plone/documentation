============
Templates
============

.. admonition:: Description

        Overriding templates with Archetypes

.. contents :: local

Introduction
--------------

This document will tell how to create custom templates for Plone
and Archetypes based content.

This does not deal with

* :doc:`browser views </develop/plone/views/browserviews>`

* :doc:`generic old style template overrides </adapt-and-extend/theming/templates_css/skin_layers>`

The template loading mechanism
---------------------------------

Archetypes tries to look up a template with name

* *Content type name lowercased* + *_view.pt*

* *Content type name lowercased* + *_edit.cpt*

from portal_skins.

Example controlled page template (cpt) file yourcontenttype.cpt:

        Check More info links

For cpt files (controlled page template) you'll also need corresponding
.metadata file::

        [default]
        title = Edit Your Content Type

        [validators]
        validators = validate_atct
        validators..form_add =
        validators..cancel =

        [actions]
        action.success = traverse_to:string:content_edit
        action.success..cancel = redirect_to:python:object.REQUEST['last_referer']
        action.success_add_reference = redirect_to:python:object.REQUEST['last_referer']
        action.failure = traverse_to_action:string:edit
        action.next_schemata = traverse_to_action:string:edit


More info

* https://plone.org/documentation/manual/theme-reference/buildingblocks/skin/templates/how-to-customise-view-or-edit-on-archetypes-content-items
