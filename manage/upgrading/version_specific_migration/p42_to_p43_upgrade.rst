=========================================================
Upgrading Plone 4.2 to 4.3
=========================================================


.. admonition:: Description

   Instructions and tips for upgrading to a newer Plone version.

.. contents:: :local:


Updating package dependencies
========================================

Plone 4.3's dependencies have been cleaned up so it pulls in fewer packages than Plone 4.2. If your add-on uses one of the packages that was removed, it needs to be updated.

Plone includes a couple hundred Python packages as dependencies. In recent history, many of these have been packages in the zope.app.* namespace that were not strictly necessary, but included as transitive dependencies of other packages. For Plone 4.3 we made a concerted effort to remove unnecessary dependencies.
