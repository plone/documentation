Testing examples
----------------

.. admonition:: description

    Here, we list a few packages and projects that demonstrate good test coverage

Testing is best learned by example. It can be very instructive to read
through the tests written by other developers and learn what they test,
what they don’t test and how they write their tests.

*  `example.tests <http://dev.plone.org/collective/browser/examples/example.tests/trunk>`_,
   which we have already mentioned, contains an
   example of each of the different types of tests covered in this
   tutorial. The test setup code is well-commented, with the intention
   that this package should provide good boilerplate for developers
   setting up a new project.
*  `Plone itself <http://dev.plone.org/plone/browser/Plone/trunk/Products/CMFPlone/tests>`_
   has more than 1,600 tests at the time of writing.
   Most of these are integration tests using unit-test syntax with
   PloneTestCase.
*  `RichDocument <http://dev.plone.org/collective/browser/RichDocument/trunk/tests/testSetup.py>`_
   has a basic test\_setup.py integration test. This is
   a good example of the kind of testing you may want to do to ensure
   that your package installs cleanly.
*  `borg.project <http://dev.plone.org/collective/browser/borg/components/borg.project/trunk>`_
   contains a
   `README.txt <http://dev.plone.org/collective/browser/borg/components/borg.project/trunk/borg/project/README.txt>`_ file with an integration
   doctest demonstrating how it is used. It has only a single test
   module, `tests.py <http://dev.plone.org/collective/browser/borg/components/borg.project/trunk/borg/project/tests.py>`_, which performs the same setup as base.py and
   test\_integration\_doctest.py from example.tests.
*  Many of the tests in the
   `plone.app.controlpanel <http://dev.plone.org/plone/browser/plone.app.controlpanel/trunk/plone/app/controlpanel/tests>`_
   package use basic test-browser functional tests to verify that the Plone control panels
   work as expected.

Feel free edit or comment on this page if you have more examples to add!



