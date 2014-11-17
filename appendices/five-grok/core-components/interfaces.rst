Interfaces
=============

**Describing functionality with interfaces**

There is nothing Grok-specific about interfaces, but they are important
because they used in various directives for describing or registering
components.

Zope interfaces are implemented in the *zope.interface* package. In addition, *zope.schema* contains various classes that can be used to describe the type of attributes on an interface (the :doc:`Dexterity developer manual </external/plone.app.dexterity/docs/index>` contains a reference).

Interfaces are typically found in an *interfaces.py* module, although
you will sometimes see schema interfaces kept in the same module as
other code (e.g. content classes, event handlers) related to the content
type described by that schema.

The simplest interface is a **marker** interface. This is used as a flag
which can either be applied or not to a particular object. A marker
interface may look like this:

.. code-block:: python

    from zope.interface import Interface

    class IImportant(Interface):
        ""Marker interface used for important objects
        ""

Notice how we have a docstring on the interface. Interfaces are useful
as documentation, and you should endeavour to describe their purpose and
behaviour in docstrings on the interface and on any attributes or
methods (see below).

Also note that although an interface is created using the
*class*keyword, they are in fact instances of type *InterfaceClass*. For
the most part, you don’t need to worry about this.

Interfaces are said to be **implemented** by classes, in which case
instances of that class is said to **provide** the interface.

::

    from five import grok

    class ImportantStuff(object):
        grok.implements(IImportant)

        ...

Note: The *grok.implements()* directive is just a convenience alias for
the *implements()* directive from *zope.interface*.

Adherence to a given interface can be tested like this:

::

    >>> IImportant.implementedBy(ImportantStuff)
    True
    >>> stuff = ImportantStuff()
    >>> IIimportant.providedBy(stuff)
    True

Again, note that we perform an “implements” check against the class and
a “provides” check against an instance.

It is also possible to apply an interface directly to an instance. This
is mostly relevant to marker interfaces, since other interfaces promise
attributes and methods that you usually cannot guarantee that the object
will provide.

::

    >>> from zope.interface import alsoProvides
    >>> alsoProvides(someObject, IImportant)

Let’s now take a look at a non-marker interface. This one promises
several attributes and methods. Typing and constraints for attributes
are described by *zope.schema* fields.

::

    from zope.interface import Interface
    from zope import schema

    class IMessage(Interface):
        """An email-like message
        """

        subject = schema.TextLine(title=u"Subject")
        recipients = schema.Tuple(title=u"Recipients",
                                  description=u"A list of email addresses",
                                  value_type=schema.TextLine())
        body = schema.Text(title=u"Body", required=False)

        def format():
            """Return a formatted string representing the message
            """

Again notice the use of docstrings for methods and titles and
descriptions for fields. Also notice how the method does not take the
*self* parameter. If the implementation is a class (as it is likely to
be), its methods will of course take the *self* parameter, but as far as
the user of the interface is concerned, this is an implementation
detail, and so does not belong in the interface.

Here is a class implementing this interface:

::

    class Message(object):
        implements(IMessage)

        subject = u""
        recipients = ()
        body = u""

        def format(self):
            return "Subject: %s\nTo: %s\n%s" % (self.subject, ', '.join(self.recipients), self.body,)

Like classes, interfaces may inherit one another. The derived interface
inherits all the attributes and methods of the parent interface. Objects
providing the derived interface must provide all attributes and methods
of both interfaces.

::

    class ITestContent(Interface):
        """Base interface for content types
        """

        title = schema.TextLine(title=u"Title")

    class IDocumentContent(ITestContent):
        """Document content
        """

        text = schema.Text(title=u"Body")

    class IFileContent(ITestContent):
        """File content
        """

        data = schema.Bytes(title=u"Octet stream")

A class may implement more than one interface. In addition, a class
automatically implements all interfaces from its base classes (unless
you use the *implementsOnly()* directive from *zope.interface*).

::

    class ImportantMessageDocument(Message):
        grok.implements(IDocumentContent, IImportant)

        title = u"Title"

        def _getText(self):
            return self.body
        def _setText(self, value):
            self.body = value
        text = property(_getText, _setText)

Here, we have implemented *text* as a property delegating to the *body*
field from the *IMessage* interface. We inherited the implementation of
*body* from the *Message*base class, from which we have also indicated
the *implements()* specification for the *IMessage* interface:

::

    >>> doc = ImportantMessageDocument()
    >>> IImportant.providedBy(doc)
    True
    >>> IMessage.providedBy(doc)
    True
    >>> ITestContent.providedBy(doc)
    True
    >>> IDocumentContent.providedBy(doc)
    True
    >>> IFileContent.providedBy(doc)
    False

There are a few other things you can do with interfaces, such as
specifying interfaces provided by modules (used to specify an API for
that module) or classes (e.g. in the case of class objects acting as
factories), looping through the interfaces provided by an instance, or
adding or removing marker interfaces. None of these is terribly common.
See the documentation for `zope.interface`_ (including its interfaces)
for details.

.. _zope.interface: https://pypi.python.org/pypi/zope.interface



