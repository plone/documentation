Interfaces and why they matter
==============================

Interfaces are a bit techie and something a non-developer would probably
rather not think about. However, they are an important part of component
wiring, so it is as well to know a bit about what they are and do.

Interfaces as Markers
---------------------

ZCML attributes often refer to interfaces rather than actual classes -
for instance the example below wires up the presentation viewlet for
content types that have the IATDocument interface.

::

    <browser:viewlet
          name="plone.presentation"
          for="Products.ATContentTypes.interface.IATDocument"
          manager="plone.app.layout.viewlets.interfaces.IAboveContentBody"
          class=".presentation.PresentationViewlet"
          permission="zope2.View"
          />

In effect this is saying that the presentation viewlet is available for
any content type which is ATDocument-like or behaves like an ATDocument.
So, in this case, the interface is a marker.

The convenience of this is that a content type can have one (or more)
interfaces, and several content types can share the same one. If you
develop a new content type and mark it with the IATDocument interface,
you can use this presentation viewlet with it - no extra wiring
required.

Components and Interfaces
-------------------------

Components themselves can be marked with an interface - the technical
term is "provides". Note that in the presentation viewlet example, the
viewlet manager is referred to by its interface, not its name:

::

     manager="plone.app.layout.viewlets.interfaces.IAboveContentBody"

To track down the actual component, look in the configure.zcml file in
the same directory as the interfaces. For instance, in
plone/app/layout/viewlets/configure.zcml you'll see the interface has
been wired up with a Python class to create a viewlet manager component:

::

          <browser:viewletManager
            name="plone.abovecontentbody"
            provides=".interfaces.IAboveContentBody"
            permission="zope2.View"
            class="plone.app.viewletmanager.manager.OrderedViewletManager"
            />

How to spot an interface
------------------------

It is usually fairly easy to spot a reference to an interface. By
convention, their names will be prefixed with an "I", and they will live
in an interface or interfaces namespace. If you investigate
interfaces.py or interface.py in any egg or product, you won't find very
much code, but you'll often find useful information – effectively it is
documentation about what a component providing (i.e. marked by) that
interface should do. For example:

::

    class IAboveContentBody(IViewletManager):
        """A viewlet manager that sits above the content body in view templates    """

If you've used the plone3\_theme paster template, you'll find you have a
ready-made interfaces.py file to which you can add your own interfaces
if you need to create them.
