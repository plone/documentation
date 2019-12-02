====================
Indexes And Metadata
====================

.. admonition:: Description

   How to program your custom fields and data queries through portal_catalog.


What does indexing mean?
------------------------

Indexing is the action to make object data search-able.
Plone stores available indexes in the database.

You can create them through-the-web and inspect existing indexes in portal_catalog on Index tab.

The Catalog Tool can be configured through the Management Interface or
programatically in Python but current best practice in the CMF
world is to use GenericSetup to configure it using the declarative
*catalog.xml* file.
The GenericSetup profile for Plone, for
example, uses the *CMFPlone/profiles/default/catalog.xml* XML data
file to configure the Catalog Tool when a Plone site is created. It
is fairly readable so taking a quick look through it can be very
informative.

When using a GenericSetup extension profile to customize the
Catalog Tool in your portal, you only need to include XML for the
pieces of the catalog you are changing. To add an index for the
Archetypes location field, as in the example below, a policy
package could include the following
*profiles/default/catalog.xml*:

::

        <?xml version="1.0"?>
        <object name="portal_catalog" meta_type="Plone Catalog Tool">
         <index name="location" meta_type="FieldIndex">
          <indexed_attr value="location"/>
         </index>
        </object>

The GenericSetup import handler for the Catalog Tool also supports
removing indexes from the catalog if present using the "remove"
attribute of the *<index>* element. To remove the "start" and "end"
indexes used for events, for example, a policy package could
include the following *profiles/default/catalog.xml*:

::

        <?xml version="1.0"?>
        <object name="portal_catalog" meta_type="Plone Catalog Tool">
         <index name="start" remove="True" />
         <index name="end" remove="True" />
        </object>

.. admonition:: Warning

      Care must be taken when setting up indexes with GenericSetup - if
      the import step for a *catalog.xml* is run a second time (for example
      when you reinstall the product), the indexes specified will be
      destroyed, losing all currently indexed entries, and then re-created
      fresh (and empty!). If you want to workaround this behavior, you can
      either update the catalog afterwards or add the indexes yourself in
      Python code using a custom import handler.

      For more info, see this setuphandler https://github.com/plone/plone.app.event/blob/master/plone/app/event/setuphandlers.py
      in plone.app.event or these discussions on more about this problem:

      * http://plone.293351.n2.nabble.com/How-to-import-catalog-xml-without-emptying-the-indexes-td2302709.html

      * https://mail.zope.org/pipermail/zope-cmf/2007-March/025664.html


Viewing Indexes And Indexed Data
--------------------------------

Indexed data
^^^^^^^^^^^^

You can do this through portal_catalog in the Management Interface.

* Click portal_catalog in the portal root

* Click *Catalog* tab

* Click any object

Indexes And Metadata Columns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Available indexes are stored in the database, not in Python code.
To see what indexes your site has

* Click portal_catalog in the portal root

* Click *Indexes* and *Metadata* tabs


Creating An Index
-----------------

To perform queries on custom data, you need to add the corresponding index to portal_catalog first.

For example, if your :doc:`Archetypes </develop/plone/content/types>` content type has a field::

		schema = [

		   DateField("revisitDate",
		        widget = atapi.DateWidget(
		            label="Revisit date"),
		            description="When you are alarmed this content should be revisited (one month beforehand this date)",
		            schemata="revisit"
		            ),
		]

        class MyContent(...):

                # This is automatically run-time generated function accessor method,
                # but could be any hand-written method as well
                # def getMyCustomValue(self):
                #        pass

You can add a new index which will *index* the value of this field, so you can
make queries based on it later.

See more information about :doc:`accessor methods </develop/plone/content/archetypes/fields>`.

.. note::

   If you want to create an index for content type you do not control yourself or if you want to do some custom logic in your indexer,
   please see *Custom index method* below.

Creating An Index Through The Web
---------------------------------

This method is suitable during development time - you can create an index
to your Plone database locally.

* Go to the Management Interface

* Click portal_catalog

* Click Indexes tab

* On top right corner, you have a drop down menu to add new indexes. Choose the index type you need to add.

	* Type: FieldIndex

	* Id: getMyCustomValue

	* Indexed attributes: getMyCustomValue

You can use Archetypes accessors methods directly as an indexed attribute.
In example we use ``getMyCustomValue`` for AT field ``customValue``.

The type of index you need depends on what kind queries you need to do on the data.
For example, direct value matching, ranged date queries, free text search, etc. need different kind of indexes.

* After this you can query portal_catalog::

        my_brains = contex.portal_catalog(getMyCustomValue=111)
        for brain in my_brains:
                print brain["getMyCustomValue"]


Adding Index Using Add-on Product Installer
-------------------------------------------

You need to have your own add-on product which
registers new indexes when the add-on installer is run.
This is the recommended method for repeated installations.

You can create an index

* Using catalog.xml where XML is written by hand

* Create the index through the web and export catalog data from a development site
  using *portal_setup* tool *Export* functionality. The index is created
  through-the-web as above, XML is generated for you and you can fine tune the resulting XML
  before dropping it in to your add-on product.

