============
Vocabularies
============

**Static and dynamic lists of valid values**

The term “vocabulary” here refers to a list of values that are allowable
by a given field. In most cases, that implies a field using a selection
widget, like a multi-select list box or a drop-down.

Selection fields use the *Choice* field type. To allow the user to
select a single value, use a *Choice* field directly:

::

    class ISimplePizza(model.Schema):
        topping = schema.Choice(
                title=_(u"Choose your topping"),
                values=[_(u'Chicken'), _(u'Pepperoni'), _(u'Tomato')]
            )

For a multi-select field, use a *List*, *Tuple, Set* or *Frozenset* with
a *Choice* as the *value\_type*:

::

    class IPizzaOrder(model.Schema):

        ...

        orderItems = schema.Set(
                title=_(u"Your order"),
                value_type=schema.Choice(values=[_(u'Margherita'), _(u'Pepperoni'), _(u'Hawaiian')])
            )

The *Choice* field must be passed one of the following arguments,
specifying its vocabulary:

-  *values* can be used to give a list of static values
-  *source* can be used to refer to an *IContextSourceBinder* or
   *ISource* instance
-  *vocabulary* can be used to refer to an *IVocabulary* instance or
   (more commonly) a string giving the name of an
   *IVocabularyFactory* named utility.

We’ll now explore various ways in which we can improve on the
*orderItems* list.

Static vocabularies
-------------------

Up until now, we have been using a static vocabulary, passing the list
of allowable values as the *values* parameters to the *Choice* field.
This is simple, but has a few draw-backs:

-  If the vocabulary changes, we have to change the interface code.
-  There is no way to separate the label that the user sees in the
   selection widget from the value that is extracted.

Dynamic vocabularies
--------------------

To implement a more dynamic vocabulary, we can use a source. Before we
do that, though, let’s consider where our data will come from.

We want to make the “order items” list more dynamic, and allow the list
of available pizza types to be managed through the web. There are
various ways to do this, including modelling pizzas as content items and
creating a source that performs a catalog query to find them all. To
manage a simple list, however, we can use *plone.app.registry* and
install the list with our product’s extension profile. An administrator
could then use the registry control panel to change the list. We won’t
go into *plone.app.registry* in detail here, but you can read its
`documentation`_ to get a full understanding of what it is and how it
works.

First, we need to add *plone.app.registry* as a dependency in
*setup.py*:

::

          install_requires=[
              'setuptools',
              'plone.app.z3cform',
              'plone.directives.form',
              'plone.app.registry',
          ],

We also want to configure it when our product is installed in Plone, so
we edit *profiles/default/metadata.xml* as follows:

::

    <metadata>
        <version>1</version>
        <dependencies>
            <dependency>profile-plone.app.z3cform:default</dependency>
            <dependency>profile-plone.app.registry:default</dependency>
        </dependencies>
    </metadata>

Next, we create a registry.xml containing the following:

::

    <registry>

        <record name="example.dexterityforms.pizzaTypes">
            <field type="plone.registry.field.Tuple">
                <title>Pizza types</title>
                <value_type type="plone.registry.field.TextLine" />
            </field>
            <value>
                <element>Margherita</element>
                <element>Pepperoni</element>
                <element>Hawaiian</element>
            </value>
        </record>

    </registry>

After re-running buildout and (re-)installing our product in the

Terminology
~~~~~~~~~~~

When working with dynamic vocabularies, we come across some terminology
that is worth explaining:

-  A *term* is an entry in the vocabulary. The term has a value. Most
   terms are *tokenised* terms which also have a token, and some terms
   are *titled*, meaning they have a title that is different to the
   token.
-  The *token* must be an ASCII string. It is the value passed with the
   request when the form is submitted. A token must uniquely identify a
   term.
-  The *value* is the actual value stored on the object. This is not
   passed to the browser or used in the form. The value is often a
   unicode string, but can be any type of object.
-  The *title* is a unicode string or translatable message. It is used
   in the form and displayed to the user.

One-off sources with a context source binder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can make a one-off dynamic vocabulary using a context source binder.
This is simply a callable (usually a function or an object with a
*\_\_call\_\_* method) that provides the *IContextSourceBinder*
interface and takes a *context* parameter. The *context* argument is the
context of the form view. The callable should return a vocabulary, which
is achieved by using the *SimpleVocabulary* class from
*zope.schema*.

Here is an example that returns our pizza types:

::

    from plone.supermodel import model
    from plone.directives import form

    from zope.component import queryUtility
    from zope.component import provider

    from zope import schema

    from zope.schema.interfaces import IContextSourceBinder
    from zope.schema.vocabulary import SimpleVocabulary

    from plone.registry.interfaces import IRegistry

    ...

    @provider(IContextSourceBinder)
    def availablePizzas(context):
        registry = queryUtility(IRegistry)

        terms = []

        if registry is not None:
            for pizza in registry.get('example.dexterityforms.pizzaTypes', ()):
                # create a term - the arguments are the value, the token, and
                # the title (optional)
                terms.append(SimpleVocabulary.createTerm(pizza, pizza.encode('utf-8'), pizza))

        return SimpleVocabulary(terms)

