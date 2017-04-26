=================================
Simple SQL CRUD with PloneFormGen
=================================

.. admonition:: Description

    A step-by-step lesson in using PloneFormGen to read, insert and update rows in a single SQL table.


Introduction
============

One of the goals of PloneFormGen is that it should be useful for simple update operations on an external database.

This tutorial covers the use of PloneFormGen to update and insert rows in a single-table SQL database.

The simple application we'll develop here would need quite a bit of polishing before you'd wish to expose it to the public,
but it will demonstrate the basic techniques.

Skills required to understand this tutorial include:

* The ability to add an SQL database connection and Z SQL Methods via the Management Interface and to understand what they do. If you've never read the Relational Database Connectivity chapter of the Zope Book, take some time now to do it; it's fundamental.

* Simple Python scripting via the Management Interface. Read the python-based scripts portions of the Advanced Zope Scripting chapter of the Zope Book if you're new to this vital Zope/Plone development skill.

Our basic steps will be to:

* Add a database and table to our SQL database and create a matching form in PloneFormGen;

* Add a Z SQL Method to insert rows into the database and show how it can be used in PFG;

* Add a Z SQL Method to read a row, write a Python script wrapper and use it to fill out the fields of our form;

* Add a Z SQL Method to update a row, write a Python wrapper for it and the insert method and use it as a form action;

* Consider the security implications of the fact that the SQL access methods we just created are not part of the Plone workflow.

By the way, we'll be skipping the "D" in CRUD. Deletion is up to you. :)

.. note::

    This tutorial uses *Z SQL Methods* because they're easy to teach quickly.
    If you're doing any significant database work with any Python application,
    `SQLAlchemy <http://www.sqlalchemy.org>`_ is a much more scalable way to use a relational database from Plone.

Database table & form
=====================

In this step, we create a simple database table and a matching form.

The database

Hope you're not feeling too ambitious at the moment, because this is going to be a demonstration table. It's going to have three columns:

uid
    A unique ID that's the primary key for the table. We'll make it auto-increment so that our SQL server (MySQL in this case) will do the work of keeping it unique.

string1
    A simple string.

string2
    Another simple string.


(I told you this was simple!)

Create a test database and then the table. In MySQL, the CREATE code to set up the table is:

.. code-block:: sql

    CREATE TABLE simple_db (
      uid bigint(20) unsigned NOT NULL auto_increment,
      string1 varchar(255) NOT NULL default '',
      string2 varchar(255) NOT NULL default '',
      PRIMARY KEY  (uid)
    ) TYPE=MyISAM;

