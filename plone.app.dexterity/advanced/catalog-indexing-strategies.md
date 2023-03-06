---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Catalog indexing strategies

You may have two different interests in regard to indexing your custom content type objects:

- Making particular fields searchable via Plone's main search facility;
- Indexing particular fields for custom lookup.

## Making content searchable

Plone's main index is called *SearchableText*. This is the index which is searched when you use the main portal search. Fields in your custom content types are not necessarily added to SearchableText. Fields added via Dublin-core behaviors are automatically part of SearchableText; others are not.

So, you may need to explicitly add fields to SearchableText if you wish their information to be findable via the main search. There are all sorts of highly customizable ways to do this, but the easiest is to use the the behavior `plone.textindexer` that is shipped with plone.app.dexterity.

It allows you to easily add fields to SearchableText. Once you turn on this behavior, you will then need to specify fields for addition to SearchableText.

:::{note}
Note that if you turn on the `Full-Text Indexing` behavior for a content type, then you must specify all fields that need SearchableText indexing. Dublin core fields like Title and Description are no longer automatically handled.
:::

Once you have turned on the indexer behavior, edit the XML field model to add `indexer:searchable="true"` to the `field` tag for each field you wish to add to the SearchableText index.

See the [/backend/indexing](https://6-dev-docs.plone.org/backend/indexing) package documentation for details and for information on how to use it via Python schema.

## Creating and using custom indexes

**How to create custom catalog indexes**

The ZODB is a hierarchical object store where objects of different schemata and sizes can live side by side.
This is great for managing individual content items, but not optimal for searching across the content repository.
A naive search would need to walk the entire object graph, loading each object into memory and comparing object metadata with search criteria.
On a large site, this would quickly become prohibitive.

Luckily, Zope comes with a technology called the *ZCatalog*, which is basically a table structure optimised for searching.
In Plone, there’s a ZCatalog instance called `portal_catalog`.
Standard event handlers will index content in the catalog when it is created or modified, and unindex when the content is removed.

The catalog manages *indexes*, which can be searched, and *metadata* (also known as *columns*), which are object attributes for which the value is copied into the catalog.
When we perform a search, the result is a lazily loaded list of objects known as *catalog brains*.
Catalog brains contain the value of metadata columns (but not indexes) as attributes.
The functions `getURL()`, `getPath()` and `getObject()` can be used to get the URL and path of the indexed content item, and to load the full item into memory.

:::{note}
Dexterity objects are more lightweight than Archetypes objects.
This means that loading objects into memory is not quite as undesirable as is sometimes assumed.
If you’re working with references, parent objects, or a small number of child objects, it is usually OK to load objects directly to work with them.
However, if you are working with a large or unknown-but-potentially-large number of objects, you should consider using catalog searches to find them and use catalog metadata to store frequently used values.
There is an important trade-off to be made between limiting object access and bloating the catalog with unneeded indexes and metadata, though.
In particular, large strings (such as the body text of a document) or binary data (such as the contents of image or file fields) should not be stored as catalog metadata.
:::

Plone comes with a number of standard indexes and metadata columns.
These correspond to much of the *Dublin Core* set of metadata as well as several Plone-specific attributes.
You can view the indexes, columns and the contents of the catalog through the ZMI pages of the `portal_catalog` tool.
If you’ve never done this, it is probably instructive to have a look, both to understand how the indexes and columns may apply to your own content types, and to learn what searches are already possible.

Indexes come in various types. The most common ones are:

`FieldIndex`

: the most common type, used to index a single value.

`KeywordIndex`

: used to index lists of values where you want to be able to search for a subset of the values.
  As the name implies, commonly used for keyword fields, such as the `Subject` Dublin Core metadata field.

`DateIndex`

: used to index Zope 2 `DateTime` objects.
  Note that if your type uses a *Python* `datetime` object, you’ll need to convert it to a Zope 2 `DateTime` using a custom indexer!

`DateRangeIndex`

: used mainly for the effective date range.

`ZCTextIndex`

: used mainly for the `SearchableText` index.
  This is the index used for full-text search.

`ExtendedPathIndex`

: a variant of `PathIndex`, which is used for the `path` index.
  This is used to search for content by path and optionally depth.

### Adding new indexes and metadata columns

When an object is indexed, the catalog will by default attempt to find attributes and methods that match index and column names on the object. Methods will be called (with no arguments) in an attempt to get a value.
If a value is found, it is indexed.

:::{note}
Objects are normally acquisition-wrapped when they are indexed, which means that an indexed value may be acquired from a parent.
This can be confusing, especially if you are building container types and creating new indexes for them.
If child objects don’t have attributes/methods with names corresponding to indexes, the parent object’s value will be indexed for all children as well.
:::

Catalog indexes and metadata can be installed with the `catalog.xml` GenericSetup import step. It is useful to look at the one in Plone (`parts/omelette/Products/CMFPlone/profiles/default/catalog.xml`).

As an example, let’s index the `track` property of a `Session` in the catalog, and add a metadata column for this property as well. In
`profiles/default/catalog.xml`, we have:

```xml
<?xml version="1.0"?>
<object name="portal_catalog">
    <index name="track" meta_type="FieldIndex">
        <indexed_attr value="track"/>
    </index>
    <column value="track"/>
</object>
```

Notice how we specify both the index name and the indexed attribute.
It is possible to use an index name (the key you use when searching) that is different to the indexed attribute, although they are usually the same.
The metadata column is just the name of an attribute.

### Creating custom indexers

Indexing based on attributes can sometimes be limiting.
First of all, the catalog is indiscriminate in that it attempts to index every attribute that’s listed against an index or metadata column for every object.
Secondly, it is not always feasible to add a method or attribute to a class just to calculate an indexed value.

Plone 3.3 and later ships with a package called [plone.indexer] to help make it easier to write custom indexers:
components that are invoked to calculate the value which the catalog sees when it tries to index a given attribute.
Indexers can be used to index a different value to the one stored on the object, or to allow indexing of a “virtual” attribute that does not actually exist on the object in question.
Indexers are usually registered on a per-type basis, so you can have different implementations for different types of content.

To illustrate indexers, we will add three indexers to `program.py`.
Two will provide values for the `start` and `end` indexes, normally used by Plone’s `Event` type.
We actually have attributes with the correct name for these already, but they use Python `datetime` objects whereas the `DateIndex` requires a
Zope 2 `DateTime.DateTime` object.
(Python didn’t have a `datetime` module when this part of Zope was created!)
The third indexer will be used to provide a value for the `Subject` index that takes its value from the `tracks` list.

```python
from DateTime import DateTime
from plone.indexer import indexer
...

@indexer(IProgram)
def startIndexer(obj):
    if obj.start is None:
        return None
    return DateTime(obj.start.isoformat())

@indexer(IProgram)
def endIndexer(obj):
    if obj.end is None:
        return None
    return DateTime(obj.end.isoformat())

@indexer(IProgram)
def tracksIndexer(obj):
    return obj.tracks
```

And we need to register the indexers in ZCML:

```xml
<adapter factory=".indexers.startIndexer" name="start" />
<adapter factory=".indexers.endIndexer" name="end" />
<adapter factory=".indexers.tracksIndexer" name="Subject" />
```

Here, we use the `@indexer` decorator to create an indexer.
This doesn’t register the indexer component, though, so we need to use ZCML to finalise the registration.
Crucially, this is where the indexer’s `name` is defined.
This is the name of the indexed attribute for which the indexer is providing a value.

:::{note}
Since all of these indexes are part of a standard Plone installation, we won’t register them in `catalog.xml`.
If you are creating custom indexers and need to add new catalog indexes or columns for them, remember that the “indexed attribute” name (and the column name) must match the name of the indexer as set in its adapter registration.
:::

### Searching using your indexes

Once we have registered our indexers and re-installed our product (to ensure that the `catalog.xml` import step is allowed to install new indexes in the catalog), we can use our new indexes just like we would any of the default indexes.

The pattern is always the same:

```python
from plone import api
# get the tool
catalog = api.portal.get_tool(name='portal_catalog')
# execute a search
results = catalog(track='Track 1')
# examine the results
for brain in results:
    start = brain.start
    url = brain.getURL()
    obj = brain.getObject() # Performance hit!
```

This shows a simple search using the `portal_catalog` tool, which we look up from some context object.
We call the tool to perform a search, passing search criteria as keyword arguments, where the left hand side refers to an installed index and the right hand side is the search term.

Some of the more commonly used indexes are:

`Title`

: the object’s title.

`Description`

: the object’s description.

`path`

: the object’s path. The argument is a string like `/foo/bar`.
  To get the path of an object (e.g. a parent folder), do
  `'/'.join(folder.getPhysicalPath())`.
  Searching for an object’s path will return the object and any children.
  To depth-limit the search, e.g. to get only those 1 level deep,
  use a compound query, e.g.
  `path={'query': '/'.join(folder.getPhysicalPath()), 'depth': 1}`.
  If a depth is specified, the object at the given path is not returned
  (but any children within the depth limit are).

`object_provides`

: used to match interfaces provided by the object.
  The argument is an interface name or list of interface names (of
  which any one may match).
  To get the name of a given interface, you can call
  `ISomeInterface.__identifier__`.

`portal_type`

: used to match the portal type.
  Note that users can rename portal types,
  so it is often better not to hardcode these.
  Often, using an `object_provides` search for a type-specific
  interface will be better.
  Conversely, if you are asking the user to select a particular type to
  search for, then they should be choosing from the currently installed
  `portal_types`.

`SearchableText`

: used for full-text searches.
  This supports operands like `AND` and `OR` in the search string.

`Creator`

: the username of the creator of a content item.

`Subject`

: a `KeywordIndex` of object keywords.

`review_state`

: an object’s workflow state.

In addition, the search results can be sorted based on any `FieldIndex`,
`KeywordIndex` or `DateIndex` using the following keyword arguments:

- Use `sort_on='<index name>'` to sort on a particular index.
  For example, `sort_on='sortable_title'` will produce a sensible title-based sort.
  `sort_on='Date'` will sort on the publication date, or the creation date if this is not set.
- Add `sort_order='reverse'` to sort in reverse.
  The default is `sort_order='ascending'`.
  `'descending'` can be used as an alias for `'reverse'`.
- Add `sort_limit=10` to limit to approximately 10 search results.
  Note that it is possible to get more results due to index optimisations.
  Use a list slice on the catalog search results to be absolutely sure that you have got the maximum number of results, e.g.
  `results = catalog(…, sort_limit=10)[:10]`.
  Also note that the use of `sort_limit` requires a `sort_on` as well.

Some of the more commonly used metadata columns are:

*Creator*

: the user who created the content object.

*Date*

: the publication date or creation date, whichever is later.

*Title*

: the object’s title.

*Description*

: the object’s description.

*getId*

: the object’s id (note that this is an attribute, not a function).

*review_state*

: the object’s workflow state.

*portal_type*

: the object’s portal type.

For more information about catalog indexes and searching, see the
[ZCatalog chapter in the Zope 2 book].

#### How to setup the index TTW:

Now that the fields are index-able, we need to create the index itself.

- Go to the Zope Management Interface
- Go on 'portal_catalog'
- Click 'Indexes' tab
- There's a drop down menu to the top right to let you choose what type of index to add - if you are using a plain text string field you would select 'FieldIndex'
- As the 'id' put in the programmatical name of your Dexterity type field that you want to index
- Hit OK, tick your new index and click 'Reindex'

You should now see content being indexed.

See the {doc}`documentation </develop/plone/searching_and_indexing/indexing>` for further information

[plone.indexer]: http://pypi.python.org/pypi/plone.indexer
[zcatalog chapter in the zope 2 book]: https://zope.readthedocs.io/en/latest/zopebook/SearchingZCatalog.html
