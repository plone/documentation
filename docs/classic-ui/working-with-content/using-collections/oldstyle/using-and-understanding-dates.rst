Using and Understanding Dates
==================================

Explanation of the Dates associated with Collections and their uses

There are several different types of dates we can choose from, many of
them sounding similar. Because of this it is very easy to get confused
about which date to use. Below, each date option is defined.

Dates Defined
-------------

**Creation Date**
The Creation Date is the date the document was made. You can think of
this as its birthday, the day it was born. You cannot change the
Creation Date of an object.

**Effective Date**
The Effective Date is the date when an object becomes published. This
date is customizable through the **Edit tab** on objects under the
**Date tab**. However, there it is referred to as the Publishing Date (a
minor discrepancy in Plone's nomenclature).

**Creation Date** and **Effective Date** are very similar. They both are
representative of the beginning point of an object. A very important
point to keep in mind when choosing which one you want to use, is that
an object can be created long before it ever becomes public. You could
have a page that is worked on for several weeks before it is actually
published. Thus you would get different results in a Collection
depending on which date you used.
We recommend using the **Effective Date**, instead of Creation Date for
date-oriented Collections. This way your Collection shows results based
on when they became viewable to the public, which is more relevant to
the audience of your Collection. Also, you can go in and manually adjust
the Effective Date to control the sort order which is not something you
can do with the Creation Date.

**Expiration Date**
The Expiration Date refers to the day that the item will no longer
become publicly available. This date is also customizable through the
Edit tab (shown above) like the Effective Date. By default, objects have
no Expiration Date.

**Modification Date**
The Modification Date is the date the object was last edited. Note that
this date is first set the day the object is created and will
automatically change every time the object is edited. There is no way to
customize this date. You could use this as a Sort Order along with an
Item Type criterion set to Page, to display all recently modified pages
within the last week, for example. The What's New listing on the
homepage of LearnPlone.Org uses Modification Date as its date criterion.
That way both newly created documents *and* ones that have been updated
appear in the listing.

**Event Specific Dates**
The two following dates **only** apply to objects that
are **Events.** These two dates are very effective for creating Recent
Events and Upcoming Events Collections that will let your audience know
what your organization is doing and will be doing in the future.

**Start Date**
The Start Date is simply the date that an Event starts.

**End Date**
The End Date is simply the date that the Event ends.

**Publication Date**

The Publication Date is the date when object was last published. It can
either be set manually by means of Effective Date field or, if the
latter hasn't been set, calculated based on date when object was last
published.

To display Publication Date on your pages you need to switch it on with
*"Display publication date in 'about' information"* option in **Site
Settings Control Panel**. Publication Date will be visible right before
object Modification Date inside 'about' information area. Make sure
*"Allow anyone to view 'about' information"* option is also enabled
inside **Security Settings Control Panel** to make it all work.

Setting Dates
-------------

A confusing thing about dates can be how its Criteria are set up. They
have a setup that is not like any of the other Criteria. First off, you
have to choose whether you want a Relative Date or a Date Range.

The Relative Date allows you to construct a **conditional statement**.
Such as: Items modified less than 5 days in the past. A Date Range will
allow you to **specify an exact range of dates**, such as 01/02/08 to
02/02/08. The Date Range is useful when you want to create a Collection
with a static date that won't change. The Relative Date can be very
useful as it will allow you to create Collections that are automatically
updating themselves, such as a Recent News Collections or an Upcoming
Event Section.

Relative Date
-------------

Looking first at the Relative Date option, you can see we have three
options to fill out.

The first option is **Which Day**. This allows us to select the number
of days our criterion will include. One of the options is called *Now*.
Using this will set the date range to the current day. The other two
options do not matter and can be ignored when using *Now*.

The second option is **In the Past or Future**. This enables us to
choose whether we are looking forward or backward into time.

The last option is **More or Less**. Here we can choose from three
options. *Less than* allows us to include everything from now to a
period of time equal to or less than the **Which Day** setting, either in
the past or future. *More than* will include everything from beyond our
specified number of days equal to or more than **Which Day**. Finally
*On the Day* will only include things that are on the day we specified in
the **Which Day**. Using the example in the image above if we had
selected *On the Day* instead of *Less than* our Collection would
display only objects that were modified (we are using the Modification
Date criterion) 5 days ago.

If this is confusing to you, try reading it as a statement substituting
in the field options you chose. "I want the results to include objects
**More or Less** than **Which Day**, **In the Past or Future**". Our
example in the image above would become "I want the results to include
objects **Less than** **5 days in the past**".

Date Range
----------

The **Date Range** is much easier to understand. Both a Start Date and
End Date are required (do not confuse these terms with the Event
Specific dates!). The Date Range allows us to enter a beginning and an
end date and the display everything within that time frame. Notice also
that it allows us to specify a specific time of day as well.

