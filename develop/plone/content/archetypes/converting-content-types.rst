=========================================
Converting one Content Type into another
=========================================

.. admonition:: Description

    It is possible to 'convert' one content type into another by extracting
    content from the source content type and adding it to the new content
    type.

.. contents:: local

Converting Pages into News Items
=======================================

In this example we take a folder of *Pages* (meta type: ``Document``)
and create *News Items* from them::

    """
    from the News Item type, the new items will be content copies
    of their corresponding Pages (Documents)"""

    source_contenttype = 'Document'
    target_contenttype = 'Service'

    items = context.listFolderContents(
            contentFilter={"portal_type": source_contenttype})

    for item in items:
        id = "%s-new" % item.getId()
        title = item.Title()
        description = item.Description()
        text = item.getText()

        service = context.invokeFactory(target_contenttype, id,
                 title=title,description=description,text=text)

.. TODO:: content type "Service"?

Converting Images into News Items
====================================

This is similar to the example of converting pages into news items.
Notice that when we pass the image data to ``invokeFactory`` we need to
make it into a string::

    source_contenttype = 'Image'
    target_contenttype = 'News Item'

    items = context.listFolderContents(
            contentFilter={"portal_type": source_contenttype})

    for item in items:
        id = "%s-new" % item.getId()
        title = item.Title()
        imageCaption = text = description =  item.Description()
        image = str(item.getImage())

        service = context.invokeFactory(
                target_contenttype,
                id,
                title=title,
                description=description,
                imageCaption=imageCaption,
                text=text,
                image=image)

