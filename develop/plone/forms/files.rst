================
Files and images
================

.. admonition:: Description

    How to program files and image fields for ``z3c.forms`` and Dexterity
    content types


Introduction
============

This chapter discuss about file uploads and downloads using
zope.schema based forms and content with :doc:`Dexterity content subsystem </develop/plone/content/dexterity>`.

.. note ::

    These instructions apply for Plone 4 and forward. These instructions
    does not apply for Archetypes content or PloneFormGen.

Plone uses "blobs" (large binary objects) to store file-like data in the
ZODB. The ZODB writes these objects to the filesystem as separate files,
but due to security, performance and transaction consideration, the original
filename is not visible. The files are stored in a distributed tree.

For more introduction information, see:

* :doc:`Dexterity developer manual </external/plone.app.dexterity/docs/advanced/files-and-images>`

Simple content item file or image field
=========================================

* * :doc:`Dexterity developer manual </external/plone.app.dexterity/docs/advanced/files-and-images>`

Simple upload form example
===========================

We use `plone.namedfile <https://pypi.python.org/pypi/plone.namedfile>`_
for the upload field, which is a CSV file. We accept the upload and then
process the file.

You need to declare an ``extends`` directive to pin down required dependency
versions in ``buildout.cfg``.
For more information, see :doc:`buildout troubleshooting </manage/troubleshooting/buildout>`.

You also need to declare the following packages as dependencies in
the ``install_dependencies`` directive of your ``setup.py`` file:

* ``plone.autoform``,
* ``plone.directives.form``.

After doing this, rerunning ``buildout`` will pull in these packages for you
and you will be able to import them successfully.
For more information, see `plone.directives.form README <https://pypi.python.org/pypi/plone.directives.form>`_.


Open the *configure.zcml* file and add register the view::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        xmlns:plone="http://namespaces.plone.org/plone"
        i18n_domain="example.dexterityforms">

        ...

        <browser:page
              for="Products.CMFCore.interfaces.ISiteRoot"
              name="import_companies"
              permission="cmf.ManagePortal"
              class=".importusers.ImportUsersForm"
              />

    </configure>

Create a module named *importusers.py*, and add the following code to it::

    # -*- coding: utf-8 -*-

    # Core Zope 2 + Zope 3 + Plone
    from zope.interface import Interface
    from zope import schema
    from zope.component.hooks import getSite
    from Products.CMFCore.interfaces import ISiteRoot
    from Products.CMFCore.utils import getToolByName
    from Products.CMFCore import permissions
    from Products.CMFPlone import PloneMessageFactory as _
    from Products.statusmessages.interfaces import IStatusMessage

    # Form and validation
    from z3c.form import field
    import z3c.form.button
    from plone.directives import form
    import plone.autoform.form

    import StringIO
    import csv


    from plone.namedfile.field import NamedFile
    from plone.i18n.normalizer import idnormalizer


    class IImportUsersFormSchema(form.Schema):
        """ Define fields used on the form """

        csv_file = NamedFile(title=_(u"CSV file"))

    class ImportUsersForm(form.SchemaForm):
        """ A sample form showing how to mass import users using an uploaded CSV file.
        """

        # Form label
        name = _(u"Import Companies")

        # Which plone.directives.form.Schema subclass is used to define
        # fields for this form
        schema = IImportUsersFormSchema

        ignoreContext = True


        def processCSV(self, data):
            """
            """
            io =  StringIO.StringIO(data)

            reader = csv.reader(io, delimiter=',', dialect="excel", quotechar='"')

            header = reader.next()
            print header

            def get_cell(row, name):
                """ Read one cell on a

                @param row: CSV row as list

                @param name: Column name: 1st row cell content value, header
                """

                assert type(name) == unicode, "Column names must be unicode"

                index = None
                for i in range(0, len(header)):
                    if header[i].decode("utf-8") == name:
                        index = i

                if index is None:
                    raise RuntimeError("CSV data does not have column:" + name)

                return row[index].decode("utf-8")


            # Map CSV import fields to a corresponding content item AT fields
            mappings = {
                        u"Puhnro" : "phonenumber",
                        u"Fax" : "faxnumber",
                        u"Postinumero" : "postalCode",
                        u"Postitoimipaikka" : "postOffice",
                        u"Www-osoite" : "homepageLink",
                        u"Lähiosoite" : "streetAddress",
                        }

            updated = 0

            for row in reader:

                # do stuff ...
                updated += 1


            return updated


        @z3c.form.button.buttonAndHandler(_('Import'), name='import')
        def importCompanies(self, action):
            """ Create and handle form button "Create company"
            """

            # Extract form field values and errors from HTTP request
            data, errors = self.extractData()
            if errors:
                self.status = self.formErrorsMessage
                return

            # Do magic
            file = data["csv_file"].data

            number = self.processCSV(file)

            # If everything was ok post success note
            # Note you can also use self.status here unless you do redirects
            if number is not None:
                # mark only as finished if we get the new object
                IStatusMessage(self.request).addStatusMessage(_(u"Created/updated companies:") + unicode(number), "info")


