===================
Fields and widgets
===================

.. admonition:: Description

        How to read, add, remove and create fields and widgets available for Archetypes content types.


Introduction
------------

This document contains instructions how to manipulate Archetypes schema
(data model for content items) and fields and widgets it consists of.

*Schema* is list of fields associated with a content type.
Each field can belong to one *schemata* which corresponds to one Edit tab
sub-tab in Plone user interface.

Field schemata is chosen by setting field's ``schemata`` attribute.

Getting hold of schema objects
-------------------------------

Archetypes based data model is defined as Schema object, which is a list of fields.

During application start-up
===========================

When your class is being constructed you can refer the schema simply in Python::


        # Assume you have YourContentSchema object
        print YourContentSchema.fields()

        class SitsCountry(ATBTreeFolder):
                schema =YourContentSchema

        print SitsCountry.schema.fields()


During HTTP request processing
==============================

You can access context schema object by using Schema() accessor.

.. note::

        Run-time schema patching is possible, so Schema() output might
        differ what you put in to your content type during the construction.

Example::

        schema = context.Schema()
        print schema.fields()

Schema introspection
-------------------------------

How to know what fields are available on content items.

Out of box schema source code
=================================

The default Plone schemas are defined

Id and title fields:

* https://github.com/plone/Products.Archetypes/blob/master/Products/Archetypes/BaseObject.py

Category and owners schemata: Dublin core metadata

* https://github.com/plone/Products.Archetypes/blob/master/Products/Archetypes/ExtensibleMetadata.py

Settings schemata: Exclude from navigation, related items and next/previous navigation

* https://github.com/plone/Products.ATContentTypes/blob/master/Products/ATContentTypes/content/schemata.py

Document content

* https://github.com/plone/Products.ATContentTypes/blob/master/Products/ATContentTypes/content/document.py

Image content

* https://github.com/plone/Products.ATContentTypes/blob/master/Products/ATContentTypes/content/image.py

News content

* https://github.com/plone/Products.ATContentTypes/blob/master/Products/ATContentTypes/content/newsitem.py

Run-time introspection
=======================

You can get hold of content item schema and its fields as in the example below.

You can do this either in

* :doc:`Your own BrowserView Python code </develop/plone/views/browserviews>`

* :doc:`pdb breakpoint </develop/debugging/pdb>`

* :doc:`Command line Zope debug console </develop/plone/misc/commandline>`

Example::

        for field in context.Schema().fields():
                print "Field:" + str(field) + " value:" + str(field.get(context))

Field can be also accessed by name::

        field = context.Schema()["yourfieldname"]

See

* https://github.com/plone/Products.Archetypes/blob/master/Products/Archetypes/Schema/__init__.py

Field name
----------

Field exposes its name through getName() attribute::

        field = context.Schema()["yourfieldname"]
        assert field.getName() == "yourfieldname"

Accessing Archetypes field value
--------------------------------

Accessor method
===============

Each field has accessor method. Accessor method is

    * In your content type class

    * Automatically generated if you don't give it manually

    * Has name ``get`` + schema field name with first letter uppercase. E.g.
      ``yourfield`` has accessor method ``context.getYourfield()``
      There are a few exceptions to this rule, for fields that correspond
      to Dublin Core metadata. To conform to the Dublin Core specification,
      the accessor method for the ``title`` field is ``Title()`` and
      ``Description()`` for the ``description`` field.

Raw access
==========

Archetypes has two kinds of access methods:

* normal, ``getSomething()``, which filters output;

* raw, the so-called *edit* accessor, ``getRawSomething()`` which does not
  filter output.

If you use direct attribute access, i.e. ``obj.something`` you can get a `BaseUnit <https://github.com/plone/Products.Archetypes/blob/master/Products/Archetypes/BaseUnit.py>`_ object.
``BaseUnit`` is an encapsulation of raw data for long text or file.
It contains information about mimetype, filename, encoding.
To get the raw value of a ``BaseUnit`` object you can use the ``getRaw``
method, or more simply ``str(baseunit)`` (but take care that you don't
mess up the encoding).


Indirect access
==================

You can use field.get(context) to read values of fields indirectly, without knowing the accessor method.

