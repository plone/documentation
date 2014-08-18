------------
Vocabularies
------------

.. admonition:: Description

        Vocabularies are lists of (value -> human readable title) pairs used
        by e.g. selection drop downs. zope.schema provides
        tools to programmatically construct their vocabularies. 

.. contents :: :local:

Introduction
------------

Vocabularies specify options for choice fields.

Vocabularies are normally described using
zope.schema.vocabulary.SimpleVocabulary
and zope.schema.vocabulary.SimpleTerm objects.
`See the source code <http://svn.zope.org/zope.schema/trunk/src/zope/schema/vocabulary.py?rev=75170&view=auto>`_.

Vocabulary terms
=======================

zope.schema defines different vocabulary term possibilities.

A term is an entry in the vocabulary. The term has a value. Most terms are tokenised terms which also have a token, and some terms are titled, meaning they have a title that is different to the token.

In ``SimpleTerm`` instances

* ``SimpleTerm.token`` must be an ASCII string. It is the value passed with the request when the form is submitted. A token must uniquely identify a term.

* ``SimpleTerm.value`` is the actual value stored on the object. This is not passed to the browser or used in the form. The value is often a unicode string, but can be any type of object.

* ``SimpleTerm.title`` is a unicode string or translatable message. It is used in the form.

Some info::

    class ITerm(Interface):
        """Object representing a single value in a vocabulary."""

        value = Attribute(
            "value", "The value used to represent vocabulary term in a field.")


    class ITokenizedTerm(ITerm):
        """Object representing a single value in a tokenized vocabulary.
        """

        # TODO: There should be a more specialized field type for this.
        token = Attribute(
            "token",
            """Token which can be used to represent the value on a stream.

            The value of this attribute must be a non-empty 7-bit string.
            Control characters are not allowed.
            """)

    class ITitledTokenizedTerm(ITokenizedTerm):
        """A tokenized term that includes a title."""

        title = TextLine(title=_(u"Title"))

.. note ::

        If you need international texts please note that 
        only title is, and should be, translated. Value and token
        should always carry the same value.

Creating a vocabulary
=====================

Example::

    from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

    items = [ ("value1", u"This is label for item"), ("value2", u"This is label for value 2")]

    terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]

    vocabulary = SimpleVocabulary(terms)

Example 2::

    from plone.directives import form

    from zope import schema
    from zope.schema.vocabulary import SimpleVocabulary

    myVocabulary = SimpleVocabulary.fromItems((
        (u"Foo", "id_foo"),
        (u"Bar", "id_bar")))

    class ISampleSchema(form.Schema):

        contentMedias = schema.Choice(vocabulary=myVocabulary,
                                      title=u"Test choice")

Stock vocabularies
-----------------------

Some vocabularies Plone provides out of the box

* :doc:`Some common named vocabularies </external/plone.app.dexterity/docs/advanced/vocabularies>` 

* `Thumbnail size vocabulary (TinyMCE) <https://github.com/plone/Products.TinyMCE/blob/master/Products/TinyMCE/vocabularies.py>`_

Creating vocabulary from list of objects
------------------------------------------

Here is one example where value = title in term::

      SimpleVocabulary.fromValues('%s.%s.%s' % (at['package'],at['meta_type'],at['portal_type']) for at in list_of_ats)"

Retrieving a vocabulary
=========================

zope.schema's SimpleVocabulary objects are retrieved via factories registered as utilities.

To get one, use zope.component's getUtility::

    from zope.component import getUtility
    from zope.schema.interfaces import IVocabularyFactory

    factory = getUtility(IVocabularyFactory, name)
    vocabulary = factory(context)


Getting a term
==============

By term value::

    # Returns SimpleTerm object by value look-up
    term = vocabulary.getTerm("value1")

    print "Term value is %s token is %s and title is %s" + (term.value, term.token, term.title)

Listing a vocabulary
====================

Example::

 for term in vocabulary:
    # Iterate vocabulary SimpleTerm objects
    print term.value + ": " + term.title

Dynamic vocabularies
-----------------------

Dynamic vocabularies' values may change run-time.
They are usually generated based on some context data.

Note that the examples below need grok package installed and <grok:grok package="...">
directive in configure.zcml.

Complete example with portal_catalog query, vocabulary creation and form

