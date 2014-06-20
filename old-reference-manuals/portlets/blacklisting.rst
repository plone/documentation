======================
Order and blacklisting
======================

.. admonition:: Description

        How to change the order of the different types of
        portlets (group, user, contextual) inside a
        portlet manager, and how portlet blocking works.


!!! Warning: Incomplete Material !!!



When giving a key for the context assignment, the root of the site can be
referred to this way:

::

    key="/"


Refer to the default 'news' folder in the site (NOTE: Prior to Plone 3.3.5, this
required a full path like /Plone/news):

::

    key="/news"

Delete a portlet assignment using the remove attribute:

::

    <assignment
        remove="True"
        manager="plone.rightcolumn"
        category="context"
        key="/"
        type="portlets.Calendar"
        name="calendar"
        />

Remove all the portlet assignments for a specific manager assigned to the
news object using the purge attribute:

::

    <assignment
        purge="True"
        manager="plone.rightcolumn"
        category="context"
        key="/news"
        />

Add or move an existing portlet at the top of the column using
insert-before:

::

    <assignment
        insert-before="*"
        manager="plone.rightcolumn"
        category="context"
        key="/"
        type="portlets.Calendar"
        name="calendar"
        />

Add or move an existing portlet before the 'news' portlet:

::

    <assignment
        insert-before="news"
        manager="plone.rightcolumn"
        category="context"
        key="/"
        type="portlets.Calendar"
        name="calendar"
        />

Pro Tip: Quickest way to find out the name of a portlet: go to @@manage-
portlets and hover over the 'X'. The name for that assignment will appear in
the URL.



Looted from Six Feet Up's QuickReferenceCard_.

.. _QuickReferenceCard: http://www.sixfeetup.com/company/technologies/plone-content-management-new/quick-reference-cards/swag/swag-images-files/generic_setup.pdf


Blacklisting portlets (from ``plone.app.portlets``'s test suite):

::

    <blacklist
        manager="test.testcolumn"
        category="context"
        location="/news"
        status="block"
        />
    <blacklist
        manager="test.testcolumn"
        category="group"
        location="/news"
        status="show"
        />
    <blacklist
        manager="test.testcolumn"
        category="content_type"
        location="/news"
        status="acquire"
        />

    <blacklist
        manager="test.testcolumn"
        category="content_type"
        location="/"
        status="block"
        />

    <blacklist
        manager="test.testcolumn"
        category="group"
        location="/"
        status="show"
        />

    <blacklist
        manager="test.testcolumn"
        category="context"
        location="/"
        status="acquire"
        />
