======================
Eventish content types
======================

.. admonition:: Description

    Creating and programming event and eventish content types in Plone


Introduction
============

Plone supports events as content. Events have a start time, end time and other fields.
They can be exported to standard ``vCal`` (compatible with Outlook) and ``iCal`` (compatible with OSX) formats.
A default calendar shows published events in a calendar view.

.. note::

    Recurring events (events repeating with an interval) are supported out-of-the-box on Plone 5.


This is provided by `plone.app.event <https://github.com/plone/plone.app.event>`_ (`documentation <https://ploneappevent.readthedocs.org/en/latest/>`_)



Purging old events
==================

After the event end day the event stays visible in Plone listings.

You need to have a special janitor script / job if you want to delete old events from your site.

