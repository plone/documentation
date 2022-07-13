================
 DataGridField
================

This document contains miscellaneous notes about DataGridField_ field and DataGridWiget widget.

DataGridField is an Archetypes field and widget to add tabular structures to your custom content types.

Basics
------

DataGridField acts as any other Archetypes based field.

To read DGF content use *accessor* function::

    data = myobject.getMyDGF() #

Data is a Python list of dictionaries. Each dictionary presents one row. Dictionary keys are column ids
and dictionary values are cell values.

To set DGF content you must replace all rows at once::

    mydata = [
        { "column1" : "value", "column2" : "something else" }, # row 1
        { "column1" : "xxx", "column2" : "yyy" } # row 2
        ]

    context.setMyDGF(mydata)

To append a row to DFG, you need to read it, manipulate the list, and then reset the value::

    rows = myobject.getMyDGF() # This returns a copy which you can modify freely
    rows.append({ "column1" : "value", "column2" : "something else" })
    myobject.setMyDGF(rows) # Now set the value with one new row


Modify cell value in DGF::

    rows = myobject.getMyDGF() # This returns a copy which you can modify freely
    rows[0]["column1"] = "newvalue" # Set a string value for row 1, cell 1 (cell using column id column1)
    myobject.setMyDGF(rows) # Now set the value with one new row

CheckboxColumn
-----------------

Checkbox column values are handled specially::

        def convertCheckboxValue(value):
            """ DataGridField value converter for CheckboxColumn """
            if value is None:
                return None

            if value == '':
                return False

            if value == '1':
                return True

            # XXX: Not sure if happens
            if value == '0':
                return False

            raise RuntimeError("Bad checkbox value:" + value)


Other resources
---------------

Please enable DEBUG in https://github.com/collective/Products.DataGridField/blob/master/Products/DataGridField/config.py
on your local computer. After this setting has been changed, you can run unit tests
and install example types on your computer.

Refer `unit tests <https://github.com/collective/Products.DataGridField/blob/master/Products/DataGridField/tests/test_columns.py>`_ for more code examples.

Refer `Archetypes manual <https://plone.org/documentation/manual/archetypes-developer-manual>`_ for basics Archetypes developer information.

.. _DataGridField: http://www.google.com/url?sa=t&source=web&ct=res&cd=1&url=http%3A%2F%2Fplone.org%2Fproducts%2Fdatagridfield&ei=_ZtjSuiXDomD-Qbx0830DA&usg=AFQjCNGWg4ZN7xjGb7kCJwtLNbMPmmVWtQ&sig2=V-ZebsEdHEzPKIRQqjaanQ

