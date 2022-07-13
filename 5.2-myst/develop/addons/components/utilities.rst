=========
Utilities
=========

.. admonition:: Description

    Utility design pattern in Zope 3 allows overridable singleton class instances for your code.


Introduction
============

* Utility classes provide site-wide utility functions.

* They are registered by marker interfaces.

* Site customization logic or add-on products can override utilities for
  enhanced or modified functionality

* Utilities can be looked up by name or interface

* Compared to "plain Python functions", utilities provide the advantage of
  being plug-in points without need of
  :doc:`monkey-patching </develop/plone/misc/monkeypatch>`.

Read more in

* `zope.component documentation <http://docs.zope.org/zope.component/>`_.

Local and global utilities
--------------------------

Utilities can be

* *global* - registered during Zope start-up

* *local* - registered during add-on installer for a certain site/content item

Local utilities are registered to persistent objects.
The context of local utilities is stored in a thread-local variable which is set
during traversal. Thus, when you ask for local utilities, they usually
come from a persistent registry set up in the Plone site root object.

Global utilities are registered in ZCML and affect all Zope application
server and Plone site instances.

Some hints::

    <Moo^_^> what's difference between gsm.queryUtility() (global site manager) and zope.component.queryUtility()
    <agroszer> Moo^_^, I think gsm... takes the global registrations, z.c.queryUtility respects the current context

Registering a global utility
=============================

A utility is constructed when Plone is started and ZCML is read.
Utilities take no constructor parameters. If you need to use parameters
like context or request, consider using views or adapters instead.
Utilities may or may not have a name.

* A utility can be provided by a function: the function is called and it
  returns the utility object.

* A utility can be provided by a class: the class ``__call__()`` method
  itself acts as an factory and returns a new class instance.

ZCML example:

.. code-block:: xml

    <!-- Register header animation picking logic - override this for your custom logic -->
    <utility
        provides="gomobile.convergence.interfaces.IConvergenceMediaFilter"
        factory=".filter.ConvergedMediaFilter"
        />


Python example (named utility)::

    def registerOnsitePaymentProcessor(processor_class):
        """ """

        # Make OnsitePaymentProcessor class available as utiltiy
        processor = processor_class()
        gsm = component.getGlobalSiteManager()
        gsm.registerUtility(processor, interfaces.IOnsitePaymentProcessor, processor.name)

The utility class "factory" is in its simplest form a class which implements
the interface::

    class ConvergedMediaFilter(object):
        """ Helper class to deal with media state of content objects.
        """

        zope.interface.implements(IConvergenceMediaFilter)

        def foobar(x):
            """ An example method """
            return x+2

Class is constructed / factory is run during the ZCML initialization.

To use this class::

    from gomobile.convergence.interfaces import IConvergenceMediaFilter

    def something():
       filter = getUtility(IConvergenceMediaFilter)
       x = filter.foobar(3)

Registering a local utility
=============================

* https://plone.org/documentation/manual/developer-manual/generic-setup/reference/component-registry

* http://davisagli.com/blog/registering-add-on-specific-components-using-z3c.baseregistry

* https://pypi.python.org/pypi/z3c.baseregistry

.. warning::

    Local utilities may be destroyed when the add-on product that
    provides them is reinstalled.
    Do not use them to store any data.

* http://markmail.org/thread/twuhyldgyje7p723

Overriding utility
==================

If you want to override any existing utility you can re-register the utility
in the ``overrides.zcml`` file in your product.

Getting a utility
==================

There are two functions:

``zope.component.getUtility``
    will raise an exception if the utility is not found.

``zope.component.queryUtility``
    will return ``None`` if the utility is not found.

Utility query parameters are passed to the utility class constructor.

Example::

    from zope.component import getUtility, queryUtility

    # context and request are passed to the utility class constructor
    # they are optional and depend on the utility itself
    picker = getUtility(IHeaderAnimationPicker, context, request)

.. note::

    You cannot use ``getUtility()`` on Python module level code
    during import, as the Zope Component Architecture is not yet initialized
    at that time.
    Always call ``getUtility()`` from an HTTP request end point or after
    Zope has been started.

Query local + global utilities:

``zope.component.queryUtility()`` for local utilities, with global fallback.

Query only global utilities::

    from zope.app import zapi
    gsm = zapi.getGlobalSiteManager()
    return gsm.getUtility(IConvergenceMediaFilter)

.. warning::

    Due to Zope component architecture initialization order, you cannot call
    ``getUtility()`` in module-level Python code.
    Module-level Python code is run when the module is being
    imported, and Zope components are not yet set up at this point.

Getting all named utilities of one interface
============================================

Use ``zope.component.getUtilitiesFor()``.

Example::

    def OnsitePaymentProcessors(context):
        """ List all registered on-site payment processors.

        Mostly useful for validating form input.

        Vocabulary contains all payment processors, not just active ones.

        @return: zope.vocabulary.SimpleVocabulary
        """

        utilities = component.getUtilitiesFor(interfaces.IOnsitePaymentProcessor)
        for name, instance in utilities:
            pass

Unregistering utilities
========================

* http://www.muthukadan.net/docs/zca.html#unregisterutility

Removing persistent local utilities
===================================

* :doc:`/manage/troubleshooting/manual-remove-utility`
* http://blog.fourdigits.nl/removing-a-persistent-local-utility
* http://blog.fourdigits.nl/removing-a-persistent-local-utility-part-ii

