===========
Skin layers
===========

.. admonition:: Description

    Skin layers are a legacy Plone 2 technology, still in use, for adding overridable templates and media resources to Plone packages.


Introduction
============

Skin layers, portal_skins and CMFCore.SkinsTool are the old-fashioned way to manage Plone templates.

* Each Plone theme has set of folders it will pick from portal_skins. These sets
  are defined in portal_skins -> properties.

* Skins layers are searched for a template by template name, higher layers first.

* Skin layers can be reordered through-the-web in portal_skins -> properties


Defining A Skin Layer
=====================

Skin files are placed in the *skins* folder of your add-on product.

The structure looks like this:

* yourproduct/namespace/configure.zcml

* yourproduct/namespace/profiles/default/skins.xml

* yourproduct/namespace/skins

* yourproduct/namespace/skins/layer1folder

* yourproduct/namespace/skins/layer2folder/document_view.pt

* yourproduct/namespace/skins/layer2folder

* ...

GenericSetup skins.xml

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_skins" meta_type="Plone Skins Tool">
     <object name="headeranimation" meta_type="Filesystem Directory View"
             directory="plone.app.headeranimation:skins/headeranimation"/>
      <skin-path name="*">
        <layer name="headeranimation" insert-after="custom"/>
      </skin-path>
    </object>

ZCML to register the layer

.. code-block:: xml

    <configure
        ...
        xmlns:cmf="http://namespaces.zope.org/cmf">

        <cmf:registerDirectory name="skins" directory="skins" recursive="True" />

    </configure>

See also

* https://mail.zope.org/pipermail/zope-cmf/2007-February/025650.html

Unit testing and portal_skins
=============================

If you test templates in your unit testing code you might need to call PloneTestCase._refreshSkinData()::

    def afterSetUp(self):
        # Must be called to load our add-on skins folders
        # for unit testing
        self._refreshSkinData()


Activating the current skin layer from a debug/ipzope shell
===========================================================

The skin needs to be initialised before its files can be accessed
e.g. via restrictedTraverse::

     portal.setupCurrentSkin()


Rendering a skin layer template
-------------------------------

Templates must be bound to a context object before rendering.  Plone
acquisition magic maps templates as acquired attributes of all
contentish objects.

Example::

    # Any page object
    doc = portal.doc

    # portal_skins/plone_content/document_view.pt template bound to document
    doc.document_view

    # Resulting HTML is rendered when template object is called
    doc.document_view()


Testing templates
-----------------

Below is some example code how templates behave.

Example:

.. code-block:: python

    (Pdb) doc
    <ATDocument at /plone/doc>
    (Pdb) template = doc.document_view
    (Pdb) template
    <FSPageTemplate at /plone/document_view used for /plone/doc>
    (Pdb) template._filepath
    '/home/moo/workspace2/plone.app.headeranimation/plone/app/headeranimation/skins/headeranimation/document_view.pt'

Nested folder overrides (z3c.jbot)
---------------------------------------

z3c.jbot allows to override any portal_skins based file based on its file-system
path + filename.

Example jbot ZCML slug (no layers, unconditional overrides)

.. code-block:: xml

        <configure
            xmlns="http://namespaces.zope.org/zope"
            xmlns:five="http://namespaces.zope.org/five"
            xmlns:i18n="http://namespaces.zope.org/i18n"
            xmlns:browser="http://namespaces.zope.org/browser"
            >

            <browser:jbot directory="jbot" />

Then your add-on has folder structure (example)::

        yourcompany.app/yourcompany/app/jbot
        yourcompany.app/yourcompany/app/jbot/Products.TinyMCE.skins.tinymce.plugins.table.js.table.js
        yourcompany.app/yourcompany/app/jbot/Products.TinyMCE.skins.tinymce.plugins.table.html.pt

For layered example (theme layer, add-on layer), see

* https://github.com/miohtama/sane_plone_addon_template/blob/master/youraddon/configure.zcml#L41

More info

* https://pypi.python.org/pypi/z3c.jbot

* http://stackoverflow.com/questions/6161802/nested-overrides-in-portal-skins-folder

Poking portal_skins
-------------------

``portal_skins`` is a persistent tool in Plone site root providing functions to manage skin layers.
Its code mostly lives in ``Products.CMFCore.SkinsTool``.

Available skin layers are directly exposed as :doc:`traversable </develop/plone/serving/traversing>` attributes::

        (Pdb) for i in dir(portal_skins): print i
        ATContentTypes
        ATReferenceBrowserWidget
        CMFEditions
        COPY
        COPY__roles__
        ChangeSet
        DELETE
        ...
        plone_form_scripts
        plone_images
        plone_prefs
        plone_scripts
        plone_templates
        plone_wysiwyg

``portal_skins.getSkinSelections()`` will list available skins.

You can edit a specific skin layer::

        skin = portal_skins.getSkinByName("Go Mobile Default Theme")

``portal_skins.selections`` is a :doc:`PersistentDict </develop/plone/persistency/persistent>` object
holding *skin name* -> *comma separated layer list* mappings.



Dumping a portal_skins folder to the filesystem
-----------------------------------------------

qPloneSkinDump can build a filesystem dump from portal_skins but it only works on Plone 2.
If you need this functionality you can try to use this script ripped off qPloneSkinDump:
https://gist.github.com/silviot/5402869. It is a WorksForMe quality script; replace the variables
and run it with::

    bin/instance run export_skin_folder.py
