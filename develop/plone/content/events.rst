=========================
 Eventish content types
=========================

.. admonition:: Description

    Creating and programming event and eventish content types in Plone

.. contents:: :local:

Introduction
============

Plone supports events as content. Events have a start time, end time
and other fields. They can be exported to standard ``vCal`` (compatible with
Outlook) and ``iCal`` (compatible with OSX) formats. A default calendar
shows published events in a calendar view.

.. note::

    Recurring events (events repeating with an interval)
    are not supported out-of-the-box on Plone 4.0 or older.

Further reading
----------------

`vs.event <http://plone.org/products/vs.event>`_
    recurring events for Plone 3 and 4.0

`plone.app.event <http://www.zopyx.com/blog/plone.app.event>`_
    recurring events for Plone 4.1+

`Dateable <http://plone.org/products/dateable>`_
    Plone code to bring all the different calendar extensions together

* http://www.inigo-tech.com/blog/customizing-p4a.calendar-and-the-power-of-collections-and-views
* http://regebro.wordpress.com/2009/01/28/ui-help-needed-recurring-events-form-usability/

``portal_calendar``
====================

The ``portal_calendar`` service is provided by ``Products.CMFCalendar``.
It provides facilities to query the event calendar conveniently.

The most useful ``portal_calendar`` call is
``portal_calendar.getEventsForCalendar(month, year, path=navigation_root_path)``
to get the event listing of a certain month.

Adding a new event type to the calendar
------------------------------------------------

Use-case: you've created a content type and want it to be shown in
the calendar portlet.

First add a custom import step. In ``profiles/default/import_steps.xml``

.. code-block:: xml

    <?xml version="1.0"?>
    <import-steps>
        <import-step
            id="compass-types-various"
            version="20090725-02"
            handler="compass.types.setuphandlers.importVarious"
            title="Additional Compass Types Setup">
        </import-step>
    </import-steps>

Then in this custom step call the ``portal_calendar`` service.
Note that you might want to preserve the existing event types.
Plone's default event type is called ``Event``.

``setuphandlers.py``::

    from Products.CMFCore.utils import getToolByName

    def addCalendarTypes(portal):
        portal_calendar = getToolByName(portal, 'portal_calendar')
        # 'Event' was already here, we're just adding the
        # 'DD Training Class' content-type.
        portal_calendar.calendar_types = ('Event', 'DD Training Class')

    def importVarious(context):
        """Miscellaneous steps import handle
        """
        if context.readDataFile('compass.types_various.txt') is None:
            return
        portal = context.getSite()

        addCalendarTypes(portal)

Credits: ecarloshanson, optilude.

Getting eventish content types
------------------------------

``portal_calendar`` maintains the list of eventish content types
appearing in Plone calendar services.

Example::

    # Get tuple of portal_type names for eventish content types
    supported_event_types = portal_calendar.getCalendarTypes()

Getting calendar publishing states
-----------------------------------

Workflow states in which events appear in the calendar::

    portal_calendar.getCalendarStates()

iCal export
==================

Plone 3+ provides ``ics_view`` which applies to:

* Single :guilabel:`Event` content items
* :guilabel:`Folder`\s

The view creates an ``iCal`` export of the content.
A single exported ``iCal`` file (mimetype: ``text/calendar``) can contain
several events.
When applied to a folder, the view exports all items that provide the
``Products.ATContentTypes.interfaces.ICalendarSupport`` interface.

More info:

* http://stackoverflow.com/q/11862095/315168

* https://github.com/plone/Products.ATContentTypes/blob/master/Products/ATContentTypes/browser/calendar.py#L25

Purging old events
=======================

After the event end day the event stays visible in Plone listings.

You need to have a special janiator script / job if you want to get old events
deleted from your site after they have been passed.

Below is a ZMI script which will delete events which are more than 30 days past their ending date::


     from StringIO import StringIO
     import DateTime

     buf = StringIO()

     # DateTime deltas are days as floating points
     # Select events which have the event ending date more than one month in past
     end = DateTime.DateTime() - 30*1
     start = DateTime.DateTime(2000, 1,1)

     date_range_query = { 'query':(start,end), 'range': 'min:max'}

     items = context.portal_catalog.queryCatalog({
                 "Language": "all", # Bypass LinguaPlone language check
                 "portal_type":["CompanyEvent", "VSEvent"],
                 "end" : date_range_query,
                 "sort_on" : "created" })

     items = list(items)

     print >> buf, "Found %d items to be purged" % len(items)

     count = 0
     for b in items:
         count += 1
         obj = b.getObject()
         print >> buf, "Deleting:" + obj.absolute_url() + " " + str(obj.created())
         obj.aq_parent.manage_delObjects([obj.getId()])

     return buf.getvalue()


