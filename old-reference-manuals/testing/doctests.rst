Telling stories with doctests
-----------------------------

.. admonition:: description

    Doctests bring code and test closer together, and makes it easier to describe what a test does, and why.

By their nature, tests should exercise an API and demonstrate how it is
used. Thus, for other developers trying to understand how a module or
library should be used, tests can be the best form of documentation.
Python supports the notion of **doctests**, otherwise known as
**executable documentation**.

Doctests look like Python interpreter sessions. They contain plain text
(normally in reStructedText, which can be rendered to HTML or PDF
easily) as well as **examples**. The idea is to show something that
could have been typed in an interpreter session and what the expected
outcome should be. In the Zope 3 world, doctests are extremely prevalent
and are used for most unit and integration testing.

Doctests come in two main flavours: You can write a simple text file,
such as a README.txt, that explains your code along with verifiable
examples, or you can add doctests for a given method or class into the
docstring of that method or class.

The full-file approach - sometimes known as **documentation-driven
development** - is the most common. This type of test is very well
suited for explaining how an API should be used and ensuring that it
works as expected at the same time. However, note that these are not
technically proper unit tests, because there is no guarantee of
isolation between the steps of the “script” that the doctest describes.
The docstring version uses the same basic syntax, but each docstring is
executed as its own test fixture, guaranteeing full isolation between
tests.

Here is a trivial example of a doctest. We will learn how to set up such
a test shortly.

::

    Interfaces are defined using Python class statements::

      >>> import zope.interface
      >>> class IFoo(zope.interface.Interface):
      ...    """Foo blah blah"""
      ...
      ...    x = zope.interface.Attribute("""X blah blah""")
      ...
      ...    def bar(q, r=None):
      ...        """bar blah blah"""

    In the example above, we've created an interface::

      >>> type(IFoo)
      <class 'zope.interface.interface.InterfaceClass'>

    We can ask for the interface's documentation::

      >>> IFoo.__doc__
      'Foo blah blah'

    We could create an arbitrary object - this will of course not provide
    the interface.

      >>> o = object()
      >>> o # doctest: +ELLIPSIS
      <object at ....>
      >>> IFoo.providedBy(o)
      False
      >>> o.bar() # doctest: +ELLIPSIS
      Traceback (most recent call last):
      ...
      AttributeError: 'object' object has no attribute 'bar'

Each time the doctest runner encounters a line starting with >>>, the
prompt of the Python interpreter (i.e. what you get by running python
without any arguments in a terminal), it will execute that line of code.
If that statement is then immediately followed by a line with the same
level of indentation as the >>> that is not a blank line and does not
start with >>>, this is taken to be the expected output of the
statement. The test runner will compare the output it got by executing
the Python statement with the output specified in the doctest, and flag
up an error if they don’t match.

Note that *not* writing an output value is equivalent to stating that
the method has no output. Thus, this is a failure:

::

        >>> foo = 'hello'
        >>> foo
        >>> # do something else

The reference to foo on its own will print the value of foo. The correct
DocTest would read:

::

        >>> foo = 'hello'
        >>> foo
        'hello'
        >>> # do something else

Notice also the … (ellipsis) element in the expected otuput. These mean
“any number of characters” (anologus to a .\* statement in a regular
expression, if you are familiar with those). They are usually convenient
shorthand, but they can sometimes be necessary. For example:

::

      >>> class Foo:
      ...     pass
      >>> Foo()
      <__main__.Foo instance at ...>

Here, the ... in the expected output replaces a hexadecimal memory address (0x0x4523a0 on
the author's computer at the time of writing), which cannot be predicted in advance. When
writing doctests in particular (but also when writing regular unit tests), you need to be
careful about values you cannot predict, such as auto-generated ids based on the current
time or a random number. The ellipsis operator can help you work around those.

Do not confuse the ellipsis operator in the expected output with the syntax of using ...
underneath a >>> line. This is the standard Python interpreter syntax used to designate
statments that run over multiple lines, normally as the result of indentation. You can,
for example, write:

::

      >>> if a == b:
      ...     foo = bar

if that is necessary in your test.

Doctest tips and tricks
~~~~~~~~~~~~~~~~~~~~~~~

As with all testing, you will get better at doctests over time. Below are a few tips that
may help you get started.

Read the documentation
    doctests have been in Python for a long time. The `doctest module <http://docs.python.org/2/library/doctest.html>`_
    comes with more documentation on how they work.
A test is just a bunch of python statements!
    Never forget this. You can, for example, reference helper methods in
    your own product, for example, imagine you have a method in
    Products.MyProduct.tests.utils that has a method setUpSite() to
    pre-populate your site with a few directories and users. Your
    doctest could contain:

    ::

          >>> from Products.MyProduct.tests.utils import setUpSite
          >>> setUpSite()

The test suite can perform additional initialisation
    A test suite can have setUp() and/or tearDown() handlers that
    perform additional set-up or clean-up. We will see further examples
    of this later.
PDB is still your friend
    You can put the standard import pdb; pdb.set\_trace() on a line in
    doctest. Unfortunately, you can’t step through a doctest line by
    line, but you can print variables and examine the state of the test
    fixture.
You can catch exceptions
    If you need to debug a doctest that is throwing an exception, this
    statement is often useful:

    ::

          >>> try:
          ...     someOperation()
          ... except:
          ...     import pdb; pdb.set_trace()
          >>> # continue as normal
