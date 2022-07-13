==========
Interfaces
==========


Introduction
============

Interfaces define what methods an object provides.
Plone extensively uses interfaces to define APIs between different subsystems.
They provide a more consistent and declarative way to define bridges between two different things,
when duct taping is not enough.

An interface defines the shape of a hole where different pieces fit.
The shape of the piece is defined by the interface, but the implementation details like color, material, etc. can vary.

See `zope.interface package README <https://pypi.python.org/pypi/zope.interface>`_.

Common interfaces
=================

Some interfaces are commonly used throughout Plone.

The usual use case is that a
:doc:`context directive for a view </develop/plone/views/browserviews>`
is provided, specifying where the view is available
(e.g. for which content types).

``zope.interface.Interface``
    Base class of all interfaces. Also used as a ``*`` wildcard when
    registering views, meaning that the view applies on every object.

``Products.CMFCore.interfaces.IContentish``
    All *content* items on the site.
    In the site root, this interface excludes Zope objects like
    ``acl_users`` (the user folder) and ``portal_skins`` which might
    otherwise appear in the item listing when you iterate through the root
    content.

``Products.CMFCore.interfaces.IFolderish``
    All *folders* in the site.

``Products.CMFCore.interfaces.ISiteRoot``
    The Plone site root object.

``plone.app.layout.navigation.interfaces import INavigationRoot``
    Navigation top object - where the breadcrumbs are anchored.
    On multilingual sites, this is the top-level folder for the current
    language.


Implementing one or multiple interfaces
=======================================

Use ``zope.interface.implements()`` in your class body.
Multiple interfaces can be provided as arguments.

Example::

    from zope.interface import implements
    from collective.mountpoint.interfaces import ILocalSyncedContent
    from ora.objects.interfaces import IORAResearcher

    class MyContent(folder.ATFolder):
        """A Researcher synchronized from ORA"""
        implements(IORAResearcher, ILocalSyncedContent)


Removing parent class interface implementations
---------------------------------------------------

``implementsOnly()`` redeclares all inherited interface implementations.
This is useful if you, for example, want to make
:doc:`z3c.form </develop/plone/forms/z3c.form>`
widget bindings more accurate.

Example::

    zope.interface.implementsOnly(IAddressWidget)

Checking whether object provides an interface
=============================================

``providedBy``
--------------

In Python you can use code::

    from yourpackage.interfaces import IMyInterface

    if IMyInterface.providedBy(object):
        # do stuff
    else:
        # was not the kind of object we wanted

``plone_interface_info``
-------------------------

In page templates you can use ``plone_interface_info`` helper view::

    <div tal:define="iinfo context/@@plone_interface_info">
        <span tal:condition="python:iinfo.provides('your.dotted.interface.IName')">
            Do stuff requiring your interface.
        </span>
    </div>

See also

* https://github.com/plone/plone.app.layout/blob/master/plone/app/layout/globals/interface.py


Interface resolution order
---------------------------

Interface resolution order (IRO) is the list of interfaces provided by the
object (directly, or implemented by a class), sorted by priority.

Interfaces are evaluated from zero index (highest priority) to the last index
(lowest priority).

You can access this information for the object for debugging purposes using
a magical attribute::

    object.__provides__.__iro__.

.. note::

    Since adapter factories are *dynamic* (adapter interfaces not hardcoded
    on the object), the object can still adapt to interfaces which are not
    listed in ``__iro__``.


Getting interface string id
===========================

The interface id is stored in the ``__identifier__`` attribute.

Example file ``yourpackage/interfaces.py``::

    import zope.interface

    class IFoo(zope.interface.Interface).
        pass

    # id is yourpackage.interfaces.IFoo
    id = IFoo.__identifier__


Note that this attribute does not respect import aliasing.

Example: ``Products.ATContentTypes.interfaces.IATDocument.__identifier__``
is ``Products.ATContentTypes.interfaces.document.IATDocument``.

Getting interface class by its string id
========================================

Use the `zope.dottedname`_ package.

Example::

    import zope.interface
    from zope.dottedname.resolve import resolve

    class IFoo(zope.interface.Interface).
        pass

    # id is yourpackage.interfaces.IFoo
    id = IFoo.__identifier__
    interface_class == resolve(id)
    assert IFoo == interface_class

