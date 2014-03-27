===================
Testing the portlet
===================

.. admonition:: Description

        Ensure everything's working as it should.

If the portlet was registered and installed correctly, it should
now show up in the list of portlets available for addition into the
type of portlet managers specified in the for argument of the
portlet type (``IColumn`` and ``IDashboard`` in our case), under
the ``@@manage-portlets`` view (*Manage Portlets* link).

However, to ensure everything's working as it should without having
to test it through the web, we can write some integration tests.
This is recommended practice in the Plone universe. Moreover, once
you've understood how the portlet infrastructure and its API work,
you will be able to write tests first (you can copy&paste tests
from other portlets products) and then start coding the portlet.
More info on testing in the `Testing in Plone`_ tutorial.

Run them using ``bin/instance test -s ploneexample.portlet``

.. _Testing in Plone: ../testing_and_debugging
