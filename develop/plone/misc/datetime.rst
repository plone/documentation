=============
Zope DateTime
=============

.. admonition:: Description

        Using Zope DateTime class in Plone programming


Introduction
------------

Some Plone dates are stored as Zope DateTime objects.
This is different from standard Python datetime (notice the letter casing).
Zope DateTime predates Python datetime which was added in Python 2.4.
Zope DateTime is old code, so do rites necessary
for your religion before programming with it.

* `Zope DateTime HTML API documentation <https://pypi.python.org/pypi/DateTime/>`_

* `Python datetime documentation <http://docs.python.org/library/datetime.html>`_

.. note::

	Using Python datetime is recommended if possible.
	Zope DateTime should be dealt in legacy systems only
	as Python datetime is much more documented and widely used.

Default formatting
-------------------

Since Plone 4

* A per-language format string from a translations is preferred

* If such string is not available the default is taken from portal_properties / site_properties

Formatting examples
===================

US example::

    localTimeFormat: %b %d, %Y
    localLongTimeFormat: %b %d, %Y %I:%M %p

European style format:

    localTimeFormat: %d.%m.%Y (like 1.12.2010)
    localLongTimeFormat: %H:%M %d.%m.%Y (like 12:59 1.12.2010)

More info

* https://dev.plone.org/wiki/DateTimeFormatting

* http://docs.python.org/library/time.html#time.strftime

DateTime API
-------------

`Zope DateTime HTML API documentation <https://pypi.python.org/pypi/DateTime/>`_

You may find the following links useful

* `Source code <http://svn.zope.org/DateTime/trunk/src/DateTime/DateTime.py?rev=96241&view=auto>`_

* `README <http://svn.zope.org/DateTime/trunk/src/DateTime/DateTime.txt?rev=96241&view=auto>`_

* `Interface description <http://svn.zope.org/DateTime/trunk/src/DateTime/interfaces.py?rev=96241&view=auto>`_

Converting between DateTime and datetime
----------------------------------------

Since two different datetime object types are used, you need to often convert between them.

You can convert Zope DateTime objects to datetime objects like so::

        from DateTime import DateTime
        zope_DT = DateTime() # this is now.
        python_dt = zope_DT.asdatetime()

Vice versa, to convert from a Python datetime object to a Zope DateTime one::

        zope_DT = DateTime(python_dt)

Note, if you use timezone information in python datetime objects, you might
loose some information when converting. Zope DateTime handles all timezone
information as offsets from GMT.


DateTime problems and pitfalls
------------------------------

This **will fail** silenty and you get a wrong date::

        dt = DateTime("02.07.2010") # Parses like US date 02/07/2010

Please see

* http://pyyou.wordpress.com/2010/01/11/datetime-against-mx-datetime/

Parsing both US and European dates
----------------------------------

Example::

    # Lazy-ass way to parse both formats
    # 2010/12/31
    # 31.12.2010
    try:
        if "." in rendDate:
            # European
            end = DateTime(rendDate, datefmt='international')
        else:
            # US
            end = DateTime(rendDate)

Friendly date/time formatting
-----------------------------

Format datetime relative to the current time,
human-readable::

    def format_datetime_friendly_ago(date):
        """ Format date & time using site specific settings.

        @param date: datetime object
        """

        if date == None:
            return ""

        date = DT2dt(date) # zope DateTime -> python datetime

        # How long ago the timestamp is
        # See timedelta doc http://docs.python.org/lib/datetime-timedelta.html
        #since = datetime.datetime.utcnow() - date

        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=pytz.utc)

        since = now - date

        seconds = since.seconds + since.microseconds / 1E6 + since.days * 86400

        days = math.floor(seconds / (3600*24))

        if days <= 0 and seconds <= 0:
            # Timezone confusion, is in future
            return "moment ago"

        if days > 7:
            # Full date
            return date.strftime("%d.%m.%Y %H:%M")
        elif days >= 1:
            # Week day format
            return date.strftime("%A %H:%M")
        else:
            hours = math.floor(seconds/3600.0)
            minutes = math.floor((seconds % 3600) /60)
            if hours > 0:
                return "%d hours %d minutes ago" % (hours, minutes)
            else:
                if minutes > 0:
                    return "%d minutes ago" % minutes
                else:
                    return "few seconds ago"

Friendly date/time from TAL
---------------------------

From within your TAL templates, you can call :meth:`toLocalizedTime` like::

    <span tal:replace="python:here.toLocalizedTime(o.ModificationDate)"></span>
