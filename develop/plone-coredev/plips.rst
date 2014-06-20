Implementing PLIPS
==================

All about PLIPS
---------------
**What is a PLIP?**
    A PLIP is a Plone Improvement Proposal. It is a change to a Plone package that would affect everyone. PLIPs go through a different process than bug fixes because of their broad reaching effect. The Plone 4.x Framework Team reviews all PLIPs to be sure that it’s in the best interest of the broader community to be implemented and that it is of high quality.

**Is it a PLIP or a bugfix?**
    In general, anything that changes the API of Plone in the backend or UI on the front end should be filed as a PLIP. When in doubt, submit it as a PLIP. The framework team is eager to reduce its own workload and will re-classify it for you.

**Who can submit PLIPs?**
    Anyone who has signed a Plone core contributor agreement can work on a PLIP. Don’t let the wording freak you out: signing the agreement is easy and you will get access almost immediately.
    You do not have to be the most amazing coder in the entire world to submit a PLIP. The Framework Team is happy to help you at any point in the process. Submitting a PLIP can be a great learning process and we encourage people of all backgrounds to submit.  When the PLIP is accepted, a Framework Team member will “champion” your PLIP and be dedicated to seeing it completed.
    PLIPs are not just for code monkeys. If you have ideas on new interactions or UI your ideas are more than welcome. We will even help you pair up with implementors if needed.

**What is a PLIP champion?**
    When you submit your PLIP and it is approved, 1 Framework Team member who is especially excited about seeing the PLIP completed will be assigned to your PLIP as a champion. They are there to push you through completion as well as answer any questions and provide guidance.

    A champion should:

      * Answer any questions the PLIP implementor has, technically and otherwise
      * Encourage the PLIP author by constantly giving feedback and encouragement
      * Keep the implementor aware of timelines and push to get things done on time
      * Assist with finding additional help when needed to complete the implementation in a timely matter

    Keep in mind that champions are in passive mode by default. If you need help or guidance, please reach out to them as soon as possible to activate help mode.

**I’m still nervous. Can I get involved other ways at first?**
    If you want to feel the process and how it works, help us review PLIPs as the implementations finish up. Simply ask on  of the Framework Team members what PLIPs are available for review or check the status of PLIPs at the `following link <https://dev.plone.org/report/24>`_. Make sure to let us know you intend to review the PLIP by joining the `Framework Team mailing list <https://lists.plone.org/mailman/listinfo/plone-framework-team>`_ and sending a quick email.
    Then, follow the simple instructions for :doc:`reviewing a PLIP <plipreview>`. Thank you in advance!

**When can I submit a PLIP?**
    Today, tomorrow, any time! After the PLIP is accepted, the Framework Team will try to judge complexity and time to completion and assign it to a milestone. You can begin working immediately, and we encourage submitting fast and furious.

**When is the PLIP due?**
    Summary: As soon as you get it done.
    Technically, we want to see it completed for the release to which it’s assigned. We know that things get busy and new problems make PLIPs more complicated and we will push it to the next release.
    In general, we don’t want to track a PLIP for more than a year. If your PLIP is accepted and we haven’t seen activity in over a year, we will probably ask you to restart the whole process.

