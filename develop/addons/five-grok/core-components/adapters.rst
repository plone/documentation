Adapters
===========

**Adapting from one interface to another with simple adapters and
multi-adapters**

Adapters are one of the most powerful concepts of the Zope Component
Architecture. They underpin a huge amount of the functionality - and
“pluggability” - of Zope and Plone. You will often see documentation (or
interfaces) that describe how a customisation can be applied by writing
an adapter.

As the name suggests, adapters implement the “adapter” software design
pattern. In the simplest terms, an adapter is a component that knows how
to use an object providing one interface to implement another interface.

The usual analogy is that of international power plugs: a European plug
has two prongs and a UK plug has three, but for the most part they do
the same job and use the same (or nearly the same) voltage. If you have
a UK appliance and you are in a country that has European sockets, you
can (re-)use your appliance (and avoid buying a new one) by employing an
adapter that makes the UK plug fit into the European socket. (If you’ve
ever lived in the UK, you’ll understand why “European” is not a superset
of “UK” in the preceding paragraph).

.. note::
    If you prefer duck metaphors, there is an awesome talk by Brandon Craig
    Rhodes about the concept of an adapter for your viewing pleasure
    `here <http://plone.org/events/conferences/2008-washington-dc/agenda/using-grok-to-walk-like-a-duck>`_.
    It even has sound effects.

In software terms, it is much the same. Let’s say that we were writing a
Twitter-to-email gateway (because Gmail has lots of storage space and
it’s important to know when some man in Kuala Lumpur got out of bed).
Suppose we have a function that can send an email, expecting an
*IMessage* object. Unfortunately, our input is a tweet, conforming to
the *ITweet* interface:

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

    class ITweet(Interface):
        """A microblogging message
        """

        from_ = schema.TextLine(title=u"Subject")
        message = schema.Text(title=u"The message")

What we need is a way to *adapt* our *ITweet* object to an *IMessage*.

The basic approach is to write a class that *implements* the attributes
and methods of *IMessage* by delegating to an *adapted* context object
that *provides* the *ITweet* interface. And a simple adapter would be
just that: a class that we instantiated directly, being passing a tweet
in its constructor, and then behaving like an *IMessage*.

Doing this, however, would tie us down to a specific implementation of
the adapter. The ZCA gives us a more powerful alternative by maintaining
a registry of adapters. We simply ask for an adapter *from* the object
we have, *to* the interface we want, and the ZCA searches the registry
for the most appropriate one. In code, it looks like this:

::

    def sendAsEmail(context):
        """Convert the object passed in to an email message and send it.
        """

        message = IMessage(context)
        sendEmail(message)

We could call this function with a tweet like this:

::

    >>> tweet = getLatestTweet() # implementaiton not shown - returns an object providing ITweet
    >>> sendAsEmail(tweet)

Here, we have assumed that the incoming object is an *ITweet*, but in
reality it could be anything that was *adaptable* to *IMessage.*
Suddenly, our *sendAsEmail()* function can be used for Identi.ca
messages and those really irritating Facebook status updates as well.
All we have to do is register an appropriate adapter from the source
type to *IMessage*, and we’re done.

.. note::
    As you may imagine, this technique is very useful in a content
    management scenario where you may have any number of different content
    types and you want to implement some common functionality that works
    across a number of objects.

The syntax we used here is to “call” the interface. This is the most
convenient way to look up a simple (unnamed, non-multi) adapter. If no
adapter can be found, the ZCA will raise a *TypeError*. That normally
indicates a programming error, so we don’t mind, but if you are unsure
whether the adapter has been registered, you can fall back to a default
value (e.g. *None*) like this:

::

    >>> message = IMessage(tweet, None)

Registering classes as adapter factories
----------------------------------------

Now that we have seen what adapters do and how to look them up, let’s
actually write and register one.