Recurrence calendar support in Plone 3
======================================

``vs.event`` has an index ``recurrence_days``
which stores the dates when the recurrent event
appears five years ahead of the time when the event is saved.

Below is the glue code which is needed to support
the recurrent event in the Plone 3 calendar portlet.
It combines ``vs.event``, ``plone.app.portlets`` and ``Products.CMFCalendar``
bits to pull the necessary stuff together (a task which was not
trivial).

Making recurrent event appear in the calendar portlet
------------------------------------------------------

Below is a calendar portlet ``Renderer`` code
which can be used to make recurrent events appear in the
standard Plone calendar portlet::

    """

        Override the default Plone 3 calendar portlet to support
        rendering of recurring events.

    """

    import datetime

    from Acquisition import aq_inner
    from DateTime import DateTime

    from zope.i18nmessageid import MessageFactory
    from zope.interface import implements
    from zope.component import getMultiAdapter

    from plone.app.portlets.portlets import calendar as base

    # Package with various calendar support code
    # - not very well documented
    import dateable.kalends

    def convert_to_indexed_format(year, month, daynumber):
        """ Convert datetime to vs.event recurrence_days index format.

        recurrence_days holds the date as compressed int format
        for efficiency reasons.

        See vs.event.context.recurrence for more information.

        @return: Indexed recurrenct_day format of given date or None if not supported
        """

        # This is an empty cell in the calendar and does not represent any meaningful day
        if daynumber == 0:
            return None

        cur_date = datetime.date(year, month, daynumber)

        return cur_date.toordinal()


    def create_event_structure(portal_calendar, results, year, month):
        """ Create calendar dict/list struct for event presentation.

        This code is mostly ripped from Products.CMFCalendar.calendar.CalendarTool catalog_getevents()

        @param results: Iterable of eventish brain objects

        @return: Dict day number -> event data
        """

        last_day = portal_calendar._getCalendar().monthrange(year, month)[1]
        first_date = portal_calendar.getBeginAndEndTimes(1, month, year)[0]
        last_date = portal_calendar.getBeginAndEndTimes(last_day, month, year)[1]

        # compile a list of the days that have events
        eventDays={}
        for daynumber in range(1, 32): # 1 to 31
            eventDays[daynumber] = {'eventslist': [],
                                    'event': 0,
                                    'day': daynumber}
        includedevents = []
        for result in results:
            if result.getRID() in includedevents:
                break
            else:
                includedevents.append(result.getRID())
            event={}
            # we need to deal with events that end next month
            if  result.end.month() != month:
                # doesn't work for events that last ~12 months
                # fix it if it's a problem, otherwise ignore
                eventEndDay = last_day
                event['end'] = None
            else:
                eventEndDay = result.end.day()
                event['end'] = result.end.Time()
            # and events that started last month
            if result.start.month() != month:  # same as above (12 month thing)
                eventStartDay = 1
                event['start'] = None
            else:
                eventStartDay = result.start.day()
                event['start'] = result.start.Time()

            event['title'] = result.Title or result.getId

            if eventStartDay != eventEndDay:
                allEventDays = range(eventStartDay, eventEndDay+1)
                eventDays[eventStartDay]['eventslist'].append(
                        {'end': None,
                         'start': result.start.Time(),
                         'title': event['title']} )
                eventDays[eventStartDay]['event'] = 1

                for eventday in allEventDays[1:-1]:
                    eventDays[eventday]['eventslist'].append(
                        {'end': None,
                         'start': None,
                         'title': event['title']} )
                    eventDays[eventday]['event'] = 1

                if result.end == result.end.earliestTime():
                    last_day_data = eventDays[allEventDays[-2]]
                    last_days_event = last_day_data['eventslist'][-1]
                    last_days_event['end'] = (result.end-1).latestTime().Time()
                else:
                    eventDays[eventEndDay]['eventslist'].append(
                        { 'end': result.end.Time()
                        , 'start': None, 'title': event['title']} )
                    eventDays[eventEndDay]['event'] = 1
            else:
                eventDays[eventStartDay]['eventslist'].append(event)
                eventDays[eventStartDay]['event'] = 1

            # This list is not uniqued and isn't sorted
            # uniquing and sorting only wastes time
            # and in this example we don't need to because
            # later we are going to do an 'if 2 in eventDays'
            # so the order is not important.
            # example:  [23, 28, 29, 30, 31, 23]
        return eventDays


    class RecurrentEventCalendarPortletRenderer(base.Renderer):
        """ Support recurring events """

        def retroFitRecurrentEvents(self, year, month, weeks):
            """
            List recurrencing events in the calendar

            1. Get a list of supported event types
            2. Build a list of queried recurrence_days
            3. Query all recurrent events occurring in the given month
            4. Retrofit calendar data with these recurrent events.

            @param weeks: Array of displayable calendar weeks.
            """

            context = aq_inner(self.context)
            request = self.request

            portal_calendar = self.context.portal_calendar

            # Get tuple of portal_type names for eventish content types
            supported_event_types = portal_calendar.getCalendarTypes()

            # Build a list of queried dates in recurrence_days format
            recurrence_days_in_this_month = []
            for week in weeks:
                for day in week:
                    # This is an empty cell in the calendar
                    # and does not present a meaningful date
                    daynumber = day['day']
                    date = convert_to_indexed_format(year, month, daynumber)
                    if date:
                        recurrence_days_in_this_month.append(date)

            # print "recurrence_days:" + str(recurrence_days_in_this_month)

            # Query all events on the site
            # Note that there is no separate list for recurrent events
            # so if you want to speed up you can hardcode
            # recurrent event type list here.
            matched_recurrence_events = self.context.portal_catalog(
                            portal_type=supported_event_types,
                            recurrence_days={
                                "query":recurrence_days_in_this_month,
                                "operator" : "or"
                            })

            # print "Matched events:" + str(len(list(matched_recurrence_events)))

            portal_catalog = self.context.portal_catalog

            for week in weeks:
                for day in week:
                    daynumber = day['day']

                    # This day is a filler slot and not a real date in a calendar
                    if daynumber == 0:
                        continue

                    cur_date = convert_to_indexed_format(year, month, daynumber)

                    for event in matched_recurrence_events:
                        # The event hit this date
                        # Get event brain result id
                        rid = event.getRID()
                        # Get list of recurrence_days indexed value.
                        # ZCatalog holds internal Catalog object which we can directly poke in evil way
                        # This call goes to Products.PluginIndexes.UnIndex.Unindex class and we
                        # read the persistent value from there what it has stored in our index
                        # recurrence_days
                        indexed_days = portal_catalog._catalog.getIndex("recurrence_days").getEntryForObject(rid, default=[])

                        if cur_date in indexed_days:
                            # Construct event info
                            # See CalendarTool.catalog_getevents()

                            day["event"] = True # This day has events

                            data = {}
                            # Shortcut the event to be one day event (though this might not be a case)
                            data["start"] = None
                            data["end"] = None
                            data["title"] = event["Title"]

                            day["eventslist"].append(data)


        def getEventsForCalendar(self):
            """
            This has been overridden to call recurrent event fetcher.

            The code is basically copy-paste from the base class.
            """
            context = aq_inner(self.context)
            year = self.year
            month = self.month
            portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
            navigation_root_path = portal_state.navigation_root_path()
            weeks = self.calendar.getEventsForCalendar(month, year, path=navigation_root_path)

            # Patched recurrent events go in here
            self.retroFitRecurrentEvents(year, month, weeks)

            for week in weeks:
                for day in week:
                    daynumber = day['day']

                    if daynumber == 0:
                        continue

                    day['is_today'] = self.isToday(daynumber)
                    if day['event']:
                        cur_date = DateTime(year, month, daynumber)
                        localized_date = [self._ts.ulocalized_time(cur_date, context=context, request=self.request)]
                        day['eventstring'] = '\n'.join(localized_date+[' %s' % self.getEventString(e) for e in day['eventslist']])
                        day['date_string'] = '%s-%s-%s' % (year, month, daynumber)

            return weeks

Beta code notice
----------------

Make sure that the ``recurrence_days`` index from ``vs.event`` is working -
if it isn't, check
:doc:`Custom indexing example </develop/plone/searching_and_indexing/indexing>`
how to create your own recurrency indexer.
After you save your ``vs.event`` content item,
you should see data in the ``recurrence_days`` index through
``portal_catalog`` browsing interface.

Further reading
---------------

* http://plone.293351.n2.nabble.com/what-s-dateable-chronos-how-to-render-recurrence-events-in-a-calendar-portlet-tp5282788p5287261.html

* ``vs.event`` has ``KeywordIndex`` ``recurrence_days`` which contains a
  * value
  created by
  ``vs.event.content.recurrence.VSRecurrenceSupport.getOccurrenceDays()``.
  This value is a list of dates 5 years ahead when the event occurs.

* Plone 3 provides a view called ``calendar_view`` (configured in
  * ``Products.CMFPlone/deprecated.zcml``)
  but this view is not used - do not it let fool you.

Required :term:`ZCML` for the indexing::

    <adapter factory=".indexing.recurrence_days"/>


