=========
Workflows
=========

.. admonition:: Description

        Programming workflows in Plone.


Introduction
-------------

The DCWorkflow product manages the default Plone workflow system.

A workflow state is not directly stored on the object. Instead, a separate
portal_workflow tool must be used to access a workflow state. Workflow look-ups
involve an extra database fetch.

For more information, see

* http://www.martinaspeli.net/articles/dcworkflows-hidden-gems

Creating workflows
------------------

The recommended method is to use portal_workflow in the Management Interface
to construct the workflow through-the-web and then you can export it using GenericSetup's portal_setup tool.

Include necessary parts from exported workflows.xml and workflows folder in your add-on product
GenericSetup profile (add-on folder profiles/default).

Model the workflow online
=========================

Go to 'http:yourhost.com:8080/yourPloneSiteName/portal_workflow/manage_main', copy and paste
'simple_publication_workflow', to have a skeleton for start-off, rename 'copy_of_simple_publication_workflow'
to 'your_workflow' or add a new workflow via the dropdwon-menu and have a tabula rasa.

Add and remove states and transitions, assign permissions etc.



Putting it in your product
==========================
Go to 'http:yourhost.com:8080/yourPloneSiteName/portal_setup/manage_exportSteps', check 'Workflow Tool' and hit
'Export selected steps', unzip the downloaded file and put the definition.xml-file in
'your/product/profiles/default/workflows/your_workflow/' (you'll need to create the latter two directories).


Configure workflow via GenericSetup
------------------------------------

Assign a workflow
==================

In your/product/profiles/default/workflows.xml, insert:

.. code-block:: xml

    <?xml version="1.0" ?>
    <object name="portal_workflow" meta_type="Plone Workflow Tool" purge="False">

		<object name="your_workflow" meta_type="Workflow" />

	</object>


Assigning a workflow globally as default
========================================

In your/product/profiles/default/workflows.xml, add:

.. code-block:: xml

    <object name="portal_workflow">
		(...)
		<bindings>
			<default>
				<bound-workflow workflow_id="simple_publication_workflow" />
			</default>
		</bindings>


Binding a workflow to a content type
========================================

Example with GenericSetup *workflows.xml*

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_workflow" meta_type="Plone Workflow Tool">
     <bindings>
       <type type_id="Image">
         <bound-workflow workflow_id="plone_workflow" />
       </type>
     </bindings>
    </object>

Disabling workflow for a content type
======================================
If a content type doesn't have a workflow it uses its parent container security settings.
By default, content types Image and File have no workflow.

Workflows can be disabled by leaving the workflow setting empty in portal_workflow in the Management Interface.

Example how to do it with GenericSetup *workflows.xml*

.. code-block:: xml

        <?xml version="1.0"?>
        <object name="portal_workflow" meta_type="Plone Workflow Tool">
         <property
            name="title">Contains workflow definitions for your portal</property>
         <bindings>
          <!-- Bind nothing for these content types -->
          <type type_id="Image"/>
          <type type_id="File"/>
         </bindings>
        </object>


Updating security settings after changing workflow
==================================================

Through the web this would be done by going to the Management Interface > portal_workflow > update security settings

To update security settings programmatically use the method updateRoleMappings.
The snippet below demonstrates this::

    from Products.CMFCore.utils import getToolByName
    # Do this after installing all workflows
    wf_tool = getToolByName(self, 'portal_workflow')
    wf_tool.updateRoleMappings()


Programatically
---------------

Getting the current workflow state
=================================================

Example::

    workflowTool = getToolByName(self.portal, "portal_workflow")
    # Returns workflow state object
    status = workflowTool.getStatusOf("plone_workflow", object)
    # Plone workflows use variable called "review_state" to store state id
    # of the object state
    state = status["review_state"]
    assert state == "published", "Got state:" + str(state)

Filtering content item list by workflow state
=================================================

Here is an example how to iterate through content item list
and let through only content items having certain state.

.. note::

        Usually you don't want to do this, but use content
        aware folder listing method or portal_catalog query
        which does filtering by permission check.

Example::


        portal_workflow = getToolByName(self.context, "portal_workflow")

        # Get list of all objects
        all_objects = [ obj for obj in self.all_content if ISubjectGroup.providedBy(obj) or IFeaturedCourses.providedBy(obj) == True ]

        # Filter objects by workflow state (by hand)
        for obj in all_objects:
            status = portal_workflow.getStatusOf("plone_workflow", obj)
            if status and status.get("review_state", None) == "published":
                yield obj



Changing workflow state
=================================================

You cannot directly set the workflow to any state, but you must push
it through legal state transitions.

**Security warning**: Workflows may have security assertations which are bypassed by admin user.
Always test your workflow methods using a normal user.

Example how to publish content item ``banner``::

        from Products.CMFCore.WorkflowCore import WorkflowException

        workflowTool = getToolByName(banner, "portal_workflow")
        try:
            workflowTool.doActionFor(banner, "publish")
        except WorkflowException:
            # a workflow exception is risen if the state transition is not available
            # (the sampleProperty content is in a workflow state which
            # does not have a "submit" transition)
            logger.info("Could not publish:" + str(banner.getId()) + " already published?")
            pass


Example how to submit to review::

        from Products.CMFCore.WorkflowCore import WorkflowException

        portal.invokeFactory("SampleContent", id="sampleProperty")

        workflowTool = getToolByName(context, "portal_workflow")
        try:
            workflowTool.doActionFor(portal.sampleProperty, "submit")
        except WorkflowException:
            # a workflow exception is risen if the state transition is not available
            # (the sampleProperty content is in a workflow state which
            # does not have a "submit" transition)
            pass

Example how to cause specific transitions based on another event (e.g. a parent folder state change).
This code must be part of your product's trusted code not a workflow script because of the permission
issues mentioned above. See also see :doc:`/develop/addons/components/events` ::

       # Subscribe to the workflow transition completed action
       from five import grok
       from Products.DCWorkflow.interfaces import IAfterTransitionEvent
       from Products.CMFCore.interfaces import IFolderish

       @grok.subscribe(IFolderish, IAfterTransitionEvent)
       def make_decisions_visible(context,event):
       if (event.status['review_state'] != 'cycle_complete'):
           #nothing to do
           return
       children = context.getFolderContents()
       wftool = context.portal_workflow
       #loop through the children objects
       for obj in children:
           state = obj.review_state
           if (state=="alternate_invisible"):
               # below is workaround for using getFolderContents() which provides a
               # 'brain' rather than an python object.  Inside if to avoid overhead
               # of getting object if do not need it.
               what = context[obj.id]
               wftool.doActionFor(what, 'to_alternate')
           elif (state=="denied_invisible"):
               what = context[obj.id]
               wftool.doActionFor(what, 'to_denied')
           elif (...


Gets the list of ids of all installed workflows
================================================

Useful to test if a particular workflow is installed::

  # Get all site workflows
  ids = workflowTool.getWorkflowIds()
  self.assertIn('link_workflow', ids, "Had workflows " + str(ids))

Getting default workflow for a portal type
==========================================

Get default workflow for the type::

 chain = workflowTool.getChainForPortalType(ExpensiveLink.portal_type)
 self.assertEqual(chain, ('link_workflow',), "Had workflow chain" + str(chain))

Getting workflows for an object
===============================

How to test which workflow the object has::

    # See that we have a right workflow in place
    workflowTool = getToolByName(context, "portal_workflow")
    # Returns tuple of all workflows assigned for a context object
    chain = workflowTool.getChainFor(context)

    # there must be only one workflow for our object
    self.assertEqual(len(chain), 1)

    # this must must be the workflow name
    self.assertEqual(chain[0], 'link_workflow', "Had workflow " + str(chain[0]))


Via HTTP
---------

Plone provides a ``workflow_action`` script which is able to trigger the status
modification through an HTTP request (browser address bar).

Example::

	http://localhost:9020/site/page/content_status_modify?workflow_action=publish
