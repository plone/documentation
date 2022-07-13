===============================
Importing And Exporting Content
===============================

.. admonition:: Description

        Importing and exporting content between Plone sites and other CMS systems


Introduction
------------

Goal: you want to import and export content between Plone sites.

* If both sites have identical version and add-on product configuration you can use the Management Interface export/import

* If they don't (e.g. have different Plone version on source and target site),
  you need to use add-on products to export and import the content to a common
  format, e.g. JSON files.

Zope 2 import / export
--------------------------

Zope 2 can import/export parts of the site in .zexp format. This is basically Python pickle data of the exported objects. The data is a raw dump of Python internal data structures, which means that the source and the target Plone versions must be compatible. For example, a export from Plone 3 to Plone 4 is not possible.

.. note::

    This method is applicable under very limited circumstances.
    Also note that for large Plone sites, the .zexp files generated is quite large,
    which could lead to memory errors.
    It is recommended to use this method only after trying other, more general methods.

To export objects from a site to another, do the following:

* In the Management Interface, navigate to the Folder, which holds the object to be exported.

* Tick the checkbox for a object to be exported.

* Click *Import / Export*

* Export as .zexp.

* Zope 2 will tell you the path where .zexp was created on the server.

* Zope .zexp to *youranothersite*/var/instance/import folder

* Go to the Management Interface root of your other site

* Press Import / Export

* In *Import from file* you should see now your .zexp file

* Import it

* Go to portal_catalog -> Advanced tab. *Clear and Rebuild* the catalog (raw Zope pickle does not know about anything living inside the catalog)


collective.transmogrifier
-------------------------

On it's own `collective.transmogrifier <https://pypi.python.org/pypi/collective.transmogrifier>`_ isn't an import tool,
rather a generic framework for creating pipelines to process data.
Pipeline configs are .ini-style files that join together blueprints to quickly create a tool for processing data.

The following add-ons make it useful in a Plone context:

* `plone.app.transmogrifier <https://pypi.python.org/pypi/plone.app.transmogrifier>`_ provides integration with GenericSetup,
  so you can run pipelines as part of import steps,
  and some useful blueprints.
* `quintagroup.transmogrifier <http://projects.quintagroup.com/products/wiki/quintagroup.transmogrifier>`_ also provides it's own Plone integration,
  and some useful blueprints.
  See the site for some example configs for migration.
* `transmogrify.dexterity <https://github.com/collective/transmogrify.dexterity>`_ provides some blueprints relevant to Dexterity types,
  and has some default pipelines for you to use.
* `collective.jsonmigrator <https://github.com/collective/collective.jsonmigrator>`_ is particularly useful when the old site is not able to install collective.transmogrifier, as collective.jsonmigrator has a low level of dependencies for that end of the migration.

transmogrify.dexterity: CSV import
==================================

``transmogrify.dexterity`` will register the pipeline ``transmogrify.dexterity.csvimport``,
which can be used to import from CSV to dexterity objects.

For more information on using, see `the package documentation <https://github.com/collective/transmogrify.dexterity>`_.

transmogrify.dexterity: JSON import/export
==========================================

``transmogrify.dexterity`` also contains some ``quintagroup.transmogrifier`` pipeline configs.
To use these, first install both ``quintagroup.transmogrifier`` and ``transmogrify.dexterity``,
then add the following to your ZCML::

    <include package="transmogrify.dexterity.pipelines" file="files.zcml" />

Then the "Content (transmogrifier)" generic setup import / export will import / export site content to JSON files.

For more information on using, see `this transmogrify blog post <http://shuttlethread.com/blog/development-with-transmogrify.dexterity>`_.

quintagroup.transmogrifier: Exporting single folder only
========================================================

Here is explained how to export and import `Plone CMS <https://plone.org>`_
folders between different Plonen versions, or
different CMS systems, using  XML based content marshalling and
`quintagroup.transmogrifier <http://projects.quintagroup.com/products/wiki/quintagroup.transmogrifier>`_.

This overcomes some problems with Zope management based export/import which uses `Python pickles
<http://docs.python.org/library/pickle.html>`_ and thus needs identical codebase on the source
and target site. Exporting and importing between Plone 3 and Plone 4 is possible.

You can limit export to cover source content to with arbitrary :doc:`portal_catalog </develop/plone/searching_and_indexing/query>` conditions.
If you limit source content by path you can effectively export single folder only.

