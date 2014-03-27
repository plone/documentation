Hiding a Portlet Manager
========================

There are several methods for hiding a portlet manager.

A portlet manager won't display if there are no portlets assigned to it
to display or if the assigned portlets have no data.

In the case of the portlet columns, if the portlet manager is empty,
then it is also useful to have the surrounding block elements disappear
too, so that you don't get a wide blank margin on your page. For this
reason, the columns containing the portlet managers in the
main\_template are wrapped around with slots. Hiding the portlet
managers is, therefore, a matter or manipulating these slots. There are
various techniques:

Defining an empty slot
    Use the following in a content view template to ensure that the
    right hand column is removed:

    -  ``<metal:column_one fill-slot="column_one_slot" />``

Using the sl and sr global variables
    These are set as conditions on the slots; they check the respective
    portlet managers for content and, if they are empty, evaluate to
    false. You can override these in the template itself.
Using show\_portlets option
    show\_portlets=false can be passed as an option to a template to set
    both sl and sr to false. To see this in action, have a look at

    -  CMFPlone/skins/plone\_templates/standard\_error\_message.py and
    -  CMFPlone/browser/ploneview.py


