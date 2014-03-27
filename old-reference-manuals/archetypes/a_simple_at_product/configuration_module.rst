===========================
The configuration module 
===========================

.. admonition:: Description

		The configuration details for your content type, in config.py. 

First, we have to import a class from Archetypes:

::

    from Products.Archetypes.atapi import DisplayList

Displaylist is a data container we use when displaying
pulldowns/radiobuttons/checkmarks with different choices. Let’s say we
wanted priorities on our instant messages, and we wanted those to be
``High``, ``Normal`` and ``Low``. We will specify these later in the
file.

The next two lines set the project (Product in Zope) name, and point to
the skin directory. ``PROJECTNAME`` should reference the name of the
package: ``example.archetype``.

::

    PROJECTNAME = "example.archetype"

Now, we need to specify our ‘Priority’ pulldown. It should look like
this, using the DisplayList utility class that Archetypes has provided
for exactly that purpose:

::

    MESSAGE_PRIORITIES = DisplayList((
        ('high', 'High Priority'),
        ('normal', 'Normal Priority'),
        ('low', 'Low Priority'),
        ))

**Python notes:**

-  The reason for double parantheses is that DisplayList is a class that
   you pass a *tuple of tuples* to.

 We also need to define the “Add” permission(s) for the content type(s):

::

    ADD_CONTENT_PERMISSIONS = {
        'InstantMessage': 'example.archetype: Add InstantMessage',
     }

We recommend using the standard way of naming permissions:
‘<ProductName>: <Permission>’. This will group the related permissions
together within the ZMI (Security tab), and allow the Administrator to
recognize which permissions belong to which Product.

Note that, unless you have an advanced case which needs custom security
settings, you don’t need to define your own permissions for the “edit”
and “view” of the content. In this simple case you will just reuse, in
the modules where needed, the generic permissions defined in
CMFCore.permissions: “View”, “Modify portal content”…

