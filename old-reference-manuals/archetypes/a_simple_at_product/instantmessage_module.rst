=====================================
The content package and its modules 
=====================================

.. admonition:: Description

		Now we are ready for the core of the product, i.e. the
		content class definition module (content/message.py). 

Since it provides a Python (sub)package, the ‘content’ directory
contains 2 modules:

-  the usual \_\_init\_\_ module that initializes the package,
-  the message module (message.py) where we will define the
   ‘InstantMessage’ class.

The message module
~~~~~~~~~~~~~~~~~~

**First imports we need**

We start the message module by adding the general Zope-related imports
we need, such as the ``implements`` function from the ``zope.interface``
module:

::

    from zope.interface import implements

We need to use a few classes and/or functions provided by the core of
our codebase, i.e. CMF/Archetypes. It is possible to have access to all
the classes and helper functions made publicly available by Archetypes,
by importing its façade or API module (``Products.Archetypes.atapi``)
this way:

::

    from Products.Archetypes import atapi 

**i18n support**

It is always a good idea to have an i18n-enabled application. To start
using Zope’s i18n support, let’s import the MessageFactory object
created in the product’s startup module:

::

    from example.archetype import exampleMessageFactory as _

The MessageFactory referenced with the ``_`` symbol can now be used to
provide i18nized labels, descriptions, and all the miscellaneous text
snippets that are injected in the UI, also known as “messages”. For a
content type implementation, this is useful for UI widgets; for example
to define the label of the content title field widget, we could define
``label = _(u'Title')``. (See later for how we make use of this
tool/practice.)

**ATContentTypes-based schema definition**

You can base your implementation directly on these stock Archetypes
schemas. But you can add better support for Plone’s UI and content
management policies (such as the parameters that allow showing/hiding
contents in the navigation menu), by basing the implementation on
ATContentTypes’ base schema, ``ATContentTypeSchema``. To be compatible
with that schema, you will also need to inherit from ATContentTypes’
ATCTContent base class.

Let’s add the import of modules we need for that:

::

    from Products.ATContentTypes.content import base
    from Products.ATContentTypes.content import schemata

Then, we import things internal to our product package, such as our
defined interface(s) and the configuration module (for access to things
such as ``PROJECTNAME`` and ``MESSAGE_PRIORITIES``):

::

    from example.archetype.interfaces import IInstantMessage

    from example.archetype import config

Now, we have everything we need to start building the schema, and then
the class that will use it. We start out by copying ATContentTypes’
``ATContentTypeSchema``, and we extend it by adding our specific fields
and/or overriden field properties.
::

    schema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

      atapi.StringField('priority',
                  vocabulary = config.MESSAGE_PRIORITIES,
                  default = 'normal',
                  widget = atapi.SelectionWidget(label = _(u'Priority')),
                 ),

      atapi.TextField('body',
                searchable = 1,
                required = 1,
                allowable_content_types = ('text/plain',
                                           'text/structured',
                                           'text/html',),
                default_output_type = 'text/x-html-safe',
                widget = atapi.RichWidget(label = _(u'Message body')),
               ),

    ))

**Notes:**

-  To instantiate an Archetypes schema object, you pass a tuple of field
   objects to the ‘Schema’ class.

We define the body of the InstantMessage object using a RichWidget, so
the user can use formatting with a WYSIWYG editor.

The full list of out-of-the-box available Fields and Widgets can be
found `in the Fields section at the end of the manual`_. You can find
more 3rd party fields and widgets `here`_.

**Content-type class definition**

The last step is to create the class for the InstantMessage content. It
inherits from ATContentTypes’ ATCTContent, which itself is based on AT’s
BaseContent, which automatically gives its ‘id’ and ‘title’ attributes,
and the entire Dublin Core metadata set (Title, Description, Creator,
CreationDate, etc):

::

    class InstantMessage(base.ATCTContent):
        """An Archetype for an InstantMessage application"""

        implements(IInstantMessage)

        schema = schema

The first information we add for the class definition is saying that it
implements the ``IInstantMessage`` interface that we have previously
defined (in ``interfaces.py``) and imported.

::

        implements(IInstantMessage)

The next thing is assigning the reference of the Archetypes schema,
using the ``schema`` class attribute.

::

        schema = schema

The content class definition is done. Now, we are ready to activate the
content type in Archetypes’ internal types registry. This is done using
the helper function called ``registerType``.

::

    atapi.registerType(InstantMessage, config.PROJECTNAME)

Congratulations! You have just created your first Archetype for Plone!
It allows you to handle the content of an instant message with
Zope-based persistent objects which:

-  can be added within your Plone site,
-  published by the Zope Publisher, which means you can visit them via
   their URLs, etc…
-  searched since they are automatically indexed,
-  etc…

But wait! You have some final packaging work to do to ease installation
of the product within your Plone site.

**Notes:**

-  At the content class level, you could also provide the ‘actions’
   attribute useful for defining the settings of the type’s actions (for
   the portal\_actions tool). In Plone 3, this is no more needed, since
   this is part of the FTI’s configuration details, and should be
   provided using GenericSetup, in the types-related XML files (i.e.
   ‘profiles/default/types/InstantMessage.xml’). *Same for the aliases.*

The \_\_init\_\_ module
~~~~~~~~~~~~~~~~~~~~~~~

The trick here is to simply import the message module so that all the
code of that module gets interpreted as soon as the Python interpreter
initializes the package.

::

    import message

 

.. _in the Fields section at the end of the manual: ../fields
.. _here: ../../../../search?path=%2Fplone.org%2Fproducts&portal_type=PSCProject&SearchableText=widget&Search=Search

