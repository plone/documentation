--------------------------
Timestamps
--------------------------

.. admonition:: Description

	How to read created and modified timestamps on
	Plone content items programmatically

.. contents :: local

Introduction
------------

Here are some useful timestamps you can extract from content objects
and examples how to use them.

Timestamps are part of metadata. For Archetypes, metadata is defined
in `ExtensibleMetadata <https://github.com/plone/Products.Archetypes/blob/master/Products/Archetypes/ExtensibleMetadata.py>`_.

:doc:`Zope 2 DateTime </develop/plone/misc/datetime>` date objects are used.

Last modification date
----------------------

Products.Archetypes.ExtensibleMetadata.modified() function will give the last
modification date as Zope DateTime object. This is part of Dublin Core metadata.

Example (Zope console debug mode)::

        >>> app.yoursite.yourpage.modified()
        DateTime('2009/02/04 10:56:25.740 Universal')

Setting modification date explicitly
====================================

You might want to manual set modification date

* When you migrate content

* When you edit content subobjects and want to update the timestamp of parent object to reflect this changes

Example (Zope console debug mode, assume obj is Archetypes content item)::

	>>> obj.modified()
	>>> DateTime('2009/10/05 16:18:32.813 GMT+2')
	
	>>> import DateTime

	>>> now = DateTime.DateTime()
	>>> now
	>>> DateTime('2010/01/20 12:58:38.033 GMT+2')
	
	>>> obj.setModificationDate(now)
	>>> obj.modified()
	>>> DateTime('2010/01/20 12:58:38.033 GMT+2')
	
Viewlet example
===============

Below is an example how to create a custom last modified viewlet.

Viewlet code::

        from zope.component import getMultiAdapter
        from plone.app.layout.viewlets.common import ViewletBase

        class LastModifiedViewlet(ViewletBase):
            """ Viewlet to change the document last modification time.
            """

            def modified(self):
                """

                https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/browser/ploneview.py

                @return: Last modified as a string, local time format
                """

                # Get Plone helper view
                # which we use to convert the date to local format
                plone = getMultiAdapter((self.context, self.request), name="plone")

                time = self.context.modified()

                return plone.toLocalizedTime(time)

Template (lastmodified.py)::

        <div id="last-modified">
                Last modified: <span tal:content="view/modified" />
        </div>

Viewlet registration::

    <!-- Last modification date, register only for contentish context objects -->
    <browser:viewlet
        name="yourapp.lastmodified"
        for="Products.CMFCore.interfaces.IContentish"
        manager="plone.app.layout.viewlets.interfaces.IBelowContent"
        template="viewlets/lastmodified.pt"
        class=".common.LastModifiedViewlet"
        permission="zope2.View"
        />


CSS::

        #last-modified {
                text-align: right;
                font-size: 80%;
                color: #888;
        }



Creation date
-------------

Products.Archetypes.ExtensibleMetadata.created() function will give the
creation date as Zope DateTime object. This is part of Dublin Core metadata.

Example (Zope console debug mode)::

        >>> app.yoursite.yourpage.created()
        DateTime('2009/02/04 10:56:25.740 Universal')


IsExpired()
--------------

* https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/utils.py#L112










