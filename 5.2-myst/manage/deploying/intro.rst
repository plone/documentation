============
Introduction
============

The purpose of this guide; its audience and assumptions
========================================================

This guide is an overview of how to set up Plone and its supporting software stack for production purposes on one of the popular Unix work-alike operating systems.

We’ll cover platform preparation and basic considerations for installation of Plone itself.
We’ll also go into common setups of the other parts of the deployment stack needed for real-life deployment:

* A general-purpose web server to handle URL rewriting and integration with other web components;
* Load balancing;
* Server-side caching;
* Backup;
* Log rotation;
* Database packing

We won't cover the details of installation or actual tool setup.
Those are better covered in the :doc:`Installation </manage/installing/installation>` and other :doc:`Hosting </manage/deploying/index>` guides.

And, what about Windows?
========================

Production deployment for Windows is typically very different from that on Unix-like systems.
While some parts of the common open-source stack are available on Windows (Apache, for example), it's more common to integrate
using tools like IIS that are often already in use in the enterprise.
If your shop is committed to a Microsoft stack, this document won't be of much use to you.
However, if you're on a Windows server, but open to using the (very often superior) open-source alternatives to Microsoft application components, the stack and tools discussion here may be very useful.

Audience
========

There is one audience for this document: system administrators who wish to deploy Plone for a production server.
We assume that you know how to install and configure your operating system, including its package manager or port
collection, file system, user permissions, firewalls, backup and logging mechanisms.

You should be able to use the command-line shell and able to translate between the file paths and hostnames used in examples and the ones you’ll be using on your deployed server.

You’ll need root access (or sudo privileges) adequate to install packages, create users and set up cron jobs.

The instructions below have been tested with clean OS platforms created on commodity cloud servers.

Assumptions
===========

We’ll be describing base-level production deployments that will meet many, but not all needs.
And we’ll be using the most commonly used and widely supported tools for the stack. Tools like Apache, Nginx, haproxy and rsync.

You may have other needs (like integration with LDAP or a relational database) or wish to use other tools (Apache Traffic Server, Varnish, squid …). That’s fine, and there are many good documents elsewhere in the plone.org documentation section that cover these needs and tools.

Security considerations
=======================

The approaches we describe here are practical for many Internet and Intranet servers.
However, they should be considered a baseline and may not meet your security needs.
Plone can be deployed in chroot jails or OpenSolaris zones or with much more compartmentalized process and file ownership if your application requires a greater degree of protection.
