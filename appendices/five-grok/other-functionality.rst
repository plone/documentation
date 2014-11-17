Other five.grok functionality
=============================

**What we haven't covered**

Grok and *five.grok* provide some functionality we deliberately haven’t
discussed in this manual. This includes:

-  Annotation factories. Annotations are very useful, but the pattern of
   using a persistent object as the adapter implementation instead of
   just using the *IAnnotations* from *zope.annotation* and its
   dict-like API to store primitives can lead to problems when code is
   moved or uninstalled. See `grokcore.annotation`_ for an example of
   this functionality.
-  Defining permissions with *grok.Permission*. We prefer to define
   permissions in configuration files, rather than code. See
   `grokcore.security`_ if you hate XML so much that you don’t mind
   using Python as a configuration language. See the :doc:`Dexterity
   developer manual </external/plone.app.dexterity/docs/index>` for more details on creating custom permissions.
-  Defining resource directories (other than the implicit *static*
   directory) using *grok.DirectoryResource* instead of the
   *<browser:resourceDirectory />* directive, for the same reasons. See
   `grokcore.view`_.
-  Defining local component sites and local utilities using
   `grokcore.site`_. In Plone, we use the *componentregistry.xml*
   GenericSetup import step for this purpose.
-  Creating browser layers with the *grok.skin()* directive. In Plone,
   we use the *browserlayer.xml* GenericSetup import step and/or the
   `plone.theme`_ package for this purpose.
-  Forms using `grokcore.formlib`_. For Dexterity development, we use
   `z3c.form`_ instead.
-  Model objects using *grok.Model*. We use Dexterity content objects
   instead.
-  The *grok.order()* directive, used to order viewlets based on an
   integer weighting. We use the base class for
   *plone.app.viewletmanager* instead, which supports explicit ordering
   as part of a theme. See `grokcore.viewlet`_ for details on how
   *grok.order()* works.
-  The *view/static* variable. This allows access to static resources in
   the *static* directory using TAL expressions like
   *tal:attributes=“href view/static/stylesheet.css”*. Unfortunately,
   the link this results in will always be relative to the context,
   rather than relative to the site navigation root, which means that it
   will not cache well. Therefore, we construct the URL manually
   instead. See `grokcore.view`_ for more details.

Some of this reflects the Dexterity developers’ preferences and views.
You are allowed to disagree.

.. _grokcore.annotation: https://pypi.python.org/pypi/grokcore.annotation
.. _grokcore.security: https://pypi.python.org/pypi/grokcore.security
.. _grokcore.view: https://pypi.python.org/pypi/grokcore.view
.. _grokcore.site: https://pypi.python.org/pypi/grokcore.site
.. _plone.theme: https://pypi.python.org/pypi/plone.theme
.. _grokcore.formlib: https://pypi.python.org/pypi/grokcore.formlib
.. _z3c.form: https://pypi.python.org/pypi/z3c.form
.. _grokcore.viewlet: https://pypi.python.org/pypi/grokcore.viewlet
