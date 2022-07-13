================
 Field storages
================

Field storage tells how the value of schema field is stored.

AttributeStorage
================

``Products.Archetypes.storage.AttributeStorage``

This is recommended for data which is *always* read when the object is
accessed:``title``, ``description``, etc.


AnnotationStorage
=================

``Products.Archetypes.storage.annotation.AnnotationStorage``

``AnnotationStorage`` creates an object attribute ``__annotations__`` which
is an ``OOBTree`` object.  An ``OOBTree`` uses *buckets* as the smallest
persistent entity. A bucket usually holds a small number of items. Buckets
are loaded on request and as needed compared to using native Python
datatypes.

It is safe to assume that you can fit few variables to one bucket.

You also might want to define ``ATFieldProperty`` accessor if you are using
this storage.  This allows you to read the object value using standard
Python attribute access notation.

Note that in this case the access goes through AT accessor and mutator
functions.  This differs from raw storage value access: for example the AT
accessor encodes strings to UTF-8 before returning them.

Example::

	VariantProductSchema['myField'].storage = atapi.AnnotationStorage()

	class VariantProduct(folder.ATFolder):

	    meta_type = "VariantProduct"
	    schema = VariantProductSchema

	    myField = atapi.ATFieldProperty('title')

	product = VariantProduct()

	product.setMyField("foobar") # Set field using AT mutator method

	products.myField = # AT field property magic. This is equal to product.getMyField()


SQLStorage
==========

This stores field values in an external SQL database.

* `An old documentation how to use SQL storage <http://plone.sourceforge.net/archetypes/sqlstorage-howto.html>`_.

FSSStorage
==========

Store the raw values of fields on the file system.

.. code-block:: python

    # Usual Zope/CMF/Plone/Archetypes imports
    ...
    from iw.fss.FileSystemStorage import FileSystemStorage
    ...
    my_schema = Schema((
              FileField('file',
                        ...
                       storage=FileSystemStorage(),
                       widget=FileWidget(...)
                       ),
              ...
              ))
    ...

* `Official documentation of fss <https://pypi.python.org/pypi/iw.fss/>`_.


