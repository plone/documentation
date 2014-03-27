=============================================
How and where are Portlet Assignments stored?
=============================================

.. admonition:: Description

        When you choose a portlet to be displayed somewhere,
        for example, using the interface that appears when
        you hit the Manage Portlets button, what you're doing
        is storing a persistent instance of the Portlet Assignment
        class into your site, together with all its associated
        configuration data.

.. contents :: :local:

Portlet Assignments are stored in what's called an Assignment
Mapping. This is an ordered container with a dict-like interface.
The keys are unique string names, and the values are instances of
the assignment class.

Assignment mappings can be stored in two different kinds of
locations depending on their type: site-wide or contextual.

Site-wide
---------

Site-wide assigned portlets are shown in the whole site, unless
blocked. They're stored in Portlet Managers. Portlet Managers
define a column or other area that can be filled with portlets, and
are analogous to the viewlet manager for viewlets. They are named
persistent local utilites providing the ``IPortletManager``
interface.

You can look up a portlet manager like this:

::

    manager = getUtility(IPortletManager, name=u"plone.leftcolumn")

By default, there are two standard portlet managers,
``plone.leftcolumn`` and ``plone.rightcolumn``, as well as four
portlet managers for the four columns on the dashboard, from
``plone.dashboard1`` to ``plone.dashboard4``. You can create your
own in ``portlets.xml`` like this:

.. code-block:: xml

    <portletmanager
      name="my.package.myportletmanager"
      type="my.package.interfaces.IMyPortletManagerType"
      />

The "type" is a marker interface that can be used to install
particular portlets only for particular types of portlet managers,
as explained above. Example:
``plone.app.portlets.interfaces.IDashboard``.

Portlets in global categories (site-wide) are stored directly
inside the ``IPortletManager`` utility, under a particular category
- e.g. "group" - a category-specific key - e.g. the group id - and
finally a unique portlet id. Putting this together, we could access
a particular portlet assignment like this:

::

    from plone.portlets.constants import GROUP_CATEGORY
    manager = getUtility(IPortletManager, name=u"plone.leftcolumn")
    recent_assignment = manager[GROUP_CATEGORY][u"Administrators"][u"recent"]

Here we look up the left column portlet manager and get the portlet
assignment named *recent* assigned to the *Administrators* group.

Each of the lookups here has a dict interface, so you can iterate,
call ``keys()`` and so on. You can store assignments under any
string as category, but the default portlet retriever is only aware
of the three site-wide assignment categories defined as constants
in *plone.portlet.constants*, ``USER_CATEGORY``, ``GROUP_CATEGORY``
and ``CONTENT_TYPE_CATEGORY``, which should be enough for most
use-cases. More on portlet retrievers later.

Contextual
----------

Location-specific portlet assignments are stored on annotations on
objects providing the ``ILocalPortletAssignable`` marker
interface.

To get hold of the assignment in this case, we multi-adapt the
content object and the manager instance to the
``IPortletAssignment`` interface, like so:

::

    manager = getUtility(IPortletManager, name=u"plone.leftcolumn")
    assignment_mapping = getMultiAdapter((context, manager), IPortletAssignmentMapping)
    news_portlet = assignment_mapping[u"news"]

There are two functions in plone.app.portlets.utils to make it
easier to find the appropriate mapping for a portlet, or to get a
portlet assignment directly: ``assignment_mapping_from_key()`` and
``assignment_from_key()``.

We can use GenericSetup to assign portlets to particular portlet
managers upon the installation of a product. Read the
`Theme Reference Manual`_ for info about how to do that. Read the
`Generic Setup tutorial`_ for further info about what's
GenericSetup and how it works.

.. _Theme Reference Manual: ../theme-reference/elements/portlet/move/
.. _Generic Setup tutorial: ../../../tutorial/genericsetup