When we register adapters, we are actually registering an
**adapter****factory.** This is a callable that takes as an argument the
object being adapted, and returns an object providing the desired
interface. Each time an adapter is looked up, the ZCA calls the adapter
factory to obtain a new adapter instance. (Compare this to utilities,
which are instantiated once and shared.)

In most cases, adapter factories are classes implementing a given
interface and taking a single parameter in their constructor. (A Python
class object is a callable which takes the arguments of the class’
*\_\_init\_\_()* method and returns an instance of the class). The
*grok.Adapter* base class relies on this convention. It even defines the
constructor (although you can override it) and stores the adapted object
in the variable *self.context*, as is the convention.

An adapter factory for adapting *ITweet* s to *IMessage* s could thus look
like this:

::

    class TweetMessage(grok.Adapter):
        """Adapts an ITweet to an IMessage.

        This adapter is readonly. Thus we are strictly speaking only implementing
        a subset of the IMessage interface.
        """

        grok.provides(IMessage)
        grok.context(ITweet)

        @property
        def subject(self):
            return u"New tweet from %s!" % self.context.form_

        @property
        def recipients(self):
            return ('tweetgateway@example.org',)

        @property
        def body(self):
            return self.context.message

        def format(self):
            return "%s\n%s" % (self.subject, self.body,)

Assuming the package is being grokked, this is all it takes to register
an adapter with *five.grok*.

Notes:

-  The adapted object is available as *self.context* when using the
   default constructor.
-  If you are writing your own constructor, use a signature like *"**def
   \_\_init\_\_(self, context):*"** and store the *context* argument as
   *self.context*. This is not strictly necessary, but it is an almost
   universal convention. Since the constructor is called when the
   adapter is looked up, it is best to avoid any resource-intensive
   operations there. If an error is raised in the constructor, the
   adaptation will fail with a “could not adapt” *TypeError*.
-  The *grok.provides()* directive indicates the interface that will be
   provided by the adapter. If the adapter factory implements a single
   interface (via *grok.implements()* or inherited from a base class),
   this is optional.
-  The *grok.context()* directive indicates what is being adapted. This
   is usually an interface, but it can also be a class, in which case
   the adapter is specific to instances of that class (or a subclass).
   This directive can sometimes be omitted if there is an unambiguous
   module-level context. This is an instance providing the *IContext*
   interface from *grokcore.component.interfaces*, and will typically be
   something like a content object. If in doubt, it is always safest to
   provide an explicit context using the *grok.context()* directive.

Modelling aspects as adapters
-----------------------------

In the example above, we used an adapter to make an object providing one
interface conform to another. In this case, the objects were similar in
purpose, they just happened to have incompatible interfaces. However,
adapters are also frequently used in situations where we are trying to
model different aspects of an object as independent components, without
having to support every possible feature in a single class.

Consider our message interface again. Let’s say that we wanted to be
able to email any content object as a message. Is our content object a
message? Not at all, but we can provide an adapter to the *IMessage*
interface which models the “messaging” aspect of the content object.

Such an adapter may look something like this (*IDocument*and
implementation not shown, but assume it supports the properties
*title*and *text*):

::

    from five import grok

    class DocumentMessage(grok.Adapter):
        grok.provides(IMessage)
        grok.context(IDocument)

        @property
        def subject(self):
            return self.context.title

        @property
        def recipients(self):
            return ('intray@example.org',)

        @property
        def body(self):
            return self.context.text

        def format(self):
            return "%s\n%s" % (self.subject, self.body,)

This is relatively straightforward, and we could imagine having a number
of such adapters to represent any number of different content types as
messages.

Now consider the alternatives:

-  we could write a bespoke email-sending function for each type of
   content and use if-statements or lookup tables to find the correct
   one; or
-  we could demand that every content type that supported being sent as
   an email inherited from a mix-in class that provided the required
   properties.

The latter is the usual approach in the world of object oriented
programming, and is fine for small, closed systems. In an open-ended
system such as Plone, however, we don’t always have the option of mixing
new functionality into old code, and classes with “fat” interfaces can
become unwieldy and difficult to work with.