This example shows how to read and duplicate all values of lc object to nc::

        from Products.Archetypes import public as atapi


        nc = createObjectSomehow()

        # List of field names which we cannot copy
        do_not_copy = ["id"]

        # Duplicate field data from one object to another
        for field in lc.Schema().fields():
            name = field.getName()

            # ComputedFields are handled specially,
            # and UID also
            if not isinstance(field, atapi.ComputedField) and name not in do_not_copy:
                value = field.getRaw(lc)
                newfield = nc.Schema()[name]
                newfield.set(nc, value)

        # Mark creation flag to be set
        nc.processForm()

Validating objects
------------------

Example for *nc* AT object::

        errors = {}
        nc.Schema().validate(nc, None, errors, True, True)
        if errors:
            assert not errors, "Got errors:" + str(errors)

Checking permissions
---------------------

field.writable() provides a short-cut whether the currently
logged in user can change the field value.

Example::

        field = context.Schema()["phone_number"]
        assert field.writable(), "Cannot set phone number"

There is also a verbose debugging version which will print the reason
to log if the writable condition is not effective::

        field = context.Schema()["phone_number"]
        assert field.writable(debug=True), "Cannot set phone number"

Modifying all fields in schema
------------------------------

You might want to modify all schema fields based on some criteria.

Example how to hide all metadata fields::

	for f in ExperienceEducatorSchema.filterFields(isMetadata=True): f.widget.visible = { "edit" : "invisible" }

Reordering fields
-----------------

See moveField() in `Schema/__init__.py <https://github.com/plone/Products.Archetypes/blob/master/Products/Archetypes/Schema/__init__.py>`_.

Example

.. code-block:: python


    ProductCardFolderSchema = MountPointSchema.copy() + atapi.Schema((

        # -*- Your Archetypes field definitions here ... -*-
        atapi.StringField(
            'pageTitle',
            stxxxge=atapi.AnnotationStxxxge(),
            widget=atapi.StringWidget(
                label=_(u"Page title"),
                description=_(u"Title shown on the page text if differs from the navigation title"),
            ),
            default=""
        ),

       ...


    ))


    schemata.finalizeATCTSchema(
        ProductCardFolderSchema,
        folderish=True,
        moveDiscussion=False
    )

    # Reorder schema fields to the final order,
    # show special pageTitle field after actual Title field
    ProductCardFolderSchema.moveField("pageTitle", after="title")

Hiding widgets
---------------

* You should not remove core Plone fields (Title, Description) as they
  are used by Plone internally e.g. in the navigation tree

* But you can override their accessor functions ``Title()`` and
  ``Description()``

* You can also hide the widgets

The recommended approach is to hide the widgets,
then update the field contents when the relevant data is update.
E.g. you can generate title value from fields firstname and lastname.