**You don’t like my PLIP :( What now?**
    Just because a PLIP isn’t accepted in core doesn’t mean it’s a bad idea. It is often the case that there are competing implementations and we want to see it vetted as an add on before “blessing” a preferred implementation.

Process Overview
----------------
#. Submit a PLIP (at any time)
#. PLIP is approved for inclusion into core for a given release
#. Developer implements PLIP (code, tests, documentation)
#. PLIP is submitted for review by developer
#. Framework Team reviews the PLIP and gives feedback
#. Developer addresses concerns in feedback and re-submits if necessary. This may go back and forth a few times until both the FWT and developer are happy with the result.
#. PLIP is approved for merge. In rare circumstances, a PLIP will be rejected. This is usually the result of the developer not responding to feedback or dropping out of the process.  Hang in there!
#. After all other PLIPS are merged, a release is cut. Standby for bugs!

.. _how_submit_plip:

How to Submit a PLIP
--------------------
Whether you want to update the default theme or rip out a piece of architecture, everyone should go through the PLIP process. If you need help at any point in this process, please contact a member of the framework team personally or ask for help on the `FWT mailing list <https://lists.plone.org/mailman/listinfo/plone-framework-team>`_.

A PLIP is just a ticket with a special template. To get started, `open a new ticket <https://dev.plone.org/newticket>`_ and select "PLIP" as the ticket type. A new ticket template will reload and you should plan to fill in all of the fields.

When writing a PLIP, be as specific and to-the-point as you can. Remember your audience - to get support for your proposal, people will have to be able to read it! A good PLIP is sufficiently clear for a knowledgeable Plone user to be able to understand the proposed changes, and sufficiently detailed for the release manager and other developers to understand the full impact the proposal would have on the codebase. You don't have to list every line of code that needs to be changed, but you should also give an indication that you have some idea that how the change can be feasibly implemented.

If your change is minor then a ticket in the tracker will be sufficient, added as an enhancement. The key point here is that each change needs documentation so other users can see what it is. This can be in the form of an issue tracker entry, or a PLIP in the case of a bigger change. A bug or minor change does normally not need to go through a review process - a PLIP does.

After your PLIP is written, solicit feedback on your idea on the plone-developers mailing list. In this vetting process, you want to make sure that the change won’t adversely affect other people on accident. Others may be able to point out risks or even offer up better or existing solutions.

When you are happy with the feedback, :ref:`submit a PLIP <how_submit_plip>`. Please use the template provided (XXX: put the template here? Can we just have a custom ticket type?). Please note a few things. It is very rare that the “Risks” section will be empty or none. If you find this is the case and your PLIP is anything more than trivial, maybe some more vetting should be done.

The seconder field is REQUIRED. We will send the PLIP back to you if it is not filled in. Currently, this is just someone else who thinks your PLIP is a good idea, a +1. In the near future, we will start asking that the seconder is either a coding partner, or someone who is willing and able to finish the PLIP should something happen to the implementor.

Everything else should be self explanatory. That or I got lazy when writing these docs. I'm betting on the latter.

Evaluating PLIPs
^^^^^^^^^^^^^^^^
After you submit your PLIP, the Framework Team will meet within a couple weeks and let you know if the PLIP is accepted. If the PLIP is not accepted, please don't be sad! We encourage most PLIPs to go through the add on process at first if at all possible to make sure the majority of the community uses it.

All communication with you occurs on the PLIP ticket itself so please keep your eyes and inbox open for changes.

These are the criteria by which the framework team will review your bundle:
 * What is size and status of the work needed to be done? Is it already an add-on and well established?
 * Is this idea well baked and expressed clearly?
 * Does the work proposed belong in Plone now, in the future?
 * Is this PLIP more appropriate as a qualified add-on?
 * Is this PLIP too risky?

See the :doc:`plipreview` page for more information.

Implementing Your PLIP
----------------------
You can start the development at any time - but if you are going to modify Plone itself, you might want to wait to see if your idea is approved first to save yourself some work if it isn't.

General Rules
^^^^^^^^^^^^^
 * Any new packages must be in a branch in the plone namespace in github. You don't have to develop there, but it must be there when submitted. We recommend using branches off of the github.com/plone repo and will detail that below.
 * Most importantly, the PLIP reviewers must be able run buildout and everything should "just work" (tm).
 * Any new code must:
    * Be :doc:`Properly Documented <documentation>`
    * Have clear code
    * User the current idioms of development
    * `Be tested <http://collective-docs.plone.org/en/latest/testing_and_debugging/index.html>`_

Creating a New PLIP Branch
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. TODO: This needs to be updated for branches

Create a buildout configuration file for your PLIP in the ``plips`` folder.
Give it a descriptive name, starting with the PLIP number;
``plip-1234-widget-frobbing.cfg`` for example. This file will define the
branches/trunks you're working with in your PLIP. It should look something
like this:

In file ``plips/plip-1234-widget-frobbing.cfg``::

 [buildout]
 extends = plipbase.cfg
 auto-checkout +=
     plone.somepackage
     plone.app.someotherpackage

 [sources]
 plone.somepackage = git git://github.com/plone/plone.somepackage.git branch=plip-1234-widget-frobbing
 plone.app.someotherpackage = git git://github.com/plone/plone.app.somepackage.git branch=plip-1234-widget-frobbing

 [instance]
 eggs +=
     plone.somepackage
     plone.app.someotherpackage
 zcml +=
     plone.somepackage
     plone.app.someotherpackage

Use the same naming convention when branching existing packages, and you
should always be branching packages when working on PLIPs.

Finishing Up
^^^^^^^^^^^^
Before marking your PLIP as ready for review, please add a file to give a set of instructions to the PLIP reviewer.

This file should be called ``plip_<number>_notes.txt``. This should include (but is not limited to):
 * URLs pointing to all documentation created / updated
 * Any concerns, issues still remaining
 * Any weird buildout things
 * XXX: What else?

Once you have finished, please update your PLIP ticket to indicate that it is ready for review. The Framework Team will assign 2-3 people to review your PLIP. They will follow the guidelines listed at :doc:`plipreview`.

After the PLIP has been accepted by the framework team and the release manager, you will be asked to merge your work into the main development line. Merging the PLIP in is not the hardest part, but you must think about it when you develop. You'll have to interact with a large number of people to get it all set up. The merge may cause problems with other PLIPs coming in. During the merge phase you must be prepared to help out with all the features and bugs that arise.

If all went as planned the next Plone release will carry on with your PLIP in it. You'll be expected to help out with that feature after it's been released (within reason).