Customisation with more-specific adapters
-----------------------------------------

So far, we have limited ourselves to having only one adapter per type of
context. The ZCA allows us to have multiple possible adapters, leaving
it to pick the most appropriate one. Here, “most appropriate” really
means “most specific”, according to the following rules:

-  An adapter registered for a class is more specific than an adapter
   registered for an interface
-  An adapter registered for an interface directly provided by an
   instance is more specific than an adapter registered for an interface
   implemented by that object’s class
-  An adapter registered for an interface listed earlier in the
   *implements()* directive is more specific than an adapter registered
   for an interface listed later
-  An adapter registered for an interface implemented by a given class
   is more specific than an adapter registered for an interface
   implemented by a base class
-  An adapter registered for a given interface provided by an object is
   more specific than an adapter registered for a base-interface of that
   interface
-  In the case of a multi-adapter (see below), the specificity of the
   adapter to the first adapted object is more important than the
   specificity to subsequent adapted objects

These rules are known as “interface resolution order” and are basically
equivalent to the “method resolution order” used to determine which
method takes precedence in the case of multiple inheritance. Most of the
time, this works as you would expect, so you do not need to worry too
much about the detail of the rules.

The power of the “more-specific adapter” concept is that we can create a
generic adapter for a generic interface, and then provide an override
for a more specific interface. Let’s say that we had the following
hierarchy of interfaces, implemented by different types of content
objects (not shown):

::

    from zope.interface import Interface
    from zope import schema

    class IContent(Interface):
        """A content object
        """

        title = schema.TextLine(title=u"Title")

    class IDocument(IContent):
        """A document content item
        """

        text = schema.TextLine(title=u"Body text")

    class IFile(IContent):
        """A file content item
        """

        contents = schema.Bytes(title=u"Raw data")

We could now register a generic adapter from *IContent* to *IMessage*,
which would be usable for any content item providing this interface,
including file content, or some future type of content we haven’t even
thought of yet. Then, we could register a *more specific* adapter for
IDocument, like the one we saw above, to provide more specific behaviour
for the document type.

But why stop there? Perhaps we want to be able to mark certain documents
as important and have the message subject change? One way to do that is
with a marker interface on the instance:

::

    class IImportantDocument(Interface):
        """Marker interface for important documents
        """

We would apply this selectively to instances using *alsoProvides()*
(perhaps in an event handler):

::

    >>> from zope.interface import alsoProvides
    >>> alsoProvides(urgentDocument, IImportantDocument)

We could then register an adapter for this. We can even re-use our
previous adapter factory by subclassing it and overriding only the
properties or methods we care about:

::

    class ImportantDocumentMessage(DocumentMessage):
        grok.provides(IMessage)
        grok.context(IImpotrantDocument)

        @property
        def subject(self):
            return u"URGENT! " + self.context.title

Note: This factory class is grokked as an adapter because it derives
from *DocumentMessage* which in turn derives from *grok.Adapter*.

.. note::
    If you have a class that derives from one of the special Grok base
    classes (like *grok.Adapter* or *grok.GlobalUtility*), but you do not
    want it to be grokked, e.g. because it is used only as a base class for
    other classes, you can use the *grok.baseclass()* directive with no
    arguments to disable grokking.

Using a function as an adapter factory
--------------------------------------

Remember we said that an adapter factory is a “callable” that returns an
object providing the appropriate interface? Classes are one type of
callable, but the most common callable, of course, is a function. It can
be useful to register a function as an adapter factory in situations
when you are not actually (or always) instantiating a class to provide
the adapter.

As an example, let’s say that we wanted to keep a cache of the adapter
instances, perhaps because they are resource intensive. In this case, we
may either create a new adapter object, or re-use an existing one (in
general, we wouldn’t do this of course, due to thread safety and state
management issues, but it’s a useful example). We can’t do that in the
*\_\_init\_\_()* method of a class, because that is not called until
after the class has been instantiated. Instead, we could use a function
as the adapter factory:

::

    from five import grok

    @grok.implementer(IMessage)
    @grok.adapter(ITweet)
    def messageFromTweetAdapter(context):
        cached = messageCache.get(context) # dict-like interface; not shown
        if cached is not None:
            return cached
        else: # create a new object
            return TweetMessage(context)

Notes:

-  The *@implementer* decorator specifies the interface(s) which will be
   provided by the returned objects. In the case of an adapter factory,
   you should pass a single interface, although the decorator can take
   multiple arguments.
-  The *@adapter* decorator actually registers the adapter. For a single
   adapter, pass a single interface. For a multi-adapter (see below),
   you can pass multiple arguments. For a named adapter (see below) you
   can pass a *name=u“name”* keyword argument.

Using an instance as an adapter factory
---------------------------------------

In addition to classes and functions, an instance of a class that has a
*\_\_call\_\_()* method may be used as an adapter factory callable. To
register such an object as an adapter factory, we can’t use the
*grok.Adapter* base class (since that would register the *class* as the
adapter factory and we want to register the *object)* or the *@adapter*
decorator. Instead, we use the *global\_adapter()* function.

This is much less common, but can be useful in certain circumstances.
Here is an example from the `z3c.form`_ library:

::

    from five import grok

    from zope.interface import Interface
    from zope import schema
    import z3c.form.widget import StaticWidgetAttribute

    class ISchema(Interface):
        """This schema will be used to power a z3c.form form"""

        field = schema.TextLine(title=u"Sample field")

    labelOverride = StaticWidgetAttribute(u"Override label", field=ISchema['field'])
    grok.global_adapter(labelOverride, name=u"label")

The *StaticWidgetAttribute()* function returns a callable object that is
intended to be registered as an adapter factory. The *global\_adapter()*
function takes care of this for us at “grok time”. In this case, we have
passed the instance and a name (see named adapters, below) because the
object provides a single interface and has an “adapts” declaration. If
this was not the case, we could use the full syntax:

::

    grok.global_adapter(adapterFactoryInstance, (IAdapted,), IProvided, name=u"name")

Note: The adapted interfaces are passed as a tuple to support
multi-adapters (see below).

Named adapters
--------------

As we have seen above, adapters - like utilities - can be registered
with a name:

-  By using the *grok.name()* directive in the class body of an adapter
   factory deriving from *grok.Adapter*.
-  By using the *name*keyword argument to the *@adapter* function
   decorator
-  By using the *name*argument to the *global\_adapter()* function

Named adapters are a lot less common than named utilities, but can be
useful in a few circumstances:

-  You want the user to choose among a number of different
   implementations at runtime. In this case, you could translate the
   user’s input (or some other external runtime state) to the name of an
   adapter.
-  You want to allow third-party packages to plug in any number of
   adapters, which you will iterate over and use as appropriate, but you
   also want to allow an individual named adapter to be overridden for a
   more specific interface (see also subscription adapters below).
-  Most browser components (views, viewlets, resource directories) are
   in fact implemented as named (multi-)adapters. For a view, the name
   is the path segment that appears in the URL.

If you want to get a simple (non-multi) adapter by name, use the
*getAdapter()* function:

::

    >>> from zope.component import getAdapter
    >>> adapted = getAdapter(context, IMessage, name=u"adapter-name")

This will raise a *ComponentLookupError* if no adapter can be found.
There is also a *queryAdapter()* function which returns *None* as a
fallback instead.

If you want to iterate over all the named adapters that provide a given
interface, you can do:

::

    >>> from zope.component import getAdapters
    >>> for name, adapter in getAdapters((context,), IMessage):
    ...     print "Name gave us", adapter.format()

Note that this function takes a tuple of objects as the context, because
it is also used for multi-adapters.

Multi-adapters
--------------

