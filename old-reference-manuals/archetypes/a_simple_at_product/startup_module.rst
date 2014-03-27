====================
The startup module 
====================

.. admonition:: Description

		The initialization module (__init__.py) provides the script
		that is run when Zope is started.

Before starting the usual Zope product initialization code, we need to
define a Message Factory for when this product is internationalized.

::

    from zope.i18nmessageid import MessageFactory

    exampleMessageFactory = MessageFactory('example.archetype')

The defined ``MessageFactory`` object will be imported with the special
name “\_” in most modules, and strings like \_(u“message”) will then be
extracted by i18n tools for translation.

Now, we import some useful stuff from the Archetypes
API:\ ``process_types`` is useful to get the product’s *content types*,
associated *constructors,* and *Factory Type Information* (FTI) data
structures, while ``listTypes`` can be used to list the types available
in the product.

We also need to import the ``utils`` module from ``CMFCore`` to be able
to use its ``ContentInit`` class later.

::

    from Products.Archetypes.atapi import process_types
    from Products.Archetypes.atapi import listTypes

    from Products.CMFCore import utils

**Python notes:**

-  Factory Type Information (FTI): Part of a CMF portal’s configuration,
   the FTI for a content type is the data structure that holds the
   information needed to expose a content type within the portal. From
   the integrator’s perspective, the FTI is the object (Factory-based
   Type Information object) within the portal\_types component that
   tells CMF and Plone how to create a content from the type and how to
   display it.

-  How exactly does ‘listTypes’ work: See those registerType() calls in
   your content type modules? Notice how we also import those modules
   (but do nothing with the import) in the ‘content’ package’s
   \_\_init\_\_.py. The registerType() call tells AT about the type so
   that listTypes() can find it later.

One of the important import steps : we import everything that is defined
in the content sub-package, i.e. all its modules:

::

    from content import message

Now, we import the configuration module, in order to have access to the
variables it contains, such as the “Add” permission setting:

::

    import config

Now for the real action. You define a function that is required by Zope
and CMF internals to initialize our content type(s):

::

    def initialize(context):

The first part of the code of this function generates the *content
types*, the *constructors* and the *Factory-based Type Informations* (or
FTIs) required to make your types work with the CMF:

::

        content_types, constructors, ftis = process_types(
            listTypes(config.PROJECTNAME),
            config.PROJECTNAME)

The second part instantiates an object of the class ContentInit (from
CMFCore), and registers your types in the CMF:

::

        utils.ContentInit(
                "%s Content" % config.PROJECTNAME,
                content_types      = content_types,
                permission         = config.ADD_CONTENT_PERMISSIONS['InstantMessage'],
                extra_constructors = constructors,
                fti                = ftis,
                ).initialize(context)

**Handling several content types**

There is a better way to write the code that initializes the content
type class with its “Add” permission and constructor, so that it still
works if you define several content types. This is useful if you plan to
later augment your product with additional types.

Here is the improved code:

::

    def initialize(context):

        content_types, constructors, ftis = process_types(
                 listTypes(config.PROJECTNAME), 
                 config.PROJECTNAME)


        # We want to register each type with its own permission,
        # this will afford us greater control during system
        # configuration/deployment (credit : Ben Saller)

        allTypes = zip(content_types, constructors)
        for atype, constructor in allTypes:
            kind = "%s: %s" % (config.PROJECTNAME, atype.portal_type)
            utils.ContentInit(kind,            
                              content_types      = (atype,),
                              permission         = config.ADD_CONTENT_PERMISSIONS[atype.portal_type],
                              extra_constructors = (constructor,),            
                              fti                = ftis,
                              ).initialize(context)

**Python notes:**

-  We can use the “ADD\_CONTENT\_PERMISSIONS[atype.portal\_type]”
   construct because ADD\_CONTENT\_PERMISSIONS references a dictionary
   in which the keys are the potential content types names.

-  The zip() function is a Python built-in that pairs up elements of two
   lists. In this case, “allTypes” will be a list of tuples containing a
   content type from “content\_types” and the corresponding constructor
   from “constructors”.

-  If you have several content types, you should not forget to import
   each content module, as is done for the message example discussed
   here !
