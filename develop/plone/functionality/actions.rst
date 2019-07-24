=======
Actions
=======

.. admonition:: Description

   Creating and using portal_actions mechanism


Introduction
------------

Plone has concept of actions which connect the end user functionality associated with site or content objects:

* View, edit, sharing etc. are actions

* Sitemap is action

* Contact form is action

* Cut, copy, paste are actions

* Logged in menu is populated by actions

Actions are managed by

* portal_actions for generic actions

* portal_types for view, edit etc. actions and object default action... all actions
  which are tied to a particular content type and may vary by type

Iterating through available actions
-------------------------------------

Here is a page template example

.. code-block:: html

          <ul>
               <tal:actions repeat="action python:context.portal_actions.listFilteredActionsFor(context)['portal_tabs']">
                 <li>
                       <a tal:attributes="href action/url; title action/title;" tal:content="action/title">
                         Action title
                       </a>
                 </li>
               </tal:actions>
         </ul>

.. _create_actions_ttw:

Creating actions through-the-web
---------------------------------

You can manage the actions from Site Setup using the Actions control panel.

This control panel lists all the existing actions, grouped by category. Any action can be modified (using the **Edit** button), or removed (using the **Delete** button). The **Add** button allows to create a new action.

To re-order actions, click **Edit** and change the position parameter value.

To move an action to another category, click **Edit** and change the category parameter value.

Exporting and importing all portal_actions
=============================================

You can transfer action configuration from a Plone site to another using GenericSetup export/import XML.
You can also do this to generate XML from which you can cut out snippets for creating
actions.xml by hand.

* Go to portal_setup

* Choose Export

* Choose actions

* Choose "Export selected steps" button at the end of the page

* ...and so on

Creating actions.xml by hand
--------------------------------------------------

Usually all actions are rewritten by site policy product using portal_actions import/export.
Actions are in GenericSetup profile file *default/profiles/actions.xml*.

#. actions.xml is exported from the development instance using portal_setup

#. actions.xml is made part of the site policy product

Alternatively, if you are developing add-on product, you can add actions one-by-one by
manually creating entries in actions.xml.

Example how to add an action to the ``document_actions`` (like ``rss`` and ``print``):

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_actions" meta_type="Plone Actions Tool"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n">
     <object name="document_actions" meta_type="CMF Action Category">
      <object name="sendto" meta_type="CMF Action" i18n:domain="plone">
       <property name="title" i18n:translate="">Send this</property>
       <property name="description" i18n:translate=""></property>
       <property name="url_expr">string:$object_url/sendto_form</property>
       <property name="icon_expr"></property>
       <property name="available_expr">object/@@shareable</property>
       <property name="permissions">
        <element value="Allow sendto"/>
       </property>
       <property name="visible">True</property>
      </object>
     </object>
    </object>

Example how to add actions to user menu, which is
visible in the top right corner for logged in users (Plone 4):

.. code-block:: xml

        <?xml version="1.0"?>
        <object name="portal_actions" meta_type="Plone Actions Tool"
           xmlns:i18n="http://xml.zope.org/namespaces/i18n">
         <object name="user" meta_type="CMF Action Category">
          <object name="ora_sync" meta_type="CMF Action" i18n:domain="plone">
           <property name="title" i18n:translate="">ORA</property>
           <property name="description" i18n:translate="">ORA site synchronization status</property>
           <property name="url_expr">string:${portal_url}/@@syncall</property>
           <property name="icon_expr"></property>
           <property name="available_expr"></property>
           <property name="permissions">
            <element value="Manage portal"/>
           </property>
           <property name="visible">True</property>
          </object>
         </object>
        </object>

Reordering actions in actions.xml
==================================

Try using these attributes

* insert-after

* insert-before

They accept * and action name parameters.

Example::

  <object name="sendto" meta_type="CMF Action" i18n:domain="plone" insert-before="*">



Action URLs
-----------

Actions are applied to objects by adding action name to url.

E.g.::

    http://localhost:8080/site/page/view

for view action and::

    http://localhost:8080/site/page/edit

for edit action.

Action can be also not related to document, like::

    http://localhost:8080/site/sitemap

Default action
--------------

Default action is executed when the content URL is opened without any
prefix.

Default action is defined in portal_types.

Default action can be dynamic - meaning that
site editor may set it from Display menu. For more information see
Dynamic Views.


Content type specific actions
-------------------------------

Content type specific actions can be registered in portal_types.
Actions are viewable and editable in the Management Interface under portal_types.
After editing actions,
content type XML can be  exported and placed to your content type add-on product.

