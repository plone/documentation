Utilities 
===========

**Singletons and registries with utilities**

Utilities are simple components which may be looked up by interface and
optionally name. They are used for two purposes:

#. To implement a “singleton” - an object which is created in memory
   once and shared by all clients.
#. To implement a registry of objects all providing the same interface.
   In this case, each object is a named utility.

As with all components, utilities can be local or global. A local
utility is installed as a persistent object in a “local component site”
(such as a Plone site). Sometimes, we use local utilities as singletons
storing persistent objects, although there are better solutions (such as
`plone.app.registry`_ / `plone.registry`_) for that. More commonly, a
local utility is simply used to override a global utility with of same
interface (and optionally name).

In Plone, local components can be installed using the
*componentregistry.xml* GenericSetup import step. See the `GenericSetup
documentation`_ for more details. The techniques mentioned in this
manual pertain to global utilities only.

Global utilities can be registered in one of two ways using *five.grok*:

#. By writing a class deriving from *GlobalUtility*. The class will be
   used as a utility factory. It will be instantiated once (its
   constructor must be callable with no arguments), on startup, and
   registered according to the directives used on the class.
#. By calling the *global\_utility()* function on an
   already-instantiated object. This allows you to configure the
   instance in code before registering it.

To illustate both of these techniques, we will create two interfaces:

::

    from zope.interface import Interface
    from zope import schema

    class ILanguage(Interface):
        """A language.

        Each language is registered as a named utility providing this interface.
        The utility name should be a locale name, e.g. 'en_GB' or 'de'.
        """

        title = schema.TextLine(title=u"Name of the language (in English)")

    class ILanguagePreference(Interface):
        """Singleton used to look up a preferred language
        """

        preferredLanguage = schema.Object(title=u"User's preferred language", schema=ILanguage, readonly=True)

        def switch(newPreferredLanguage):
            """Switch preferred languages.
            
            Takes a local name as a parameter)
            """

Before we implement these utilities, let’s consider how we may use these
two interfaces from client code which does not care about their
implementation.

To look up the currently preferred language, we could do:

::

    >>> from zope.component import getUtility
    >>> preference = getUtility(ILanguagePreference)
    >>> preference.preferredLanguage
    <Language object at ...>
    >>> preference.switch('en_GB')

Languages are looked up as named utilities. Thus, we could get a
language like this:

::

    >>> from zope.component import queryUtility
    >>> en_GB = queryUtility(ILanguage, name=u"en_GB")

Notes:

-  *getUtility()* will return the default utility for the given
   interface if no name is passed (in fact, the default utility has a
   name of *u“”*, i.e. an empty string).
-  If no utility can be found, a *ComponentLookupError* will be raised.
-  We can use *queryUtility()* instead to fall back on another value
   (*None*, by default) instead of raising an error if the utility is
   not found.
-  Each time we call *getUtility()* with the same arguments, we get the
   same object back. This may lead to thread-safety issues in
   multi-threaded environments (such as Zope), so be careful if your
   utility can be modified after startup.

Let’s now show how these utilities could be registered. First, we will
create a class to encapsulate languages, instantiate a objects of this
class, and register each as a named utility providing the *ILanguage*
interface:

::

    from five import grok

    class Language(object):
        grok.implements(ILanguage)
        
        def __init__(title):
            self.title = title

    en_GB = Language(u"English (British)")
    en_US = Language(u"English (US)")
    de = Language(u"German")

    grok.global_utility(en_GB, provides=ILanguage, name="en_GB", direct=True)
    grok.global_utility(en_US, provides=ILanguage, name="en_US", direct=True)
    grok.global_utility(de, provides=ILanguage, name="en_de", direct=True)

Notes:

-  The *provides* argument can be omitted if (as is the case here) the
   object provides exactly one interface. Otherwise, it is required.
-  Name *name*parameter defaults to *u“”* and so can be omitted if you
   are registered an unnamed utility.
-  The *direct=True* argument indicates that the utility instance is
   being passed as the first argument. The argument should be *False* if
   a class or factory is being passed.

Next, we will define the preferred language utility. This time, we will
create a utility class and ask *five.grok* to register an instance of it
for us.

::

    from five import grok
    import os

    class EnvironmentLanguagePreference(grok.GlobalUtility):
        """Language preference taken from the PREFERRED_LANGUAGE environment variable
        """
        grok.provides(ILanguagePreference)

        @property
        def preferredLanguage(self):
            envKey = os.environ.get('PREFERRED_LANGUAGE', 'en_US')
            return getUtility(ILanguage, envKey)
     
        def switch(self, newPreferredLanguage):
            os.environ['PREFERRED_LANGUAGE'] = newPreferredLanguage

Notes:

-  The class is recognised as a factory for a global utility from its
   base class.
-  The class does not have a constructor. If it did, it would need to be
   callable with no arguments.
-  The utility’s interface is given with the *grok.provides()*
   directive. We could also have used *grok.implements()*, but bear in
   mind that the class can implement multiple interfaces whilst a
   utility can provide only one. *grok.provides()* can only be used once
   per class and can only be passed a single interface.
-  Here, we are registering an unnamed utility. We could have used the
   *grok.name()* directive to give the utility a name.

Provided the package is grokked, this is all it takes to register one
unnamed and three named global utilities with *five.grok*.

.. _plone.app.registry: http://pypi.python.org/pypi/plone.app.registry
.. _plone.registry: http://pypi.python.org/pypi/plone.registry
.. _GenericSetup documentation: http://developer.plone.org/components/genericsetup.html