::


    """

        A vocabulary example where vocabulary gets populated from portal_catalog query
        and then this vocabulary is used in Dexterity form.

    """

    from five import grok
    from plone.directives import form

    from zope import schema
    from z3c.form import button

    from Products.CMFCore.interfaces import ISiteRoot, IFolderish
    from Products.statusmessages.interfaces import IStatusMessage

    from zope.schema.interfaces import IContextSourceBinder
    from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


    def make_terms(items):
        """ Create zope.schema terms for vocab from tuples """
        terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]
        return terms

    @grok.provider(IContextSourceBinder)
    def course_source(context):
        """
        Populate vocabulary with values from portal_catalog.

        @param context: z3c.form.Form context object (in our case site root)

        @return: SimpleVocabulary containing all areas as terms.
        """

        # Get site root from any content item using portal_url tool thru acquisition
        root = context.portal_url.getPortalObject()

        # Acquire portal catalog
        portal_catalog = root.portal_catalog

        # We need to get Plone site path relative to ZODB root
        # See traversing docs for more info about getPhysicalPath()
        site_physical_path = '/'.join(root.getPhysicalPath())

        # Target path we are querying
        folder_name = "courses"

        # Query all folder like objects in the target path
        # These portal_catalog query conditions are AND
        # but inside keyword query they are OR (the different content types
        # we are looking for)
        brains = portal_catalog.searchResults(path={ "query": site_physical_path + "/" + folder_name },
                       portal_type=["CourseInfo", "Folder"] )

        # Create a list of tuples (UID, Title) of results
        result = [ (brain["UID"], brain["Title"]) for brain in brains ]

        # Convert tuples to SimpleTerm objects
        terms = make_terms(result)

        return SimpleVocabulary(terms)

    class IMyForm(form.Schema):
        """ Define form fields """

        name = schema.TextLine(
                title=u"Your name",
            )

        courses = schema.List(title=u"Promoted courses",
                              required=False,
                              value_type=schema.Choice(source=course_source)
                              )

    class MyForm(form.SchemaForm):
        """ Define Form handling

        This form can be accessed as http://yoursite/@@my-form

        """
        grok.name('my-form')
        grok.require('zope2.View')
        grok.context(ISiteRoot)

        schema = IMyForm
        ignoreContext = True

        @button.buttonAndHandler(u'Ok')
        def handleApply(self, action):
            data, errors = self.extractData()
            if errors:
                self.status = self.formErrorsMessage
                return

            # Do something with valid data here

            # Set status on this form page
            # (this status message is not bind to the session and does not go through redirects)
            self.status = "Thank you very much!"

        @button.buttonAndHandler(u"Cancel")
        def handleCancel(self, action):
            """User cancelled. Redirect back to the front page.
            """



Complex example 2

.. code-block:: python


    from five import grok
    from zope.schema.interfaces import IContextSourceBinder
    from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
    from Products.CMFCore.utils import getToolByName
    from plone.i18n.normalizer import idnormalizer

    def make_terms(items):
        """ Create zope.schema terms for vocab from tuples """
        terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]
        return terms


    @grok.provider(IContextSourceBinder)
    def area_source(context):
        """
        Populate vocabulary with values from portal_catalog.

        Custom index name getArea contains utf-8 strings of
        possible area field values found on all content objects.

        @param context: Form context object.

        @return: SimpleVocabulary containing all areas as terms.
        """

        # Get catalog brain objects of all accommodation content
        accommodations = context.queryAllAccommodation()

        # Extract getArea index from the brains
        areas = [ a["getArea"] for a in accommodations ]
        # result will contain tuples (term, title) of acceptable items
        result = []

        # Create a form choice "do not filter"
        # which is always present
        result.append( ("all", _(u"All")) )

        # done list filter outs duplicates
        done = []
        for area in areas:
            if area != None and area not in done:

                # Archetype accessors return utf-8
                area_unicode = area.decode("utf-8")

                # Id must be 7-bit
                id = idnormalizer.normalize(area_unicode)
                # Decode area name to unicode
                # show that form shows international area
                # names correctly
                entry = (id, area_unicode)
                result.append(entry)
                done.append(area)

        # Convert tuples to SimpleTerm objects
        terms = make_terms(result)

        return SimpleVocabulary(terms)

	 
For another example, see the :doc:`Dynamic sources </external/plone.app.dexterity/docs/advanced/vocabularies>`
chapter in the Dexterity manual.

Registering a named vocabulary provider in ZCML
===================================================

You can use ``<utility>`` in ZCML to register vocabularies by name
and then refer them by name via ``getUtility()`` or in zope.schema.Choice.

.. code-block:: xml

  <utility
      provides="zope.schema.interfaces.IVocabularyFactory"
      component="zope.app.gary.paths.Favorites"
      name="garys-favorite-path-references"
      />
      
Then you can refer to vocabulary by its name::


    class ISearchCriteria(form.Schema):
        """ Alternative header flash animation/imagae """

        area = schema.Choice(source="garys-favorite-path-references", title=_("Area"), required=False)

For more information see `vocabularies API doc <http://apidoc.zope.org/++apidoc++/ZCML/http_co__sl__sl_namespaces.zope.org_sl_zope/vocabulary/index.html>`_.  