Here, we have defined a function acting as the *IContextSourceBinder*, as
specified via the *@provider()* decorator. This looks up the
registry and looks for the record we created with *registry.xml* above
(remember to re-install the product in the Add-on control panel or the
*portal\_quickinstaller* tool if you modify this file). We then use the
*SimpleVocabulary* helper class to create the actual vocabulary.

The *SimpleVocabulary* class additionally contains two class methods
that can be used to create vocabularies from lists:

-  *fromValues()* takes a simple list of values and returns a tokenised
   vocabulary where the values are the items in the list, and the tokens
   are created by calling *str()* on the values.
-  *fromItems()* takes a list of *(token, value)* tuples and creates a
   tokenised vocabulary with the token and value specified.

We can also instantiate a *SimpleVocabulary* directly and pass a list of
terms in the initialiser as we have done above. The *createTerm()* class
method can be used to create a term from a *value*, *token* and *title*.
Only the value is required.

To use this context source binder, we use the *source* argument to the
*Choice* constructor:

::

    class IPizzaOrder(model.Schema):

        ...

        orderItems = schema.Set(
                title=_(u"Your order"),
                value_type=schema.Choice(source=availablePizzas)
            )

Parameterised sources
---------------------

Sometimes, it is useful to parameterise the source. For example, we
could generalise the pizza source to work with any registry value
containing a sequence, by passing the registry key as an argument. This
would allow us to create many similar vocabularies and call upon them in
code.

This degree of generalisation is probably overkill for our use case, but
to illustrate the point, we’ll outline the solution below.

First, we turn our *IContextSourceBinder* into a class that is
initialised with the registry key

::

    from zope.interface import implementer

    @implementer
    class RegistrySource(object):

        def __init__(self, key):
            self.key = key

        def __call__(self, context):
            registry = queryUtility(IRegistry)
            terms = []

            if registry is not None:
                for value in registry.get(self.key, ()):
                    terms.append(SimpleVocabulary.createTerm(value, value.encode('utf-8'), value))

            return SimpleVocabulary(terms)

Notice how in our first implementation, the function *provided* the
*IContextSourceBinder* interface, but the class here *implements* it.
This is because the function was the context source binder callable
itself. Conversely, the class is a factory that creates
*IContextSourceBinder* objects, which in turn are callable.

Again, the source is set using the *source* argument to the *Choice*
constructor.

::

        orderItems = schema.Set(
                title=_(u"Your order"),
                value_type=schema.Choice(source=RegistrySource('example.dexterityforms.pizzaTypes'))
            )

When the schema is initialised on startup, the a *RegistrySource* object
is instantiated, storing the desired registry key in an instance
variable. Each time the vocabulary is needed, this object will be called
(i.e. the *\_\_call\_\_()* method is invoked) with the context as an
argument, and is expected to return an appropriate vocabulary.

Named vocabularies
------------------

Context source binders are great for simple dynamic vocabularies. They
are also re-usable, since we can import the source from a single
location and use it in multiple instances. However, we may want to
provide an additional level of decoupling, by locating a vocabulary by
name, not necessarily caring where or how it is implemented.

Named vocabularies are similar to context source binders, but are
components registered as named utilities, referenced in the schema by
name only. This allows local overrides of the vocabulary via the
Component Architecture, and makes it easier to distribute vocabularies
in third party packages.

.. note::
    Named vocabularies cannot be parameterised in the way as we did
    with the context source binder above, since they are looked up by name
    only.

We can turn our first dynamic vocabulary into a named vocabulary by
creating a named utility providing *IVocabularyFactory*, like so:

::

    from zope.component import queryUtility

    from zope import schema
    from zope.interface import implementer
    from zope.schema.interfaces import IVocabularyFactory

    from zope.schema.vocabulary import SimpleVocabulary

    from plone.registry.interfaces import IRegistry

    @implementer
    class PizzasVocabulary(object):

        def __call__(self, context):
            registry = queryUtility(IRegistry)
            terms = []
            if registry is not None:
                for pizza in registry.get('example.dexterityforms.pizzaTypes', ()):
                    # create a term - the arguments are the value, the token, and
                    # the title (optional)
                    terms.append(SimpleVocabulary.createTerm(pizza, pizza.encode('utf-8'), pizza))
            return SimpleVocabulary(terms)
    grok.global_utility(PizzasVocabulary, name=u"example.dexterityforms.availablePizzas")

.. note::
    By convention, the vocabulary name is prefixed with the package name, to
    ensure uniqueness.

We can make use of this vocabulary in any schema by passing its name to
the *vocabulary* argument of the *Choice* field constructor:

::

    orderItems = schema.Set(
            title=_(u"Your order"),
            value_type=schema.Choice(vocabulary='example.dexterityforms.availablePizzas')
        )

As you might expect, there are a number of standard vocabularies that
come with Plone and third party packages, most of which are named
vocabularies. Many of these can be found in the *plone.app.vocabularies*
package, and add-ons such as *plone.principalsource*.

.. _documentation: https://pypi.python.org/pypi/plone.app.registry
