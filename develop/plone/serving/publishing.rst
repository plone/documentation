============
Publishing
============

To *publish* an object means to make it available in the Zope traversal
graph and URLS.

A published object may have a reverse-mapping of object to path via
``getPhysicalPath()`` and ``absolute_url()`` but this is not always the
requirement.

You can publish objects by providing a ``browser:page`` view which
implements the ``zope.publisher.interfaces.IPublishTraverse`` interface.

Example publishers
==================

* A widget to make specified files downloadable: `plone.formwidgets.namedfile.widget <https://github.com/plone/plone.formwidget.namedfile/blob/master/plone/formwidget/namedfile/widget.py>`_.

.. XXX: Marked in code as: "Do not use - was not working idea".
.. * `plone.app.headeranimations animations traversing code <https://svn.plone.org/svn/collective/plone.app.headeranimation/trunk/plone/app/headeranimation/browser/traverse.py>`_.
