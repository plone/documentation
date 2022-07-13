================
Content Settings
================

.. figure:: ../../_robot/content-setup.png
   :align: center
   :alt: Content setup configuration


This seemingly innocent looking screen is the gateway to setting up advanced functionality: Workflows, visibility and versioning settings.

When (Default) is selected, as in the above screen-shot, you set the workflow that new content types will get.
It is, so to say, the default one for your entire website.

Plone comes with a few pre-defined workflows:

Simple publication workflow
    This is the default: Items start out as "private", and then can get published.
Single State workflow
    The most simple one: everything is always published. Recommended for really uncomplicated sites, basically it means there is no real workflow.
Community workflow
    Best for a community-driven website, where all members of the community can create content that will be visible, but certain content can be 'promoted', usually to the front page.
Intranet/Extranet workflow
    Meant for intranets, where the majority of users is logged in.
    Some content can be 'externally published' so it is available to anonymous visitors as well.
No Workflow
    In this one, items 'inherit' the state of their parent folder. If a certain type of content has the "No Workflow" workflow, it will be published if the folder where it lives is published, and private if the folder where it lives is private.


All of these workflows can be assigned on a per-contenttype base.

Once you select a content type in the top drop-down field, more options become available.
In the screen-shot below, we have picked the "Page" content type:


.. figure:: ../../_robot/content-document.png
   :align: center
   :alt: Content Page configuration

Now we can set a whole range of options on the "Page" content type:

Globally addable
    Selecting this option means the content type can be added anywhere in the site *(provided you or somebody else has not set up specific exclusions for an individual Folder)*
Allow comment
    This setting **overrides** the global setting in the :doc:`discussion settings <discussion>`
Visible in searches
    Will this content type show up in search results?
Versioning policy
    The "Page" content type has 'Automatic' versioning enabled, meaning you can use the :doc:`versioning features </working-with-content/managing-content/versioning>` on it.
Manage portlets assigned to this content type
    This link will take you to "content-specific" portlets. This is a feature that some add-ons use.
Current workflow:
    Explains in short what the current workflow for this content type does
New workflow:
    Allows you to change the workflow for this content type.


All in all, this allows sophisticated setups, where some content items just follow the Plone standard workflow.
Some others (think of a content type for Expenditures) goes through a whole other chain of workflow states.

.. note::

   **Defining your own workflows**

   It is no problem to define your own workflows.
   That involves a trip to the :doc:`Management Interface <management-interface>` which is not incredibly user friendly,
    and defining new workflows is a task best left for your Site Administrator or other specialist.

   There are several add-ons, however, like `plone.app.workflowmanager <https://github.com/plone/plone.app.workflowmanager>`_
   that will present a graphical tool to define workflows.
