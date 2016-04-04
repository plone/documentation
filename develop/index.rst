Developing for Plone
====================

An overview of all documentation for developers, both for writing your own add-ons and for working with Plone itself.

.. toctree::
   :maxdepth: 2

   Developing add-ons for Plone <addons/index>

.. toctree::
   :maxdepth: 2

   Programming with Plone <plone/index>

.. toctree::
   :maxdepth: 2

   Debugging <debugging/index>

.. toctree::
   :maxdepth: 2

   Writing tests <testing/index>


Developing for Plone Core follows similar patterns, but it requires you to sign the Plone Contributor license.
The process is documented here.

.. toctree::
   :maxdepth: 2


   The process for developing for Plone core <coredev/docs/index>

Writing proper code and documentation that others can expand upon is vital.
As Plone community, we stick to the following style guides, and ask that all developers and documentation writers do the same.

.. toctree::
   :maxdepth: 2

   Plone style guides <styleguide/index>


Importing content from other systems often requires the help of tools to get content out from various sources and into Plone. A number of these tools exist.

.. toctree::
   :maxdepth: 2

   import/index


Tutorials
----------

`“Mastering Plone”-training <http://training.plone.org/5>`_

Mastering Plone is intended as a week-long training for people who are new to Plone or want to learn about the current best-practices of Plone-development.

It is in active use by various trainers in the Plone world, and is being developed as a 'collaborative syllabus'.

And while attending one of the trainings with real trainers is the best thing to do, you can learn a great deal from following the documentation for these trainings.


`"Mastering Mockup"-training <https://mockup-training.readthedocs.org/en/latest/index.html>`_

This training was created to teach about Mockup, the new Frontend library for Plone 5 .

.. toctree::
   :maxdepth: 1


Selected Plone core package documentation
-----------------------------------------

plone.api
^^^^^^^^^
plone.api is the recommended way of accessing Plone's functionality in your own code.

.. toctree::
   :maxdepth: 2

   full plone.api documentaton <plone.api/docs/index>

plone.app.multilingual
^^^^^^^^^^^^^^^^^^^^^^
The default solution to create multilingual content.

.. toctree::
   :maxdepth: 1

   /external/plone.app.multilingual/README

plone.app.contenttypes
^^^^^^^^^^^^^^^^^^^^^^
The default dexterity-based content types, since Plone 5.

.. toctree::
   :maxdepth: 1

   /external/plone.app.contenttypes/docs/README

plone.app.contentlisting
^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   /external/plone.app.contentlisting/README

plone.app.event
^^^^^^^^^^^^^^^

The calendar framework for Plone, default since Plone 5.

.. toctree::
   :maxdepth: 1

   plone.app.event documentation </external/plone.app.event/docs/index>