The recipe described here assumes the exported and imported site have the same path for the folder.
Manually rename or move the folder on source or target to change its location.

.. note::

        The instructions here requires quintagroup.transmogrify version 0.4 or later.

Source site
-----------

Execute these actions on the source Plone site.

Install ``quintagroup.transmogrifier`` via buildout and Plone add-on control panel.

Go to *Site setup* > *Content migration*.

Edit export settings. Remove unnecessary pipeline entries by looking the example below. Add a new ``catalogsource`` blueprint.
The ``exclude-contained`` option makes sure we do not export unnecessary items from the parent folders::

        [transmogrifier]
        pipeline =
            catalogsource
            fileexporter
            marshaller
            datacorrector
            writer
            EXPORTING

        [catalogsource]
        blueprint = quintagroup.transmogrifier.catalogsource
        path = query= /isleofback/ohjeet
        exclude-contained = true

Also we need to include some field-level excluding bits for the folders, because the target site does not necessary
have the same content types available as the source site and this may prevent
setting up folderish content settings::

        [marshaller]
        blueprint = quintagroup.transmogrifier.marshaller
        exclude =
          immediatelyAddableTypes
          locallyAllowedTypes

You might want to remove other, unneeded blueprints from the export ``pipeline``.
For example, ``portletexporter`` may cause problems if the source and target site
do not have the same portlet code.

Go to the *Management Interface* > *portal_setup* > *Export* tab. Check Content (transmogrifier) step.
Press *Export Selected Steps* at the bottom of the page. Now a .tar.gz file will be downloaded.

During the export process ``instance.log`` file is updated with status info. You might want to follow
it in real-time from UNIX command line

.. code-block:: console

        tail -f var/log/instance.log

In log you should see entries running like::

        2010-12-27 12:05:30 INFO EXPORTING _path=sisalto/ohjeet/yritys/yritysten-tuotetiedot/tuotekortti
        2010-12-27 12:05:30 INFO EXPORTING
        Pipeline processing time: 00:00:02
                  94 items were generated in source sections
                  94 went through full pipeline
                   0 were discarded in some section

Target site
-----------

Execute these actions on the target Plone site.

Install ``quintagroup.transmogrifier`` via buildout and Plone add-on control panel.

Open target site ``instance.log`` file for monitoring the import process

.. code-block:: console

        tail -f var/log/instance.log

Go to the *Management Interface* > *portal_setup* > *Import* tab.

Choose downloaded ``setup_toolxxx.tar.gz`` file at the bottom of the page,
for *Import uploaded tarball* input.

Run import and monitoring log file for possible errors. Note that the import
completes even if the target site would not able to process incoming content.
If there is a serious problem the import seems to complete successfully,
but no content is created.

.. note::

    Currently export/import is not perfect.
    For example, the Management Interface content type icons  are currently
    lost in the process. It is recommended to do a test run on a staging server
    before doing this process on a production server.
    Also, the item order in the folder is being lost.

More information
----------------

* :doc:`How to perform portal_catalog queries </develop/plone/searching_and_indexing/query>`

* http://webteam.medsci.ox.ac.uk/integrators-developers/transmogrifier-i-want-to-.../

* https://github.com/collective/quintagroup.transmogrifier/blob/master/quintagroup/transmogrifier/catalogsource.py

collective.jsonmigrator
=======================

collective.jsonmigrator is basically a collective.transmogrifier pipeline that pulls Plone content from to JSON views on an old site and writes it into your new site.
It's major advantage is that the JSON view product: collective.jsonify is very low on dependencies (basically just simplejson),
it can be installed on old Plone sites that would be difficult if not impossible to install collective.transmogrifier into.

See:

* <https://github.com/collective/collective.jsonmigrator>`_

* <https://github.com/collective/collective.jsonify>`_

* A basic tutorial: <http://www.jowettenterprises.com/blog/plone-content-migration-using-transmogrifier-and-collective.jsonify>`_

* <http://stackoverflow.com/questions/13721016/exporting-plone-archetypes-data-in-json>`_

Fast content import
-------------------

For specific use-cases, you can create 'brains' first and import later
* See `this blog post <http://blog.redturtle.it/redturtle-blog/fast-content-import>`_

