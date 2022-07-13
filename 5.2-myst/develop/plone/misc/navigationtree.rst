================
Navigation trees
================


.. admonition:: Description

        How navigation trees are generate in Plone and how to generate
        custom navigation trees.

Introduction
------------

Plone exposes methods to build navigation trees.

* `Products.CMFPlone.browser.navtree <https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/browser/navtree.py>`_

* `plone.app.layout.navigation.navtree.buildFolderTree <https://github.com/plone/plone.app.layout/blob/master/plone/app/layout/navigation/navtree.py>`_

These are internally used by navigation portlet and sitemap.

Creating a custom navigation tree
----------------------------------

See `Products.PloneHelpCenter <https://github.com/collective/Products.PloneHelpCenter/blob/0f2fac5a7216eb8c0d83736dbcbd6a4385f9b4f4/Products/PloneHelpCenter/content/ReferenceManual.py>`_ for full code.

The following example builds Table of Contents for *Reference Manual* content type::

        class Strategy(NavtreeStrategyBase):

            rootPath = '/'.join(root.getPhysicalPath())
            showAllParents = False

        strategy = Strategy()
        query=  {'path'        : '/'.join(root.getPhysicalPath()),
                 'object_provides' : 'Products.PloneHelpCenter.interfaces.IHelpCenterMultiPage',
                 'sort_on'     : 'getObjPositionInParent'}

        toc = buildFolderTree(self, current, query, strategy)['children']

Excluding items in the navigation tree
----------------------------------------

Your navigation tree strategy must define method ``nodeFilter()``
which can check for portal_catalog metadata column ``exclude_from_nav``.

Example (from Products.CMFPlone.browser.navtree)::

    class SitemapNavtreeStrategy(NavtreeStrategyBase):

            def nodeFilter(self, node):
                item = node['item']
                if getattr(item, 'exclude_from_nav', False):
                    return False
                else:
                    return True


Querying items in natural sort order
--------------------------------------

Sometimes you want to display content items as they appear in Plone navigation.
Below is an example which builds a flat vobulary for a form checbox list
based on a custom portal_catalog query and root folder.

query_items_in_natural_sort_order::

    from plone.app.layout.navigation.navtree import buildFolderTree
    from plone.app.layout.navigation.navtree import NavtreeStrategyBase
    # https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/browser/navtree.py
    from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy, DefaultNavtreeStrategy

    def query_items_in_natural_sort_order(root, query):
        """
        Create a flattened out list of portal_catalog queried items in their natural depth first navigation order.

        @param root: Content item which acts as a navigation root

        @param query: Dictionary of portal_catalog query parameters

        @return: List of catalog brains
        """

        # Navigation tree base portal_catalog query parameters
        applied_query=  {
            'path' : '/'.join(root.getPhysicalPath()),
            'sort_on' : 'getObjPositionInParent'
        }

        # Apply caller's filters
        applied_query.update(query)

        # Set the navigation tree build strategy
        # - use navigation portlet strategy as base
        strategy = DefaultNavtreeStrategy(root)
        strategy.rootPath = '/'.join(root.getPhysicalPath())
        strategy.showAllParents = False
        strategy.bottomLevel = 999
        # This will yield out tree of nested dicts of
        # item brains with retrofitted navigational data
        tree = buildFolderTree(root, root, query, strategy=strategy)

        items = []

        def flatten(children):
            """ Recursively flatten the tree """
            for c in children:
                # Copy catalog brain object into the result
                items.append(c["item"])
                children = c.get("children", None)
                if children:
                    flatten(children)

        flatten(tree["children"])

        return items

How to use::


    def make_terms(items):
        """ Create zope.schema terms for vocab from tuples """
        terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]
        return terms

    def course_source(context):
        """
        Populate vocabulary with values from portal_catalog.

        @param context: z3c.form.Form context object (in our case site root)

        @return: SimpleVocabulary containg all areas as terms.
        """

        # Get site root from any content item using portal_url tool thru acquisition
        root = context.portal_url.getPortalObject()

        context = root.unrestrictedTraverse("courses")

        # We need to include "Folder" in the query even if it's not any of the results -
        # this is because the query criteria must match the root content item too
        brains = query_items_in_natural_sort_order(context, query = { "portal_type" : ["xxx2011.app.courseinfo", "xxx2011.app.subjectgroup", "xxx2011.app.coursecategory", "Folder"] })

        def filter(brain):
            # Remove some unwanted items from the list
            # XXX: Not needed anymore after new content types - remove
            x = brain["Title"]

            if "Carousel" in x:
                return False

            return True

        # Create a list of tuples (UID, Title) of results
        result = [ (brain["UID"], brain["Title"]) for brain in brains if filter(brain) == True ]

        # Convert tuples to SimpleTerm objects
        terms = make_terms(result)

        return SimpleVocabulary(terms)

    directlyProvides(course_source, IContextSourceBinder)
