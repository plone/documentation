
Theming
=======

To understand Plone's theming story you must first understand the technology
stack on which it is built (or not built).

Zope2
-----

*Old style*

Zope2 is the oldest portion of the stack. It offers technologies like
``Acquisition`` (among others) which facilitate the reuse of objects 
such as page templates amongst a website full of "content" objects.

CMF
---

*Old style*

Next came The Zope ``Content Management Framework`` (CMF); it offers
technologies like file system directory views (FSDV) and skin layers (among
others). The CMF allows people to manage their website's CSS, JavaScript and
image resources on the filesystem, typically inside a "skins" directory.

ZTK
---

*New style*

Initially called Zope 3 (more or less), the ``Zope Toolkit`` (ZTK) is a set of
reusable packages (including ``zope.component`` and ``zope.interface`` which
provide the Zope Component Architecture) that bring a modern, scalable
development environment to Plone.

Diazo
-----

*New style*

Born out of a desire to separate Python package code from website resources
like CSS, JavaScript and images; Diazo (orginally called XDV) is a technology
that maps Plone content to an XHTML template, based on an XML ruleset. 