File field contents
===================

Example::

    from zope import schema
    from zope.interface import implements, alsoProvides
    from persistent import Persistent
    from plone import namedfile
    from plone.namedfile.field import NamedBlobFile, NamedBlobImage
    from zope.schema.fieldproperty import FieldProperty

    class IHeaderAnimation(form.Schema):
        """ Alternative header flash animation/imagae """

        animation = NamedBlobFile(title=u"Header flash animation", description=u"Upload SWF file which is shown in the header", required=False)


    # Sample file data used in simulated uploads
    sample_data = (
             'GIF89a\x10\x00\x10\x00\xd5\x00\x00\xff\xff\xff\xff\xff\xfe\xfc\xfd\xfd'
             '\xfa\xfb\xfc\xf7\xf9\xfa\xf5\xf8\xf9\xf3\xf6\xf8\xf2\xf5\xf7\xf0\xf4\xf6'
             '\xeb\xf1\xf3\xe5\xed\xef\xde\xe8\xeb\xdc\xe6\xea\xd9\xe4\xe8\xd7\xe2\xe6'
             '\xd2\xdf\xe3\xd0\xdd\xe3\xcd\xdc\xe1\xcb\xda\xdf\xc9\xd9\xdf\xc8\xd8\xdd'
             '\xc6\xd7\xdc\xc4\xd6\xdc\xc3\xd4\xda\xc2\xd3\xd9\xc1\xd3\xd9\xc0\xd2\xd9'
             '\xbd\xd1\xd8\xbd\xd0\xd7\xbc\xcf\xd7\xbb\xcf\xd6\xbb\xce\xd5\xb9\xcd\xd4'
             '\xb6\xcc\xd4\xb6\xcb\xd3\xb5\xcb\xd2\xb4\xca\xd1\xb2\xc8\xd0\xb1\xc7\xd0'
             '\xb0\xc7\xcf\xaf\xc6\xce\xae\xc4\xce\xad\xc4\xcd\xab\xc3\xcc\xa9\xc2\xcb'
             '\xa8\xc1\xca\xa6\xc0\xc9\xa4\xbe\xc8\xa2\xbd\xc7\xa0\xbb\xc5\x9e\xba\xc4'
             '\x9b\xbf\xcc\x98\xb6\xc1\x8d\xae\xbaFgs\x00\x00\x00\x00\x00\x00\x00\x00'
             '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
             '\x00,\x00\x00\x00\x00\x10\x00\x10\x00\x00\x06z@\x80pH,\x12k\xc8$\xd2f\x04'
             '\xd4\x84\x01\x01\xe1\xf0d\x16\x9f\x80A\x01\x91\xc0ZmL\xb0\xcd\x00V\xd4'
             '\xc4a\x87z\xed\xb0-\x1a\xb3\xb8\x95\xbdf8\x1e\x11\xca,MoC$\x15\x18{'
             '\x006}m\x13\x16\x1a\x1f\x83\x85}6\x17\x1b $\x83\x00\x86\x19\x1d!%)\x8c'
             '\x866#\'+.\x8ca`\x1c`(,/1\x94B5\x19\x1e"&*-024\xacNq\xba\xbb\xb8h\xbeb'
             '\x00A\x00;'
             )

    class HeaderAnimation(Persistent):
        """ Persistent storage object used in IHeaderBehavior.alternatives list.

        This holds information about one animation/image upload.
        """
        implements(IHeaderAnimation)

        animation = FieldProperty(IHeaderAnimation["animation"])

    animation = HeaderAnimation()
    animation.file = namedfile.NamedBlobFile(sample_data, filename=u"flash.swf")

