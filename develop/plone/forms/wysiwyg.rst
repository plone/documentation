================================
WYSIWYG text editing and TinyMCE
================================

.. admonition:: Description

        WYSIWYG text field editor programming in Plone.


Introduction
------------

Plone supports TinyMCE (default), and CKEditor and others through external add-ons.

In Plone 5, TinyMCE and the Plone integration is provided by the `Mockup project <https://github.com/plone/mockup>`_.

Disabling HTML filtering and safe HTML transformation
------------------------------------------------------

By default Plone does HTML filtering to prevent `cross-site scripting <http://en.wikipedia.org/wiki/Cross-site_scripting>`_
attacks. This will make Plone to strip away from HTML

* `<script>` tags

* Some other potentially unsafe tags and attributes

If you need to put a `<script>` tag on your content text in TinyMCE you can disable this security feature.

.. warning::

        If you don't trust all of your site editors, then this will open your site for an attack.

**Step 1:** Turn off Plone’s safe_html transform. Go to /portal_transforms/safe_html in the Management Interface, and enter a 1 in the ‘disable_transform’ box. This prevents Plone from removing tags and attributes while rendering rich text.

**Step 2:** Set the "X-XSS-Protection: 0" response header. This can be done in your frontend webserver such as apache or nginx. Alternatively, if you only need to disable the protection for users who have permission to edit, you can add this to the site’s main_template:

.. code-block:: bash

    tal:define="dummy python:checkPermission('Modify portal content', context) and request.RESPONSE.setHeader('X-XSS-Protection', '0');"

**Step 3:** Add script tag to the list of `extended_valid_elements` of TinyMCE. Go to the Control Panel, TinyMCE settings, Advanced tab. Add to the Other settings field:

.. code-block:: bash

  {"extended_valid_elements": "script[language|type|src]"}


More info

* https://www.tinymce.com/docs/configure/content-filtering/#extended_valid_elements
* http://glicksoftware.com/blog/disable-html-filtering



Content linking
---------------

Plone offers many kind of support and enhancements in site internal content linking

* Delete protection: :doc:`warning if you try to delete content which is being referred </develop/plone/content/deleting>`.

* Migrating of links when the content is being moved

The recommended method for linking the content is *Linking by UID* since *Products.TinyMCE* version 1.3.

* When the text is saved in TinyMCE all relative links are converted to :doc:`UID links </develop/plone/content/uid>` in the saved HTML payload

* When the text is displayed again, the HTML is run through output filter and UID links are converted back to human readable links

This solves issues with earlier Plone versions where the link targets become invalid when a HTML textfield with relative
links where shown on the other page as the original context.

.. note::

   You might need to turn on *Linking by UID* setting on in the site setup if you are migrating from older Plone sites.

Editor preferences
------------------

Plone supports user text changeable editor. The active editor is stored in
the :doc:`user preferences </develop/plone/members/member_profile>`.

The user can fallback to hand-edited HTML by setting active editor to none.

The rich text widget can also support optional input formats besides
HTML: structured text and so on.

Text format selector
====================

The format selector itself is rendered by ``wysiwyg_support.pt`` macros
which is Plone core

* https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/skins/plone_wysiwyg/wysiwyg_support.pt

Applying styles only edit view
------------------------------

You can use TinyMCE body selector make your CSS class have different styles in view and edit modes (inside TinyMCE)

.. code-block:: css


        /* Break columns in two column layout
         *
         * https://developer.mozilla.org/en/css3_columns
         *
         */

        .column-breaker {
                column-break-before: always;
                display: block;
        }

        .mce-content-body .column-breaker {
                color: red;
                border: 1px dashed red;
                display: block;
        }

.. note::

        Firefox does not actually support column breaks, so this was useful headaching experience.


Customizing TinyMCE options
----------------------------

Plone 4 uses TinyMCE 3. Plone 5 upgraded to TinyMCE 4, which works with a new concept called formats and therefore a new syntax for inline styles: `Your Custom Format's Title|custom_format_id|custom_icon_id`.

.. note::

        The icon id will be suffixed and used as a CSS class, so you can hook styles to the `.mce-ico.mce-i-custom_icon_id` selector. For block styles there are no icon hooks so you register them similarly to inline styles but omitting the last part, that is, the icon). That's different from Plone 4's `tinymce.xml`, where you specify `Your Custom Format's Title|tag|custom-css-class`.

