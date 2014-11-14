Working with the new resource registry
======================================

If you want to include a pattern in Plone 5's new resource registry, follow
these instructions.


Include a pattern from the ``Mockup`` package in Plone core
-----------------------------------------------------------

The ``Mockup`` package is already a core dependency of ``Products.CMFPlone``
and Mockup's pattern directory is available as a browser resource and thus
accessible for Plone.

All you have to do is to edit
``Products/CMFPlone/profiles/dependencies/registry.xml`` and add the a new
record for your pattern. You have to define a name, like
``plone.resources/mockup-patterns-select2`` and the paths to your JS and LESS
files. Don't forget to rerun the profile again (the name of this profile is:
"Mandatory dependencies for a Plone site").

If you want to include your pattern by default, include it in the
``Products/CMFPlone/static/plone.js`` bundle, compile it client-side via the
new resource registry (``@@resourceregistry-controlpanel``), which puts the
compiled file back to the filesystem, commit it and push it.


Include a pattern from an external Mockup based project in your Plone project
-----------------------------------------------------------------------------

If your pattern is in a separate package than ``Mockup``, then you have to make
sure that your pattern is accessible for Plone via a browser resource.
You also have to provide a Generic Setup profile for plone.app.registry
(``registry.xml``) and add an entry for your pattern in it.
