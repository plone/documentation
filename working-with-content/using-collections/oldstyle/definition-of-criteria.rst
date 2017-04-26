Definition of Criteria
===========================

Definitions and examples of the different criteria fields available

The power of Collections most certainly lies with the Criteria fields.
Mastering how to use the different Criteria will allow you to use
Collections in several useful ways. In this section, we will use
examples to illustrate the many ways of using Criteria.

Categories
--------------

The Category criterion allows you to search the **Category field** of
objects. For this to work you must specify Categories for the content
objects ahead of time (this is done through the Categorization tab on
content objects). An example where you could use this is you want to
create a Collection that would display all objects relating to the
Category *Organization*. As you can see in the image below, we are able
to select the value *Organization* for our criterion. Then, by saving
this criterion and viewing our Collection, the results would be all
content objects we had designated with the Category *Organization*.

Once again the values available to you are completely dependent on what
you have specified on your objects in the Categorization tab.

Creator
-----------

When using the Creator criterion, we are **filtering objects based on
who created them**. This might be useful if you want to do a featured
author section, where you would only want to display content on your
site that has been created by a certain author.

As you can see we have several options for our criterion type. They
allow us to restrict the creator to the person currently logged in,
enter the name of another user as text, or to select users from a list.

If you want to display results from multiple users, you would need to
use the **List of Values** option. Otherwise you would normally use the
Text option unless the creator you wanted to select was yourself in
which case you would use Restrict to Current User.

Description
---------------

The Description field is essentially a **search box type** criterion.
However, instead of searching the title and body of a page, it will
**only search for the text in the Description field** of a content
object. This criterion is only really useful if you fill out the
Description field consistently for all your content objects.

Location
------------

Using the Location criterion is much like specifying a location when you
search for a document on your hard drive. By specifying a Location
criterion, **the results that are displayed in your Collection will only
come from that location**, most commonly a Folder. This can be useful if
you only want to display content that is in the About Us section of your
site, for example. This is also useful for narrowing Collection results
when combined with other criteria.

To specify a Location, simply click the **Add button**, which will pop
up a new window showing you a directory of your site. If we follow our
example and want to search the About Us section of our site, we would
click the Insert button next to the About Us folder.

You can open folders to view content contained within them either by
clicking the Browse button or directly on the title of the folder you
want to open. You may also use the Search box to search for the Title of
an object.

Search Text
---------------

The Search Text is a very useful criterion. It is similar to the search
box on your site or an Internet search engine. It takes the text you
specify and searches the Title, Description, and Body of all objects and
returns **any that have the word or phrase you specify**. This is useful
when you want to find objects that have to deal with a certain thing,
especially if the word or phrase appears across many content types.
Using training.plone.org as an example, if I want to create a Collection
that displays all objects that reference the word Collections, I would
use the Search Text criterion and specify *collections*. All Tutorials,
Videos, Glossary items, etc with *collections* in the Title,
Description, or Body would then appear in the Collection results.

Related To
--------------

The Related To field is another field, like Category, that **must be
specified on a content object prior to being used for a Collection**.
The Related To field on an object lets you specify which other objects
in your site are similar or are relevant to the object you created. By
specifying this field, when you create an object you can create a web of
related content that will reference each other (think of a "see also"
kind of function). When you have done this, you can use the Related To
criterion in a Collection to display anything related to a specific
object.

In this case we have specified that there are pages related to Our
Staff, History, and the About Us Homepage. By selecting one or multiple
values from this list, our Collection will display the pages that
related to that Value.

If we selected History as the value we wanted, our Collection would show
us everything that is related to the History page.

Keep in mind that the Related To Values list does not work based on
which objects are related to content but on which objects have another
object related **to it**. The Collection will display the results that
are related to that value.

State
---------

Using the State criterion is very simple. It allows us to **sort by
published or private** state. It is a very good idea to restrict
publicly viewable Collections **to filter on published**, so that no
private content appears in the Collection results. Filtering on the
Private state can be useful as well. For example, a site administrator
might want to quickly see private content, so that they could determine
what work needs to be done and what could deleted.

Dates
---------

You may have noticed that there are **several different dates
available** to use as Criteria. Since there are such a large number of
dates, they will be covered in :doc:`their own section of the manual <using-and-understanding-dates>`

