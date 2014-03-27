===========================
Useful buildout recipes
===========================

.. admonition:: Description

   A list of the most common and useful buildout recipes used when
   working with Plone.

The list is more or less sorted by topic. Check all available
recipes `at PyPI`_.


-  `zc.recipe.egg`_ - Installs eggs into a buildout eggs directory.
   It also generates scripts in a buildout bin directory with egg
   paths baked into them.
-  `infrae.subversion`_ - This zc.buildout recipe will check out a
   *number* of URLs into its parts directory. It won't remove its
   parts directory if there are any changes in the checkout, so it's
   safe to work with that checkout for development.
-  `plone.recipe.zope2install`_ - Installs Zope 2, i.e. its Python
   libraries and scripts, but doesn't create any instance.
-  `plone.recipe.zope2instance`_ - Creates and configures a Zope 2
   instance in parts. It also installs a control script, which is like
   zopectl, in the bin/ directory.
-  `plone.recipe.zope2zeoserver`_ - This recipe creates and
   configures a Zope 2 ZEO server in parts. It also installs a control
   script, which is like zeoctl, in the bin/ directory.
-  `plone.recipe.distros`_ -  Installs distributions, i.e. Zope
   products not packaged as eggs.
-  `plone.recipe.apache`_ - Builds and configures the Apache web
   server.
-  `gocept.nginx`_ - zc.buildout recipe for configuring an nginx
   server
-  `plone.recipe.varnish`_ - Installs the Varnish reverse-cache
   proxy. It works for non-Zope sites as well.
-  `plone.recipe.squid`_ - Installs the Squid proxy. It works for
   non-Zope sites as well.
-  `collective.recipe.omelette`_ - Creates a unified directory
   structure of all namespace packages, symlinking to the actual
   contents, in order to ease navigation.
-  `collective.recipe.i18noverrides`_ - Creates an i18n directory
   within one or more Zope 2 instances in your buildout. It copies
   some .po files to those directories. The translations in those .po
   files will override any other translations.
-  `zc.recipe.cmmi`_ - The Configure-Make-Make-Install recipe
   automates installation of configure-based source distribution into
   buildouts.
-  `plone.recipe.command`_ - Execute arbitrary commands in buildout
   through os.system.

.. _at PyPI: http://pypi.python.org/pypi?:action=browse&show=all&c=512
.. _zc.recipe.egg: http://pypi.python.org/pypi/zc.recipe.egg/
.. _infrae.subversion: http://pypi.python.org/pypi/infrae.subversion/1.4.5
.. _plone.recipe.zope2install: http://pypi.python.org/pypi/plone.recipe.zope2install/
.. _plone.recipe.zope2instance: http://pypi.python.org/pypi/plone.recipe.zope2instance/
.. _plone.recipe.zope2zeoserver: http://pypi.python.org/pypi/plone.recipe.zope2zeoserver/
.. _plone.recipe.distros: http://pypi.python.org/pypi/plone.recipe.distros/
.. _plone.recipe.apache: http://pypi.python.org/pypi/plone.recipe.apache/
.. _gocept.nginx: http://pypi.python.org/pypi/gocept.nginx/0.9.4
.. _plone.recipe.varnish: http://pypi.python.org/pypi/plone.recipe.varnish/
.. _plone.recipe.squid: http://pypi.python.org/pypi/plone.recipe.squid
.. _collective.recipe.omelette: http://pypi.python.org/pypi/collective.recipe.omelette/
.. _collective.recipe.i18noverrides: http://pypi.python.org/pypi/collective.recipe.i18noverrides/
.. _zc.recipe.cmmi: http://pypi.python.org/pypi/zc.recipe.cmmi/
.. _plone.recipe.command: http://pypi.python.org/pypi/plone.recipe.command/