This means that after defining styles by associating format titles and ids, you need to define each format by using the `Formats` field. There's already a default JSON structure, so if you add your custom entry after `discreet`, you will end up with:

.. code-block:: json

    {
        "clearfix": {
            "classes": "clearfix",
            "block": "div"
        },
        "discreet": {
            "inline": "span",
            "classes": "discreet"
        },
        "custom_format_id": {
            "block": "div",
            "classes": "custom-css-class additional-class-1 additional-class-2"
        }
    }

Available format options are described in https://www.tinymce.com/docs/configure/content-formatting/#formatparameters

In your add-on code, all TinyMCE options in the control panel can be exported and imported
:doc:`using GenericSetup, portal_setup and registry.xml </develop/addons/components/genericsetup>`. For instance, you could add the following records to your `registry.xml`:

.. code-block:: xml

  <records interface="Products.CMFPlone.interfaces.ITinyMCESchema" prefix="plone">
    <value key="block_styles" purge="False">
      <element>Your Custom Format's Title|custom_format_id</element>
    </value>
    <value key="inline_styles" purge="False">
      <element>Your Custom Format's Title|custom_format_id|custom_format_id</element>
    </value>
    <value key="formats">
    {
      "clearfix": {
        "block": "div",
        "classes": "clearfix"
      },
      "discreet": {
        "inline": "span",
        "classes": "discreet"
      },
      "custom_format_id": {
        "block": "div",
        "classes": "custom-css-class"
      }
    }
    </value>
  </records>

Alternatively you can define "Quick access custom formats", namely those accessible directly in the first level of the `Formats` menu (instead of inside of `Inline` or `Blocks` styles submenus). You can do this by providing information in the more generic `Other Settings` field, located in the TinyMCE's control panel `Advanced` tab, instead of in the `formats` field, so ending up with:

.. code-block:: xml

  <records interface="Products.CMFPlone.interfaces.ITinyMCESchema" prefix="plone">
    <value key="other_settings">
    {
      "style_formats": [
        {
          "title": "Quick access custom format",
          "inline": "span",
          "attributes": {
            "class": "custom-css-class"
          }
        }
      ],
      "style_formats_merge": "True"
    }
    </value>
  </records>


Rich text transformations
-------------------------

* :doc:`/external/plone.app.dexterity/docs/advanced/rich-text-markup-transformations`

* https://pypi.python.org/pypi/plone.app.textfield


Hacking TinyMCE JavaScript
--------------------------

All JavaScript is built and compiled with Plone 5's new Resource Registry.


TinyMCE plug-ins
----------------

The TinyMCE control panel has the ability to provide custom plugins. Custom plugins
map to the http://www.tinymce.com/wiki.php/Configuration:external_plugins setting.

A value is in the format of "plugin name|path/to/javascript.js".

TinyMCE 3 plugins should still work as Plone ships with the TinyMCE backward
compatibility layer for TinyMCE 3.


Adding a new plug-in
---------------------

Here are instructions how to add new plugins to TinyMCE

Plug-in configuration goes to ``registry.xml`` GS profile with the record:

.. code-block:: xml

  <record name="plone.custom_plugins"
          interface="Products.CMFPlone.interfaces.controlpanel.ITinyMCESchema"
          field="custom_plugins">
    <field type="plone.registry.field.List">
      <value_type type="plone.registry.field.TextLine" />
    </field>
    <value>
      <element>myplugin|some/path/to/script.js</element>
    </value>
  </record>


Customizing existing plugin
---------------------------

* Go to the Resource Registry control panel

* Click the ``Overrides`` tab

* Use the search to find the plugin code you want to override

* Save your changes

* Click the ``Registry`` tab

* Click the ``build`` button next to the ``plone-logged-in`` bundle


Overriding plug-in resources
============================

You can also override CSS, HTML (.htm.pt templates) with ``z3c.jbot``
as instructed above.

Example:

.. code-block:: bash

  jbot/Products.CMFPlone.static.components.tinymce-builded.js.tinymce.plugins.autosave.plugin.js

.. warning ::

        Since there resources are loaded in built into one JavaScript file,
        any change this way will require you to re-build the JavaScript.