Applying interfaces for several content types
=====================================================

You can apply marker interfaces to content types at any time.

Example use cases:

* You want to assign a viewlet to a set of particular content types.

* You want to enable certain behavior on certain content types.

.. note::

    A marker interface is needed only when you need to create a common
    nominator for several otherwise unrelated classes.
    You can use one existing class or interface as a context without
    explicitly creating a marker interface.
    Places accepting ``zope.interface.Interface`` as a context
    usually accept a normal Python class as well (``isinstance`` behavior).

You can assign the marker interface for several classes in ZCML using
a ``<class>`` declaration. Here we're assigning ``ILastModifiedSupport``
to documents, events and news items:

.. code-block:: xml

    <!-- List of content types where "last modified" viewlet is enabled -->
    <class class="Products.ATContentTypes.content.document.ATDocument">
      <implements interface=".interfaces.ILastModifiedSupport" />
    </class>

    <class class="Products.ATContentTypes.content.event.ATEvent">
      <implements interface=".interfaces.ILastModifiedSupport" />
    </class>

    <class class="Products.ATContentTypes.content.newsitem.ATNewsItem">
      <implements interface=".interfaces.ILastModifiedSupport" />
    </class>


Then we can have a view for these content types only using the following::

.. code-block:: python

    from Products.Five import BrowserView
    from interfaces import ILastModifiedSupport
    from plone.app.layout.viewlets.interfaces import IBelowContent

    class LastModified(BrowserView):
        """ View for .interfaces.ILastModifiedSupport only
        """

.. code-block:: xml

    <browser:view
            for=".interfaces.ILastModifiedSupport"
            name="lastmodified"
            class=".views.LastModified"
            template="templates/lastmodified.pt"
            />

Related:

* `zope.dottedname`_ allows you to resolve dotted names to Python objects
  manually

Dynamic marker interfaces
==========================

Zope allows to you to dynamically turn on and off interfaces on any content
objects through the Management Interface.
Browse to any object and visit the :guilabel:`Interfaces` tab.

Marker interfaces might need to be explicitly declared using the
:term:`ZCML` ``<interface>`` directive, so that Zope can find them:

.. code-block:: xml

    <!-- Declare marker interface, so that it is available in the Management Interface -->
    <interface interface="mfabrik.app.interfaces.promotion.IPromotionsPage" />

.. note::

    The interface dotted name must refer directly to the interface class and
    not to an import from other module, like ``__init__.py``.

Setting dynamic marker interfaces programmatically
--------------------------------------------------

Use the ``mark()`` function from `Products.Five`_.

Example::

	from Products.Five.utilities.marker import mark

	mark(portal.doc, interfaces.IBuyableMarker)

.. note::

    This marking persists with the object: it is not temporary.

    Under the hood:
    ``mark()`` delegates to ``zope.interface.directlyProvides()`` |---| with
    the result that
    a persistent object (e.g. content item) has a reference to the interface
    class you mark it with in its ``__provides__`` attribute; this attribute
    is
    serialized and loaded by ZODB like any other reference to a class, and
    `zope.interface`_ uses object specification descriptor magic (just like
    it does
    for any other object, persistent or not) to resolve provided interfaces.

To remove a marker interface from an object, use the ``erase()`` function
from `Products.Five`_.

Example::

	from Products.Five.utilities.marker import erase

	erase(portal.doc, interfaces.IBuyableMarker)


Tagged values
==============

Tagged values are arbitrary metadata you can stick on
``zope.interface.Interface`` subclasses.
For example, the `plone.autoform`_ package uses them to set form widget
hints for `zope.schema`_ data model declarations.

.. _zope.schema: https://pypi.python.org/pypi/zope.schema
.. _plone.autoform: https://pypi.python.org/pypi/plone.autoform
.. _zope.dottedname: https://pypi.python.org/pypi/zope.dottedname
.. _zope.interface: https://pypi.python.org/pypi/zope.interfaces
.. _Products.Five: https://github.com/zopefoundation/Zope/blob/master/src/Products/Five/README.txt
.. |---| unicode:: U+02014 .. em dash
