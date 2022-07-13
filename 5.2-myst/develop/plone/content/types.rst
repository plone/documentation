=============
Content types
=============

.. admonition:: Description

   Plone's content type subsystems and creating new content types programmatically.

.. note::

   While using Archetypes is fully supported in the Plone 5.x series, the recommendation is to
   use Dexterity content types for any new development.

   Archetypes support will be removed from core Plone in version 6.



Introduction
=============

Plone has two kind of content types subsystems:

* :doc:`Archetypes </develop/plone/content/archetypes/index>`-based

* :doc:`Dexterity </develop/plone/content/dexterity>`-based (new)

See also Plomino (later in this document).

Flexible architecture allows other kinds of content type subsystems as well.

Type information registry
=========================

Plone maintains available content types in the ``portal_types`` tool.

``portal_types`` is a folderish object which stores type information as
child objects,
keyed by the ``portal_type`` property of the types.

``portal_factory`` is a tool responsible for creating the persistent object representing the content.

`TypesTool source code <http://svn.zope.org/Products.CMFCore/trunk/Products/CMFCore/TypesTool.py?rev=101748&view=auto>`_.

Listing available content types
--------------------------------

Often you need to ask the user to choose specific Plone content types.

Plone offers two Zope 3 vocabularies for this purpose:

``plone.app.vocabularies.PortalTypes``
    a list of types installed in ``portal_types``
``plone.app.vocabularies.ReallyUserFriendlyTypes``
    a list of those types that are likely to mean something to users.

If you need to build a vocabulary of user-selectable content types in
Python instead, here's how::

    from Acquisition import aq_inner
    from zope.app.component.hooks import getSite
    from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
    from Products.CMFCore.utils import getToolByName

    def friendly_types(site):
        """ List user-selectable content types.

        We cannot use the method provided by the IPortalState utility view,
        because the vocabulary factory must be available in contexts where
        there is no HTTP request (e.g. when installing add-on product).

        This code is copied from
        https://github.com/plone/plone.app.layout/blob/master/plone/app/layout/globals/portal.py

        @return: Generator for (id, type_info title) tuples
        """

        context = aq_inner(site)
        site_properties = getToolByName(context, "portal_properties").site_properties
        not_searched = site_properties.getProperty('types_not_searched', [])

        portal_types = getToolByName(context, "portal_types")
        types = portal_types.listContentTypes()

        # Get list of content type ids which are not filtered out
        prepared_types = [t for t in types if t not in not_searched]

        # Return (id, title) pairs
        return [ (id, portal_types[id].title) for id in prepared_types ]

Creating a new content type
============================

These instructions apply to
:doc:`Archetypes</develop/plone/content/archetypes/index>`-based content types.

Install ZopeSkel
----------------

Add ZopeSkel to your buildout.cfg and run buildout::

    [buildout]
    ...
    parts =
        instance
        zopeskel

    ...
    [zopeskel]
    recipe = zc.recipe.egg
    eggs =
       PasteScript
       ZopeSkel


Create an archetypes product
----------------------------

Run the following command and answer the questions e.g. for the
project name use my.product::

    ./bin/paster create -t archetype

Install the product
-------------------

Adjust your buildout.cfg and run buildout again::

    [buildout]
    develop = my.product
    ...
    parts =
        instance
        zopeskel

    ...
    [instance]
    eggs = my.product

.. note::

   You need to install your new product using buildout before you
   can add a new content type in the next step. Otherwise paster
   complains with the following message: "Command 'addcontent' not
   known".

Create a new content type
-------------------------

.. deprecated:: may_2015
    Use :doc:`bobtemplates.plone </develop/addons/bobtemplates.plone/README>` instead

Change into the directory of the new product and then use paster to
add a new content type::

    cd my.product
    ../bin/paster addcontent contenttype



Related how-tos:

* http://lionfacelemonface.wordpress.com/tutorials/zopeskel-archetypes-howto/

* http://docs.openia.com/howtos/development/plone/creating-a-site-archetypes-object-and-contenttypes-with-paster?set_language=fi&cl=fi

* http://www.unc.edu/~jj/plone/

.. note::

    Creating types by hand is not worth the trouble. Please use a
    code generator to create the skeleton for your new content type.

.. warning::

    The content type name must not contain spaces.
    Neither the content type name or the description
    may contain non-ASCII letters. If you need to change these please
    create a translation catalog which will translate the text to
    one with spaces or international letters.


Debugging new content type problems
-----------------------------------

Creating types by hand is not worth the trouble.

* `Why doesn't my custom content type show up in add menu <https://plone.org/documentation/faq/why-doesnt-my-custom-content-type-show-up-in-add-menu/>`_ checklist.

Creating new content types through-the-web
=============================================

There are solutions for non-programmers and Plone novices to create their content types.

Dexterity
---------

* http://docs.plone.org/external/plone.app.dexterity/docs/

* Core feature

* Use Dexterity control panel in site setup

* Use :doc:`bobtemplates.plone </develop/addons/bobtemplates.plone>`

Plomino (Archetypes-based add-on)
---------------------------------

* With Plomino you can make an entire web application that can organize &
  manipulate data with very limited programming experience.

* http://www.plomino.net/

* http://www.youtube.com/view_play_list?p=469DE37C742F31D1

Implicitly allowed
==================

:guilabel:`Implictly allowed` is a flag specifying whether the content is
globally addable or
must be specifically enabled for certain folders.

The following example allows creation of :guilabel:`Large Plone Folder`
anywhere at the site
(it is disabled by default). For available properties, see
``TypesTool._advanced_properties``.

Example::

    portal_types = self.context.portal_types
    lpf = portal_types["Large Plone Folder"]
    lpf.global_allow = True # This is "Globally allowed" property


Constraining the addable types per type instance
================================================

For the instances of some content types, the user may manually
restrict which kinds of objects may be added inside. This is done by clicking
the :guilabel:`Add new...` link on the green edit bar and then choosing
:guilabel:`Restrictions...`.

This can also be done programmatically on an instance of a content type that
supports it.

First, we need to know whether the instance supports this.

Example::

    from Products.Archetypes.utils import shasattr # To avoid acquisition
    if shasattr(context, 'canSetConstrainTypes'):
        # constrain the types
        context.setConstrainTypesMode(1)
        context.setLocallyAllowedTypes(('News Item',))

If ``setConstrainTypesMode`` is ``1``, then only the types enabled by using
``setLocallyAllowedTypes`` will be allowed.

The types specified by ``setLocallyAllowedTypes`` must be a subset
of the allowable
types specified in the content type's FTI (Factory Type Information) in the
``portal_types`` tool.

If you want the types to appear in the :guilabel:
``Add new..`` dropdown menu, then you must
also set the immediately addable types. Otherwise, they will appear under the
:guilabel:`more` submenu of :guilabel:`Add new..`.

Example::

    context.setImmediatelyAddableTypes(('News Item',))

The immediately addable types must be a subset of the locally allowed types.

To retrieve information on the constrained types, you can just use the accessor
equivalents of the above methods.

Example::

    context.getConstrainTypesMode()
    context.getLocallyAllowedTypes()
    context.getImmediatelyAddableTypes()
    context.getDefaultAddableTypes()
    context.allowedContentTypes()

**Be careful of Acquisition**. You might be acquiring these methods from the
current instance's parent. It would be wise to first check whether the current
object has this attribute,
either by using ``shasattr`` or by using ``hasattr`` on the
object's base (access the base object using ``aq_base``).

The default addable types are the types that are addable when
``constrainTypesMode`` is ``0`` (i.e not enabled).

For more information, see **Products/CMFPlone/interfaces/constraints.py**

