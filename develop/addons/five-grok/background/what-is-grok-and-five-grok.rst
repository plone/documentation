What is Grok and five.grok? 
=============================

**Heritage and anthropology**

This manual is about using *five.grok* to configure components in the
Zope Component Architecture. But what is *five.grok*?

`Grok`_ is a web development framework built on top of Zope 3 (aka Zope
Toolkit, or ZTK). One of the main aims of the Grok project is to make it
easier to get started with Zope development by employing
“convention-over-configuration” techniques. Whereas in a “plain Zope” a
developer would typically write a component in Python code and then
register it in ZCML (an XML syntax, normally found in a file called
*configure.zcml)*, a Grok developer uses base classes and inline code
directives to achieve the same thing. The advantage is that the “wiring”
of a component is maintained right next to its code, making it easier to
understand what registrations are in effect, and reducing the need for
context-switching between different files and syntaxes.

It is important to realise that, for the purposes of this manual at
least, the Grok concepts are just an alternate way to configure the Zope
Component Archiecture. Everything that can be done with Grok
configuration can also be done with “plain Zope” and ZCML. The grok
syntax is merely a more convenient, compact and opinionated way to
achieve the same thing.

Opinionated? That’s right. In part, the design of the various Grok
directives and base classes aims to steer developers towards good
practice, well-organised code and shared standards. That’s not to say
you can’t go your own way if you really need to, but it is usually best
to follow the conventions and standards used by everybody else, unless
you have good reason to do otherwise.

Example
-------

Let’s take a look at an example. Here is a simple adapter registration
in vanilla Zope. First, the adapter factory, a Python class:

::

    from zope.interface import implements
    from zope.component import adapts

    from my.package.interfaces import IMyType
    from zope.size.interfaces import ISized

    class MyTypeSized(object):
        implements(ISized)
        adapts(IMyType)

        def __init__(self, context):
            self.context = context

        def sizeForSorting(self):
            return 'bytes', 0

        def sizeForDisplay(self):
            return u'nada'

Then, the registration in *configure.zcml*:

::

    <configure xmlns="http://namespaces.zope.org/zope" i18n_domain="my.package">

        <adapter
            for=".interfaces.IMyType"
            provides="zope.size.interfaces.ISized"
            factory=".size.MytypeSized"
            />

    </configure>

(note: in this case we could omit the *for* and *provides* lines, but
this is the full syntax)

With Grok convention-over-configuration, you can do it all in one file,
like this:

::

    from five import grok

    from my.package.interfaces import IMyType
    from zope.size.interfaces import ISized

    class MyTypeSized(grok.Adapter):
        grok.provides(ISized)
        grok.context(IMyType)

        def sizeForSorting(self):
            return 'bytes', 0

        def sizeForDisplay(self):
            return u'nada'

For this to work, the package needs to be “grokked”. This is done with a
single statement in *configure.zcml*, which then grokks all modules in
the package:

::

    <configure xmlns="http://namespaces.zope.org/zope" i18n_domain="my.package"
               xmlns:grok="http://namespaces.zope.org/grok">

        <include package="five.grok" />
        <grok:grok package="." />

    </configure>

The *<include />* statement ensures that the grok directive is
available. Once these two lines are in *configure.zcml*, we should not
need to add any more registrations to this file, no matter how many
grokked components we added to modules inside this package.

When the configuration is loaded (at “grok time”), various “grokkers”
will analyse the code in the package, typically looking for special base
classes (like *grok.Adapter* above), *directives*(like the
*grok.provides()* and *grok.implements()* lines above), module-level
function calls, directories and files (e.g. page templates), and
configure components based on these conventions.

Grok vs. five.grok vs. grokcore
-------------------------------

Grok started life as a monolithic framework, but the nice cavemen of the
Grok project decided to factor out the various grokkers into multiple
smaller packages. Thus, we have packages like `martian`_, the toolkit
used to write grokkers, `grokcore.component`_, which contains grokkers
for basic component architecture primitives such as adapters and
utilities, `grokcore.security`_, which provides for permissions and
security declarations, `grokcore.view`_, which provides support for
browser views, `grokcore.viewlet`_, which provides support for viewlets,
and so on.

`five.grok`_ is an integration package for Zope 2 which brings these
directives to Zope 2 applications such as Plone. In most Grok
documentation, you will see a line like this:

::

    import grok

This is using the standalone Grok framework. The *five.grok* equivalent
is:

::

    from five import grok

As far as possible, the *five.grok* project aims to make the conventions
and syntax used in standalone Grok work identically in Zope 2. If you
come across a piece of Grok documentation, chances are you can get it to
work in Zope 2 by switching the "*import grok*" line to "*from five
import grok*", although there are situations where this is not the case.
In particular, we tend to use Plone content types instead of
Grok ”models" and standard add/edit forms instead of the formlib-based
forms from Grok.

.. _martian: https://pypi.python.org/pypi/martian
.. _grokcore.component: https://pypi.python.org/pypi/grokcore.component
.. _grokcore.security: https://pypi.python.org/pypi/grokcore.security
.. _grokcore.view: https://pypi.python.org/pypi/grokcore.view
.. _grokcore.viewlet: https://pypi.python.org/pypi/grokcore.viewlet
.. _five.grok: https://pypi.python.org/pypi/five.grok
.. _Grok: http://grok.zope.org