* Create indexes in Python code of add-on custom import step.

* As a prerequisite, your add-on product must have
  :doc:`GenericSetup profile support </develop/addons/components/genericsetup>`.

This way is repeatable: index gets created every time an add-on product is installed.
It is more cumbersome, however.

.. warning ::

   There is a known issue of indexed data getting pruned when an add-on product is reinstalled.

   If you want to avoid this then you need to create new indexes in add-on installer custom setup step (Python code).


The example below is not safe for data prune on reinstall.
This file is ``profiles/default/catalog.xml``
It installs a new index called ``revisit_date`` of DateIndex type.

.. code-block:: xml

	<?xml version="1.0"?>
	<object name="portal_catalog" meta_type="Plone Catalog Tool">
		 <index name="revisit_date" meta_type="DateIndex">
  			<property name="index_naive_time_as_local">True</property>
 		</index>
 	</object>

For more information see

* http://maurits.vanrees.org/weblog/archive/2009/12/catalog

Custom Index Methods
--------------------

The `plone.indexer <https://pypi.python.org/pypi/plone.indexer>`_ package provides method to create custom indexing functions.

Sometimes you want to index "virtual" attributes of an object computed from existing ones,
or you want to customize the way certain attributes are indexed, for example, saving only the 10
first characters of a field instead of its whole content.

To do so in an elegant and flexible way, Plone>=3.3 includes a new
package, `plone.indexer <https://pypi.python.org/pypi/plone.indexer>`_,
which provides a series of primitives to delegate indexing operations to adapters.

Let's say you have a content type providing the interface
``IMyType``. To define an indexer for your type which takes the
first 10 characters from the body text, just type (assuming the
attribute's name is 'text'):

::

    from plone.indexer.decorator import indexer

    @indexer(IMyType)
    def mytype_description(object, **kw):
         return object.text[:10]

Finally, register this factory function as a named adapter using
ZCML. Assuming you've put the code above into a file named
``indexers.py``:

::

       <adapter name="description" factory=".indexers.mytype_description" />


.. note::

   You can omit the ``for`` attribute because you passed this to the ``@indexer`` decorator,
   and you can omit the ``provides`` attribute because the thing returned by the decorator is actually a
   class providing the required ``IIndexer`` interface.

To learn more about the *plone.indexer* package, read `its doctest <http://dev.plone.org/plone/browser/plone.indexer/trunk/plone/indexer/README.txt>`_.

For more info about how to create content types, refer to the :doc:`developing add-ons section </develop/addons/index>`.
For older Archetypes content types, see the `Plone 4 documentention on Archetypes <http://docs.plone.org/4/en/old-reference-manuals/archetypes/index.html>`_

.. important::

   If you want to adapt an Archetypes content type like Event or News Item, take into account
   you will have to feed the ``indexer`` decorator with the Zope 3 interfaces defined in ``Products.ATContentTypes.interface.*``
   files, not with the deprecated Zope 2 ones into the ``Products.ATContentTypes.interfaces`` file.

Creating A Metadata Column
^^^^^^^^^^^^^^^^^^^^^^^^^^

The same rules and methods apply for metadata columns as creating index above.
The difference with metadata is that

* It is not used for searching, only displaying the search result

* You store always a value copy as is

To create metadata colums in your ``catalog.xml`` add:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_catalog" meta_type="Plone Catalog Tool">
      <!-- Add a new metadata column which will read from context.getSignificant() function -->
      <column value="getSignificant"/>
    </object>


When Indexing Happens And How To Reindex Manually
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Content indexing happens automatically if:

* The object is modified by the user using the standard edit forms

* portal_catalog rebuild is run (from *Advanced* tab)

You must call ``reindexObject()`` manually if you:

* Directly call object field mutators

* Otherwise directly change any object data

``reindexObject()`` method takes the optional argument *idxs* which will list the changed indexes.
If *idxs* is not given, all related indexes are updated even though they were not changed.

Example:

.. code-block:: python

    obj.setTitle('Foobar')
    # update only the index associated with this change
    obj.reindexObject(idxs=['Title'])

If you add a new index you need to run :doc:`Rebuild catalog </develop/plone/searching_and_indexing/catalog>`
to get the existing values from content objects into the new index.

Also, if you modify security related parameters (permissions), you need to call ``reindexObjectSecurity()``.

Check the thread `Best practices on reindexing the catalog <https://community.plone.org/t/best-practices-on-reindexing-the-catalog/4157>`_
for more tips on how to reduce memory consumption and speed up the process.

.. warning::

   **Unit test warning:** Usually Plone reindexes modified objects at the end of each request (each transaction).
   If you modify the object yourself you are responsible to notify related catalogs about the new object data.


Index Types
-----------

Zope 2 product `PluginIndexes <https://github.com/zopefoundation/Products.ZCatalog/tree/master/src/Products/PluginIndexes>`_
defines various portal_catalog index types used by Plone.

* FieldIndex stores values as is

* DateIndex and DateRangeIndex store dates (Zope 2 DateTime objects) in searchable format. The latter
  provides ranged searches.

* KeywordIndex allows keyword-style look-ups (query term is matched against all the values of a stored list)

* ZCTextIndex is used for full text indexing

* `ExtendedPathIndex <https://github.com/plone/Products.ExtendedPathIndex>`_ is used for indexing content object locations.


Default Plone Indexes And Metadata Columns
------------------------------------------

Some interesting indexes

* start and end: Calendar event timestamps, used to make up calendar portlet

* sortable_title: Title provided for sorting

* portal_type: Content type as it appears in portal_types

* Type: Translated, human readable, type of the content

* path: Where the object is (getPhysicalPath accessor method).

* object_provides: What interfaces and marker interfaces object has. KeywordIndex of
  interface full names.

* is_default_page: is_default_page is method in CMFPlone/CatalogTool.py handled by plone.indexer, so there is nothing
  like object.is_default_page and this method calls ptool.isDefaultPage(obj)

Some interesting columns

* getRemoteURL: Where to go when the object is clicked

* getIcon: **This might be confusing:**
           Since Plone 5.0.2 - **getIcon is a boolean value which is set to ``True``, when the item is an image ore has an image property (named image)
           e.g.: lead image or teaser image).** The value of getIcon is used for showing preview images (thumbs) in lists, tables, content view, portlets, etc.).

           Content type icons (aka portaltype-icons) ( e.g.: for folder, document, news item etc.) are now rendered as fontello fonts since Plone 5.0.
           Mime type icons are read from the mime type registry for all file content types instead a fontello font (since Plone 5.1)

