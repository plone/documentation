===================================================
Moving portlet assignments from one item to another
===================================================

.. admonition:: Description

         This gives some example code for moving portlets and their settings.

.. contents :: :local:

The following method moves portlet assigned from one item to another and copies 
over it blocking settings as well for good measure.

.. code-block:: python

    from logging import getLogger

    from plone.portlets.interfaces import ILocalPortletAssignable
    from plone.portlets.interfaces import ILocalPortletAssignmentManager
    from plone.portlets.interfaces import IPortletAssignmentMapping
    from plone.portlets.interfaces import IPortletManager
    from plone.portlets.constants import CONTEXT_CATEGORY, GROUP_CATEGORY, CONTENT_TYPE_CATEGORY
    
    from zope.interface import alsoProvides
    from zope.component import getMultiAdapter
    from zope.component import getUtility
    from zope.component import getUtilitiesFor
    from zope.component import queryUtility
    from zope.component import provideUtility
    
    logger = getLogger('collective.developermanual')
    
    def move_portlet_assignments_and_settings(src, target):
        if not ILocalPortletAssignable.providedBy(src):
            alsoProvides(src, ILocalPortletAssignable)
            
        for manager_name, src_manager in getUtilitiesFor(IPortletManager, context=src):
            src_manager_assignments = getMultiAdapter((src, src_manager), IPortletAssignmentMapping)
            target_manager = queryUtility(IPortletManager, name=manager_name, context=target)
            if target_manager is None:
                logger.warning('New folder %s does not have portlet manager %s' % 
                               (target.getId(), target_manager))
            else:
                target_manager_assignments = getMultiAdapter((target, target_manager), 
                                                    IPortletAssignmentMapping)
                for id, assignment in src_manager_assignments.items():
                    target_manager_assignments[id] = assignment
                    del src_manager_assignments[id]
                    
                src_assignment_manager = getMultiAdapter((src, src_manager),
                                                     ILocalPortletAssignmentManager)
                target_assignment_manager = getMultiAdapter((target, target_manager),
                                                     ILocalPortletAssignmentManager)
                # 
                # In lineage 0.1 child folders did not inherit their parent's portlets
                # no matter what porlet block settings were set.
                #
                target_assignment_manager.setBlacklistStatus(CONTEXT_CATEGORY, True)
                for category in (GROUP_CATEGORY, CONTENT_TYPE_CATEGORY):
                    target_assignment_manager.setBlacklistStatus(category, 
                                          src_assignment_manager.getBlacklistStatus(category))