Simple JSON export
----------------------

Below is a simple helper script / BrowserView for a JSON export of Plone folder content.
Works Plone 3.3+. It handles also binary data and nested folders.

export.py::

    """

        Export folder contents as JSON.

        Can be run as a browser view or command line script.

    """

    import os
    import base64

    try:
        import json
    except ImportError:
        # Python 2.54 / Plone 3.3 use simplejson
        # version 2.3.3
        import simplejson as json

    from Products.Five.browser import BrowserView
    from Products.CMFCore.interfaces import IFolderish
    from DateTime import DateTime

    #: Private attributes we add to the export list
    EXPORT_ATTRIBUTES = ["portal_type", "id"]

    #: Do we dump out binary data... default we do, but can be controlled with env var
    EXPORT_BINARY = os.getenv("EXPORT_BINARY", None)
    if EXPORT_BINARY:
        EXPORT_BINARY = EXPORT_BINARY == "true"
    else:
        EXPORT_BINARY = True


    class ExportFolderAsJSON(BrowserView):
        """
        Exports the current context folder Archetypes as JSON.

        Returns downloadable JSON from the data.
        """

        def convert(self, value):
            """
            Convert value to more JSON friendly format.
            """
            if isinstance(value, DateTime):
                # Zope DateTime
                # https://pypi.python.org/pypi/DateTime/3.0.2
                return value.ISO8601()
            elif hasattr(value, "isBinary") and value.isBinary():

                if not EXPORT_BINARY:
                    return None

                # Archetypes FileField and ImageField payloads
                # are binary as OFS.Image.File object
                data = getattr(value.data, "data", None)
                if not data:
                    return None
                return base64.b64encode(data)
            else:
                # Passthrough
                return value

        def grabArchetypesData(self, obj):
            """
            Export Archetypes schemad data as dictionary object.

            Binary fields are encoded as BASE64.
            """
            data = {}
            for field in obj.Schema().fields():
                name = field.getName()
                value = field.getRaw(obj)
                print "%s" % (value.__class__)

                data[name] = self.convert(value)
            return data

        def grabAttributes(self, obj):
            data = {}
            for key in EXPORT_ATTRIBUTES:
                data[key] = self.convert(getattr(obj, key, None))
            return data

        def export(self, folder, recursive=False):
            """
            Export content items.

            Possible to do recursively nesting into the children.

            :return: list of dictionaries
            """

            array = []
            for obj in folder.listFolderContents():
                data = self.grabArchetypesData(obj)
                data.update(self.grabAttributes(obj))

                if recursive:
                    if IFolderish.providedBy(obj):
                        data["children"] = self.export(obj, True)

                array.append(data)

            return array

        def __call__(self):
            """
            """
            folder = self.context.aq_inner
            data = self.export(folder)
            pretty = json.dumps(data, sort_keys=True, indent='    ')
            self.request.response.setHeader("Content-type", "application/json")
            return pretty


    def spoof_request(app):
        """
        http://docs.plone.org/develop/plone/misc/commandline.html
        """
        from AccessControl.SecurityManagement import newSecurityManager
        from AccessControl.SecurityManager import setSecurityPolicy
        from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy, OmnipotentUser
        _policy = PermissiveSecurityPolicy()
        setSecurityPolicy(_policy)
        newSecurityManager(None, OmnipotentUser().__of__(app.acl_users))
        return app


    def run_export_as_script(path):
        """ Command line helper function.

        Using from the command line::

            bin/instance script export.py yoursiteid/path/to/folder

        If you have a lot of binary data (images) you probably want

            bin/instance script export.py yoursiteid/path/to/folder > yourdata.json

        ... to prevent your terminal being flooded with base64.

        Or just pure data, no binary::

            EXPORT_BINARY=false bin/instance run export.py yoursiteid/path/to/folder

        :param path: Full ZODB path to the folder
        """
        global app

        secure_aware_app = spoof_request(app)
        folder = secure_aware_app.unrestrictedTraverse(path)
        view = ExportFolderAsJSON(folder, None)
        data = view.export(folder, recursive=True)
        # Pretty pony is prettttyyyyy
        pretty = json.dumps(data, sort_keys=True, indent='    ')
        print pretty


    # Detect if run as a bin/instance run script
    if "app" in globals():
        run_export_as_script(sys.argv[1])