Now, set up an SQL user with privileges adequate to select, insert and update the table.
Use that user identity to set up an SQL database connection object via the Management Interface.
(If you're using MySQL, this would be a Z MySQL Database Connection.) The connection must be in a place where it will be visible to the form you'll be creating.

The form

Create a PloneFormGen form with three fields:

uid
    An string field with id uid, marked hidden, with a default value of "-1". Later in the tutorial, we'll use the "-1" as a marker value to indicate a new record.

string1
    A string field with id string1.

string2
    A string field with id string2.

Note that the form field ids must exactly match our column ids.
You can script your way around this requirement, but it's a lot easier this way.

While you're at it, turn off or delete the mailer action adapter. It's harmless, but it would be a distraction.

That's it. We now have a form that matches our database table.

Inserting rows
==============

In this step, we create a method to insert a row, and show how to make of it.

Now, inside the Management Interface, in your form folder, create a Z SQL Method with the id *testCreateRow*.

Set the parameters:

Connection ID
    This should be the database connection you set up to allow access to your test database.
Arguments
    On separate lines, specify "string1" and "string2". (Leave off the quotes.)

Then, in the big text area, specify the code:

.. code-block:: python

    insert into simple_db values (
        0,
        <dtml-sqlvar string1 type=string>,
        <dtml-sqlvar string2 type=string>
    )

Note: always use <dtml-sqlvar ...> to insert your variables. It protects you against SQL-injection attacks by SQL quoting the values.

Now for a little magic: Z SQL Methods can pick up their arguments from REQUEST.form, which is exactly where Zope is putting your form variables when you submit a form.
That means that you can just go to the [overrides] pane of your Form Folder and set ``here/testCreateRow`` as your After Validation Script.

Your form will now store its input into your SQL table! Add a few rows to check it out.
Reading a Row, Filling in the Fields

If we want to update records, we're going to have to get rows from our SQL table and use the columns to populate our form fields.

The SQL

Now, use the Management Interface to create, inside your form folder, a Z SQL Method named testReadRow. Set up the following parameters:

Connection ID
    Choose your test database adapter.
Arguments
    Just "uid"

Then, add the SQL Code:

.. code-block:: sql

    select * from simple_db where
        <dtml-sqltest uid type="int">

The <dtml-sqltest ...> operator is a safe way to use user input for an SQL "where" test. The default test is "=".

The Script

Let's wrap this method in a simple Python script that will selectively use it. Create a Python Script with the id formSetup and the Python:

.. code-block:: python

    request = container.REQUEST
    form = request.form

    if form.has_key('uid') and not form.has_key('form.submitted') :
        res = context.testReadRow().dictionaries()
        if len(res) == 1:
            row = res[0]
            for key in row.keys():
                form[key] = row[key]

Let's deconstruct this code.

The if test:

.. code-block:: python

    if form.has_key('uid') and not form.has_key('form.submitted')

will make sure that this code does nothing if the form has already been submitted (we don't want to overwrite values the user just input). It also won't do anything if we don't have a "uid" variable in the form dictionary. (form.submitted is a hidden input that's part of every PFG form.)

If we have a uid variable and we won't be overwriting user input, then we call our SQL read method:

.. code-block:: python

    res = context.testReadRow().dictionaries()

This will return the results of our SQL query in the form of a list of dictionaries.
The dictionary entries will be in the form columnid:value.

Note that the uid value is being passed via the request variable, and doesn't need to be specified.

The rest of the code checks to make sure that we got one result, and throws all of its key:value pairs into the form dictionary -- just where our form will expect them.

The form
========

Now, go to the [override] pane of your form folder, and specify ``here/formSetup`` for your Form Setup Script.

Calling The Form
----------------

Hopefully, you've got a few rows in your table.

Now, try calling your form with the URL::

    http://localhost/testfolder/myform?uid=1

Everything up to the question mark (the query string marker) should be the URL of your form folder.
The "?uid=1" specifies that we want to use the data from the row where the uid is "1".

How would you actually get your users to such a URL? Typically, you'd have some sort of drill-down search that offered them a list of links constructed in this fashion.

Creating a drill-down template is left as an exercise for the reader.

Updating or inserting as necessary
==================================

In this step, we'll create an update SQL method and show how to selectively update or insert data.

Using the Management Interface, create a Z SQL Method inside your form folder with the id testUpdateRow.
For its parameters, set:


Connection ID
    Choose your test database connection.
Arguments
    Add "uid", "string1" and "string2" on separate lines, without quotes.

Then, specify the SQL code:

.. code-block:: sql

    UPDATE simple_db
    SET
        <dtml-sqltest string1 type="string">,
        <dtml-sqltest string2 type="string">
    WHERE <dtml-sqltest uid type="int">

Notice the use <dtml-sqltest ...> for the SQL set id=value lines.
This is a hack that uses sqltest where we could have instead written lines like "string1=<dtml-sqlvar string1 type=string>".

Now, we've got to solve a problem.
How do we update our table under some circumstances, and insert new values under others?

Remember how we set "-1" as the default value of our hidden "uid" form field?
If we've read a record, uid will have changed to match a real row.
If it's "-1", that means that we started with a clean form rather than values read from a table row.

Let's use that knowledge in a simple switchboard script with the id doUpdateInsert:

.. code-block:: python

    request = container.REQUEST
    form = request.form

    if int(form.get('uid', '-1')) >= 0:
        # we have a real uid, so update
        context.testUpdateRow()
    else:
        context.testCreateRow()

Now, go to the [overrides] pane of your form folder and set ``here/doUpdateInsert`` as the *AfterValidationScript*.

.. Note:: Believe it or not ... you're done.

Time to go back and repeat the process with your own table.
Don't forget to add lots of sanity-checking code along the way.

A note on security
==================

It takes extra steps to secure a database connection and SQL methods.

If this is the first time you've worked with a Zope database connection, there's an important security point you may not have considered:

.. warning::

    Zope Database Connections and Z SQL Methods are not part of the Plone workflow.

This means that you may not depend on the Plone content workflow to provide security for these connections and methods.
You must use the Zope security mechanisms directly to control access.

This is also true of Python scripts and other Zope-level objects you might create via the Management Interface.
But Zope provides a safety net of security for most of those.
There is no such automatic safety net for external RDBMS access methods.

The easiest way to do this is to use the Management Interface to visit the top-most folder of your form and use the Security tab to customize security. Look in particular for the Use Database Methods permission, and make sure it is not extended to any user role that should not have a right to read or update your external database.