Connstring download URLs
========================

Simple example
----------------

In Dexterity you can specify a ``@@download`` field for content types:

.. code-block:: html

    <!-- Render link to video file if it's uploaded to this context item -->
    <tal:video define="video nocall:context/videoFile"
        tal:condition="nocall:video">
        <a class="flow-player" tal:attributes="href string:${context/absolute_url}/@@download/videoFile/${video/filename}"></a>
    </tal:video>

Complex example
---------------

You need to expose file content to the site user through a view and then
refer to the URL of the view in your HTML template. There are some tricks
you need to keep in mind:

* All file download URLs should be timestamped, or the reupload file change
  will not be reflected in the browser.

* You might want to serve different file types from different URLs and set
  special HTTP headers for them.

Complex example (``plone.app.headeranimations``)::

    from plone.namedfile.interfaces import INamedBlobFile, INamedBlobImage

    # <browser:page> providing blob object traverse and streaming
    # using download_blob() function below
    download_view_name = "@@header_animation_helper"

    def construct_url(context, animation_object_id, blob):
        """ Construct download URL for delivering files.

        Adds file upload timestamp to URL to prevent cache issues.

        @param context: Content object who own the files

        @param animation_object_id: Unique identified for the animation in the animation container
               (in the case there are several of them)

        @param field_value: NamedBlobFile or NamedBlobImage or None

        @return: None if there is no blob or the blob field value is empty (file has been removed from admin interface)
        """

        if blob == None:
            return None

        # This case occurs when the file has been removed thorugh form interfaces
        # (one of keep, replace, remove options on file widget)


        if animation_object_id == None:
            raise RuntimeError("Cannot have None id")

        # Timestamping prevents caching issues,
        # otherwise the browser shows the old version after reupload
        if hasattr(blob, "_p_mtime"):
            # Zope persistency timestamp is float seconds since epoch
            timestamp = blob._p_mtime
        else:
            timestamp = ""

        # We have different BrowserView methods for download depending on the file type
        # (to apply Flash fix)
        if INamedBlobFile.providedBy(blob):
            func_name = "download_animation"
        else:
            func_name = "download_image"

        # This looks like
        return context.absolute_url() + "/" + download_view_name + "/" + func_name + "?timestamp=" + str(timestamp)

Streaming file data
===================

File data is delivered to the browser as a stream. The view function returns
a streaming iterator instead of raw data. This greatly reduces the latency
and memory usage when the file should not be buffered as a whole to
memory before sending.

Example (``plone.app.headeranimation``)::

    from zope.publisher.interfaces import IPublishTraverse, NotFound

    from plone.namedfile.utils import set_headers, stream_data
    from plone.namedfile.interfaces import INamedBlobFile, INamedBlobImage

    def download_blob(context, request, file):
        """ Stream animation or image BLOB to the browser.

        @param context: Context object name is used to set the filename if blob itself doesn't provide one

        @param request: HTTP request

        @param file: Blob object
        """
        if file == None:
            raise NotFound(context, '', request)

        # Try determine blob name and default to "context_id_download"
        # This is only visible if the user tried to save the file to local computer
        filename = getattr(file, 'filename', context.id + "_download")

        # Sets Content-Type and Content-Length
        set_headers(file, request.response)

        # Set headers for Flash 10
        # http://www.littled.net/new/2008/10/17/plone-and-flash-player-10/
        cd = 'inline; filename=%s' % filename
        request.response.setHeader("Content-Disposition", cd)

        return stream_data(file)

    class HeaderAnimationFieldDownload(BrowserView):
        """ Allow file and image downloads in form widgets.

        Unlike HeaderAnimationHelper, this does not do
        any kind of header resolving, but serves files always
        from the context object itself.
        """

        def __init__(self, context, request):
            self.context = context
            self.request = request
            self.behavior = IHeaderBehavior(self.context)

            self.animation_object_id = self.request.form["animation_object_id"]


        def lookUpAnimation(self):
            """ Don't do look-up in init, since failure there will raise ComponentLookupError instead of NotFound.

            @return: Blob object to be streamed
            """
            if not self.animation_object_id in self.behavior.alternatives:
                raise NotFound(self, "Bad animation id:" + self.animation_object_id , self.request)

            return self.behavior.alternatives[self.animation_object_id]

        def download_animation(self):
            """ """
            animation = self.lookUpAnimation()
            return download_blob(self.context, self.request, animation.animation)

        def download_image(self):
            """ """
            animation = self.lookUpAnimation()
            stream_iterator = download_blob(self.context, self.request, animation.image)
            return stream_iterator

