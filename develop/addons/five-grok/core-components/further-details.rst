Further details 
================

**Where to find more information about the core components**

In this section, we have described how to use *five.grok* to configure
standard Zope Component Architecture components. In fact, the
functionality for this can be found in the `grokcore.component`_
package, and does not strictly require the use of *five.grok*: you could
use *grokcore.component* directly. This may be useful if you are trying
to create a package that should work with other frameworks using the
Zope Toolkit / Zope 3, such as Grok itself.

grokcore.component contains a few other grokkers and helper functions
which we have not described here. You are encouraged to read its
`documentation`_ for details.

If you need to introspect the interfaces of your components, you should
also take a look at the *zope.interface* API, which for example provides
functions for enumerating the interfaces implemented by a class or
provided by an object.

If you need to introspect the component architecture itself, look up the
*zope.component* API, where you will find methods for enumerating,
querying, registering and removing adapters, utilities and event
subscribers.

Both of these packages have interfaces containing copious internal
documentation.

.. _grokcore.component: http://pypi.python.org/pypi/grokcore.component
.. _documentation: http://pypi.python.org/pypi/grokcore.component