Below is an example which uses custom JSON field as input,
and then sets title and description based on it::

        """Definition of the XXX Researcher content type
        """

        import logging
        import json # py2.6

        from zope.interface import implements, directlyProvides, alsoProvides

        from five import grok

        from Products.Archetypes.interfaces import IObjectEditedEvent
        from Products.Archetypes import atapi
        from Products.ATContentTypes.content import folder
        from Products.ATContentTypes.content import schemata

        from xxx.objects import objectsMessageFactory as _
        from xxx.objects.interfaces import IXXXResearcher
        from xxx.objects.config import PROJECTNAME

        XXXResearcherSchema = folder.ATFolderSchema.copy() + atapi.Schema((

            # -*- Your Archetypes field definitions here ... -*-

            # Stores XXX entry as JSON string
            atapi.TextField("XXXData",
                            required =  True,
                            widget=atapi.StringWidget(
                                        label="XXX source entry",
                                        description="Start typing person's name"
                                        )),

        ))

        XXXResearcherSchema["title"].widget.visible = {"edit": "invisible" }
        XXXResearcherSchema["description"].widget.visible = {"edit": "invisible" }

        # Set stxxxge on fields copied from ATFolderSchema, making sure
        # they work well with the python bridge properties.

        schemata.finalizeATCTSchema(
            XXXResearcherSchema,
            folderish=True,
            moveDiscussion=False
        )

        class XXXResearcher(folder.ATFolder):
            """A Researcher synchronized from XXX.

            This content will have all



            """
            implements(IXXXResearcher)

            meta_type = "XXXResearcher"
            schema = XXXResearcherSchema

            # -*- Your ATSchema to Python Property Bridges Here ... -*-

            def refreshXXXData(self):
                """
                Performs collective.mountpoint synchronization for one object.
                """
                #synchronize_item(self, logging.WARNING)

            def updateXXX(self, json):
                """
                @param json: JSON payload as a string
                """
                data = self.parseXXXData(json)

                # Set this core Plone fields to actual values,
                # so that we surely co-operate with old legacy code

                title = self.getTitleFromData(data)
                desc = self.getDescriptionFromData(data)

                self.setTitle(title)
                self.setDescription(desc)

            def parseXXXData(self, jsonData):
                """
                @return Python dict
                """
                return json.loads(jsonData)

            def getParsedXXXData(self):
                """
                Return XXX JSON data parsed to Python object.
                """

                data = self.getXXXData()
                if data == "" or data is None:
                    return None

                return self.parseXXXData(data)

            def getTitleFromData(self, data):
                """
                Use lastname + surname from FOAF data as the connt title.
                """

                title = data.get(u"foaf_name", None)

                if title == "" or title is None:
                    # Title must have something so that the users
                    # can click this item in list...
                    title = "(unnamed)"

                # foaf_name is actually list of values, so we need to merge them
                title = " ".join(title)

                return title

            def getDescriptionFromData(self, data):
                """ Extract content item description from data blob """

                desc = data.get(u"dc_description", None)

                if desc is None or len(desc) == 0:
                    # Decription is not required, we get omit it
                    return None

                # dc_description is actually a list of description
                # let's merge them to string here
                desc = " ".join(desc)

                return desc


        atapi.registerType(XXXResearcher, PROJECTNAME)

        @grok.subscribe(XXXResearcher, IObjectEditedEvent)
        def object_edited(context, event):
            """
            Event handler which will update title + description
            values every time the object has been edited.

            @param context: Object for which the event was fired
            """

            # Read JSON data entry which user entered on the form
            json = context.getXXXData()

            if json != None:

                # Update the core fields to reflect changes
                # in JSON data
                context.updateXXX(json)

                # Reflect object changes back to the portal catalog
                # Note that we are running reindexObject()
                # here again... edit itself runs it and
                # we could do some optimization here
                context.reindexObject()


Rendering widget
----------------

Archetypes is hardwired to render widgets from viewless TAL page templates.

Example how to render widget for field 'maintext'::

          <tal:fields tal:define="field_macro here/widgets/field/macros/view;
                                  field python:here.Schema()['maintext']">

            <tal:if_visible define="mode string:view;
                                    visState python:field.widget.isVisible(here, mode);
                                    visCondition python:field.widget.testCondition(context.aq_inner.aq_parent, portal, context);"
                            condition="python:visState == 'visible' and visCondition">
              <metal:use_field use-macro="field_macro" />
            </tal:if_visible>
          </tal:fields>

Creating your own Field
------------------------

Here is an example how to create a custom field based on TextField.

Example (mfabrik/rstpage/archetypes/fields.py)::

        from Products.Archetypes import public as atapi
        from Products.Archetypes.Field import TextField, ObjectField, encode, decode, registerField

        from mfabrik.rstpage.transform import transform_rst_to_html

        class RSTField(atapi.TextField):
            """ """

            def _getCooked(self, instance, text):
                """ Perform reST to HTML transformation for the field cotent.

                """
                html, errors = transform_rst_to_html(text)
                return html

            def get(self, instance, **kwargs):
                """ Field accessor.

                Define view mode accessor for the widget.

                @param instance: Archetypes content item instance

                @param kwargs: Arbitrary parameters passed to the field getter
                """

                # Read the stored field value from the instance
                text = ObjectField.get(self, instance, **kwargs)

                # raw = edit mode, get reST source in that case
                raw = kwargs.get("raw", False)

                if raw:
                    # Return reST source
                    return text
                else:
                    # Return HTML for viewing
                    return self._getCooked(instance, text)


        registerField(RSTField,
                      title='Restructured Text field',
                      description=('Edit HTML as reST source'))


Automatically generating description based on body text
--------------------------------------------------------

Below is a through-the-web (TTW) Python Script which you can drop into through the Management Interface.

Use case: People are lazy to write descriptions (as in Dublin Core metadata).
You can generate some kind of description by taking the few first sentences of the text.

This is not perfect, but this is way better than empty description.

This script will provide one-time operation to automatically generate content item descriptions based on their body text
by taking the first three sentences.

