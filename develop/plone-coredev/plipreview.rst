Reviewing PLIPs
===============

Expectations
------------
A good PLIP review takes about 4 hours so please plan accordingly. When you are done, if you have access to core please commit the review to the plips folder and reference the PLIP in your commit message. If you do not have access, please attach your review to the PLIP ticket itself.

Setting up the environment
--------------------------
Follow the instructions on `setting up a development environment <https://dev.plone.org/wiki/DevelopmentEnvironment>`_ for "Getting the Code". You will need to checkout the branch to which the PLIP is assigned. Instead of running the buildout with the default buildout file, you will run the config specific to that plip::

  > ./bin/buildout -c plips/plipXXXX.cfg

Functionality Review
--------------------
There are several things that could be addressed in a PLIP review depending on the nature of the PLIP itself. This is by no means an exhaustive list, but a place to start. Things to think about when reviewing:

General
-------
 * Does the PLIP actually do what the implementors proposed? Are there incomplete variations?
 * Were there any errors running buildout? Did the migration(s) work?
 * Do error and status messages make sense? Are they properly internationalized?
 * Are there any performance considerations? Has the implementor addressed them if so?

Bugs
----
 * Are there any bugs? Nothing is too big nor small.
 * Do fields handle whacky data? How about strings in date fields or nulls in required?
 * Is validation up to snuff and sensical? Is it too restrictive or not restrictive enough?

Usability Issues
----------------
 * Is the implementation usable?
 * How will novice end users respond to the change?
 * Does this PLIP need a usability review? If you think this PLIP needs a usability review, please change the state to "please review" and add a note in the comments.
 * Is the PLIP consistent with the rest of Plone? For example, if there is control panel configuration, does the new form fit in with the rest of the panels?
 * Does everything flow nicely for novice and advanced users? Is there any workflow that feels odd?
 * Are there any new permissions and do they work properly? Does their role assignment make sense?

Documentation Issues
--------------------
 * Is the corresponding documentation for the end user, be it developer or plone user, sufficient?
 * Is the change itself properly documented?

Please report bugs/issues in Trac as you would for any Plone bug. Reference the PLIP in the bug, assign to its implementor, and add a tag for the PLIP in the form of plip-xxx. This way the implementor can find help if he needs it. Please also prioritize the ticket. The PLIP will not be merged until all blockers and critical bugs are fixed.

Code Review
-----------

Python
^^^^^^
 * Is this code maintainable?
 * Is the code properly documented?
 * Does the code adhere to PEP8 standards (more or less)?
 * Are they importing deprecated modules?

Javascript
^^^^^^^^^^
 * Does the javascript meet our set of javascript standards? See :doc:`/develop/addons/javascript_standards`
 * Does the Javascript work in all currently supported browsers? Is it performant?

ME/TAL
^^^^^^
 * Does the PLIP use views appropriately and avoiding too much logic?
 * Is there any code in a loop that could potentially be a performance issue?
 * Are there any deprecated or old style ME/TAL lines of code such as using DateTime?
 * Is the rendered html standards compliant? Are ids and classes used appropriately?

Example PLIP Reviews
^^^^^^^^^^^^^^^^^^^^
 * https://svn.plone.org/svn/plone/buildouts/plone-coredev/branches/4.1/plips/plip9352-review-davisagli.txt
 * https://svn.plone.org/svn/plone/buildouts/plone-coredev/branches/4.1/plips/plip10886-review-cah190.txt
 * https://svn.plone.org/svn/plone/buildouts/plone-coredev/branches/4.1/plips/plip9352-review-rossp.txt