``POSKeyError`` on missing blob
===============================

A ``POSKeyError`` is raised when you try to access blob *attributes*, but
the actual file is not available on the disk. You can still load the blob
object itself fine (as it's being stored in the ZODB, not on the
filesystem).

Example::

    Module ZPublisher.Publish, line 119, in publish
    Module ZPublisher.mapply, line 88, in mapply
    Module ZPublisher.Publish, line 42, in call_object
    Module plone.app.headeranimation.browser.views, line 92, in download_image
    Module plone.app.headeranimation.browser.views, line 75, in _download_blob
    Module plone.app.headeranimation.browser.download, line 90, in download_blob
    Module plone.namedfile.utils, line 58, in stream_data
    Module ZODB.Connection, line 811, in setstate
    Module ZODB.Connection, line 876, in _setstate
    Module ZODB.blob, line 623, in loadBlob
    POSKeyError: 'No blob file'

This might occur for example because you have copied the ``Data.fs`` file to
another computer, but not blob files.

You probably want to catch ``POSKeyError`` s and return something more
sane instead::

    def download_blob(context, request, file):
        """ Stream animation or image BLOB to the browser.

        @param context: Context object name is used to set the filename if blob itself doesn't provide one

        @param request: HTTP request

        @param file: Blob object
        """

        from ZODB.POSException import POSKeyError
        try:
            if file == None:
                raise NotFound(context, '', request)

            # Try determine blob name and default to "context_id_download"
            # This is only visible if the user tried to save the file to local computer
            filename = getattr(file, 'filename', context.id + "_download")

            set_headers(file, request.response)

            # Set headers for Flash 10
            # http://www.littled.net/new/2008/10/17/plone-and-flash-player-10/
            cd = 'inline; filename=%s' % filename
            request.response.setHeader("Content-Disposition", cd)

            return stream_data(file)
        except POSKeyError:
            # Blob storage damaged
            logger.warn("Could not load blob for " + str(context))
            raise NotFound(context, '', request)

See also

* https://pypi.python.org/pypi/experimental.gracefulblobmissing/

Widget download URLs
====================

Some things you might want to keep in mind when playing with forms and
images:

* Image data might be incomplete (no width/height) during the first ``POST``.

* Image URLs might change in the middle of request (image was updated).

If your form content is something else than traversable context object then
you must fix file download URLs manually.

Migrating custom content for blobs
==================================

Some hints how to migrate your custom content:

* http://plone.293351.n2.nabble.com/plone-4-upgrade-blob-and-large-files-tp5500503p5500503.html

Form encoding
=============

.. warning::

    Make sure that all forms containing file content are posted as
    ``enctype="multipart/form-data"``.  If you don't do this, Zope decodes
    request ``POST`` values as string input and you get either empty strings
    or filenames as your file content data. The older ``plone.app.z3cform``
    templates do not necessarily declare ``enctype``, meaning that you need
    to use a custom page template file for forms doing uploads.

Example correct form header:

.. code-block:: xml

  <form action="." enctype="multipart/form-data" method="post" tal:attributes="action request/getURL">


File-system access in load-balanced configurations
==================================================

The `plone.namedfiled <https://plone.org/products/plone.app.blob>`_
product page contains configuration instructions
for ``plone.namedfile`` and ZEO.