The script will provide logging output to standard Plone log (var/log and stdout if Plone is run in debug mode).

Example code::

        def create_automatic_description(content, text_field_name="text"):
            """ Creates an automatic description from HTML body by taking three first sentences.

            Takes the body text

            @param content: Any Plone contentish item (they all have description)

            @param text_field_name: Which schema field is used to supply the body text (may very depending on the content type)
            """

            # Body is Archetype "text" field in schema by default.
            # Accessor can take the desired format as a mimetype parameter.
            # The line below should trigger conversion from text/html -> text/plain automatically using portal_transforms
            field = content.Schema()[text_field_name]

            # Returns a Python method which you can call to get field's
            # for a certain content type. This is also security aware
            # and does not breach field-level security provided by Archetypes
            accessor = field.getAccessor(content)

            # body is UTF-8
            body = accessor(mimetype="text/plain")

            # Now let's take three first sentences or the whole content of body
            sentences = body.split(".")

            if len(sentences) > 3:
               intro = ".".join(sentences[0:3])
               intro += "." # Don't forget closing the last sentence
            else:
               # Body text is shorter than 3 sentences
               intro = body

            content.setDescription(intro)


        # context is the reference of the folder where this script is run
        for id, item in context.contentItems():
             # Iterate through all content items (this ignores Zope objects like this script itself)

             # Use RestrictedPython safe logging.
             # plone_log() method is permission aware and available on any contentish object
             # so we can safely use it from through-the-web scripts
             context.plone_log("Fixing:" + id)

             # Check that the description has never been saved (None)
             # or it is empty, so we do not override a description someone has
             # set before automatically or manually
             desc = context.Description() # All Archetypes accessor method, returns UTF-8 encoded string

             if desc is None or desc.strip() == "":
                  # We use the HTML of field called "text" to generate the description
                  create_automatic_description(item, "text")

        # This will be printed in the browser when the script completes successfully
        return "OK"

See also

* http://blog.mfabrik.com/2010/06/04/automatically-generating-description-based-on-body-text/

Vocabularies
------------

Archetypes has its own vocabulary infrastructure which is not compatible with :doc:`zope.schema vocabularies </develop/plone/forms/vocabularies>`.

Dynamic vocabularies
====================

* http://www.universalwebservices.net/web-programming-resources/zope-plone/dynamic-vocabularies-in-plone-archetypes

Rendering single field
------------------------

Example::

        <metal:fieldMacro use-macro="python:context.widget(field.getName(), mode='edit')" />

Hiding widgets conditionally
-------------------------------

AT widgets have ``condition`` :doc:`expression </develop/plone/functionality/expressions>`.

Example how to set a condition for multiple widgets to call a BrowserView to ask whether the widget should be visible or not::

        for field in ResearcherSchema.values():
            # setCondition() is in Products.Archetypes.Widget
            # possible expression variables are_ object, portal, folder.
            field.widget.setCondition("python:object.restrictedTraverse('@@msd_widget_condition')('" + field.getName() + "')")

The related view with some sample code::

        class WidgetCondition(BrowserView):
            """
            This is referred in msd.researcher schema conditions field.
            """

            def __call__(self, fieldName):
                """

                """
                settings = getResearcherSettings(self.context)
                customization = settings.getFieldCustomization(fieldName, "visible")
                if customization is not None:
                    return customization

                # Default is visible
                return True


Dynamic field definitions
-----------------------------

You can override ``Schema()`` and ``Schemata()`` methods in your content type class
to poke the schema per HTTP request access basis.

Example::

    def Schema(self):
        """ Overrides field definitions in fly.

        """

        # XXX: Cache this method?
        from Acquisition import ImplicitAcquisitionWrapper
        from Products.Archetypes.interfaces import ISchema

        # Create modifiable copy of schema
        # See Products.Archetypes.BaseObject
        schema = ISchema(self)
        schema = schema.copy()
        schema = ImplicitAcquisitionWrapper(schema, self)

        settings = self.getResearchSettings()

        for row in settings.getFieldCustomizations():
            name = row.get("fieldName", None)
            vocab = row.get("vocabToUse", None)

            field = schema.get(name, None)

            if field and vocab and hasattr(field, "vocabulary"):
                # Modify field copy ion

                displayList = settings.getVocabulary(vocab)
                if displayList is not None:
                    field.vocabulary = displayList

        return schema
