==========
References
==========

.. admonition:: Description

    Inter-content references in Plone are done using the
    ``reference_catalog`` tool.


Introduction
============

Plone uses a persistent tool called ``reference_catalog`` to store
(Archetypes) object references.  It is used by the out-of-the-box "Related
items" and you can use it in your own content types with ``ReferenceField``.

``reference_catalog`` references can be bidirectional.

The ``reference_catalog`` is a catalog just like the
:doc:`portal_catalog </develop/plone/searching_and_indexing/catalog>` |---| it just uses
different indexes and metadata.

The ``reference_catalog`` is defined in `ReferenceEngine.py <https://github.com/plone/Products.Archetypes/blob/master/Products/Archetypes/ReferenceEngine.py>`_.

Using references
================

Here is an example how to use reference field to make
*programme* -> *researcher* references, and how to do reverse look-ups for
the relationship.

You use ``getReferences()`` and ``getBackReferences()`` methods to look up
relationships.

Example::

    from Products.CMFCore.utils import getToolByName
    from Products.Archetypes.config import REFERENCE_CATALOG

    def getResearcherProgrammes(researcher):
        """
        Find all Programmes which refer to this researcher.

        The Programme<->Researcher relationship is defined in Programme as::

          atapi.ReferenceField(
            name='researchers',
            widget=ReferenceBrowserWidget(
                label="Researchers",
                description="Researchers involved in this project",
                base_query={'object_provides': IResearcher.__identifier__ },
                allow_browse=0,
                show_results_without_query=1,
            ),
            multiValued=1,
            relationship="researchers_in_theme"
          ),

        @param researcher: Content item on the site
        """
        reference_catalog = getToolByName(researcher, REFERENCE_CATALOG)

        # relationship: field name used
        # Plone 4.1: objects=True argument to fetch full objects, not just
        # index brains
        references = reference_catalog.getBackReferences(
                            researcher,
                            relationship="researchers_in_theme")
        # Resolve Reference objects to full objects
        # Return a generator method which will yield all full objects
        return [ ref.getSourceObject() for ref in references ]


.. |---| unicode:: U+02014 .. em dash
