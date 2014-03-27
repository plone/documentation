=================================
Other Useful Archetypes Features 
=================================

.. admonition:: Description

		Complementary features you'd be pleased to know about. 

How to use events to hook the Archetypes creation process
----------------------------------------------------------

.. admonition:: Description

	Times have changed since the days of at_post_create_script(). Here is the
	way to hook into Zope3 (or Five's) event system in order to execute code
	during the Archetypes content creation and or editing process. 

In the old days the only way to execute code during the object creation
process for Archetypes was to add a method to your content type called
*at\_post\_create\_script*. In this script you would add any code that
should execute after Archetypes was done creating the object.

The new method for hooking the Archetypes object creation and editing
process is to use Zope3 style events,
like \ *Products.Archetypes.interfaces.IObjectInitializedEvent*.

Prerequisites
-------------

Have a content type handy so we can add a post creation hook to it. To
learn how to create a content type, check previous sections of this
manual.

We’re going to use a content type called *ExampleContent* with the
interface *IExampleContent* for this how to. The code structure will
look like this:

::

    tutorial/configure.zcml
    tutorial/interfaces.py
    tutorial/content/examplecontent.py

Step by step
------------

First let’s create the interface for our *ExampleContent* type. In
*interfaces.py*, add:

::

    from zope.interfaces import Interface

    class IExampleContent(Interface):
        ''' Interface for the ExampleContent type
        '''

You can store the implementation for your event handlers anywhere but
for the purpose of this example we’re going to put it in the same module
as the *ExampleContent* type:

::

    from zope.interface import implements
    from Products.ATContentTypes import atct

    def addSubFolder(obj, event):
        obj.invokeFactory(type_name='Folder', id='subfolder')

    class ExampleContent(atct.ATFolder):
        implements(IExampleContent)
        portal_type = archetype_name = 'ExampleContent'  # <-- this is no longer needed with GenericSetup.

All we need to do now is register the *addSubFolder* method as a handler
for \ *Products.Archetypes.interfaces.IObjectInitializedEvent* and for
anything implementing the *IExampleContent* interface. We do this in a
*configure.zcml* file:

::

    <subscriber for=".interfaces.IExampleContent
                     Products.Archetypes.interfaces.IObjectInitializedEvent"
                handler=".content.examplecontent.addSubFolder" />

Notice that there are two interfaces in the “for” attribute. This is
because we are registering a multi-adapter. Now when you add an
*ExampleContent* type the *addSubFolder* method will be executed after
Archetypes has created the object. The object itself will be passed to
the handler and we can use the object reference to make additional
modifications, in this case adding a sub folder.
You can register as many handlers as you need.

Warnings from your future
-------------------------

Having implemented all of your content type’s event hooks you might then
run off and try using *invokeFactory* somewhere in your code only to
realize that your \ *IObjectInitializedEvent* handlers are not being
executed. This is because *invokeFactory* does not notify Zope’s event
system that new objects are being created. You have to provide these
notifications yourself. So here is an example:

::

    import zope.event
    from Products.Archetypes.event import ObjectInitializedEvent
    some_folder.invokeFactory(type_name='ExampleContent', id='foobar')
    obj = getattr(some_folder, 'foobar')
    zope.event.notify(ObjectInitializedEvent(obj))

This will both create your object and invoke
any \ *IObjectInitializedEvent* handlers you have registered. Notice
that we are importing *ObjectInitializedEvent*, not the interface
*IObjectInitializedEvent*. We want to actually instantiate an event
passing it our newly created object as the single parameter and then
pass the event to *zope.event.notify*. From there, Zope takes care of
figuring out which handlers need to execute.

So for example, in our *addSubFolder* method above, any events
registered for the folder we created would not fire. To complete our
hook in this case we should provide a notification for our newly created
folder. Archetypes or other products may be expecting notifications so
when using invokeFactory, always send an *IObjectInitializedEvent*\ for
the object\ *.*\ The complete method looks like this:

::

    def addSubFolder(obj, event):
        obj.invokeFactory(type_name='Folder', id='subfolder')
        folder = getattr(obj, 'subfolder')
        zope.event.notify(ObjectInitializedEvent(folder))

Further information
-------------------

.. raw:: html

   <div>

The \ *IObjectInitializedEvent* is fired once during the objects
creation process. To hook the editing process for an object
use \ *IObjectEditedEvent*.

The \ `Sending and handling events`_ tutorial is a little out of date
but provides a broader explanation of the underlying mechanics. `Walking
through Five to Zope 3 - Events`_ is another great introduction to
events handling. 

.. raw:: html

   </div>

 

.. _Sending and handling events: ../../../tutorial/borg/sending-and-handling-events/
.. _Walking through Five to Zope 3 - Events: ../../../tutorial/five-zope3-walkthrough/events
