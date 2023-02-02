.. -*- coding: utf-8 -*-

=============
Mr. Developer
=============

This buildout uses mr.developer to manage package development.
See http://pypi.python.org/pypi/mr.developer for more information,
or run :command:`bin/develop help` for a list of available commands.

The most common workflow to get all the latest updates is::

  > git pull
  > bin/develop rb

This will get you the latest coredev configuration,
checkout and update all packages via git and Subversion in src and run buildout to configure the whole thing.

From time to time you can check if some old cruft has accumulated::

  > bin/develop st

If this prints any lines with a question mark in front, you can cleanup by::

  > bin/develop purge

This will remove packages from :file:`src/` which are no longer needed,
as they have been replaced by proper egg releases of these packages.
