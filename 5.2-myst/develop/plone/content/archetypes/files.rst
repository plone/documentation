=====
Files
=====

.. admonition:: Description

    Using files with Archetype field

.. contents:: local

Download URL for files for ATFile content
=========================================

Append ``@@download`` view to URL.

Checking whether a File field has uploaded content
====================================================

Calling AT File field accessor will return a ``File`` object::

    (Pdb) self.context.getAttachment()
    <File at /mfabrik/success-stories/case-studies/finnish-national-broadcasting-company/attachment>

Note that this may return ``None`` if the content item has been constructed
but the form has not been properly saved.

If the size is ``0``, the file is not yet uploaded::

    (Pdb) attach.getSize()
    0

Example how to check in a view whether AT context file size exists::

    @property
    def available(self):

        # Make sure that we have content item of right kind
        if ICaseStudy.providedBy(self.context):

            # Make sure the content item is not anymore in the creation stage
            if self.context.getAttachment() is not None:

                # Check the content of File field
                if self.context.getAttachment().getSize() > 0:
                    return True

        return False

Setting max file size to FileField and ImageField
=====================================================

TODO

http://stackoverflow.com/questions/11347200/setting-max-upload-size-for-archetypes-filefield


Old, deprecated, info

* http://keeshink.blogspot.fi/2009/09/how-to-limit-file-upload-size.html