GenericSetup example file for content type "ProductCard" which has a new tab added
next to view, edit, sharing, etc. File is located in profiles/default/types/ProductCard.xml.

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="ProductCard"
       meta_type="Factory-based Type Information with dynamic views"
       i18n:domain="saariselka.app" xmlns:i18n="http://xml.zope.org/namespaces/i18n">
      <property name="title" i18n:translate="">Tuotekortti</property>
      ....
      <alias from="(Default)" to="(dynamic view)" />
      <alias from="edit" to="atct_edit" />
      <alias from="sharing" to="@@sharing" />
      <alias from="view" to="(selected layout)" />
      <action title="View" action_id="view" category="object" condition_expr=""
        url_expr="string:${object_url}/" visible="True">
        <permission value="View" />
      </action>
      <action title="Edit" action_id="edit" category="object" condition_expr=""
        url_expr="string:${object_url}/edit" visible="True">
        <permission value="Modify portal content" />
      </action>

      <!-- Custom action code goes here. We add a new tab with title "Data" and
             uri @@productdata_view which is a registered BrowserView for the content type.
        -->

     <action title="Data" action_id="productdata_view" category="object" condition_expr=""
        url_expr="string:${object_url}/@@productdata_view" visible="True">
        <permission value="Modify portal content" />
      </action>

    </object>

The corresponding BrowserView is registered as any other view in *browser/configure.zcml*:

.. code-block:: xml

  <browser:page
      for="*"
      name="productdata_view"
      class=".productdataview.ProductDataView"
      template="productdataview.pt"
      allowed_attributes="renderData"
      permission="zope2.View"
      />

Toggling action visibility programmatically
--------------------------------------------

.. warning::

    This applies only for Plone 2.5. You should use actions.xml instead.

Example::

    def disable_actions(portal):
        """ Remove unneeded Plone actions

        @param portal Plone instance
        """

        # getActionObject takes parameter category/action id
        # For ids and categories please refer to portal_actins in the Management Interface
        actionInformation = portal.portal_actions.getActionObject("document_actions/rss")

        # See ActionInformation.py / ActionInformation for available edits
        actionInformation.edit(visible=False)

Visibility expressions
----------------------

In portal_actions expression is used to determine whether an action is visible
on a particular page.

Expression is "expression" field in actions.xml or "Expression" field in
portal_actions.

.. note::

        This check is just a visibility check. Users can still
        try to type the action by typing the URL manually. You need
        to do the permission level security check on the view providing the action.

For more information see :doc:`expressions </develop/plone/functionality/expressions>`.

Condition examples
===================

See in :doc:`expressions </develop/plone/functionality/expressions>`.

Using actions in views and viewlets
------------------------------------

Example::

    context_state = getMultiAdapter((self.context, self.request),
                                name=u'plone_context_state')

    # First argument is action category,
    # we have custom "mobile_actions"
    self.actions = context_state.actions().get('mobile_actions', None)

Tabs (sections)
----------------

Tabs are special actions

* Some of tabs are automatically generated from root level content items

* Some of tabs are manually added to portal_actions.portal_tabs

By default, they are shown as the top vertical navigation of Plone site.

Example how to generate tabs list::

    def getSections(self):
        """

        @return: tuple (selectedTabs, currentSelectedTab)
        """

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        actions = context_state.actions()


        # Get CatalogNavigationTabs instance
        portal_tabs_view = getMultiAdapter((self.context, self.request),
                                           name='portal_tabs_view')

        # Action parameter is "portal_tabs" by default, but can be other
        portal_tabs = portal_tabs_view.topLevelTabs(actions=actions)

        selectedTabs = self.context.restrictedTraverse('selectedTabs')

        selected_tabs = selectedTabs('index_html',
                                          self.context,
                                          portal_tabs)

        selected_portal_tab = selected_tabs['portal']

        return (portal_tabs, selected_portal_tab)

Custom action listings
----------------------

Example::

        import Acquisition
        from zope.component import getMultiAdapter

        class Sections(base.Sections):
            """
            """

            def update(self):
                base.Sections.update(self)

                context = Acquisition.aq_inner(self.context)
                # IContextState view provides shortcut to get different action listings
                context_state = getMultiAdapter((context, self.request), name=u'plone_context_state')
                all_actions = context_state.keyed_actions() # id -> action mappings
                mobile_site_actions = all_actions["mobile_site_actions"].values()
                self.portal_tabs = mobile_site_actions

Different tabs per section/folder
---------------------------------

You might want to have different actions for different site sections or folders.

* http://plone.293351.n2.nabble.com/Custom-portal-tabs-per-subsection-tp5747768p5747768.html

Custom object and object_buttons actions per portal type
--------------------------------------------------------

If you need to override or customize an action from ``object_buttons`` that still uses ``CMFFormController`` for a specific ``portal_type``, check:

* https://stackoverflow.com/questions/11218272/plone-reacting-to-object-removal/11225447#11225447

Copy, cut and paste
----------------------

These action are based on ``OFS`` Zope 2 package SimpleItem mechanisms.
Plone specific event handlers are used to update Plone related stuff like ``portal_catalog``
on move.

Plone internal clipboard relies on the presence of Zope 2 session (different from authentication session).
Paste action fails silenlty (is missing) if ``_ZopeId`` session cookie does not work correctly on your
web server.
