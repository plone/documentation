============
Introduction
============

.. contents:: :local:

.. admonition:: Description

    The Pluggable Authentication Service (PAS) is an alternative 
    to the standard Zope User Folder 
    or the popular Group User Folder (GRUF). 
    PAS has a highly modular design, which is
    very powerful, but also a lot harder to understand.

PAS is built around the concepts of interfaces and plugins:
all possible tasks related to user and group management and authentication
are described in separate interfaces.
These interfaces are implemented by plugins
which can be selectively enabled per interface.

Plone uses PlonePAS, which extends PAS with a couple of extra plugin types
and which adds GRUF compatibility.
Since PlonePAS extensions are rarely needed and are subject to change
in new Plone releases, this tutorial will focus only on pure PAS features.
