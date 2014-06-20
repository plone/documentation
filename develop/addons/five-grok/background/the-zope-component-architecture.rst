The Zope Component Architecture
=================================

**A high level overview of the basic concepts of the Zope Component
Architecture**

The Zope Component Architecture underpins much of the advanced
functionality in Zope and Plone. By mastering a few core concepts, you
will be able to understand, extend and customise a wide range of Zope
technologies. These concepts include:

-  Using interfaces formalise a contract for and document a given
   component
-  Implementing the singleton pattern with unnamed utilities
-  Using named utilities to build a registry of homogenous objects
-  Using adapters to implement generic functionality that can work with
   heterogeneous objects
-  Customising behaviour with the concept of a more-specific adapter or
   multi-adapter
-  Event subscribers and event notification
-  Display components, including browser views, viewlets and resource
   directories

This tutorial will explain these concepts using simple examples, and
illustrate how to use convention-over-configuration with the *five.grok*
package to quickly and easily employ adapters, utilities, event
subscribers and browser components in your own code.

Conventions used in this manual
-------------------------------

The examples in this manual are sometimes shortened for readability, and
you may find that certain details of implementation are not shown to
keep the examples short and focused.

You will find two kinds of code listings here. A code block illustrating
code you may write in your own files is shown verbatim like this:

::

    from five import grok

    class SampleAdapter(grok.Adapter):
        grok.provides(ISomeInterface)
        grok.context(ISomeOtherInterface)

        ...

Note:

-  Code snippets may refer to code defined earlier on the same page. In
   this case, import statements for this code are not shown.
-  An ellipsis is sometimes used to abbreviate code listings.

Sometimes, we will also show how a component or function can be used in
client code. Here, “client code” means any code that is making use of
the features implemented with the components illustrated. These are
shown using Python interpreter (aka doctest) conventions, like this:

::

    >>> from five import grok
    >>> context = SomeObjects()
    >>> adapted = ISomeInterface(context)
    >>> adapted.someValue
    123

Lines starting with *>>>* indicate executable Python code, be that in a
test, in the interactive interpreter, or in the body of a function or
method somewhere. Return values and output are shown underneath without
the three-chevron prefix.
