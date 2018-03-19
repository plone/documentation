==================
Files And Images
==================

.. admonition:: Description

   How to program files and image fields for ``z3c.forms`` and Dexterity content types.


Introduction
=============

This chapter discuss about file uploads and downloads using ``zope.schema`` based
forms and content with :doc:`Dexterity content subsystem </develop/plone/content/dexterity>`.

.. note::

   These instructions apply for Plone 5 and forward.
   These instructions do not apply for Archetypes content or PloneFormGen.

For more introduction information, see:

* :doc:`Dexterity developer manual </external/plone.app.dexterity/docs/advanced/files-and-images>`

Simple Content Item File Or Image Field
=========================================

* * :doc:`Dexterity developer manual </external/plone.app.dexterity/docs/advanced/files-and-images>`

Example
-------

Simple CSV file Upload Form
~~~~~~~~~~~~~~~~~~~~~~~~~~~

`plone.namedfile <https://pypi.python.org/pypi/plone.namedfile>`_ is used for the upload field.

Then the the upload is accepted and the file processed.

A view with the form is registered using the ``configure.zcml`` file.

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        xmlns:plone="http://namespaces.plone.org/plone"
        i18n_domain="example.dexterityforms">

        ...

        <browser:page
            for="Products.CMFCore.interfaces.ISiteRoot"
            name="import_csv"
            permission="cmf.ManagePortal"
            class=".importcsv.ImportCSVForm"
        />

    </configure>

Create a module named *importcsv.py*, and add the following code to it

.. code-block:: python

    # -*- coding: utf-8 -*-
    from plone.autoform import form
    from plone.namedfile.field import NamedFile
    from Products.CMFPlone import PloneMessageFactory as _
    from Products.statusmessages.interfaces import IStatusMessage

    import csv
    import StringIO
    import z3c.form.button


    class IImportCSVFormSchema(form.Schema):
        """ Define fields used on the form """

        csv_file = NamedFile(title=_(u'CSV file'))


    class ImportCSVForm(form.SchemaForm):
        """ A sample form showing how to mass import users using an uploaded CSV file.
        """

        name = _(u'Import Companies')  # Form label
        schema = IImportCSVFormSchema  # Form schema
        ignoreContext = True

        def processCSV(self, data):
            """
            """
            reader = csv.reader(
                StringIO.StringIO(data),
                delimiter=',',
                dialect='excel',
                quotechar='"'
            )
            header = reader.next()

            updated = 0

            for row in reader:
                # process the data here as needed for the specific case
                for idx, name in header:
                    value = row[idx]
                updated += 1

            return updated

        @z3c.form.button.buttonAndHandler(_('Import CSV'), name='import')
        def importCSV(self, action):
            """ Create and handle form button
            """

            # Extract form field values and errors from HTTP request
            data, errors = self.extractData()
            if errors:
                self.status = self.formErrorsMessage
                return

            # get the actual data
            file = data["csv_file"].data

            # do the processing
            number = self.processCSV(file)

            # If everything was ok post success note
            # Note you can also use self.status here unless you do redirects
            if number is not None:
                # mark only as finished if we get the new object
                IStatusMessage(
                    self.request
                ).addStatusMessage(
                    _(u'Processed: {0}').format(number),
                    'info'
                )


Programmatically Filling A Field With Content
=============================================

Given a field ``plone.namedfile.field.NamedBlobFile`` named ``some_file``.

It can be filled programmatically with data by creating a blob first.

.. code-block:: python

    # Attention, this is the blob-file object itself,
    # opposed to the field with the same class-name used above!
    from plone.namedfile.file import NamedBlobFile

    blob_data = NamedBlobFile(some_data_string, filename=u'video.mp4')

It can be set on some persistent context, like an arbitary dexterity content type.

.. code-block:: python

    context.some_file = blob_data


Getting Download URLs
=====================

Simple Download URLs
--------------------

To create a download link for file and image fields of Dexterity content types
the ``@@download`` view can be used.

The common schema is ``http://host/path/to/filecontent/@@download/FIELDNAME``.

To get a URL containing the original filename it may be appended this way:
``http://host/path/to/filecontent/@@download/FIELDNAME/FILENAME.EXT``.

As in the example below, the original uploaded filename may be used.
But a new/custom filename is fine too.

.. code-block:: html

    <!--
      Precondition: Custom content type with a "video_file" field.
                    Flowplayer JavaScript installed.
      Renders: Link to video file, only if it's uploaded to this context item.
    -->
    <tal:if define="video_file nocall:context/video_file"
            tal:condition="nocall:video_file">
      <a class="flow-player"
         tal:attributes="href string:${context/absolute_url}/@@download/video_file/${video_file/filename}">
        Video
      </a>
    </tal:if>

Timestamped Download URL
------------------------

You need to expose file content to the site user through a view
and then refer to the URL of the view in your HTML template.

There are some tricks you need to keep in mind:

* All file download URLs should be timestamped, or the re-upload file change
  will not be reflected in the browser.

* You might want to serve different file types from different URLs and set special HTTP headers for them.

Example:

.. code-block:: python

    from plone.namedfile.interfaces import INamedBlobFile

    # <browser:page> providing blob object traverse and streaming
    # using download_blob() function below
    download_view_name = "@@header_animation_helper"


    def construct_url(context, animation_object_id, blob):
        """ Construct download URL for delivering files.

        Adds file upload timestamp to URL to prevent cache issues.

        @param context: Content object who own the files

        @param video_object_id: Unique identified for the animation in the
               animation container
               (in the case there are several of them)

        @param field_value: NamedBlobFile or NamedBlobImage or None

        @return: None if there is no blob or the blob field value is empty
                 (file has been removed from admin interface)
        """

        if blob is None:
            return None

        # This case occurs when the file has been removed thorugh form interfaces
        # (one of keep, replace, remove options on file widget)

        if animation_object_id is None:
            raise RuntimeError('Cannot have None id')

        # Timestamping prevents caching issues,
        # otherwise the browser shows the old version after reupload
        if hasattr(blob, "_p_mtime"):
            # Zope persistency timestamp is float seconds since epoch
            timestamp = blob._p_mtime
        else:
            timestamp = ''

        # We have different BrowserView methods for download depending on the
        # file type
        if INamedBlobFile.providedBy(blob):
            func_name = "download_video"
        else:
            func_name = "download_image"

        # This looks like
        return '{0}/{1}/{2}?timestamp={3}'.format(
            context.absolute_url(),
            download_view_name,
            func_name,
            timestamp
        )


Streaming File Data
===================

File data is delivered to the browser as a stream.
The view function returns a streaming iterator instead of raw data.

This greatly reduces the latency and memory usage when the file should
not be buffered as a whole to memory before sending.

Example of a streaming browser view:

.. code-block:: python

    from plone.namedfile.utils import set_headers
    from plone.namedfile.utils import stream_data
    from Products.Five import BrowserView
    from zope.publisher.interfaces import NotFound


    class StreamingFieldDownload(BrowserView):
        """ Stream file and image downloads.
        """

        def __init__(self, context, request):
            self.context = context
            self.request = request

        def __call__(self):
            """Stream BLOB of context ``file`` field to the browser.

            @param file: Blob object
            """
            blob = self.context.file
            if blob is None:
                raise NotFound('No file present')
            # Try determine blob name and default to "context_id_download."
            # This is only visible if the user tried to save the file to local
            # computer.
            filename = getattr(blob, 'filename', self.context.id + '_download')

            # Sets Content-Type and Content-Length
            set_headers(blob, self.request.response)

            # Set Content-Disposition
            self.request.response.setHeader(
                'Content-Disposition',
                'inline; filename={0}'.format(filename)
            )
            return stream_data(blob)


POSKeyError On Missing Blob
===========================

A ``POSKeyError`` is raised when you try to access blob *attributes*,
but the actual file is not available on the disk.

You can still load the blob object itself fine (as it's being stored in the ZODB, not on the filesystem).

Example traceback snippet::

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

This might occur for example because you have copied the ``Data.fs`` file to another computer,
but not (all) blob files.

You probably want to catch ``POSKeyError`` s and return something more sane instead

.. code-block:: python

    from plone.namedfile.utils import set_headers
    from plone.namedfile.utils import stream_data
    from Products.Five import BrowserView
    from ZODB.POSException import POSKeyError
    from zope.publisher.interfaces import NotFound

    import logging

    logger = logging.getLogger(__name__)


    class StreamingFieldDownload(BrowserView):
        """ Stream file and image downloads.
        """

        def __init__(self, context, request):
            self.context = context
            self.request = request

        def __call__(self):
            """Stream BLOB of context ``file`` field to the browser.

            @param file: Blob object
            """
            blob = self.context.file
            if blob is None:
                raise NotFound('No file present')
            # Try determine blob name and default to "context_id_download."
            # This is only visible if the user tried to save the file to local
            # computer.
            try:
                filename = getattr(blob, 'filename', self.context.id + '_download')

                # Sets Content-Type and Content-Length
                set_headers(blob, self.request.response)

                # Set Content-Disposition
                self.request.response.setHeader(
                    'Content-Disposition',
                    'inline; filename={0}'.format(filename)
                )
                return stream_data(blob)
            except POSKeyError:
                logger.exception(
                    'Could not load blob for {0}'.format(str(self.context))
                )
                raise NotFound('Blob file is missing in blob storage.')

See also

* https://pypi.python.org/pypi/experimental.gracefulblobmissing/

Widget Download URLs
====================

Some things you might want to keep in mind when playing with forms and images:

* Image data might be incomplete (no width/height) during the first ``POST``.

* Image URLs might change in the middle of request (image was updated).

If your form content is something else than traversable context object then you must fix file download URLs manually.


Migrating Custom Content For Blobs
====================================

Some hints how to migrate your custom content:

* http://plone.293351.n2.nabble.com/plone-4-upgrade-blob-and-large-files-tp5500503p5500503.html


Form Encoding
=============

.. warning::

   Make sure that all forms containing file content are posted as ``enctype="multipart/form-data"``.
   If you don't do this, Zope decodes request ``POST`` values as string input and you get either empty strings or filenames as your file content data.

   The older ``plone.app.z3cform`` templates do not necessarily declare ``enctype``,
   meaning that you need to use a custom page template file for forms doing uploads.

Example correct form header:

.. code-block:: xml

  <form action="."
        enctype="multipart/form-data"
        method="post"
        tal:attributes="action request/getURL">
