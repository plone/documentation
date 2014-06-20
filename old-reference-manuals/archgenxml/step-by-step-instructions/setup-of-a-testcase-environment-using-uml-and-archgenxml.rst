========================================================
Setup of a Testcase Environment using UML and ArchGenXML
========================================================

.. contents :: :local:

.. admonition:: Description

        Environment for test-driven and architecture centric development.

.. TODO:: Check if it works in 2.0. Add some information how to run the tests.

About Testing
-------------
Since development is going on at many places in the Plone system,
it is important to have a way ready to *test* if the software
you wrote is affected by the changes. And, more important the other
way around, if your work, in case it makes it way into the Plone
core or other add-on products, affects the work of *others*.

There are several documents available to read on why testing is
important, so feel free to have a look:

* `Testing in Plone - Introduction <http://plone.org/documentation/tutorial/testing/introduction>`_
* `Best Practices for Plone development - Unit Testing <http://plone.org/documentation/tutorial/best-practices/unit-testing>`_
* `RichDocument Tutorial - Unit testing <http://plone.org/documentation/tutorial/richdocument/unit-testing>`_

and there are many more: Try the *testing*. Some of these documents
are describing in detail how to write the tests itself, which this
manual page is not intended for.

Testing and UML/ ArchGenXML
---------------------------
This document describes the few steps necessary to setup your testing
environment when using an UML diagram and ArchGenXML. It generates
your projects with the test infrastructure and you can focus on writing
the test itself

ArchGenXML provides a pre-configured testing environment - no more
hand-work to create it !

Steps:

1. Check if `PloneTestCase <http://plone.org/products/plonetestcase/>`_ product was shipped with your Plone. If not install it in the version for your Plone.
2. Create a package in your model and name it 'tests' and give it the stereotype ``<<tests>>``
3. Inside the new tests package create class 'MyFancyTestcase' (in the uml below named 'testPlone') and give it the stereotype ``<<plone_testcase>>``. This is your main testcase class.
4. Create an additional class inside the test package, call it 'testSetup', and give it the stereotype ``<<setup_testcase>>``. Let it derive from the main testcase class using the generalization arrow.
5. Testing methods/behaviour of archetypes classes: Create a class inside the test package. Give it the stereotype ``<<testcase>>`` or ``<<doc_testcase>>``. Make them derive from main testcase class using the generalization arrow. On a testcase class you can add methods starting with 'test' such as 'testMyFancyFeature'. After code generation you just need to fill in your test code. A doc_testcase class creates an empty doctest text-file in the '/docs' directory of your product. There are some tagged value available to control the testcase in detail. Please look at the chapter :ref:`agx-tagged-values` for more information.
6. To generate all imports and some startup code, you can use the dependency arrow from the testcase class to the archetypes class.
7. You can repeat 5 and 6 for every class you want to include in yout test. You can organize your tests also different, like one integration test, as you like.
8. Generate and run the tests.

.. TODO:: steps needed to get the test fly, such as 'zopectl test' or setting SOFTWAREHOME and INSTANCEHOME environment.

.. image:: ../basic-features/uml-testcase.png
   :alt: Sample UML

These are the basic steps necessary to get it running.