So far, our adapters have all adapted a single context. A multi-adapter
is an adapter that adapts more than one thing. There are a few reasons
to want to do this:

-  If you have written an adapter and you find that you need to pass an
   object to (almost) every one of its methods, you could use a
   multi-adapter to allow the adapter to be initialised with more than
   one object.
-  The rules of “more specific” adapters applies to each adapted context
   of multi-adapters. Thus, if you want to allow a component to be
   swapped out (customised) along multiple dimensions, you could look it
   up as a multi-adapter.

Multi-adapters are frequently used in browser components (such as views
and viewlets), which adapt a context object and the request. This allows
multiple views to be registered with the same name, with different
implementations based on the type of context (i.e. the "*index*" view
for an *IDocument* is different to the view of an *IFile*) or the type
of request (i.e. an HTTP request results in a different response to an
XML-RPC request). Furthermore, the request may be marked with marker
interfaces (known as “browser layers”) upon traversal, allowing you to
register a different view depending on which layer is in effect.

Browser components are registered using specific grokkers which also
take care of things like security and template binding. We will cover
those later. For a simple example, however, consider the following:

::

    from zope.interface import Interface
    from zope import schema

    class IBloggingService(Interface):
        """A blogging service
        """

        title = schema.TextLine(title=u"Name of service")
        url = schema.URI(title=u"API URL")

    class IMicroBloggingService(IBloggingService):
        """A micro-blogging service
        """

        maxMessageLength = schema.Int(title=u"Max message length allowed")

    class IMessageBroadcaster(Interface):
        """Multi-adapt a context and a blogging service to this interface
        """

        def send():
            """Send the context as a message using the given service
            """

We could imagine looking up a multi-adapter like this:

::

    >>> from zope.component import getMultiAdapter()
    >>> context = Document() # an object providing IDocument
    >>> service = TwitterService() # an object providing IMicroBloggingService
    >>> broadcaster = getMultiAdapter((context, service,), IMessageBroadcaster)

This will raise a *ComponentLookupError* if no suitable adapter can be
found. There is also *queryMultiAdapter()*, which will return *None* as
a fallback.

Like other adapters, a multi-adapter is registered with a callable that
acts as the adapter factory. The callable must take one argument for
each adapted object (two, in this case). We can register multi-adapters
with the *@adapter* function decorator or the *grok.global\_adapter()*
function, as indicated above. More commonly, however, we will use the
*grok.MultiAdapter* base class, like this:

::

    class BloggingBroadcaster(grok.MultiAdapter):
        grok.provides(IMessageBroadcaster)
        grok.adapts(IContent, IBloggingService)

        def __init__(self, context, service):
            self.context = context
            self.service = service

        def send(self):
            message = IMessage(self.context)
            text = message.format()
            print text

    class MicroBloggingBroadcaster(grok.MultiAdapter):
        grok.provides(IMessageBroadcaster)
        grok.adapts(IContent, IMicroBloggingService)

        def __init__(self, context, service):
            self.context = context
            self.service = service

        def send(self):
            message = IMessage(self.context)
            text = message.format()
            print text[:self.service.maxMessageLength]

Here, we have registered two multi-adapters, the second more specific
than the first. Notice how we have to define a constructor: the base
class can’t do it for us, since it doesn’t know how many things we will
adapt or what we may want to call the variables where they are stored.

Subscription adapters
---------------------

There is one final type of adapter known as a *subscription adapter*.
These can be used when you always want to look up and iterate over *all*
available adapters to a specific interface, as opposed to finding the
most specific one. However, it is not possible to override or disable a
subscription adapter without removing its registration directly, so most
people prefer to use named adapters instead, which allow an adapter with
a given name to be overridden for a more specific interface. Like event
handlers (which are in fact implemented using subscription adapters),
subscription adapters are registered with the *<subscriber />* ZCML
directive. There is currently no way to register one using Grok
conventions.

.. _z3c.form: https://pypi.python.org/pypi/z3c.form
