Workflow Policies
======================

Workflow policies allow a site administrator to create a formalized system for controlling publication and content management as a step-by-step flow involving different users in set roles.

Workflow is a relatively advanced subject.

It involves creation of a more regimented control of content creation, review, and publication.
If you have a user account on a typical small Plone site, you will probably not encounter custom workflow policies, because there isn't a need for this more sophisticated control.

But, the potential is there for using this functionality, as it is built in to Plone, and larger organisations often use it to model their internal structure and business logic.

For an introduction to the workflow concept, consider an example involving a web site for a newspaper business, for which these different groups of people are at work:

Reporters
    Can create stories, but can only submit them for review.
Editors
    Can review stories, but can't publish completely. They send positively reviewed and edited stories up the line for further approval.
Copy Editors
    Do final fact checking, fixes, and review, and may publish stories.

A *workflow policy*, sometimes abbreviated to *workflow*, describes the constraints on state-changing actions for different groups of people.
Once the workflow policy has been created, it needs to be applied to an area of the website for the rules to take effect.

In the example of the newspaper web site, a workflow policy would be set up and then applied to the folders where reporters do the work of adding news articles.

Then, reporters would create stories and send them up the line for
review and approval:

.. figure:: /_static/workflowsteps.png
   :align: center
   :alt:

Reporters would add news articles and would *submit* them (the *publish* menu choice is not available to them).
Likewise, editors may *reject* the article for revision or they may, in turn, *submit* the article up the line to a copy editor for final proofreading and publication.
In this newspaper business example, this policy could be called something like "Editorial Review Policy."

Configuring a workflow policy is a matter of defining the scope of the workflow.

This is a web site administrator task.

There are two main ways to set workflow policies: by content type or by area of the site. Our newspaper may set their "Editorial Review Policy" on the content type "Article", whereas they may have another workflow for Images since they go through a different process of review and approval.

But it is also possible to have different workflows for different sections of the website. The "Letters to the Editor" section may have a different workflow.

The web site administrator would use control panels of Plone to specify where on the web site the "Editorial Review Policy" applies, site-wide or to a subsection.

Plone comes with several useful workflow policies -- the default one is a simple web publishing policy.
Your web site administrator might employ a more specific policy, such as a policy for a community-based web site or a company Intranet (internal web system).
If so, you may need to learn some procedural steps to publishing, but these are just elaborations of principles in the default, basic workflow policy.
