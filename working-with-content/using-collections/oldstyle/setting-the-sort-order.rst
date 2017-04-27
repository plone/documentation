Setting the Sort Order
===========================

Learn how to use the Sort Order feature to customize the order in which
your results display

The Sort Order **determines the order the results of the Collection will
be displayed in**. Sort Order allows you to sort by three main
categories: text, object properties, and dates. When you sort by text,
objects will be sorted in alphabetical order. When sorting by one of the
object properties, we effectively are grouping objects together by the
specified properties. When we sort by a date the results will be
displayed with the most recent first (although there are many 'dates' in
Plone). All Sort Orders are in Ascending Order unless the Reverse Order
check box is selected. By checking this we can display in reverse order,
or newest dates first, etc.

**Dates**
-------------

There are numerous Date options which will be explained in the next
section of the manual.

Object Properties
-----------------

**Item Type**

When sorting by Item Type, we end up with a Collection that has results
that are grouped by Item Type. We would want to use this if we have a
Collection that will return many different Item Types. This way we can
make the Collection very easy to browse for the site visitor.

**State**

Sorting by State will display results grouped by the publishing state.
Since there are only two States in the default configuration of Plone,
there will only be Published and Private items. We can use this to
separate all pages on our site and see what we have that is
public (Published) and what we are hiding from the public eye (Private).

**Category**

Category Sort Order is useful when we want to display the objects on our
site in a manner where they are grouped by the Category we placed them
in. Keep in mind, for sorting by Category to even be remotely useful,
you must have specified the Category on several objects. If you have not
specified any Categories, then sorting by Categories will do nothing.

**Related To**

The Related To Sort Order will actually apply a criterion to your
Collection. It limits to the results to only those that have Related To
information specified on their properties.

Text
----

**Short Name**

Sorting by the Short Name is the same as putting the result objects in
alphabetical order. By default Plone sets the Short Name of an object to
be the same as the Title. The difference between the two is that the
Short Name is all lower case and hyphenated between all words. For
example the Short Name for the page titled About Us would be *about-us*.
The Short Name is what Plone also uses in the URL for the page
(www.myplonesite.org/about-us). You can specify a different Short Name
for an object by using the Rename button on the Contents tab.

**Creator**

Sorting by the Creator will group all results in alphabetical order by
their author. For example, let's say we had several documents published
by Bob Baker and several of other documents published by Jane Smith.
Sorting by the creator would result in all the documents created by Bob
Baker listed first followed by those of Jane Smith.

**Title**

Sorting by Title will display the results in alphabetical order, by
the object titles.

Next we will cover the Dates that we skipped over in this section as
well as the Criteria Field section.

