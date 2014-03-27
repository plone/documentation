=============================
ATContentTypes
=============================

.. admonition:: Description

        Since Plone 2.1, Plone has shipped with ATContentTypes for its
        default content types

“ATContentTypes”:/products/atcontenttypes is a re-implementation of the
standard CMF types as Archetypes content. It adds a numer of features to
the standard CMF types and offers more flexibility in extending and
re-using content types. The “RichDocument
tutorial”:/documentation/tutorial/richdocument explains how
ATContentTypes are subclassed and how they make use of the latest
conventions in Archetypes and CMF.
The ATContentTypes product is installed during the creation of a Plone
site. It will migrate the base CMF content types to its own equivalents
using its own highly generic migration framework.
Please note that ATContentTypes aims to be usable in plain CMF. It has a
number of optional Plone dependencies, in the form::

 if HAS_PLONE21:
 …
 else:
 …

Plone has no direct dependencies on ATContentTypes, nor on Archetypes.
There are a few generic interfaces in ‘CMFPlone.interfaces’ that are
used by both Archetypes/ATContentTypes and Plone, but we do not wish to
have any direct dependency on Archetypes, since Archetypes is
essentially just a development framework to make developing CMF content
types easier. By minimising the number of dependencies, we ensure that
plain-CMF (and in the future, plain-Zope 3) content types are still
usable within Plone.
ATContentTypes and Plone both depend on ‘CMFDynamicViewFTI’. This is a
wrapper on the standard CMF FTI type that adds support for the ‘display’
menu by recording a few extra properties for the available and
currently-selected view methods. It also provides a mixin class,
‘CMFDynamicViewFTI.browserdefault.BrowserDefaultMixin’, which enables
support for the ‘display’ menu (or rather, the interface
‘CMFDynamicViewFTI.interfaces.ISelectableBrowserDefault’).
