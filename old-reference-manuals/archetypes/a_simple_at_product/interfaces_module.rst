======================
The interfaces module
======================

.. admonition:: Description

		The module where you define interfaces describing what 
		your content class(es) will do. 

Why do you need interfaces?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Interfaces are useful to describe what a class will do. They are a kind
of contract between a class and the components that class interact with.
Starting a content management functionality package with writing
interfaces is recommended practice as it helps document your code. In
addition to that, Zope Component Architecture (ZCA) allows us to use
interfaces as components for adapting a class (which is useful as new
user requirements appear) and thus specializing its behaviour.

The interface for the Instant Message class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is done by convention in the ``interfaces.py`` file, that you need
to add at the root of the package.

First, we need an import from Zope’s ``zope.interface`` module, which is
included into Zope 2’s distribution since version 2.8:

::

        from zope.interface import Interface

Following ZCA naming conventions (interface names start with an *I*), we
define the ``IInstantMessage`` interface we need for the
``InstantMessage`` class that we will define later:

::

        class IInstantMessage(Interface):
            """
            Interface for the InstantMessage class.
            """

That’s it!

We could add attribute definitions to it using the
``zope.interface.Attribute`` class, but this is not mandatory. When an
interface is defined as above, without any function nor attribute, we
call it a “marker interface” meaning that it will be used simply to
“mark” the instances of the class that implements it.

More information about interfaces in the context of Archetypes can be
found in the `b-org tutorial - Interfaces section`_. For a detailed
presentation of interfaces and their usage patterns, read the `doctests
document available from Zope’s documentation site`_.

.. _b-org tutorial - Interfaces section: ../../../tutorial/borg/interfaces
.. _doctests document available from Zope’s documentation site: http://docs.zope.org/zope3/Code/zope/interface/README.txt
