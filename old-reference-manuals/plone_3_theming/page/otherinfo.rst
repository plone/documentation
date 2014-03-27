Using Other Information about your Site on a Page
=================================================

How to get information about the state of your site and other global
variables.

At some point or other you'll find you need to use the title of your
site in a template; or you'll want your template to deliver something
depending on the roles or permissions of your visitor or user. There are
two approaches for obtaining this information:

1. Browser Views (recommended)
------------------------------

The first, newer, and recommended approach is to use the methods
available in one of three browser views:

-  @@plone\_portal\_state
-  @@plone\_context\_state
-  @@plone\_tools

These are kept in

-  [your egg location]/plone/app/layout/globals OR
-  [your egg
   location]/plone.app.layout-[version]/plone/app/layout/globals

You can find a description of each method in interfaces.py in that
directory, but the main methods are outlined below. This excerpt from
the main\_template in the core Plone Default templates in Plone 4,
demonstrates how these views, or their individual methods, are made
available to every page:

::

    <html xmlns="http://www.w3.org/1999/xhtml"
          ...
          tal:define="portal_state context/@@plone_portal_state;
                      context_state context/@@plone_context_state;
                      ...
                      lang portal_state/language;
                      ...
                      portal_url portal_state/portal_url;
                      ..."
         ...
    >

Here's an excerpt from the newsitem\_view template in the core Plone
Default templates illustrating how the @@plone\_context\_state can be
used to establish whether an item is editable or not:

::

            <p tal:define="is_editable context/@@plone_context_state/is_editable"
               tal:condition="python: not len_text and is_editable"
               i18n:translate="no_body_text"
               class="discreet">
                This item does not have any body text, click the edit tab to change it.
            </p>

2.  Global Defines (deprecated)
-------------------------------

The second approach has been around for a long time, but is being phased
out (as it is slower) in Plone 3 and has been pretty much removed in
Plone 4. This is to use a set of variables that are available to every
single page.

In Plone 3:

These are called by main\_template:

::

    <metal:block use-macro="here/global_defines/macros/defines" />

If you want to investigate them further, you'll find them in

-  [your products directory]/CMFPlone/browser/ploneview.py.

These variables are used in a number of the default Plone templates in
Plone 3 and so they are listed below alongside their equivalent in the
available views.

In Plone 4:

The global\_defines macro is not used at all and the variables have been
entirely replaced in all Plone templates. However, should it be
required, the global\_defines macro is still available in the core Plone
Default skin layers in the plone\_deprecated folder.  For more
information on making a Plone 3 theme compatible with Plone 4, consult
the `upgrade
guide <http://plone.org/documentation/manual/upgrade-guide/version/upgrading-plone-3-x-to-4.0/updating-add-on-products-for-plone-4.0/no-more-global-definitions-in-templates>`_.

Available Views and Methods
---------------------------

About the site
~~~~~~~~~~~~~~

View @@plone\_portal\_state

Method

What you get

global defines

portal

Portal Object

portal

portal\_title

The title of your site

portal\_title

portal\_url

The URL of your site

portal\_url

navigation\_root\_path

Path of the navigation root

navigation\_root\_url

The URL of the navigation root

navigation\_root\_url

default\_language

The default language of the site

language

The current language

locale

The current locale

is\_rtl

Whether the site is being viewed in an RTL language

isRTL

member

The current authenticated member

member

anonymous

Whether or not the current visitor is anonymous

isAnon

friendly\_types

Get a list of types that can be deployed by a user

About the current context
~~~~~~~~~~~~~~~~~~~~~~~~~

View @@plone\_context\_state

Method

what you get

global defines

current\_page\_url

The URL of the current page

current\_page\_url

current\_base\_url

The actual URL of the current page

 

canonical\_object

The current object itself

 

canonical\_object\_url

The URL of the current object

 

view\_url

The URL used for viewing the object

 

view\_template\_id

The id of the view template

 

is\_view\_template

True if the current URL refers to the standard view

 

object\_url

The URL of the current object

 

object\_title

The 'prettified' title of the current object

 

workflow\_state

The workflow state of the current object

wf\_state

parent

The direct parent of the current object

 

folder

The current folder

 

is\_folderish

True if this is a folderish object

isFolderish

is\_structural\_folder

True if this is a structural folder

isStructuralFolder

is\_default\_page

True if this is the default page in a folder

 

is\_portal\_root

True if this is the portal root or the default page in the portal root

 

is\_editable

True if the current object is editable

is\_editable

is\_locked

True if the current object is locked

isLocked

 actions
(Plone 4)

The filtered actions in the context. You can restrict the actions to
just one category.

 

 portlet\_assignable
(Plone 4)

 Whether or not the context is capable of having locally assigned
portlets.

 

Tools
~~~~~

view @@plone\_tools

method

what you get

global defines

actions

The portal actions tool

atool

catalog

The portal\_catalog tool

 

membership

The portal\_membership tool

mtool

properties

The portal\_properties tool

 

syndication

The portal\_syndication tool

syntool

types

The portal\_types tool

 

url

The portal\_url tool

utool

workflow

The portal\_workflow tool

wtool

 