* exclude_from_nav: If True the object won't appear in sitemap, navigation tree

* mime_type: Since Plone 5.1: Mime type information for content items where applicable (file, image, custom types,...) e.g.: ``text/plain``, ``image/jpeg``, ``application/pdf`` ...

Custom Sorting By Title
^^^^^^^^^^^^^^^^^^^^^^^

sortable_title is type of FieldIndex (raw value) and normal ``Title`` index is type of searchable text.

``sortable_title`` is generated from ``Title`` in ``Products/CMFPlone/CatalogTool.py``.

You can override ``sortable_title`` by providing an indexer adapter with a specific interface of your content type.

Example indexes.py::

        from plone.indexer import indexer

        from xxx.researcher.interfaces import IResearcher

        @indexer(IResearcher)
        def sortable_title(obj):
            """
            Provide custom sorting title.

            This is used by various folder functions of Plone.
            This can differ from actual Title.
            """

            # Remember to handle None value if the object has not been edited yet
            first_name = obj.getFirst_name() or ""
            last_name = obj.getLast_name() or ""

            return last_name + " " + first_name

Related ``configure.zcml``

.. code-block:: xml

    <adapter factory=".indexes.sortable_title" name="sortable_title" />



Full-text Searching
-------------------

Plone provides special index called ``SearchableText`` which is used on the site full-text search.

Your content types can override ``SearchableText`` index with custom method to populate this index
with the text they want to go into full-text searching.

Below is an example of having ``SearchableText`` on a custom Archetypes content class.
This class has some methods which are not part of AT schema and thus must be manually
added to ``SearchableText``

::

    def SearchableText(self):
        """
        Override searchable text logic based on the requirements.

        This method constructs a text blob which contains all full-text
        searchable text for this content item.

        This method is called by portal_catalog to populate its SearchableText index.
        """

        # Test this by enable pdb here and run catalog rebuild in the Management Interface
        # xxx

        # Speed up string concatenation ops by using a buffer
        entries = []

        # plain text fields we index from ourself,
        # a list of accessor methods of the class
        plain_text_fields = ("Title", "Description")

        # HTML fields we index from ourself
        # a list of accessor methods of the class
        html_fields = ("getSummary", "getBiography")


        def read(accessor):
            """
            Call a class accessor method to give a value for certain Archetypes field.
            """
            try:
                value = accessor()
            except:
                value = ""

            if value is None:
                value = ""

            return value


        # Concatenate plain text fields as is
        for f in plain_text_fields:
            accessor = getattr(self, f)
            value = read(accessor)
            entries.append(value)

        transforms = getToolByName(self, 'portal_transforms')

        # Run HTML valued fields through text/plain conversion
        for f in html_fields:
            accessor = getattr(self, f)
            value = read(accessor)

            if value != "":
                stream = transforms.convertTo('text/plain', value, mimetype='text/html')
                value = stream.getData()

            entries.append(value)

        # Plone accessor methods assume utf-8
        def convertToUTF8(text):
            if type(text) == unicode:
                return text.encode("utf-8")
            return text

        entries = [ convertToUTF8(entry) for entry in entries ]

        # Concatenate all strings to one text blob
        return " ".join(entries)


Other
-----

* http://toutpt.wordpress.com/2008/12/14/archetype_tool-queuecatalog-becareful-with-indexing-with-plones-portal_catalog/
